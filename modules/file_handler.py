from docx import Document

def extract_text(file):
    suffix = file.name.split(".")[-1]
    if suffix == "docx":
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        return file.read().decode("utf-8")
