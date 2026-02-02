from app.ingestion.loader import load_document
from app.ingestion.chunker import chunk_text, normalize_text
from app.vector_db.chroma_db import create_vector_data_store
from app.rag.rag import retrieve_context
from app.core.chain import generate_answer
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent
test_file_dir=BASE_DIR/"test_data"
file_pth=test_file_dir/"leave_policy.pdf"

text=load_document(str(file_pth)) 
text=normalize_text(text)
chunks=chunk_text(text) 

vectordb=create_vector_data_store(chunks, "company_docs")

question_1="How many paid leaves do employees get?"
context_1=retrieve_context(vectordb, question_1)

print("\n=== QUESTION 1 ===")
print(generate_answer(context_1, question_1))

question_2="What is the company's stock price?"
context_2=retrieve_context(vectordb, question_2)

print("\n=== QUESTION 2 ===")
print(generate_answer(context_2, question_2))
