import re
import os
import pdfplumber
import tempfile


def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def process_file(file):
    if isinstance(file, str):
        return clean_text(file)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        path = tmp.name

    if file.name.endswith(".pdf"):
        text = extract_text_from_pdf(path)
    elif file.name.endswith(".txt"):
        text = read_txt(path)

    os.remove(path)
    return clean_text(text)
