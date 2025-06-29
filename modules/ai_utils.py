import openai
from typing import List, Optional

def ai_classify_paragraphs(
    paragraphs: List[str],
    api_key: str,
    categories: Optional[List[str]] = None
) -> List[str]:
    """
    여러 문단(혹은 문장)을 OpenAI로 자동 분류
    :param paragraphs: 분류 대상 문단 리스트
    :param api_key: OpenAI API KEY
    :param categories: 카테고리 리스트(없으면 AI가 자유 분류)
    :return: 각 문단별 분류 결과 리스트
    """
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
