"""
애플리케이션 설정 관리
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 기본 설정
    APP_NAME: str = "Agentic AI API"
    VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    # 디렉토리 설정
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "app" / "data" / "docs"
    INDEX_DIR: Path = BASE_DIR / "app" / "data" / "index"
    
    # LLM 설정
    LLM_PROVIDER: str = "azure"
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_VERSION: str = "2024-06-01"
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-4o-mini"
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT: str = "text-embedding-3-small"
    
    # 데이터베이스 설정
    SQLITE_DB: str = str(BASE_DIR / "app" / "data" / "demo.db")
    
    # PostgreSQL 설정 (AI 학습 및 프로젝트 관리용)
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "agentic_ai"
    POSTGRES_USER: str = "agentic_user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_URL: str = "postgresql://agentic_user:password@localhost:5432/agentic_ai"
    
    # API 설정
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Agentic AI"
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# 전역 설정 인스턴스
settings = Settings()

# 디렉토리 생성
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.INDEX_DIR.mkdir(parents=True, exist_ok=True)
