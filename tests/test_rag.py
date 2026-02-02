import os
from pathlib import Path
from app.ingestion.loader import load_document 
from app.ingestion.chunker import chunk_text, normalize_text 
from app.vector_db.chroma_db import create_vector_data_store 
from app.rag.rag import retrieve_context 

BASE_DIR=Path(__file__).resolve().parent
test_file_dir=BASE_DIR/"test_data"
file_pth=test_file_dir/"attire_policy.pdf"

text=load_document(str(file_pth)) 
text=normalize_text(text)
chunks=chunk_text(text) 
print(f"Chunks created: {len(chunks)}") 

vectordb=create_vector_data_store(chunks, "company_attire_policy") 
question = "Can I wear formals to zignuts technolab?" 
context = retrieve_context(vectordb, question) 

if context is None: 
    print("No matching information identified.") 
else: 
    print("Retrieved context:") 

print(context)