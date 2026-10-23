"""Read supported text documents (.txt, .pdf, .docx)."""
from pathlib import Path

SUPPORTED_EXTENSIONS = {'.txt', '.pdf', '.docx'}

def read_document(path: str | Path) -> str:
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f'Unsupported file type: {suffix}. Use TXT, PDF, or DOCX.')
    if not file_path.is_file():
        raise FileNotFoundError(file_path)
    if suffix == '.txt':
        return file_path.read_text(encoding='utf-8')
    if suffix == '.pdf':
        from pypdf import PdfReader
        reader = PdfReader(str(file_path))
        return '\n'.join(page.extract_text() or '' for page in reader.pages).strip()
    from docx import Document
    doc = Document(str(file_path))
    return '\n'.join(p.text for p in doc.paragraphs if p.text.strip()).strip()
