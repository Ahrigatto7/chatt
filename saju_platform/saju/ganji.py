"""Ganji calculation utilities for stems and branches.
This module provides simple algorithms to compute the Heavenly
stem (천간) and Earthly branch (지지) for year, month, day and hour.
Algorithms are simplified and may not cover all edge cases.
"""
from datetime import datetime, timedelta

# 10 Heavenly stems
STEMS = [
    "갑", "을", "병", "정", "무",
    "기", "경", "신", "임", "계"
]

# 12 Earthly branches
BRANCHES = [
    "자", "축", "인", "묘", "진", "사",
    "오", "미", "신", "유", "술", "해"
]

CYCLE = [f"{STEMS[i % 10]}{BRANCHES[i % 12]}" for i in range(60)]


def get_year_ganji(year: int) -> str:
    """Return ganji (stem+branch) for the given Gregorian year."""
    index = (year - 1984) % 60  # 1984 is 갑자 year
    return CYCLE[index]


def get_day_ganji(date: datetime) -> str:
    """Compute ganji for a specific Gregorian date."""
    base = datetime(1984, 2, 2)  # known 갑자일
    delta = date - base
    index = delta.days % 60
    return CYCLE[index]


def get_hour_ganji(day_stem_index: int, hour: int) -> str:
    """Return ganji for the given hour based on day stem index.

    Parameters
    ----------
    day_stem_index: int
        Index of the day's heavenly stem (0-9).
    hour: int
        Hour in 24h format.
    """
    branch_index = ((hour + 1) // 2) % 12
    stem_index = (day_stem_index * 2 + branch_index) % 10
    return f"{STEMS[stem_index]}{BRANCHES[branch_index]}"


def get_month_ganji(year_gan_index: int, month: int) -> str:
    """Simplified month ganji calculation based on year stem index."""
    stem_index = (year_gan_index * 2 + month + 1) % 10
    branch_index = (month + 1) % 12
    return f"{STEMS[stem_index]}{BRANCHES[branch_index]}"
