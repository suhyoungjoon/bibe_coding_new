"""
프로젝트 관리 서비스
프로젝트 생성, 파일 관리, 버전 관리, 세션 추적
"""

import json
import hashlib
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.database import db_manager

logger = logging.getLogger(__name__)

class ProjectManagementService:
    """프로젝트 관리 서비스"""
    
    async def create_project(self, name: str, description: str, owner_id: str,
                           project_type: str = 'coding', language: str = 'python',
                           settings: Optional[Dict[str, Any]] = None) -> str:
        """새 프로젝트 생성"""
        try:
            async with db_manager.get_connection() as conn:
                project_id = await conn.fetchval("""
                    INSERT INTO projects (name, description, owner_id, project_type, language, settings)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                """, name, description, owner_id, project_type, language,
                    json.dumps(settings) if settings else None)
                
                logger.info(f"프로젝트 생성 완료: {name} (ID: {project_id})")
                return str(project_id)
                
        except Exception as e:
            logger.error(f"프로젝트 생성 실패: {e}")
            raise
    
    async def get_projects(self, owner_id: str, status: str = 'active') -> List[Dict[str, Any]]:
        """사용자의 프로젝트 목록 조회"""
        try:
            async with db_manager.get_connection() as conn:
                projects = await conn.fetch("""
                    SELECT p.*, 
                           COUNT(pf.id) as file_count,
                           MAX(pf.updated_at) as last_activity
                    FROM projects p
                    LEFT JOIN project_files pf ON p.id = pf.project_id AND pf.is_active = TRUE
                    WHERE p.owner_id = $1 AND p.status = $2
                    GROUP BY p.id
                    ORDER BY p.updated_at DESC
                """, owner_id, status)
                
                result = []
                for project in projects:
                    result.append({
                        'id': str(project['id']),
                        'name': project['name'],
                        'description': project['description'],
                        'project_type': project['project_type'],
                        'language': project['language'],
                        'status': project['status'],
                        'file_count': project['file_count'],
                        'last_activity': project['last_activity'],
                        'created_at': project['created_at'],
                        'settings': json.loads(project['settings']) if project['settings'] else {}
                    })
                
                return result
                
        except Exception as e:
            logger.error(f"프로젝트 목록 조회 실패: {e}")
            return []
    
    async def add_file_to_project(self, project_id: str, file_path: str, content: str,
                                file_type: str, created_by: str) -> str:
        """프로젝트에 파일 추가"""
        try:
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            async with db_manager.get_connection() as conn:
                file_id = await conn.fetchval("""
                    INSERT INTO project_files 
                    (project_id, file_path, file_name, file_type, file_size, content_hash, content, created_by)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (project_id, file_path)
                    DO UPDATE SET content = $7, content_hash = $6, file_size = $5, updated_at = CURRENT_TIMESTAMP
                    RETURNING id
                """, project_id, file_path, file_path.split('/')[-1], file_type,
                    len(content), content_hash, content, created_by)
                
                # 파일 버전 생성
                await self._create_file_version(str(file_id), content, created_by, "파일 추가")
                
                logger.info(f"파일 추가 완료: {file_path} (프로젝트: {project_id})")
                return str(file_id)
                
        except Exception as e:
            logger.error(f"파일 추가 실패: {e}")
            raise
    
    async def update_file(self, file_id: str, content: str, author_id: str,
                         commit_message: str = "파일 수정") -> bool:
        """파일 내용 업데이트"""
        try:
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            async with db_manager.get_connection() as conn:
                # 기존 내용과 비교
                old_content = await conn.fetchval("""
                    SELECT content FROM project_files WHERE id = $1
                """, file_id)
                
                if old_content == content:
                    logger.info("파일 내용이 변경되지 않음")
                    return True
                
                # 파일 업데이트
                await conn.execute("""
                    UPDATE project_files 
                    SET content = $1, content_hash = $2, file_size = $3, updated_at = CURRENT_TIMESTAMP
                    WHERE id = $4
                """, content, content_hash, len(content), file_id)
                
                # 파일 버전 생성
                await self._create_file_version(file_id, content, author_id, commit_message)
                
                logger.info(f"파일 업데이트 완료: {file_id}")
                return True
                
        except Exception as e:
            logger.error(f"파일 업데이트 실패: {e}")
            return False
    
    async def get_project_files(self, project_id: str) -> List[Dict[str, Any]]:
        """프로젝트 파일 목록 조회"""
        try:
            async with db_manager.get_connection() as conn:
                files = await conn.fetch("""
                    SELECT id, file_path, file_name, file_type, file_size, 
                           content_hash, created_by, created_at, updated_at
                    FROM project_files
                    WHERE project_id = $1 AND is_active = TRUE
                    ORDER BY file_path
                """, project_id)
                
                result = []
                for file in files:
                    result.append({
                        'id': str(file['id']),
                        'file_path': file['file_path'],
                        'file_name': file['file_name'],
                        'file_type': file['file_type'],
                        'file_size': file['file_size'],
                        'content_hash': file['content_hash'],
                        'created_by': file['created_by'],
                        'created_at': file['created_at'],
                        'updated_at': file['updated_at']
                    })
                
                return result
                
        except Exception as e:
            logger.error(f"프로젝트 파일 목록 조회 실패: {e}")
            return []
    
    async def get_file_content(self, file_id: str) -> Optional[str]:
        """파일 내용 조회"""
        try:
            async with db_manager.get_connection() as conn:
                content = await conn.fetchval("""
                    SELECT content FROM project_files WHERE id = $1 AND is_active = TRUE
                """, file_id)
                
                return content
                
        except Exception as e:
            logger.error(f"파일 내용 조회 실패: {e}")
            return None
    
    async def get_file_versions(self, file_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """파일 버전 히스토리 조회"""
        try:
            async with db_manager.get_connection() as conn:
                versions = await conn.fetch("""
                    SELECT id, version_number, diff_summary, commit_message, 
                           author_id, created_at
                    FROM file_versions
                    WHERE file_id = $1
                    ORDER BY version_number DESC
                    LIMIT $2
                """, file_id, limit)
                
                result = []
                for version in versions:
                    result.append({
                        'id': str(version['id']),
                        'version_number': version['version_number'],
                        'diff_summary': version['diff_summary'],
                        'commit_message': version['commit_message'],
                        'author_id': version['author_id'],
                        'created_at': version['created_at']
                    })
                
                return result
                
        except Exception as e:
            logger.error(f"파일 버전 히스토리 조회 실패: {e}")
            return []
    
    async def start_coding_session(self, project_id: str, user_id: str, session_name: str,
                                 session_type: str = 'coding') -> str:
        """코딩 세션 시작"""
        try:
            async with db_manager.get_connection() as conn:
                session_id = await conn.fetchval("""
                    INSERT INTO project_sessions 
                    (project_id, session_name, user_id, session_type)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id
                """, project_id, session_name, user_id, session_type)
                
                logger.info(f"코딩 세션 시작: {session_name} (ID: {session_id})")
                return str(session_id)
                
        except Exception as e:
            logger.error(f"코딩 세션 시작 실패: {e}")
            raise
    
    async def end_coding_session(self, session_id: str, activity_summary: Optional[Dict[str, Any]] = None):
        """코딩 세션 종료"""
        try:
            async with db_manager.get_connection() as conn:
                await conn.execute("""
                    UPDATE project_sessions 
                    SET status = 'completed', end_time = CURRENT_TIMESTAMP, activity_summary = $1
                    WHERE id = $2
                """, json.dumps(activity_summary) if activity_summary else None, session_id)
                
                logger.info(f"코딩 세션 종료: {session_id}")
                
        except Exception as e:
            logger.error(f"코딩 세션 종료 실패: {e}")
    
    async def record_session_activity(self, session_id: str, activity_type: str,
                                    activity_data: Dict[str, Any], file_id: Optional[str] = None):
        """세션 활동 기록"""
        try:
            async with db_manager.get_connection() as conn:
                await conn.execute("""
                    INSERT INTO session_activities 
                    (session_id, activity_type, file_id, activity_data)
                    VALUES ($1, $2, $3, $4)
                """, session_id, activity_type, file_id, json.dumps(activity_data))
                
                logger.debug(f"세션 활동 기록: {activity_type} (세션: {session_id})")
                
        except Exception as e:
            logger.error(f"세션 활동 기록 실패: {e}")
    
    async def get_session_activities(self, session_id: str) -> List[Dict[str, Any]]:
        """세션 활동 목록 조회"""
        try:
            async with db_manager.get_connection() as conn:
                activities = await conn.fetch("""
                    SELECT id, activity_type, file_id, activity_data, timestamp
                    FROM session_activities
                    WHERE session_id = $1
                    ORDER BY timestamp DESC
                """, session_id)
                
                result = []
                for activity in activities:
                    result.append({
                        'id': str(activity['id']),
                        'activity_type': activity['activity_type'],
                        'file_id': str(activity['file_id']) if activity['file_id'] else None,
                        'activity_data': json.loads(activity['activity_data']),
                        'timestamp': activity['timestamp']
                    })
                
                return result
                
        except Exception as e:
            logger.error(f"세션 활동 목록 조회 실패: {e}")
            return []
    
    async def get_project_statistics(self, project_id: str) -> Dict[str, Any]:
        """프로젝트 통계 조회"""
        try:
            async with db_manager.get_connection() as conn:
                # 기본 통계
                stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(DISTINCT pf.id) as total_files,
                        SUM(pf.file_size) as total_size,
                        COUNT(DISTINCT ps.id) as total_sessions,
                        MAX(pf.updated_at) as last_activity
                    FROM projects p
                    LEFT JOIN project_files pf ON p.id = pf.project_id AND pf.is_active = TRUE
                    LEFT JOIN project_sessions ps ON p.id = ps.project_id
                    WHERE p.id = $1
                """, project_id)
                
                # 언어별 파일 분포
                language_stats = await conn.fetch("""
                    SELECT file_type, COUNT(*) as count
                    FROM project_files
                    WHERE project_id = $1 AND is_active = TRUE
                    GROUP BY file_type
                    ORDER BY count DESC
                """, project_id)
                
                # 세션별 활동 통계
                session_stats = await conn.fetch("""
                    SELECT 
                        ps.session_type,
                        COUNT(sa.id) as activity_count,
                        AVG(EXTRACT(EPOCH FROM (ps.end_time - ps.start_time))) as avg_duration
                    FROM project_sessions ps
                    LEFT JOIN session_activities sa ON ps.id = sa.session_id
                    WHERE ps.project_id = $1 AND ps.status = 'completed'
                    GROUP BY ps.session_type
                """, project_id)
                
                return {
                    'total_files': stats['total_files'],
                    'total_size': stats['total_size'],
                    'total_sessions': stats['total_sessions'],
                    'last_activity': stats['last_activity'],
                    'file_types': {row['file_type']: row['count'] for row in language_stats},
                    'session_types': {row['session_type']: {
                        'activity_count': row['activity_count'],
                        'avg_duration': row['avg_duration']
                    } for row in session_stats}
                }
                
        except Exception as e:
            logger.error(f"프로젝트 통계 조회 실패: {e}")
            return {}
    
    async def delete_file(self, file_id: str) -> bool:
        """파일 삭제 (소프트 삭제)"""
        try:
            async with db_manager.get_connection() as conn:
                await conn.execute("""
                    UPDATE project_files 
                    SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
                    WHERE id = $1
                """, file_id)
                
                logger.info(f"파일 삭제 완료: {file_id}")
                return True
                
        except Exception as e:
            logger.error(f"파일 삭제 실패: {e}")
            return False
    
    async def _create_file_version(self, file_id: str, content: str, author_id: str, commit_message: str):
        """파일 버전 생성"""
        try:
            async with db_manager.get_connection() as conn:
                # 다음 버전 번호 조회
                version_number = await conn.fetchval("""
                    SELECT COALESCE(MAX(version_number), 0) + 1
                    FROM file_versions
                    WHERE file_id = $1
                """, file_id)
                
                # 간단한 diff 요약 생성
                diff_summary = f"파일 크기: {len(content)} 문자"
                
                await conn.execute("""
                    INSERT INTO file_versions 
                    (file_id, version_number, content, diff_summary, commit_message, author_id)
                    VALUES ($1, $2, $3, $4, $5, $6)
                """, file_id, version_number, content, diff_summary, commit_message, author_id)
                
        except Exception as e:
            logger.error(f"파일 버전 생성 실패: {e}")
    
    async def restore_file_version(self, version_id: str) -> bool:
        """파일 버전 복원"""
        try:
            async with db_manager.get_connection() as conn:
                # 버전 내용 조회
                version_data = await conn.fetchrow("""
                    SELECT fv.content, fv.file_id, fv.commit_message
                    FROM file_versions fv
                    WHERE fv.id = $1
                """, version_id)
                
                if not version_data:
                    return False
                
                # 파일 내용 복원
                content_hash = hashlib.sha256(version_data['content'].encode()).hexdigest()
                await conn.execute("""
                    UPDATE project_files 
                    SET content = $1, content_hash = $2, file_size = $3, updated_at = CURRENT_TIMESTAMP
                    WHERE id = $4
                """, version_data['content'], content_hash, len(version_data['content']), version_data['file_id'])
                
                # 복원 기록을 새 버전으로 생성
                await self._create_file_version(
                    str(version_data['file_id']), 
                    version_data['content'], 
                    'system', 
                    f"버전 복원: {version_data['commit_message']}"
                )
                
                logger.info(f"파일 버전 복원 완료: {version_id}")
                return True
                
        except Exception as e:
            logger.error(f"파일 버전 복원 실패: {e}")
            return False
