# Enterprise AI Knowledge Assistant - 
## An enterprise-assistant Retrieval-Augmented Generation (RAG) system that allows organizations to upload internal documents and query them using natural language — with source attribution, metadata tracking, and usage logging.

## Tech-Stack:
- Python (3.11.x)
- FastAPI
- Uvicorn
- Pydantic
- LangChain
- Groq LLM
- ChromaDB
- Sentence Transformer Embeddings
- PostgreSQL
- SQLModel

## Users:
- Enterprise employees

## Key Features:
Features
- Document ingestion (PDFs)
- Text normalization & chunking (overlap-aware)
- Vector storage using ChromaDB
- MMR-based semantic retrieval
- LLM-powered answers with citations
- PostgreSQL metadata storage
- Query & usage logging
-  Confidence score tracking
- Production-ready architecture

## Project Structure:
```text
Enterprise-AI-Knowledge-Assistant
├── app/
│    ├── api/
│    │   ├── __init__.py
│    │   └── routes.py
│    ├── business_logic/
│    │   ├── __init__.py
│    │   ├── logs.py
│    │   └── metadata.py
│    ├── ingestion/
│    ├── __init__.py
│    │   ├── __init__.py
│    │   ├── loader.py
│    │   └── chunker.py
│    ├── vector_db/
│    │   ├── __init__.py
│    │   └── chroma_db.py
│    ├── rag/
│    │   ├── __init__.py
│    │   └── rag.py
│    ├── core/
│    │   ├── __init__.py
│    │   ├── config.py
│    │   └── chain.py
│    ├── llm/
│    │   ├── __init__.py
│    │   └── llm.py
│    ├── prompt/
│    │   ├── __init__.py
│    │   └── prompt.py
│    ├── models/
│    │   ├── __init__.py
│    │   └── model.py
│    ├── schemas/
│    │   ├── __init__.py
│    │   └── responses.py
│    ├── db/
│    ├── __init__.py
│    │   ├── init_db.py
│    │   └── session.py
│    └── main.py
├── tests/
│    ├── test_data/
│    │   └── ...
│    ├── __init__.py
│    ├── test_chain.py
│    └── test_rag.py
├── .gitignore
├── README.md
└── requirement.txt
```

## Project and Environment Setup:


- Environment Setup:

1. Clone the repo:
 ```bash
git clone https://github.com/het-zignuts/Enterprise-AI-Knowledge-Assistant.git
```

Create a new env in project folder (ensure python 3.11.x):
```bash
python -m venv .venv
```

2. Activate the environemnt:
```bash
source .venv/bin/activate
```

3. Intsall the dependencies:
```bash
pip install -r requirements.txt
```

4. Running the server:
```bash
uvicorn app.main:app --reload
```
The server starts running on (https://127.0.0.1:8000)

#### Interactive docs:
- Swagger UI → https://127.0.0.1:8000/docs
- ReDoc → https://127.0.0.1:8000/redoc

## Database Setup (Persistent Database: PostgreSQL):

```psql
CREATE USER enterprise_ai_user WITH PASSWORD 'enterprise_ai_user@1';
CREATE DATABASE enterprise_ai_db OWNER enterprise_ai_user;
GRANT ALL PRIVILEGES ON DATABASE enterprise_ai_db TO enterprise_ai_user;
```

### API Summary:

| **Request Pattern** | **Method** | **Operation**         | **Remarks**                   | **Path Operation**            |
| ------------------- | ---------- | --------------------- | ----------------------------- | ----------------------------- |
| `/upload/`          | POST       | Upload a document     | emedded and stored in vector db, metadata in Postgresql             | `upload_document(...)`         |
| `/query/`            | GET        | Ask the AI system a question         | Query embedded and context is retrieved, sent to LLM to generate response | `query_knowledge(...)`          |
| `/logs/`    | GET        | Retrieve logs of usage throughout the session    | -                        | `get_query_logs(...)`            |
| `/uploads/`    | GET        | Retrieve all uploaded docs in the session   | -        | `get_uploaded_docs(...)`         |


#### You can check the API endpoints and test them using Swagger UI at (https://127.0.0.1:8000/docs) while running the app.

### Work flow:

#### Ingestion:

                Uploaded document
                        |
                        v
                FastAPI Endpoint
                        |
                        v
            Loaded, Chunked and Embedded
                        |
                        v
    ChromaDB (Vector Store) (Embeddings stored here)
                        |
                        v
            Metadata storage (PostgreSQL)

#### Retrieval:

                    User Query
                        |
                        v
                    FastAPI Endpoint
                        |
                        v
                    Retriever (MMR)
                        |
                        v
                    ChromaDB (Vector Store)
                        |
                        v
                    Context + Metadata
                        |
                        v
                    LLM (RAG Prompt)
                        |
                        v
                    Structured Response
                        |
                        v
                    PostgreSQL Logs


## Check out the docs for FastAPI [here](https://fastapi.tiangolo.com/).
### Author:  
#### Het Shukla