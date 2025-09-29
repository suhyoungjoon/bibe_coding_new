"""
Railway 디버깅용 라우트
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging
import os
import sys
import platform
import traceback
from pathlib import Path

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/debug/railway")
async def railway_debug():
    """Railway 환경 디버깅 정보"""
    try:
        debug_info = {
            "timestamp": datetime.now().isoformat(),
            "environment": {
                "railway_environment": os.getenv('RAILWAY_ENVIRONMENT'),
                "railway_project_id": os.getenv('RAILWAY_PROJECT_ID'),
                "railway_service_id": os.getenv('RAILWAY_SERVICE_ID'),
                "port": os.getenv('PORT'),
                "host": os.getenv('HOST'),
                "python_version": sys.version,
                "platform": platform.platform(),
                "working_directory": os.getcwd(),
                "python_path": sys.path[:5]  # 처음 5개만
            },
            "files": {
                "main_py_exists": Path("main.py").exists(),
                "requirements_txt_exists": Path("requirements.txt").exists(),
                "railway_json_exists": Path("railway.json").exists(),
                "dockerfile_exists": Path("Dockerfile").exists(),
                "app_dir_exists": Path("app").exists(),
                "vectorstore_dir_exists": Path("app/vectorstore").exists()
            },
            "imports": {
                "fastapi": False,
                "uvicorn": False,
                "app_modules": {}
            }
        }
        
        # 모듈 import 테스트
        try:
            import fastapi
            debug_info["imports"]["fastapi"] = True
            debug_info["imports"]["fastapi_version"] = fastapi.__version__
        except Exception as e:
            debug_info["imports"]["fastapi_error"] = str(e)
        
        try:
            import uvicorn
            debug_info["imports"]["uvicorn"] = True
            debug_info["imports"]["uvicorn_version"] = uvicorn.__version__
        except Exception as e:
            debug_info["imports"]["uvicorn_error"] = str(e)
        
        # app 모듈들 테스트
        app_modules = [
            "app.core.config",
            "app.api.routes.health",
            "app.vectorstore.faiss_store",
            "app.services.live_coding_service",
            "app.services.enhanced_sandbox_service"
        ]
        
        for module in app_modules:
            try:
                __import__(module)
                debug_info["imports"]["app_modules"][module] = True
            except Exception as e:
                debug_info["imports"]["app_modules"][module] = {
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
        
        return debug_info
        
    except Exception as e:
        logger.error(f"Railway 디버그 정보 수집 실패: {e}")
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/debug/startup")
async def startup_debug():
    """애플리케이션 시작 과정 디버깅"""
    try:
        startup_info = {
            "timestamp": datetime.now().isoformat(),
            "startup_steps": {
                "1_config_import": False,
                "2_main_import": False,
                "3_fastapi_app": False,
                "4_routers": False
            },
            "errors": []
        }
        
        # 1. config import 테스트
        try:
            from app.core.config import settings
            startup_info["startup_steps"]["1_config_import"] = True
            startup_info["config"] = {
                "data_dir": str(settings.DATA_DIR),
                "index_dir": str(settings.INDEX_DIR),
                "llm_provider": settings.LLM_PROVIDER
            }
        except Exception as e:
            startup_info["startup_steps"]["1_config_import"] = False
            startup_info["errors"].append(f"Config import failed: {str(e)}")
        
        # 2. main import 테스트
        try:
            import main
            startup_info["startup_steps"]["2_main_import"] = True
        except Exception as e:
            startup_info["startup_steps"]["2_main_import"] = False
            startup_info["errors"].append(f"Main import failed: {str(e)}")
        
        # 3. FastAPI app 테스트
        try:
            from main import app
            startup_info["startup_steps"]["3_fastapi_app"] = True
            startup_info["fastapi_app"] = {
                "title": app.title,
                "version": app.version,
                "routes_count": len(app.routes)
            }
        except Exception as e:
            startup_info["startup_steps"]["3_fastapi_app"] = False
            startup_info["errors"].append(f"FastAPI app failed: {str(e)}")
        
        return startup_info
        
    except Exception as e:
        logger.error(f"시작 과정 디버깅 실패: {e}")
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }
