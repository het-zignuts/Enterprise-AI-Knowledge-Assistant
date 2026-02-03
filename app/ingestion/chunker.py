from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

def chunk_text(text: str):
    """
    This function creates chunks from the text extracted from the file.
    """
    # Splitter instance
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500, # generally, a couple of paragraphs for semantic completeness
        chunk_overlap=100, # ensures across-the-chunk-boundry info not lost
        separators=["\n\n", "\n", ".", " ", ""] # seperating characters for chunking.
    )
    return splitter.split_text(text)

def normalize_text(text: str) -> str:
    """
    This function normalizes the text before chunkig to ensure clean etx boundries. 
    Ensures no extra spaces, line breaks, extra numberings (page no.s, index, title, etc.)
    """
    text = re.sub(r"\n{2,}", "\n\n", text) # convert multiple line breaks to paragraph sepearation
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text) # replace single newline character with white space 
    text = re.sub(r"\s+", " ", text) # replace multiple spaces, tabs, etc. with single space.
    #trim trailing and leading whitespaces before returning as normalized text
    return text.strip()
