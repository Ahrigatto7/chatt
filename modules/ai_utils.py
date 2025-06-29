def auto_summarize_text(text, ratio=0.2):
    from gensim.summarization import summarize
    try:
        result = summarize(text, ratio=ratio)
        if not result:
            result = text[:max(100, int(len(text)*ratio))]
    except Exception as e:
        result = f"요약 실패: {e}"
    return result

def ai_classify_paragraphs(paragraphs, api_key, categories=None):
    import openai  # 함수 내부에서만 import
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

def ai_summarize_text(
    text: str,
    api_key: str,
    max_words: int = 100
) -> str:
    """
    텍스트를 지정한 길이로 요약 (OpenAI)
    :param text: 요약할 텍스트
    :param api_key: OpenAI API KEY
    :param max_words: 요약 단어 수 제한
    :return: 요약 결과(str)
    """
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
