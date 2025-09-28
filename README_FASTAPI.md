# 🚀 Agentic AI FastAPI 서버

FastAPI 기반의 REST API 서버로 변환된 Agentic AI 시스템입니다.

## 📋 주요 기능

- **REST API**: FastAPI 기반의 고성능 API 서버
- **자동 문서화**: Swagger UI 및 ReDoc 자동 생성
- **비동기 처리**: async/await 기반의 비동기 처리
- **타입 안전성**: Pydantic 모델을 통한 타입 검증
- **오류 처리**: 구조화된 예외 처리 및 오류 응답
- **CORS 지원**: 크로스 오리진 요청 지원

## 🚀 빠른 시작

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
# 개발 모드 (자동 재시작)
python main.py

# 또는 uvicorn 직접 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. API 문서 확인
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API 엔드포인트

### 🏥 헬스 체크
```bash
# 기본 헬스 체크
GET /api/v1/health

# 상세 헬스 체크
GET /api/v1/health/detailed
```

### 🔍 쿼리 처리
```bash
# 쿼리 처리
POST /api/v1/query
Content-Type: application/json

{
  "question": "Strategy 패턴에 대해 설명해주세요",
  "include_context": true,
  "include_tools": true,
  "max_contexts": 5
}
```

### 📄 문서 관리
```bash
# 문서 목록 조회
GET /api/v1/documents

# 문서 업로드
POST /api/v1/documents/upload
Content-Type: multipart/form-data

# 문서 다운로드
GET /api/v1/documents/{filename}

# 문서 삭제
DELETE /api/v1/documents/{filename}

# 문서 내용 조회
GET /api/v1/documents/{filename}/content?max_length=1000
```

### 🔍 인덱스 관리
```bash
# 인덱스 통계 조회
GET /api/v1/index/stats

# 인덱스 구축
POST /api/v1/index/build
Content-Type: application/json

{
  "force_rebuild": false
}

# 인덱스 삭제
DELETE /api/v1/index

# 인덱스 상태 조회
GET /api/v1/index/status

# 인덱스 재구축
POST /api/v1/index/rebuild
```

## 🧪 API 테스트 예제

### 1. cURL을 사용한 테스트

#### 헬스 체크
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

#### 쿼리 처리
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Strategy 패턴에 대해 설명해주세요",
    "include_context": true,
    "include_tools": true,
    "max_contexts": 5
  }'
```

#### 문서 업로드
```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "files=@example.txt" \
  -F "files=@example.md"
```

#### 인덱스 구축
```bash
curl -X POST "http://localhost:8000/api/v1/index/build" \
  -H "Content-Type: application/json" \
  -d '{"force_rebuild": false}'
```

### 2. Python 클라이언트 예제

```python
import requests
import json

# 기본 설정
BASE_URL = "http://localhost:8000"

# 헬스 체크
response = requests.get(f"{BASE_URL}/api/v1/health")
print("헬스 체크:", response.json())

# 쿼리 처리
query_data = {
    "question": "Strategy 패턴에 대해 설명해주세요",
    "include_context": True,
    "include_tools": True,
    "max_contexts": 5
}

response = requests.post(
    f"{BASE_URL}/api/v1/query",
    json=query_data
)
print("쿼리 결과:", response.json())

# 인덱스 구축
response = requests.post(f"{BASE_URL}/api/v1/index/build")
print("인덱스 구축:", response.json())
```

### 3. JavaScript 클라이언트 예제

```javascript
const BASE_URL = 'http://localhost:8000';

// 헬스 체크
fetch(`${BASE_URL}/api/v1/health`)
  .then(response => response.json())
  .then(data => console.log('헬스 체크:', data));

// 쿼리 처리
const queryData = {
  question: "Strategy 패턴에 대해 설명해주세요",
  include_context: true,
  include_tools: true,
  max_contexts: 5
};

fetch(`${BASE_URL}/api/v1/query`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(queryData)
})
.then(response => response.json())
.then(data => console.log('쿼리 결과:', data));
```

## 🔧 설정

### 환경 변수
```bash
# .env 파일
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
SQLITE_DB=./app/data/demo.db
DEBUG=false
```

### CORS 설정
```python
# main.py에서 CORS 설정 수정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

## 📊 응답 형식

### 성공 응답
```json
{
  "question": "Strategy 패턴에 대해 설명해주세요",
  "answer": "Strategy 패턴은...",
  "contexts": [
    {
      "source": "design_patterns.md",
      "chunk": "Strategy Pattern은...",
      "score": "0.8542"
    }
  ],
  "tool_results": {},
  "plan": ["1) Understand question", "2) Retrieve context"],
  "processing_time": 2.34,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 오류 응답
```json
{
  "error": "QueryProcessingError",
  "message": "쿼리 처리 중 오류가 발생했습니다",
  "details": {
    "error": "LLM 서비스 연결 실패"
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🚀 배포

### Docker 배포
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  agentic-ai:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LLM_PROVIDER=azure
      - AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
      - AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT}
    volumes:
      - ./app/data:/app/app/data
```

### 프로덕션 실행
```bash
# Gunicorn 사용
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 또는 uvicorn 직접
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🔍 모니터링

### 로그 확인
```bash
# 개발 모드에서 로그 확인
python main.py

# 프로덕션에서 로그 확인
tail -f /var/log/agentic-ai.log
```

### 메트릭 수집
```python
# Prometheus 메트릭 추가 (선택사항)
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')
```

## 🛠️ 개발

### 코드 구조
```
app/
├── api/
│   ├── models.py          # Pydantic 모델
│   └── routes/            # API 라우트
│       ├── health.py      # 헬스 체크
│       ├── query.py       # 쿼리 처리
│       ├── documents.py   # 문서 관리
│       └── index.py       # 인덱스 관리
├── core/
│   ├── config.py          # 설정 관리
│   └── exceptions.py      # 커스텀 예외
├── services/              # 비즈니스 로직
│   ├── query_service.py   # 쿼리 처리 서비스
│   └── index_service.py   # 인덱스 관리 서비스
└── ...                    # 기존 모듈들
```

### 테스트
```bash
# API 테스트
python -m pytest tests/

# 특정 엔드포인트 테스트
curl -X GET "http://localhost:8000/api/v1/health"
```

## 🎯 사용 사례

1. **웹 애플리케이션**: React, Vue.js 등과 연동
2. **모바일 앱**: REST API로 모바일 앱과 연동
3. **마이크로서비스**: 다른 서비스와 API 통신
4. **자동화**: 스크립트나 봇과 연동
5. **분석 도구**: 데이터 분석 도구와 연동

이제 Agentic AI 시스템을 REST API로 활용할 수 있습니다! 🚀
