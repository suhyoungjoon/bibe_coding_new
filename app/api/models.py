"""
Pydantic 모델 정의
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class QueryRequest(BaseModel):
    """쿼리 요청 모델"""
    question: str = Field(..., description="사용자 질문", min_length=1, max_length=1000)
    include_context: bool = Field(True, description="컨텍스트 포함 여부")
    include_tools: bool = Field(True, description="도구 실행 여부")
    max_contexts: int = Field(5, description="최대 컨텍스트 수", ge=1, le=20)

class QueryResponse(BaseModel):
    """쿼리 응답 모델"""
    question: str
    answer: str
    contexts: List[Dict[str, Any]] = Field(default_factory=list)
    tool_results: Dict[str, Any] = Field(default_factory=dict)
    plan: List[str] = Field(default_factory=list)
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)

class DocumentInfo(BaseModel):
    """문서 정보 모델"""
    name: str
    path: str
    size: int
    modified_time: datetime
    file_type: str

class IndexStats(BaseModel):
    """인덱스 통계 모델"""
    total_files: int
    total_chunks: int
    index_dimension: Optional[int] = None
    last_built: Optional[datetime] = None
    index_size_mb: Optional[float] = None

class IndexBuildRequest(BaseModel):
    """인덱스 구축 요청 모델"""
    force_rebuild: bool = Field(False, description="강제 재구축 여부")

class IndexBuildResponse(BaseModel):
    """인덱스 구축 응답 모델"""
    success: bool
    files_processed: int
    chunks_created: int
    processing_time: float
    message: str

class HealthResponse(BaseModel):
    """헬스 체크 응답 모델"""
    status: str
    timestamp: datetime
    version: str
    services: Dict[str, str]

class ErrorResponse(BaseModel):
    """오류 응답 모델"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class ToolResult(BaseModel):
    """도구 실행 결과 모델"""
    tool_name: str
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: float

class ContextInfo(BaseModel):
    """컨텍스트 정보 모델"""
    source: str
    chunk: str
    score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)
