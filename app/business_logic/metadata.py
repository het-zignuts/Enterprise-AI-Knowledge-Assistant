from app.models.model import MetadataDocument
from sqlmodel import Session, select
from datetime import datetime, timezone

def store_metadata(filename: str, chunk_count: int, collection_name: str, session: Session):
    document=MetadataDocument(
        filename=filename,
        upload_time=datetime.utcnow(),
        chunk_count=chunk_count,
        vector_collection=collection_name
    )
    session.add(document)
    session.commit()
    session.refresh(document)
    return document

def get_metadata_docs(collection_name: str, session: Session):
    docs=session.exec(select(MetadataDocument).where(MetadataDocument.vector_collection==collection_name)).all()
    return docs