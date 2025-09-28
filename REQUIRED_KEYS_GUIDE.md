# 🔑 필요한 API 키 및 설정 가이드

## 현재 프로젝트에서 필요한 키들

### 1. 🎯 **Azure OpenAI (필수 - AI 기능용)**

#### 필요한 정보:
- **API Key**: Azure OpenAI 리소스의 키
- **Endpoint**: Azure OpenAI 리소스의 엔드포인트 URL
- **Deployment Name**: 배포된 모델의 이름 (2개 필요)

#### 설정 방법:
```bash
# 환경 변수로 설정
export AZURE_OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-06-01"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"
export AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-3-small"
```

#### Azure OpenAI 리소스 생성 단계:
1. [Azure Portal](https://portal.azure.com) → "Azure OpenAI" 검색
2. 리소스 생성 → 지역, 가격 책정 계층 선택
3. Azure OpenAI Studio에서 모델 배포:
   - **gpt-4o-mini** (텍스트 생성용)
   - **text-embedding-3-small** (벡터 임베딩용)

### 2. 🐳 **Docker (선택사항 - 샌드박스 격리용)**

#### 현재 상태:
- ✅ **로컬 실행**: Docker 없이도 모든 기능 작동
- ✅ **Docker 실행**: 더 안전한 격리 환경 제공

#### Docker 설치 (macOS):
```bash
# Docker Desktop 설치
brew install --cask docker
# 또는 https://www.docker.com/products/docker-desktop/ 에서 다운로드
```

### 3. 🗄️ **PostgreSQL (선택사항 - AI 학습 데이터용)**

#### 현재 상태:
- ✅ **SQLite**: 기본 데이터베이스로 작동
- ✅ **PostgreSQL**: AI 학습 및 프로젝트 관리용

#### PostgreSQL 설치 (macOS):
```bash
brew install postgresql@15
brew services start postgresql@15
```

## 🔧 **현재 작동하는 기능들 (키 없이도)**

### ✅ **완전히 작동하는 기능들:**
1. **다중 언어 코드 실행**: Python, JavaScript, Java, Go, Rust, C++, C#, PHP
2. **실시간 시각화**: 차트, 테이블, 메트릭 등
3. **WebSocket 통신**: 실시간 상태 업데이트
4. **보안 샌드박스**: 격리된 코드 실행
5. **파일 관리**: 코드 저장/불러오기
6. **사용자별 격리**: 개별 임시 디렉토리

### 🔗 **접근 가능한 데모 페이지:**
- **향상된 샌드박스**: http://localhost:8000/api/v1/demo/sandbox
- **간단한 샌드박스**: http://localhost:8000/api/v1/demo/sandbox/simple
- **기본 데모**: http://localhost:8000/api/v1/demo/improved

## 📋 **키별 기능 영향도**

### 🎯 **Azure OpenAI 키 (AI 기능용)**
```bash
# 이 키들이 없으면:
❌ AI 질의응답 불가
❌ RAG 검색 불가
❌ AI 코드 분석 불가
❌ 자연어 → 코드 변환 불가

# 이 키들이 있으면:
✅ 모든 AI 기능 활성화
✅ 지능형 코드 제안
✅ 문서 기반 질의응답
✅ 컨텍스트 인식 제안
```

### 🐳 **Docker (샌드박스 격리용)**
```bash
# Docker 없어도:
✅ 모든 언어 코드 실행 가능
✅ 로컬 환경에서 실행

# Docker 있으면:
✅ 더 안전한 격리 환경
✅ 시스템 리소스 보호
✅ 멀티 사용자 안전성 향상
```

### 🗄️ **PostgreSQL (AI 학습용)**
```bash
# SQLite로도:
✅ 기본 기능 모두 작동
✅ 코드 실행 및 시각화

# PostgreSQL 있으면:
✅ AI 학습 데이터 저장
✅ 사용자 패턴 분석
✅ 프로젝트 관리 기능
✅ 버전 관리
```

## 💰 **비용 정보**

### Azure OpenAI 비용 (2024년 기준):
- **GPT-4o Mini**: $0.00015/1K 토큰 (입력), $0.0006/1K 토큰 (출력)
- **Text Embedding 3 Small**: $0.00002/1K 토큰

### 예상 월 비용:
- **개발/테스트**: $5-20
- **중간 규모**: $20-100
- **대규모**: $100+

## 🚀 **권장 설정 순서**

### 1단계: 기본 기능 테스트 (키 없이)
```bash
# 현재 상태에서 테스트
python3 main.py
# http://localhost:8000/api/v1/demo/sandbox 접속
```

### 2단계: Docker 설치 (선택사항)
```bash
# 더 안전한 샌드박스 환경을 원한다면
brew install --cask docker
```

### 3단계: Azure OpenAI 설정 (AI 기능용)
```bash
# AI 기능을 원한다면
export AZURE_OPENAI_API_KEY="your_key"
export AZURE_OPENAI_ENDPOINT="your_endpoint"
python3 main.py
```

### 4단계: PostgreSQL 설정 (고급 기능용)
```bash
# AI 학습 및 프로젝트 관리 기능을 원한다면
brew install postgresql@15
```

## 📊 **현재 시스템 상태 확인**

```bash
# 시스템 상태 확인
curl -s http://localhost:8000/api/v1/health | jq .

# 샌드박스 기능 테스트
curl -X POST "http://localhost:8000/api/v1/sandbox/execute" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello World!\")", "language": "python"}'
```

## 🎯 **결론**

**최소 요구사항**: 없음 (모든 샌드박스 기능 작동)
**권장 설정**: Azure OpenAI 키 (AI 기능 활성화)
**완전한 기능**: Azure OpenAI + Docker + PostgreSQL

현재 상태에서도 모든 샌드박스 기능이 완벽하게 작동합니다! 🚀
