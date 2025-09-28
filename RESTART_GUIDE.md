# 🔄 컴퓨터 재기동 후 시작 가이드

## 🚀 빠른 시작 (5분)

### 1. 프로젝트 디렉토리로 이동
```bash
cd /Users/syj/Downloads/agentic-ai-langgraph-azure-v2
```

### 2. PostgreSQL 서비스 시작
```bash
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
brew services start postgresql@15
```

### 3. 의존성 확인 및 설치
```bash
pip3 install psutil
```

### 4. FastAPI 서버 시작
```bash
python3 main.py
```

### 5. 브라우저에서 확인
- **API 문서**: http://localhost:8000/docs
- **샌드박스 API**: http://localhost:8000/api/v1/sandbox/

## 🧪 기능 테스트

### 샌드박스 기능 테스트
```bash
python3 test_enhanced_sandbox.py
```

### PostgreSQL 연결 테스트
```bash
python3 simple_db_test.py
```

### AI 학습 & 프로젝트 관리 테스트
```bash
python3 test_ai_learning_project.py
```

## 📊 현재 구현된 기능들

### ✅ 완료된 기능
1. **FastAPI REST API**: 모든 기존 기능 API화
2. **WebSocket 실시간 통신**: 라이브 코딩 지원
3. **AI 코딩 어시스턴트**: 코드 분석, 제안, 대화
4. **향상된 샌드박스**: 8개 언어, 4단계 보안, 모니터링
5. **PostgreSQL 통합**: AI 학습 & 프로젝트 관리 준비
6. **파일 작업**: 저장, 로드, 실행 모드 선택

### 🔄 진행 중인 기능
1. **AI 학습 서비스**: 데이터베이스 모델 정의 필요
2. **프로젝트 관리 서비스**: 실제 DB 연동 구현 필요

## 🎯 다음 작업 우선순위

### 높음
1. **AI 학습 DB 모델 구현**
2. **프로젝트 관리 DB 연동**
3. **Java 실행 환경 개선**

### 중간
1. **웹 UI에서 샌드박스 API 연동**
2. **실시간 코드 실행 상태 표시**
3. **Monaco Editor 통합**

### 낮음
1. **Phase 3 기능 구현**
2. **성능 최적화**
3. **클라우드 배포**

## 🔧 문제 해결

### PostgreSQL 연결 오류
```bash
# 서비스 상태 확인
brew services list | grep postgresql

# 수동 시작
/opt/homebrew/opt/postgresql@15/bin/postgres -D /opt/homebrew/var/postgresql@15
```

### Docker 관련 오류
```bash
# Docker 상태 확인
docker ps

# Docker 서비스 시작 (필요시)
open -a Docker
```

### 포트 충돌
```bash
# 포트 사용 확인
lsof -ti:8000

# 프로세스 종료
lsof -ti:8000 | xargs kill -9
```

## 📚 주요 파일 위치

### API 엔드포인트
- `main.py` - FastAPI 메인 애플리케이션
- `app/api/routes/` - API 라우터들
- `app/api/routes/sandbox.py` - 샌드박스 API

### 서비스
- `app/services/enhanced_sandbox_service.py` - 향상된 샌드박스
- `app/services/ai_learning_service.py` - AI 학습 서비스
- `app/services/project_management_service.py` - 프로젝트 관리

### 설정
- `app/core/config.py` - 프로젝트 설정
- `requirements.txt` - Python 의존성
- `app/core/database.py` - PostgreSQL 연결

### 테스트
- `test_enhanced_sandbox.py` - 샌드박스 테스트
- `test_ai_learning_project.py` - AI 학습 테스트
- `simple_db_test.py` - PostgreSQL 테스트

---

**재기동 후 위 단계를 따라 진행하시면 모든 기능이 정상 작동합니다!** 🎉

