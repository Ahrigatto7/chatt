import streamlit as st
import pandas as pd
from datetime import datetime
from collections import OrderedDict
import os
import json

데이터 로딩 함수
@st.cache_data
def load_topic_db(filepath):
if os.path.exists(filepath):
return pd.read_csv(filepath).fillna('')
return None

@st.cache_data
def load_concepts(files):
combined_concepts = OrderedDict()
for file_path in files:
if os.path.exists(file_path):
try:
with open(file_path, 'r', encoding='utf-8') as f:
data = json.load(f)
for key, value in data.items():
if key not in combined_concepts:
combined_concepts[key] = value
except (FileNotFoundError, json.JSONDecodeError):
pass
return combined_concepts

계산 로직
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ELEMENT_MAP = {'甲':'목', '乙':'목', '丙':'화', '丁':'화', '戊':'토', '己':'토', '庚':'금', '辛':'금', '壬':'수', '癸':'수', '寅':'목', '卯':'목', '巳':'화', '午':'화', '辰':'토', '戌':'토', '丑':'토', '未':'토', '申':'금', '酉':'금', '子':'수', '亥':'수'}
SOLAR_TERMS_INFO = {1: {'name': '소한', 'day': 5}, 2: {'name': '입춘', 'day': 4}, 3: {'name': '경칩', 'day': 5}, 4: {'name': '청명', 'day': 4}, 5: {'name': '입하', 'day': 5}, 6: {'name': '망종', 'day': 5}, 7: {'name': '소서', 'day': 7}, 8: {'name': '입추', 'day': 7}, 9: {'name': '백로', 'day': 7}, 10: {'name': '한로', 'day': 8}, 11: {'name': '입동', 'day': 7}, 12: {'name': '대설', 'day': 7}}

def get_ganji_from_cycle(cycle_index):
return HEAVENLY_STEMS[cycle_index % 10] + EARTHLY_BRANCHES[cycle_index % 12]

def get_saju_pillars(birth_dt):
year, month, day, hour = birth_dt.year, birth_dt.month, birth_dt.day, birth_dt.hour
ipchun_day = 4
year_for_ganji = year if not (month == 1 or (month == 2 and day &lt; ipchun_day)) else year - 1
year_cycle = (year_for_ganji - 1864) % 60
year_pillar = get_ganji_from_cycle(year_cycle)
term_day = SOLAR_TERMS_INFO[month]['day']
month_for_ganji = month if day >= term_day else (month - 1 if month > 1 else 12)
year_stem_char = year_pillar[0]
month_stem_start_map = {"甲己": 2, "乙庚": 4, "丙辛": 6, "丁壬": 8, "戊癸": 0}
for k, v in month_stem_start_map.items():
if year_stem_char in k: month_stem_start = v
month_stem_index = (month_stem_start + month_for_ganji - 1) % 10
month_branch_index = (month_for_ganji + 1) % 12
month_pillar = HEAVENLY_STEMS[month_stem_index] + EARTHLY_BRANCHES[month_branch_index]
delta_days = (birth_dt.date() - datetime(1900, 1, 1).date()).days
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

def analyze_suam_force(pillars):
scores = {'목화': 0, '금수': 0}
for char in "".join(pillars.values()):
element = ELEMENT_MAP.get(char)
if element in ['목', '화']: scores['목화'] += 1
elif element in ['금', '수']: scores['금수'] += 1
if scores['목화'] > scores['금수']: return "목화(木火)세력", "목화", scores
elif scores['금수'] > scores['목화']: return "금수(金水)세력", "금수", scores
else: return "세력 균형", "균형", scores

def analyze_che_yong(pillars, force_keyword):
if force_keyword == "균형": return None, None
che_elements = ['목', '화'] if force_keyword == "목화" else ['금', '수']
yong_elements = ['금', '수'] if force_keyword == "목화" else ['목', '화']
che_chars, yong_chars = [], []
for char in list("".join(pillars.values())):
element = ELEMENT_MAP.get(char)
if element in che_elements: che_chars.append(char)
elif element in yong_elements: yong_chars.append(char)
return che_chars, yong_chars

def analyze_suppression_structure(che_chars, yong_chars):
if not che_chars or not yong_chars: return "세력이 한쪽으로 치우쳐 제압구조를 논하기 어렵습니다."
if len(che_chars) >= 6 and len(yong_chars) &lt;= 2: return "나의 세력(체)이 상대 세력(용)을 포위하여 제압하는 **적포구조(賊捕構造)**의 형태일 가능성이 높습니다."
elif len(che_chars) > len(yong_chars): return "나의 세력(체)이 상대 세력(용)을 제압하는 일반 제압구조의 형태입니다."
else: return "상대 세력(용)이 강하여 제압의 효율이 낮은 구조일 수 있습니다."

Streamlit UI
st.set_page_config(page_title="수암명리 분석기", layout="wide")
st.title("🔬 수암명리학 학습 및 분석기")

topic_df = load_topic_db('Topic DB 216b50e66dba805abdb2ebd9cbd601da.csv')
JSON_FILES = ['concepts_from_doc.json', '록(祿)과 원신(原身)의 개념 및 사주 적용 사례.json']
concept_db = load_concepts(JSON_FILES)

with st.form("saju_input_form"):
col1, col2, col3 = st.columns(3)
with col1: st.date_input("🗓️ 생년월일", value=datetime(2000, 1, 1), key="birth_date")
with col2: st.time_input("⏰ 태어난 시각", value=datetime(2000, 1, 1, 12, 0).time(), key="birth_time")
with col3: st.radio("🚻 성별", ("남자", "여자"), horizontal=True, key="gender")
submitted = st.form_submit_button("분석 시작하기", use_container_width=True, type="primary")

if submitted:
birth_datetime = datetime.combine(st.session_state.birth_date, st.session_state.birth_time)
pillars = get_saju_pillars(birth_datetime)

st.markdown("---")
st.subheader("📝 사주 원국")
p_cols = st.columns(4)
for i, (name, val) in enumerate(reversed(list(pillars.items()))):
    p_cols[i].metric(label=name, value=val)

st.markdown("---")
st.subheader("🤖 수리 분석 어시스턴트")

with st.container(border=True):
    st.markdown("#### 1단계: 세력 분석")
    force_text, force_keyword, scores = analyze_suam_force(pillars)
    st.info(f"**분석 결과:** 목화세 {scores['목화']}개, 금수세 {scores['금수']}개로, **{force_text}**")
    if st.button("'제압방식' 이론 보기", key="force_theory"):
        if concept_db and "제압방식" in concept_db:
            st.markdown(concept_db["제압방식"].get("정의", "관련 이론 없음"))

with st.container(border=True):
    st.markdown("#### 2단계: 체용(體用) 구분")
    che_chars, yong_chars = analyze_che_yong(pillars, force_keyword)
    if che_chars:
        st.info(f"- **나의 주체 (체 體):** {', '.join(che_chars)} ({len(che_chars)}개)\n- **나의 쓰임 (용 用):** {', '.join(yong_chars)} ({len(yong_chars)}개)")
    else:
        st.warning("세력이 균형을 이루어 체용 구분이 무의미합니다.")
    if st.button("'체용' 이론 보기", key="cheyong_theory"):
         if concept_db and "해설" in concept_db:
             st.markdown(concept_db["해설"].get("정의", "관련 이론 없음"))

with st.container(border=True):
    st.markdown("#### 3단계: 제압구조 분석")
    structure_result = analyze_suppression_structure(che_chars, yong_chars)
    st.info(f"**분석 결과:** {structure_result}")
    if st.button("'적포구조' 등 이론 보기", key="structure_theory"):
        if topic_df is not None:
            result_df = topic_df[topic_df['Name'].str.contains("제압방식", na=False)]
            if not result_df.empty:
                st.markdown(result_df.iloc[0]['Description'])