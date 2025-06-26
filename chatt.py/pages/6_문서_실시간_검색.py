import streamlit as st
from modules import file_handler
import re
import urllib.parse

st.set_page_config(page_title="실시간 문서 검색", layout="wide")
st.title("🔍 실시간 문서 검색기")
st.markdown("가지고 계신 PDF, TXT 등 원본 문서를 직접 업로드하여 내용을 검색합니다.")
st.markdown("---")

if 'document_text_map' not in st.session_state:
    st.session_state.document_text_map = {}

uploaded_files = st.file_uploader(
    "📂 검색할 문서들을 업로드하세요. (여러 파일 선택 가능)",
    type=["pdf", "docx", "md", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    new_files_processed = False
    with st.spinner("파일을 읽고 텍스트를 추출하는 중입니다..."):
        for file in uploaded_files:
            if file.name not in st.session_state.document_text_map:
                try:
                    extracted_text = file_handler.extract_text(file)
                    st.session_state.document_text_map[file.name] = extracted_text
                    new_files_processed = True
                except Exception as e:
                    st.error(f"'{file.name}' 파일 처리 중 오류 발생: {e}")
    if new_files_processed:
        st.success(f"{len(uploaded_files)}개의 문서가 검색 대상으로 준비되었습니다.")

if st.session_state.document_text_map:
    with st.expander("현재 로드된 문서 목록 보기"):
        for doc_name in st.session_state.document_text_map.keys():
            st.write(f"- {doc_name}")

    st.markdown("---")
    query = st.text_input("💡 문서 내용에서 찾고 싶은 키워드를 입력하세요.", placeholder="예: '적포구조', '관인상생'")

    if query:
        st.subheader(f"'{query}'에 대한 검색 결과")
        found_results = False
        for doc_name, text in st.session_state.document_text_map.items():
            results_in_doc = []
            paragraphs = text.split('\n\n')
            for i, para in enumerate(paragraphs):
                if query.lower() in para.lower():
                    results_in_doc.append(para)
            
            if results_in_doc:
                found_results = True
                with st.container(border=True):
                    st.markdown(f"#### 📄 문서: {doc_name}")
                    for para in results_in_doc:
                        highlighted_para = re.sub(f'({re.escape(query)})', r'**\1**', para, flags=re.IGNORECASE)
                        st.markdown(f"> {highlighted_para}")
                        
                        # --- NEW: session_state를 사용하는 버튼 로직 ---
                        if st.button("✅ 이 내용으로 DB 토픽 만들기", key=f"btn_{doc_name}_{i}"):
                            # 세션 상태에 추가할 데이터 정보를 저장
                            st.session_state.new_topic_data = {
                                "name": f"{query}에 대한 내용",
                                "desc": para # 인코딩 필요 없음
                            }
                            # DB 편집기 페이지로 이동
                            st.switch_page("pages/5_DB_편집기.py")
                        
                        st.markdown("---")
        if not found_results:
            st.warning("입력하신 키워드를 포함한 내용을 문서에서 찾을 수 없습니다.")
else:
    st.info("문서를 업로드하면 실시간 검색을 시작할 수 있습니다.")