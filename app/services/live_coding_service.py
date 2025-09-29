"""
라이브 코딩 서비스 (Railway 환경 최적화)
실시간 코드 실행 및 파일 관리
"""

import os
import tempfile
import subprocess
import shutil
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class LiveCodingService:
    """라이브 코딩 서비스 (Railway 환경 최적화)"""
    
    def __init__(self):
        self.temp_dirs = {}  # 사용자별 임시 디렉토리
        logger.info("LiveCodingService 초기화 완료 (Railway 환경 최적화)")
    
    def _get_user_temp_dir(self, user_id: str) -> Path:
        """사용자별 임시 디렉토리 가져오기"""
        if user_id not in self.temp_dirs:
            temp_dir = Path(tempfile.mkdtemp(prefix=f"live_coding_{user_id}_"))
            self.temp_dirs[user_id] = temp_dir
            logger.info(f"사용자 {user_id} 임시 디렉토리 생성: {temp_dir}")
        return self.temp_dirs[user_id]
    
    async def execute_code(self, code: str, language: str = "python", file_path: str = None, user_id: str = "default", force_mode: str = None) -> Dict[str, Any]:
        """코드 실행 (Railway 환경에서는 로컬 실행만 지원)"""
        logger.info(f"코드 실행 시작 - 언어: {language}, 사용자: {user_id}")
        
        # Railway 환경에서는 항상 로컬 실행
        execution_mode = "local"
        logger.info(f"실행 모드: {execution_mode} (Railway 환경)")
        
        try:
            return await self._execute_locally(code, language, file_path, user_id)
        except Exception as e:
            logger.error(f"코드 실행 실패: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "execution_time": 0,
                "method": "local"
            }
    
    async def _execute_locally(self, code: str, language: str, file_path: str, user_id: str) -> Dict[str, Any]:
        """로컬 코드 실행"""
        logger.info(f"로컬 코드 실행 - 언어: {language}")
        
        # 언어별 설정
        language_config = {
            "python": {
                "command": ["python3", "-c"],
                "code_wrapper": lambda c: c,
                "extension": ".py"
            },
            "javascript": {
                "command": ["node", "-e"],
                "code_wrapper": lambda c: c,
                "extension": ".js"
            }
        }
        
        if language not in language_config:
            return {
                "success": False,
                "error": f"Railway 환경에서는 {language} 실행이 지원되지 않습니다. Python 또는 JavaScript만 지원됩니다.",
                "output": "",
                "execution_time": 0,
                "method": "local"
            }
        
        config = language_config[language]
        
        try:
            # 사용자별 임시 디렉토리에서 작업
            temp_dir = self._get_user_temp_dir(user_id)
            
            # 코드 실행
            start_time = datetime.now()
            
            if language == "python":
                # Python 코드 직접 실행
                result = subprocess.run(
                    ["python3", "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=temp_dir
                )
            elif language == "javascript":
                # JavaScript 코드 직접 실행
                result = subprocess.run(
                    ["node", "-e", code],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=temp_dir
                )
            else:
                return {
                    "success": False,
                    "error": f"지원하지 않는 언어: {language}",
                    "output": "",
                    "execution_time": 0,
                    "method": "local"
                }
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # 결과 반환
            if result.returncode == 0:
                return {
                    "success": True,
                    "output": result.stdout,
                    "error": result.stderr if result.stderr else "",
                    "execution_time": execution_time,
                    "method": "local"
                }
            else:
                return {
                    "success": False,
                    "output": result.stdout,
                    "error": result.stderr if result.stderr else f"실행 실패 (종료 코드: {result.returncode})",
                    "execution_time": execution_time,
                    "method": "local"
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": "코드 실행 시간 초과 (30초)",
                "execution_time": 30,
                "method": "local"
            }
        except Exception as e:
            logger.error(f"로컬 실행 중 오류 발생: {e}", exc_info=True)
            return {
                "success": False,
                "output": "",
                "error": f"로컬 실행 오류: {str(e)}",
                "execution_time": 0,
                "method": "local"
            }
    
    async def save_file(self, content: str, filename: str, user_id: str = "default") -> Dict[str, Any]:
        """파일 저장"""
        try:
            temp_dir = self._get_user_temp_dir(user_id)
            file_path = temp_dir / filename
            
            file_path.write_text(content, encoding='utf-8')
            
            return {
                "success": True,
                "file_path": str(file_path),
                "message": f"파일이 저장되었습니다: {filename}"
            }
        except Exception as e:
            logger.error(f"파일 저장 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def load_file(self, filename: str, user_id: str = "default") -> Dict[str, Any]:
        """파일 로드"""
        try:
            temp_dir = self._get_user_temp_dir(user_id)
            file_path = temp_dir / filename
            
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"파일을 찾을 수 없습니다: {filename}"
                }
            
            content = file_path.read_text(encoding='utf-8')
            
            return {
                "success": True,
                "content": content,
                "filename": filename
            }
        except Exception as e:
            logger.error(f"파일 로드 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def list_files(self, user_id: str = "default") -> Dict[str, Any]:
        """사용자 파일 목록"""
        try:
            temp_dir = self._get_user_temp_dir(user_id)
            files = []
            
            for file_path in temp_dir.iterdir():
                if file_path.is_file():
                    files.append({
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
            
            return {
                "success": True,
                "files": files
            }
        except Exception as e:
            logger.error(f"파일 목록 조회 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def delete_file(self, filename: str, user_id: str = "default") -> Dict[str, Any]:
        """파일 삭제"""
        try:
            temp_dir = self._get_user_temp_dir(user_id)
            file_path = temp_dir / filename
            
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"파일을 찾을 수 없습니다: {filename}"
                }
            
            file_path.unlink()
            
            return {
                "success": True,
                "message": f"파일이 삭제되었습니다: {filename}"
            }
        except Exception as e:
            logger.error(f"파일 삭제 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def cleanup_user_files(self, user_id: str) -> Dict[str, Any]:
        """사용자 파일 정리"""
        try:
            if user_id in self.temp_dirs:
                temp_dir = self.temp_dirs[user_id]
                shutil.rmtree(temp_dir, ignore_errors=True)
                del self.temp_dirs[user_id]
                
                return {
                    "success": True,
                    "message": f"사용자 {user_id}의 파일이 정리되었습니다."
                }
            else:
                return {
                    "success": True,
                    "message": f"사용자 {user_id}의 파일이 이미 정리되었습니다."
                }
        except Exception as e:
            logger.error(f"파일 정리 실패: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_stats(self) -> Dict[str, Any]:
        """서비스 통계"""
        return {
            "active_users": len(self.temp_dirs),
            "supported_languages": ["python", "javascript"],
            "docker_available": False,  # Railway 환경에서는 Docker 사용 불가
            "railway_mode": True
        }