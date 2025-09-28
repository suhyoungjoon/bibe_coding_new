"""
WebSocket 메시지 처리기
바이브 코딩을 위한 실시간 메시지 처리
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio

from .connection_manager import manager
from ..services.live_coding_service import LiveCodingService
from ..services.code_analysis_service import CodeAnalysisService
from ..services.ai_coding_assistant import AICodingAssistant
from ..services.interactive_assistant import InteractiveAssistant
from ..services.enhanced_sandbox_service import EnhancedSandboxService

logger = logging.getLogger(__name__)

class MessageHandler:
    """WebSocket 메시지 처리기"""
    
    def __init__(self):
        self.live_coding_service = LiveCodingService()
        self.code_analysis_service = CodeAnalysisService()
        self.ai_coding_assistant = AICodingAssistant()
        self.interactive_assistant = InteractiveAssistant()
        self.enhanced_sandbox_service = EnhancedSandboxService()
        self.message_handlers = {
            "ping": self._handle_ping,
            "join_room": self._handle_join_room,
            "leave_room": self._handle_leave_room,
            "code_change": self._handle_code_change,
            "cursor_change": self._handle_cursor_change,
            "execute_code": self._handle_execute_code,
            "request_analysis": self._handle_request_analysis,
            "request_suggestion": self._handle_request_suggestion,
            "chat_message": self._handle_chat_message,
            "file_operation": self._handle_file_operation,
            "ai_analysis": self._handle_ai_analysis,
            "ai_conversation": self._handle_ai_conversation,
            "request_ai_suggestions": self._handle_request_ai_suggestions,
            "sandbox_execute": self._handle_sandbox_execute,
            "sandbox_status": self._handle_sandbox_status,
        }
    
    async def handle_message(self, websocket, connection_id: str, message: str):
        """메시지 처리 메인 함수"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if not message_type:
                await self._send_error(connection_id, "메시지 타입이 필요합니다")
                return
            
            # 사용자 활동 업데이트
            manager.update_user_activity(connection_id)
            
            # 메시지 타입별 처리
            if message_type in self.message_handlers:
                await self.message_handlers[message_type](connection_id, data)
            else:
                await self._send_error(connection_id, f"알 수 없는 메시지 타입: {message_type}")
                
        except json.JSONDecodeError:
            await self._send_error(connection_id, "잘못된 JSON 형식")
        except Exception as e:
            logger.error(f"메시지 처리 오류 {connection_id}: {e}")
            await self._send_error(connection_id, f"메시지 처리 중 오류 발생: {str(e)}")
    
    async def _handle_ping(self, connection_id: str, data: Dict[str, Any]):
        """핑 메시지 처리"""
        await manager.send_personal_message({
            "type": "pong",
            "timestamp": datetime.now().isoformat(),
            "connection_id": connection_id
        }, connection_id)
    
    async def _handle_join_room(self, connection_id: str, data: Dict[str, Any]):
        """방 참여 처리"""
        room_id = data.get("room_id")
        if not room_id:
            await self._send_error(connection_id, "방 ID가 필요합니다")
            return
        
        # 방 참여
        manager.join_room(connection_id, room_id)
        
        # 방 멤버들에게 알림
        await manager.send_room_message({
            "type": "user_joined",
            "user_id": manager.get_connection_info(connection_id)["user_id"],
            "room_id": room_id,
            "timestamp": datetime.now().isoformat()
        }, room_id, exclude_connection=connection_id)
        
        # 참여 확인 메시지
        await manager.send_personal_message({
            "type": "joined_room",
            "room_id": room_id,
            "members": manager.get_room_members(room_id),
            "timestamp": datetime.now().isoformat()
        }, connection_id)
    
    async def _handle_leave_room(self, connection_id: str, data: Dict[str, Any]):
        """방 나가기 처리"""
        user_session = manager.get_connection_info(connection_id)
        current_room = user_session.get("current_room")
        
        if current_room:
            # 방 멤버들에게 알림
            await manager.send_room_message({
                "type": "user_left",
                "user_id": user_session["user_id"],
                "room_id": current_room,
                "timestamp": datetime.now().isoformat()
            }, current_room, exclude_connection=connection_id)
            
            # 방에서 제거
            manager.leave_room(connection_id)
            
            await manager.send_personal_message({
                "type": "left_room",
                "room_id": current_room,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
    
    async def _handle_code_change(self, connection_id: str, data: Dict[str, Any]):
        """코드 변경 처리"""
        file_path = data.get("file_path")
        content = data.get("content")
        change_type = data.get("change_type", "edit")  # edit, insert, delete
        position = data.get("position", {})
        
        if not file_path or content is None:
            await self._send_error(connection_id, "파일 경로와 내용이 필요합니다")
            return
        
        # 사용자 세션 업데이트
        user_session = manager.get_connection_info(connection_id)
        if user_session:
            user_session["coding_session"]["files"][file_path] = content
            user_session["coding_session"]["last_modified"] = datetime.now().isoformat()
        
        # 방 멤버들에게 코드 변경 알림
        current_room = user_session.get("current_room")
        if current_room:
            await manager.send_room_message({
                "type": "code_updated",
                "file_path": file_path,
                "content": content,
                "change_type": change_type,
                "position": position,
                "user_id": user_session["user_id"],
                "timestamp": datetime.now().isoformat()
            }, current_room, exclude_connection=connection_id)
        
        # 비동기 코드 분석 시작
        asyncio.create_task(self._analyze_code_async(connection_id, file_path, content))
    
    async def _handle_cursor_change(self, connection_id: str, data: Dict[str, Any]):
        """커서 위치 변경 처리"""
        position = data.get("position", {})
        file_path = data.get("file_path")
        
        # 사용자 세션 업데이트
        user_session = manager.get_connection_info(connection_id)
        if user_session:
            user_session["coding_session"]["cursor_position"] = position
            user_session["coding_session"]["current_file"] = file_path
        
        # 방 멤버들에게 커서 변경 알림
        current_room = user_session.get("current_room")
        if current_room:
            await manager.send_room_message({
                "type": "cursor_updated",
                "position": position,
                "file_path": file_path,
                "user_id": user_session["user_id"],
                "timestamp": datetime.now().isoformat()
            }, current_room, exclude_connection=connection_id)
    
    async def _handle_execute_code(self, connection_id: str, data: Dict[str, Any]):
        """코드 실행 처리"""
        code = data.get("code")
        language = data.get("language", "python")
        file_path = data.get("file_path")
        execution_mode = data.get("execution_mode")  # "docker" 또는 "local"
        user_id = manager.get_connection_info(connection_id).get("user_id", "default")
        
        if not code:
            await self._send_error(connection_id, "실행할 코드가 필요합니다")
            return
        
        # 코드 실행 시작 알림
        await manager.send_personal_message({
            "type": "execution_started",
            "execution_mode": execution_mode or "auto",
            "timestamp": datetime.now().isoformat()
        }, connection_id)
        
        try:
            # 코드 실행
            result = await self.live_coding_service.execute_code(
                code, language, file_path, user_id, execution_mode
            )
            logger.info(f"코드 실행 결과: {result}")
            
            # 실행 결과 전송
            await manager.send_personal_message({
                "type": "execution_result",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
        except Exception as e:
            logger.error(f"코드 실행 중 오류 발생: {e}", exc_info=True)
            # 실행 오류 전송
            await manager.send_personal_message({
                "type": "execution_error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }, connection_id)
    
    async def _handle_request_analysis(self, connection_id: str, data: Dict[str, Any]):
        """코드 분석 요청 처리"""
        file_path = data.get("file_path")
        content = data.get("content")
        
        if not file_path or not content:
            await self._send_error(connection_id, "파일 경로와 내용이 필요합니다")
            return
        
        try:
            # 코드 분석
            analysis = await self.code_analysis_service.analyze_code(content, file_path)
            
            # 분석 결과 전송
            await manager.send_personal_message({
                "type": "analysis_result",
                "file_path": file_path,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
        except Exception as e:
            await self._send_error(connection_id, f"코드 분석 실패: {str(e)}")
    
    async def _handle_request_suggestion(self, connection_id: str, data: Dict[str, Any]):
        """코드 제안 요청 처리"""
        file_path = data.get("file_path")
        content = data.get("content")
        position = data.get("position", {})
        
        if not file_path or content is None:
            await self._send_error(connection_id, "파일 경로와 내용이 필요합니다")
            return
        
        try:
            # 코드 제안 생성
            suggestions = await self.code_analysis_service.generate_suggestions(content, file_path, position)
            
            # 제안 결과 전송
            await manager.send_personal_message({
                "type": "suggestions_result",
                "file_path": file_path,
                "suggestions": suggestions,
                "position": position,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
        except Exception as e:
            await self._send_error(connection_id, f"제안 생성 실패: {str(e)}")
    
    async def _handle_chat_message(self, connection_id: str, data: Dict[str, Any]):
        """채팅 메시지 처리"""
        message = data.get("message")
        if not message:
            await self._send_error(connection_id, "메시지 내용이 필요합니다")
            return
        
        user_session = manager.get_connection_info(connection_id)
        current_room = user_session.get("current_room")
        
        if current_room:
            # 방 멤버들에게 채팅 메시지 전송
            await manager.send_room_message({
                "type": "chat_message",
                "message": message,
                "user_id": user_session["user_id"],
                "room_id": current_room,
                "timestamp": datetime.now().isoformat()
            }, current_room)
    
    async def _handle_file_operation(self, connection_id: str, data: Dict[str, Any]):
        """파일 작업 처리"""
        operation = data.get("operation")  # create, delete, rename
        file_path = data.get("file_path")
        new_path = data.get("new_path")
        
        if not operation or not file_path:
            await self._send_error(connection_id, "작업 타입과 파일 경로가 필요합니다")
            return
        
        try:
            # 파일 작업 실행
            result = await self.live_coding_service.handle_file_operation(operation, file_path, new_path)
            
            # 작업 결과 전송
            await manager.send_personal_message({
                "type": "file_operation_result",
                "operation": operation,
                "file_path": file_path,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
            # 방 멤버들에게 파일 변경 알림
            user_session = manager.get_connection_info(connection_id)
            current_room = user_session.get("current_room")
            if current_room:
                await manager.send_room_message({
                    "type": "file_changed",
                    "operation": operation,
                    "file_path": file_path,
                    "new_path": new_path,
                    "user_id": user_session["user_id"],
                    "timestamp": datetime.now().isoformat()
                }, current_room, exclude_connection=connection_id)
            
        except Exception as e:
            await self._send_error(connection_id, f"파일 작업 실패: {str(e)}")
    
    async def _handle_ai_analysis(self, connection_id: str, data: Dict[str, Any]):
        """AI 기반 고급 코드 분석 처리"""
        file_path = data.get("file_path")
        content = data.get("content")
        
        if not file_path or not content:
            await self._send_error(connection_id, "파일 경로와 내용이 필요합니다")
            return
        
        try:
            # AI 분석 시작 알림
            await manager.send_personal_message({
                "type": "ai_analysis_started",
                "file_path": file_path,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
            # AI 기반 분석 실행
            user_session = manager.get_connection_info(connection_id)
            user_id = user_session["user_id"] if user_session else connection_id
            
            analysis_result = await self.ai_coding_assistant.analyze_and_suggest(
                content, file_path, user_id
            )
            
            # 분석 결과 전송
            await manager.send_personal_message({
                "type": "ai_analysis_result",
                "file_path": file_path,
                "analysis": {
                    "success": analysis_result.get("success", False),
                    "metrics": analysis_result.get("basic_analysis", {}).get("metrics", {}),
                    "quality_score": analysis_result.get("basic_analysis", {}).get("quality_score", 0),
                    "suggestions": analysis_result.get("suggestions", []),
                    "ai_analysis": analysis_result.get("ai_analysis", {}),
                    "issues": analysis_result.get("basic_analysis", {}).get("issues", [])
                },
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
        except Exception as e:
            await self._send_error(connection_id, f"AI 분석 실패: {str(e)}")
    
    async def _handle_ai_conversation(self, connection_id: str, data: Dict[str, Any]):
        """AI 대화형 어시스턴트 처리"""
        message = data.get("message")
        current_code = data.get("current_code")
        file_path = data.get("file_path")
        context = data.get("context", {})
        
        if not message:
            await self._send_error(connection_id, "메시지 내용이 필요합니다")
            return
        
        try:
            # AI 대화 처리 시작 알림
            await manager.send_personal_message({
                "type": "ai_conversation_started",
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
            # 사용자 정보 가져오기
            user_session = manager.get_connection_info(connection_id)
            user_id = user_session["user_id"] if user_session else connection_id
            
            # AI 대화 처리
            conversation_result = await self.interactive_assistant.process_user_message(
                message, user_id, current_code, file_path, context
            )
            
            # 대화 결과 전송
            await manager.send_personal_message({
                "type": "ai_conversation_result",
                "conversation": conversation_result,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
        except Exception as e:
            await self._send_error(connection_id, f"AI 대화 처리 실패: {str(e)}")
    
    async def _handle_request_ai_suggestions(self, connection_id: str, data: Dict[str, Any]):
        """AI 제안 요청 처리"""
        file_path = data.get("file_path")
        content = data.get("content")
        position = data.get("position", {})
        
        if not file_path or content is None:
            await self._send_error(connection_id, "파일 경로와 내용이 필요합니다")
            return
        
        try:
            # 사용자 정보 가져오기
            user_session = manager.get_connection_info(connection_id)
            user_id = user_session["user_id"] if user_session else connection_id
            
            # 컨텍스트 인식 제안 생성
            suggestions = await self.ai_coding_assistant.get_context_aware_suggestions(
                content, file_path, user_id, position
            )
            
            # 제안 결과 전송
            await manager.send_personal_message({
                "type": "ai_suggestions_result",
                "file_path": file_path,
                "suggestions": suggestions,
                "position": position,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
        except Exception as e:
            await self._send_error(connection_id, f"AI 제안 생성 실패: {str(e)}")
    
    async def _handle_sandbox_execute(self, connection_id: str, data: Dict[str, Any]):
        """샌드박스 코드 실행 처리 (실시간 상태 업데이트)"""
        code = data.get("code")
        language = data.get("language", "python")
        security_level = data.get("security_level", "MEDIUM")
        user_id = data.get("user_id", connection_id)
        
        if not code:
            await self._send_error(connection_id, "실행할 코드가 필요합니다")
            return
        
        try:
            # 실행 시작 알림
            await manager.send_personal_message({
                "type": "sandbox_execution_started",
                "language": language,
                "security_level": security_level,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
            # 비동기로 코드 실행
            asyncio.create_task(self._execute_sandbox_code_async(
                connection_id, code, language, security_level, user_id
            ))
            
        except Exception as e:
            await self._send_error(connection_id, f"샌드박스 실행 시작 실패: {str(e)}")
    
    async def _execute_sandbox_code_async(
        self, 
        connection_id: str, 
        code: str, 
        language: str, 
        security_level: str, 
        user_id: str
    ):
        """비동기 샌드박스 코드 실행"""
        try:
            # 샌드박스 서비스에서 실행
            result = await self.enhanced_sandbox_service.execute_code_enhanced(
                code=code,
                language=language,
                user_id=user_id,
                security_level=security_level
            )
            
            # 실행 완료 알림
            await manager.send_personal_message({
                "type": "sandbox_execution_completed",
                "result": {
                    "success": result.success,
                    "output": result.output,
                    "error": result.error,
                    "execution_time": result.execution_time,
                    "memory_used": result.memory_usage_mb,
                    "cpu_usage": result.cpu_usage_percent
                },
                "language": language,
                "security_level": security_level,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
        except Exception as e:
            # 실행 실패 알림
            await manager.send_personal_message({
                "type": "sandbox_execution_failed",
                "error": str(e),
                "language": language,
                "security_level": security_level,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
    
    async def _handle_sandbox_status(self, connection_id: str, data: Dict[str, Any]):
        """샌드박스 상태 요청 처리"""
        try:
            # 시스템 상태 가져오기
            stats = await self.enhanced_sandbox_service.get_system_stats()
            
            # 상태 정보 전송
            await manager.send_personal_message({
                "type": "sandbox_status_update",
                "stats": {
                    "cpu_percent": stats.get("cpu_percent", 0),
                    "memory_percent": stats.get("memory_percent", 0),
                    "active_executions": stats.get("active_executions", 0),
                    "total_executions": stats.get("total_executions", 0)
                },
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
        except Exception as e:
            await self._send_error(connection_id, f"샌드박스 상태 조회 실패: {str(e)}")
    
    async def _analyze_code_async(self, connection_id: str, file_path: str, content: str):
        """비동기 코드 분석"""
        try:
            analysis = await self.code_analysis_service.analyze_code(content, file_path)
            
            # 분석 결과 전송 (자동 분석)
            await manager.send_personal_message({
                "type": "auto_analysis",
                "file_path": file_path,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }, connection_id)
            
        except Exception as e:
            logger.error(f"자동 코드 분석 실패 {connection_id}: {e}")
    
    async def _send_error(self, connection_id: str, error_message: str):
        """오류 메시지 전송"""
        await manager.send_personal_message({
            "type": "error",
            "message": error_message,
            "timestamp": datetime.now().isoformat()
        }, connection_id)

# 전역 메시지 처리기 인스턴스
message_handler = MessageHandler()
