
from flask import Flask, render_template, request, send_file
import os
import re
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FILE = "enhanced_rules.json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

KEYWORDS_MAP = {
    "입묘": ("override", "성별 변경"),
    "묘고": ("override", "성별 변경"),
    "공망": ("override", "성별 변경"),
    "허투": ("override", "성별 변경"),
    "穿": ("override", "성별 변경"),
    "陰官": ("zss", "딸"),
    "陽官": ("zss", "아들"),
    "陰財": ("zss", "딸"),
    "陽財": ("zss", "아들"),
    "생을 받지 못": ("zss_condition", "딸"),
    "생을 받": ("zss_condition", "아들"),
    "자식궁에 있음": ("zsg", "아들"),
    "자식궁에 있다": ("zsg", "아들"),
    "자식성이 자식궁에": ("zsg", "아들"),
    "妻星과 합이 없어": ("invalidation", "자식 없음"),
    "妻星과 합": ("zsg", "자식 있음"),
    "자식이 없다": ("invalidation", "자식 없음"),
    "자식이 있다": ("zss", "자식 있음")
}

REGEX_PATTERNS = [
    (r"(.*?)는 (아들|딸)인데 (입묘|공망|허투|穿).*?(아들|딸)이다", "override"),
    (r"(.*?)입묘하니 (아들|딸)이다", "override"),
    (r"(.*?)공망이라 (아들|딸)이다", "override"),
    (r"(.*?)허투하니 (아들|딸)이다", "override"),
    (r"(.*?)穿을 받아 (아들|딸)이다", "override"),
    (r"자식을 낳을 수 없[다음]", "invalidation"),
    (r"자식이 없는", "invalidation"),
    (r"자식이 없어", "invalidation"),
    (r"(아들|딸)을 낳았", "birth_result"),
    (r"(아들|딸)을 얻었", "birth_result")
]

def extract_saju_rules(text, output_path):
    rules = []
    seen = set()
    for keyword, (rtype, result) in KEYWORDS_MAP.items():
        if keyword in text:
            rule = {"type": rtype, "condition": keyword, "result": result}
            key = (rtype, keyword, result)
            if key not in seen:
                seen.add(key)
                rules.append(rule)
    for pattern, rtype in REGEX_PATTERNS:
        matches = re.findall(pattern, text)
        for m in matches:
            if rtype == "override":
                condition = f"{m[0]}는 {m[1]}인데 {m[2]} → {m[3]}"
                result = m[3]
            elif rtype == "birth_result":
                condition = f"출산 결과: {m[0]}"
                result = m[0]
            else:
                condition = m[0] if isinstance(m, tuple) else m
                result = "자식 없음"
            key = (rtype, condition, result)
            if key not in seen:
                seen.add(key)
                rules.append({"type": rtype, "condition": condition, "result": result})
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)

@app.route("/", methods=["GET", "POST"])
def index():
    result_url = None
    if request.method == "POST":
        file = request.files["saju_file"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            extract_saju_rules(text, RESULT_FILE)
            result_url = "/download"

    return render_template("index_fixed.html", result_url=result_url)

@app.route("/download")
def download():
    return send_file(RESULT_FILE, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
