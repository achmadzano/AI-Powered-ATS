import fitz  # PyMuPDF for PDF extraction
import docx
from typing import Optional

def extract_text_from_pdf(file_path: str) -> Optional[str]:
    """Extract text from a PDF using PyMuPDF (fitz)."""
    try:
        doc = fitz.open(file_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text.strip() if text else None
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return None

def extract_text_from_docx(file_path: str) -> Optional[str]:
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join(para.text for para in doc.paragraphs)
        return text.strip() if text else None
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        return None

def extract_text(file_path: str) -> Optional[str]:
    """Detect file format and extract text."""
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        print("Unsupported file format")
        return None
