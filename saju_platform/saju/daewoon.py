"""Daewoon (대운) calculation utilities.

The algorithms here are greatly simplified. Real implementations
would consider lunar months, solar terms and gender for forward
or reverse progression.
"""
from datetime import datetime
from .ganji import STEMS, BRANCHES


def calculate_daewoon(birth_year: int, gender: str) -> list:
    """Return a list of ten-year fortune cycles.

    Parameters
    ----------
    birth_year: int
        Gregorian birth year.
    gender: str
        'male' or 'female'.
    """
    start = birth_year + 10
    cycles = []
    stem_index = (birth_year - 1984) % 10
    branch_index = (birth_year - 1984) % 12
    direction = 1 if gender.lower() == 'male' else -1
    for i in range(8):
        stem_index = (stem_index + direction) % 10
        branch_index = (branch_index + direction) % 12
        cycles.append({
            "age": start + i * 10,
            "ganji": f"{STEMS[stem_index]}{BRANCHES[branch_index]}"
        })
    return cycles
