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

# FastAPI Router instance
router=APIRouter()

# Defining global vars
VECTOR_DB_COLLECTION="company_docs" # collection name for storing embeddings for enterprise docs
UPLOAD_DIR="uploads" # directory name for uploaded files.

os.makedirs(UPLOAD_DIR, exist_ok=True) # create the direcory if not already exists

# API endpoint to upload PDFs.
@router.post("/upload")
async def upload_document(file: UploadFile = File(...), session: Session = Depends(db_session_manager.get_session)): # path handler with dependencies to support file upload and get database session
    if not file.filename.endswith(".pdf"): # support only pdf upload
        raise HTTPException(
            status_code=400,
            detail="Only .pdf files supported."
        )
    file_path=os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f) # copy the file to the specified directory

    text=load_document(file_path) # load the text from the file
    chunks=chunk_text(text) # chunking the text
    document=store_metadata(file.filename, len(chunks), VECTOR_DB_COLLECTION, session) # store meteadata about the file.
    metadata=[
        {
            "document_id": document.id,
            "filename": file.filename,
            "chunk_id": i
        }
        for i in range(len(chunks))
    ]
    vectordb=create_vector_data_store(chunks, VECTOR_DB_COLLECTION, metadata) # generate and store the embeddings into the vector db.
    return {
        "status": "success",
        "document": file.filename,
        "chunks_created": len(chunks)
    }

# API endpoint to pass query to LLM and retrieve response.
@router.post("/query")
async def query_knowledge(question: str, session: Session = Depends(db_session_manager.get_session)):
    vectordb=load_vectordb(VECTOR_DB_COLLECTION) # load the vector db instance with given collection
    if vectordb is None:
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet"
        )
    doc_ids, context=retrieve_context(vectordb, question) # retrieve relevant context for the query through the function 
    response=generate_answer(context, question) # pass the query and context to the chain to invoke response.
    log=store_logs(response["question"], response["answer"], doc_ids, response["confidence"], session) # log the response fields
    return response # forward the response

# API endpoit to get logs throughout the session
@router.get("/logs")
async def get_query_logs(session: Session = Depends(db_session_manager.get_session)):
    logs=get_logs(session) # calling the business logic to retrieve logs
    return logs

# API endpoint to retrieve documents uploaded.
@router.get("/uploads")
async def get_uploaded_docs(session: Session = Depends(db_session_manager.get_session)):
    docs=get_metadata_docs(VECTOR_DB_COLLECTION, session) # call to the appropriate business logic for the retrieval.
    return docs