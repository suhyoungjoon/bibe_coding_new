# Agentic AI 테스트 예제 모음

이 문서는 Agentic AI 시스템의 다양한 기능을 테스트하기 위한 예제들을 포함합니다.

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# .env 파일 설정 (Azure OpenAI 설정 필요)
cp .env.example .env
# .env 파일에 Azure OpenAI 정보 입력
```

### 2. 서버 실행
```bash
streamlit run ui/streamlit_app.py
```

### 3. 인덱스 구축
1. 웹 UI에서 "🔁 Rebuild FAISS Index" 버튼 클릭
2. 성공 메시지 확인

## 📝 테스트 예제

### 1. RAG 검색 테스트

#### 기본 질문 답변
```
질문: Strategy 패턴에 대해 설명해주세요
```

#### 하이브리드 검색 테스트
```
질문: 계산기 클래스의 기능을 설명해주세요
```

#### 복합 질문
```
질문: 디자인 패턴 중에서 Strategy 패턴과 Observer 패턴의 차이점을 설명해주세요
```

### 2. 코드 실행 테스트

#### Python 코드 실행
```
질문: python: print("Hello from Agentic AI!")
```

#### Python 데이터 분석
```
질문: python: 
import statistics
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"평균: {statistics.mean(data)}")
print(f"중앙값: {statistics.median(data)}")
print(f"표준편차: {statistics.stdev(data)}")
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
```

### 3. 수학 계산 테스트

#### 기본 계산
```
질문: 15 + 25 * 2를 계산해주세요
```

#### 복잡한 수식
```
질문: (100 + 50) * 2 - 75 / 3을 계산해주세요
```

#### 지수 계산
```
질문: 2^10 + 3^3을 계산해주세요
```

### 4. SQLite 데이터베이스 테스트

#### 기본 조회
```
질문: sql: SELECT * FROM users LIMIT 5
```

#### 그룹별 통계
```
질문: query: SELECT department, COUNT(*) as count, AVG(salary) as avg_salary FROM users GROUP BY department
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
```

#### 제품별 매출 분석
```
질문: query: 
SELECT p.name, COUNT(o.id) as order_count, SUM(o.total_amount) as total_sales
FROM products p
LEFT JOIN orders o ON p.id = o.product_id
GROUP BY p.name
ORDER BY total_sales DESC
```

### 5. 복합 기능 테스트

#### RAG + 코드 실행
```
질문: Strategy 패턴에 대해 설명하고, python: print("Strategy pattern example")를 실행해주세요
```

#### RAG + SQL + 계산
```
질문: 사용자 데이터를 분석하고, sql: SELECT COUNT(*) FROM users를 실행한 후, 결과에 10을 곱해주세요
```

#### 다중 도구 사용
```
질문: 
1. python: print("Python 실행 테스트")
2. java: public class Test { public static void main(String[] args) { System.out.println("Java 실행 테스트"); } }
3. sql: SELECT name, department FROM users WHERE department = '개발팀'
4. 100 * 2 + 50을 계산해주세요
```

## 🔍 테스트 시나리오

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

## 📊 예상 결과

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

## 🛠️ 문제 해결

### 일반적인 문제들
1. **인덱스 구축 실패**: 문서가 `app/data/docs/` 폴더에 있는지 확인
2. **Azure OpenAI 연결 실패**: `.env` 파일의 API 키와 엔드포인트 확인
3. **코드 실행 실패**: Python/Java 환경 설정 확인
4. **SQLite 오류**: 데이터베이스 파일 경로 확인

### 디버깅 팁
- "Debug State" 탭에서 전체 상태 확인
- "Tool Results" 탭에서 도구 실행 결과 확인
- "Contexts" 탭에서 검색된 문서 확인

## 📈 성능 테스트

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

이 테스트 예제들을 통해 Agentic AI 시스템의 모든 주요 기능을 검증할 수 있습니다.

