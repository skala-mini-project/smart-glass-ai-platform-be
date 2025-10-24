from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # API 설정
    api_title: str = "Field Intelligence Cloud Platform - Backend"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # 벡터 데이터베이스 설정
    vector_db_type: str = "faiss"  # faiss, chroma, pinecone
    vector_db_path: str = "./rag_service/data/embeddings"
    
    # 임베딩 모델 설정
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embedding_dimension: int = 384
    
    # LLM 설정
    llm_provider: str = "openai"  # openai, anthropic, local
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # 문서 처리 설정
    chunk_size: int = 1000
    chunk_overlap: int = 200
    documents_path: str = "./rag_service/data/documents"
    
    # 로깅 설정
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
