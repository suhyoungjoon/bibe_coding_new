"""
인덱스 관리 라우트
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import datetime
import time
import logging

from app.api.models import IndexStats, IndexBuildRequest, IndexBuildResponse
from app.core.exceptions import IndexBuildError
from app.services.index_service import IndexService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/index/stats", response_model=IndexStats)
async def get_index_stats():
    """인덱스 통계 조회"""
    try:
        index_service = IndexService()
        stats = await index_service.get_index_stats()
        
        logger.info(f"인덱스 통계 조회: {stats.total_files}개 파일, {stats.total_chunks}개 청크")
        return stats
        
    except Exception as e:
        logger.error(f"인덱스 통계 조회 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"인덱스 통계 조회 실패: {str(e)}"
        )

@router.post("/index/build", response_model=IndexBuildResponse)
async def build_index(
    request: IndexBuildRequest,
    background_tasks: BackgroundTasks
):
    """인덱스 구축"""
    start_time = time.time()
    
    try:
        logger.info("인덱스 구축 시작")
        
        index_service = IndexService()
        
        # 인덱스 구축
        result = await index_service.build_index(force_rebuild=request.force_rebuild)
        
        processing_time = time.time() - start_time
        
        response = IndexBuildResponse(
            success=True,
            files_processed=result["files_processed"],
            chunks_created=result["chunks_created"],
            processing_time=processing_time,
            message=f"인덱스 구축 완료: {result['files_processed']}개 파일, {result['chunks_created']}개 청크"
        )
        
        logger.info(f"인덱스 구축 완료: {processing_time:.2f}초")
        return response
        
    except IndexBuildError as e:
        logger.error(f"인덱스 구축 오류: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "error": e.error_type,
                "message": e.message,
                "details": e.details
            }
        )
    except Exception as e:
        logger.error(f"인덱스 구축 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"인덱스 구축 실패: {str(e)}"
        )

@router.delete("/index")
async def delete_index():
    """인덱스 삭제"""
    try:
        logger.info("인덱스 삭제 시작")
        
        index_service = IndexService()
        await index_service.delete_index()
        
        logger.info("인덱스 삭제 완료")
        return {
            "message": "인덱스가 성공적으로 삭제되었습니다.",
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"인덱스 삭제 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"인덱스 삭제 실패: {str(e)}"
        )

@router.get("/index/status")
async def get_index_status():
    """인덱스 상태 조회"""
    try:
        index_service = IndexService()
        status = await index_service.get_index_status()
        
        return status
        
    except Exception as e:
        logger.error(f"인덱스 상태 조회 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"인덱스 상태 조회 실패: {str(e)}"
        )

@router.post("/index/rebuild")
async def rebuild_index(background_tasks: BackgroundTasks):
    """인덱스 재구축 (강제)"""
    try:
        logger.info("인덱스 재구축 시작")
        
        index_service = IndexService()
        
        # 기존 인덱스 삭제
        await index_service.delete_index()
        
        # 새 인덱스 구축
        result = await index_service.build_index(force_rebuild=True)
        
        logger.info("인덱스 재구축 완료")
        return {
            "message": "인덱스가 성공적으로 재구축되었습니다.",
            "files_processed": result["files_processed"],
            "chunks_created": result["chunks_created"],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"인덱스 재구축 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"인덱스 재구축 실패: {str(e)}"
        )
