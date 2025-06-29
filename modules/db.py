import sqlite3
import pandas as pd
import os
from typing import Dict, List, Optional
from datetime import datetime

KNOW_CSV = "data/지식센터.csv"

def save_to_knowledge_center(field, text, category, user_id, tags="", review="", approve="대기"):
    """지식센터 DB에 분류 결과 저장"""
    row = {
        "분야": field,
        "원문/문단": text,
        "분류결과": category,
        "태그": tags,
        "리뷰": review,
        "승인여부": approve,
        "수정일시": datetime.now().isoformat(),
        "등록일시": datetime.now().isoformat(),
        "사용자ID": user_id
    }
    if os.path.exists(KNOW_CSV):
        df = pd.read_csv(KNOW_CSV)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_csv(KNOW_CSV, index=False, encoding="utf-8-sig")

def load_knowledge_center():
    """지식센터 데이터 전체 로드"""
    if os.path.exists(KNOW_CSV):
        return pd.read_csv(KNOW_CSV)
    else:
        cols = ["분야","원문/문단","분류결과","태그","리뷰","승인여부","수정일시","등록일시","사용자ID"]
        return pd.DataFrame(columns=cols)

def update_knowledge_row(idx, update_dict):
    """지식센터 특정 row 수정(idx: DataFrame 인덱스)"""
    df = load_knowledge_center()
    for k,v in update_dict.items():
        df.at[idx, k] = v
    df.at[idx, "수정일시"] = datetime.now().isoformat()
    df.to_csv(KNOW_CSV, index=False, encoding="utf-8-sig")

DB_DIR = "data"
DB_NAME = os.path.join(DB_DIR, "suri_platform_data.db")
os.makedirs(DB_DIR, exist_ok=True)

def init_db() -> None:
    """
    DB 및 테이블 자동 초기화(없으면 생성)
    """
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                condition TEXT NOT NULL,
                result TEXT NOT NULL,
                UNIQUE(condition, result)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                birth_info TEXT UNIQUE NOT NULL,
                memo TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_rules_to_db(rules: Dict[str, List[str]]) -> None:
    """룰(추천문) 저장"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        data_to_insert = [(cond, res) for cond, results in rules.items() for res in results]
        cursor.executemany(
            "INSERT INTO rules (condition, result) VALUES (?, ?) ON CONFLICT(condition, result) DO NOTHING",
            data_to_insert
        )
        conn.commit()

def load_all_rules() -> pd.DataFrame:
    """모든 추천문을 DataFrame으로 반환"""
    with sqlite3.connect(DB_NAME) as conn:
        return pd.read_sql_query("SELECT id, condition, result FROM rules ORDER BY id", conn)

def get_db_tip(field: str, pattern_key: Optional[str] = None) -> str:
    """
    분야/키워드로 추천문 1개 반환
    """
    df = load_all_rules()
    hit = df[df['condition'].str.contains(field, na=False)]
    if pattern_key:
        hit = hit[hit['condition'].str.contains(pattern_key, na=False)]
    if not hit.empty:
        return hit.iloc[0]['result']
    return ""

def save_note(birth_info: str, memo: str) -> None:
    """개인 분석 노트 저장"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notes (birth_info, memo)
            VALUES (?, ?)
            ON CONFLICT(birth_info) DO UPDATE SET memo=excluded.memo, last_updated=CURRENT_TIMESTAMP
        """, (birth_info, memo))
        conn.commit()

# --- 유저 입력/해석 로그 저장 함수 ---
def save_user_log(user_id: str, action: str, payload: dict) -> None:
    """
    유저 입력/해석 등 로그를 CSV로 기록
    :param user_id: 사용자 식별자
    :param action: 이벤트 종류(예: '해석', '문서업로드')
    :param payload: 입력/결과 등 json/dict
    """
    import json, datetime, csv
    os.makedirs("data/logs", exist_ok=True)
    log_path = os.path.join("data/logs", f"user_log.csv")
    with open(log_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().isoformat(), user_id, action, json.dumps(payload, ensure_ascii=False)])
