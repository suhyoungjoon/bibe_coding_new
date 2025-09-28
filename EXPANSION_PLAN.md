# 🚀 프로젝트 확장 계획: PostgreSQL + 샌드박스 Agent

## 📋 **현재 상태 분석**

### **기존 아키텍처**
- **데이터베이스**: SQLite (단순한 파일 기반)
- **Agent**: LangGraph 기반 다중 Agent
- **실행 환경**: Docker + 로컬 실행
- **도구**: Calculator, SQLite, Python/Java 실행

### **확장 목표**
1. **PostgreSQL 통합**: 더 강력한 데이터 관리
2. **샌드박스 Agent**: 안전하고 격리된 Agent 실행 환경
3. **확장 가능한 구조**: 미래 기능 추가 용이성

## 🗄️ **PostgreSQL 통합 설계**

### **1. 데이터베이스 스키마 설계**

#### **핵심 테이블들**
```sql
-- 사용자 관리
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- 세션 관리
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    session_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);

-- 문서 관리
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    content TEXT,
    file_type VARCHAR(50),
    file_size INTEGER,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- 코드 실행 기록
CREATE TABLE code_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id),
    code TEXT NOT NULL,
    language VARCHAR(20) NOT NULL,
    execution_mode VARCHAR(20), -- 'docker', 'local', 'sandbox'
    result JSONB,
    execution_time FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent 실행 기록
CREATE TABLE agent_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id),
    agent_type VARCHAR(50) NOT NULL,
    input_data JSONB,
    output_data JSONB,
    execution_time FLOAT,
    sandbox_id VARCHAR(100), -- 샌드박스 식별자
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 채팅 기록
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id),
    user_message TEXT,
    agent_response TEXT,
    message_type VARCHAR(20), -- 'query', 'code', 'analysis'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 인덱스 통계
CREATE TABLE index_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    document_count INTEGER,
    chunk_count INTEGER,
    vector_count INTEGER,
    last_rebuild TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **2. PostgreSQL 연결 설정**

#### **환경 변수 추가**
```env
# PostgreSQL 설정
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=agentic_ai
POSTGRES_USER=agentic_user
POSTGRES_PASSWORD=your_password
POSTGRES_URL=postgresql://agentic_user:your_password@localhost:5432/agentic_ai

# 기존 SQLite (호환성을 위해 유지)
SQLITE_DB=./app/data/demo.db
```

### **3. 데이터베이스 마이그레이션**

#### **SQLite → PostgreSQL 마이그레이션 도구**
```python
# 마이그레이션 스크립트
def migrate_sqlite_to_postgres():
    # SQLite 데이터 읽기
    # PostgreSQL로 변환
    # 데이터 검증
    pass
```

## 🏗️ **샌드박스 Agent 설계**

### **1. 샌드박스 아키텍처**

#### **격리 수준**
- **Level 1**: Docker 컨테이너 (현재 구현됨)
- **Level 2**: Kubernetes Pod
- **Level 3**: VM 기반 샌드박스
- **Level 4**: 하드웨어 기반 격리

#### **Agent 타입별 샌드박스**
```python
class SandboxAgent:
    """샌드박스 기반 Agent 실행"""
    
    def __init__(self, agent_type: str, isolation_level: int = 1):
        self.agent_type = agent_type
        self.isolation_level = isolation_level
        self.sandbox_id = self._create_sandbox()
    
    async def execute_agent(self, input_data: dict) -> dict:
        """Agent를 샌드박스에서 실행"""
        pass
    
    def _create_sandbox(self) -> str:
        """샌드박스 환경 생성"""
        pass
    
    def _cleanup_sandbox(self):
        """샌드박스 정리"""
        pass
```

### **2. Agent 실행 환경**

#### **샌드박스 도구들**
```python
# 새로운 도구들
- Web Scraping Tool (격리된 환경에서)
- File System Tool (제한된 접근)
- Network Tool (화이트리스트 기반)
- Database Tool (읽기 전용 연결)
- ML Model Tool (제한된 리소스)
```

### **3. 보안 및 격리**

#### **보안 정책**
```yaml
sandbox_policies:
  network:
    allowed_hosts: ["api.openai.com", "github.com"]
    blocked_ports: [22, 23, 25, 53]
  
  filesystem:
    read_only: true
    allowed_paths: ["/tmp", "/app/data"]
    blocked_paths: ["/etc", "/home", "/root"]
  
  resources:
    memory_limit: "512MB"
    cpu_limit: "0.5"
    execution_timeout: 30
  
  environment:
    blocked_vars: ["PATH", "HOME", "USER"]
    allowed_vars: ["LANG", "TZ"]
```

## 🔧 **구현 단계별 계획**

### **Phase 1: PostgreSQL 통합 (1-2일)**
1. **PostgreSQL 설치 및 설정**
2. **데이터베이스 스키마 생성**
3. **기존 SQLite 데이터 마이그레이션**
4. **PostgreSQL 연결 모듈 구현**
5. **기본 CRUD 작업 구현**

### **Phase 2: 샌드박스 Agent 기본 구조 (2-3일)**
1. **샌드박스 관리 시스템 구현**
2. **Agent 실행 환경 격리**
3. **기본 보안 정책 적용**
4. **샌드박스 모니터링 시스템**

### **Phase 3: 고급 샌드박스 기능 (3-4일)**
1. **다중 격리 수준 지원**
2. **동적 보안 정책**
3. **샌드박스 성능 최적화**
4. **실시간 모니터링 대시보드**

### **Phase 4: 통합 및 최적화 (2-3일)**
1. **전체 시스템 통합 테스트**
2. **성능 최적화**
3. **보안 감사**
4. **문서화 및 사용자 가이드**

## 🎯 **기대 효과**

### **PostgreSQL 통합**
- ✅ **확장성**: 대용량 데이터 처리
- ✅ **성능**: 복잡한 쿼리 최적화
- ✅ **안정성**: ACID 트랜잭션 보장
- ✅ **분석**: 고급 데이터 분석 기능

### **샌드박스 Agent**
- ✅ **보안**: 격리된 환경에서 안전한 실행
- ✅ **확장성**: 다양한 Agent 타입 지원
- ✅ **모니터링**: 실행 과정 실시간 추적
- ✅ **제어**: 세밀한 리소스 및 권한 관리

## 🚀 **다음 단계**

1. **PostgreSQL 설치 및 설정**
2. **데이터베이스 스키마 구현**
3. **샌드박스 Agent 기본 구조 설계**
4. **마이그레이션 도구 개발**

이 계획으로 진행하시겠습니까?
