import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="토픽 탐색기", layout="wide")
st.title("📚 토픽 탐색기")
st.markdown("데이터베이스에 저장된 사주 명리 토픽을 검색하고 탐색합니다.")

CSV_PATH = 'Topic DB 216b50e66dba805abdb2ebd9cbd601da.csv'

@st.cache_data
def load_data(filepath):
    if os.path.exists(filepath):
        return pd.read_csv(filepath).fillna('')
    return None

topic_df = load_data(CSV_PATH)

if topic_df is None:
    st.error(f"'{CSV_PATH}' 파일을 찾을 수 없습니다. 프로젝트 폴더에 파일이 있는지 확인해주세요.")
else:
    topic_list = [""] + topic_df['Name'].tolist()
    search_query = st.text_input("🔍 토픽 검색", placeholder="키워드로 토픽 이름을 검색하세요...")
    
    if search_query:
        filtered_df = topic_df[topic_df['Name'].str.contains(search_query, case=False, na=False)]
        filtered_topic_list = [""] + filtered_df['Name'].tolist()
        selected_topic_name = st.selectbox("📝 검색된 토픽 선택", options=filtered_topic_list)
    else:
        selected_topic_name = st.selectbox("📝 전체 토픽 목록에서 선택", options=topic_list)

    st.markdown("---")

    if selected_topic_name:
        selected_row = topic_df[topic_df['Name'] == selected_topic_name].iloc[0]
        st.subheader(f"🔖 {selected_row['Name']}")
        with st.container(border=True):
            st.markdown("#### 💬 설명")
            st.markdown(selected_row.get('Description', '내용 없음'))
        with st.container(border=True):
            st.markdown("#### 🔑 관련 키워드")
            st.info(selected_row.get('Related Keywords', '내용 없음'))
        with st.container(border=True):
            st.markdown("#### ✨ 관련 사례")
            st.markdown(selected_row.get('Related Examples', '내용 없음'))