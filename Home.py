import streamlit as st
from modules import file_handler, keyword_analyzer, rule_extractor, storage, database

st.set_page_config(page_title="분석기", layout="wide")
st.title("📘 분석기")

uploaded_file = st.file_uploader("📂 분석할 문서 업로드 (.docx / .md / .txt)", type=["docx", "md", "txt"])

if uploaded_file:
    st.success("✅ 문서 업로드 완료")

    # 1. 텍스트 추출
    text = file_handler.extract_text(uploaded_file)

    # 2. 키워드 기반 문단 추출
    st.subheader("🔍 관련 키워드 분석")
    extracted, keywords = keyword_analyzer.extract_sections(text)
    summary_df, keyword_map = keyword_analyzer.analyze_keywords(extracted, keywords)

    if not summary_df.empty:
        st.dataframe(summary_df)
    else:
        st.warning("키워드와 관련된 문장이 발견되지 않았습니다.")

    # 3. 해석 규칙 추출
    st.subheader("📑 해석 규칙 추출")
    rules = rule_extractor.extract_interpretive_rules(text)

    if rules:
        st.json(rules)
    else:
        st.warning("해석 규칙이 추출되지 않았습니다.")

    # 4. 결과 저장 옵션
    st.subheader("💾 결과 저장")
    col1, col2 = st.columns(2)
    with col1:
        filename = st.text_input("저장할 파일명 (확장자 제외)", "분석결과")
    with col2:
        fmt = st.selectbox("파일 형식", ["Markdown (.md)", "JSON (.json)", "Excel (.xlsx)"])

    if st.button("📁 저장하기"):
        if fmt.endswith(".md"):
            content = rule_extractor.format_rules_to_markdown(rules)
            storage.save_text(content, filename + ".md")
        elif fmt.endswith(".json"):
            storage.save_json(rules, filename + ".json")
        elif fmt.endswith(".xlsx"):
            storage.save_excel(summary_df, keyword_map, filename + ".xlsx")
        st.success(f"{filename}{fmt[-4:]} 저장 완료!")

    # 5. DB 저장 버튼
    st.subheader("🧩 결과 DB 저장")
    if st.button("🗃️ DB에 저장하기"):
        database.init_db()
        database.save_rules_to_db(rules)
        database.save_keywords_to_db(keyword_map)
        st.success("✅ SQLite DB에 저장 완료 (saju_analysis.db)")
