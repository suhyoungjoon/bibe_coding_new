"""
커스텀 예외 클래스들
"""

from typing import Optional, Dict, Any

class AgenticAIException(Exception):
    """AgenticAI 기본 예외 클래스"""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_type: str = "AgenticAIError",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.details = details or {}
        super().__init__(self.message)

class IndexBuildError(AgenticAIException):
    """인덱스 구축 오류"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_type="IndexBuildError",
            details=details
        )

class DocumentNotFoundError(AgenticAIException):
    """문서를 찾을 수 없음"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=404,
            error_type="DocumentNotFoundError",
            details=details
        )

class QueryProcessingError(AgenticAIException):
    """쿼리 처리 오류"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=400,
            error_type="QueryProcessingError",
            details=details
        )

class LLMServiceError(AgenticAIException):
    """LLM 서비스 오류"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=503,
            error_type="LLMServiceError",
            details=details
        )

class ToolExecutionError(AgenticAIException):
    """도구 실행 오류"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_type="ToolExecutionError",
            details=details
        )
