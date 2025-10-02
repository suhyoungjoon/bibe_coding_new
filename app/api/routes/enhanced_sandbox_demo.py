"""
향상된 샌드박스 데모 페이지
다중 언어 지원, 실시간 실행 상태, 결과 시각화
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/test/simple")
async def simple_test():
    """간단한 JavaScript 테스트 페이지"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>간단한 테스트</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f0f0f0;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            button {
                padding: 10px 20px;
                margin: 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            .btn-primary {
                background-color: #007bff;
                color: white;
            }
            .btn-secondary {
                background-color: #6c757d;
                color: white;
            }
            .btn-success {
                background-color: #28a745;
                color: white;
            }
            #result {
                margin-top: 20px;
                padding: 15px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                min-height: 100px;
                font-family: monospace;
                white-space: pre-wrap;
            }
            textarea {
                width: 100%;
                height: 200px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-family: monospace;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧪 JavaScript 테스트 페이지</h1>
            <p>이 페이지는 JavaScript가 정상 작동하는지 테스트합니다.</p>
            
            <div>
                <h3>코드 에디터</h3>
                <textarea id="codeEditor" placeholder="코드를 입력하세요...">print("Hello World!")</textarea>
            </div>
            
            <div>
                <h3>테스트 버튼들</h3>
                <button id="executeBtn" class="btn-primary" onclick="testExecute()">▶️ 실행</button>
                <button id="clearBtn" class="btn-secondary" onclick="testClear()">🗑️ 지우기</button>
                <button id="testBtn" class="btn-success" onclick="testAlert()">🔔 알림 테스트</button>
            </div>
            
            <div>
                <h3>결과</h3>
                <div id="result">결과가 여기에 표시됩니다...</div>
            </div>
        </div>

        <script>
            console.log('=== JavaScript 시작 ===');
            console.log('페이지 로드 완료');
            
            // DOM 요소 확인
            const codeEditor = document.getElementById('codeEditor');
            const executeBtn = document.getElementById('executeBtn');
            const clearBtn = document.getElementById('clearBtn');
            const testBtn = document.getElementById('testBtn');
            const resultDiv = document.getElementById('result');
            
            console.log('DOM 요소들:');
            console.log('- codeEditor:', codeEditor);
            console.log('- executeBtn:', executeBtn);
            console.log('- clearBtn:', clearBtn);
            console.log('- testBtn:', testBtn);
            console.log('- resultDiv:', resultDiv);
            
            // 테스트 함수들
            function testExecute() {
                console.log('testExecute 함수 호출됨!');
                const code = codeEditor.value;
                console.log('실행할 코드:', code);
                
                resultDiv.textContent = `실행 결과:\\n${code}\\n\\n실행 시간: ${new Date().toLocaleTimeString()}`;
                
                // API 호출 테스트
                fetch('/api/v1/sandbox/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code: code,
                        language: 'python',
                        security_level: 'LOW',
                        user_id: 'test_user'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('API 응답:', data);
                    if (data.success) {
                        resultDiv.textContent = `✅ 실행 성공!\\n\\n출력:\\n${data.output}\\n\\n실행 시간: ${data.execution_time}초`;
                    } else {
                        resultDiv.textContent = `❌ 실행 실패!\\n\\n오류:\\n${data.error}`;
                    }
                })
                .catch(error => {
                    console.error('API 오류:', error);
                    resultDiv.textContent = `❌ 네트워크 오류: ${error.message}`;
                });
            }
            
            function testClear() {
                console.log('testClear 함수 호출됨!');
                codeEditor.value = '';
                resultDiv.textContent = '코드가 지워졌습니다.';
            }
            
            function testAlert() {
                console.log('testAlert 함수 호출됨!');
                alert('JavaScript가 정상 작동합니다!');
            }
            
            // 페이지 로드 완료 메시지
            window.addEventListener('load', function() {
                console.log('페이지 완전 로드 완료');
                resultDiv.textContent = '페이지가 준비되었습니다. 버튼을 클릭해보세요!';
            });
            
            console.log('=== JavaScript 초기화 완료 ===');
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@router.get("/demo/sandbox")
async def enhanced_sandbox_demo():
    """향상된 샌드박스 데모 페이지"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🚀 향상된 샌드박스 - Agentic AI</title>
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
                grid-template-columns: 1fr 400px;
                gap: 20px;
                margin-bottom: 20px;
            }

            .code-section {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }

            .controls-section {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }

            .control-card {
                background: white;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }

            .section-title {
                font-size: 1.3rem;
                font-weight: bold;
                margin-bottom: 15px;
                color: #4a5568;
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .language-selector {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
                gap: 10px;
                margin-bottom: 20px;
            }

            .lang-btn {
                padding: 12px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                background: white;
                cursor: pointer;
                transition: all 0.3s ease;
                text-align: center;
                font-weight: 600;
                font-size: 0.9rem;
            }

            .lang-btn:hover {
                border-color: #667eea;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
            }

            .lang-btn.active {
                background: #667eea;
                color: white;
                border-color: #667eea;
            }

            .security-level {
                margin-bottom: 20px;
            }

            .security-btn {
                width: 100%;
                padding: 12px;
                margin: 5px 0;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background: white;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 600;
            }

            .security-btn:hover {
                border-color: #667eea;
                transform: translateY(-1px);
            }

            .security-btn.active {
                background: #667eea;
                color: white;
                border-color: #667eea;
            }

            .code-editor {
                width: 100%;
                height: 400px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                font-size: 14px;
                resize: vertical;
                background: #f8fafc;
                transition: border-color 0.3s ease;
            }

            .code-editor:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }

            .execution-controls {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }

            .btn {
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                gap: 8px;
                text-decoration: none;
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
                transform: translateY(-1px);
            }

            .btn-success {
                background: #48bb78;
                color: white;
            }

            .btn-success:hover {
                background: #38a169;
                transform: translateY(-1px);
            }

            .btn-warning {
                background: #ed8936;
                color: white;
            }

            .btn-warning:hover {
                background: #dd6b20;
                transform: translateY(-1px);
            }

            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none !important;
            }

            .execution-status {
                background: #f7fafc;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                border-left: 4px solid #667eea;
            }

            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 8px;
            }

            .status-idle { background: #a0aec0; }
            .status-running { background: #ed8936; animation: pulse 1.5s infinite; }
            .status-success { background: #48bb78; }
            .status-error { background: #f56565; }

            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }

            .result-section {
                background: #1a202c;
                color: #e2e8f0;
                border-radius: 10px;
                padding: 20px;
                font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                font-size: 13px;
                min-height: 200px;
                max-height: 400px;
                overflow-y: auto;
                white-space: pre-wrap;
                word-break: break-word;
            }

            .result-success {
                border-left: 4px solid #48bb78;
            }

            .result-error {
                border-left: 4px solid #f56565;
            }

            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 10px;
                margin-top: 15px;
            }

            .stat-item {
                background: #f7fafc;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #e2e8f0;
            }

            .stat-value {
                font-size: 1.2rem;
                font-weight: bold;
                color: #667eea;
            }

            .stat-label {
                font-size: 0.8rem;
                color: #718096;
                margin-top: 2px;
            }

            .file-operations {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
                flex-wrap: wrap;
            }

            .hidden {
                display: none;
            }

            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            .execution-history {
                max-height: 300px;
                overflow-y: auto;
            }

            .history-item {
                background: #f7fafc;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 8px;
                border-left: 3px solid #e2e8f0;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .history-item:hover {
                background: #edf2f7;
                border-left-color: #667eea;
            }

            .history-time {
                font-size: 0.8rem;
                color: #718096;
                margin-bottom: 4px;
            }

            .history-language {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 0.7rem;
                margin-right: 8px;
            }

            .history-status {
                display: inline-block;
                padding: 2px 6px;
                border-radius: 8px;
                font-size: 0.7rem;
                font-weight: 600;
            }

            .history-status.success {
                background: #c6f6d5;
                color: #22543d;
            }

            .history-status.error {
                background: #fed7d7;
                color: #742a2a;
            }

            @media (max-width: 1024px) {
                .main-grid {
                    grid-template-columns: 1fr;
                }
                
                .header h1 {
                    font-size: 2rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 향상된 샌드박스</h1>
                <p>다중 언어 지원 • 실시간 실행 • 보안 강화</p>
            </div>

            <div class="main-grid">
                <div class="code-section">
                    <div class="section-title">
                        <span>📝</span>
                        코드 에디터
                    </div>

                    <!-- 언어 선택 -->
                    <div class="language-selector">
                        <div class="lang-btn active" data-lang="python" onclick="selectLanguage('python', this)">🐍 Python</div>
                        <div class="lang-btn" data-lang="javascript" onclick="selectLanguage('javascript', this)">🟨 JavaScript</div>
                        <div class="lang-btn" data-lang="java" onclick="selectLanguage('java', this)">☕ Java</div>
                        <div class="lang-btn" data-lang="go" onclick="selectLanguage('go', this)">🐹 Go</div>
                        <div class="lang-btn" data-lang="rust" onclick="selectLanguage('rust', this)">🦀 Rust</div>
                        <div class="lang-btn" data-lang="cpp" onclick="selectLanguage('cpp', this)">⚡ C++</div>
                        <div class="lang-btn" data-lang="csharp" onclick="selectLanguage('csharp', this)">🔷 C#</div>
                        <div class="lang-btn" data-lang="php" onclick="selectLanguage('php', this)">🐘 PHP</div>
                    </div>

                    <!-- 코드 에디터 -->
                    <textarea id="codeEditor" class="code-editor" placeholder="여기에 코드를 입력하세요..."># Python 예제
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 피보나치 수열 계산
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")</textarea>

                    <!-- 실행 컨트롤 -->
                    <div class="execution-controls">
                        <button id="executeBtn" class="btn btn-primary" onclick="
                            console.log('실행 버튼 클릭!');
                            const codeEditor = document.getElementById('codeEditor');
                            const resultSection = document.getElementById('resultSection');
                            if (!codeEditor || !resultSection) {
                                alert('DOM 요소를 찾을 수 없습니다!');
                                return;
                            }
                            const code = codeEditor.value.trim();
                            if (!code) {
                                alert('실행할 코드를 입력해주세요!');
                                return;
                            }
                            
                            // 현재 선택된 언어 확인
                            const activeLangBtn = document.querySelector('.lang-btn.active');
                            const language = activeLangBtn ? activeLangBtn.dataset.lang : 'python';
                            console.log('선택된 언어:', language);
                            
                            resultSection.textContent = '실행 중...';
                            fetch('/api/v1/sandbox/execute', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    code: code,
                                    language: language,
                                    security_level: 'low',
                                    user_id: 'demo_user'
                                })
                            })
                            .then(response => response.json())
                            .then(data => {
                                console.log('API 응답:', data);
                                if (data.success) {
                                    resultSection.textContent = data.output;
                                    resultSection.className = 'result-section result-success';
                                } else {
                                    resultSection.textContent = data.error || '실행 중 오류가 발생했습니다.';
                                    resultSection.className = 'result-section result-error';
                                }
                            })
                            .catch(error => {
                                console.error('API 오류:', error);
                                resultSection.textContent = '❌ 네트워크 오류: ' + error.message;
                                resultSection.className = 'result-section result-error';
                            });
                        ">
                            <span>▶️</span> 실행
                        </button>
                        <button id="clearBtn" class="btn btn-secondary" onclick="
                            console.log('지우기 버튼 클릭!');
                            const codeEditor = document.getElementById('codeEditor');
                            const resultSection = document.getElementById('resultSection');
                            if (codeEditor) codeEditor.value = '';
                            if (resultSection) {
                                resultSection.textContent = '';
                                resultSection.className = 'result-section';
                            }
                        ">
                            <span>🗑️</span> 지우기
                        </button>
                        <button id="saveBtn" class="btn btn-success">
                            <span>💾</span> 저장
                        </button>
                        <button id="loadBtn" class="btn btn-secondary">
                            <span>📁</span> 불러오기
                            <input type="file" id="fileInput" accept=".py,.js,.java,.go,.rs,.cpp,.cs,.php" style="display: none;">
                        </button>
                    </div>

                    <!-- 실행 상태 -->
                    <div id="executionStatus" class="execution-status hidden">
                        <div>
                            <span id="statusIndicator" class="status-indicator status-idle"></span>
                            <span id="statusText">대기 중</span>
                        </div>
                        <div id="executionProgress" class="hidden">
                            <div class="loading"></div>
                            <span>실행 중...</span>
                        </div>
                    </div>

                    <!-- 실행 결과 -->
                    <div class="section-title">
                        <span>📊</span>
                        실행 결과
                    </div>
                    <div id="resultSection" class="result-section">
실행 결과가 여기에 표시됩니다...
                    </div>
                    
                    <!-- 시각화 섹션 -->
                    <div class="section-title">
                        <span>📊</span>
                        결과 시각화
                    </div>
                    <div id="visualizationSection" class="result-section hidden">
                        <div id="visualizationContent"></div>
                    </div>
                </div>

                <div class="controls-section">
                    <!-- 보안 레벨 -->
                    <div class="control-card">
                        <div class="section-title">
                            <span>🔒</span>
                            보안 레벨
                        </div>
                        <div class="security-level">
                            <button class="security-btn active" data-level="LOW">
                                🟢 LOW<br>
                                <small>기본 제한</small>
                            </button>
                            <button class="security-btn" data-level="MEDIUM">
                                🟡 MEDIUM<br>
                                <small>중간 제한</small>
                            </button>
                            <button class="security-btn" data-level="HIGH">
                                🟠 HIGH<br>
                                <small>강한 제한</small>
                            </button>
                            <button class="security-btn" data-level="MAXIMUM">
                                🔴 MAXIMUM<br>
                                <small>최대 제한</small>
                            </button>
                        </div>
                    </div>

                    <!-- 시스템 상태 -->
                    <div class="control-card">
                        <div class="section-title">
                            <span>📈</span>
                            시스템 상태
                        </div>
                        <div id="systemStats" class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-value" id="cpuUsage">--</div>
                                <div class="stat-label">CPU 사용률</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value" id="memoryUsage">--</div>
                                <div class="stat-label">메모리 사용률</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value" id="activeExecutions">0</div>
                                <div class="stat-label">실행 중</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value" id="totalExecutions">0</div>
                                <div class="stat-label">총 실행</div>
                            </div>
                        </div>
                        <button id="refreshStatsBtn" class="btn btn-secondary" style="width: 100%; margin-top: 10px;">
                            <span>🔄</span> 상태 새로고침
                        </button>
                    </div>

                    <!-- 실행 히스토리 -->
                    <div class="control-card">
                        <div class="section-title">
                            <span>📜</span>
                            실행 히스토리
                        </div>
                        <div id="executionHistory" class="execution-history">
                            <div style="text-align: center; color: #718096; padding: 20px;">
                                아직 실행 기록이 없습니다
                            </div>
                        </div>
                        <button id="clearHistoryBtn" class="btn btn-secondary" style="width: 100%; margin-top: 10px;">
                            <span>🗑️</span> 히스토리 지우기
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            console.log('JavaScript 시작!');
            
            // 전역 변수
            let currentLanguage = 'python';
            let currentSecurityLevel = 'LOW';
            let executionHistory = [];
            let isExecuting = false;
            
            console.log('전역 변수 초기화 완료');

            // 언어 선택 함수
            function selectLanguage(language, element) {
                console.log('언어 선택:', language);
                
                // 모든 언어 버튼에서 active 클래스 제거
                document.querySelectorAll('.lang-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // 선택된 버튼에 active 클래스 추가
                element.classList.add('active');
                
                // 전역 변수 업데이트
                currentLanguage = language;
                
                // 언어별 코드 템플릿 로드
                const codeTemplates = {
                    python: `# Python 예제
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 피보나치 수열 계산
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")`,

                    javascript: `// JavaScript 고급 예제 - 배열 조작과 비동기 처리
console.log("=== JavaScript 고급 예제 ===");

// 1. 배열 메서드 체이닝
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const result = numbers
    .filter(n => n % 2 === 0)  // 짝수만 필터링
    .map(n => n * n)           // 제곱 계산
    .reduce((sum, n) => sum + n, 0); // 합계 계산

console.log("원본 배열:", numbers);
console.log("짝수의 제곱의 합:", result);

// 2. 객체 조작
const users = [
    { name: "Alice", age: 25, city: "Seoul" },
    { name: "Bob", age: 30, city: "Busan" },
    { name: "Charlie", age: 35, city: "Seoul" }
];

const seoulUsers = users.filter(user => user.city === "Seoul");
console.log("서울 거주자:", seoulUsers);

// 3. 클래스와 상속
class Animal {
    constructor(name) {
        this.name = name;
    }
    
    speak() {
        console.log(\`\${this.name}가 소리를 냅니다.\`);
    }
}

class Dog extends Animal {
    speak() {
        console.log(\`\${this.name}가 멍멍 짖습니다!\`);
    }
}

const myDog = new Dog("멍멍이");
myDog.speak();

// 4. 비동기 처리 (Promise)
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function asyncExample() {
    console.log("비동기 작업 시작...");
    await delay(1000);
    console.log("1초 후 실행됨!");
    await delay(500);
    console.log("추가 0.5초 후 실행됨!");
}

asyncExample().then(() => {
    console.log("모든 비동기 작업 완료!");
});`,

                    java: `// Java 예제
public class Fibonacci {
    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            System.out.println("F(" + i + ") = " + fibonacci(i));
        }
    }
    
    public static int fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}`,

                    go: `// Go 예제
package main

import "fmt"

func fibonacci(n int) int {
    if n <= 1 {
        return n
    }
    return fibonacci(n-1) + fibonacci(n-2)
}

func main() {
    for i := 0; i < 10; i++ {
        fmt.Printf("F(%d) = %d\\n", i, fibonacci(i))
    }
}`
                };
                
                const codeEditor = document.getElementById('codeEditor');
                if (codeEditor && codeTemplates[language]) {
                    codeEditor.value = codeTemplates[language];
                    console.log('코드 템플릿 로드됨:', language);
                }
                
                alert(`언어가 ${language}로 변경되었습니다!`);
            }

            // 인라인 함수들 (onclick에서 호출)
            function executeCodeInline() {
                console.log('executeCodeInline 함수 호출됨!');
                
                const codeEditor = document.getElementById('codeEditor');
                const resultSection = document.getElementById('resultSection');
                
                if (!codeEditor) {
                    console.error('codeEditor를 찾을 수 없습니다!');
                    alert('코드 에디터를 찾을 수 없습니다!');
                    return;
                }
                
                if (!resultSection) {
                    console.error('resultSection을 찾을 수 없습니다!');
                    alert('결과 섹션을 찾을 수 없습니다!');
                    return;
                }
                
                const code = codeEditor.value.trim();
                console.log('실행할 코드:', code);
                
                if (!code) {
                    resultSection.textContent = '❌ 실행할 코드가 없습니다.';
                    resultSection.className = 'result-section result-error';
                    alert('실행할 코드를 입력해주세요!');
                    return;
                }
                
                resultSection.textContent = '실행 중...';
                resultSection.className = 'result-section';
                
                console.log('API 호출 시작...');
                
                // API 호출
                fetch('/api/v1/sandbox/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code: code,
                        language: 'python',
                        security_level: 'low',
                        user_id: 'demo_user'
                    })
                })
                .then(response => {
                    console.log('API 응답 상태:', response.status);
                    return response.json();
                })
                .then(data => {
                    console.log('API 응답 데이터:', data);
                    if (data.success) {
                        resultSection.textContent = data.output;
                        resultSection.className = 'result-section result-success';
                        console.log('실행 성공!');
                    } else {
                        resultSection.textContent = data.error || '실행 중 오류가 발생했습니다.';
                        resultSection.className = 'result-section result-error';
                        console.log('실행 실패:', data.error);
                    }
                })
                .catch(error => {
                    console.error('API 오류:', error);
                    resultSection.textContent = `❌ 네트워크 오류: ${error.message}`;
                    resultSection.className = 'result-section result-error';
                });
            }
            
            function clearCodeInline() {
                console.log('clearCodeInline 함수 호출됨!');
                
                const codeEditor = document.getElementById('codeEditor');
                const resultSection = document.getElementById('resultSection');
                
                if (codeEditor) {
                    codeEditor.value = '';
                    console.log('코드 에디터가 지워졌습니다');
                }
                
                if (resultSection) {
                    resultSection.textContent = '';
                    resultSection.className = 'result-section';
                    console.log('결과 섹션이 지워졌습니다');
                }
                
                alert('코드가 지워졌습니다!');
            }

            // 실제 API 호출 함수들
            function executeCode() {
                console.log('executeCodeNow 함수 호출됨!');
                
                const codeEditor = document.getElementById('codeEditor');
                const resultSection = document.getElementById('resultSection');
                
                if (!codeEditor) {
                    console.error('codeEditor를 찾을 수 없습니다!');
                    alert('코드 에디터를 찾을 수 없습니다!');
                    return;
                }
                
                if (!resultSection) {
                    console.error('resultSection을 찾을 수 없습니다!');
                    alert('결과 섹션을 찾을 수 없습니다!');
                    return;
                }
                
                const code = codeEditor.value.trim();
                console.log('실행할 코드:', code);
                
                if (!code) {
                    resultSection.textContent = '❌ 실행할 코드가 없습니다.';
                    resultSection.className = 'result-section result-error';
                    alert('실행할 코드를 입력해주세요!');
                    return;
                }
                
                resultSection.textContent = '실행 중...';
                resultSection.className = 'result-section';
                
                console.log('API 호출 시작...');
                
                // API 호출
                fetch('/api/v1/sandbox/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code: code,
                        language: 'python',
                        security_level: 'LOW',
                        user_id: 'demo_user'
                    })
                })
                .then(response => {
                    console.log('API 응답 상태:', response.status);
                    return response.json();
                })
                .then(data => {
                    console.log('API 응답 데이터:', data);
                    if (data.success) {
                        resultSection.textContent = data.output;
                        resultSection.className = 'result-section result-success';
                        console.log('실행 성공!');
                    } else {
                        resultSection.textContent = data.error || '실행 중 오류가 발생했습니다.';
                        resultSection.className = 'result-section result-error';
                        console.log('실행 실패:', data.error);
                    }
                })
                .catch(error => {
                    console.error('API 오류:', error);
                    resultSection.textContent = `❌ 네트워크 오류: ${error.message}`;
                    resultSection.className = 'result-section result-error';
                });
            }
            
            function clearCode() {
                console.log('clearCodeNow 함수 호출됨!');
                
                const codeEditor = document.getElementById('codeEditor');
                const resultSection = document.getElementById('resultSection');
                
                if (codeEditor) {
                    codeEditor.value = '';
                    console.log('코드 에디터가 지워졌습니다');
                }
                
                if (resultSection) {
                    resultSection.textContent = '';
                    resultSection.className = 'result-section';
                    console.log('결과 섹션이 지워졌습니다');
                }
                
                alert('코드가 지워졌습니다!');
            }

            // 간단한 테스트 함수들
            function testExecute() {
                console.log('testExecute 함수 호출됨!');
                alert('실행 버튼이 클릭되었습니다!');
            }
            
            function testClear() {
                console.log('testClear 함수 호출됨!');
                alert('지우기 버튼이 클릭되었습니다!');
            }
            
            // 샌드박스 데모용 간단한 함수들
            function simpleExecute() {
                console.log('simpleExecute 함수 호출됨!');
                const codeEditor = document.getElementById('codeEditor');
                const resultSection = document.getElementById('resultSection');
                
                if (!codeEditor) {
                    console.error('codeEditor를 찾을 수 없습니다!');
                    alert('코드 에디터를 찾을 수 없습니다!');
                    return;
                }
                
                if (!resultSection) {
                    console.error('resultSection을 찾을 수 없습니다!');
                    alert('결과 섹션을 찾을 수 없습니다!');
                    return;
                }
                
                const code = codeEditor.value.trim();
                console.log('실행할 코드:', code);
                
                if (!code) {
                    resultSection.textContent = '❌ 실행할 코드가 없습니다.';
                    resultSection.className = 'result-section result-error';
                    return;
                }
                
                resultSection.textContent = '실행 중...';
                resultSection.className = 'result-section';
                
                // API 호출
                fetch('/api/v1/sandbox/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        code: code,
                        language: 'python',
                        security_level: 'LOW',
                        user_id: 'demo_user'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('API 응답:', data);
                    if (data.success) {
                        resultSection.textContent = data.output;
                        resultSection.className = 'result-section result-success';
                    } else {
                        resultSection.textContent = data.error || '실행 중 오류가 발생했습니다.';
                        resultSection.className = 'result-section result-error';
                    }
                })
                .catch(error => {
                    console.error('API 오류:', error);
                    resultSection.textContent = `❌ 네트워크 오류: ${error.message}`;
                    resultSection.className = 'result-section result-error';
                });
            }
            
            function simpleClear() {
                console.log('simpleClear 함수 호출됨!');
                const codeEditor = document.getElementById('codeEditor');
                const resultSection = document.getElementById('resultSection');
                
                if (codeEditor) {
                    codeEditor.value = '';
                    console.log('코드 에디터가 지워졌습니다');
                }
                
                if (resultSection) {
                    resultSection.textContent = '';
                    resultSection.className = 'result-section';
                    console.log('결과 섹션이 지워졌습니다');
                }
            }

            // DOM 요소
            const codeEditor = document.getElementById('codeEditor');
            const executeBtn = document.getElementById('executeBtn');
            const clearBtn = document.getElementById('clearBtn');
            const saveBtn = document.getElementById('saveBtn');
            const loadBtn = document.getElementById('loadBtn');
            const fileInput = document.getElementById('fileInput');
            const executionStatus = document.getElementById('executionStatus');
            const statusIndicator = document.getElementById('statusIndicator');
            const statusText = document.getElementById('statusText');
            const executionProgress = document.getElementById('executionProgress');
            const resultSection = document.getElementById('resultSection');
            const visualizationSection = document.getElementById('visualizationSection');
            const visualizationContent = document.getElementById('visualizationContent');
            const systemStats = document.getElementById('systemStats');
            const executionHistoryDiv = document.getElementById('executionHistory');
            const refreshStatsBtn = document.getElementById('refreshStatsBtn');
            const clearHistoryBtn = document.getElementById('clearHistoryBtn');

            // DOM 요소 존재 확인
            console.log('=== DOM 요소 확인 ===');
            console.log('codeEditor:', codeEditor);
            console.log('executeBtn:', executeBtn);
            console.log('clearBtn:', clearBtn);
            console.log('saveBtn:', saveBtn);
            console.log('loadBtn:', loadBtn);
            console.log('fileInput:', fileInput);
            console.log('executionStatus:', executionStatus);
            console.log('statusIndicator:', statusIndicator);
            console.log('statusText:', statusText);
            console.log('executionProgress:', executionProgress);
            console.log('resultSection:', resultSection);
            console.log('visualizationSection:', visualizationSection);
            console.log('visualizationContent:', visualizationContent);
            console.log('systemStats:', systemStats);
            console.log('executionHistoryDiv:', executionHistoryDiv);
            console.log('refreshStatsBtn:', refreshStatsBtn);
            console.log('clearHistoryBtn:', clearHistoryBtn);

            // 언어별 기본 코드 템플릿
            const codeTemplates = {
                python: `# Python 예제
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 피보나치 수열 계산
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")`,

                javascript: `// JavaScript 예제
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// 피보나치 수열 계산
for (let i = 0; i < 10; i++) {
    console.log(`F(${i}) = ${fibonacci(i)}`);
}`,

                java: `// Java 예제
public class Fibonacci {
    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            System.out.println("F(" + i + ") = " + fibonacci(i));
        }
    }
    
    public static int fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}`,

                go: `// Go 예제
package main

import "fmt"

func fibonacci(n int) int {
    if n <= 1 {
        return n
    }
    return fibonacci(n-1) + fibonacci(n-2)
}

func main() {
    for i := 0; i < 10; i++ {
        fmt.Printf("F(%d) = %d\\n", i, fibonacci(i))
    }
}`,

                rust: `// Rust 예제
fn fibonacci(n: u32) -> u32 {
    match n {
        0 | 1 => n,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn main() {
    for i in 0..10 {
        println!("F({}) = {}", i, fibonacci(i));
    }
}`,

                cpp: `// C++ 예제
#include <iostream>
using namespace std;

int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    for (int i = 0; i < 10; i++) {
        cout << "F(" << i << ") = " << fibonacci(i) << endl;
    }
    return 0;
}`,

                csharp: `// C# 예제
using System;

class Program {
    static int Fibonacci(int n) {
        if (n <= 1) return n;
        return Fibonacci(n - 1) + Fibonacci(n - 2);
    }
    
    static void Main() {
        for (int i = 0; i < 10; i++) {
            Console.WriteLine($"F({i}) = {Fibonacci(i)}");
        }
    }
}`,

                php: `<?php
// PHP 예제
function fibonacci($n) {
    if ($n <= 1) return $n;
    return fibonacci($n - 1) + fibonacci($n - 2);
}

// 피보나치 수열 계산
for ($i = 0; $i < 10; $i++) {
    echo "F($i) = " . fibonacci($i) . "\\n";
}
?>`
            };

            // 초기화
            document.addEventListener('DOMContentLoaded', function() {
                console.log('DOM 로드 완료, 이벤트 리스너 초기화 시작');
                initializeEventListeners();
                updateSystemStats();
                setInterval(updateSystemStats, 5000); // 5초마다 업데이트
                console.log('초기화 완료');
            });

            function initializeEventListeners() {
                console.log('이벤트 리스너 초기화 시작');
                
                // 언어 선택
                const langButtons = document.querySelectorAll('.lang-btn');
                console.log('언어 버튼 개수:', langButtons.length);
                langButtons.forEach(btn => {
                    btn.addEventListener('click', function() {
                        console.log('언어 버튼 클릭:', this.dataset.lang);
                        document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
                        this.classList.add('active');
                        currentLanguage = this.dataset.lang;
                        loadLanguageTemplate();
                    });
                });

                // 보안 레벨 선택
                const securityButtons = document.querySelectorAll('.security-btn');
                console.log('보안 버튼 개수:', securityButtons.length);
                securityButtons.forEach(btn => {
                    btn.addEventListener('click', function() {
                        console.log('보안 버튼 클릭:', this.dataset.level);
                        document.querySelectorAll('.security-btn').forEach(b => b.classList.remove('active'));
                        this.classList.add('active');
                        currentSecurityLevel = this.dataset.level;
                    });
                });

                // 버튼 이벤트
                console.log('주요 버튼 이벤트 리스너 등록');
                
                if (executeBtn) {
                    executeBtn.addEventListener('click', executeCode);
                    console.log('실행 버튼 이벤트 리스너 등록 완료');
                } else {
                    console.error('실행 버튼을 찾을 수 없습니다!');
                }
                
                if (clearBtn) {
                    clearBtn.addEventListener('click', clearCode);
                    console.log('지우기 버튼 이벤트 리스너 등록 완료');
                } else {
                    console.error('지우기 버튼을 찾을 수 없습니다!');
                }
                
                if (saveBtn) {
                    saveBtn.addEventListener('click', saveCode);
                    console.log('저장 버튼 이벤트 리스너 등록 완료');
                } else {
                    console.error('저장 버튼을 찾을 수 없습니다!');
                }
                
                if (loadBtn && fileInput) {
                    loadBtn.addEventListener('click', () => fileInput.click());
                    fileInput.addEventListener('change', loadCode);
                    console.log('로드 버튼 이벤트 리스너 등록 완료');
                } else {
                    console.error('로드 버튼 또는 파일 입력을 찾을 수 없습니다!');
                }
                
                if (refreshStatsBtn) {
                    refreshStatsBtn.addEventListener('click', updateSystemStats);
                    console.log('상태 새로고침 버튼 이벤트 리스너 등록 완료');
                } else {
                    console.error('상태 새로고침 버튼을 찾을 수 없습니다!');
                }
                
                if (clearHistoryBtn) {
                    clearHistoryBtn.addEventListener('click', clearHistory);
                    console.log('히스토리 지우기 버튼 이벤트 리스너 등록 완료');
                } else {
                    console.error('히스토리 지우기 버튼을 찾을 수 없습니다!');
                }
                
                console.log('이벤트 리스너 초기화 완료');
                
                // 추가 디버깅: 직접 onclick 이벤트도 설정
                if (executeBtn) {
                    executeBtn.onclick = function() {
                        console.log('실행 버튼 onclick 이벤트 발생!');
                        executeCode();
                    };
                    console.log('실행 버튼 onclick 이벤트 설정 완료');
                }
                
                if (clearBtn) {
                    clearBtn.onclick = function() {
                        console.log('지우기 버튼 onclick 이벤트 발생!');
                        clearCode();
                    };
                    console.log('지우기 버튼 onclick 이벤트 설정 완료');
                }
            }

            function loadLanguageTemplate() {
                const template = codeTemplates[currentLanguage];
                if (template) {
                    codeEditor.value = template;
                }
            }

            async function executeCode() {
                console.log('executeCode 함수 호출됨');
                
                if (isExecuting) {
                    console.log('이미 실행 중입니다');
                    return;
                }

                const code = codeEditor.value.trim();
                console.log('코드 길이:', code.length);
                
                if (!code) {
                    showResult('❌ 실행할 코드가 없습니다.', 'error');
                    return;
                }

                isExecuting = true;
                updateExecutionStatus('running', '실행 중...');
                showExecutionProgress(true);
                
                console.log('API 요청 시작:', {
                    language: currentLanguage,
                    security_level: currentSecurityLevel,
                    code_length: code.length
                });

                try {
                    const response = await fetch('/api/v1/sandbox/execute', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            code: code,
                            language: currentLanguage,
                            security_level: currentSecurityLevel,
                            user_id: 'demo_user'
                        })
                    });

                    console.log('API 응답 상태:', response.status);
                    const result = await response.json();
                    console.log('API 응답 결과:', result);

                    if (result.success) {
                        showResult(result.output, 'success');
                        hideVisualization();
                        addToHistory(result, 'success');
                    } else {
                        showResult(result.error || '실행 중 오류가 발생했습니다.', 'error');
                        hideVisualization();
                        addToHistory(result, 'error');
                    }

                } catch (error) {
                    console.error('API 요청 오류:', error);
                    showResult(`❌ 네트워크 오류: ${error.message}`, 'error');
                } finally {
                    isExecuting = false;
                    updateExecutionStatus('idle', '대기 중');
                    showExecutionProgress(false);
                }
            }

            function updateExecutionStatus(status, text) {
                statusIndicator.className = `status-indicator status-${status}`;
                statusText.textContent = text;
                executionStatus.classList.remove('hidden');
            }

            function showExecutionProgress(show) {
                if (show) {
                    executionProgress.classList.remove('hidden');
                } else {
                    executionProgress.classList.add('hidden');
                }
            }

            function showResult(content, type) {
                resultSection.textContent = content;
                resultSection.className = `result-section result-${type}`;
            }

            function showVisualization(visualization) {
                if (visualization && visualization.html) {
                    visualizationContent.innerHTML = visualization.html;
                    visualizationSection.classList.remove('hidden');
                    
                    // Chart.js가 필요한 경우 스크립트 로드
                    if (visualization.type === 'chart' && !window.Chart) {
                        loadChartJS();
                    }
                } else {
                    hideVisualization();
                }
            }

            function hideVisualization() {
                visualizationSection.classList.add('hidden');
                visualizationContent.innerHTML = '';
            }

            function loadChartJS() {
                const script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
                script.onload = function() {
                    console.log('Chart.js 로드 완료');
                };
                document.head.appendChild(script);
            }

            function addToHistory(result, status) {
                const historyItem = {
                    id: Date.now(),
                    timestamp: new Date().toLocaleString(),
                    language: currentLanguage,
                    status: status,
                    execution_time: result.execution_time || 0,
                    memory_used: result.memory_used || 0,
                    code_length: codeEditor.value.length
                };

                executionHistory.unshift(historyItem);
                if (executionHistory.length > 50) {
                    executionHistory.pop();
                }

                updateHistoryDisplay();
                updateExecutionCounts();
            }

            function updateHistoryDisplay() {
                if (executionHistory.length === 0) {
                    executionHistoryDiv.innerHTML = `
                        <div style="text-align: center; color: #718096; padding: 20px;">
                            아직 실행 기록이 없습니다
                        </div>
                    `;
                    return;
                }

                executionHistoryDiv.innerHTML = executionHistory.map(item => `
                    <div class="history-item" onclick="loadHistoryItem('${item.id}')">
                        <div class="history-time">${item.timestamp}</div>
                        <span class="history-language">${item.language.toUpperCase()}</span>
                        <span class="history-status ${item.status}">${item.status === 'success' ? '성공' : '실패'}</span>
                        <div style="font-size: 0.8rem; color: #718096; margin-top: 4px;">
                            실행시간: ${item.execution_time}ms | 메모리: ${item.memory_used}MB
                        </div>
                    </div>
                `).join('');
            }

            function loadHistoryItem(itemId) {
                const item = executionHistory.find(h => h.id == itemId);
                if (item) {
                    // 해당 히스토리 항목의 코드를 에디터에 로드
                    // 실제 구현에서는 코드 내용을 저장해야 함
                    console.log('히스토리 항목 로드:', item);
                }
            }

            function updateExecutionCounts() {
                document.getElementById('totalExecutions').textContent = executionHistory.length;
                document.getElementById('activeExecutions').textContent = isExecuting ? '1' : '0';
            }

            async function updateSystemStats() {
                try {
                    const response = await fetch('/api/v1/sandbox/stats');
                    const stats = await response.json();

                    if (stats.success) {
                        document.getElementById('cpuUsage').textContent = `${stats.cpu_percent.toFixed(1)}%`;
                        document.getElementById('memoryUsage').textContent = `${stats.memory_percent.toFixed(1)}%`;
                    }
                } catch (error) {
                    console.error('시스템 상태 업데이트 실패:', error);
                }
            }

            function clearCode() {
                console.log('clearCode 함수 호출됨');
                codeEditor.value = '';
                showResult('코드가 지워졌습니다.', 'success');
                console.log('코드 에디터가 지워졌습니다');
            }

            function saveCode() {
                const code = codeEditor.value;
                const blob = new Blob([code], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `code.${getFileExtension(currentLanguage)}`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }

            function loadCode(event) {
                const file = event.target.files[0];
                if (!file) return;

                const reader = new FileReader();
                reader.onload = function(e) {
                    codeEditor.value = e.target.result;
                    showResult('파일이 로드되었습니다.', 'success');
                };
                reader.readAsText(file);
            }

            function clearHistory() {
                executionHistory = [];
                updateHistoryDisplay();
                updateExecutionCounts();
            }

            function getFileExtension(language) {
                const extensions = {
                    python: 'py',
                    javascript: 'js',
                    java: 'java',
                    go: 'go',
                    rust: 'rs',
                    cpp: 'cpp',
                    csharp: 'cs',
                    php: 'php'
                };
                return extensions[language] || 'txt';
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
                            saveCode();
                            break;
                    }
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/demo/sandbox/simple")
async def simple_sandbox_demo():
    """간단한 샌드박스 데모 페이지"""
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🚀 간단한 샌드박스</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }
            .language-selector {
                margin-bottom: 20px;
            }
            .lang-btn {
                padding: 10px 15px;
                margin: 5px;
                border: 1px solid #ddd;
                background: white;
                cursor: pointer;
                border-radius: 5px;
            }
            .lang-btn.active {
                background: #007bff;
                color: white;
            }
            textarea {
                width: 100%;
                height: 300px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-family: monospace;
                font-size: 14px;
            }
            .controls {
                margin: 20px 0;
                text-align: center;
            }
            .btn {
                padding: 12px 24px;
                margin: 0 10px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }
            .btn-primary {
                background: #007bff;
                color: white;
            }
            .btn-secondary {
                background: #6c757d;
                color: white;
            }
            .result {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 15px;
                margin-top: 20px;
                min-height: 100px;
                font-family: monospace;
                white-space: pre-wrap;
            }
            .status {
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                text-align: center;
            }
            .status-running {
                background: #fff3cd;
                color: #856404;
            }
            .status-success {
                background: #d4edda;
                color: #155724;
            }
            .status-error {
                background: #f8d7da;
                color: #721c24;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 간단한 샌드박스 데모</h1>
            
            <div class="language-selector">
                <button class="lang-btn active" data-lang="python">Python</button>
                <button class="lang-btn" data-lang="javascript">JavaScript</button>
                <button class="lang-btn" data-lang="java">Java</button>
                <button class="lang-btn" data-lang="go">Go</button>
            </div>

            <textarea id="codeEditor" placeholder="여기에 코드를 입력하세요..."># Python 예제
print("Hello, Sandbox!")
for i in range(5):
    print(f"숫자: {i}")</textarea>

            <div class="controls">
                <button class="btn btn-primary" onclick="executeCode()">실행</button>
                <button class="btn btn-secondary" onclick="clearCode()">지우기</button>
            </div>

            <div id="status" class="status" style="display: none;"></div>
            <div id="result" class="result">실행 결과가 여기에 표시됩니다...</div>
        </div>

        <script>
            let currentLanguage = 'python';

            // 언어 선택
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    currentLanguage = this.dataset.lang;
                });
            });

            async function executeCode() {
                const code = document.getElementById('codeEditor').value;
                const status = document.getElementById('status');
                const result = document.getElementById('result');

                if (!code.trim()) {
                    result.textContent = '실행할 코드가 없습니다.';
                    return;
                }

                status.className = 'status status-running';
                status.textContent = '실행 중...';
                status.style.display = 'block';

                try {
                    const response = await fetch('/api/v1/sandbox/execute', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            code: code,
                            language: currentLanguage,
                            security_level: 'LOW',
                            user_id: 'demo_user'
                        })
                    });

                    const data = await response.json();

                    if (data.success) {
                        status.className = 'status status-success';
                        status.textContent = `실행 완료 (${data.execution_time}ms)`;
                        result.textContent = data.output;
                    } else {
                        status.className = 'status status-error';
                        status.textContent = '실행 실패';
                        result.textContent = data.error || '알 수 없는 오류가 발생했습니다.';
                    }

                } catch (error) {
                    status.className = 'status status-error';
                    status.textContent = '네트워크 오류';
                    result.textContent = `오류: ${error.message}`;
                }
            }

            function clearCode() {
                document.getElementById('codeEditor').value = '';
                document.getElementById('result').textContent = '코드가 지워졌습니다.';
                document.getElementById('status').style.display = 'none';
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
