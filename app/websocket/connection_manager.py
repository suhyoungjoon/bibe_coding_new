"""
WebSocket 연결 관리자
실시간 바이브 코딩을 위한 WebSocket 연결 관리
"""

import json
import logging
from typing import Dict, List, Optional, Any
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class ConnectionManager:
    """WebSocket 연결 관리자"""
    
    def __init__(self):
        # 활성 연결 저장
        self.active_connections: Dict[str, WebSocket] = {}
        # 사용자별 연결 정보
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        # 방별 연결 관리
        self.room_connections: Dict[str, List[str]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str = None) -> str:
        """새 연결 수락"""
        await websocket.accept()
        
        # 고유 연결 ID 생성
        connection_id = str(uuid.uuid4())
        self.active_connections[connection_id] = websocket
        
        # 사용자 세션 정보 초기화
        if user_id is None:
            user_id = f"user_{connection_id[:8]}"
        
        self.user_sessions[connection_id] = {
            "user_id": user_id,
            "connected_at": datetime.now(),
            "last_activity": datetime.now(),
            "current_room": None,
            "coding_session": {
                "language": "python",
                "files": {},
                "cursor_position": {"line": 0, "column": 0},
                "selection": None
            }
        }
        
        logger.info(f"새 연결 수락: {connection_id} (사용자: {user_id})")
        
        # 연결 확인 메시지 전송
        await self.send_personal_message({
            "type": "connection_established",
            "connection_id": connection_id,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }, connection_id)
        
        return connection_id
    
    def disconnect(self, connection_id: str):
        """연결 종료"""
        if connection_id in self.active_connections:
            # 방에서 제거
            user_session = self.user_sessions.get(connection_id, {})
            current_room = user_session.get("current_room")
            if current_room and current_room in self.room_connections:
                self.room_connections[current_room].remove(connection_id)
                if not self.room_connections[current_room]:
                    del self.room_connections[current_room]
            
            # 연결 정보 삭제
            del self.active_connections[connection_id]
            if connection_id in self.user_sessions:
                del self.user_sessions[connection_id]
            
            logger.info(f"연결 종료: {connection_id}")
    
    async def send_personal_message(self, message: Dict[str, Any], connection_id: str):
        """개인 메시지 전송"""
        if connection_id in self.active_connections:
            try:
                await self.active_connections[connection_id].send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"메시지 전송 실패 {connection_id}: {e}")
                self.disconnect(connection_id)
    
    async def send_room_message(self, message: Dict[str, Any], room_id: str, exclude_connection: str = None):
        """방 전체에 메시지 전송"""
        if room_id in self.room_connections:
            for connection_id in self.room_connections[room_id]:
                if connection_id != exclude_connection:
                    await self.send_personal_message(message, connection_id)
    
    async def broadcast(self, message: Dict[str, Any]):
        """모든 연결에 브로드캐스트"""
        for connection_id in list(self.active_connections.keys()):
            await self.send_personal_message(message, connection_id)
    
    def join_room(self, connection_id: str, room_id: str):
        """방 참여"""
        if connection_id in self.active_connections:
            # 기존 방에서 제거
            user_session = self.user_sessions.get(connection_id, {})
            current_room = user_session.get("current_room")
            if current_room and current_room in self.room_connections:
                self.room_connections[current_room].remove(connection_id)
            
            # 새 방에 참여
            if room_id not in self.room_connections:
                self.room_connections[room_id] = []
            self.room_connections[room_id].append(connection_id)
            
            # 사용자 세션 업데이트
            self.user_sessions[connection_id]["current_room"] = room_id
            
            logger.info(f"사용자 {connection_id}가 방 {room_id}에 참여")
    
    def leave_room(self, connection_id: str):
        """방 나가기"""
        user_session = self.user_sessions.get(connection_id, {})
        current_room = user_session.get("current_room")
        if current_room and current_room in self.room_connections:
            self.room_connections[current_room].remove(connection_id)
            if not self.room_connections[current_room]:
                del self.room_connections[current_room]
        
        self.user_sessions[connection_id]["current_room"] = None
        logger.info(f"사용자 {connection_id}가 방에서 나감")
    
    def update_user_activity(self, connection_id: str):
        """사용자 활동 시간 업데이트"""
        if connection_id in self.user_sessions:
            self.user_sessions[connection_id]["last_activity"] = datetime.now()
    
    def get_connection_info(self, connection_id: str) -> Optional[Dict[str, Any]]:
        """연결 정보 조회"""
        return self.user_sessions.get(connection_id)
    
    def get_room_members(self, room_id: str) -> List[str]:
        """방 멤버 목록 조회"""
        return self.room_connections.get(room_id, [])
    
    def get_active_connections_count(self) -> int:
        """활성 연결 수 조회"""
        return len(self.active_connections)
    
    def get_rooms_info(self) -> Dict[str, Any]:
        """방 정보 조회"""
        return {
            room_id: {
                "member_count": len(members),
                "members": [self.user_sessions.get(conn_id, {}).get("user_id", "unknown") 
                           for conn_id in members]
            }
            for room_id, members in self.room_connections.items()
        }

# 전역 연결 관리자 인스턴스
manager = ConnectionManager()
