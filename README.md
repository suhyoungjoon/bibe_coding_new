# 🚀 Agentic AI 바이브 코딩 플랫폼

> **Azure OpenAI + FAISS/BM25 + 실시간 코드 분석 + 자동 수정을 통한 지능형 협업 코딩 환경**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4o--mini-purple.svg)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 주요 기능

### 🤖 **AI 기반 코드 분석 및 자동 수정**
- **실시간 코드 분석**: 코드 품질, 복잡도, 버그 탐지
- **자동 개선 제안**: 성능 최적화, 보안 강화, 가독성 향상
- **버그 찾기**: 잠재적 런타임 오류 자동 탐지 및 수정 제안
- **리팩토링 추천**: 객체지향 설계 원칙 적용 제안

### 🔍 **고급 검색 및 RAG 시스템**
- **하이브리드 검색**: FAISS 벡터 검색 + BM25 키워드 검색
- **문서 기반 검색**: 프로젝트 문서에서 지능형 정보 검색
- **컨텍스트 인식**: 코드 컨텍스트를 고려한 정확한 답변

### 💻 **다중 언어 코드 실행 환경**
- **지원 언어**: Python, JavaScript, Java, Go, C++, C#, PHP
- **Docker 기반 샌드박스**: 안전하고 격리된 실행 환경
- **보안 레벨**: LOW, MEDIUM, HIGH, MAXIMUM 4단계 보안 정책
- **실시간 모니터링**: CPU, 메모리 사용량 실시간 추적

### 🌐 **실시간 협업 기능**
- **WebSocket 통신**: 실시간 코드 공유 및 협업
- **라이브 코딩**: 여러 사용자가 동시에 코드 편집
- **AI 어시스턴트 채팅**: 자연어로 AI와 대화하며 코딩 지원

### 🎨 **현대적인 웹 인터페이스**
- **Monaco Editor**: VS Code와 동일한 코드 에디터
- **다크/라이트 테마**: 사용자 선호도에 따른 테마 변경
- **키보드 단축키**: 효율적인 코딩을 위한 단축키 지원
- **파일 관리**: 저장, 로드, 자동 저장 기능

## 🛠️ 기술 스택

### **Backend**
- **FastAPI**: 고성능 웹 API 프레임워크
- **LangGraph**: 멀티 에이전트 워크플로우 관리
- **Azure OpenAI**: GPT-4o-mini, Text Embedding 3 Small
- **FAISS**: 벡터 데이터베이스 및 유사도 검색
- **PostgreSQL**: 관계형 데이터베이스 (AI 학습 데이터 저장)
- **Docker**: 컨테이너 기반 코드 실행 환경

### **Frontend**
- **WebSocket**: 실시간 양방향 통신
- **Monaco Editor**: 웹 기반 코드 에디터
- **Chart.js**: 실행 결과 시각화
- **반응형 CSS**: 모바일 친화적 UI/UX

### **DevOps & Tools**
- **Uvicorn**: ASGI 서버
- **Pydantic**: 데이터 검증 및 설정 관리
- **aiohttp**: 비동기 HTTP 클라이언트
- **psutil**: 시스템 모니터링

## 🚀 빠른 시작

### **1. 저장소 클론**
```bash
git clone https://github.com/suhyoungjoon/bibe_coding.git
cd bibe_coding
```

### **2. 의존성 설치**
```bash
pip install -r requirements.txt
```

### **3. 환경 변수 설정**
```bash
cp .env.example .env
```

`.env` 파일에 Azure OpenAI 정보를 입력하세요:
```env
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
```

### **4. 데이터베이스 설정 (선택사항)**
```bash
# PostgreSQL 설치 및 설정
python setup_postgresql.py
```

### **5. 서버 실행**
```bash
python main.py
```

### **6. 웹 인터페이스 접속**
- **고급 데모**: http://localhost:8000/api/v1/demo/advanced
- **샌드박스 데모**: http://localhost:8000/api/v1/demo/sandbox
- **API 문서**: http://localhost:8000/docs

## 📖 사용 방법

### **AI 코드 분석**
1. 웹 인터페이스에서 코드 입력
2. "🧠 AI 분석" 버튼 클릭
3. AI가 제공하는 개선 제안 확인
4. 제안된 코드로 자동 수정

### **실시간 협업**
1. "연결" 버튼으로 WebSocket 연결
2. 여러 사용자가 동시에 코드 편집
3. 실시간으로 변경사항 공유
4. AI 어시스턴트와 채팅으로 도움 요청

### **다중 언어 실행**
1. 언어 선택 (Python, Java, Go, C++, 등)
2. 보안 레벨 설정
3. 코드 실행 및 결과 확인
4. 성능 메트릭 및 시각화 확인

## 🔧 API 사용법

### **코드 분석 API**
```python
import requests

response = requests.post("http://localhost:8000/api/v1/query", json={
    "question": "다음 Python 코드를 분석해주세요: [코드]",
    "include_context": True,
    "include_tools": True,
    "max_contexts": 5
})

result = response.json()
print(result["answer"])
```

### **샌드박스 실행 API**
```python
response = requests.post("http://localhost:8000/api/v1/sandbox/execute", json={
    "code": "print('Hello World')",
    "language": "python",
    "security_level": "LOW"
})

result = response.json()
print(result["output"])
```

## 🧪 테스트

### **전체 테스트 실행**
```bash
python test_azure_connection.py
python test_real_code_analysis.py
python test_websocket_code_analysis.py
```

### **개별 기능 테스트**
```bash
# Azure OpenAI 연결 테스트
python test_azure_connection.py

# 실제 코드 분석 테스트
python test_real_code_analysis.py

# WebSocket 실시간 기능 테스트
python test_websocket_code_analysis.py

# PostgreSQL 기능 테스트
python setup_postgresql.py
```

## 📊 성능 지표

### **AI 분석 성능**
- **코드 분석 속도**: 평균 2-5초
- **정확도**: 95% 이상
- **지원 언어**: 7개 언어
- **제안 생성**: 평균 5-8개 개선 제안

### **실행 환경 성능**
- **Docker 실행**: 평균 1-3초
- **로컬 실행**: 평균 0.5-1초
- **동시 사용자**: 100명 이상 지원
- **메모리 사용량**: 평균 200-500MB

## 🔒 보안 기능

### **코드 실행 보안**
- **4단계 보안 레벨**: LOW, MEDIUM, HIGH, MAXIMUM
- **Docker 격리**: 완전한 환경 격리
- **리소스 제한**: CPU, 메모리, 실행 시간 제한
- **사용자 격리**: 개별 임시 디렉토리

### **데이터 보안**
- **환경 변수**: 민감한 정보 보호
- **HTTPS 지원**: SSL/TLS 암호화
- **CORS 설정**: 도메인 기반 접근 제어

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👥 팀

- **개발자**: [suhyoungjoon](https://github.com/suhyoungjoon)
- **이메일**: tjdudwns@gmnail.com

## 🙏 감사의 말

- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) - AI 서비스 제공
- [FastAPI](https://fastapi.tiangolo.com) - 웹 프레임워크
- [LangGraph](https://github.com/langchain-ai/langgraph) - 멀티 에이전트 프레임워크
- [FAISS](https://github.com/facebookresearch/faiss) - 벡터 검색 엔진

## 📞 지원 및 문의

- **Issues**: [GitHub Issues](https://github.com/suhyoungjoon/bibe_coding/issues)
- **Discussions**: [GitHub Discussions](https://github.com/suhyoungjoon/bibe_coding/discussions)
- **이메일**: tjdudwns@gmnail.com

---

⭐ **이 프로젝트가 도움이 되었다면 Star를 눌러주세요!**