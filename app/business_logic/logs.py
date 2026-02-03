from app.models.model import QueryLog
from sqlmodel import Session, select
from datetime import datetime, timezone
from typing import List

def store_logs(question: str|None, answer: str|None, document_ids: List[str] | None, confidence: float | None, session: Session):
    """
    business logic to store query logs.
    """
    # creating model instance
    log=QueryLog(
        question=question,
        answer=answer,
        document_ids=document_ids,
        confidence=confidence,
        timestamp=datetime.utcnow()
    )
    # Adding to db
    session.add(log)
    session.commit() # committing the changes
    session.refresh(log) # refreshing session by updating the model object with latest set fields.
    return log

def get_logs(session: Session):
    """
    Retrieving logs from the database.
    """
    logs=session.exec(select(QueryLog)).all()
    return logs