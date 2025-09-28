"""
UI 개선사항 및 접근성 기능
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/demo/advanced")
async def advanced_demo():
    """고급 기능이 포함된 데모 페이지"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🚀 Agentic AI 바이브 코딩 - 고급 모드</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                min-height: 100vh;
                color: #333;
            }

            .container {
                max-width: 1600px;
                margin: 0 auto;
                padding: 20px;
            }

            .header {
                text-align: center;
                margin-bottom: 30px;
                color: white;
            }

            .header h1 {
                font-size: 3rem;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }

            .header p {
                font-size: 1.2rem;
                opacity: 0.9;
            }

            .toolbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                padding: 15px 25px;
                border-radius: 15px;
                margin-bottom: 20px;
                color: white;
            }

            .toolbar-left, .toolbar-right {
                display: flex;
                gap: 15px;
                align-items: center;
            }

            .main-layout {
                display: grid;
                grid-template-columns: 300px 1fr 350px;
                grid-template-rows: auto 1fr;
                gap: 20px;
                height: calc(100vh - 200px);
            }

            .sidebar {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                overflow-y: auto;
            }

            .main-content {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }

            .right-panel {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                overflow-y: auto;
            }

            .code-editor-container {
                flex: 1;
                display: flex;
                flex-direction: column;
                margin-bottom: 20px;
            }

            .editor-toolbar {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
                flex-wrap: wrap;
            }

            .code-editor {
                flex: 1;
                font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
                font-size: 14px;
                line-height: 1.6;
                padding: 20px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background: #f8f9fa;
                resize: none;
                outline: none;
                transition: border-color 0.3s ease;
            }

            .code-editor:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }

            .editor-actions {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 10px;
                margin-top: 15px;
            }

            .btn {
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                position: relative;
                overflow: hidden;
            }

            .btn::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }

            .btn:hover::before {
                left: 100%;
            }

            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }

            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }

            .btn-success {
                background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                color: white;
            }

            .btn-success:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(72, 187, 120, 0.4);
            }

            .btn-warning {
                background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
                color: white;
            }

            .btn-warning:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(237, 137, 54, 0.4);
            }

            .btn-info {
                background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                color: white;
            }

            .btn-info:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(66, 153, 225, 0.4);
            }

            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }

            .status-connected { background-color: #48bb78; }
            .status-disconnected { background-color: #f56565; }
            .status-connecting { background-color: #ed8936; }

            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }

            .chat-container {
                height: 100%;
                display: flex;
                flex-direction: column;
            }

            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 15px;
                background: #f8f9fa;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                margin-bottom: 15px;
                max-height: 400px;
            }

            .chat-input-container {
                display: flex;
                gap: 10px;
                align-items: center;
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
                word-wrap: break-word;
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

            .file-tree {
                margin-bottom: 20px;
            }

            .file-item {
                padding: 8px 12px;
                cursor: pointer;
                border-radius: 6px;
                transition: background-color 0.2s;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .file-item:hover {
                background: #f0f0f0;
            }

            .file-item.active {
                background: #667eea;
                color: white;
            }

            .shortcuts-panel {
                margin-bottom: 20px;
            }

            .shortcut-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px 0;
                border-bottom: 1px solid #e2e8f0;
            }

            .shortcut-key {
                background: #e2e8f0;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-family: monospace;
            }

            .stats-panel {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-bottom: 20px;
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

            .notification.success { background: #48bb78; }
            .notification.error { background: #f56565; }
            .notification.info { background: #4299e1; }

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

            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.5);
                backdrop-filter: blur(5px);
            }

            .modal-content {
                background-color: white;
                margin: 5% auto;
                padding: 30px;
                border-radius: 15px;
                width: 80%;
                max-width: 600px;
                animation: modalSlideIn 0.3s ease;
            }

            @keyframes modalSlideIn {
                from {
                    opacity: 0;
                    transform: translateY(-50px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .close {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
            }

            .close:hover {
                color: #000;
            }

            .theme-toggle {
                background: none;
                border: none;
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
                transition: transform 0.3s ease;
            }

            .theme-toggle:hover {
                transform: rotate(180deg);
            }

            .dark-theme {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                color: #e2e8f0;
            }

            .dark-theme .card {
                background: #2d3748;
                color: #e2e8f0;
            }

            .dark-theme .code-editor {
                background: #1a202c;
                color: #e2e8f0;
                border-color: #4a5568;
            }

            .dark-theme .chat-messages {
                background: #1a202c;
                border-color: #4a5568;
            }

            /* 반응형 디자인 */
            @media (max-width: 1200px) {
                .main-layout {
                    grid-template-columns: 1fr;
                    grid-template-rows: auto auto 1fr;
                }
                
                .sidebar, .right-panel {
                    order: 3;
                }
            }

            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2rem;
                }
                
                .toolbar {
                    flex-direction: column;
                    gap: 10px;
                }
                
                .editor-actions {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Agentic AI 바이브 코딩</h1>
                <p>고급 기능과 함께하는 지능형 협업 코딩 환경</p>
            </div>

            <div class="toolbar">
                <div class="toolbar-left">
                    <div class="status-indicator status-connecting" id="statusIndicator"></div>
                    <span id="connectionStatus">연결 중...</span>
                    <button class="btn btn-primary" id="connectButton" onclick="connect()">연결</button>
                    <button class="btn btn-warning" id="disconnectButton" onclick="disconnect()" disabled>해제</button>
                </div>
                <div class="toolbar-right">
                    <button class="theme-toggle" onclick="toggleTheme()" title="다크 모드 토글">🌙</button>
                    <button class="btn btn-info" onclick="showShortcuts()">단축키</button>
                    <button class="btn btn-success" onclick="showSettings()">설정</button>
                </div>
            </div>

            <div class="main-layout">
                <!-- 왼쪽 사이드바 -->
                <div class="sidebar">
                    <h3>📁 프로젝트 파일</h3>
                    <div class="file-tree" id="fileTree">
                        <div class="file-item active" data-file="main.py">
                            <span>📄</span>
                            <span>main.py</span>
                        </div>
                        <div class="file-item" data-file="utils.py">
                            <span>📄</span>
                            <span>utils.py</span>
                        </div>
                        <div class="file-item" data-file="config.py">
                            <span>📄</span>
                            <span>config.py</span>
                        </div>
                    </div>

                    <h3>⌨️ 키보드 단축키</h3>
                    <div class="shortcuts-panel" id="shortcutsPanel">
                        <div class="shortcut-item">
                            <span>코드 실행</span>
                            <span class="shortcut-key">Ctrl+Enter</span>
                        </div>
                        <div class="shortcut-item">
                            <span>AI 분석</span>
                            <span class="shortcut-key">Ctrl+S</span>
                        </div>
                        <div class="shortcut-item">
                            <span>AI 질문</span>
                            <span class="shortcut-key">Ctrl+D</span>
                        </div>
                        <div class="shortcut-item">
                            <span>테마 변경</span>
                            <span class="shortcut-key">Ctrl+T</span>
                        </div>
                    </div>

                    <h3>📊 통계</h3>
                    <div class="stats-panel">
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
                        <div class="stat-card">
                            <div class="stat-number" id="linesOfCode">0</div>
                            <div class="stat-label">코드 라인</div>
                        </div>
                    </div>
                </div>

                <!-- 메인 콘텐츠 -->
                <div class="main-content">
                    <div class="code-editor-container">
                        <div class="editor-toolbar">
                            <select id="languageSelect" class="btn">
                                <option value="python">Python</option>
                                <option value="javascript">JavaScript</option>
                                <option value="java">Java</option>
                            </select>
                            <button class="btn btn-primary" onclick="saveCode()">💾 저장</button>
                            <button class="btn btn-info" onclick="loadCode()">📁 열기</button>
                            <button class="btn btn-warning" onclick="clearCode()">🗑️ 지우기</button>
                        </div>
                        
                        <textarea id="codeEditor" class="code-editor" placeholder="여기에 코드를 입력하세요...">def fibonacci(n):
    \"\"\"
    Fibonacci sequence calculation function
    Recursive implementation (inefficient)
    \"\"\"
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_optimized(n):
    \"\"\"
    Optimized Fibonacci function
    Using memoization
    \"\"\"
    memo = {}
    
    def fib(n):
        if n in memo:
            return memo[n]
        if n <= 1:
            memo[n] = n
        else:
            memo[n] = fib(n-1) + fib(n-2)
        return memo[n]
    
    return fib(n)

def fibonacci_iterative(n):
    \"\"\"
    Iterative implementation (most efficient)
    \"\"\"
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b

# Test
if __name__ == \"__main__\":
    import time
    
    n = 35
    
    print(\"=== Fibonacci Performance Comparison ===\")
    
    # Iterative implementation (fastest)
    start = time.time()
    result1 = fibonacci_iterative(n)
    time1 = time.time() - start
    print(f\"Iterative Fibonacci({n}) = {result1} (time: {time1:.4f}s)\")
    
    # Optimized recursive implementation
    start = time.time()
    result2 = fibonacci_optimized(n)
    time2 = time.time() - start
    print(f\"Optimized Fibonacci({n}) = {result2} (time: {time2:.4f}s)\")
    
    # Basic recursive implementation (slow)
    if n <= 25:  # Too slow, test only small values
        start = time.time()
        result3 = fibonacci(n)
        time3 = time.time() - start
        print(f\"Basic Fibonacci({n}) = {result3} (time: {time3:.4f}s)\")
    else:
        print(f\"Basic Fibonacci({n}) = Too slow, skipped\")
    
    print(f\"\\nPerformance comparison:\")
    print(f\"- Iterative is {time2/time1:.1f}x faster (vs optimized recursive)\")
    if n <= 25:
        print(f\"- Iterative is {time3/time1:.1f}x faster (vs basic recursive)\")</textarea>
                        
                        <div class="editor-actions">
                            <button class="btn btn-primary" onclick="executeCode()">
                                ▶️ 실행
                            </button>
                            <button class="btn btn-success" onclick="analyzeCode()">
                                🔍 분석
                            </button>
                            <button class="btn btn-warning" onclick="aiAnalyze()">
                                🧠 AI 분석
                            </button>
                            <button class="btn btn-info" onclick="getAISuggestions()">
                                💡 AI 제안
                            </button>
                            <button class="btn btn-primary" onclick="formatCode()">
                                ✨ 포맷팅
                            </button>
                            <button class="btn btn-success" onclick="optimizeCode()">
                                ⚡ 최적화
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 오른쪽 패널 -->
                <div class="right-panel">
                    <h3>🤖 AI 어시스턴트</h3>
                    <div class="chat-container">
                        <div class="chat-messages" id="chatMessages">
                            <div class="message ai">
                                안녕하세요! 저는 고급 AI 코딩 어시스턴트입니다.\\n\\n다음과 같은 도움을 드릴 수 있습니다:\\n• 코드 최적화 및 리팩토링\\n• 버그 찾기 및 디버깅\\n• 성능 분석 및 개선\\n• 코드 설명 및 문서화\\n• 새로운 기능 구현\\n\\n무엇을 도와드릴까요?
                            </div>
                        </div>
                        <div class="chat-input-container">
                            <input type="text" id="chatInput" class="chat-input" 
                                   placeholder="AI에게 질문하세요... (예: 이 코드를 최적화해주세요)">
                            <button class="btn btn-primary" onclick="sendMessage()">
                                전송
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 단축키 모달 -->
        <div id="shortcutsModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('shortcutsModal')">&times;</span>
                <h2>⌨️ 키보드 단축키</h2>
                <div style="margin-top: 20px;">
                    <div class="shortcut-item">
                        <span>코드 실행</span>
                        <span class="shortcut-key">Ctrl + Enter</span>
                    </div>
                    <div class="shortcut-item">
                        <span>AI 분석</span>
                        <span class="shortcut-key">Ctrl + S</span>
                    </div>
                    <div class="shortcut-item">
                        <span>AI 질문 전송</span>
                        <span class="shortcut-key">Ctrl + D</span>
                    </div>
                    <div class="shortcut-item">
                        <span>테마 변경</span>
                        <span class="shortcut-key">Ctrl + T</span>
                    </div>
                    <div class="shortcut-item">
                        <span>코드 포맷팅</span>
                        <span class="shortcut-key">Ctrl + Shift + F</span>
                    </div>
                    <div class="shortcut-item">
                        <span>코드 최적화</span>
                        <span class="shortcut-key">Ctrl + Shift + O</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 설정 모달 -->
        <div id="settingsModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal('settingsModal')">&times;</span>
                <h2>⚙️ 설정</h2>
                <div style="margin-top: 20px;">
                    <div style="margin-bottom: 15px;">
                        <label>AI 응답 속도:</label>
                        <select id="aiSpeed">
                            <option value="fast">빠름</option>
                            <option value="normal" selected>보통</option>
                            <option value="detailed">상세</option>
                        </select>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <label>코드 테마:</label>
                        <select id="codeTheme">
                            <option value="light">라이트</option>
                            <option value="dark">다크</option>
                            <option value="auto">자동</option>
                        </select>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <label>알림 설정:</label>
                        <input type="checkbox" id="notifications" checked> 알림 표시
                    </div>
                    <button class="btn btn-primary" onclick="saveSettings()">설정 저장</button>
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
            let isDarkTheme = false;

            // 상태 업데이트
            function updateConnectionStatus(status) {
                const indicator = document.getElementById('statusIndicator');
                const statusText = document.getElementById('connectionStatus');
                const connectBtn = document.getElementById('connectButton');
                const disconnectBtn = document.getElementById('disconnectButton');

                indicator.className = `status-indicator status-${status}`;
                
                switch(status) {
                    case 'connected':
                        statusText.textContent = '연결됨';
                        connectBtn.disabled = true;
                        disconnectBtn.disabled = false;
                        isConnected = true;
                        showNotification('연결되었습니다!', 'success');
                        break;
                    case 'connecting':
                        statusText.textContent = '연결 중...';
                        connectBtn.disabled = true;
                        disconnectBtn.disabled = true;
                        break;
                    case 'disconnected':
                        statusText.textContent = '연결 해제됨';
                        connectBtn.disabled = false;
                        disconnectBtn.disabled = true;
                        isConnected = false;
                        showNotification('연결이 해제되었습니다.', 'info');
                        break;
                }
            }

            function updateStats() {
                const code = document.getElementById('codeEditor').value;
                const linesOfCode = code.split('\\n').length;
                
                document.getElementById('messageCount').textContent = messageCount;
                document.getElementById('aiInteractions').textContent = aiInteractions;
                document.getElementById('codeExecutions').textContent = codeExecutions;
                document.getElementById('linesOfCode').textContent = linesOfCode;
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

            function addMessage(content, type = 'ai') {
                const chatMessages = document.getElementById('chatMessages');
                const message = document.createElement('div');
                message.className = `message ${type}`;
                
                if (type === 'ai' && content.includes('```')) {
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
                const chatMessages = document.getElementById('chatMessages');
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

                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/api/v1/ws/demo`;
                
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function(event) {
                    updateConnectionStatus('connected');
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    handleMessage(data);
                    messageCount++;
                    updateStats();
                };
                
                ws.onclose = function(event) {
                    updateConnectionStatus('disconnected');
                };
                
                ws.onerror = function(error) {
                    updateConnectionStatus('disconnected');
                    showNotification('연결 오류가 발생했습니다.', 'error');
                };
            }

            function disconnect() {
                if (ws) {
                    ws.close();
                    ws = null;
                }
            }

            function executeCode() {
                const code = document.getElementById('codeEditor').value;
                if (!code.trim()) {
                    showNotification('실행할 코드를 입력해주세요.', 'error');
                    return;
                }

                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'execute_code',
                        code: code,
                        language: document.getElementById('languageSelect').value
                    }));
                    codeExecutions++;
                    updateStats();
                    showNotification('코드 실행 중...', 'info');
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
                    addMessage('코드 분석을 시작합니다...', 'system');
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
                    showLoading('AI가 코드 제안을 생성하고 있습니다...');
                } else {
                    showNotification('먼저 연결해주세요.', 'error');
                }
            }

            function formatCode() {
                const code = document.getElementById('codeEditor').value;
                if (!code.trim()) {
                    showNotification('포맷팅할 코드를 입력해주세요.', 'error');
                    return;
                }

                // 간단한 포맷팅 (실제로는 더 정교한 포맷터 사용)
                const formatted = code
                    .split('\\n')
                    .map(line => line.trim())
                    .filter(line => line.length > 0)
                    .join('\\n');
                
                document.getElementById('codeEditor').value = formatted;
                showNotification('코드가 포맷팅되었습니다.', 'success');
            }

            function optimizeCode() {
                const code = document.getElementById('codeEditor').value;
                if (!code.trim()) {
                    showNotification('최적화할 코드를 입력해주세요.', 'error');
                    return;
                }

                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'ai_conversation',
                        message: '이 코드를 최적화해주세요. 성능을 개선하고 더 효율적으로 만들어주세요.',
                        current_code: code,
                        file_path: 'main.py',
                        context: {}
                    }));
                    aiInteractions++;
                    updateStats();
                    showLoading('AI가 코드를 최적화하고 있습니다...');
                } else {
                    showNotification('먼저 연결해주세요.', 'error');
                }
            }

            function sendMessage() {
                const chatInput = document.getElementById('chatInput');
                const message = chatInput.value.trim();
                const code = document.getElementById('codeEditor').value;

                if (!message) {
                    showNotification('메시지를 입력해주세요.', 'error');
                    return;
                }

                if (ws && ws.readyState === WebSocket.OPEN) {
                    addMessage(message, 'user');
                    
                    ws.send(JSON.stringify({
                        type: 'ai_conversation',
                        message: message,
                        current_code: code,
                        file_path: 'main.py',
                        context: {}
                    }));
                    
                    aiInteractions++;
                    updateStats();
                    chatInput.value = '';
                    showLoading('AI가 답변을 준비하고 있습니다...');
                } else {
                    showNotification('먼저 연결해주세요.', 'error');
                }
            }

            function handleMessage(data) {
                switch(data.type) {
                    case 'connection_established':
                        connectionId = data.connection_id;
                        addMessage(`연결이 완료되었습니다. (ID: ${data.connection_id.substring(0, 8)}...)`, 'system');
                        break;

                    case 'execution_result':
                        hideLoading();
                        const result = data.result;
                        if (result.success) {
                            addMessage(`✅ 실행 성공\\n\\n출력:\\n${result.output}`, 'success');
                        } else {
                            addMessage(`❌ 실행 실패\\n\\n오류: ${result.error}`, 'error');
                        }
                        break;

                    case 'analysis_result':
                        hideLoading();
                        const analysis = data.analysis;
                        if (analysis.success) {
                            const metrics = analysis.metrics || {};
                            let analysisText = `📊 코드 분석 결과\\n\\n`;
                            analysisText += `📏 라인 수: ${metrics.lines_of_code || 0}\\n`;
                            analysisText += `🔧 함수 수: ${metrics.functions || 0}\\n`;
                            analysisText += `📦 클래스 수: ${metrics.classes || 0}\\n`;
                            analysisText += `⚡ 복잡도: ${metrics.complexity || 0}\\n`;
                            analysisText += `⭐ 품질 점수: ${analysis.quality_score || 0}/100`;
                            
                            addMessage(analysisText, 'success');
                        } else {
                            addMessage(`❌ 분석 실패: ${analysis.error}`, 'error');
                        }
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
                            
                            addMessage(responseText, 'ai');
                        } else {
                            addMessage(`❌ AI 응답 오류: ${conversation.error}`, 'error');
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
                            addMessage(suggestionText, 'success');
                        } else {
                            addMessage('제안할 수 있는 내용이 없습니다.', 'system');
                        }
                        break;
                }
            }

            // 파일 트리 기능
            function setupFileTree() {
                const fileItems = document.querySelectorAll('.file-item');
                fileItems.forEach(item => {
                    item.addEventListener('click', function() {
                        fileItems.forEach(i => i.classList.remove('active'));
                        this.classList.add('active');
                        
                        const fileName = this.dataset.file;
                        // 실제로는 파일 내용을 로드
                        showNotification(`${fileName} 선택됨`, 'info');
                    });
                });
            }

            // 모달 기능
            function showShortcuts() {
                document.getElementById('shortcutsModal').style.display = 'block';
            }

            function showSettings() {
                document.getElementById('settingsModal').style.display = 'block';
            }

            function closeModal(modalId) {
                document.getElementById(modalId).style.display = 'none';
            }

            function saveSettings() {
                const aiSpeed = document.getElementById('aiSpeed').value;
                const codeTheme = document.getElementById('codeTheme').value;
                const notifications = document.getElementById('notifications').checked;
                
                localStorage.setItem('aiSpeed', aiSpeed);
                localStorage.setItem('codeTheme', codeTheme);
                localStorage.setItem('notifications', notifications);
                
                showNotification('설정이 저장되었습니다.', 'success');
                closeModal('settingsModal');
            }

            function loadSettings() {
                const aiSpeed = localStorage.getItem('aiSpeed') || 'normal';
                const codeTheme = localStorage.getItem('codeTheme') || 'light';
                const notifications = localStorage.getItem('notifications') !== 'false';
                
                document.getElementById('aiSpeed').value = aiSpeed;
                document.getElementById('codeTheme').value = codeTheme;
                document.getElementById('notifications').checked = notifications;
                
                if (codeTheme === 'dark') {
                    toggleTheme();
                }
            }

            function toggleTheme() {
                isDarkTheme = !isDarkTheme;
                document.body.classList.toggle('dark-theme', isDarkTheme);
                localStorage.setItem('darkTheme', isDarkTheme);
                
                const themeToggle = document.querySelector('.theme-toggle');
                themeToggle.textContent = isDarkTheme ? '☀️' : '🌙';
            }

            function saveCode() {
                const code = document.getElementById('codeEditor').value;
                const filename = prompt('저장할 파일명을 입력하세요:', 'my_code.py');
                
                if (filename) {
                    // 로컬 스토리지에도 저장
                    localStorage.setItem('savedCode', code);
                    localStorage.setItem('lastFilename', filename);
                    
                    // 파일 다운로드
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

            function autoSaveCode() {
                // 자동 저장: 팝업 없이 로컬 스토리지만 저장
                const code = document.getElementById('codeEditor').value;
                if (code.trim()) {
                    localStorage.setItem('savedCode', code);
                    const lastFilename = localStorage.getItem('lastFilename') || 'auto_saved_code.py';
                    localStorage.setItem('lastFilename', lastFilename);
                    
                    // 조용히 저장 (알림 없음)
                    console.log('자동 저장 완료:', lastFilename);
                }
            }

            function loadCode() {
                // 먼저 로컬 스토리지에서 확인
                const savedCode = localStorage.getItem('savedCode');
                const lastFilename = localStorage.getItem('lastFilename');
                
                if (savedCode && confirm(`저장된 코드 "${lastFilename || 'unnamed'}"를 불러오시겠습니까?`)) {
                    document.getElementById('codeEditor').value = savedCode;
                    showNotification('저장된 코드를 불러왔습니다.', 'success');
                    return;
                }
                
                // 파일 시스템에서 파일 선택
                const input = document.createElement('input');
                input.type = 'file';
                input.accept = '.py,.js,.java,.txt,.md,.json';
                
                input.onchange = function(event) {
                    const file = event.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            document.getElementById('codeEditor').value = e.target.result;
                            localStorage.setItem('savedCode', e.target.result);
                            localStorage.setItem('lastFilename', file.name);
                            showNotification(`파일 "${file.name}"이 로드되었습니다.`, 'success');
                            addLogMessage('info', `코드 로드: ${file.name}`);
                        };
                        reader.readAsText(file);
                    }
                };
                
                input.click();
            }

            function clearCode() {
                if (confirm('코드를 모두 지우시겠습니까?')) {
                    document.getElementById('codeEditor').value = '';
                    localStorage.removeItem('savedCode');
                    localStorage.removeItem('lastFilename');
                    showNotification('코드가 지워졌습니다.', 'info');
                    addLogMessage('info', '코드 에디터 지우기');
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
                            sendMessage();
                            break;
                        case 't':
                            e.preventDefault();
                            toggleTheme();
                            break;
                        case 'Shift':
                            if (e.key === 'F') {
                                e.preventDefault();
                                formatCode();
                            } else if (e.key === 'O') {
                                e.preventDefault();
                                optimizeCode();
                            }
                            break;
                    }
                }
            });

            // Enter 키로 메시지 전송
            document.getElementById('chatInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // 코드 에디터 변경 감지
            document.getElementById('codeEditor').addEventListener('input', function() {
                updateStats();
            });

            // 초기화
            window.onload = function() {
                connect();
                setupFileTree();
                loadSettings();
                updateStats();
                
                // 자동 저장 (팝업 없이 로컬 스토리지만)
                setInterval(autoSaveCode, 30000); // 30초마다 자동 저장
            };

            // 페이지 종료 시 연결 해제
            window.onbeforeunload = function() {
                if (ws) {
                    ws.close();
                }
            };

            // 모달 외부 클릭 시 닫기
            window.onclick = function(event) {
                const shortcutsModal = document.getElementById('shortcutsModal');
                const settingsModal = document.getElementById('settingsModal');
                
                if (event.target === shortcutsModal) {
                    shortcutsModal.style.display = 'none';
                }
                if (event.target === settingsModal) {
                    settingsModal.style.display = 'none';
                }
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
