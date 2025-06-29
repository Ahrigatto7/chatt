import streamlit as st
import pandas as pd
import json
import os

DB_PATH = "knowledge_base.json"

def load_knowledge_json():
    if os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 0:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def flatten_knowledge_json(json_db):
    """지식센터 JSON → DataFrame(문단별)"""
    data = []
    for main_topic, topic_data in json_db.items():
        for sub_key, sub in topic_data.get("sub_topics", {}).items():
            d = {
                "대주제": main_topic,
                "문단ID": sub_key,
                "내용": sub.get("content", ""),
                "카테고리": sub.get("category", ""),
                "태그": sub.get("tags", ""),
                "리뷰": sub.get("review", ""),
                "등록일": sub.get("registered_at", "")
            }
            data.append(d)
    return pd.DataFrame(data)

# ----- Streamlit UI -----
st.set_page_config(page_title="지식센터 탐색/검색/통계", layout="wide")
st.title("📚 지식센터 탐색/검색/통계")

json_db = load_knowledge_json()
df = flatten_knowledge_json(json_db)
if df.empty:
    st.info("아직 등록된 데이터가 없습니다.")
    st.stop()

# ---- 1. 탐색/필터 ----
col1, col2, col3 = st.columns(3)
with col1:
    main_topics = ["전체"] + sorted(df['대주제'].unique())
    topic = st.selectbox("대주제", main_topics)
with col2:
    cats = ["전체"] + sorted(df['카테고리'].unique())
    cat = st.selectbox("카테고리", cats)
with col3:
    kw = st.text_input("키워드(내용/태그/리뷰 포함 검색)")

filtered = df.copy()
if topic != "전체":
    filtered = filtered[filtered['대주제'] == topic]
if cat != "전체":
    filtered = filtered[filtered['카테고리'] == cat]
if kw:
    f1 = filtered['내용'].str.contains(kw, case=False, na=False)
    f2 = filtered['태그'].str.contains(kw, case=False, na=False)
    f3 = filtered['리뷰'].str.contains(kw, case=False, na=False)
    filtered = filtered[f1 | f2 | f3]

st.markdown(f"#### 검색 결과 ({len(filtered)}건)")
st.dataframe(filtered, use_container_width=True)

# ---- 2. 상세/편집 ----
if not filtered.empty:
    sel_idx = st.number_input("상세보기/편집할 행 번호", min_value=0, max_value=len(filtered)-1, value=0)
    row = filtered.iloc[sel_idx]
    st.markdown(f"**문단ID**: {row['문단ID']}")
    content = st.text_area("내용", row['내용'], height=100, key="edit_content")
    category = st.text_input("카테고리", row['카테고리'], key="edit_cat")
    tags = st.text_input("태그(쉼표)", row['태그'], key="edit_tags")
    review = st.text_area("리뷰", row['리뷰'], height=60, key="edit_review")
    if st.button("수정 저장"):
        # JSON 파일 직접 수정(문단ID로 검색)
        db = load_knowledge_json()
        main_topic = row['대주제']
        docid = row['문단ID']
        db[main_topic]["sub_topics"][docid]['content'] = content
        db[main_topic]["sub_topics"][docid]['category'] = category
        db[main_topic]["sub_topics"][docid]['tags'] = tags
        db[main_topic]["sub_topics"][docid]['review'] = review
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        st.success("수정 저장 완료! 새로고침 해주세요.")

# ---- 3. 통계/차트 ----
st.subheader("카테고리/태그별 통계")
col4, col5 = st.columns(2)
with col4:
    st.bar_chart(df['카테고리'].value_counts())
with col5:
    tags_series = df['태그'].str.split(',').explode().str.strip()
    tag_counts = tags_series.value_counts()
    st.bar_chart(tag_counts[tag_counts.index != ''].head(10))

st.subheader("최근 등록/수정 문단")
recent = df.sort_values("등록일", ascending=False).head(10)
st.table(recent[["대주제","카테고리","내용","태그","리뷰","등록일"]])
