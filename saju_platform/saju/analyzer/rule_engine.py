"""Basic rule engine for Saju analysis."""
from typing import Dict, List
from ..ohaeng import analyze_elements


def determine_strength(element_dist: Dict[str, int]) -> str:
    """Determine if the day master is strong or weak based on element counts."""
    max_elem = max(element_dist, key=element_dist.get)
    if element_dist[max_elem] >= 3:
        return "신강"
    return "신약"


def analyze(ganji_list: List[str]) -> Dict[str, str]:
    """Return simple analysis results for given ganji list."""
    elements = analyze_elements(ganji_list)
    strength = determine_strength(elements)
    return {"strength": strength, "elements": elements}
