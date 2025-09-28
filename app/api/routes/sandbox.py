"""
샌드박스 전용 API 엔드포인트
향상된 샌드박스 기능을 위한 REST API
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

from ...services.enhanced_sandbox_service import (
    EnhancedSandboxService, 
    ExecutionMode, 
    SecurityLevel, 
    ResourceLimits
)
from ...services.result_visualization_service import ResultVisualizationService

logger = logging.getLogger(__name__)

router = APIRouter()

# 전역 서비스 인스턴스
sandbox_service = EnhancedSandboxService()
visualization_service = ResultVisualizationService()

# Pydantic 모델들
class CodeExecutionRequest(BaseModel):
    """코드 실행 요청"""
    code: str = Field(..., description="실행할 코드")
    language: str = Field(default="python", description="프로그래밍 언어")
    user_id: str = Field(default="default", description="사용자 ID")
    execution_mode: str = Field(default="auto", description="실행 모드 (auto/docker/local)")
    security_level: str = Field(default="medium", description="보안 수준 (low/medium/high/maximum)")
    custom_resource_limits: Optional[Dict[str, Any]] = Field(None, description="커스텀 리소스 제한")

class CodeExecutionResponse(BaseModel):
    """코드 실행 응답"""
    success: bool
    output: str
    error: str
    execution_time: float
    memory_usage_mb: float
    cpu_usage_percent: float
    language: str
    method: str
    security_level: str
    resource_limits: Dict[str, Any]
    metadata: Dict[str, Any]

class ExecutionHistoryResponse(BaseModel):
    """실행 히스토리 응답"""
    execution_id: str
    user_id: str
    language: str
    execution_mode: str
    security_level: str
    timestamp: str
    success: bool
    execution_time: float

class SystemStatsResponse(BaseModel):
    """시스템 통계 응답"""
    docker_available: bool
    active_users: int
    total_executions: int
    supported_languages: int
    memory_usage: float
    cpu_usage: float
    timestamp: str

class SupportedLanguagesResponse(BaseModel):
    """지원 언어 목록 응답"""
    languages: Dict[str, Dict[str, Any]]

@router.post("/execute", response_model=CodeExecutionResponse)
async def execute_code(request: CodeExecutionRequest):
    """코드 실행"""
    try:
        # 실행 모드 변환
        execution_mode = ExecutionMode(request.execution_mode)
        security_level = SecurityLevel(request.security_level)
        
        # 커스텀 리소스 제한 처리
        custom_limits = None
        if request.custom_resource_limits:
            custom_limits = ResourceLimits(**request.custom_resource_limits)
        
        # 코드 실행
        result = await sandbox_service.execute_code_enhanced(
            code=request.code,
            language=request.language,
            user_id=request.user_id,
            execution_mode=execution_mode,
            security_level=security_level,
            custom_resource_limits=custom_limits
        )
        
        return CodeExecutionResponse(
            success=result.success,
            output=result.output,
            error=result.error,
            execution_time=result.execution_time,
            memory_usage_mb=result.memory_usage_mb,
            cpu_usage_percent=result.cpu_usage_percent,
            language=result.language,
            method=result.method,
            security_level=result.security_level,
            resource_limits=result.resource_limits,
            metadata=result.metadata
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"잘못된 파라미터: {str(e)}")
    except Exception as e:
        logger.error(f"코드 실행 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"코드 실행 실패: {str(e)}")

@router.get("/languages", response_model=SupportedLanguagesResponse)
async def get_supported_languages():
    """지원하는 언어 목록 조회"""
    try:
        languages = sandbox_service.get_supported_languages()
        return SupportedLanguagesResponse(languages=languages)
    except Exception as e:
        logger.error(f"언어 목록 조회 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"언어 목록 조회 실패: {str(e)}")

@router.get("/history", response_model=List[ExecutionHistoryResponse])
async def get_execution_history(
    user_id: Optional[str] = None,
    limit: int = 100
):
    """실행 히스토리 조회"""
    try:
        history = sandbox_service.get_execution_history(user_id=user_id, limit=limit)
        
        response = []
        for item in history:
            result = item["result"]
            response.append(ExecutionHistoryResponse(
                execution_id=result["metadata"]["execution_id"],
                user_id=item["user_id"],
                language=item["language"],
                execution_mode=item["execution_mode"],
                security_level=item["security_level"],
                timestamp=item["timestamp"],
                success=result["success"],
                execution_time=result["execution_time"]
            ))
        
        return response
        
    except Exception as e:
        logger.error(f"실행 히스토리 조회 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"실행 히스토리 조회 실패: {str(e)}")

@router.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats():
    """시스템 통계 조회"""
    try:
        stats = sandbox_service.get_system_stats()
        return SystemStatsResponse(**stats)
    except Exception as e:
        logger.error(f"시스템 통계 조회 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"시스템 통계 조회 실패: {str(e)}")

@router.delete("/cleanup/{user_id}")
async def cleanup_user_data(user_id: str):
    """사용자 데이터 정리"""
    try:
        sandbox_service.cleanup_user_data(user_id)
        return {"message": f"사용자 {user_id}의 데이터가 정리되었습니다."}
    except Exception as e:
        logger.error(f"사용자 데이터 정리 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"사용자 데이터 정리 실패: {str(e)}")

@router.post("/validate")
async def validate_code_security(request: CodeExecutionRequest):
    """코드 보안 검증"""
    try:
        security_level = SecurityLevel(request.security_level)
        is_secure, message = sandbox_service._validate_code_security(
            request.code, 
            request.language, 
            security_level
        )
        
        return {
            "is_secure": is_secure,
            "message": message,
            "language": request.language,
            "security_level": request.security_level
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"잘못된 파라미터: {str(e)}")
    except Exception as e:
        logger.error(f"코드 보안 검증 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"코드 보안 검증 실패: {str(e)}")

@router.get("/languages")
async def get_supported_languages():
    """지원 언어 목록 조회"""
    try:
        languages = sandbox_service.get_supported_languages()
        return {
            "success": True,
            "languages": list(languages.keys()),
            "details": languages,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"지원 언어 조회 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"지원 언어 조회 실패: {str(e)}")

@router.get("/stats")
async def get_system_stats():
    """시스템 통계 조회"""
    try:
        stats = sandbox_service.get_system_stats()
        return {
            "success": True,
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"시스템 통계 조회 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"시스템 통계 조회 실패: {str(e)}")

@router.get("/health")
async def health_check():
    """샌드박스 서비스 상태 확인"""
    try:
        stats = sandbox_service.get_system_stats()
        return {
            "status": "healthy",
            "docker_available": stats["docker_available"],
            "supported_languages": stats["supported_languages"],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"헬스 체크 실패: {e}", exc_info=True)
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.post("/execute-with-visualization")
async def execute_code_with_visualization(
    request: CodeExecutionRequest,
    background_tasks: BackgroundTasks
):
    """코드 실행 및 결과 시각화"""
    try:
        logger.info(f"코드 실행 요청 (시각화 포함): {request.language}")
        
        # 실행 모드 변환
        execution_mode = ExecutionMode.AUTO
        if request.execution_mode == "docker":
            execution_mode = ExecutionMode.DOCKER
        elif request.execution_mode == "local":
            execution_mode = ExecutionMode.LOCAL
        
        # 보안 레벨 변환
        security_level = SecurityLevel.MEDIUM
        if request.security_level == "low":
            security_level = SecurityLevel.LOW
        elif request.security_level == "high":
            security_level = SecurityLevel.HIGH
        elif request.security_level == "maximum":
            security_level = SecurityLevel.MAXIMUM
        
        # 커스텀 리소스 제한 처리
        custom_limits = None
        if request.custom_resource_limits:
            custom_limits = ResourceLimits(**request.custom_resource_limits)
        
        # 코드 실행
        result = await sandbox_service.execute_code_enhanced(
            code=request.code,
            language=request.language,
            user_id=request.user_id,
            execution_mode=execution_mode,
            security_level=security_level,
            custom_resource_limits=custom_limits
        )
        
        # 결과 데이터 준비
        result_data = {
            "success": result.success,
            "output": result.output,
            "error": result.error,
            "execution_time": result.execution_time,
            "memory_used": result.memory_usage_mb,
            "cpu_usage": result.cpu_usage_percent,
            "language": request.language,
            "security_level": request.security_level
        }
        
        # 시각화 생성
        visualization = await visualization_service.visualize_result(result_data)
        
        # 응답 구성
        response_data = {
            "success": result.success,
            "output": result.output,
            "error": result.error,
            "execution_time": result.execution_time,
            "memory_usage_mb": result.memory_usage_mb,
            "cpu_usage_percent": result.cpu_usage_percent,
            "language": request.language,
            "method": "enhanced_sandbox",
            "security_level": request.security_level,
            "resource_limits": request.custom_resource_limits or {},
            "metadata": {
                "execution_id": getattr(result, 'execution_id', None),
                "timestamp": datetime.now().isoformat()
            },
            "visualization": visualization
        }
        
        # 백그라운드에서 실행 히스토리 저장 (메서드가 있는 경우에만)
        if hasattr(sandbox_service, '_save_execution_history'):
            background_tasks.add_task(
                sandbox_service._save_execution_history,
                result_data,
                request.user_id
            )
        
        return response_data
        
    except Exception as e:
        logger.error(f"코드 실행 및 시각화 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"코드 실행 및 시각화 실패: {str(e)}")

@router.post("/visualize-result")
async def visualize_execution_result(result_data: Dict[str, Any]):
    """실행 결과 시각화만 수행"""
    try:
        visualization_type = result_data.pop("visualization_type", "auto")
        visualization = await visualization_service.visualize_result(
            result_data, 
            visualization_type
        )
        
        return {
            "success": True,
            "visualization": visualization,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"결과 시각화 실패: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"결과 시각화 실패: {str(e)}")

@router.get("/visualization-types")
async def get_visualization_types():
    """사용 가능한 시각화 타입 목록"""
    return {
        "success": True,
        "visualization_types": {
            "auto": "자동 감지",
            "chart": "차트",
            "table": "테이블",
            "graph": "그래프",
            "timeline": "타임라인",
            "metrics": "메트릭",
            "default": "기본"
        },
        "timestamp": datetime.now().isoformat()
    }
