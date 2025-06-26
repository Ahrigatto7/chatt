import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from docx import Document
import json
from collections import defaultdict
import os

def extract_marriage_sections(doc_path):
    doc = Document(doc_path)
    results = []
    keywords = ['夫宮', '妻宮', '夫星', '副夫宮', '副妻宮', '부궁', '배우자궁', '혼인', '결혼', '再婚', '初婚']
    current_block = []
    capturing = False

    for para in doc.paragraphs:
        text = para.text.strip()
        if any(kw in text for kw in keywords):
            capturing = True
        if capturing:
            if text:
                current_block.append(text)
            else:
                if current_block:
                    results.append('\n'.join(current_block))
                    current_block = []
                    capturing = False
    if current_block:
        results.append('\n'.join(current_block))

    return results, keywords

def analyze_keywords(results, keywords):
    keyword_hits = defaultdict(list)
    for text in results:
        for kw in keywords:
            if kw in text:
                keyword_hits[kw].append(text)

    summary = {
        "키워드": [],
        "빈도": [],
        "예시 일부": []
    }

    for kw, texts in keyword_hits.items():
        summary["키워드"].append(kw)
        summary["빈도"].append(len(texts))
        summary["예시 일부"].append(texts[0][:100] + "..." if texts else "")
    return pd.DataFrame(summary), keyword_hits

def save_keyword_texts_with_toc(grouped_texts, output_path):
    filename = os.path.join(output_path, "혼인_배우자궁_키워드별_시트저장.xlsx")
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        workbook = writer.book
        toc_data = []

        for keyword, texts in grouped_texts.items():
            if texts:
                sheet_name = keyword[:31].replace('/', '_').replace('\\', '_')
                df = pd.DataFrame({f"{keyword} 관련 설명": texts})
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                toc_data.append({'키워드': keyword, '시트': sheet_name})

        toc_df = pd.DataFrame(toc_data)
        toc_df.to_excel(writer, sheet_name="목차", index=False, startrow=1)
        worksheet = writer.sheets["목차"]
        header_format = workbook.add_format({'bold': True, 'bg_color': '#DDEBF7'})
        worksheet.write(0, 0, "키워드별 분석 시트 목록", header_format)

        for i, row in enumerate(toc_data, start=2):
            worksheet.write_url(i, 1, f"internal:'{row['시트']}'!A1", string=row['시트'])

# GUI 처리
def run_batch_extraction():
    files = filedialog.askopenfilenames(title="혼인 관련 Word 파일들 선택", filetypes=[("Word Documents", "*.docx")])
    if not files:
        return

    output_dir = filedialog.askdirectory(title="결과 저장 폴더 선택")
    if not output_dir:
        return

    try:
        for file_path in files:
            base = os.path.splitext(os.path.basename(file_path))[0]
            results, keywords = extract_marriage_sections(file_path)

            # 개별 파일마다 결과 저장
            df = pd.DataFrame({'혼인/배우자궁 관련 설명': results})
            df.to_excel(os.path.join(output_dir, f"{base}_해석.xlsx"), index=False)

            analysis_df, grouped_texts = analyze_keywords(results, keywords)
            analysis_df.to_excel(os.path.join(output_dir, f"{base}_키워드분석.xlsx"), index=False)

            save_keyword_texts_with_toc(grouped_texts, output_dir)

        messagebox.showinfo("완료", f"{len(files)}개 파일 분석 완료!\n저장 위치: {output_dir}")
    except Exception as e:
        messagebox.showerror("오류 발생", str(e))

# GUI 생성
root = tk.Tk()
root.title("혼인·배우자궁 다중 분석 도구")
root.geometry("420x230")

tk.Label(root, text="📂 여러 Word 파일을 선택하고 결과 저장 폴더를 지정하세요.", wraplength=400).pack(pady=20)

tk.Button(root, text="Word 파일 여러 개 선택 + 저장 폴더 지정", command=run_batch_extraction,
          height=2, width=35, bg="#2196F3", fg="white").pack()

root.mainloop()
