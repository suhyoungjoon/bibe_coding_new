# 🧪 Agentic AI 테스트 완료 가이드

## ✅ 테스트 결과 요약

모든 기본 기능 테스트가 성공적으로 완료되었습니다!

### 📊 테스트 통과 현황
- ✅ **모듈 Import**: 모든 필수 모듈 정상 로드
- ✅ **설정 파일**: 환경 설정 정상 로드
- ✅ **데이터 파일**: 4개 테스트 문서 준비 완료
- ✅ **SQLite 데이터베이스**: 8명 사용자, 8개 제품, 10건 주문 데이터
- ✅ **LangGraph 빌드**: 멀티 에이전트 워크플로우 정상 구성
- ✅ **LLM 클라이언트**: Mock 모드로 정상 동작 (Azure OpenAI 설정 시 실제 모드)
- ✅ **벡터스토어**: FAISS 인덱스 준비 완료
- ✅ **간단한 기능**: 기본 워크플로우 정상 동작

## 🚀 시스템 실행 방법

### 1. 서버 시작
```bash
cd /Users/syj/Downloads/agentic-ai-langgraph-azure-v2
streamlit run ui/streamlit_app.py
```

### 2. 웹 UI 접속
브라우저에서 `http://localhost:8501` 접속

### 3. 인덱스 구축
웹 UI에서 "🔁 Rebuild FAISS Index" 버튼 클릭

## 🧪 테스트 예제 모음

### 1. RAG 검색 테스트
```
질문: Strategy 패턴에 대해 설명해주세요
예상 결과: design_patterns.md에서 Strategy 패턴 정보 검색 및 답변
```

### 2. 하이브리드 검색 테스트
```
질문: 계산기 클래스의 기능을 설명해주세요
예상 결과: Calculator.java에서 클래스 정보 검색 및 답변
```

### 3. Python 코드 실행 테스트
```
질문: python: print("Hello from Agentic AI!")
예상 결과: "Hello from Agentic AI!" 출력
```

### 4. Java 코드 실행 테스트
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

### 5. 수학 계산 테스트
```
질문: 15 + 25 * 2를 계산해주세요
예상 결과: 65
```

### 6. SQLite 데이터베이스 테스트
```
질문: sql: SELECT * FROM users LIMIT 5
예상 결과: 사용자 데이터 5개 행 출력
```

### 7. 복합 워크플로우 테스트
```
질문: 
1. Strategy 패턴에 대해 설명해주세요
2. python: print("Strategy pattern example")
3. sql: SELECT department, COUNT(*) FROM users GROUP BY department
4. 100 * 2 + 50을 계산해주세요
```

## 📁 준비된 테스트 데이터

### 문서 파일들
- **design_patterns.md**: 디자인 패턴 가이드 (Strategy, Observer, Factory 패턴)
- **Calculator.java**: Java 계산기 클래스 (메서드별 기능 설명)
- **data_analysis.py**: Python 데이터 분석 모듈 (통계 계산 기능)
- **README.txt**: 테스트 문서 설명

### SQLite 데이터베이스
- **users 테이블**: 8명의 사용자 정보 (이름, 이메일, 나이, 부서, 연봉)
- **products 테이블**: 8개 제품 정보 (이름, 카테고리, 가격, 재고)
- **orders 테이블**: 10건의 주문 정보 (사용자-제품-주문 연결)

## 🎯 테스트 시나리오

### 시나리오 1: 기본 RAG 검색
1. "Strategy 패턴의 장점을 설명해주세요"
2. "계산기 클래스에서 예외 처리는 어떻게 되어 있나요?"
3. "데이터 분석 모듈의 주요 기능은 무엇인가요?"

### 시나리오 2: 코드 실행 검증
1. "python: print('Hello World')"
2. "java: public class Main { public static void main(String[] args) { System.out.println(1+2); } }"

### 시나리오 3: 데이터베이스 분석
1. "sql: SELECT department, COUNT(*) FROM users GROUP BY department"
2. "query: SELECT p.name, SUM(o.total_amount) FROM products p JOIN orders o ON p.id = o.product_id GROUP BY p.name"

### 시나리오 4: 수학 계산
1. "2 + 3 * 4를 계산해주세요"
2. "(100 + 50) * 2 - 75 / 3을 계산해주세요"

### 시나리오 5: 복합 워크플로우
1. "사용자 데이터를 분석하고, 개발팀의 평균 연봉을 계산한 후, 그 결과에 1.1을 곱해주세요"
2. "Strategy 패턴에 대해 설명하고, python으로 간단한 예제를 실행해주세요"

## 🔧 문제 해결

### 일반적인 문제들
1. **인덱스 구축 실패**: 문서가 `app/data/docs/` 폴더에 있는지 확인
2. **Azure OpenAI 연결 실패**: `.env` 파일의 API 키와 엔드포인트 확인
3. **코드 실행 실패**: Python/Java 환경 설정 확인
4. **SQLite 오류**: 데이터베이스 파일 경로 확인

### 디버깅 팁
- "Debug State" 탭에서 전체 상태 확인
- "Tool Results" 탭에서 도구 실행 결과 확인
- "Contexts" 탭에서 검색된 문서 확인

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

모든 테스트를 통과했으며, Agentic AI 시스템이 정상적으로 설정되었습니다!

### 다음 단계
1. 실제 문서를 `app/data/docs/`에 추가
2. 인덱스 재구축
3. 실제 사용 시나리오 테스트
4. 성능 최적화

이 테스트 가이드를 통해 Agentic AI 시스템의 모든 주요 기능을 체계적으로 검증할 수 있습니다.

