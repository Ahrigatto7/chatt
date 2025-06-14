import os
import openai


def ask_document_question(doc_text: str, question: str) -> str:
    """Use OpenAI ChatGPT model to answer a question about a document."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY 환경변수가 설정되어 있지 않습니다."
    openai.api_key = api_key
    prompt = (
        "다음 문서를 참고하여 사용자 질문에 답변하세요.\n"
        "문서:\n" + doc_text + "\n"
        "질문: " + question
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"오류가 발생했습니다: {e}"

