import os

def extract_text(file):
    """
    업로드된 파일에서 텍스트를 추출합니다.
    - 지원 포맷: pdf, txt, docx, md
    - Streamlit UploadedFile 객체/로컬 파일 모두 지원
    """
    # 파일 확장자 추출
    name = getattr(file, 'name', None)
    if not name:
        raise ValueError("파일 이름을 확인할 수 없습니다.")
    ext = os.path.splitext(name)[1].lower()
    if ext == ".pdf":
        return extract_pdf(file)
    elif ext in [".txt", ".md"]:
        return extract_txt(file)
    elif ext == ".docx":
        return extract_docx(file)
    else:
        raise ValueError(f"지원하지 않는 파일 유형: {ext}")

def extract_pdf(file):
    """
    PDF 파일에서 텍스트 추출 (PyPDF2 사용)
    """
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text
    except Exception as e:
        raise RuntimeError(f"PDF 추출 오류: {e}")

def extract_txt(file):
    """
    TXT/MD 파일에서 텍스트 추출
    """
    try:
        file.seek(0)
        content = file.read()
        if isinstance(content, bytes):
            return content.decode("utf-8", errors="ignore")
        return content
    except Exception as e:
        raise RuntimeError(f"텍스트 파일 추출 오류: {e}")

def extract_docx(file):
    """
    DOCX 파일에서 텍스트 추출 (python-docx 사용)
    """
    try:
        from docx import Document
        import io
        file.seek(0)
        doc = Document(io.BytesIO(file.read()))
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        raise RuntimeError(f"DOCX 추출 오류: {e}")
