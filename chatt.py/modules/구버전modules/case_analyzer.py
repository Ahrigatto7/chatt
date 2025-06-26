import re
import json

def parse_case_structure(case_text):
    # 천간/지지/궁위 등 자동 분해 (간단 예시)
    pattern = re.compile(r'([갑을병정무기경신임계]{1,2})[^\w]?([자축인묘진사오미신유술해]{1,2})')
    result = pattern.findall(case_text)
    return result

def detect_special_structures(case_text):
    # 형, 충, 합, 파, 입묘 등 구조 자동 식별 (예시)
    detected = []
    if "합" in case_text:
        detected.append("합")
    if "충" in case_text:
        detected.append("충")
    if "형" in case_text:
        detected.append("형")
    if "파" in case_text:
        detected.append("파")
    if "穿" in case_text:
        detected.append("천")
    return detected

def analyze_case(case_text):
    parsed = parse_case_structure(case_text)
    specials = detect_special_structures(case_text)
    return {"parsed": parsed, "specials": specials}

# 모듈 단독 실행 예시
if __name__ == "__main__":
    with open("data/sample_case.txt", encoding='utf-8') as f:
        case = f.read()
    result = analyze_case(case)
    print(result)
