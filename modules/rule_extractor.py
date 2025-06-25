import re
import json

def extract_interpretive_rules(text):
    pattern = re.compile(r'([^\s]+)[은는이가]? ?([^\s]+)?(때|경우|이면|이라면|일 때|일 경우|인 경우)[ ,]*(.+?)(\.|$)')
    rules = {}
    for match in pattern.finditer(text):
        cond = match.group(1).strip()
        trigger = match.group(2).strip() if match.group(2) else ""
        result = match.group(4).strip()
        key = f"{cond} {trigger}".strip()
        rules.setdefault(key, []).append(result)
    return rules

def format_rules_to_markdown(rules):
    lines = ["# 사주 해석 규칙"]
    for key, vals in rules.items():
        lines.append(f"## {key}")
        for i, v in enumerate(vals, 1):
            lines.append(f"- {i}. {v}")
    return "\n".join(lines)
