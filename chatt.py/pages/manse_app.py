import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from collections import OrderedDict

# --- 데이터 로딩 함수 (이전과 동일) ---
@st.cache_data
def load_topic_db(filepath):
    try:
        df = pd.read_csv(filepath)
        return df.fillna('')
    except FileNotFoundError:
        return None

# --- 사주 계산 로직 (십신, 오행, 음양 맵 포함) ---
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ELEMENT_MAP = {'甲':'목', '乙':'목', '丙':'화', '丁':'화', '戊':'토', '己':'토', '庚':'금', '辛':'금', '壬':'수', '癸':'수', '寅':'목', '卯':'목', '巳':'화', '午':'화', '辰':'토', '戌':'토', '丑':'토', '未':'토', '申':'금', '酉':'금', '子':'수', '亥':'수'}
YIN_YANG_MAP = {'甲':'양', '丙':'양', '戊':'양', '庚':'양', '壬':'양', '乙':'음', '丁':'음', '己':'음', '辛':'음', '癸':'음', '子':'양', '寅':'양', '辰':'양', '午':'양', '申':'양', '戌':'양', '亥':'음', '卯':'음', '巳':'음', '未':'음', '酉':'음', '丑':'음'}
SOLAR_TERMS_INFO = {
    1: {'name': '소한', 'day': 5}, 2: {'name': '입춘', 'day': 4}, 3: {'name': '경칩', 'day': 5}, 4: {'name': '청명', 'day': 4},
    5: {'name': '입하', 'day': 5}, 6: {'name': '망종', 'day': 5}, 7: {'name': '소서', 'day': 7}, 8: {'name': '입추', 'day': 7},
    9: {'name': '백로', 'day': 7}, 10: {'name': '한로', 'day': 8}, 11: {'name': '입동', 'day': 7}, 12: {'name': '대설', 'day': 7}
}

def get_sipsin_char(day_elem, day_yy, target_char):
    target_elem = ELEMENT_MAP[target_char]
    target_yy = YIN_YANG_MAP[target_char]
    sipsin_logic = {'목': {'목': ('비견', '겁재'), '화': ('식신', '상관'), '토': ('편재', '정재'), '금': ('편관', '정관'), '수': ('편인', '정인')},'화': {'화': ('비견', '겁재'), '토': ('식신', '상관'), '금': ('편재', '정재'), '수': ('편관', '정관'), '목': ('편인', '정인')},'토': {'토': ('비견', '겁재'), '금': ('식신', '상관'), '수': ('편재', '정재'), '목': ('편관', '정관'), '화': ('편인', '정인')},'금': {'금': ('비견', '겁재'), '수': ('식신', '상관'), '목': ('편재', '정재'), '화': ('편관', '정관'), '토': ('편인', '정인')},'수': {'수': ('비견', '겁재'), '목': ('식신', '상관'), '화': ('편재', '정재'), '금': ('편인', '정인'), '목': ('편관', '정관'),}}
    sipsin_pair = sipsin_logic.get(day_elem, {}).get(target_elem)
    if not sipsin_pair: return "알수없음"
    yin_yang_index = 0 if day_yy == target_yy else 1
    if day_elem == target_elem: yin_yang_index = 0 if day_yy == target_yy else 1
    return sipsin_pair[yin_yang_index]

def calculate_sipsin_for_pillars(pillars):
    day_stem = pillars['일주'][0]
    day_element = ELEMENT_MAP[day_stem]
    day_yinyang = YIN_YANG_MAP[day_stem]
    sipsin_pillars = OrderedDict()
    for pillar_name, ganji in pillars.items():
        gan, ji = ganji[0], ganji[1]
        sipsin_gan = get_sipsin_char(day_element, day_yinyang, gan)
        sipsin_ji = get_sipsin_char(day_element, day_yinyang, ji)
        sipsin_pillars[pillar_name] = (sipsin_gan, sipsin_ji)
    return sipsin_pillars

def get_ganji_from_cycle(cycle_index):
    return HEAVENLY_STEMS[cycle_index % 10] + EARTHLY_BRANCHES[cycle_index % 12]

def get_saju_pillars(birth_dt):
    year, month, day, hour = birth_dt.year, birth_dt.month, birth_dt.day, birth_dt.hour
    is_after_term = day >= SOLAR_TERMS_INFO[month]['day']
    current_month_for_calc = month if is_after_term else month - 1 if month > 1 else 12
    current_year_for_calc = year if is_after_term or month > 1 else year -1
    
    year_cycle = (current_year_for_calc - 1864) % 60
    year_pillar = get_ganji_from_cycle(year_cycle)
    
    year_stem_char = year_pillar[0]
    month_stem_start_map = {"甲己": 2, "乙庚": 4, "丙辛": 6, "丁壬": 8, "戊癸": 0}
    for k, v in month_stem_start_map.items():
        if year_stem_char in k: month_stem_start = v
    month_stem_index = (month_stem_start + current_month_for_calc -1) % 10
    month_branch_index = (current_month_for_calc + 1) % 12
    month_pillar = HEAVENLY_STEMS[month_stem_index] + EARTHLY_BRANCHES[month_branch_index]

    start_dt = datetime(1900, 1, 1)
    delta_days = (birth_dt.replace(hour=0, minute=0, second=0, microsecond=0) - start_dt).days
    day_cycle = (delta_days + 46) % 60
    day_pillar = get_ganji_from_cycle(day_cycle)

    day_stem_char = day_pillar[0]
    hour_stem_start_map = {"甲己": 0, "乙庚": 2, "丙辛": 4, "丁壬": 6, "戊癸": 8}
    for k, v in hour_stem_start_map.items():
        if day_stem_char in k: hour_stem_start = v
    hour_index = (hour + 1) // 2 % 12
    hour_stem_index = (hour_stem_start + hour_index) % 10
    hour_pillar = HEAVENLY_STEMS[hour_stem_index] + EARTHLY_BRANCHES[hour_index]
    
    return OrderedDict([("년주", year_pillar), ("월주", month_pillar), ("일주", day_pillar), ("시주", hour_pillar)])

# --- NEW: 대운 계산 로직 ---
def calculate_daewoon(birth_dt, gender, pillars):
    year_pillar = pillars["년주"]
    month_pillar = pillars["월주"]
    
    year_gan = year_pillar[0]
    is_yang_year = YIN_YANG_MAP[year_gan] == '양'
    
    # 순행/역행 결정
    is_forward = (gender == '남자' and is_yang_year) or \
                 (gender == '여자' and not is_yang_year)

    # 대운수 계산
    current_month = birth_dt.month if birth_dt.day >= SOLAR_TERMS_INFO[birth_dt.month]['day'] else birth_dt.month-1 or 12
    
    if is_forward:
        next_term_month = current_month % 12 + 1
        next_term_year = birth_dt.year if next_term_month > current_month else birth_dt.year + 1
        term_day = SOLAR_TERMS_INFO[next_term_month]['day']
        term_dt = datetime(next_term_year, next_term_month, term_day)
        diff_days = (term_dt - birth_dt).days
    else: # 역행
        prev_term_month = current_month
        prev_term_year = birth_dt.year
        term_day = SOLAR_TERMS_INFO[prev_term_month]['day']
        term_dt = datetime(prev_term_year, prev_term_month, term_day)
        diff_days = (birth_dt - term_dt).days
        
    daewoon_num = round(diff_days / 3)
    if daewoon_num == 0: daewoon_num = 1
    
    # 대운 간지 리스트 생성
    all_ganji = [get_ganji_from_cycle(i) for i in range(60)]
    month_pillar_index = all_ganji.index(month_pillar)
    
    daewoon_ganji_list = []
    direction = 1 if is_forward else -1
    for i in range(1, 10): # 9개의 대운
        next_index = (month_pillar_index + i * direction) % 60
        daewoon_ganji_list.append(all_ganji[next_index])
        
    return daewoon_num, daewoon_ganji_list

# --- Streamlit UI 부분 ---
st.set_page_config(page_title="만세력 분석", layout="wide")
st.title("⚖️ 만세력 분석 및 학습")
st.markdown("생년월일시를 입력하여 사주팔자와 십신, 대운을 확인하고 관련 이론을 학습합니다.")
topic_df = load_topic_db('Topic DB 216b50e66dba805abdb2ebd9cbd601da.csv')

with st.form("saju_input_form"):
    # (입력 UI 이전과 동일)
    col1, col2, col3 = st.columns(3)
    with col1:
        birth_date = st.date_input("🗓️ 생년월일", value=datetime(2000, 1, 1))
    with col2:
        birth_time = st.time_input("⏰ 태어난 시각", value=datetime(2000, 1, 1, 12, 0).time())
    with col3:
        gender = st.radio("🚻 성별", ("남자", "여자"), horizontal=True)
    submitted = st.form_submit_button("만세력 확인하기", use_container_width=True, type="primary")

if submitted:
    birth_datetime = datetime.combine(birth_date, birth_time)
    st.markdown("---")
    st.subheader("📊 사주팔자 분석 결과")

    try:
        pillars = get_saju_pillars(birth_datetime)
        sipsin_results = calculate_sipsin_for_pillars(pillars)
        daewoon_num, daewoon_ganji = calculate_daewoon(birth_datetime, gender, pillars)

        # 사주팔자와 십신 표시 (이전과 동일)
        p_col4, p_col3, p_col2, p_col1 = st.columns(4)
        for i, (name, val) in enumerate(reversed(list(pillars.items()))):
            with [p_col1, p_col2, p_col3, p_col4][i]: st.metric(label=name, value=val)
        
        s_col4, s_col3, s_col2, s_col1 = st.columns(4)
        for i, (name, val) in enumerate(reversed(list(sipsin_results.items()))):
             with [s_col1, s_col2, s_col3, s_col4][i]:
                st.markdown(f"<div style='text-align: center; font-size: 1.1em; color: #6E7A8A;'>{val[0]}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align: center; font-size: 1.1em; color: #6E7A8A;'>{val[1]}</div>", unsafe_allow_html=True)

        st.info(f"**일간(日干)은 '{pillars['일주'][0]}' 입니다.** 이 사주의 주인공(나 자신)을 나타냅니다.")

        # --- NEW: 대운 흐름 표시 ---
        st.markdown("---")
        st.subheader(f"📈 대운의 흐름 (대운수: {daewoon_num}세)")
        daewoon_data = []
        for i, ganji in enumerate(daewoon_ganji):
            age_start = daewoon_num + i * 10
            age_end = age_start + 9
            sipsin_gan = get_sipsin_char(pillars['일주'][0], YIN_YANG_MAP[pillars['일주'][0]], ganji[0])
            daewoon_data.append({
                "나이": f"{age_start}세 ~ {age_end}세",
                "대운": ganji,
                "십신": sipsin_gan
            })
        st.dataframe(pd.DataFrame(daewoon_data), use_container_width=True)

        # 십신 상세 해설 (이전과 동일)
        st.markdown("---")
        st.subheader("📚 십신(十神) 상세 해설")
        if topic_df is not None:
            unique_sipsins = set(s for p in sipsin_results.values() for s in p)
            for sipsin_name in sorted(list(unique_sipsins)):
                result_df = topic_df[topic_df['Name'] == sipsin_name]
                if not result_df.empty:
                    row = result_df.iloc[0]
                    with st.expander(f"**'{sipsin_name}'에 대한 해설 보기**"):
                        st.markdown(f"#### 💬 설명\n{row.get('Description', '내용 없음')}")
                        st.markdown(f"#### 🔑 관련 키워드\n> {row.get('Related Keywords', '내용 없음')}")
                else:
                    st.warning(f"'{sipsin_name}'에 대한 해설 정보를 지식 DB에서 찾을 수 없습니다.")
        else:
             st.error("지식 데이터베이스(Topic DB.csv)를 불러올 수 없습니다.")

    except Exception as e:
        st.error(f"계산 중 오류가 발생했습니다: {e}")