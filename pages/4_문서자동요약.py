import streamlit as st
from modules.file_handler import extract_text
from modules.ai_utils import auto_summarize_text
import pandas as pd
import io

st.set_page_config(page_title="여러 파일 자동 요약", layout="wide")
st.header("📄 여러 문서 자동 요약 및 다운로드 (OpenAI 없이)")

uploaded_files = st.file_uploader(
    "문서 여러개 업로드 (pdf, txt, docx, 10개까지 추천)", 
    type=["pdf", "txt", "docx"], 
    accept_multiple_files=True
)
ratio = st.slider("요약 비율(ratio)", min_value=0.05, max_value=0.5, value=0.2, step=0.05)

if uploaded_files:
    rows = []
    for file in uploaded_files:
        try:
            text = extract_text(file)
            summary = auto_summarize_text(text, ratio=ratio)
            rows.append({
                "파일명": file.name,
                "본문(앞 200자)": text[:200].replace('\n', ' '),
                "요약": summary
            })
        except Exception as e:
            rows.append({
                "파일명": file.name,
                "본문(앞 200자)": "읽기 실패",
                "요약": f"요약 실패: {e}"
            })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    # --- CSV 다운로드 ---
    csv_buf = io.StringIO()
    df.to_csv(csv_buf, index=False, encoding='utf-8-sig')
    st.download_button(
        "CSV로 다운로드", csv_buf.getvalue(), file_name="여러문서_요약결과.csv", mime="text/csv"
    )

    # --- 텍스트 다운로드 ---
    txt_buf = io.StringIO()
    for i, row in df.iterrows():
        txt_buf.write(f"[{row['파일명']}]\n")
        txt_buf.write("----- 본문(앞 200자) -----\n")
        txt_buf.write(row["본문(앞 200자)"] + "\n")
        txt_buf.write("----- 요약 -----\n")
        txt_buf.write(row["요약"] + "\n\n")
    st.download_button(
        "텍스트로 다운로드", txt_buf.getvalue(), file_name="여러문서_요약결과.txt", mime="text/plain"
    )
else:
    st.info("여러 문서를 동시에 업로드하면 파일별로 자동 요약/다운로드가 가능합니다.")
