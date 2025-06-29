import streamlit as st
from modules import db

# DB, 폴더, 파일 자동 초기화
db.init_db()

st.set_page_config(page_title="analyzer", layout="wide")
st.title("🔮 analyzer")
st.markdown("""
## 환영합니다!
좌측 메뉴에서 원하는 기능을 선택하세요.
---
""")
st.info("이 플랫폼은 AI+DB 기반 자동 해석, 사례분석, 문서AI 등 다양한 도구를 제공합니다.")
