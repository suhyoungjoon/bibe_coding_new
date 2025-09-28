"""
쿼리 처리 서비스
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

from app.graph import build_graph
from app.agents.state import AgentState
from app.core.exceptions import QueryProcessingError, LLMServiceError, ToolExecutionError

logger = logging.getLogger(__name__)

class QueryService:
    """쿼리 처리 서비스"""
    
    def __init__(self):
        self.graph = None
        self.app = None
    
    def _get_graph_app(self):
        """그래프 앱 인스턴스 가져오기"""
        if self.app is None:
            try:
                self.graph = build_graph()
                self.app = self.graph.compile()
                logger.info("LangGraph 앱 초기화 완료")
            except Exception as e:
                logger.error(f"LangGraph 앱 초기화 실패: {e}")
                raise QueryProcessingError(
                    message="쿼리 처리 시스템 초기화 실패",
                    details={"error": str(e)}
                )
        return self.app
    
    async def process_query(
        self,
        question: str,
        include_context: bool = True,
        include_tools: bool = True,
        max_contexts: int = 5
    ) -> Dict[str, Any]:
        """쿼리 처리"""
        try:
            logger.info(f"쿼리 처리 시작: {question[:100]}...")
            
            # 그래프 앱 가져오기
            app = self._get_graph_app()
            
            # 초기 상태 설정
            state: AgentState = {
                "question": question,
                "need_rag": include_context,
                "need_calc": False,  # 자동 감지
                "use_sqlite": False  # 자동 감지
            }
            
            # 쿼리 처리 실행
            result = app.invoke(state, config={"recursion_limit": 10})
            
            # 결과 검증
            if not result:
                raise QueryProcessingError(
                    message="쿼리 처리 결과가 없습니다",
                    details={"question": question}
                )
            
            # 컨텍스트 수 제한
            if "contexts" in result and len(result["contexts"]) > max_contexts:
                result["contexts"] = result["contexts"][:max_contexts]
            
            logger.info(f"쿼리 처리 완료: {len(result.get('contexts', []))}개 컨텍스트")
            return result
            
        except QueryProcessingError:
            raise
        except Exception as e:
            logger.error(f"쿼리 처리 중 오류 발생: {e}")
            raise QueryProcessingError(
                message="쿼리 처리 중 오류가 발생했습니다",
                details={"error": str(e), "question": question}
            )
    
    async def process_simple_query(self, question: str) -> str:
        """간단한 쿼리 처리 (답변만 반환)"""
        try:
            result = await self.process_query(
                question=question,
                include_context=True,
                include_tools=True
            )
            return result.get("final", "답변을 생성할 수 없습니다.")
        except Exception as e:
            logger.error(f"간단한 쿼리 처리 실패: {e}")
            raise QueryProcessingError(
                message="간단한 쿼리 처리 실패",
                details={"error": str(e)}
            )
    
    async def get_query_plan(self, question: str) -> List[str]:
        """쿼리 실행 계획 조회"""
        try:
            result = await self.process_query(
                question=question,
                include_context=False,
                include_tools=False
            )
            return result.get("plan", [])
        except Exception as e:
            logger.error(f"쿼리 계획 조회 실패: {e}")
            raise QueryProcessingError(
                message="쿼리 계획 조회 실패",
                details={"error": str(e)}
            )
    
    async def get_contexts_only(self, question: str, max_contexts: int = 5) -> List[Dict[str, Any]]:
        """컨텍스트만 조회"""
        try:
            result = await self.process_query(
                question=question,
                include_context=True,
                include_tools=False
            )
            contexts = result.get("contexts", [])
            return contexts[:max_contexts]
        except Exception as e:
            logger.error(f"컨텍스트 조회 실패: {e}")
            raise QueryProcessingError(
                message="컨텍스트 조회 실패",
                details={"error": str(e)}
            )
    
    async def execute_tools_only(self, question: str) -> Dict[str, Any]:
        """도구만 실행"""
        try:
            result = await self.process_query(
                question=question,
                include_context=False,
                include_tools=True
            )
            return result.get("tool_results", {})
        except Exception as e:
            logger.error(f"도구 실행 실패: {e}")
            raise ToolExecutionError(
                message="도구 실행 실패",
                details={"error": str(e)}
            )
