from typing import List, Optional

def ai_classify_paragraphs(paragraphs, api_key, categories=None):
    try:
        import openai
    except ImportError:
        return ["(OpenAI 모듈 미설치, 분류 실행 불가)"] * len(paragraphs)
    openai.api_key = api_key
    results = []
    for para in paragraphs:
        prompt = (
            f"아래 텍스트를 가장 적합한 카테고리로 분류하세요."
            + (f" (카테고리: {categories})" if categories else "")
            + f"\n\n텍스트: {para}\n카테고리:"
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20,
                temperature=0
            )
            result = response['choices'][0]['message']['content'].strip()
        except Exception as e:
            result = f"분류 실패: {e}"
        results.append(result)
    return results

def ai_summarize_text(text, api_key, max_words=100):
    try:
        import openai
    except ImportError:
        return "요약 실패: openai 모듈 미설치"
    openai.api_key = api_key
    prompt = f"아래 내용을 {max_words}단어 이내로 한국어로 요약하세요.\n\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0
        )
        result = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        result = f"요약 실패: {e}"
    return result

def auto_summarize_text(text, ratio=0.2):
    """
    Gensim 기반 텍스트 요약 (OpenAI 필요 없음)
    """
    try:
        from gensim.summarization import summarize
        result = summarize(text, ratio=ratio)
        if not result:
            result = text[:max(100, int(len(text)*ratio))]
    except Exception as e:
        result = f"요약 실패: {e}"
    return result
