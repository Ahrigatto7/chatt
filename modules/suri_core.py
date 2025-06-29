from collections import OrderedDict
from typing import Dict, Optional

def get_saju_pillars(birth_dt) -> OrderedDict:
    """
    출생일시 → 4주(년/월/일/시주) 변환 예시
    :param birth_dt: datetime 객체
    :return: OrderedDict
    """
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    year = birth_dt.year % 10
    month = (birth_dt.month + 1) % 12
    day = (birth_dt.day + 3) % 10
    hour = (birth_dt.hour // 2) % 12
    return OrderedDict([
        ("년주", HEAVENLY_STEMS[year] + EARTHLY_BRANCHES[year]),
        ("월주", HEAVENLY_STEMS[month % 10] + EARTHLY_BRANCHES[month]),
        ("일주", HEAVENLY_STEMS[day] + EARTHLY_BRANCHES[day]),
        ("시주", HEAVENLY_STEMS[hour] + EARTHLY_BRANCHES[hour]),
    ])

def suri_analyze_marry(
    pillars: Dict, 
    sipsin: Dict, 
    daewoon: str, 
    sewoon: str, 
    gender: str, 
    db_tip: Optional[str] = None
) -> str:
    """
    혼인/인연 해석(추천문 자동 포함)
    """
    spouse_signs = ["정관", "편관"] if gender == "여자" else ["정재", "편재"]
    spouse_gan, spouse_ji = sipsin["일주"]
    cond_spouse_real = spouse_gan in spouse_signs or spouse_ji in spouse_signs
    has_hap = "합" in daewoon or "합" in sewoon
    has_chong = "충" in daewoon or "충" in sewoon
    marry_result = ""
    if cond_spouse_real:
        marry_result += "🌷 배우자성 실상, 인연 현실화 가능성↑"
        if has_hap:
            marry_result += "- 합 작용: 만남/결혼운 상승"
        if has_chong:
            marry_result += "- 충 작용: 관계 변화"
    else:
        marry_result += "배우자성이 허상"
    marry_result += "\n실천TIP: 열린 소통!"
    if db_tip:
        marry_result += f"\n\n[추천문]\n{db_tip}"
    return marry_result
