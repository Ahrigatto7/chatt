"""Main Flask application for the Saju platform.

This file wires the web interface with the analysis logic and
provides endpoints for saving and viewing results.
"""
from datetime import datetime
from flask import Flask, render_template, request, jsonify

from saju.ganji import (
    get_year_ganji,
    get_month_ganji,
    get_day_ganji,
    get_hour_ganji,
    STEMS,
)
from saju.daewoon import calculate_daewoon
from saju.analyzer import (
    rule_engine,
    text_generator,
    classifier,
    interpreter,
)
from saju.storage import save_record, load_records

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result=None)


@app.route("/analyze", methods=["POST"])
def analyze():
    birthdate = request.form.get("birthdate")
    birthtime = request.form.get("birthtime")
    gender = request.form.get("gender", "male")

    dt = datetime.strptime(f"{birthdate} {birthtime}", "%Y-%m-%d %H:%M")

    year_ganji = get_year_ganji(dt.year)
    year_gan_index = (dt.year - 1984) % 10
    month_ganji = get_month_ganji(year_gan_index, dt.month)
    day_ganji = get_day_ganji(dt)
    day_stem_index = STEMS.index(day_ganji[0])
    hour_ganji = get_hour_ganji(day_stem_index, dt.hour)

    ganji_list = [year_ganji, month_ganji, day_ganji, hour_ganji]

    analysis = rule_engine.analyze(ganji_list)
    text = text_generator.generate_text(analysis)
    categories = classifier.classify(analysis)
    interpretation = interpreter.generate_topic_interpretation(
        {"일간": day_ganji[0], "오행": analysis.get("elements", {})},
        {}
    )
    summary = interpreter.get_summary_text(interpretation)
    daewoon = calculate_daewoon(dt.year, gender)

    result = {
        "ganji": {
            "year": year_ganji,
            "month": month_ganji,
            "day": day_ganji,
            "hour": hour_ganji,
        },
        "analysis": analysis,
        "categories": categories,
        "daewoon": daewoon,
        "text": text,
        "interpretation": interpretation,
        "summary": summary,
    }

    save_record({
        "input": {
            "birthdate": birthdate,
            "birthtime": birthtime,
            "gender": gender,
        },
        "result": result,
    })

    if request.headers.get("Accept") == "application/json":
        return jsonify(result)
    return render_template("index.html", result=result)


@app.route("/records", methods=["GET"])
def records():
    return render_template("records.html", records=load_records())


if __name__ == "__main__":
    app.run(debug=True)
