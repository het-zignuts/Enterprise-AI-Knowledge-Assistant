from app.ingestion.loader import load_document
from app.ingestion.chunker import chunk_text, normalize_text
from app.vector_db.chroma_db import create_vector_data_store
from app.rag.rag import retrieve_context
from app.core.chain import generate_answer
from pathlib import Path

# test pdf file path
BASE_DIR=Path(__file__).resolve().parent
test_file_dir=BASE_DIR/"test_data"
file_pth=test_file_dir/"leave_policy.pdf"

#load and preprocess the text
text=load_document(str(file_pth)) 
text=normalize_text(text)
chunks=chunk_text(text) # chunking

vectordb=create_vector_data_store(chunks, "company_docs") #creating and storing embeds

question_1="How many paid leaves do employees get?" #user query 1
context_1=retrieve_context(vectordb, question_1) # context-1

print("\nQuestion-1:")
print(generate_answer(context_1, question_1)) # answer-1 from llm

question_2="What is the company's stock price?" # user query 2
context_2=retrieve_context(vectordb, question_2) # context-2

print("\nQuestion-2:")
print(generate_answer(context_2, question_2))# answer 2 from llm
