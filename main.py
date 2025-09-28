"""
FastAPI 메인 애플리케이션
Agentic AI 시스템의 REST API 서버
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import logging

from app.api.routes import query, documents, index, health, websocket, improved_demo, ui_enhancements, sandbox, enhanced_sandbox_demo
from app.core.config import settings
from app.core.exceptions import AgenticAIException

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # 시작 시 실행
    logger.info("🚀 Agentic AI FastAPI 서버 시작")
    logger.info(f"📁 데이터 디렉토리: {settings.DATA_DIR}")
    logger.info(f"📁 인덱스 디렉토리: {settings.INDEX_DIR}")
    logger.info(f"🤖 LLM 프로바이더: {settings.LLM_PROVIDER}")
    
    yield
    
    # 종료 시 실행
    logger.info("🛑 Agentic AI FastAPI 서버 종료")

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="Agentic AI API",
    description="Azure OpenAI + FAISS/BM25 + Self-Critique + Code Execution API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 예외 처리기
@app.exception_handler(AgenticAIException)
async def agentic_ai_exception_handler(request, exc: AgenticAIException):
    """AgenticAI 커스텀 예외 처리"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_type,
            "message": exc.message,
            "details": exc.details
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """일반 예외 처리"""
    logger.error(f"예상치 못한 오류 발생: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "서버 내부 오류가 발생했습니다.",
            "details": str(exc) if settings.DEBUG else None
        }
    )

# 라우터 등록
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])
app.include_router(index.router, prefix="/api/v1", tags=["index"])
app.include_router(websocket.router, prefix="/api/v1", tags=["websocket"])
app.include_router(improved_demo.router, prefix="/api/v1", tags=["demo"])
app.include_router(ui_enhancements.router, prefix="/api/v1", tags=["ui"])
app.include_router(sandbox.router, prefix="/api/v1/sandbox", tags=["sandbox"])
app.include_router(enhanced_sandbox_demo.router, prefix="/api/v1", tags=["demo"])

# 루트 엔드포인트
@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Agentic AI API 서버가 실행 중입니다",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health",
        "sandbox": "/api/v1/sandbox",
        "enhanced_sandbox_demo": "/api/v1/demo/sandbox",
        "simple_sandbox_demo": "/api/v1/demo/sandbox/simple"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
