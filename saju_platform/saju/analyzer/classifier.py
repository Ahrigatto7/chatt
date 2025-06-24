"""Simple classifier for categorizing interpretation topics."""
from typing import Dict


def classify(result: Dict[str, str]) -> Dict[str, str]:
    strength = result.get("strength", "")
    if strength == "신강":
        return {"성격": "리더십", "건강": "과로 주의", "직업": "관리자"}
    else:
        return {"성격": "협력적", "건강": "허약 주의", "직업": "연구직"}
