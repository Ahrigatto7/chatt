"""Ohaeng (오행) distribution utilities.

This module provides simple counting of the five elements based on
stems and branches. The mapping is illustrative only.
"""
from collections import Counter
from .ganji import STEMS, BRANCHES

ELEMENTS = {
    "갑": "목", "을": "목",
    "병": "화", "정": "화",
    "무": "토", "기": "토",
    "경": "금", "신": "금",
    "임": "수", "계": "수",
    "인": "목", "묘": "목",
    "사": "화", "오": "화",
    "진": "토", "술": "토", "축": "토", "미": "토",
    "신": "금", "유": "금",
    "자": "수", "해": "수",
}


def analyze_elements(ganji_list: list) -> dict:
    """Return distribution of five elements from a list of ganji strings."""
    counts = Counter(ELEMENTS.get(ch) for gj in ganji_list for ch in gj)
    return dict(counts)
