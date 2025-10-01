"""
Enhanced Sandbox Service (Railway 환경 최적화)
Railway 환경에서 안전하고 간단한 코드 실행 서비스
"""

import os
import tempfile
import subprocess
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

logger = logging.getLogger(__name__)

class ExecutionMode(Enum):
    """실행 모드"""
    LOCAL = "local"

class SecurityLevel(Enum):
    """보안 레벨"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class ResourceLimits:
    """리소스 제한"""
    max_memory_mb: int = 128
    max_cpu_percent: float = 50.0
    timeout_seconds: int = 30

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
    """Railway 환경 최적화 샌드박스 서비스"""
    
    def __init__(self):
        self.temp_dirs = {}  # 사용자별 임시 디렉토리
        self.execution_history = {}  # 실행 히스토리
        self.resource_monitor = {}   # 리소스 모니터링
        self.security_policies = self._init_security_policies()
        self.language_configs = self._init_language_configs()
        logger.info("EnhancedSandboxService 초기화 완료 (Railway 환경 최적화)")
    
    def _init_security_policies(self) -> Dict[str, Dict[str, Any]]:
        """보안 정책 초기화"""
        return {
            SecurityLevel.LOW.value: {
                "allowed_modules": ["os", "sys", "datetime", "math", "random"],
                "max_execution_time": 30,
                "max_memory_mb": 128
            },
            SecurityLevel.MEDIUM.value: {
                "allowed_modules": ["os", "sys", "datetime", "math", "random", "json"],
                "max_execution_time": 20,
                "max_memory_mb": 64
            },
            SecurityLevel.HIGH.value: {
                "allowed_modules": ["math", "random", "datetime"],
                "max_execution_time": 10,
                "max_memory_mb": 32
            }
        }
    
    def _init_language_configs(self) -> Dict[str, Dict[str, Any]]:
        """언어별 설정 초기화"""
        return {
            "python": {
                "command": ["python3", "-c"],
                "extension": ".py",
                "supported": True
            },
            "javascript": {
                "command": ["node", "-e"],
                "extension": ".js", 
                "supported": True
            },
            "java": {
                "command": ["java", "-version"],
                "extension": ".java",
                "supported": False  # Railway에서는 지원하지 않음
            },
            "go": {
                "command": ["go", "version"],
                "extension": ".go",
                "supported": False  # Railway에서는 지원하지 않음
            }
        }
    
    def _get_user_temp_dir(self, user_id: str) -> Path:
        """사용자별 임시 디렉토리 가져오기"""
        if user_id not in self.temp_dirs:
            temp_dir = Path(tempfile.mkdtemp(prefix=f"sandbox_{user_id}_"))
            self.temp_dirs[user_id] = temp_dir
            logger.info(f"사용자 {user_id} 임시 디렉토리 생성: {temp_dir}")
        return self.temp_dirs[user_id]
    
    def _validate_code_security(self, code: str, language: str, security_level: SecurityLevel) -> tuple[bool, str]:
        """코드 보안 검증"""
        # Railway 환경에서는 간단한 검증만 수행
        dangerous_patterns = [
            "import os", "import sys", "import subprocess", 
            "import shutil", "__import__", "eval(", "exec("
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code.lower():
                return False, f"위험한 패턴 감지: {pattern}"
        
        return True, "보안 검증 통과"
    
    async def execute_code_enhanced(
        self,
        code: str,
        language: str = "python",
        user_id: str = "default",
        security_level: SecurityLevel = SecurityLevel.MEDIUM,
        execution_mode: ExecutionMode = ExecutionMode.LOCAL,
        custom_resource_limits: Optional[ResourceLimits] = None
    ) -> ExecutionResult:
        """Railway 환경 최적화 코드 실행"""
        logger.info(f"코드 실행 시작 - 언어: {language}, 사용자: {user_id}, 보안레벨: {security_level.value}")
        
        resource_limits = custom_resource_limits or ResourceLimits()
        execution_id = str(uuid.uuid4())
        
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
                method="validation_failed",
                security_level=security_level.value,
                resource_limits=asdict(resource_limits),
                metadata={"execution_id": execution_id}
            )
        
        config = self.language_configs[language]
        if not config.get("supported", False):
            return ExecutionResult(
                success=False,
                output="",
                error=f"Railway 환경에서는 {language} 실행이 지원되지 않습니다. Python 또는 JavaScript만 지원됩니다.",
                execution_time=0,
                memory_usage_mb=0,
                cpu_usage_percent=0,
                language=language,
                method="language_not_supported",
                security_level=security_level.value,
                resource_limits=asdict(resource_limits),
                metadata={"execution_id": execution_id}
            )
        
        # 보안 검증
        is_safe, security_message = self._validate_code_security(code, language, security_level)
        if not is_safe:
            return ExecutionResult(
                success=False,
                output="",
                error=f"보안 검증 실패: {security_message}",
                execution_time=0,
                memory_usage_mb=0,
                cpu_usage_percent=0,
                language=language,
                method="security_failed",
                security_level=security_level.value,
                resource_limits=asdict(resource_limits),
                metadata={"execution_id": execution_id}
            )
        
        try:
            # Railway 환경에서는 항상 로컬 실행
            result = await self._execute_locally_enhanced(
                code, language, user_id, execution_id, resource_limits, security_level
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
            logger.error(f"코드 실행 중 오류 발생: {e}", exc_info=True)
            return ExecutionResult(
                success=False,
                output="",
                error=f"실행 오류: {str(e)}",
                execution_time=0,
                memory_usage_mb=0,
                cpu_usage_percent=0,
                language=language,
                method="error",
                security_level=security_level.value,
                resource_limits=asdict(resource_limits),
                metadata={"execution_id": execution_id, "error": str(e)}
            )
    
    async def _execute_locally_enhanced(
        self,
        code: str,
        language: str,
        user_id: str,
        execution_id: str,
        resource_limits: ResourceLimits,
        security_level: SecurityLevel
    ) -> ExecutionResult:
        """로컬에서 향상된 코드 실행 (Railway 최적화)"""
        start_time = datetime.now()
        config = self.language_configs[language]
        
        try:
            # 사용자별 임시 디렉토리에서 작업
            temp_dir = self._get_user_temp_dir(user_id)
            
            # 코드 실행
            if language == "python":
                result = subprocess.run(
                    ["python3", "-c", code],
                    capture_output=True,
                    text=True,
                    timeout=resource_limits.timeout_seconds,
                    cwd=temp_dir
                )
            elif language == "javascript":
                result = subprocess.run(
                    ["node", "-e", code],
                    capture_output=True,
                    text=True,
                    timeout=resource_limits.timeout_seconds,
                    cwd=temp_dir
                )
            else:
                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"지원하지 않는 언어: {language}",
                    execution_time=0,
                    memory_usage_mb=0,
                    cpu_usage_percent=0,
                    language=language,
                    method="language_not_supported",
                    security_level=security_level.value,
                    resource_limits=asdict(resource_limits),
                    metadata={"execution_id": execution_id}
                )
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # 결과 반환
            if result.returncode == 0:
                return ExecutionResult(
                    success=True,
                    output=result.stdout,
                    error=result.stderr if result.stderr else "",
                    execution_time=execution_time,
                    memory_usage_mb=0,
                    cpu_usage_percent=0,
                    language=language,
                    method="local",
                    security_level=security_level.value,
                    resource_limits=asdict(resource_limits),
                    metadata={"execution_id": execution_id, "returncode": result.returncode}
                )
            else:
                return ExecutionResult(
                    success=False,
                    output=result.stdout,
                    error=result.stderr if result.stderr else f"실행 실패 (종료 코드: {result.returncode})",
                    execution_time=execution_time,
                    memory_usage_mb=0,
                    cpu_usage_percent=0,
                    language=language,
                    method="local",
                    security_level=security_level.value,
                    resource_limits=asdict(resource_limits),
                    metadata={"execution_id": execution_id, "returncode": result.returncode}
                )
                
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="",
                error=f"코드 실행 시간 초과 ({resource_limits.timeout_seconds}초)",
                execution_time=resource_limits.timeout_seconds,
                memory_usage_mb=0,
                cpu_usage_percent=0,
                language=language,
                method="timeout",
                security_level=security_level.value,
                resource_limits=asdict(resource_limits),
                metadata={"execution_id": execution_id}
            )
        except Exception as e:
            logger.error(f"로컬 실행 중 오류 발생: {e}", exc_info=True)
            return ExecutionResult(
                success=False,
                output="",
                error=f"로컬 실행 오류: {str(e)}",
                execution_time=0,
                memory_usage_mb=0,
                cpu_usage_percent=0,
                language=language,
                method="error",
                security_level=security_level.value,
                resource_limits=asdict(resource_limits),
                metadata={"execution_id": execution_id, "error": str(e)}
            )
    
    def get_execution_history(self, user_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """실행 히스토리 조회"""
        if user_id:
            user_history = [
                record for record in self.execution_history.values()
                if record["user_id"] == user_id
            ]
            return sorted(user_history, key=lambda x: x["timestamp"], reverse=True)[:limit]
        else:
            all_history = list(self.execution_history.values())
            return sorted(all_history, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_supported_languages(self) -> Dict[str, Dict[str, Any]]:
        """지원 언어 목록"""
        return {
            language: {
                "supported": config["supported"],
                "extension": config["extension"],
                "railway_compatible": config["supported"]
            }
            for language, config in self.language_configs.items()
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """시스템 통계 조회"""
        return {
            "docker_available": False,
            "active_users": len(self.temp_dirs),
            "total_executions": len(self.execution_history),
            "supported_languages": len([lang for lang, config in self.language_configs.items() if config["supported"]]),
            "memory_usage": 0,
            "cpu_usage": 0,
            "timestamp": datetime.now().isoformat()
        }
    
    def cleanup_user_data(self, user_id: str):
        """사용자 데이터 정리"""
        if user_id in self.temp_dirs:
            import shutil
            temp_dir = self.temp_dirs[user_id]
            try:
                shutil.rmtree(temp_dir)
                del self.temp_dirs[user_id]
                logger.info(f"사용자 {user_id} 임시 디렉토리 삭제: {temp_dir}")
            except Exception as e:
                logger.error(f"임시 디렉토리 삭제 실패: {e}")
