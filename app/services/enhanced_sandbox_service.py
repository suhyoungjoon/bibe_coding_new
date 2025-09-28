"""
향상된 샌드박스 서비스
보안, 모니터링, 리소스 관리 기능이 강화된 코드 실행 환경
"""

import os
import tempfile
import subprocess
import shutil
import logging
import asyncio
import json
import psutil
import time
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import docker
import uuid

logger = logging.getLogger(__name__)

class ExecutionMode(Enum):
    """실행 모드"""
    DOCKER = "docker"
    LOCAL = "local"
    AUTO = "auto"

class SecurityLevel(Enum):
    """보안 수준"""
    LOW = "low"          # 기본 제한
    MEDIUM = "medium"    # 중간 제한
    HIGH = "high"        # 높은 제한
    MAXIMUM = "maximum"  # 최대 제한

@dataclass
class ResourceLimits:
    """리소스 제한 설정"""
    memory_mb: int = 128
    cpu_percent: float = 50.0
    execution_timeout: int = 30
    max_file_size_mb: int = 10
    max_files: int = 100

@dataclass
class ExecutionResult:
    """실행 결과"""
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

class EnhancedSandboxService:
    """향상된 샌드박스 서비스"""
    
    def __init__(self):
        self.temp_dirs = {}  # 사용자별 임시 디렉토리
        self.docker_client = None
        self.execution_history = {}  # 실행 히스토리
        self.resource_monitor = {}   # 리소스 모니터링
        self.security_policies = self._init_security_policies()
        self.language_configs = self._init_language_configs()
        self._init_docker()
    
    def _init_docker(self):
        """Docker 클라이언트 초기화"""
        try:
            self.docker_client = docker.from_env()
            self.docker_client.ping()
            logger.info("Docker 클라이언트 초기화 성공")
        except Exception as e:
            logger.warning(f"Docker 클라이언트 초기화 실패: {e}")
            self.docker_client = None
    
    def _init_security_policies(self) -> Dict[str, Dict[str, Any]]:
        """보안 정책 초기화"""
        return {
            SecurityLevel.LOW.value: {
                "forbidden_imports": ["os", "subprocess", "sys", "shutil"],
                "forbidden_functions": ["eval", "exec", "compile", "input"],
                "network_access": True,
                "file_access": True,
                "resource_limits": ResourceLimits(memory_mb=256, cpu_percent=75.0)
            },
            SecurityLevel.MEDIUM.value: {
                "forbidden_imports": ["os", "subprocess", "sys", "shutil", "socket", "urllib"],
                "forbidden_functions": ["eval", "exec", "compile", "input", "open"],
                "network_access": False,
                "file_access": False,
                "resource_limits": ResourceLimits(memory_mb=128, cpu_percent=50.0)
            },
            SecurityLevel.HIGH.value: {
                "forbidden_imports": ["os", "subprocess", "sys", "shutil", "socket", "urllib", "requests", "http"],
                "forbidden_functions": ["eval", "exec", "compile", "input", "open", "file", "raw_input"],
                "network_access": False,
                "file_access": False,
                "resource_limits": ResourceLimits(memory_mb=64, cpu_percent=25.0)
            },
            SecurityLevel.MAXIMUM.value: {
                "forbidden_imports": ["os", "subprocess", "sys", "shutil", "socket", "urllib", "requests", "http", "ftplib", "smtplib"],
                "forbidden_functions": ["eval", "exec", "compile", "input", "open", "file", "raw_input", "__import__"],
                "network_access": False,
                "file_access": False,
                "resource_limits": ResourceLimits(memory_mb=32, cpu_percent=10.0)
            }
        }
    
    def _init_language_configs(self) -> Dict[str, Dict[str, Any]]:
        """언어별 설정 초기화"""
        return {
            "python": {
                "name": "Python",
                "version": "3.11",
                "extension": ".py",
                "docker_image": "python:3.11-slim",
                "docker_command": ["python", "/tmp/code.py"],
                "local_command": ["python3", "{file}"],
                "fallback_command": ["python", "{file}"]
            },
            "javascript": {
                "name": "JavaScript (Node.js)",
                "version": "18",
                "extension": ".js",
                "docker_image": "node:18-slim",
                "docker_command": ["node", "/tmp/code.js"],
                "local_command": ["node", "{file}"]
            },
            "java": {
                "name": "Java",
                "version": "11",
                "extension": ".java",
                "docker_image": "openjdk:11-jdk-slim",
                "docker_command": ["sh", "-c", "cd /tmp && javac code.java && java -cp /tmp Main"],
                "local_command": ["javac", "{file}", "&&", "java", "{class}"]
            },
            "go": {
                "name": "Go",
                "version": "1.21",
                "extension": ".go",
                "docker_image": "golang:1.21-alpine",
                "docker_command": ["sh", "-c", "cd /tmp && go run code.go"],
                "local_command": ["go", "run", "{file}"]
            },
            "rust": {
                "name": "Rust",
                "version": "1.75",
                "extension": ".rs",
                "docker_image": "rust:1.75-slim",
                "docker_command": ["sh", "-c", "cd /tmp && rustc code.rs && ./code"],
                "local_command": ["rustc", "{file}", "&&", "./{executable}"]
            },
            "cpp": {
                "name": "C++",
                "version": "17",
                "extension": ".cpp",
                "docker_image": "gcc:latest",
                "docker_command": ["sh", "-c", "cd /tmp && g++ -std=c++17 code.cpp -o code && ./code"],
                "local_command": ["g++", "-std=c++17", "{file}", "-o", "{executable}", "&&", "./{executable}"]
            },
            "csharp": {
                "name": "C#",
                "version": "8.0",
                "extension": ".cs",
                "docker_image": "mcr.microsoft.com/dotnet/sdk:8.0",
                "docker_command": ["sh", "-c", "cd /tmp && dotnet new console --force && mv code.cs Program.cs && dotnet run"],
                "local_command": ["dotnet", "run"]
            },
            "php": {
                "name": "PHP",
                "version": "8.2",
                "extension": ".php",
                "docker_image": "php:8.2-cli",
                "docker_command": ["php", "/tmp/code.php"],
                "local_command": ["php", "{file}"]
            }
        }
    
    def _get_user_temp_dir(self, user_id: str) -> Path:
        """사용자별 임시 디렉토리 가져오기"""
        if user_id not in self.temp_dirs:
            temp_dir = Path(tempfile.mkdtemp(prefix=f"sandbox_{user_id}_"))
            self.temp_dirs[user_id] = temp_dir
            logger.info(f"사용자 {user_id} 임시 디렉토리 생성: {temp_dir}")
        return self.temp_dirs[user_id]
    
    def _validate_code_security(self, code: str, language: str, security_level: SecurityLevel) -> Tuple[bool, str]:
        """코드 보안 검증"""
        policy = self.security_policies[security_level.value]
        
        # 금지된 import 검사
        for forbidden_import in policy["forbidden_imports"]:
            if f"import {forbidden_import}" in code or f"from {forbidden_import}" in code:
                return False, f"금지된 모듈 사용: {forbidden_import}"
        
        # 금지된 함수 검사
        for forbidden_func in policy["forbidden_functions"]:
            if f"{forbidden_func}(" in code:
                return False, f"금지된 함수 사용: {forbidden_func}"
        
        # 언어별 추가 검사
        if language == "python":
            # 위험한 패턴 검사
            dangerous_patterns = [
                "__import__",
                "getattr",
                "setattr",
                "delattr",
                "globals()",
                "locals()",
                "vars()",
                "dir()"
            ]
            for pattern in dangerous_patterns:
                if pattern in code:
                    return False, f"위험한 패턴 감지: {pattern}"
        
        return True, "보안 검증 통과"
    
    def _monitor_resource_usage(self, process_id: str, user_id: str) -> Dict[str, float]:
        """리소스 사용량 모니터링"""
        try:
            process = psutil.Process(process_id)
            memory_info = process.memory_info()
            cpu_percent = process.cpu_percent()
            
            return {
                "memory_mb": memory_info.rss / 1024 / 1024,
                "cpu_percent": cpu_percent,
                "timestamp": datetime.now().isoformat()
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {"memory_mb": 0, "cpu_percent": 0, "timestamp": datetime.now().isoformat()}
    
    async def execute_code_enhanced(
        self, 
        code: str, 
        language: str = "python", 
        user_id: str = "default",
        execution_mode: ExecutionMode = ExecutionMode.AUTO,
        security_level: SecurityLevel = SecurityLevel.MEDIUM,
        custom_resource_limits: Optional[ResourceLimits] = None
    ) -> ExecutionResult:
        """향상된 코드 실행"""
        
        execution_id = str(uuid.uuid4())
        start_time = time.time()
        
        logger.info(f"향상된 코드 실행 시작 - ID: {execution_id}, 언어: {language}, 사용자: {user_id}")
        
        try:
            # 언어 지원 확인
            if language not in self.language_configs:
                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"지원하지 않는 언어: {language}",
                    execution_time=0,
                    memory_usage_mb=0,
                    cpu_usage_percent=0,
                    language=language,
                    method="validation",
                    security_level=security_level.value,
                    resource_limits={},
                    metadata={"execution_id": execution_id, "error_type": "unsupported_language"}
                )
            
            # 보안 검증
            is_secure, security_message = self._validate_code_security(code, language, security_level)
            if not is_secure:
                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"보안 검증 실패: {security_message}",
                    execution_time=time.time() - start_time,
                    memory_usage_mb=0,
                    cpu_usage_percent=0,
                    language=language,
                    method="security_check",
                    security_level=security_level.value,
                    resource_limits={},
                    metadata={"execution_id": execution_id, "error_type": "security_violation"}
                )
            
            # 리소스 제한 설정
            resource_limits = custom_resource_limits or self.security_policies[security_level.value]["resource_limits"]
            
            # 실행 모드 결정
            if execution_mode == ExecutionMode.AUTO:
                if self.docker_client:
                    execution_mode = ExecutionMode.DOCKER
                else:
                    execution_mode = ExecutionMode.LOCAL
            
            # 코드 실행
            if execution_mode == ExecutionMode.DOCKER and self.docker_client:
                result = await self._execute_in_docker_enhanced(
                    code, language, user_id, execution_id, resource_limits
                )
            else:
                result = await self._execute_locally_enhanced(
                    code, language, user_id, execution_id, resource_limits
                )
            
            # 실행 히스토리 저장
            self.execution_history[execution_id] = {
                "user_id": user_id,
                "language": language,
                "execution_mode": execution_mode.value,
                "security_level": security_level.value,
                "timestamp": datetime.now().isoformat(),
                "result": asdict(result)
            }
            
            return result
            
        except Exception as e:
            logger.error(f"코드 실행 실패: {e}", exc_info=True)
            return ExecutionResult(
                success=False,
                output="",
                error=str(e),
                execution_time=time.time() - start_time,
                memory_usage_mb=0,
                cpu_usage_percent=0,
                language=language,
                method="error",
                security_level=security_level.value,
                resource_limits=asdict(resource_limits) if custom_resource_limits else {},
                metadata={"execution_id": execution_id, "error_type": "execution_error"}
            )
    
    async def _execute_in_docker_enhanced(
        self, 
        code: str, 
        language: str, 
        user_id: str, 
        execution_id: str,
        resource_limits: ResourceLimits
    ) -> ExecutionResult:
        """Docker에서 향상된 코드 실행"""
        
        start_time = time.time()
        config = self.language_configs[language]
        
        try:
            # Docker 이미지 준비
            try:
                self.docker_client.images.get(config["docker_image"])
            except docker.errors.ImageNotFound:
                logger.info(f"Docker 이미지 다운로드: {config['docker_image']}")
                self.docker_client.images.pull(config["docker_image"])
            
            # 사용자별 임시 디렉토리
            temp_dir = self._get_user_temp_dir(user_id)
            
            # Java 특별 처리: 클래스명 추출 및 파일명 조정
            if language == "java":
                # 클래스명 추출
                class_name = "Main"
                try:
                    import re
                    class_match = re.search(r'public class (\w+)', code)
                    if class_match:
                        class_name = class_match.group(1)
                except:
                    pass
                
                # 파일명을 클래스명과 일치시키기
                filename = f"{class_name}.java"
            else:
                filename = f"code_{execution_id[:8]}{config['extension']}"
            
            temp_file = temp_dir / filename
            
            # 코드 파일 생성
            temp_file.write_text(code, encoding='utf-8')
            
            # 명령어 준비 (파일명 치환)
            command = []
            for cmd_part in config["docker_command"]:
                if "code.py" in cmd_part:
                    command.append(cmd_part.replace("code.py", filename))
                elif "code.js" in cmd_part:
                    command.append(cmd_part.replace("code.js", filename))
                elif "code.java" in cmd_part:
                    command.append(cmd_part.replace("code.java", filename))
                elif "code.rs" in cmd_part:
                    command.append(cmd_part.replace("code.rs", filename))
                elif "code.cpp" in cmd_part:
                    command.append(cmd_part.replace("code.cpp", filename))
                elif "code.cs" in cmd_part:
                    command.append(cmd_part.replace("code.cs", filename))
                elif "code.php" in cmd_part:
                    command.append(cmd_part.replace("code.php", filename))
                else:
                    command.append(cmd_part)
            
            # Java 명령어에서 Main을 실제 클래스명으로 치환
            if language == "java":
                for i, cmd_part in enumerate(command):
                    if "Main" in cmd_part:
                        command[i] = cmd_part.replace("Main", class_name)
            
            # 컨테이너 실행 (향상된 보안 설정)
            container = self.docker_client.containers.run(
                config["docker_image"],
                command=command,
                detach=True,
                mem_limit=f"{resource_limits.memory_mb}m",
                cpu_period=100000,
                cpu_quota=int(100000 * resource_limits.cpu_percent / 100),
                network_disabled=True,
                remove=False,
                read_only=True,  # 읽기 전용 파일시스템
                security_opt=["no-new-privileges:true"],  # 권한 상승 방지
                cap_drop=["ALL"],  # 모든 권한 제거
                cap_add=[],  # 필요한 권한만 추가
                volumes={
                    str(temp_dir): {'bind': '/tmp', 'mode': 'rw'}
                },
                working_dir='/tmp'
            )
            
            try:
                # 실행 대기 (타임아웃 적용)
                result = container.wait(timeout=resource_limits.execution_timeout)
                
                # 로그 수집
                output = ""
                error_output = ""
                
                try:
                    logs = container.logs(stdout=True, stderr=False)
                    output = logs.decode('utf-8')
                except Exception as e:
                    logger.warning(f"표준 출력 로그 읽기 실패: {e}")
                
                try:
                    error_logs = container.logs(stdout=False, stderr=True)
                    error_output = error_logs.decode('utf-8')
                except Exception as e:
                    logger.warning(f"오류 출력 로그 읽기 실패: {e}")
                
                execution_time = time.time() - start_time
                
                return ExecutionResult(
                    success=result['StatusCode'] == 0,
                    output=output,
                    error=error_output,
                    execution_time=execution_time,
                    memory_usage_mb=0,  # Docker 컨테이너 메모리 사용량은 별도 모니터링 필요
                    cpu_usage_percent=0,
                    language=language,
                    method="docker",
                    security_level="enhanced",
                    resource_limits=asdict(resource_limits),
                    metadata={
                        "execution_id": execution_id,
                        "container_id": container.id,
                        "image": config["docker_image"]
                    }
                )
                
            finally:
                # 컨테이너 정리
                try:
                    container.remove(force=True)
                except Exception as e:
                    logger.warning(f"컨테이너 정리 실패: {e}")
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=f"Docker 실행 오류: {str(e)}",
                execution_time=time.time() - start_time,
                memory_usage_mb=0,
                cpu_usage_percent=0,
                language=language,
                method="docker",
                security_level="enhanced",
                resource_limits=asdict(resource_limits),
                metadata={"execution_id": execution_id, "error_type": "docker_error"}
            )
    
    async def _execute_locally_enhanced(
        self, 
        code: str, 
        language: str, 
        user_id: str, 
        execution_id: str,
        resource_limits: ResourceLimits
    ) -> ExecutionResult:
        """로컬에서 향상된 코드 실행"""
        
        start_time = time.time()
        config = self.language_configs[language]
        
        try:
            # 임시 파일 생성
            temp_dir = self._get_user_temp_dir(user_id)
            filename = f"code_{execution_id[:8]}{config['extension']}"
            temp_file = temp_dir / filename
            
            temp_file.write_text(code, encoding='utf-8')
            
            # 명령어 준비
            command = []
            for cmd_part in config["local_command"]:
                if "{file}" in cmd_part:
                    command.append(cmd_part.replace("{file}", str(temp_file)))
                elif "{executable}" in cmd_part:
                    executable_name = filename.rsplit('.', 1)[0]
                    command.append(cmd_part.replace("{executable}", executable_name))
                elif "{class}" in cmd_part:
                    class_name = filename.rsplit('.', 1)[0]
                    command.append(cmd_part.replace("{class}", class_name))
                else:
                    command.append(cmd_part)
            
            # 프로세스 실행
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(temp_dir)
            )
            
            # 리소스 모니터링 시작
            monitor_task = None
            if process.pid:
                monitor_task = asyncio.create_task(
                    self._monitor_process_resources(process.pid, resource_limits.execution_timeout)
                )
            
            # 실행 완료 대기
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=resource_limits.execution_timeout
                )
                
                output = stdout.decode('utf-8')
                error_output = stderr.decode('utf-8')
                
                # 리소스 모니터링 중지
                if monitor_task:
                    monitor_task.cancel()
                
                execution_time = time.time() - start_time
                
                return ExecutionResult(
                    success=process.returncode == 0,
                    output=output,
                    error=error_output,
                    execution_time=execution_time,
                    memory_usage_mb=self.resource_monitor.get(process.pid, {}).get("memory_mb", 0),
                    cpu_usage_percent=self.resource_monitor.get(process.pid, {}).get("cpu_percent", 0),
                    language=language,
                    method="local",
                    security_level="basic",
                    resource_limits=asdict(resource_limits),
                    metadata={"execution_id": execution_id, "pid": process.pid}
                )
                
            except asyncio.TimeoutError:
                # 타임아웃 시 프로세스 종료
                process.kill()
                await process.wait()
                
                if monitor_task:
                    monitor_task.cancel()
                
                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"실행 시간 초과 ({resource_limits.execution_timeout}초)",
                    execution_time=resource_limits.execution_timeout,
                    memory_usage_mb=self.resource_monitor.get(process.pid, {}).get("memory_mb", 0),
                    cpu_usage_percent=self.resource_monitor.get(process.pid, {}).get("cpu_percent", 0),
                    language=language,
                    method="local",
                    security_level="basic",
                    resource_limits=asdict(resource_limits),
                    metadata={"execution_id": execution_id, "error_type": "timeout"}
                )
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=f"로컬 실행 오류: {str(e)}",
                execution_time=time.time() - start_time,
                memory_usage_mb=0,
                cpu_usage_percent=0,
                language=language,
                method="local",
                security_level="basic",
                resource_limits=asdict(resource_limits),
                metadata={"execution_id": execution_id, "error_type": "execution_error"}
            )
    
    async def _monitor_process_resources(self, process_id: int, timeout: int):
        """프로세스 리소스 모니터링"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                resource_usage = self._monitor_resource_usage(process_id, "monitor")
                self.resource_monitor[process_id] = resource_usage
                await asyncio.sleep(0.5)  # 0.5초마다 모니터링
            except Exception as e:
                logger.warning(f"리소스 모니터링 오류: {e}")
                break
    
    def get_execution_history(self, user_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """실행 히스토리 조회"""
        history = list(self.execution_history.values())
        
        if user_id:
            history = [h for h in history if h["user_id"] == user_id]
        
        # 최신 순으로 정렬
        history.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return history[:limit]
    
    def get_supported_languages(self) -> Dict[str, Dict[str, Any]]:
        """지원하는 언어 목록 반환"""
        result = {}
        for lang, config in self.language_configs.items():
            result[lang] = {
                "name": config["name"],
                "version": config["version"],
                "extension": config["extension"],
                "docker_available": self.docker_client is not None,
                "local_available": self._check_local_availability(lang)
            }
        return result
    
    def _check_local_availability(self, language: str) -> bool:
        """로컬 환경에서 언어 사용 가능 여부 확인"""
        config = self.language_configs.get(language)
        if not config:
            return False
        
        try:
            if language == "python":
                subprocess.run(["python3", "--version"], capture_output=True, timeout=5)
                return True
            elif language == "javascript":
                subprocess.run(["node", "--version"], capture_output=True, timeout=5)
                return True
            elif language == "java":
                subprocess.run(["javac", "-version"], capture_output=True, timeout=5)
                return True
            elif language == "go":
                subprocess.run(["go", "version"], capture_output=True, timeout=5)
                return True
            elif language == "rust":
                subprocess.run(["rustc", "--version"], capture_output=True, timeout=5)
                return True
            elif language == "cpp":
                subprocess.run(["g++", "--version"], capture_output=True, timeout=5)
                return True
            elif language == "csharp":
                subprocess.run(["dotnet", "--version"], capture_output=True, timeout=5)
                return True
            elif language == "php":
                subprocess.run(["php", "--version"], capture_output=True, timeout=5)
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
        
        return False
    
    def cleanup_user_data(self, user_id: str):
        """사용자 데이터 정리"""
        if user_id in self.temp_dirs:
            try:
                shutil.rmtree(self.temp_dirs[user_id])
                del self.temp_dirs[user_id]
                logger.info(f"사용자 {user_id} 임시 데이터 정리 완료")
            except Exception as e:
                logger.error(f"사용자 {user_id} 임시 데이터 정리 실패: {e}")
        
        # 실행 히스토리에서 사용자 데이터 정리
        self.execution_history = {
            k: v for k, v in self.execution_history.items() 
            if v["user_id"] != user_id
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """시스템 통계 조회"""
        return {
            "docker_available": self.docker_client is not None,
            "active_users": len(self.temp_dirs),
            "total_executions": len(self.execution_history),
            "supported_languages": len(self.language_configs),
            "memory_usage": psutil.virtual_memory().percent,
            "cpu_usage": psutil.cpu_percent(),
            "timestamp": datetime.now().isoformat()
        }
