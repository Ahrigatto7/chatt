import pytest
from modules import suri_core
import datetime

def test_get_saju_pillars():
    dt = datetime.datetime(1991, 5, 4, 10)
    res = suri_core.get_saju_pillars(dt)
    assert "년주" in res

def test_suri_analyze_marry():
    pillars = {"일주": "갑자"}
    sipsin = {"일주": ("정관", "편재")}
    out = suri_core.suri_analyze_marry(pillars, sipsin, "합", "", "여자")
    assert "인연" in out
