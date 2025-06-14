import streamlit as st
from modules import file_handler, chatbot_ai

st.set_page_config(page_title="챗봇 문서 분석", layout="wide")
st.title("📝 챗봇 기반 문서 분석")

text = st.session_state.get("uploaded_text")
if text:
    st.info("홈 페이지에서 업로드한 문서를 사용합니다.")
else:
    uploaded_file = st.file_uploader(
        "분석할 문서 업로드 (.docx / .md / .txt)", type=["docx", "md", "txt"]
    )
    if uploaded_file:
        text = file_handler.extract_text(uploaded_file)
        st.session_state["uploaded_text"] = text

if text:
    st.success("문서가 로드되었습니다. 질문을 입력해 보세요.")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    question = st.text_input("질문 입력")
    if st.button("질문하기") and question:
        answer = chatbot_ai.ask_document_question(text, question)
        st.session_state.chat_history.append((question, answer))

    for q, a in st.session_state.chat_history:
        st.write(f"**Q:** {q}")
        st.write(f"**A:** {a}")
else:
    st.warning("문서를 업로드하세요.")

