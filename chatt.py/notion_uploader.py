import os
import json
import datetime
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
from notion_client import Client
import fitz  # PyMuPDF for PDF

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN") or "your-secret-token"
DATABASE_ID = "218b50e66dba80d580e5dafe31b59434"
notion = Client(auth=NOTION_TOKEN)

# ✅ 파일 선택 GUI
def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="업로드할 파일을 선택하세요",
        filetypes=[("지원 파일", "*.txt *.md *.json *.py *.pdf")]
    )
    return list(file_paths)

# ✅ 파일 내용 읽기
def read_file_content(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.pdf':
            text = ""
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text()
            return text
        elif ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.dumps(json.load(f), ensure_ascii=False, indent=2)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        print(f"❌ 파일 읽기 실패: {file_path} - {e}")
        return ""

# ✅ 태그 자동 추출
def extract_tags(content, file_path):
    ext = os.path.splitext(file_path)[1].lower()
    tags = []
    if ext == '.py': tags.append("코드")
    elif ext == '.pdf': tags.append("문서")
    elif ext == '.json': tags.append("데이터")

    content_lower = content.lower()
    keyword_tag_map = {
        "기획": ["기획", "전략", "방향성", "로드맵"],
        "개발": ["코드", "개발", "프로그래밍", "알고리즘"],
        "디자인": ["디자인", "ui", "ux", "사용자경험"],
        "Book": ["책", "북리뷰", "book"],
        "학습자료": ["학습", "공부", "강의", "튜토리얼"],
        "Case": ["사례", "케이스", "벤치마킹"],
        "용어": ["용어", "정의", "개념", "의미"],
        "수암명리": ["수암명리", "명리", "사주", "상법"]
    }

    for tag, keywords in keyword_tag_map.items():
        if any(k in content_lower for k in keywords):
            tags.append(tag)

    return tags or ["미분류"]

# ✅ 중요도 자동 평가
def evaluate_importance(content):
    if "중요" in content or "urgent" in content.lower() or "핵심" in content:
        return "높음"
    elif len(content) > 1000:
        return "중간"
    return "낮음"

# ✅ Notion 블록 변환
def md_to_notion_blocks(text):
    blocks = []
    for para in text.strip().split("\n\n"):
        if para.strip():
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": para[:2000]}}]
                }
            })
    return blocks[:100]  # 최대 100개 제한

# ✅ 중복 확인: 같은 제목이 이미 존재하는지
def is_duplicate(title):
    response = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "제목",
                "title": {
                    "equals": title
                }
            }
        }
    )
    return len(response["results"]) > 0

# ✅ Notion 페이지 생성
def create_page(file_path):
    content = read_file_content(file_path)
    title = os.path.splitext(os.path.basename(file_path))[0]

    if is_duplicate(title):
        print(f"⚠️ 중복: '{title}'은(는) 이미 업로드된 파일입니다.")
        return None

    tags = extract_tags(content, file_path)
    importance = evaluate_importance(content)
    blocks = md_to_notion_blocks(content)
    date_now = datetime.datetime.now().isoformat()

    properties = {
        "제목": {"title": [{"text": {"content": title}}]},
        "태그": {"multi_select": [{"name": t} for t in tags]},
        "중요도": {"select": {"name": importance}},
        "추가일": {"date": {"start": date_now}},
        "상태": {"status": {"name": "미처리"}},
        "파일유형": {"select": {"name": os.path.splitext(file_path)[1][1:].upper()}}
    }

    return notion.pages.create(parent={"database_id": DATABASE_ID}, properties=properties, children=blocks)

# ✅ 실행 메인
def main():
    files = select_files()
    if not files:
        print("❌ 파일이 선택되지 않았습니다.")
        return

    print(f"📁 총 {len(files)}개의 파일이 선택되었습니다.")
    for file_path in files:
        try:
            result = create_page(file_path)
            if result:
                print(f"✅ 업로드 완료: {result['url']}")
        except Exception as e:
            print(f"❌ 오류 발생 ({os.path.basename(file_path)}): {e}")

if __name__ == "__main__":
    main()
