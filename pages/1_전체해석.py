import streamlit as st
from modules.suri_core import get_saju_pillars, suri_analyze_marry
from modules import db

st.header("🧬 전체 해석")
name = st.text_input("이름")
year = st.number_input("출생 연", 1900, 2100, 2000)
month = st.number_input("월", 1, 12, 1)
day = st.number_input("일", 1, 31, 1)
hour = st.selectbox("시", list(range(24)), 12)
gender = st.radio("성별", ("남자", "여자"))
daewoon = st.text_input("대운")
sewoon = st.text_input("세운")
if st.button("해석하기"):
    import datetime
    birth_dt = datetime.datetime(year, month, day, hour)
    pillars = get_saju_pillars(birth_dt)
    db_tip = db.get_db_tip("혼인")
    result = suri_analyze_marry(pillars, {}, daewoon, sewoon, gender, db_tip)
    st.success(result)
    db.save_user_log(name, "해석", {
        "input": dict(name=name, year=year, month=month, day=day, hour=hour, gender=gender),
        "output": result
    })
