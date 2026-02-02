from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ingestion.loader import load_document
from app.ingestion.chunker import chunk_text, normalize_text
from app.vector_db.chroma_db import create_vector_data_store, load_vectordb
from app.rag.rag import retrieve_context
from app.core.chain import generate_answer
import shutil
import os

router = APIRouter()

VECTOR_DB_COLLECTION="company_docs"
UPLOAD_DIR="uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only .pdf files supported."
        )
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text=load_document(file_path)
    chunks=chunk_text(text)
    vectordb=create_vector_data_store(chunks, VECTOR_DB_COLLECTION)
    return {
        "status": "success",
        "document": file.filename,
        "chunks_created": len(chunks)
    }

@router.post("/query")
async def query_knowledge(question: str):
    vectordb=load_vectordb(VECTOR_DB_COLLECTION)
    if vectordb is None:
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet"
        )
    context=retrieve_context(vectordb, question)
    answer=generate_answer(context, question)
    return {
        "question": question,
        "response": answer
    }

