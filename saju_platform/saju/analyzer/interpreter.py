"""Rule-based interpretation module for Saju analysis.

This module generates textual interpretations from Saju data using
simple heuristics. It is intentionally lightweight and can be extended
with more sophisticated rules or external JSON rule sets.
"""

from typing import Dict, List


# Example rules for demonstration purposes only. A real application would
# use a much richer rule base loaded from a file.
RULES = {
    "재성>3": "돈 관리 능력이 뛰어납니다.",
    "인성 부족+관성 과다": "건강 문제를 주의하세요.",
    "비견 많고 재성 없음": "배우자와 갈등이 있을 수 있습니다.",
}


def judge_strength(ohaeng_dict: Dict[str, int]) -> str:
    """Return '신강' if any element count is 3 or more, else '신약'."""
    if not ohaeng_dict:
        return ""
    return "신강" if max(ohaeng_dict.values()) >= 3 else "신약"


def estimate_yongshin(ohaeng_dict: Dict[str, int]) -> str:
    """Return the element with the lowest presence as the tentative yongshin."""
    if not ohaeng_dict:
        return ""
    return min(ohaeng_dict, key=ohaeng_dict.get)


def _apply_rules(structure: Dict[str, int]) -> List[str]:
    """Internal helper that returns interpretation snippets based on rules."""
    texts = []
    if structure.get("재성", 0) > 3:
        texts.append(RULES["재성>3"])
    if structure.get("인성", 0) == 0 and structure.get("관성", 0) > 1:
        texts.append(RULES["인성 부족+관성 과다"])
    if structure.get("비견", 0) > 1 and structure.get("재성", 0) == 0:
        texts.append(RULES["비견 많고 재성 없음"])
    return texts


def generate_topic_interpretation(saju_data: Dict, structure: Dict) -> Dict[str, str]:
    """Generate interpretation texts for predefined topics.

    Parameters
    ----------
    saju_data: dict
        Basic saju information including day master and element distribution.
    structure: dict
        육친 구조 정보.
    """
    ohaeng = saju_data.get("오행", {})
    strength = judge_strength(ohaeng)
    yongshin = estimate_yongshin(ohaeng)
    rule_texts = _apply_rules(structure)

    return {
        "요약": f"일간 {saju_data.get('일간', '')} 기준 {strength}한 사주입니다.",
        "건강": " ".join(rule_texts) or "특별한 건강 상의 문제는 보이지 않습니다.",
        "직업": f"{yongshin} 관련 업종이 유리할 수 있습니다.",
        "혼인": "배우자운은 평균적입니다.",
        "가족": "가족 간의 유대가 중요합니다.",
        "성격": "침착하고 분석적인 성향을 가집니다." if strength == "신약" else "적극적이고 리더십이 강합니다.",
    }


def get_summary_text(results: Dict[str, str]) -> str:
    """Concatenate topic texts into a single summary string."""
    return " ".join(results.get(topic, "") for topic in [
        "요약",
        "건강",
        "직업",
        "혼인",
        "가족",
        "성격",
    ]).strip()

