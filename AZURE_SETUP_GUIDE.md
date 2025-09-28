# 🔧 Azure OpenAI 연결 설정 가이드

## 현재 상태
- ✅ **샌드박스 기능**: 정상 동작 (목업 모드)
- ✅ **다중 언어 실행**: Python, JavaScript, Java, Go 등 지원
- ✅ **실시간 시각화**: 차트, 테이블, 메트릭 등
- ❌ **AI 질의**: 목업 모드 (실제 Azure OpenAI 연결 필요)
- ❌ **RAG 검색**: 목업 모드 (실제 Azure OpenAI 연결 필요)

## Azure OpenAI 연결 설정

### 1. Azure OpenAI 리소스 생성
1. [Azure Portal](https://portal.azure.com)에 로그인
2. "Azure OpenAI" 검색 후 리소스 생성
3. 리소스 그룹, 지역, 가격 책정 계층 선택
4. 배포 모델 선택:
   - **GPT-4o-mini**: 일반적인 질의응답용
   - **text-embedding-3-small**: 벡터 임베딩용

### 2. 모델 배포
1. Azure OpenAI Studio에서 "Deployments" 메뉴
2. 다음 모델들을 배포:
   - `gpt-4o-mini` (GPT-4o Mini)
   - `text-embedding-3-small` (Text Embedding 3 Small)

### 3. 환경 변수 설정

#### 방법 1: .env 파일 생성
```bash
# 프로젝트 루트에 .env 파일 생성
cat > .env << EOF
AZURE_OPENAI_API_KEY=your_actual_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
EOF
```

#### 방법 2: 시스템 환경 변수 설정
```bash
export AZURE_OPENAI_API_KEY="your_actual_api_key_here"
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
export AZURE_OPENAI_API_VERSION="2024-06-01"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o-mini"
export AZURE_OPENAI_EMBEDDING_DEPLOYMENT="text-embedding-3-small"
```

### 4. 연결 테스트

서버 재시작 후 테스트:
```bash
# 서버 재시작
python3 main.py

# 다른 터미널에서 테스트
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "안녕하세요, AI입니다."}'
```

## 현재 작동하는 기능들

### ✅ 샌드박스 기능 (목업 모드에서도 정상 작동)
- **다중 언어 지원**: Python, JavaScript, Java, Go, Rust, C++, C#, PHP
- **실시간 실행**: WebSocket 기반 실시간 코드 실행
- **시각화**: 차트, 테이블, 메트릭 등 실행 결과 시각화
- **보안 레벨**: LOW, MEDIUM, HIGH, MAXIMUM
- **Docker 지원**: 격리된 환경에서 안전한 코드 실행

### 🔗 접근 가능한 데모 페이지
- **향상된 샌드박스**: http://localhost:8000/api/v1/demo/sandbox
- **간단한 샌드박스**: http://localhost:8000/api/v1/demo/sandbox/simple
- **기본 데모**: http://localhost:8000/api/v1/demo/improved

## Azure 연결 후 활성화될 기능들

### 🤖 AI 기능
- **실시간 AI 질의응답**: 자연어로 코드 관련 질문
- **AI 코드 분석**: 코드 품질 분석 및 개선 제안
- **AI 코드 생성**: 자연어 설명을 코드로 변환
- **컨텍스트 인식 제안**: 현재 코드 컨텍스트 기반 제안

### 🔍 RAG 기능
- **문서 검색**: 프로젝트 문서에서 관련 정보 검색
- **지식 베이스**: 문서 기반 지능형 응답
- **하이브리드 검색**: FAISS + BM25 조합 검색

## 비용 고려사항

### Azure OpenAI 가격 (2024년 기준)
- **GPT-4o Mini**: $0.00015/1K 토큰 (입력), $0.0006/1K 토큰 (출력)
- **Text Embedding 3 Small**: $0.00002/1K 토큰

### 예상 월 비용 (개발용)
- 소규모 사용: $5-20
- 중간 규모: $20-100
- 대규모 사용: $100+

## 현재 상태에서도 사용 가능한 기능

Azure 연결 없이도 다음 기능들은 완전히 작동합니다:

1. **코드 실행 환경**: 8개 언어 지원
2. **실시간 시각화**: 실행 결과 차트/테이블
3. **WebSocket 통신**: 실시간 상태 업데이트
4. **보안 샌드박스**: 격리된 코드 실행
5. **파일 관리**: 코드 저장/불러오기
6. **다중 사용자**: 사용자별 격리된 환경

Azure OpenAI 연결은 **AI 질의응답과 RAG 검색** 기능을 활성화하기 위한 것입니다.
