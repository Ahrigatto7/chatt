import streamlit as st
import json
from collections import OrderedDict
import os

st.set_page_config(page_title="개념 사전", layout="wide")
st.title("📕 개념 사전")
st.markdown("주요 개념들의 정의와 사례를 찾아봅니다.")

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

JSON_FILES = ['concepts_from_doc.json', '록(祿)과 원신(原身)의 개념 및 사주 적용 사례.json']
concepts = load_concepts(JSON_FILES)

if not concepts:
    st.error("표시할 개념 데이터가 없습니다. JSON 파일들을 확인해주세요.")
else:
    concept_names = [""] + list(concepts.keys())
    selected_concept = st.selectbox("알고 싶은 개념을 선택하세요.", options=concept_names)
    st.markdown("---")

    if selected_concept:
        concept_data = concepts[selected_concept]
        st.subheader("📖 정의")
        definition = concept_data.get("정의", "정의 정보가 없습니다.")
        st.markdown(definition)
        st.markdown("---")
        st.subheader("💡 사례")
        examples = concept_data.get("사례", {})
        if examples:
            for title, content in examples.items():
                with st.expander(f"**{title}**"):
                    if isinstance(content, dict):
                        st.markdown(f"**사주:** {content.get('사주', '정보 없음')}")
                        st.markdown(f"**설명:**\n\n {content.get('설명', '정보 없음')}")
                    else:
                        st.markdown(str(content))
        else:
            st.info("이 개념에 대한 구체적인 사례 정보가 없습니다.")