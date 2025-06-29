import streamlit as st
from modules.file_handler import extract_text
from modules.ai_utils import ai_classify_paragraphs
import pandas as pd
import json
import os
from datetime import datetime

# --- 지식센터 DB(JSON) 로드/저장 함수 ---
DB_PATH = "knowledge_base.json"

def load_knowledge_json():
    if os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 0:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_knowledge_json(data):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="문서AI 도구 → 지식센터 연동", layout="wide")
st.header("📄 문서AI 도구 → 지식센터 연동/수정/저장")

uploaded_file = st.file_uploader("문서 업로드 (pdf, txt, docx)", type=["pdf", "txt", "docx"])
api_key = st.text_input("OpenAI API Key", type="password")
categories = st.text_input("카테고리(쉼표로)", value="혼인,재물,직업,건강")
cat_list = [c.strip() for c in categories.split(',') if c.strip()]

# 1. 문서 추출 및 분류
if uploaded_file and api_key:
    text = extract_text(uploaded_file)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    st.info(f"문단 {len(paragraphs)}개 추출됨")
    if st.button("AI 자동분류 실행"):
        with st.spinner("AI 분류중..."):
            results = ai_classify_paragraphs(paragraphs, api_key, cat_list)
            df = pd.DataFrame({
                "문단": paragraphs,
                "카테고리": results,
                "태그": [""] * len(paragraphs),
                "리뷰": ["" for _ in paragraphs],
                "승인여부": ["대기"] * len(paragraphs)    # 승인(대기/승인/반려)
            })
            st.session_state["문서분석DF"] = df
            st.success("분류 결과를 아래에서 수정/저장할 수 있습니다.")

# 2. 분류결과 수정 UI (표 형태 입력)
if "문서분석DF" in st.session_state:
    st.markdown("### 분류 결과 확인 및 수정")
    df = st.session_state["문서분석DF"]
    # 데이터 에디터로 셀 직접 수정(태깅/리뷰/승인까지)
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        key="문서분석에디터"
    )
    st.write("필요하다면 셀을 직접 수정하세요! (카테고리, 태그, 리뷰, 승인여부 등)")

    # 3. 저장 버튼 → 지식센터 누적 저장
    if st.button("지식센터에 저장"):
        now = datetime.now().isoformat()
        knowledge = load_knowledge_json()
        if "문서AI" not in knowledge:
            knowledge["문서AI"] = {"description": "AI 자동분류 문서 누적", "sub_topics": {}}
        sub_topics = knowledge["문서AI"]["sub_topics"]
        for idx, row in edited_df.iterrows():
            key = f"{now[:19]}_{idx}"
            sub_topics[key] = {
                "content": row["문단"],
                "category": row["카테고리"],
                "tags": row.get("태그", ""),
                "review": row.get("리뷰", ""),
                "approve": row.get("승인여부", "대기"),
                "registered_at": now
            }
        save_knowledge_json(knowledge)
        st.success("지식센터에 저장 완료! (탐색/편집탭에서 확인)")

    # 4. 저장된 데이터 미리보기
    if st.button("저장된 지식센터 미리보기"):
        knowledge = load_knowledge_json()
        if "문서AI" in knowledge and knowledge["문서AI"]["sub_topics"]:
            st.json(knowledge["문서AI"]["sub_topics"])
        else:
            st.info("아직 데이터가 없습니다.")
else:
    st.info("문서 업로드, API 키 입력, 분류 실행 후 결과가 표시됩니다.")

# --- CSV/엑셀로 내보내기 (옵션) ---
if "문서분석DF" in st.session_state:
    df = st.session_state["문서분석DF"]
    csv = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        "현재 분석결과 CSV로 다운로드", data=csv, file_name="문서AI분석결과.csv", mime="text/csv"
    )
    excel_buf = df.to_excel(index=False, engine='openpyxl')
    st.download_button(
        "현재 분석결과 엑셀로 다운로드", data=excel_buf, file_name="문서AI분석결과.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
