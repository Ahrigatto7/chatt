from fpdf import FPDF

def generate_pdf_report(filename, rule_data: dict, keyword_summary_df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="사주 문서 분석 보고서", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="📑 추출된 해석 규칙", ln=True)

    for k, v_list in rule_data.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(200, 8, txt=f"[{k}]", ln=True)
        pdf.set_font("Arial", '', 11)
        for v in v_list:
            pdf.multi_cell(0, 6, f"- {v}")

    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="📊 혼인 키워드 분석 요약", ln=True)

    for i, row in keyword_summary_df.iterrows():
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 6, f"{row['키워드']} ({row['빈도']}회): {row['예시 일부']}")

    pdf.output(filename)