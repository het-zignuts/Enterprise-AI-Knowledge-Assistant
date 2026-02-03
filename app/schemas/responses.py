from pydantic import BaseModel
from typing import List

class SourceQuotation(BaseModel):
    source: str
    quoted_context: str

class AssistantResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceQuotation]
    confidence: float