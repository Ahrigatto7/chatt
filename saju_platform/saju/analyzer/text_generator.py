"""Generate interpretation texts based on analysis result."""
from typing import Dict


def generate_text(result: Dict[str, str]) -> str:
    strength = result.get("strength", "")
    if strength == "신강":
        return "당신은 의지가 강하며 주도적인 성향을 지닙니다."
    else:
        return "섬세하고 배려심이 많으나 결정에 시간이 걸릴 수 있습니다."
