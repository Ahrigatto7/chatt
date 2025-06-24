# Saju Platform

간단한 만세력(사주) 분석 웹 앱 예제입니다. Flask를 사용하여 입력된 생년월일과 시간 정보를
기반으로 오행 분포, 신강/신약 여부 등을 계산합니다. 결과는 JSON 파일로 저장되어
나중에 다시 확인할 수 있습니다.
간단한 rule 기반 해석기는 `analyzer/interpreter.py`에 구현되어 있습니다.

## 구조

```
saju_platform/
├── app.py
├── saju/
│   ├── ganji.py
│   ├── lunar_converter.py
│   ├── daewoon.py
│   ├── ohaeng.py
│   ├── storage.py
│   └── analyzer/
│       ├── rule_engine.py
│       ├── text_generator.py
│       ├── classifier.py
│       ├── clustering.py
│       ├── interpreter.py
│       └── templates/default.json
├── templates/
│   ├── index.html
│   └── records.html
├── static/style.css
└── data/records.json
```

## 실행 방법

```
cd saju_platform
export FLASK_APP=app.py
flask run
```
