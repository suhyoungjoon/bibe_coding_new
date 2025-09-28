"""
WebSocket 라우트
바이브 코딩을 위한 실시간 WebSocket 엔드포인트
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
import logging
import json

from app.websocket.connection_manager import manager
from app.websocket.message_handler import message_handler

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/ws/{connection_id}")
async def websocket_endpoint(websocket: WebSocket, connection_id: str):
    """WebSocket 연결 엔드포인트"""
    connection_id = await manager.connect(websocket, connection_id)
    
    try:
        while True:
            # 메시지 수신
            data = await websocket.receive_text()
            
            # 메시지 처리
            await message_handler.handle_message(websocket, connection_id, data)
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket 연결 종료: {connection_id}")
        manager.disconnect(connection_id)
    except Exception as e:
        logger.error(f"WebSocket 오류 {connection_id}: {e}")
        manager.disconnect(connection_id)

@router.websocket("/ws/room/{room_id}")
async def websocket_room_endpoint(websocket: WebSocket, room_id: str):
    """방 기반 WebSocket 연결 엔드포인트"""
    connection_id = await manager.connect(websocket)
    
    # 자동으로 방에 참여
    manager.join_room(connection_id, room_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            await message_handler.handle_message(websocket, connection_id, data)
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket 연결 종료: {connection_id}")
        manager.disconnect(connection_id)
    except Exception as e:
        logger.error(f"WebSocket 오류 {connection_id}: {e}")
        manager.disconnect(connection_id)

@router.get("/ws/demo")
async def websocket_demo():
    """WebSocket 데모 페이지"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agentic AI 바이브 코딩 데모</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            #messages { height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; }
            #messageInput { width: 70%; }
            #sendButton { width: 25%; }
            .message { margin: 5px 0; padding: 5px; border-radius: 5px; }
            .system { background-color: #f0f0f0; }
            .user { background-color: #e3f2fd; }
            .error { background-color: #ffebee; color: red; }
            .success { background-color: #e8f5e8; color: green; }
        </style>
    </head>
    <body>
        <h1>🚀 Agentic AI 바이브 코딩 데모</h1>
        
        <div>
            <h3>연결 상태: <span id="status">연결 중...</span></h3>
            <button id="connectButton" onclick="connect()">연결</button>
            <button id="disconnectButton" onclick="disconnect()">연결 해제</button>
        </div>
        
        <div>
            <h3>방 관리</h3>
            <input type="text" id="roomInput" placeholder="방 ID" />
            <button onclick="joinRoom()">방 참여</button>
            <button onclick="leaveRoom()">방 나가기</button>
        </div>
        
        <div>
            <h3>코드 테스트</h3>
            <textarea id="codeInput" rows="8" cols="80" placeholder="실행할 코드를 입력하세요">def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f"Fibonacci(10) = {result}")</textarea><br><br>
            <button onclick="executeCode()">코드 실행</button>
            <button onclick="analyzeCode()">기본 분석</button>
            <button onclick="aiAnalyze()">AI 고급 분석</button>
            <button onclick="getAISuggestions()">AI 제안</button>
        </div>
        
        <div>
            <h3>AI 대화형 어시스턴트</h3>
            <input type="text" id="aiMessageInput" placeholder="AI에게 질문하세요 (예: 이 코드를 최적화해주세요)" style="width: 70%;" />
            <button onclick="sendAIMessage()">AI에게 질문</button>
            <div id="aiResponses" style="height: 200px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; margin-top: 10px; background-color: #f9f9f9;"></div>
        </div>
        
        <div>
            <h3>메시지</h3>
            <div id="messages"></div>
            <input type="text" id="messageInput" placeholder="메시지를 입력하세요" />
            <button id="sendButton" onclick="sendMessage()">전송</button>
        </div>

        <script>
            let ws = null;
            let connectionId = null;

            function connect() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/api/v1/ws/demo`;
                
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function(event) {
                    addMessage('시스템', 'WebSocket 연결됨', 'success');
                    document.getElementById('status').textContent = '연결됨';
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    handleMessage(data);
                };
                
                ws.onclose = function(event) {
                    addMessage('시스템', 'WebSocket 연결 종료', 'system');
                    document.getElementById('status').textContent = '연결 해제됨';
                };
                
                ws.onerror = function(error) {
                    addMessage('오류', 'WebSocket 오류: ' + error, 'error');
                };
            }

            function disconnect() {
                if (ws) {
                    ws.close();
                    ws = null;
                }
            }

            function joinRoom() {
                const roomId = document.getElementById('roomInput').value;
                if (roomId && ws) {
                    ws.send(JSON.stringify({
                        type: 'join_room',
                        room_id: roomId
                    }));
                }
            }

            function leaveRoom() {
                if (ws) {
                    ws.send(JSON.stringify({
                        type: 'leave_room'
                    }));
                }
            }

            function executeCode() {
                const code = document.getElementById('codeInput').value;
                if (code && ws) {
                    ws.send(JSON.stringify({
                        type: 'execute_code',
                        code: code,
                        language: 'python'
                    }));
                }
            }

            function analyzeCode() {
                const code = document.getElementById('codeInput').value;
                if (code && ws) {
                    ws.send(JSON.stringify({
                        type: 'request_analysis',
                        file_path: 'test.py',
                        content: code
                    }));
                }
            }

            function aiAnalyze() {
                const code = document.getElementById('codeInput').value;
                if (code && ws) {
                    ws.send(JSON.stringify({
                        type: 'ai_analysis',
                        file_path: 'test.py',
                        content: code
                    }));
                }
            }

            function getAISuggestions() {
                const code = document.getElementById('codeInput').value;
                if (code && ws) {
                    ws.send(JSON.stringify({
                        type: 'request_ai_suggestions',
                        file_path: 'test.py',
                        content: code,
                        position: {line: 0, column: 0}
                    }));
                }
            }

            function sendAIMessage() {
                const messageInput = document.getElementById('aiMessageInput');
                const message = messageInput.value;
                const code = document.getElementById('codeInput').value;
                
                if (message && ws) {
                    ws.send(JSON.stringify({
                        type: 'ai_conversation',
                        message: message,
                        current_code: code,
                        file_path: 'test.py',
                        context: {}
                    }));
                    messageInput.value = '';
                }
            }

            function sendMessage() {
                const messageInput = document.getElementById('messageInput');
                const message = messageInput.value;
                if (message && ws) {
                    ws.send(JSON.stringify({
                        type: 'chat_message',
                        message: message
                    }));
                    messageInput.value = '';
                }
            }

            function handleMessage(data) {
                switch(data.type) {
                    case 'connection_established':
                        connectionId = data.connection_id;
                        addMessage('시스템', `연결 ID: ${data.connection_id}`, 'success');
                        break;
                    case 'pong':
                        addMessage('시스템', '핑 응답 받음', 'system');
                        break;
                    case 'joined_room':
                        addMessage('시스템', `방 참여: ${data.room_id}`, 'success');
                        break;
                    case 'left_room':
                        addMessage('시스템', `방 나감: ${data.room_id}`, 'system');
                        break;
                    case 'execution_result':
                        addMessage('실행 결과', data.result.output || '실행 완료', 'success');
                        break;
                    case 'execution_error':
                        addMessage('실행 오류', data.error, 'error');
                        break;
                    case 'analysis_result':
                        addMessage('분석 결과', JSON.stringify(data.analysis, null, 2), 'success');
                        break;
                    case 'ai_analysis_started':
                        addMessage('AI', 'AI 고급 분석을 시작합니다...', 'system');
                        break;
                    case 'ai_analysis_result':
                        const aiAnalysis = data.analysis;
                        if (aiAnalysis.success) {
                            addMessage('AI 분석', `품질 평가: ${aiAnalysis.ai_analysis?.quality_assessment || 'N/A'}`, 'success');
                            if (aiAnalysis.suggestions && aiAnalysis.suggestions.length > 0) {
                                aiAnalysis.suggestions.forEach(suggestion => {
                                    addMessage('AI 제안', `${suggestion.title}: ${suggestion.description}`, 'success');
                                });
                            }
                        } else {
                            addMessage('AI 분석', aiAnalysis.error, 'error');
                        }
                        break;
                    case 'ai_conversation_started':
                        addMessage('AI', 'AI 어시스턴트가 응답을 준비하고 있습니다...', 'system');
                        break;
                    case 'ai_conversation_result':
                        const conversation = data.conversation;
                        if (conversation.success) {
                            const response = conversation.response;
                            addAIResponse(response.content, response.type);
                            
                            if (response.generated_code) {
                                addAIResponse('생성된 코드:\\n' + response.generated_code, 'code');
                            }
                            if (response.suggestions && response.suggestions.length > 0) {
                                response.suggestions.forEach(suggestion => {
                                    addAIResponse('• ' + suggestion, 'suggestion');
                                });
                            }
                        } else {
                            addAIResponse('AI 응답 오류: ' + conversation.error, 'error');
                        }
                        break;
                    case 'ai_suggestions_result':
                        if (data.suggestions && data.suggestions.length > 0) {
                            data.suggestions.forEach(suggestion => {
                                addMessage('AI 제안', `${suggestion.type}: ${suggestion.text}`, 'success');
                            });
                        } else {
                            addMessage('AI 제안', '제안할 수 있는 내용이 없습니다.', 'system');
                        }
                        break;
                    case 'chat_message':
                        addMessage(data.user_id, data.message, 'user');
                        break;
                    case 'error':
                        addMessage('오류', data.message, 'error');
                        break;
                    default:
                        addMessage('알 수 없음', JSON.stringify(data, null, 2), 'system');
                }
            }

            function addMessage(sender, message, type) {
                const messagesDiv = document.getElementById('messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}`;
                messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }

            function addAIResponse(message, type) {
                const aiResponsesDiv = document.getElementById('aiResponses');
                const responseDiv = document.createElement('div');
                responseDiv.className = `ai-response ${type}`;
                
                let formattedMessage = message;
                if (type === 'code') {
                    formattedMessage = `<pre style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">${message}</pre>`;
                }
                
                responseDiv.innerHTML = `<strong>🤖 AI:</strong> ${formattedMessage}`;
                aiResponsesDiv.appendChild(responseDiv);
                aiResponsesDiv.scrollTop = aiResponsesDiv.scrollHeight;
            }

            // Enter 키로 메시지 전송
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // AI 메시지 입력에도 Enter 키 이벤트 추가
            document.getElementById('aiMessageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendAIMessage();
                }
            });

            // 페이지 로드 시 자동 연결
            window.onload = function() {
                connect();
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
