from app.models.model import QueryLog
from sqlmodel import Session, select
from datetime import datetime, timezone
from typing import List

def store_logs(question: str|None, answer: str|None, document_ids: List[str] | None, confidence: float | None, session: Session):
    log=QueryLog(
        question=question,
        answer=answer,
        document_ids=document_ids,
        confidence=confidence,
        timestamp=datetime.utcnow()
    )
    session.add(log)
    session.commit()
    session.refresh(log)
    return log

def get_logs(session: Session):
    logs=session.exec(select(QueryLog)).all()
    return logs