import sqlite3

DB_PATH = "saju_analysis.db"

def init_db(db_path=DB_PATH):
    """DB 초기화 및 테이블 생성"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 규칙 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        condition TEXT,
        result TEXT
    )
    """)

    # 키워드 테이블
    cur.execute("""
    CREATE TABLE IF NOT EXISTS keyword_hits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        snippet TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_rules_to_db(rules: dict, db_path=DB_PATH):
    """사주 해석 규칙을 DB에 저장"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for condition, results in rules.items():
        for result in results:
            cur.execute("INSERT INTO rules (condition, result) VALUES (?, ?)", (condition, result))
    conn.commit()
    conn.close()

def save_keywords_to_db(keyword_map: dict, db_path=DB_PATH):
    """혼인 키워드 분석 결과를 DB에 저장"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for keyword, snippets in keyword_map.items():
        for snippet in snippets:
            cur.execute("INSERT INTO keyword_hits (keyword, snippet) VALUES (?, ?)", (keyword, snippet))
    conn.commit()
    conn.close()
