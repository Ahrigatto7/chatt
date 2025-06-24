"""Storage utilities for saving and loading Saju records."""
import json
from pathlib import Path

# Path to JSON file storing records
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "records.json"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_records() -> list:
    """Load saved Saju records from the JSON file."""
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_record(record: dict) -> None:
    """Append a new record to the JSON file."""
    records = load_records()
    records.append(record)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
