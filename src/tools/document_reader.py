from langchain.tools import tool
from pypdf import PdfReader
from docx import Document

@tool
def read_document(file_path: str) -> str:
    """Reads text from PDF, DOCX, or TXT."""
    try:
        text = ""
        if file_path.lower().endswith('.pdf'):
            reader = PdfReader(file_path)
            for page in reader.pages: text += page.extract_text() or ""
        elif file_path.lower().endswith('.docx'):
            doc = Document(file_path)
            for para in doc.paragraphs: text += para.text + "\n"
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r') as f: text = f.read()
        else: return "Error: Unsupported file type. Use .pdf, .docx, or .txt."
        return f"Successfully read document '{file_path}'. Content:\n\n{text}"
    except Exception as e: return f"Error reading document: {e}"