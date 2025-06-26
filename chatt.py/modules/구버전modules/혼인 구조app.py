
import streamlit as st

# 제목
st.title("수암명리 혼인 구조 분석기")

# 성별 선택
gender = st.radio("성별을 선택하세요:", ("남", "여"))

# 일간 입력
ilgan = st.selectbox("일간을 선택하세요:", ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"])

# 8자 입력
st.subheader("사주 8자 입력 (천간 / 지지)")
col1, col2 = st.columns(2)
with col1:
    cheongan = [st.text_input(f"{i+1}번째 천간") for i in range(4)]
with col2:
    jiji = [st.text_input(f"{i+1}번째 지지") for i in range(4)]

# 결과 분석 버튼
if st.button("혼인 구조 분석"):
    spouse_star_table = {
        '甲': {'재': '己', '관': '庚'},
        '乙': {'재': '戊', '관': '辛'},
        '丙': {'재': '庚', '관': '癸'},
        '丁': {'재': '辛', '관': '壬'},
        '戊': {'재': '壬', '관': '乙'},
        '己': {'재': '癸', '관': '甲'},
        '庚': {'재': '乙', '관': '丙'},
        '辛': {'재': '甲', '관': '丁'},
        '壬': {'재': '丙', '관': '己'},
        '癸': {'재': '丁', '관': '庚'}
    }

    spouse_star = spouse_star_table[ilgan]['재'] if gender == '남' else spouse_star_table[ilgan]['관']
    spouse_exists = spouse_star in cheongan + jiji

    # 일지 = 제3지지
    ilji = jiji[2] if len(jiji) >= 3 else ""

    result = f"배우자성 ({spouse_star}) {'존재함' if spouse_exists else '존재하지 않음'}\n"

    if spouse_exists:
        result += "→ 배우자성이 존재하므로 일반적인 혼인 구조로 분석됩니다."
    else:
        result += "→ 배우자성이 명확히 존재하지 않으므로 다음을 추가로 검토해야 합니다:\n"
        result += "- 식상 또는 원신의 존재 여부\n"
        result += "- 배우자궁(일지)에 타성의 입궁 여부\n"
        result += "- 대운/세운에서 성이 도달할 가능성"

    st.success(result)
