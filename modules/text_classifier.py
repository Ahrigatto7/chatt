from typing import Dict, List
import re


def classify_text(text: str) -> Dict[str, List[str]]:
    """Classify lines of unstructured Saju text into rules, examples, and terms.

    Parameters
    ----------
    text: str
        Input text that may contain rules, examples, or terminology.

    Returns
    -------
    Dict[str, List[str]]
        A dictionary with keys ``"규칙"``, ``"사례"``, and ``"용어"`` mapping to
        lists of extracted sentences.
    """
    if not text:
        return {"규칙": [], "사례": [], "용어": []}

    rule_lines: List[str] = []
    example_lines: List[str] = []
    term_lines: List[str] = []

    term_pattern_colon = re.compile(r"^[^\s:]{1,20}\s*:\s*.+")
    term_pattern_meaning = re.compile(r"^[^\s]{1,20}(?:은|는|이란|란) .+(?:의미|뜻).*다\.?$")

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if "예:" in line or "사례:" in line:
            example_lines.append(line)
            continue

        if term_pattern_colon.match(line) or term_pattern_meaning.match(line):
            term_lines.append(line)
            continue

        if line.endswith("이다") or line.endswith("이다.") or line.endswith("판단한다") or line.endswith("판단한다.") or line.endswith("사용한다") or line.endswith("사용한다."):
            rule_lines.append(line)
            continue

        if line.endswith("다") or line.endswith("다."):
            rule_lines.append(line)

    return {"규칙": rule_lines, "사례": example_lines, "용어": term_lines}
