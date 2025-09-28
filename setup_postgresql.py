#!/usr/bin/env python3
"""
PostgreSQL 데이터베이스 설정 및 테스트
AI 학습 및 프로젝트 관리 기능 테스트
"""

import asyncio
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.core.database import db_manager
from app.services.ai_learning_service import AILearningService
from app.services.project_management_service import ProjectManagementService
from app.core.config import settings

class PostgreSQLTester:
    """PostgreSQL 기능 테스트"""
    
    def __init__(self):
        self.ai_learning_service = AILearningService()
        self.project_service = ProjectManagementService()
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """테스트 결과 로깅"""
        status = "✅ 성공" if success else "❌ 실패"
        print(f"{status} {test_name}")
        if details:
            print(f"   📝 {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    async def test_database_connection(self):
        """데이터베이스 연결 테스트"""
        print("\n🗄️ PostgreSQL 데이터베이스 연결 테스트")
        
        try:
            # 데이터베이스 초기화
            await db_manager.initialize()
            self.log_test("데이터베이스 초기화", True, "연결 풀 및 스키마 생성 완료")
            
        except Exception as e:
            self.log_test("데이터베이스 초기화", False, f"오류: {str(e)}")
            return False
        
        try:
            # 연결 테스트
            async with db_manager.get_connection() as conn:
                result = await conn.fetchval("SELECT 1")
                if result == 1:
                    self.log_test("데이터베이스 연결", True, "연결 성공")
                    return True
                else:
                    self.log_test("데이터베이스 연결", False, "연결 실패")
                    return False
                    
        except Exception as e:
            self.log_test("데이터베이스 연결", False, f"오류: {str(e)}")
            return False
    
    async def test_project_management(self):
        """프로젝트 관리 기능 테스트"""
        print("\n📁 프로젝트 관리 기능 테스트")
        
        try:
            # 프로젝트 생성
            project_id = await self.project_service.create_project(
                name="테스트 프로젝트",
                description="PostgreSQL 기능 테스트용 프로젝트",
                owner_id="test_user"
            )
            
            if project_id:
                self.log_test("프로젝트 생성", True, f"프로젝트 ID: {project_id}")
            else:
                self.log_test("프로젝트 생성", False, "프로젝트 생성 실패")
                return
            
            # 파일 추가
            file_id = await self.project_service.add_file_to_project(
                project_id=project_id,
                file_path="test.py",
                content="# 테스트 파일\nprint('Hello PostgreSQL!')\n",
                file_type="python",
                created_by="test_user"
            )
            
            if file_id:
                self.log_test("파일 추가", True, f"파일 ID: {file_id}")
            else:
                self.log_test("파일 추가", False, "파일 추가 실패")
                return
            
            # 파일 업데이트 (새 버전 생성)
            updated = await self.project_service.update_file(
                file_id=file_id,
                content="# 업데이트된 테스트 파일\nprint('Hello PostgreSQL v2!')\n",
                author_id="test_user"
            )
            
            if updated:
                self.log_test("파일 업데이트", True, "새 버전 생성 완료")
            else:
                self.log_test("파일 업데이트", False, "파일 업데이트 실패")
            
            # 프로젝트 목록 조회
            projects = await self.project_service.get_projects("test_user")
            if projects:
                self.log_test("프로젝트 목록 조회", True, f"{len(projects)}개 프로젝트")
            else:
                self.log_test("프로젝트 목록 조회", False, "목록 조회 실패")
            
            # 파일 목록 조회
            files = await self.project_service.get_project_files(project_id)
            if files:
                self.log_test("파일 목록 조회", True, f"{len(files)}개 파일")
            else:
                self.log_test("파일 목록 조회", False, "파일 목록 조회 실패")
                
        except Exception as e:
            self.log_test("프로젝트 관리 테스트", False, f"예외: {str(e)}")
    
    async def test_ai_learning(self):
        """AI 학습 기능 테스트"""
        print("\n🤖 AI 학습 기능 테스트")
        
        try:
            # AI 학습 세션 기록
            session_id = await self.ai_learning_service.record_learning_session(
                user_id="test_user",
                learning_type="code_analysis",
                input_data={
                    "code": "for i in range(10):\n    print(i)",
                    "language": "python"
                },
                ai_response={
                    "suggestions": ["f-string 사용 권장"],
                    "confidence": 0.8
                },
                user_feedback={
                    "rating": 5,
                    "comment": "매우 유용한 제안이었습니다!"
                }
            )
            
            if session_id:
                self.log_test("AI 학습 세션 기록", True, f"세션 ID: {session_id}")
            else:
                self.log_test("AI 학습 세션 기록", False, "세션 기록 실패")
            
            # 사용자 패턴 조회
            patterns = await self.ai_learning_service.get_user_patterns("test_user")
            if patterns:
                self.log_test("사용자 패턴 조회", True, "패턴 데이터 조회 성공")
            else:
                self.log_test("사용자 패턴 조회", False, "패턴 조회 실패")
            
            # 개인화된 제안 생성
            suggestions = await self.ai_learning_service.get_personalized_suggestions(
                user_id="test_user",
                context={
                    "code": "print('hello')",
                    "language": "python"
                }
            )
            
            if suggestions:
                self.log_test("개인화된 제안 생성", True, f"{len(suggestions)}개 제안")
            else:
                self.log_test("개인화된 제안 생성", False, "제안 생성 실패")
            
            # 코딩 스타일 분석
            style_analysis = await self.ai_learning_service.analyze_coding_style(
                user_id="test_user",
                code_samples=[
                    "def hello():\n    print('Hello')\n",
                    "for i in range(5):\n    print(i)"
                ]
            )
            
            if style_analysis:
                self.log_test("코딩 스타일 분석", True, "스타일 분석 완료")
            else:
                self.log_test("코딩 스타일 분석", False, "스타일 분석 실패")
                
        except Exception as e:
            self.log_test("AI 학습 테스트", False, f"예외: {str(e)}")
    
    async def test_coding_session(self):
        """코딩 세션 관리 테스트"""
        print("\n💻 코딩 세션 관리 테스트")
        
        try:
            # 제안 피드백 기록 (유효한 UUID 사용)
            import uuid
            suggestion_id = str(uuid.uuid4())
            await self.ai_learning_service.record_suggestion_feedback(
                user_id="test_user",
                suggestion_id=suggestion_id,
                is_accepted=True,
                feedback_rating=5,
                modifications="매우 유용한 제안이었습니다!"
            )
            
            self.log_test("제안 피드백 기록", True, "피드백 기록 완료")
            
            # 추가 학습 세션 기록
            session_id2 = await self.ai_learning_service.record_learning_session(
                user_id="test_user",
                learning_type="code_generation",
                input_data={
                    "prompt": "리스트를 정렬하는 함수를 만들어주세요",
                    "language": "python"
                },
                ai_response={
                    "generated_code": "def sort_list(lst):\n    return sorted(lst)",
                    "confidence": 0.9
                }
            )
            
            if session_id2:
                self.log_test("추가 학습 세션 기록", True, f"세션 ID: {session_id2}")
            else:
                self.log_test("추가 학습 세션 기록", False, "세션 기록 실패")
                
        except Exception as e:
            self.log_test("코딩 세션 테스트", False, f"예외: {str(e)}")
    
    async def run_all_tests(self):
        """모든 테스트 실행"""
        print("🚀 PostgreSQL 기능 테스트 시작")
        print("=" * 50)
        
        # 데이터베이스 연결 테스트
        db_connected = await self.test_database_connection()
        
        if db_connected:
            # 기능 테스트들
            await self.test_project_management()
            await self.test_ai_learning()
            await self.test_coding_session()
        else:
            print("❌ 데이터베이스 연결 실패로 인해 추가 테스트를 건너뜁니다.")
        
        # 결과 요약
        print("\n" + "=" * 50)
        print("📊 PostgreSQL 기능 테스트 결과 요약")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - successful_tests
        
        print(f"총 테스트: {total_tests}개")
        print(f"성공: {successful_tests}개")
        print(f"실패: {failed_tests}개")
        print(f"성공률: {(successful_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ 실패한 테스트:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        print("\n🎯 PostgreSQL 기능 테스트 완료!")
        return successful_tests == total_tests

async def main():
    """메인 함수"""
    tester = PostgreSQLTester()
    success = await tester.run_all_tests()
    return success

if __name__ == "__main__":
    asyncio.run(main())
