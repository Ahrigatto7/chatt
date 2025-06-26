import streamlit as st
from modules import file_handler
import re

st.set_page_config(page_title="AI 문서 대화", layout="wide")
st.title("🤖 AI 문서 대화")
st.markdown("문서를 업로드하고, 내용에 대해 AI에게 질문하여 답변을 얻으세요.")
st.markdown("---")

# --- 세션 상태 초기화 ---
# 'documents'는 파일 내용 저장, 'messages'는 채팅 기록 저장
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- 사이드바: 파일 업로드 ---
with st.sidebar:
    st.header("1. 문서 업로드")
    uploaded_files = st.file_uploader(
        "대화할 문서들을 업로드하세요.",
        type=["pdf", "docx", "md", "txt"],
        accept_multiple_files=True
    )
    if st.button("문서 처리 시작"):
        st.session_state.documents = [] # 새로 시작할 때마다 초기화
        st.session_state.messages = [] # 채팅 기록도 초기화
        with st.spinner("파일을 읽고 AI가 학습할 준비를 합니다..."):
            for file in uploaded_files:
                try:
                    text = file_handler.extract_text(file)
                    st.session_state.documents.append({'name': file.name, 'text': text})
                except Exception as e:
                    st.error(f"'{file.name}' 처리 중 오류: {e}")
        st.success(f"{len(st.session_state.documents)}개의 문서가 성공적으로 처리되었습니다.")

# --- 메인 화면: 채팅 인터페이스 ---

st.header("2. AI와 대화하기")

# 이전 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 질문 입력
if prompt := st.chat_input("문서 내용에 대해 질문해보세요..."):
    # 사용자 메시지 기록 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 답변 생성
    with st.chat_message("ai"):
        if not st.session_state.documents:
            st.warning("먼저 사이드바에서 문서를 업로드하고 '문서 처리 시작' 버튼을 눌러주세요.")
        else:
            with st.spinner("AI가 문서를 기반으로 답변을 생각하는 중입니다..."):
                # 1단계: 정보 검색 (Retrieval)
                # 업로드된 모든 문서에서 질문과 관련된 문단 찾기
                context_snippets = []
                for doc in st.session_state.documents:
                    # 간단한 키워드 기반 검색 (질문의 주요 단어)
                    keywords = re.findall(r'\b\w+\b', prompt)
                    for keyword in keywords:
                        if len(keyword) > 1: # 한 글자 단어는 제외
                            for para in doc['text'].split('\n\n'):
                                if keyword.lower() in para.lower():
                                    context_snippets.append(f"[{doc['name']}에서 발췌]\n{para}")
                
                # 중복 제거
                context_snippets = list(dict.fromkeys(context_snippets))
                
                if not context_snippets:
                    response = "죄송합니다, 업로드하신 문서에서 질문과 관련된 정보를 찾을 수 없습니다. 더 일반적인 키워드로 질문해보시겠어요?"
                else:
                    # 2단계: 답변 생성 (Generation) - 이 부분은 제가 직접 수행합니다.
                    # 다음 턴에 제가 답변을 생성할 수 있도록, 검색된 내용을 준비하라는 메시지를 출력합니다.
                    response = (
                        "관련 정보를 찾았습니다. 이 정보를 바탕으로 답변을 생성하려면, "
                        "**아래 '관련 문단' 내용을 포함하여 저에게 다시 한번 질문**해주시겠어요?\n\n"
                        "그러면 제가 그 내용을 요약하고 정리해서 답변을 드릴게요.\n\n"
                        "--- \n"
                        "**[관련 문단]**\n"
                        + "\n\n---\n\n".join(context_snippets[:3]) # 너무 길지 않게 최대 3개 문단만 표시
                    )

                st.markdown(response)
                st.session_state.messages.append({"role": "ai", "content": response})