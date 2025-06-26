
import streamlit as st
import pandas as pd
from io import BytesIO
import base64


# ✅ 자동 해석 함수 정의
def auto_interpret(격국, 제압수단):
    summary = []
    if "食神生財格" in 격국:
        if any(x in 제압수단 for x in ["火", "木", "卯", "巳"]):
            summary.append("→ 식신생재격 + 火/卯 구조 → 자영업, 유통, 창의 업종 적합.")
        else:
            summary.append("→ 식신생재격이나 재성 흐름 약할 수 있음.")
    if "比劫" in 제압수단:
        summary.append("→ 비겁이 강하면 재성 통제, 부부 갈등 가능성.")
    if not summary:
        summary.append("→ 등록된 격국/제압수단 조합 해석 없음.")
    return "\n".join(summary)


st.set_page_config(page_title="Suri 사례 분석기", layout="centered")

# 저장 파일
LOG_FILE = "saved_cases.csv"

# 초기 로딩
try:
    log_df = pd.read_csv(LOG_FILE)
except FileNotFoundError:
    log_df = pd.DataFrame(columns=["사례번호", "제목", "사주원국", "격국", "제압수단", "직업", "육친해석", "운세흐름"])

st.title("📘 Suri 사례 분석기")

with st.expander("📂 기존 기록 보기", expanded=True):
    if log_df.empty:
        st.info("기록된 사례가 없습니다.")
    else:
        st.dataframe(log_df)

st.markdown("---")
st.header("🆕 새 사례 추가")

with st.form("new_case_form"):
    사례번호 = st.text_input("사례번호")
    제목 = st.text_input("제목")
    사주원국 = st.text_input("사주 원국 (천간/지지)")
    격국 = st.text_input("격국")
    제압수단 = st.text_input("제압 수단")
    직업 = st.text_area("직업 해석")
    육친해석 = st.text_area("육친 해석")
    운세흐름 = st.text_area("운세 흐름")
    submitted = st.form_submit_button("사례 저장")

if submitted:
    new_row = pd.DataFrame([{
        "사례번호": 사례번호,
        "제목": 제목,
        "사주원국": 사주원국,
        "격국": 격국,
        "제압수단": 제압수단,
        "직업": 직업,
        "육친해석": 육친해석,
        "운세흐름": 운세흐름
    }])
    log_df = pd.concat([log_df, new_row], ignore_index=True)
    log_df.to_csv(LOG_FILE, index=False)
    st.success(f"✅ 사례 {사례번호} 저장 완료!")
        st.markdown("### 🔍 자동 해석")
        st.markdown(auto_interpret(격국, 제압수단))


st.markdown("---")
st.header("📥 저장된 사례 백업")
csv = log_df.to_csv(index=False).encode("utf-8-sig")
st.download_button("⬇️ 사례 전체 백업 (CSV)", data=csv, file_name="saved_cases.csv", mime="text/csv")
