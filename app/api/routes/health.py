"""
헬스 체크 라우트
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging

from app.api.models import HealthResponse
from app.core.config import settings
from app.core.exceptions import AgenticAIException

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """시스템 헬스 체크"""
    try:
        # 기본 서비스 상태 확인
        services = {
            "database": "healthy",
            "llm": "healthy", 
            "vectorstore": "healthy",
            "index": "healthy"
        }
        
        # LLM 서비스 상태 확인
        try:
            from app.llm import LLMClient
            llm_client = LLMClient()
            if llm_client.is_mock:
                services["llm"] = "mock_mode"
            else:
                services["llm"] = "connected"
        except Exception as e:
            services["llm"] = f"error: {str(e)}"
            logger.warning(f"LLM 서비스 상태 확인 실패: {e}")
        
        # 벡터스토어 상태 확인
        try:
            from app.vectorstore.faiss_store import FaissStore
            store = FaissStore()
            if store.load():
                services["vectorstore"] = "loaded"
            else:
                services["vectorstore"] = "not_loaded"
        except Exception as e:
            services["vectorstore"] = f"error: {str(e)}"
            logger.warning(f"벡터스토어 상태 확인 실패: {e}")
        
        # 데이터베이스 상태 확인
        try:
            import sqlite3
            conn = sqlite3.connect(settings.SQLITE_DB)
            conn.close()
            services["database"] = "connected"
        except Exception as e:
            services["database"] = f"error: {str(e)}"
            logger.warning(f"데이터베이스 상태 확인 실패: {e}")
        
        # 인덱스 상태 확인
        try:
            index_path = settings.INDEX_DIR / "faiss.index"
            if index_path.exists():
                services["index"] = "exists"
            else:
                services["index"] = "not_exists"
        except Exception as e:
            services["index"] = f"error: {str(e)}"
            logger.warning(f"인덱스 상태 확인 실패: {e}")
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(),
            version=settings.VERSION,
            services=services
        )
        
    except Exception as e:
        logger.error(f"헬스 체크 실패: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"서비스 상태 확인 실패: {str(e)}"
        )

@router.get("/health/detailed")
async def detailed_health_check():
    """상세 헬스 체크"""
    try:
        health_info = {
            "timestamp": datetime.now().isoformat(),
            "version": settings.VERSION,
            "environment": {
                "debug": settings.DEBUG,
                "llm_provider": settings.LLM_PROVIDER,
                "data_dir": str(settings.DATA_DIR),
                "index_dir": str(settings.INDEX_DIR)
            },
            "services": {}
        }
        
        # 각 서비스별 상세 정보 수집
        # LLM 서비스
        try:
            from app.llm import LLMClient
            llm_client = LLMClient()
            health_info["services"]["llm"] = {
                "status": "mock_mode" if llm_client.is_mock else "connected",
                "provider": settings.LLM_PROVIDER,
                "endpoint": settings.AZURE_OPENAI_ENDPOINT
            }
        except Exception as e:
            health_info["services"]["llm"] = {"status": "error", "error": str(e)}
        
        # 벡터스토어
        try:
            from app.vectorstore.faiss_store import FaissStore
            store = FaissStore()
            if store.load():
                health_info["services"]["vectorstore"] = {
                    "status": "loaded",
                    "meta_entries": len(store.meta),
                    "dimension": store.dim
                }
            else:
                health_info["services"]["vectorstore"] = {"status": "not_loaded"}
        except Exception as e:
            health_info["services"]["vectorstore"] = {"status": "error", "error": str(e)}
        
        # 데이터베이스
        try:
            import sqlite3
            conn = sqlite3.connect(settings.SQLITE_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            health_info["services"]["database"] = {
                "status": "connected",
                "tables": [table[0] for table in tables]
            }
        except Exception as e:
            health_info["services"]["database"] = {"status": "error", "error": str(e)}
        
        return health_info
        
    except Exception as e:
        logger.error(f"상세 헬스 체크 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"상세 헬스 체크 실패: {str(e)}"
        )
