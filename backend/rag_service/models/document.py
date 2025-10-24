from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Document(BaseModel):
    """문서 모델"""
    id: str
    title: str
    content: str
    domain: str
    file_path: str
    page_number: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class QueryRequest(BaseModel):
    """쿼리 요청 모델"""
    query: str
    domain: Optional[str] = None
    top_k: int = 5
    threshold: float = 0.7

class SourceDocument(BaseModel):
    """소스 문서 모델"""
    document: str
    page: Optional[int] = None
    content: str
    similarity: float

class QueryResponse(BaseModel):
    """쿼리 응답 모델"""
    answer: str
    sources: List[SourceDocument]
    processing_time: float
