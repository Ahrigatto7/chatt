import re
import yaml
import json
import pandas as pd

def extract_rules_from_text(text):
    # 규칙 추출 (간단 예시)
    rules = []
    rule_pattern = re.compile(r'※\s*(.+?)\s*:?([^\n]+)')
    for match in rule_pattern.finditer(text):
        name = match.group(1).strip()
        desc = match.group(2).strip()
        rules.append({'name': name, 'description': desc})
    return rules

def extract_cases_from_text(text):
    # 사례 추출 (예시: <사례 n> ~ 블록)
    cases = []
    for block in re.findall(r'<사례.*?>.*?(?=(<사례|$))', text, re.DOTALL):
        cases.append(block.strip())
    return cases

def load_yaml_rules(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('rules', [])

def save_rules_json(rules, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(rules, f, ensure_ascii=False, indent=2)

# 모듈 단독 실행 예시
if __name__ == "__main__":
    with open("data/sample.txt", encoding='utf-8') as f:
        text = f.read()
    rules = extract_rules_from_text(text)
    save_rules_json(rules, "output/extracted_rules.json")
    print("규칙 추출 및 저장 완료")
