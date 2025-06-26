import streamlit as st
import pandas as pd
import yaml
from rule_extractor import extract_rules_from_text, load_yaml_rules, extract_cases_from_text
from case_analyzer import analyze_case
from report_generator import generate_markdown_report, generate_excel_report, generate_pdf_report

st.title("수암명리 자동 분석기")

tab1, tab2 = st.tabs(["규칙/사례 추출", "분석 리포트"])

with tab1:
    st.header("규칙 및 사례 추출")
    uploaded = st.file_uploader("문서 업로드", type=["txt", "md"])
    yaml_file = st.file_uploader("규칙(yaml) 파일 업로드", type=["yaml"])
    if uploaded:
        text = uploaded.read().decode("utf-8")
        rules = extract_rules_from_text(text)
        cases = extract_cases_from_text(text)
        st.write("추출 규칙", rules)
        st.write("추출 사례", cases)
        st.session_state["rules"] = rules
        st.session_state["cases"] = cases
    elif yaml_file:
        rules = load_yaml_rules(yaml_file)
        st.write("Yaml 규칙", rules)
        st.session_state["rules"] = rules
        st.session_state["cases"] = []
    else:
        st.info("문서 또는 yaml 규칙 파일을 업로드하세요.")

with tab2:
    st.header("자동 분석/리포트")
    cases = st.session_state.get("cases", [])
    rules = st.session_state.get("rules", [])
    if cases and rules:
        if st.button("분석/리포트 생성"):
            analyzed = [analyze_case(c) for c in cases]
            st.write("분석 결과", analyzed)
            generate_markdown_report(cases, rules, "output/report.md")
            generate_excel_report(cases, "output/report.xlsx")
            generate_pdf_report(cases, rules, "output/report.pdf")
            st.success("보고서 생성 완료! output/ 폴더를 확인하세요.")
    else:
        st.info("먼저 규칙/사례를 추출하세요.")

st.sidebar.markdown("""
- [프로젝트 가이드 보기](https://your.project.url)
- 각 모듈은 단독 실행 가능하며, 함수 import로 앱에 연동됩니다.
""")
