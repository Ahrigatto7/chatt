import pandas as pd
from fpdf import FPDF

def generate_markdown_report(cases, rules, out_path):
    md = "# 분석 보고서\n\n## 규칙\n"
    for rule in rules:
        md += f"- **{rule.get('name')}**: {rule.get('description')}\n"
    md += "\n## 사례\n"
    for i, case in enumerate(cases, 1):
        md += f"### 사례 {i}\n{case}\n\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

def generate_excel_report(cases, out_path):
    df = pd.DataFrame({"사례": cases})
    df.to_excel(out_path, index=False)

def generate_pdf_report(cases, rules, out_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="분석 보고서", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, "규칙", ln=True)
    for rule in rules:
        pdf.multi_cell(0, 8, f"{rule.get('name')}: {rule.get('description')}")
    pdf.ln(5)
    pdf.cell(0, 10, "사례", ln=True)
    for i, case in enumerate(cases, 1):
        pdf.multi_cell(0, 8, f"사례 {i}: {case}")
        pdf.ln(2)
    pdf.output(out_path)

# 모듈 단독 실행 예시
if __name__ == "__main__":
    cases = ["예시 사례1", "예시 사례2"]
    rules = [{"name": "관인상생", "description": "관성이 인성을 생하면 귀격"}]
    generate_markdown_report(cases, rules, "output/report.md")
    generate_excel_report(cases, "output/report.xlsx")
    generate_pdf_report(cases, rules, "output/report.pdf")
    print("보고서 생성 완료")
