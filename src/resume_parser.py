from pathlib import Path

import fitz  # PyMuPDF
from docx import Document


def extract_text_from_pdf(file_path):
    """Extract text from a PDF resume."""

    text = []

    with fitz.open(file_path) as pdf:
        for page in pdf:
            page_text = page.get_text()
            if page_text.strip():
                text.append(page_text)

    return "\n".join(text)


def extract_text_from_docx(file_path):
    """Extract text from a DOCX resume."""

    document = Document(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_resume_text(file_path):
    """Extract text based on the resume file extension."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Resume file not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(path)

    elif extension == ".docx":
        return extract_text_from_docx(path)

    else:
        raise ValueError(
            "Unsupported file format. Please provide a PDF or DOCX file."
        )


if __name__ == "__main__":
    file_path = input("Enter the resume file path: ").strip().strip('"')

    try:
        resume_text = extract_resume_text(file_path)

        if resume_text.strip():
            print("\n===== Extracted Resume Text =====\n")
            print(resume_text)
        else:
            print(
                "No readable text found. "
                "The PDF may be scanned or image-based."
            )

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")