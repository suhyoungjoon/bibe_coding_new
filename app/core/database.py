"""
PostgreSQL 데이터베이스 연결 및 설정
AI 학습 및 프로젝트 관리 전용
"""

import os
import asyncpg
import logging
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)

class DatabaseManager:
    """PostgreSQL 데이터베이스 관리자"""
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self._connection_params = self._get_connection_params()
    
    def _get_connection_params(self) -> Dict[str, Any]:
        """데이터베이스 연결 파라미터 가져오기"""
        return {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': int(os.getenv('POSTGRES_PORT', '5432')),
            'database': os.getenv('POSTGRES_DB', 'agentic_ai'),
            'user': os.getenv('POSTGRES_USER', 'agentic_user'),
            'password': os.getenv('POSTGRES_PASSWORD', 'password'),
            'min_size': 1,
            'max_size': 10,
        }
    
    async def initialize(self):
        """데이터베이스 연결 풀 초기화"""
        try:
            self.pool = await asyncpg.create_pool(**self._connection_params)
            logger.info("PostgreSQL 연결 풀 초기화 성공")
            
            # 스키마 생성
            await self._create_schemas()
            
        except Exception as e:
            logger.error(f"PostgreSQL 연결 실패: {e}")
            raise
    
    async def close(self):
        """데이터베이스 연결 풀 종료"""
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL 연결 풀 종료")
    
    async def _create_schemas(self):
        """AI 학습 및 프로젝트 관리 스키마 생성"""
        async with self.pool.acquire() as conn:
            # AI 학습 관련 테이블
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_learning_sessions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id VARCHAR(100) NOT NULL,
                    session_name VARCHAR(100),
                    learning_type VARCHAR(50) NOT NULL, -- 'coding_pattern', 'error_analysis', 'preference_learning'
                    input_data JSONB NOT NULL,
                    ai_response JSONB,
                    user_feedback JSONB, -- 사용자 피드백 (좋음/나쁨, 수정사항 등)
                    learning_score FLOAT, -- 학습 효과 점수
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS user_coding_patterns (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id VARCHAR(100) NOT NULL,
                    pattern_type VARCHAR(50) NOT NULL, -- 'naming_style', 'code_structure', 'error_pattern'
                    pattern_data JSONB NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    confidence_score FLOAT DEFAULT 0.5,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, pattern_type)
                );
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_suggestions_history (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id VARCHAR(100) NOT NULL,
                    session_id UUID,
                    suggestion_type VARCHAR(50) NOT NULL, -- 'code_completion', 'bug_fix', 'optimization'
                    original_code TEXT,
                    suggested_code TEXT,
                    explanation TEXT,
                    confidence_score FLOAT,
                    is_accepted BOOLEAN,
                    is_implemented BOOLEAN,
                    user_modifications TEXT, -- 사용자가 수정한 부분
                    feedback_rating INTEGER, -- 1-5 점수
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # 프로젝트 관리 관련 테이블
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    owner_id VARCHAR(100) NOT NULL,
                    project_type VARCHAR(50) DEFAULT 'coding', -- 'coding', 'data_analysis', 'web_app'
                    language VARCHAR(20), -- 주요 언어
                    status VARCHAR(20) DEFAULT 'active', -- 'active', 'archived', 'deleted'
                    settings JSONB, -- 프로젝트 설정
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS project_files (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
                    file_path VARCHAR(500) NOT NULL,
                    file_name VARCHAR(255) NOT NULL,
                    file_type VARCHAR(50),
                    file_size INTEGER,
                    content_hash VARCHAR(64),
                    content TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_by VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(project_id, file_path)
                );
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS file_versions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    file_id UUID REFERENCES project_files(id) ON DELETE CASCADE,
                    version_number INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    diff_summary TEXT, -- 변경사항 요약
                    commit_message TEXT,
                    author_id VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS project_sessions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
                    session_name VARCHAR(100),
                    user_id VARCHAR(100) NOT NULL,
                    session_type VARCHAR(50) DEFAULT 'coding', -- 'coding', 'debugging', 'review'
                    status VARCHAR(20) DEFAULT 'active', -- 'active', 'paused', 'completed'
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    activity_summary JSONB, -- 세션 활동 요약
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS session_activities (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    session_id UUID REFERENCES project_sessions(id) ON DELETE CASCADE,
                    activity_type VARCHAR(50) NOT NULL, -- 'file_edit', 'code_execution', 'ai_interaction'
                    file_id UUID REFERENCES project_files(id),
                    activity_data JSONB NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # 인덱스 생성
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_ai_learning_user_id ON ai_learning_sessions(user_id);
                CREATE INDEX IF NOT EXISTS idx_ai_learning_type ON ai_learning_sessions(learning_type);
                CREATE INDEX IF NOT EXISTS idx_user_patterns_user_id ON user_coding_patterns(user_id);
                CREATE INDEX IF NOT EXISTS idx_suggestions_user_id ON ai_suggestions_history(user_id);
                CREATE INDEX IF NOT EXISTS idx_projects_owner_id ON projects(owner_id);
                CREATE INDEX IF NOT EXISTS idx_project_files_project_id ON project_files(project_id);
                CREATE INDEX IF NOT EXISTS idx_file_versions_file_id ON file_versions(file_id);
                CREATE INDEX IF NOT EXISTS idx_project_sessions_project_id ON project_sessions(project_id);
                CREATE INDEX IF NOT EXISTS idx_session_activities_session_id ON session_activities(session_id);
            """)
            
            logger.info("AI 학습 및 프로젝트 관리 스키마 생성 완료")
    
    @asynccontextmanager
    async def get_connection(self):
        """데이터베이스 연결 컨텍스트 매니저"""
        if not self.pool:
            raise RuntimeError("데이터베이스가 초기화되지 않았습니다")
        
        async with self.pool.acquire() as conn:
            yield conn

# 전역 데이터베이스 매니저 인스턴스
db_manager = DatabaseManager()
