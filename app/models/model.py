from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy import Column, JSON

class MetadataDocument(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    chunk_count: Optional[int] = None
    vector_collection: Optional[str] = None

class QueryLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: Optional[str] = None
    answer: Optional[str] = None
    document_ids: Optional[List[Dict]] = Field(
        default=None,
        sa_column=Column(JSON)
    )
    confidence: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
