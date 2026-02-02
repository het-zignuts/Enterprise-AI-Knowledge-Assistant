from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def load_document(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError("Document not found")
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")
    elif path.suffix.lower() == ".pdf":
        loader = PyPDFLoader(str(path))
        pages = loader.load()
        text = "\n\n".join(page.page_content for page in pages)
        return text 
    else:
        raise ValueError("Unsupported file type. Only .txt and .pdf are supported.")
