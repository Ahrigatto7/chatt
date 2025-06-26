import streamlit as st
from modules import file_handler, keyword_analyzer, rule_extractor, storage, database
import pandas as pd
import os
import json

CSV_PATH = 'Topic DB 216b50e66dba805abdb2ebd9cbd601da.csv'

def load_db_for_editing(filepath):
    expected_columns = ['Name', 'Description', 'Related Keywords', 'Related Examples']
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame(columns=expected_columns)

st.set_page_config(page_title="문서 분석기", layout="wide")
st.title("📖 문서 분석기")
st.markdown("`.docx`, `.md`, `.txt` 형식의 문서를 업로드하면, 핵심 키워드와 해석 규칙을 추출합니다.")

uploaded_file = st.file_uploader("📂 분석할 문서 업로드", type=["docx", "md", "txt"])

if uploaded_file:
    st.success(f"✅ **{uploaded_file.name}** 문서 업로드 완료!")

    text = file_handler.extract_text(uploaded_file)
    rules = rule_extractor.extract_interpretive_rules(text)
    extracted, keywords = keyword_analyzer.extract_sections(text)
    summary_df, keyword_map = keyword_analyzer.analyze_keywords(extracted, keywords)

    tab1, tab2 = st.tabs(["🔍 키워드 분석", "📑 해석 규칙"])
    with tab1:
        st.subheader("혼인 관련 키워드 분석")
        if not summary_df.empty:
            st.dataframe(summary_df, use_container_width=True)
        else:
            st.warning("관련된 키워드가 발견되지 않았습니다.")
    with tab2:
        st.subheader("사주 해석 규칙 추출")
        if rules:
            st.json(rules)
        else:
            st.warning("해석 규칙이 추출되지 않았습니다.")
    
    st.markdown("---")

    with st.expander("🧠 분석 결과를 지식 DB에 추가하기"):
        st.markdown("방금 분석한 내용을 새로운 토픽으로 만들어 지식 DB에 영구적으로 저장할 수 있습니다.")
        with st.form("upload_to_db_form"):
            default_description = json.dumps(rules, ensure_ascii=False, indent=2)
            default_examples = "\n\n".join([f"### {kw}\n" + "\n---\n".join(texts) for kw, texts in keyword_map.items()])
            default_keywords = ", ".join(keyword_map.keys())
            st.info("아래 내용은 분석 결과로 자동 완성되었습니다. 자유롭게 수정하여 저장하세요.")
            topic_name = st.text_input("새 토픽 이름 (Name)", placeholder="예: 혼인과 관련된 새로운 규칙")
            description = st.text_area("설명 (Description)", value=default_description, height=200)
            related_keywords = st.text_input("관련 키워드 (Related Keywords)", value=default_keywords)
            related_examples = st.text_area("관련 사례 (Related Examples)", value=default_examples, height=200)

            if st.form_submit_button("지식 DB에 업로드"):
                if topic_name:
                    df = load_db_for_editing(CSV_PATH)
                    if not df['Name'].str.contains(topic_name).any():
                        new_row = pd.DataFrame([{'Name': topic_name, 'Description': description, 'Related Keywords': related_keywords, 'Related Examples': related_examples}])
                        df = pd.concat([df, new_row], ignore_index=True)
                        df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
                        st.success(f"'{topic_name}' 토픽이 지식 DB에 성공적으로 추가되었습니다!")
                    else:
                        st.error(f"'{topic_name}'은(는) 이미 존재하는 토픽 이름입니다. 다른 이름을 사용해주세요.")
                else:
                    st.warning("새 토픽 이름은 반드시 입력해야 합니다.")