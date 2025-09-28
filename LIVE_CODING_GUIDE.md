# 🚀 바이브 코딩 가이드

## 🎯 **개요**

Agentic AI 시스템에 실시간 바이브 코딩 기능이 추가되었습니다! WebSocket 기반의 실시간 코드 실행, 분석, 협업 환경을 제공합니다.

## ✨ **주요 기능**

### 🔌 **실시간 WebSocket 통신**
- 클라이언트-서버 간 양방향 실시간 통신
- 연결 상태 관리 및 자동 재연결
- 방 기반 멀티 유저 협업

### 💻 **실시간 코드 실행**
- Python, JavaScript, Java, Go 지원
- Docker 기반 안전한 실행 환경
- 로컬 실행 모드 지원
- 실행 결과 실시간 반환

### 🔍 **실시간 코드 분석**
- AST 기반 코드 품질 분석
- 버그 탐지 및 개선 제안
- 코드 복잡도 측정
- 자동 제안 생성

### 🏠 **협업 환경**
- 방 기반 실시간 협업
- 코드 변경사항 실시간 동기화
- 채팅 기능
- 커서 위치 공유

## 🚀 **빠른 시작**

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
python3 main.py
```

### 3. 데모 페이지 접속
```
http://localhost:8000/api/v1/ws/demo
```

### 4. 바이브 코딩 테스트
```bash
python3 test_live_coding.py
```

## 📡 **WebSocket API**

### **연결**
```
ws://localhost:8000/api/v1/ws/demo
ws://localhost:8000/api/v1/ws/{connection_id}
ws://localhost:8000/api/v1/ws/room/{room_id}
```

### **메시지 타입**

#### 🔗 **연결 관리**
```json
// 연결 확인
{
  "type": "ping"
}

// 방 참여
{
  "type": "join_room",
  "room_id": "room_123"
}

// 방 나가기
{
  "type": "leave_room"
}
```

#### 💻 **코드 실행**
```json
// 코드 실행
{
  "type": "execute_code",
  "code": "print('Hello, World!')",
  "language": "python",
  "file_path": "main.py"
}
```

#### 🔍 **코드 분석**
```json
// 코드 분석 요청
{
  "type": "request_analysis",
  "file_path": "main.py",
  "content": "def hello():\n    print('Hello!')"
}

// 코드 제안 요청
{
  "type": "request_suggestion",
  "file_path": "main.py",
  "content": "def hello():\n    print('Hello!')",
  "position": {"line": 1, "column": 10}
}
```

#### 📝 **코드 편집**
```json
// 코드 변경
{
  "type": "code_change",
  "file_path": "main.py",
  "content": "def hello():\n    print('Hello, World!')",
  "change_type": "edit",
  "position": {"line": 0, "column": 0}
}

// 커서 위치 변경
{
  "type": "cursor_change",
  "file_path": "main.py",
  "position": {"line": 1, "column": 15}
}
```

#### 💬 **채팅**
```json
// 채팅 메시지
{
  "type": "chat_message",
  "message": "이 코드를 어떻게 개선할 수 있을까요?"
}
```

#### 📁 **파일 작업**
```json
// 파일 작업
{
  "type": "file_operation",
  "operation": "create",  // create, delete, rename
  "file_path": "new_file.py",
  "new_path": "renamed_file.py"  // rename 시에만
}
```

## 📥 **응답 메시지**

### **연결 응답**
```json
{
  "type": "connection_established",
  "connection_id": "uuid-123",
  "user_id": "user_456",
  "timestamp": "2024-01-15T10:30:00"
}
```

### **실행 결과**
```json
{
  "type": "execution_result",
  "result": {
    "success": true,
    "output": "Hello, World!\n",
    "error": "",
    "execution_time": 0.05,
    "language": "python",
    "method": "docker"
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

### **분석 결과**
```json
{
  "type": "analysis_result",
  "file_path": "main.py",
  "analysis": {
    "language": "python",
    "success": true,
    "syntax_valid": true,
    "metrics": {
      "lines_of_code": 10,
      "functions": 2,
      "classes": 1,
      "complexity": 3
    },
    "issues": [
      {
        "type": "warning",
        "message": "함수가 너무 깁니다",
        "line": 5,
        "suggestion": "함수를 분할하세요"
      }
    ],
    "quality_score": 85
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🛠️ **지원 언어**

### **Python**
- 버전: 3.11
- 실행 환경: Docker/Local
- 분석 기능: AST 기반 품질 분석

### **JavaScript**
- 버전: Node.js 18
- 실행 환경: Docker/Local
- 분석 기능: 정적 분석

### **Java**
- 버전: OpenJDK 11
- 실행 환경: Docker
- 분석 기능: 기본 분석

### **Go**
- 버전: 1.21
- 실행 환경: Docker
- 분석 기능: 기본 분석

## 🔧 **설정**

### **Docker 설정**
```bash
# Docker 설치 확인
docker --version

# Docker 서비스 시작
sudo systemctl start docker
```

### **환경 변수**
```bash
# .env 파일
DOCKER_ENABLED=true
MAX_EXECUTION_TIME=10
MAX_MEMORY_LIMIT=128m
MAX_CPU_QUOTA=50000
```

## 🧪 **테스트**

### **자동 테스트**
```bash
# 전체 바이브 코딩 기능 테스트
python3 test_live_coding.py
```

### **수동 테스트**
```bash
# 1. 데모 페이지에서 테스트
# http://localhost:8000/api/v1/ws/demo

# 2. WebSocket 클라이언트로 테스트
wscat -c ws://localhost:8000/api/v1/ws/demo
```

## 📊 **성능 지표**

### **실행 성능**
- 코드 실행 지연시간: < 100ms
- 분석 처리 시간: < 500ms
- WebSocket 메시지 지연: < 50ms

### **리소스 사용량**
- 메모리 제한: 128MB per container
- CPU 제한: 50% per container
- 실행 시간 제한: 10초

## 🔒 **보안**

### **코드 실행 보안**
- Docker 컨테이너 격리
- 네트워크 비활성화
- 파일 시스템 제한
- 실행 시간 제한

### **금지된 작업**
- 파일 시스템 접근
- 네트워크 요청
- 시스템 명령 실행
- 무한 루프

## 🚀 **다음 단계**

### **Phase 2: AI 코딩 어시스턴트**
- 실시간 코드 분석
- 자동 코드 완성
- 리팩토링 제안
- 테스트 코드 생성

### **Phase 3: 협업 환경**
- 멀티 유저 편집
- 실시간 코드 리뷰
- 음성 인터페이스
- 화면 공유

### **Phase 4: 고급 기능**
- 디버깅 어시스턴트
- 자동 테스트 생성
- 코드 생성 및 변환
- 성능 프로파일링

## 🎯 **사용 사례**

### **1. 교육용**
- 실시간 코딩 교육
- 즉시 피드백 제공
- 학생-강사 협업

### **2. 개발 협업**
- 페어 프로그래밍
- 코드 리뷰
- 실시간 디버깅

### **3. 프로토타이핑**
- 빠른 아이디어 검증
- 실시간 결과 확인
- 반복적 개발

### **4. 학습 및 연습**
- 코딩 챌린지
- 알고리즘 연습
- 언어 학습

이제 진정한 바이브 코딩 환경을 경험해보세요! 🚀
