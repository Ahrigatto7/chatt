from collections import defaultdict
import pandas as pd

def extract_sections(text):
    keywords = ['혼인', '결혼', '再婚', '初婚', '배우자궁', '부궁', '夫星', '妻宮', '副夫宮']
    lines = text.splitlines()
    results = []
    current_block = []
    capture = False

    for line in lines:
        if any(kw in line for kw in keywords):
            capture = True
        if capture:
            if line.strip():
                current_block.append(line.strip())
            else:
                if current_block:
                    results.append("\n".join(current_block))
                    current_block = []
                    capture = False
    return results, keywords

def analyze_keywords(results, keywords):
    keyword_hits = defaultdict(list)
    for text in results:
        for kw in keywords:
            if kw in text:
                keyword_hits[kw].append(text)

    df = {
        "키워드": [],
        "빈도": [],
        "예시 일부": []
    }
    for k, v in keyword_hits.items():
        df["키워드"].append(k)
        df["빈도"].append(len(v))
        df["예시 일부"].append(v[0][:100] + "..." if v else "")
    return pd.DataFrame(df), keyword_hits
