촛# 🧪 Agentic AI 테스트 가이드

이 가이드는 Agentic AI 시스템의 모든 기능을 체계적으로 테스트하기 위한 완전한 가이드입니다.

## 📋 목차
1. [환경 설정](#환경-설정)
2. [빠른 테스트](#빠른-테스트)
3. [기능별 테스트](#기능별-테스트)
4. [통합 테스트](#통합-테스트)
5. [문제 해결](#문제-해결)

## 🚀 환경 설정

### 1. 시스템 요구사항
- Python 3.8+
- 가상환경 지원
- Azure OpenAI 계정 (선택사항 - Mock 모드 지원)

### 2. 설치 및 설정
```bash
# 1. 저장소 클론 (이미 완료)
cd /Users/syj/Downloads/agentic-ai-langgraph-azure-v2

# 2. 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 테스트 데이터 준비
python3 create_test_db.py

# 5. 빠른 테스트 실행
python3 quick_test.py
```

### 3. Azure OpenAI 설정 (선택사항)
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-06-01
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
```

## 🔍 빠른 테스트

### 자동 테스트 실행
```bash
python3 quick_test.py
```

이 스크립트는 다음을 자동으로 테스트합니다:
- ✅ 모듈 import
- ✅ 설정 파일
- ✅ 데이터 파일
- ✅ SQLite 데이터베이스
- ✅ LangGraph 빌드
- ✅ LLM 클라이언트
- ✅ 벡터스토어
- ✅ 기본 기능

### 수동 테스트
```bash
# 1. 서버 시작
streamlit run ui/streamlit_app.py

# 2. 브라우저에서 http://localhost:8501 접속
# 3. "🔁 Rebuild FAISS Index" 클릭
# 4. 테스트 질문 입력
```

## 🧪 기능별 테스트

### 1. RAG 검색 테스트

#### 기본 검색
```
질문: Strategy 패턴에 대해 설명해주세요
예상 결과: design_patterns.md에서 Strategy 패턴 정보 검색 및 답변
```

#### 하이브리드 검색
```
질문: 계산기 클래스의 기능을 설명해주세요
예상 결과: Calculator.java에서 클래스 정보 검색 및 답변
```

#### 복합 검색
```
질문: 디자인 패턴과 데이터 분석의 공통점을 찾아주세요
예상 결과: 여러 문서에서 정보를 종합하여 답변
```

### 2. 코드 실행 테스트

#### Python 기본 실행
```
질문: python: print("Hello from Agentic AI!")
예상 결과: "Hello from Agentic AI!" 출력
```

#### Python 데이터 분석
```
질문: python: 
import statistics
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"평균: {statistics.mean(data)}")
print(f"중앙값: {statistics.median(data)}")
예상 결과: 평균과 중앙값 계산 결과 출력
```

#### Java 코드 실행
```
질문: java: 
public class Test {
    public static void main(String[] args) {
        System.out.println("Java 실행 테스트");
        System.out.println("2 + 3 = " + (2 + 3));
    }
}
예상 결과: Java 코드 컴파일 및 실행 결과 출력
```

### 3. 수학 계산 테스트

#### 기본 계산
```
질문: 15 + 25 * 2를 계산해주세요
예상 결과: 65
```

#### 복잡한 수식
```
질문: (100 + 50) * 2 - 75 / 3을 계산해주세요
예상 결과: 275
```

#### 지수 계산
```
질문: 2^10 + 3^3을 계산해주세요
예상 결과: 1051
```

### 4. SQLite 데이터베이스 테스트

#### 기본 조회
```
질문: sql: SELECT * FROM users LIMIT 5
예상 결과: 사용자 데이터 5개 행 출력
```

#### 그룹별 통계
```
질문: query: SELECT department, COUNT(*) as count, AVG(salary) as avg_salary FROM users GROUP BY department
예상 결과: 부서별 사용자 수와 평균 연봉
```

#### 복합 조인 쿼리
```
질문: sql: 
SELECT u.name, u.department, p.name as product_name, o.total_amount
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN products p ON o.product_id = p.id
ORDER BY o.total_amount DESC
LIMIT 3
예상 결과: 상위 3개 주문 정보
```

## 🔄 통합 테스트

### 시나리오 1: 문서 기반 질문 답변
1. **목적**: RAG 시스템의 문서 검색 및 답변 생성 능력 테스트
2. **테스트 질문들**:
   - "Strategy 패턴의 장점을 설명해주세요"
   - "계산기 클래스에서 예외 처리는 어떻게 되어 있나요?"
   - "데이터 분석 모듈의 주요 기능은 무엇인가요?"

### 시나리오 2: 코드 실행 및 검증
1. **목적**: Python/Java 코드 실행 능력 테스트
2. **테스트 질문들**:
   - "python: print('Hello World')"
   - "java: public class Main { public static void main(String[] args) { System.out.println(1+2); } }"

### 시나리오 3: 데이터베이스 분석
1. **목적**: SQLite 도구를 통한 데이터 분석 능력 테스트
2. **테스트 질문들**:
   - "sql: SELECT department, COUNT(*) FROM users GROUP BY department"
   - "query: SELECT p.name, SUM(o.total_amount) FROM products p JOIN orders o ON p.id = o.product_id GROUP BY p.name"

### 시나리오 4: 수학 계산
1. **목적**: 계산기 도구의 수학 연산 능력 테스트
2. **테스트 질문들**:
   - "2 + 3 * 4를 계산해주세요"
   - "(100 + 50) * 2 - 75 / 3을 계산해주세요"

### 시나리오 5: 복합 워크플로우
1. **목적**: 여러 도구를 조합한 복잡한 작업 처리 능력 테스트
2. **테스트 질문들**:
   - "사용자 데이터를 분석하고, 개발팀의 평균 연봉을 계산한 후, 그 결과에 1.1을 곱해주세요"
   - "Strategy 패턴에 대해 설명하고, python으로 간단한 예제를 실행해주세요"

## 🛠️ 문제 해결

### 일반적인 문제들

#### 1. 인덱스 구축 실패
**증상**: "Index build failed" 오류
**해결 방법**:
- `app/data/docs/` 폴더에 문서가 있는지 확인
- 문서 파일이 텍스트 형식인지 확인
- 권한 문제 확인

#### 2. Azure OpenAI 연결 실패
**증상**: Mock 모드로 동작
**해결 방법**:
- `.env` 파일의 API 키와 엔드포인트 확인
- Azure OpenAI 리소스가 활성화되어 있는지 확인
- API 버전이 올바른지 확인

#### 3. 코드 실행 실패
**증상**: Python/Java 코드 실행 오류
**해결 방법**:
- Python/Java 환경이 설치되어 있는지 확인
- 경로 설정 확인
- 권한 문제 확인

#### 4. SQLite 오류
**증상**: 데이터베이스 쿼리 실패
**해결 방법**:
- `app/data/demo.db` 파일이 존재하는지 확인
- `create_test_db.py` 실행하여 데이터베이스 재생성
- 파일 권한 확인

### 디버깅 팁

#### 1. 로그 확인
- Streamlit 콘솔에서 오류 메시지 확인
- "Debug State" 탭에서 전체 상태 확인

#### 2. 단계별 테스트
- 각 기능을 개별적으로 테스트
- `quick_test.py`로 기본 설정 확인

#### 3. 데이터 확인
- "ℹ️ Show Index Stats" 버튼으로 인덱스 상태 확인
- 데이터베이스 파일 크기 확인

## 📊 성능 테스트

### 검색 정확도 테스트
- 다양한 키워드로 검색 테스트
- 하이브리드 검색 vs 단일 검색 비교
- 쿼리 재작성 효과 확인

### 응답 시간 테스트
- 단순 질문 응답 시간
- 복합 워크플로우 응답 시간
- 대용량 문서 처리 시간

### 메모리 사용량 테스트
- 인덱스 크기 확인
- 메모리 사용량 모니터링
- 대용량 데이터 처리 능력

## 🎯 테스트 체크리스트

### 기본 설정
- [ ] 가상환경 활성화
- [ ] 의존성 설치 완료
- [ ] 테스트 데이터 준비
- [ ] 빠른 테스트 통과

### 기능 테스트
- [ ] RAG 검색 테스트
- [ ] Python 코드 실행 테스트
- [ ] Java 코드 실행 테스트
- [ ] 수학 계산 테스트
- [ ] SQLite 쿼리 테스트

### 통합 테스트
- [ ] 복합 워크플로우 테스트
- [ ] 오류 처리 테스트
- [ ] 성능 테스트

### 최종 확인
- [ ] 모든 기능 정상 동작
- [ ] 오류 없이 완료
- [ ] 예상 결과와 일치

## 📈 예상 결과

### RAG 검색 결과
- 관련 문서에서 정보를 검색하여 정확한 답변 제공
- 파일명 인용을 통한 출처 명시
- 하이브리드 검색(FAISS + BM25)을 통한 정확도 향상

### 코드 실행 결과
- Python/Java 코드의 정상 실행
- 실행 결과 출력
- 오류 발생 시 적절한 오류 메시지

### SQLite 쿼리 결과
- 정확한 SQL 쿼리 실행
- 결과 데이터 표시
- 오류 발생 시 오류 메시지

### 수학 계산 결과
- 정확한 수학 연산 수행
- 복잡한 수식 처리
- 연산자 우선순위 준수

## 🎉 완료!

모든 테스트를 통과했다면 Agentic AI 시스템이 정상적으로 설정되었습니다!

### 다음 단계
1. 실제 문서를 `app/data/docs/`에 추가
2. 인덱스 재구축
3. 실제 사용 시나리오 테스트
4. 성능 최적화

이 테스트 가이드를 통해 Agentic AI 시스템의 모든 기능을 체계적으로 검증할 수 있습니다.

