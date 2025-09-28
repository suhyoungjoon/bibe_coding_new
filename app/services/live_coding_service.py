"""
라이브 코딩 서비스
실시간 코드 실행 및 파일 관리
"""

import os
import tempfile
import subprocess
import shutil
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import docker
from datetime import datetime

logger = logging.getLogger(__name__)

class LiveCodingService:
    """라이브 코딩 서비스"""
    
    def __init__(self):
        self.temp_dirs = {}  # 사용자별 임시 디렉토리
        self.docker_client = None
        self._init_docker()
    
    def _init_docker(self):
        """Docker 클라이언트 초기화"""
        try:
            self.docker_client = docker.from_env()
            # 테스트 연결
            self.docker_client.ping()
            logger.info("Docker 클라이언트 초기화 성공")
        except Exception as e:
            logger.warning(f"Docker 클라이언트 초기화 실패: {e}")
            logger.info("로컬 실행 모드로 전환합니다.")
            self.docker_client = None
    
    def _get_user_temp_dir(self, user_id: str) -> Path:
        """사용자별 임시 디렉토리 가져오기"""
        if user_id not in self.temp_dirs:
            temp_dir = Path(tempfile.mkdtemp(prefix=f"live_coding_{user_id}_"))
            self.temp_dirs[user_id] = temp_dir
            logger.info(f"사용자 {user_id} 임시 디렉토리 생성: {temp_dir}")
        return self.temp_dirs[user_id]
    
    async def execute_code(self, code: str, language: str = "python", file_path: str = None, user_id: str = "default", force_mode: str = None) -> Dict[str, Any]:
        """코드 실행"""
        logger.info(f"코드 실행 시작 - 언어: {language}, 사용자: {user_id}")
        
        # 실행 모드 결정
        execution_mode = force_mode
        if not execution_mode:
            if self.docker_client:
                execution_mode = "docker"
            else:
                execution_mode = "local"
        
        logger.info(f"실행 모드: {execution_mode}")
        
        try:
            if execution_mode == "docker" and self.docker_client:
                return await self._execute_in_docker(code, language, file_path, user_id)
            elif execution_mode == "docker" and not self.docker_client:
                logger.warning("Docker 모드 요청되었지만 Docker가 사용 불가능합니다. 로컬 모드로 전환합니다.")
                return await self._execute_locally(code, language, file_path, user_id)
            else:
                return await self._execute_locally(code, language, file_path, user_id)
        except Exception as e:
            logger.error(f"코드 실행 실패: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "execution_time": 0
            }
    
    async def _execute_in_docker(self, code: str, language: str, file_path: str, user_id: str) -> Dict[str, Any]:
        """Docker 컨테이너에서 코드 실행"""
        start_time = datetime.now()
        
        # 언어별 Docker 이미지 및 실행 명령
        language_config = {
            "python": {
                "image": "python:3.11-slim",
                "command": ["python", "/tmp/code.py"],
                "extension": ".py"
            },
            "javascript": {
                "image": "node:18-slim",
                "command": ["node", "/tmp/code.js"],
                "extension": ".js"
            },
            "java": {
                "image": "openjdk:11-jdk-slim",
                "command": ["sh", "-c", "javac /tmp/code.java && java -cp /tmp Main"],
                "extension": ".java"
            },
            "go": {
                "image": "golang:1.21-alpine",
                "command": ["sh", "-c", "cd /tmp && go run code.go"],
                "extension": ".go"
            }
        }
        
        if language not in language_config:
            return {
                "success": False,
                "error": f"지원하지 않는 언어: {language}",
                "output": "",
                "execution_time": 0
            }
        
        config = language_config[language]
        
        try:
            # Docker 이미지 확인 및 다운로드
            try:
                self.docker_client.images.get(config["image"])
                logger.info(f"Docker 이미지 {config['image']} 사용 가능")
            except docker.errors.ImageNotFound:
                logger.info(f"Docker 이미지 {config['image']} 다운로드 중...")
                self.docker_client.images.pull(config["image"])
                logger.info(f"Docker 이미지 {config['image']} 다운로드 완료")
            
            # 사용자별 임시 디렉토리에서 작업
            temp_dir = self._get_user_temp_dir(user_id)
            filename = f"code_{datetime.now().strftime('%Y%m%d_%H%M%S')}{config['extension']}"
            temp_file = temp_dir / filename
            
            # 코드 파일 생성
            temp_file.write_text(code, encoding='utf-8')
            
            # 명령어 준비 (파일명 치환)
            command_list = []
            for cmd_part in config["command"]:
                if 'code.py' in cmd_part:
                    command_list.append(cmd_part.replace('code.py', filename))
                elif 'code.js' in cmd_part:
                    command_list.append(cmd_part.replace('code.js', filename))
                elif 'code.java' in cmd_part:
                    command_list.append(cmd_part.replace('code.java', filename))
                else:
                    command_list.append(cmd_part)
            
            logger.debug(f"Docker 명령어: {command_list}")
            logger.debug(f"파일 경로: {temp_file}")
            logger.debug(f"파일 존재 여부: {temp_file.exists()}")
            
            # 컨테이너 실행 (볼륨 마운트 방식)
            container = self.docker_client.containers.run(
                config["image"],
                command=command_list,
                detach=True,
                mem_limit="128m",
                cpu_period=100000,
                cpu_quota=50000,
                network_disabled=True,
                remove=False,  # 자동 제거 비활성화
                volumes={
                    str(temp_dir): {'bind': '/tmp', 'mode': 'rw'}
                }
            )
            
            try:
                # 실행 및 결과 수집
                result = container.wait(timeout=10)
                
                # 로그 수집
                try:
                    logs = container.logs()
                    output = logs.decode('utf-8')
                except Exception as e:
                    logger.warning(f"표준 출력 로그 읽기 실패: {e}")
                    output = ""
                
                try:
                    error_logs = container.logs(stderr=True)
                    error_output = error_logs.decode('utf-8')
                except Exception as e:
                    logger.warning(f"오류 출력 로그 읽기 실패: {e}")
                    error_output = ""
                
                execution_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "success": result['StatusCode'] == 0,
                    "output": output,
                    "error": error_output if result['StatusCode'] != 0 else "",
                    "execution_time": execution_time,
                    "language": language,
                    "method": "docker"
                }
                
            finally:
                # 컨테이너 정리
                try:
                    container.remove(force=True)
                    logger.debug("Docker 컨테이너 정리 완료")
                except Exception as e:
                    logger.warning(f"Docker 컨테이너 정리 실패: {e}")
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Docker 실행 오류: {str(e)}",
                "output": "",
                "execution_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def _execute_locally(self, code: str, language: str, file_path: str, user_id: str) -> Dict[str, Any]:
        """로컬에서 코드 실행"""
        start_time = datetime.now()
        
        try:
            if language == "python":
                return await self._execute_python_locally(code, user_id)
            elif language == "javascript":
                return await self._execute_javascript_locally(code, user_id)
            else:
                return {
                    "success": False,
                    "error": f"로컬 실행에서 지원하지 않는 언어: {language}",
                    "output": "",
                    "execution_time": 0
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"로컬 실행 오류: {str(e)}",
                "output": "",
                "execution_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def _execute_python_locally(self, code: str, user_id: str) -> Dict[str, Any]:
        """Python 코드 로컬 실행"""
        start_time = datetime.now()
        
        try:
            # 임시 파일 생성
            temp_dir = self._get_user_temp_dir(user_id)
            temp_file = temp_dir / f"code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            temp_file.write_text(code, encoding='utf-8')
            
            # 실행 (python3 우선 시도)
            try:
                result = subprocess.run(
                    ["python3", str(temp_file)],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=str(temp_dir)
                )
            except FileNotFoundError:
                # python3가 없으면 python 시도
                result = subprocess.run(
                    ["python", str(temp_file)],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=str(temp_dir)
                )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "execution_time": execution_time,
                "language": "python",
                "method": "local"
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "실행 시간 초과 (10초)",
                "output": "",
                "execution_time": 10.0,
                "language": "python",
                "method": "local"
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Python 인터프리터를 찾을 수 없습니다. Python이 설치되어 있는지 확인하세요.",
                "output": "",
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "language": "python",
                "method": "local"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"실행 오류: {str(e)}",
                "output": "",
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "language": "python",
                "method": "local"
            }
    
    async def _execute_javascript_locally(self, code: str, user_id: str) -> Dict[str, Any]:
        """JavaScript 코드 로컬 실행"""
        start_time = datetime.now()
        
        try:
            # 임시 파일 생성
            temp_dir = self._get_user_temp_dir(user_id)
            temp_file = temp_dir / f"code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.js"
            temp_file.write_text(code, encoding='utf-8')
            
            # 실행
            result = subprocess.run(
                ["node", str(temp_file)],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(temp_dir)
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "execution_time": execution_time,
                "language": "javascript",
                "method": "local"
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "실행 시간 초과 (10초)",
                "output": "",
                "execution_time": 10.0
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": "",
                "execution_time": (datetime.now() - start_time).total_seconds()
            }
    
    async def handle_file_operation(self, operation: str, file_path: str, new_path: str = None) -> Dict[str, Any]:
        """파일 작업 처리"""
        try:
            if operation == "create":
                # 파일 생성
                Path(file_path).touch()
                return {"success": True, "message": f"파일 생성됨: {file_path}"}
            
            elif operation == "delete":
                # 파일 삭제
                if Path(file_path).exists():
                    Path(file_path).unlink()
                    return {"success": True, "message": f"파일 삭제됨: {file_path}"}
                else:
                    return {"success": False, "error": f"파일이 존재하지 않음: {file_path}"}
            
            elif operation == "rename" and new_path:
                # 파일 이름 변경
                if Path(file_path).exists():
                    Path(file_path).rename(new_path)
                    return {"success": True, "message": f"파일 이름 변경됨: {file_path} -> {new_path}"}
                else:
                    return {"success": False, "error": f"파일이 존재하지 않음: {file_path}"}
            
            else:
                return {"success": False, "error": f"지원하지 않는 작업: {operation}"}
                
        except Exception as e:
            return {"success": False, "error": f"파일 작업 실패: {str(e)}"}
    
    def cleanup_user_data(self, user_id: str):
        """사용자 데이터 정리"""
        if user_id in self.temp_dirs:
            try:
                shutil.rmtree(self.temp_dirs[user_id])
                del self.temp_dirs[user_id]
                logger.info(f"사용자 {user_id} 임시 데이터 정리 완료")
            except Exception as e:
                logger.error(f"사용자 {user_id} 임시 데이터 정리 실패: {e}")
    
    def get_supported_languages(self) -> Dict[str, Dict[str, str]]:
        """지원하는 언어 목록 반환"""
        return {
            "python": {
                "name": "Python",
                "version": "3.11",
                "extension": ".py",
                "docker_available": self.docker_client is not None
            },
            "javascript": {
                "name": "JavaScript",
                "version": "18",
                "extension": ".js",
                "docker_available": self.docker_client is not None
            },
            "java": {
                "name": "Java",
                "version": "11",
                "extension": ".java",
                "docker_available": self.docker_client is not None
            },
            "go": {
                "name": "Go",
                "version": "1.21",
                "extension": ".go",
                "docker_available": self.docker_client is not None
            }
        }
