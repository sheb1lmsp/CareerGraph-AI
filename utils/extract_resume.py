import fitz  # PyMuPDF — for reading PDF files
from docx import Document  # for reading .docx files

def extract_resume_text(file_path: str) -> str:
    """
    Extract clean text from resume files (.pdf or .docx).

    Automatically detects the file type and extracts textual content accordingly.

    Args:
        file_path (str): Path to the resume file.

    Returns:
        str: Extracted plain text content.
    """

    # Handle PDF resume extraction
    if file_path.endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text("text") + "\n"
        return text.strip()

    # Handle DOCX resume extraction
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text.strip()

    # Unsupported file format
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX resume.")
