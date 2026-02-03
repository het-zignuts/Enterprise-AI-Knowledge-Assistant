from fastapi import APIRouter, UploadFile, File, HTTPException
from app.ingestion.loader import load_document
from app.ingestion.chunker import chunk_text, normalize_text
from app.vector_db.chroma_db import create_vector_data_store, load_vectordb
from app.rag.rag import retrieve_context
from app.core.chain import generate_answer
import shutil
import os
from app.business_logic.metadata import *
from app.business_logic.logs import *
from app.db.session import db_session_manager
from fastapi import Depends

router = APIRouter()

VECTOR_DB_COLLECTION="company_docs"
UPLOAD_DIR="uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/")
def health():
    return {"status": "ok"}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), session: Session = Depends(db_session_manager.get_session)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only .pdf files supported."
        )
    file_path=os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text=load_document(file_path)
    chunks=chunk_text(text)
    document=store_metadata(file.filename, len(chunks), VECTOR_DB_COLLECTION, session)
    metadata=[
        {
            "document_id": document.id,
            "filename": file.filename,
            "chunk_id": i
        }
        for i in range(len(chunks))
    ]
    vectordb=create_vector_data_store(chunks, VECTOR_DB_COLLECTION, metadata)
    return {
        "status": "success",
        "document": file.filename,
        "chunks_created": len(chunks)
    }

@router.post("/query")
async def query_knowledge(question: str, session: Session = Depends(db_session_manager.get_session)):
    vectordb=load_vectordb(VECTOR_DB_COLLECTION)
    if vectordb is None:
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet"
        )
    doc_ids, context=retrieve_context(vectordb, question)
    response=generate_answer(context, question)
    log=store_logs(response["question"], response["answer"], doc_ids, response["confidence"], session)
    return response

@router.get("/logs")
async def get_query_logs(session: Session = Depends(db_session_manager.get_session)):
    logs=get_logs(session)
    return logs

@router.get("/uploads")
async def get_uploaded_docs(session: Session = Depends(db_session_manager.get_session)):
    docs=get_metadata_docs(VECTOR_DB_COLLECTION, session)
    return docs