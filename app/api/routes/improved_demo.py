"""
개선된 데모 페이지
현대적이고 직관적인 UI/UX 제공
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/demo/improved")
async def improved_demo():
    """개선된 바이브 코딩 데모 페이지"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🚀 Agentic AI 바이브 코딩</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }

            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }

            .header {
                text-align: center;
                margin-bottom: 30px;
                color: white;
            }

            .header h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }

            .header p {
                font-size: 1.1rem;
                opacity: 0.9;
            }

            .main-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }

            .card {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }

            .card-header {
                display: flex;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f0f0f0;
            }

            .card-header h3 {
                font-size: 1.3rem;
                color: #4a5568;
                margin-left: 10px;
            }

            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }

            .status-connected {
                background-color: #48bb78;
            }

            .status-disconnected {
                background-color: #f56565;
            }

            .status-connecting {
                background-color: #ed8936;
            }

            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }

            .connection-panel {
                grid-column: 1 / -1;
            }

            .connection-controls {
                display: flex;
                gap: 10px;
                align-items: center;
                flex-wrap: wrap;
            }

            .btn {
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }

            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }

            .btn-secondary {
                background: #e2e8f0;
                color: #4a5568;
            }

            .btn-secondary:hover {
                background: #cbd5e0;
            }

            .btn-danger {
                background: #f56565;
                color: white;
            }

            .btn-danger:hover {
                background: #e53e3e;
            }

            .btn-success {
                background: #48bb78;
                color: white;
            }

            .btn-success:hover {
                background: #38a169;
            }

            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none !important;
            }

            .input-group {
                display: flex;
                gap: 10px;
                align-items: center;
                margin-bottom: 15px;
            }

            .input-group input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
                transition: border-color 0.3s ease;
            }

            .input-group input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }

            .code-editor {
                width: 100%;
                min-height: 300px;
                padding: 20px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-family: 'Fira Code', 'Consolas', monospace;
                font-size: 14px;
                line-height: 1.5;
                background: #f8f9fa;
                resize: vertical;
                transition: border-color 0.3s ease;
            }

            .code-editor:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }

            .execution-mode {
                margin-bottom: 15px;
                padding: 10px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .execution-mode label {
                color: #fff;
                margin-right: 10px;
                font-weight: 500;
            }
            
            .mode-select {
                padding: 8px 12px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.1);
                color: #fff;
                font-size: 14px;
            }
            
            .mode-select option {
                background: #2c3e50;
                color: #fff;
            }
            
            .code-actions {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 10px;
                margin-top: 15px;
            }

            .ai-chat {
                display: flex;
                flex-direction: column;
                height: 400px;
            }

            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 15px;
                background: #f8f9fa;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                margin-bottom: 15px;
                max-height: 300px;
            }

            .chat-input-group {
                display: flex;
                gap: 10px;
            }

            .chat-input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 25px;
                font-size: 14px;
                transition: border-color 0.3s ease;
            }

            .chat-input:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }

            .message {
                margin-bottom: 15px;
                padding: 12px 16px;
                border-radius: 12px;
                animation: slideIn 0.3s ease;
            }

            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .message.system {
                background: #e2e8f0;
                color: #4a5568;
            }

            .message.user {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin-left: 20px;
            }

            .message.ai {
                background: #f0fff4;
                border-left: 4px solid #48bb78;
                margin-right: 20px;
            }

            .message.error {
                background: #fed7d7;
                border-left: 4px solid #f56565;
                color: #c53030;
            }

            .message.success {
                background: #c6f6d5;
                border-left: 4px solid #48bb78;
                color: #22543d;
            }

            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 10px;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            .activity-log {
                grid-column: 1 / -1;
                max-height: 300px;
            }

            .log-messages {
                max-height: 200px;
                overflow-y: auto;
                padding: 15px;
                background: #1a202c;
                color: #e2e8f0;
                border-radius: 8px;
                font-family: 'Fira Code', 'Consolas', monospace;
                font-size: 12px;
                line-height: 1.4;
            }

            .log-message {
                margin-bottom: 8px;
                padding: 4px 0;
            }

            .log-timestamp {
                color: #718096;
                margin-right: 10px;
            }

            .log-type {
                font-weight: bold;
                margin-right: 10px;
            }

            .log-type.info { color: #63b3ed; }
            .log-type.success { color: #68d391; }
            .log-type.warning { color: #f6e05e; }
            .log-type.error { color: #fc8181; }

            .room-info {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 15px;
                padding: 15px;
                background: #f7fafc;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }

            .room-badge {
                background: #667eea;
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
            }

            .progress-bar {
                width: 100%;
                height: 4px;
                background: #e2e8f0;
                border-radius: 2px;
                overflow: hidden;
                margin: 10px 0;
            }

            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 2px;
                transition: width 0.3s ease;
                animation: shimmer 2s infinite;
            }

            @keyframes shimmer {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }

            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }

            .stat-card {
                text-align: center;
                padding: 15px;
                background: #f7fafc;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            }

            .stat-number {
                font-size: 1.5rem;
                font-weight: bold;
                color: #667eea;
            }

            .stat-label {
                font-size: 0.8rem;
                color: #718096;
                margin-top: 5px;
            }

            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                z-index: 1000;
                animation: slideInRight 0.3s ease;
            }

            .notification.success {
                background: #48bb78;
            }

            .notification.error {
                background: #f56565;
            }

            .notification.info {
                background: #4299e1;
            }

            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }

            .tooltip {
                position: relative;
                display: inline-block;
                cursor: help;
            }

            .tooltip .tooltiptext {
                visibility: hidden;
                width: 200px;
                background-color: #1a202c;
                color: white;
                text-align: center;
                border-radius: 6px;
                padding: 8px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -100px;
                font-size: 12px;
                opacity: 0;
                transition: opacity 0.3s;
            }

            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }

            /* 반응형 디자인 */
            @media (max-width: 768px) {
                .main-grid {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 2rem;
                }
                
                .code-actions {
                    grid-template-columns: 1fr;
                }
                
                .connection-controls {
                    flex-direction: column;
                    align-items: stretch;
                }
                
                .btn {
                    width: 100%;
                    margin-bottom: 5px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Agentic AI 바이브 코딩</h1>
                <p>실시간 AI 어시스턴트와 함께하는 지능형 코딩 환경</p>
            </div>

            <div class="main-grid">
                <!-- 연결 상태 패널 -->
                <div class="card connection-panel">
                    <div class="card-header">
                        <div class="status-indicator status-connecting" id="statusIndicator"></div>
                        <h3>🔌 연결 상태</h3>
                    </div>
                    <div class="connection-controls">
                        <button class="btn btn-primary" id="connectButton" onclick="connect()">
                            연결하기
                        </button>
                        <button class="btn btn-secondary" id="disconnectButton" onclick="disconnect()" disabled>
                            연결 해제
                        </button>
                        <div class="room-info" id="roomInfo" style="display: none;">
                            <span class="room-badge" id="roomBadge">방 없음</span>
                            <input type="text" id="roomInput" placeholder="방 ID 입력" class="chat-input" style="flex: 1;">
                            <button class="btn btn-success" onclick="joinRoom()">참여</button>
                            <button class="btn btn-danger" onclick="leaveRoom()">나가기</button>
                        </div>
                    </div>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number" id="messageCount">0</div>
                            <div class="stat-label">메시지</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="aiInteractions">0</div>
                            <div class="stat-label">AI 상호작용</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="codeExecutions">0</div>
                            <div class="stat-label">코드 실행</div>
                        </div>
                    </div>
                </div>

                <!-- 코드 에디터 패널 -->
                <div class="card">
                    <div class="card-header">
                        <span>💻</span>
                        <h3>스마트 코드 에디터</h3>
                    </div>
                        <textarea id="codeEditor" class="code-editor" placeholder="코드를 입력하세요...">def fibonacci(n):
    \"\"\"
    Fibonacci sequence calculation function
    \"\"\"
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test
result = fibonacci(10)
print(f"Fibonacci(10) = {result}")

# More efficient version
def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

result2 = fibonacci_iterative(10)
print(f"Iterative Fibonacci(10) = {result2}")</textarea>
                    
                    <div class="execution-mode">
                        <label>실행 모드:</label>
                        <select id="executionMode" class="mode-select">
                            <option value="auto">자동 선택</option>
                            <option value="local">로컬 실행</option>
                            <option value="docker">Docker 실행</option>
                        </select>
                    </div>
                    
                    <div class="code-actions">
                        <button class="btn btn-primary" onclick="executeCode()">
                            ▶️ 실행
                        </button>
                        <button class="btn btn-secondary" onclick="analyzeCode()">
                            🔍 기본 분석
                        </button>
                        <button class="btn btn-success" onclick="aiAnalyze()">
                            🧠 AI 분석
                        </button>
                        <button class="btn btn-info" onclick="saveCode()">
                            💾 저장
                        </button>
                        <button class="btn btn-warning" onclick="loadCode()">
                            📁 열기
                        </button>
                        <button class="btn btn-danger" onclick="clearCode()">
                            🗑️ 지우기
                        </button>
                        <button class="btn btn-secondary" onclick="getAISuggestions()">
                            💡 AI 제안
                        </button>
                    </div>
                </div>

                <!-- AI 대화 패널 -->
                <div class="card">
                    <div class="card-header">
                        <span>🤖</span>
                        <h3>AI 어시스턴트</h3>
                    </div>
                    <div class="ai-chat">
                        <div class="chat-messages" id="aiChatMessages">
                            <div class="message ai">
                                안녕하세요! 저는 AI 코딩 어시스턴트입니다. 코드에 대해 질문하거나 개선을 요청해보세요!
                            </div>
                        </div>
                        <div class="chat-input-group">
                            <input type="text" id="aiMessageInput" class="chat-input" 
                                   placeholder="예: 이 코드를 최적화해주세요, 버그를 찾아주세요, 리팩토링해주세요">
                            <button class="btn btn-primary" onclick="sendAIMessage()">
                                전송
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 활동 로그 패널 -->
                <div class="card activity-log">
                    <div class="card-header">
                        <span>📊</span>
                        <h3>실시간 활동 로그</h3>
                    </div>
                    <div class="log-messages" id="logMessages">
                        <div class="log-message">
                            <span class="log-timestamp">[시작]</span>
                            <span class="log-type info">INFO</span>
                            <span>바이브 코딩 환경이 준비되었습니다.</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let ws = null;
            let connectionId = null;
            let messageCount = 0;
            let aiInteractions = 0;
            let codeExecutions = 0;
            let isConnected = false;

            // 상태 업데이트 함수
            function updateConnectionStatus(status) {
                const indicator = document.getElementById('statusIndicator');
                const connectBtn = document.getElementById('connectButton');
                const disconnectBtn = document.getElementById('disconnectButton');
                const roomInfo = document.getElementById('roomInfo');

                indicator.className = `status-indicator status-${status}`;
                
                if (status === 'connected') {
                    isConnected = true;
                    connectBtn.disabled = true;
                    disconnectBtn.disabled = false;
                    roomInfo.style.display = 'flex';
                    showNotification('연결되었습니다!', 'success');
                } else {
                    isConnected = false;
                    connectBtn.disabled = false;
                    disconnectBtn.disabled = true;
                    roomInfo.style.display = 'none';
                    if (status === 'disconnected') {
                        showNotification('연결이 해제되었습니다.', 'info');
                    }
                }
            }

            function updateStats() {
                document.getElementById('messageCount').textContent = messageCount;
                document.getElementById('aiInteractions').textContent = aiInteractions;
                document.getElementById('codeExecutions').textContent = codeExecutions;
            }

            function showNotification(message, type = 'info') {
                const notification = document.createElement('div');
                notification.className = `notification ${type}`;
                notification.textContent = message;
                document.body.appendChild(notification);

                setTimeout(() => {
                    notification.remove();
                }, 3000);
            }

            function addLogMessage(type, message) {
                const logMessages = document.getElementById('logMessages');
                const timestamp = new Date().toLocaleTimeString();
                const logMessage = document.createElement('div');
                logMessage.className = 'log-message';
                logMessage.innerHTML = `
                    <span class="log-timestamp">[${timestamp}]</span>
                    <span class="log-type ${type}">${type.toUpperCase()}</span>
                    <span>${message}</span>
                `;
                logMessages.appendChild(logMessage);
                logMessages.scrollTop = logMessages.scrollHeight;
            }

            function addAIMessage(content, type = 'ai') {
                const chatMessages = document.getElementById('aiChatMessages');
                const message = document.createElement('div');
                message.className = `message ${type}`;
                
                if (type === 'ai' && content.includes('```')) {
                    // 코드 블록이 포함된 경우 포맷팅
                    const parts = content.split('```');
                    let formattedContent = '';
                    for (let i = 0; i < parts.length; i++) {
                        if (i % 2 === 0) {
                            formattedContent += parts[i];
                        } else {
                            formattedContent += `<pre style="background: #2d3748; color: #e2e8f0; padding: 10px; border-radius: 5px; margin: 10px 0; overflow-x: auto;"><code>${parts[i]}</code></pre>`;
                        }
                    }
                    message.innerHTML = formattedContent;
                } else {
                    message.textContent = content;
                }
                
                chatMessages.appendChild(message);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function showLoading(message) {
                const chatMessages = document.getElementById('aiChatMessages');
                const loadingMessage = document.createElement('div');
                loadingMessage.className = 'message ai';
                loadingMessage.id = 'loadingMessage';
                loadingMessage.innerHTML = `
                    <div class="loading"></div>
                    ${message}
                `;
                chatMessages.appendChild(loadingMessage);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function hideLoading() {
                const loadingMessage = document.getElementById('loadingMessage');
                if (loadingMessage) {
                    loadingMessage.remove();
                }
            }

            // WebSocket 연결
            function connect() {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    return;
                }

                updateConnectionStatus('connecting');
                addLogMessage('info', 'WebSocket 연결 시도 중...');

                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/api/v1/ws/demo`;
                
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function(event) {
                    updateConnectionStatus('connected');
                    addLogMessage('success', 'WebSocket 연결 성공');
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    handleMessage(data);
                    messageCount++;
                    updateStats();
                };
                
                ws.onclose = function(event) {
                    updateConnectionStatus('disconnected');
                    addLogMessage('warning', 'WebSocket 연결 종료');
                };
                
                ws.onerror = function(error) {
                    updateConnectionStatus('disconnected');
                    addLogMessage('error', 'WebSocket 오류 발생');
                    showNotification('연결 오류가 발생했습니다.', 'error');
                };
            }

            function disconnect() {
                if (ws) {
                    ws.close();
                    ws = null;
                }
            }

            function joinRoom() {
                const roomId = document.getElementById('roomInput').value.trim();
                if (!roomId) {
                    showNotification('방 ID를 입력해주세요.', 'error');
                    return;
                }

                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'join_room',
                        room_id: roomId
                    }));
                    document.getElementById('roomBadge').textContent = roomId;
                    addLogMessage('info', `방 "${roomId}"에 참여 요청`);
                }
            }

            function leaveRoom() {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'leave_room'
                    }));
                    document.getElementById('roomBadge').textContent = '방 없음';
                    addLogMessage('info', '방에서 나가기 요청');
                }
            }

            function executeCode() {
                const code = document.getElementById('codeEditor').value;
                const executionMode = document.getElementById('executionMode').value;
                
                if (!code.trim()) {
                    showNotification('실행할 코드를 입력해주세요.', 'error');
                    return;
                }

                if (ws && ws.readyState === WebSocket.OPEN) {
                    const message = {
                        type: 'execute_code',
                        code: code,
                        language: 'python'
                    };
                    
                    // 실행 모드가 'auto'가 아닌 경우에만 추가
                    if (executionMode !== 'auto') {
                        message.execution_mode = executionMode;
                    }
                    
                    ws.send(JSON.stringify(message));
                    codeExecutions++;
                    updateStats();
                    addLogMessage('info', `코드 실행 요청 (${executionMode === 'auto' ? '자동' : executionMode} 모드)`);
                } else {
                    showNotification('먼저 연결해주세요.', 'error');
                }
            }

            function analyzeCode() {
                const code = document.getElementById('codeEditor').value;
                if (!code.trim()) {
                    showNotification('분석할 코드를 입력해주세요.', 'error');
                    return;
                }

                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'request_analysis',
                        file_path: 'main.py',
                        content: code
                    }));
                    addLogMessage('info', '기본 분석 요청');
                } else {
                    showNotification('먼저 연결해주세요.', 'error');
                }
            }

            function aiAnalyze() {
                const code = document.getElementById('codeEditor').value;
                if (!code.trim()) {
                    showNotification('분석할 코드를 입력해주세요.', 'error');
                    return;
                }

                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'ai_analysis',
                        file_path: 'main.py',
                        content: code
                    }));
                    aiInteractions++;
                    updateStats();
                    addLogMessage('info', 'AI 고급 분석 요청');
                    showLoading('AI가 코드를 분석하고 있습니다...');
                } else {
                    showNotification('먼저 연결해주세요.', 'error');
                }
            }

            function getAISuggestions() {
                const code = document.getElementById('codeEditor').value;
                if (!code.trim()) {
                    showNotification('제안을 받을 코드를 입력해주세요.', 'error');
                    return;
                }

                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'request_ai_suggestions',
                        file_path: 'main.py',
                        content: code,
                        position: {line: 0, column: 0}
                    }));
                    aiInteractions++;
                    updateStats();
                    addLogMessage('info', 'AI 제안 요청');
                    showLoading('AI가 코드 제안을 생성하고 있습니다...');
                } else {
                    showNotification('먼저 연결해주세요.', 'error');
                }
            }

            // 파일 작업 함수들
            function saveCode() {
                const code = document.getElementById('codeEditor').value;
                const filename = prompt('저장할 파일명을 입력하세요:', 'my_code.py');
                
                if (filename) {
                    const blob = new Blob([code], { type: 'text/plain' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                    
                    showNotification(`파일 "${filename}"이 저장되었습니다.`, 'success');
                    addLogMessage('info', `코드 저장: ${filename}`);
                }
            }

            function loadCode() {
                const input = document.createElement('input');
                input.type = 'file';
                input.accept = '.py,.js,.java,.txt,.md';
                
                input.onchange = function(event) {
                    const file = event.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            document.getElementById('codeEditor').value = e.target.result;
                            showNotification(`파일 "${file.name}"이 로드되었습니다.`, 'success');
                            addLogMessage('info', `코드 로드: ${file.name}`);
                        };
                        reader.readAsText(file);
                    }
                };
                
                input.click();
            }

            function clearCode() {
                if (confirm('코드 에디터를 지우시겠습니까?')) {
                    document.getElementById('codeEditor').value = '';
                    showNotification('코드 에디터가 지워졌습니다.', 'info');
                    addLogMessage('info', '코드 에디터 지우기');
                }
            }

            function sendAIMessage() {
                const messageInput = document.getElementById('aiMessageInput');
                const message = messageInput.value.trim();
                const code = document.getElementById('codeEditor').value;

                if (!message) {
                    showNotification('메시지를 입력해주세요.', 'error');
                    return;
                }

                if (ws && ws.readyState === WebSocket.OPEN) {
                    // 사용자 메시지 표시
                    addAIMessage(message, 'user');
                    
                    ws.send(JSON.stringify({
                        type: 'ai_conversation',
                        message: message,
                        current_code: code,
                        file_path: 'main.py',
                        context: {}
                    }));
                    
                    aiInteractions++;
                    updateStats();
                    messageInput.value = '';
                    addLogMessage('info', `AI에게 질문: "${message.substring(0, 30)}..."`);
                    showLoading('AI가 답변을 준비하고 있습니다...');
                } else {
                    showNotification('먼저 연결해주세요.', 'error');
                }
            }

            function handleMessage(data) {
                addLogMessage('info', `메시지 수신: ${data.type}`);

                switch(data.type) {
                    case 'connection_established':
                        connectionId = data.connection_id;
                        addAIMessage(`연결이 완료되었습니다. (ID: ${data.connection_id.substring(0, 8)}...)`, 'system');
                        break;

                    case 'pong':
                        addLogMessage('success', '핑-퐁 응답 수신');
                        break;

                    case 'joined_room':
                        addAIMessage(`방 "${data.room_id}"에 참여했습니다.`, 'system');
                        break;

                    case 'left_room':
                        addAIMessage(`방에서 나갔습니다.`, 'system');
                        break;

                    case 'execution_result':
                        hideLoading();
                        const result = data.result;
                        if (result.success) {
                            addAIMessage(`✅ 실행 성공\\n\\n출력:\\n${result.output}`, 'success');
                            addLogMessage('success', '코드 실행 성공');
                        } else {
                            addAIMessage(`❌ 실행 실패\\n\\n오류: ${result.error}`, 'error');
                            addLogMessage('error', `코드 실행 실패: ${result.error}`);
                        }
                        break;

                    case 'execution_error':
                        hideLoading();
                        addAIMessage(`❌ 실행 오류: ${data.error}`, 'error');
                        addLogMessage('error', `실행 오류: ${data.error}`);
                        break;

                    case 'analysis_result':
                        hideLoading();
                        const analysis = data.analysis;
                        if (analysis.success) {
                            const metrics = analysis.metrics || {};
                            const issues = analysis.issues || [];
                            let analysisText = `📊 코드 분석 결과\\n\\n`;
                            analysisText += `📏 라인 수: ${metrics.lines_of_code || 0}\\n`;
                            analysisText += `🔧 함수 수: ${metrics.functions || 0}\\n`;
                            analysisText += `📦 클래스 수: ${metrics.classes || 0}\\n`;
                            analysisText += `⚡ 복잡도: ${metrics.complexity || 0}\\n`;
                            analysisText += `⭐ 품질 점수: ${analysis.quality_score || 0}/100\\n\\n`;
                            
                            if (issues.length > 0) {
                                analysisText += `⚠️ 발견된 이슈:\\n`;
                                issues.slice(0, 3).forEach(issue => {
                                    analysisText += `• ${issue.message}\\n`;
                                });
                            } else {
                                analysisText += `✅ 특별한 이슈가 발견되지 않았습니다.`;
                            }
                            
                            addAIMessage(analysisText, 'success');
                            addLogMessage('success', '코드 분석 완료');
                        } else {
                            addAIMessage(`❌ 분석 실패: ${analysis.error}`, 'error');
                            addLogMessage('error', `분석 실패: ${analysis.error}`);
                        }
                        break;

                    case 'ai_analysis_started':
                        addLogMessage('info', 'AI 분석 시작');
                        break;

                    case 'ai_analysis_result':
                        hideLoading();
                        const aiAnalysis = data.analysis;
                        if (aiAnalysis.success) {
                            const aiData = aiAnalysis.ai_analysis || {};
                            let aiText = `🧠 AI 고급 분석 결과\\n\\n`;
                            
                            if (aiData.quality_assessment) {
                                aiText += `📋 품질 평가:\\n${aiData.quality_assessment}\\n\\n`;
                            }
                            
                            const performanceIssues = aiData.performance_issues || [];
                            if (performanceIssues.length > 0) {
                                aiText += `⚡ 성능 이슈:\\n`;
                                performanceIssues.slice(0, 3).forEach(issue => {
                                    aiText += `• ${issue}\\n`;
                                });
                                aiText += `\\n`;
                            }
                            
                            const suggestions = aiAnalysis.suggestions || [];
                            if (suggestions.length > 0) {
                                aiText += `💡 개선 제안:\\n`;
                                suggestions.slice(0, 2).forEach(suggestion => {
                                    aiText += `• ${suggestion.title}: ${suggestion.description}\\n`;
                                });
                            }
                            
                            addAIMessage(aiText, 'success');
                            addLogMessage('success', 'AI 분석 완료');
                        } else {
                            addAIMessage(`❌ AI 분석 실패: ${aiAnalysis.error}`, 'error');
                            addLogMessage('error', `AI 분석 실패: ${aiAnalysis.error}`);
                        }
                        break;

                    case 'ai_conversation_started':
                        addLogMessage('info', 'AI 대화 시작');
                        break;

                    case 'ai_conversation_result':
                        hideLoading();
                        const conversation = data.conversation;
                        if (conversation.success) {
                            const response = conversation.response;
                            let responseText = response.content || '응답을 생성했습니다.';
                            
                            if (response.generated_code) {
                                responseText += `\\n\\n생성된 코드:\\n\\`\\`\\`python\\n${response.generated_code}\\n\\`\\`\\``;
                            }
                            
                            if (response.suggestions && response.suggestions.length > 0) {
                                responseText += `\\n\\n💡 추가 제안:\\n`;
                                response.suggestions.forEach(suggestion => {
                                    responseText += `• ${suggestion}\\n`;
                                });
                            }
                            
                            addAIMessage(responseText, 'ai');
                            addLogMessage('success', 'AI 대화 응답 수신');
                        } else {
                            addAIMessage(`❌ AI 응답 오류: ${conversation.error}`, 'error');
                            addLogMessage('error', `AI 응답 오류: ${conversation.error}`);
                        }
                        break;

                    case 'ai_suggestions_result':
                        hideLoading();
                        const suggestions = data.suggestions || [];
                        if (suggestions.length > 0) {
                            let suggestionText = `💡 AI 제안 (${suggestions.length}개):\\n\\n`;
                            suggestions.forEach((suggestion, index) => {
                                suggestionText += `${index + 1}. ${suggestion.type}: ${suggestion.text}\\n`;
                            });
                            addAIMessage(suggestionText, 'success');
                            addLogMessage('success', `AI 제안 ${suggestions.length}개 수신`);
                        } else {
                            addAIMessage('제안할 수 있는 내용이 없습니다.', 'system');
                            addLogMessage('warning', 'AI 제안 없음');
                        }
                        break;

                    case 'error':
                        hideLoading();
                        addAIMessage(`❌ 오류: ${data.message}`, 'error');
                        addLogMessage('error', `오류: ${data.message}`);
                        break;

                    default:
                        addLogMessage('warning', `알 수 없는 메시지 타입: ${data.type}`);
                }
            }

            // 키보드 단축키
            document.addEventListener('keydown', function(e) {
                if (e.ctrlKey || e.metaKey) {
                    switch(e.key) {
                        case 'Enter':
                            e.preventDefault();
                            executeCode();
                            break;
                        case 's':
                            e.preventDefault();
                            aiAnalyze();
                            break;
                        case 'd':
                            e.preventDefault();
                            sendAIMessage();
                            break;
                    }
                }
            });

            // Enter 키로 AI 메시지 전송
            document.getElementById('aiMessageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendAIMessage();
                }
            });

            // 자동 연결
            window.onload = function() {
                connect();
                addLogMessage('info', '페이지 로드 완료');
            };

            // 페이지 종료 시 연결 해제
            window.onbeforeunload = function() {
                if (ws) {
                    ws.close();
                }
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
