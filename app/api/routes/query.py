"""
쿼리 처리 라우트
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import datetime
import time
import logging

from app.api.models import QueryRequest, QueryResponse, ErrorResponse
from app.core.exceptions import QueryProcessingError, LLMServiceError, ToolExecutionError
from app.services.query_service import QueryService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """사용자 쿼리 처리"""
    start_time = time.time()
    
    try:
        logger.info(f"쿼리 처리 시작: {request.question[:100]}...")
        
        # 쿼리 서비스 인스턴스 생성
        query_service = QueryService()
        
        # 쿼리 처리
        result = await query_service.process_query(
            question=request.question,
            include_context=request.include_context,
            include_tools=request.include_tools,
            max_contexts=request.max_contexts
        )
        
        processing_time = time.time() - start_time
        
        response = QueryResponse(
            question=request.question,
            answer=result.get("final", "답변을 생성할 수 없습니다."),
            contexts=result.get("contexts", []),
            tool_results=result.get("tool_results", {}),
            plan=result.get("plan", []),
            processing_time=processing_time,
            timestamp=datetime.now()
        )
        
        logger.info(f"쿼리 처리 완료: {processing_time:.2f}초")
        return response
        
    except QueryProcessingError as e:
        logger.error(f"쿼리 처리 오류: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "error": e.error_type,
                "message": e.message,
                "details": e.details
            }
        )
    except LLMServiceError as e:
        logger.error(f"LLM 서비스 오류: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "error": e.error_type,
                "message": e.message,
                "details": e.details
            }
        )
    except ToolExecutionError as e:
        logger.error(f"도구 실행 오류: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "error": e.error_type,
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        logger.error(f"예상치 못한 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "서버 내부 오류가 발생했습니다.",
                "details": str(e)
            }
        )

@router.post("/query/stream")
async def process_query_stream(request: QueryRequest):
    """스트리밍 쿼리 처리 (향후 구현)"""
    # TODO: 스트리밍 응답 구현
    raise HTTPException(
        status_code=501,
        detail="스트리밍 기능은 아직 구현되지 않았습니다."
    )

@router.get("/query/history")
async def get_query_history(limit: int = 10, offset: int = 0):
    """쿼리 히스토리 조회 (향후 구현)"""
    # TODO: 쿼리 히스토리 저장 및 조회 구현
    return {
        "message": "쿼리 히스토리 기능은 아직 구현되지 않았습니다.",
        "limit": limit,
        "offset": offset
    }
