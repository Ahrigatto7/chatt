import json
import pandas as pd

def save_text(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_excel(summary_df, keyword_map, filename):
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        summary_df.to_excel(writer, sheet_name="목차", index=False)
        for kw, texts in keyword_map.items():
            df = pd.DataFrame({kw: texts})
            df.to_excel(writer, sheet_name=kw[:31], index=False)
