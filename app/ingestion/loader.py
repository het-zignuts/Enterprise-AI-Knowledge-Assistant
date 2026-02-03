from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

def load_document(file_path: str) -> str:
    """
    This function loades the PDF file from the path specified.
    """
    path=Path(file_path)
    if not path.exists():
        raise FileNotFoundError("Document not found")
    if path.suffix.lower()==".txt":
        return path.read_text(encoding="utf-8") # return the read file content if it is a text file
    elif path.suffix.lower()==".pdf": # if the file is in PDF format
        loader=PyPDFLoader(str(path)) # create loader instance with the file path
        pages=loader.load() # load the file content
        text="\n\n".join(page.page_content for page in pages) # concatenate the content pages into a single text blob
        return text 
    else:
        raise ValueError("Unsupported file type. Only .txt and .pdf are supported.")
