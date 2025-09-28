"""
인터랙티브 AI 어시스턴트 서비스
실시간 대화형 코딩 어시스턴트
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import json

from ..llm import LLMClient
from .ai_coding_assistant import AICodingAssistant

logger = logging.getLogger(__name__)

class InteractiveAssistant:
    """인터랙티브 AI 어시스턴트"""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.ai_coding_assistant = AICodingAssistant()
        self.conversation_sessions = {}  # 세션별 대화 기록
        self.code_snapshots = {}  # 코드 스냅샷 저장
    
    async def process_user_message(
        self, 
        message: str, 
        user_id: str, 
        current_code: str = None, 
        file_path: str = None,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """사용자 메시지 처리"""
        try:
            # 세션 초기화
            if user_id not in self.conversation_sessions:
                self.conversation_sessions[user_id] = {
                    "messages": [],
                    "code_history": [],
                    "current_context": {},
                    "created_at": datetime.now()
                }
            
            session = self.conversation_sessions[user_id]
            
            # 메시지 저장
            session["messages"].append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat()
            })
            
            # 컨텍스트 업데이트
            if current_code:
                session["current_context"]["current_code"] = current_code
                session["current_context"]["file_path"] = file_path
                
                # 코드 히스토리 저장
                session["code_history"].append({
                    "code": current_code,
                    "file_path": file_path,
                    "timestamp": datetime.now().isoformat()
                })
            
            # 추가 컨텍스트 저장
            if context:
                session["current_context"].update(context)
            
            # 메시지 유형 분석
            message_type = await self._analyze_message_type(message, current_code)
            
            # 유형별 처리
            if message_type == "code_question":
                response = await self._handle_code_question(message, user_id, session)
            elif message_type == "code_request":
                response = await self._handle_code_request(message, user_id, session)
            elif message_type == "debug_help":
                response = await self._handle_debug_help(message, user_id, session)
            elif message_type == "refactor_request":
                response = await self._handle_refactor_request(message, user_id, session)
            elif message_type == "explanation_request":
                response = await self._handle_explanation_request(message, user_id, session)
            else:
                response = await self._handle_general_conversation(message, user_id, session)
            
            # 응답 저장
            session["messages"].append({
                "role": "assistant",
                "content": response["content"],
                "type": message_type,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "response": response,
                "message_type": message_type,
                "session_id": user_id,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"메시지 처리 실패: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _analyze_message_type(self, message: str, current_code: str = None) -> str:
        """메시지 유형 분석"""
        try:
            prompt = f"""
다음 사용자 메시지의 유형을 분석해주세요:

메시지: "{message}"

현재 코드가 있는 경우:
{current_code[:200] + "..." if current_code and len(current_code) > 200 else current_code or "없음"}

다음 유형 중 하나로 분류해주세요:
1. code_question - 코드에 대한 질문
2. code_request - 코드 작성 요청
3. debug_help - 디버깅 도움 요청
4. refactor_request - 리팩토링 요청
5. explanation_request - 코드 설명 요청
6. general_conversation - 일반 대화

JSON 형식으로 응답:
{{"type": "분류된_유형", "confidence": 0.9, "reasoning": "분류 이유"}}
"""
            
            response = await self._call_llm(prompt, self._get_classification_system_prompt())
            result = self._parse_ai_response(response)
            
            return result.get("type", "general_conversation")
            
        except Exception as e:
            logger.error(f"메시지 유형 분석 실패: {e}")
            return "general_conversation"
    
    async def _handle_code_question(self, message: str, user_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """코드 질문 처리"""
        try:
            current_code = session["current_context"].get("current_code", "")
            file_path = session["current_context"].get("file_path", "")
            
            prompt = f"""
사용자가 코드에 대해 질문했습니다:

질문: "{message}"

현재 코드:
```python
{current_code}
```

파일: {file_path}

질문에 대해 정확하고 도움이 되는 답변을 제공해주세요. 
코드의 특정 부분을 참조하고, 예시나 개선 제안이 있다면 포함하세요.

응답 형식:
{{
    "content": "답변 내용",
    "code_examples": ["관련 코드 예시들"],
    "suggestions": ["개선 제안들"],
    "references": ["참조할 코드 라인들"]
}}
"""
            
            response = await self._call_llm(prompt, self._get_code_question_system_prompt())
            result = self._parse_ai_response(response)
            
            return {
                "content": result.get("content", "코드에 대한 질문을 이해하지 못했습니다."),
                "code_examples": result.get("code_examples", []),
                "suggestions": result.get("suggestions", []),
                "references": result.get("references", []),
                "type": "code_question_response"
            }
            
        except Exception as e:
            logger.error(f"코드 질문 처리 실패: {e}")
            return {"content": f"질문 처리 중 오류가 발생했습니다: {str(e)}", "type": "error"}
    
    async def _handle_code_request(self, message: str, user_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """코드 작성 요청 처리"""
        try:
            current_code = session["current_context"].get("current_code", "")
            file_path = session["current_context"].get("file_path", "")
            
            prompt = f"""
사용자가 코드 작성을 요청했습니다:

요청: "{message}"

현재 코드 컨텍스트:
```python
{current_code}
```

파일: {file_path}

요청에 맞는 코드를 작성해주세요. 다음을 포함하세요:
1. 요청사항을 정확히 구현한 코드
2. 주석과 문서화
3. 오류 처리
4. 사용 예시

응답 형식:
{{
    "content": "코드 작성 완료 설명",
    "generated_code": "생성된 코드",
    "explanation": "코드 설명",
    "usage_example": "사용 예시",
    "integration_notes": "기존 코드와의 통합 방법"
}}
"""
            
            response = await self._call_llm(prompt, self._get_code_request_system_prompt())
            result = self._parse_ai_response(response)
            
            return {
                "content": result.get("content", "코드 생성이 완료되었습니다."),
                "generated_code": result.get("generated_code", ""),
                "explanation": result.get("explanation", ""),
                "usage_example": result.get("usage_example", ""),
                "integration_notes": result.get("integration_notes", ""),
                "type": "code_generation_response"
            }
            
        except Exception as e:
            logger.error(f"코드 요청 처리 실패: {e}")
            return {"content": f"코드 생성 중 오류가 발생했습니다: {str(e)}", "type": "error"}
    
    async def _handle_debug_help(self, message: str, user_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """디버깅 도움 처리"""
        try:
            current_code = session["current_context"].get("current_code", "")
            file_path = session["current_context"].get("file_path", "")
            
            prompt = f"""
사용자가 디버깅 도움을 요청했습니다:

요청: "{message}"

문제가 있는 코드:
```python
{current_code}
```

파일: {file_path}

디버깅을 도와주세요:
1. 잠재적인 문제점 식별
2. 디버깅 방법 제안
3. 수정된 코드 제공
4. 예방 방법 제안

응답 형식:
{{
    "content": "디버깅 도움 설명",
    "issues_found": ["발견된 문제들"],
    "debugging_steps": ["디버깅 단계들"],
    "fixed_code": "수정된 코드",
    "prevention_tips": ["예방 팁들"]
}}
"""
            
            response = await self._call_llm(prompt, self._get_debug_system_prompt())
            result = self._parse_ai_response(response)
            
            return {
                "content": result.get("content", "디버깅 도움을 제공했습니다."),
                "issues_found": result.get("issues_found", []),
                "debugging_steps": result.get("debugging_steps", []),
                "fixed_code": result.get("fixed_code", ""),
                "prevention_tips": result.get("prevention_tips", []),
                "type": "debug_response"
            }
            
        except Exception as e:
            logger.error(f"디버깅 처리 실패: {e}")
            return {"content": f"디버깅 처리 중 오류가 발생했습니다: {str(e)}", "type": "error"}
    
    async def _handle_refactor_request(self, message: str, user_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """리팩토링 요청 처리"""
        try:
            current_code = session["current_context"].get("current_code", "")
            file_path = session["current_context"].get("file_path", "")
            
            # AI 코딩 어시스턴트를 통한 분석
            analysis_result = await self.ai_coding_assistant.analyze_and_suggest(current_code, file_path, user_id)
            
            prompt = f"""
사용자가 리팩토링을 요청했습니다:

요청: "{message}"

현재 코드:
```python
{current_code}
```

AI 분석 결과:
{json.dumps(analysis_result.get('ai_analysis', {}), indent=2, ensure_ascii=False)}

리팩토링 제안을 해주세요:
1. 코드 개선점 식별
2. 리팩토링 계획 수립
3. 개선된 코드 제공
4. 개선 효과 설명

응답 형식:
{{
    "content": "리팩토링 완료 설명",
    "refactored_code": "리팩토링된 코드",
    "improvements": ["개선사항들"],
    "refactoring_plan": ["리팩토링 계획"],
    "benefits": ["개선 효과들"]
}}
"""
            
            response = await self._call_llm(prompt, self._get_refactor_system_prompt())
            result = self._parse_ai_response(response)
            
            return {
                "content": result.get("content", "리팩토링이 완료되었습니다."),
                "refactored_code": result.get("refactored_code", ""),
                "improvements": result.get("improvements", []),
                "refactoring_plan": result.get("refactoring_plan", []),
                "benefits": result.get("benefits", []),
                "type": "refactor_response"
            }
            
        except Exception as e:
            logger.error(f"리팩토링 처리 실패: {e}")
            return {"content": f"리팩토링 처리 중 오류가 발생했습니다: {str(e)}", "type": "error"}
    
    async def _handle_explanation_request(self, message: str, user_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """코드 설명 요청 처리"""
        try:
            current_code = session["current_context"].get("current_code", "")
            file_path = session["current_context"].get("file_path", "")
            
            prompt = f"""
사용자가 코드 설명을 요청했습니다:

요청: "{message}"

설명할 코드:
```python
{current_code}
```

파일: {file_path}

코드를 자세히 설명해주세요:
1. 전체적인 목적과 기능
2. 주요 구성 요소들
3. 알고리즘과 로직 설명
4. 중요한 부분 강조

응답 형식:
{{
    "content": "코드 설명",
    "overview": "전체 개요",
    "components": ["주요 구성 요소들"],
    "logic_flow": "로직 흐름 설명",
    "key_points": ["중요한 포인트들"]
}}
"""
            
            response = await self._call_llm(prompt, self._get_explanation_system_prompt())
            result = self._parse_ai_response(response)
            
            return {
                "content": result.get("content", "코드 설명을 제공했습니다."),
                "overview": result.get("overview", ""),
                "components": result.get("components", []),
                "logic_flow": result.get("logic_flow", ""),
                "key_points": result.get("key_points", []),
                "type": "explanation_response"
            }
            
        except Exception as e:
            logger.error(f"설명 처리 실패: {e}")
            return {"content": f"설명 처리 중 오류가 발생했습니다: {str(e)}", "type": "error"}
    
    async def _handle_general_conversation(self, message: str, user_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """일반 대화 처리"""
        try:
            # 대화 히스토리 포함
            recent_messages = session["messages"][-5:]  # 최근 5개 메시지
            
            prompt = f"""
사용자와의 일반 대화를 처리해주세요:

현재 메시지: "{message}"

최근 대화 히스토리:
{self._format_message_history(recent_messages)}

현재 작업 컨텍스트:
- 파일: {session["current_context"].get("file_path", "없음")}
- 코드 길이: {len(session["current_context"].get("current_code", ""))} 문자

도움이 되고 친근한 답변을 제공해주세요.

응답 형식:
{{
    "content": "대화 응답",
    "suggestions": ["도움 제안들"],
    "follow_up_questions": ["후속 질문들"]
}}
"""
            
            response = await self._call_llm(prompt, self._get_conversation_system_prompt())
            result = self._parse_ai_response(response)
            
            return {
                "content": result.get("content", "안녕하세요! 코딩을 도와드릴게요."),
                "suggestions": result.get("suggestions", []),
                "follow_up_questions": result.get("follow_up_questions", []),
                "type": "conversation_response"
            }
            
        except Exception as e:
            logger.error(f"일반 대화 처리 실패: {e}")
            return {"content": "죄송합니다. 잠시 문제가 있었습니다.", "type": "error"}
    
    def _format_message_history(self, messages: List[Dict[str, Any]]) -> str:
        """메시지 히스토리 포맷팅"""
        formatted = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:100]  # 처음 100자만
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)
    
    async def _call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """LLM 호출"""
        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.llm_client.chat(messages, system=system_prompt)
            return response
        except Exception as e:
            logger.error(f"LLM 호출 실패: {e}")
            return f"응답 생성 실패: {str(e)}"
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """AI 응답 파싱 (개선된 버전)"""
        try:
            import json
            import re
            
            # JSON 블록 찾기
            json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
            json_match = re.search(json_pattern, response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1)
            else:
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response[json_start:json_end]
                else:
                    # JSON이 없는 경우 구조화된 응답 생성
                    return self._create_structured_conversation_response(response)
            
            # JSON 파싱
            parsed = json.loads(json_str)
            return parsed
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON 파싱 실패, 구조화된 응답 생성: {e}")
            return self._create_structured_conversation_response(response)
        except Exception as e:
            logger.error(f"응답 파싱 실패: {e}")
            return self._create_structured_conversation_response(response)
    
    def _create_structured_conversation_response(self, response: str) -> Dict[str, Any]:
        """구조화된 대화 응답 생성"""
        return {
            "content": response,
            "suggestions": ["추가 질문이 있으시면 언제든 말씀해주세요."],
            "follow_up_questions": ["다른 도움이 필요한 부분이 있나요?"]
        }
    
    def _get_classification_system_prompt(self) -> str:
        """분류 시스템 프롬프트"""
        return """당신은 사용자 메시지를 정확히 분류하는 전문가입니다. 
코딩 관련 맥락에서 메시지의 의도를 파악하고 적절한 유형으로 분류하세요."""
    
    def _get_code_question_system_prompt(self) -> str:
        """코드 질문 시스템 프롬프트"""
        return """당신은 코드 전문가입니다. 사용자의 질문에 대해 정확하고 도움이 되는 답변을 제공하세요."""
    
    def _get_code_request_system_prompt(self) -> str:
        """코드 요청 시스템 프롬프트"""
        return """당신은 코드 작성 전문가입니다. 요청사항을 정확히 구현하고, 깔끔하고 효율적인 코드를 작성하세요."""
    
    def _get_debug_system_prompt(self) -> str:
        """디버깅 시스템 프롬프트"""
        return """당신은 디버깅 전문가입니다. 문제를 정확히 진단하고 효과적인 해결책을 제시하세요."""
    
    def _get_refactor_system_prompt(self) -> str:
        """리팩토링 시스템 프롬프트"""
        return """당신은 코드 리팩토링 전문가입니다. 코드 품질을 향상시키는 개선 방안을 제시하세요."""
    
    def _get_explanation_system_prompt(self) -> str:
        """설명 시스템 프롬프트"""
        return """당신은 코드 설명 전문가입니다. 복잡한 코드를 이해하기 쉽게 설명하세요."""
    
    def _get_conversation_system_prompt(self) -> str:
        """대화 시스템 프롬프트"""
        return """당신은 친근하고 도움이 되는 코딩 어시스턴트입니다. 사용자와 자연스럽게 대화하세요."""
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """대화 히스토리 조회"""
        if user_id not in self.conversation_sessions:
            return []
        
        session = self.conversation_sessions[user_id]
        return session["messages"][-limit:]
    
    def clear_session(self, user_id: str):
        """세션 정리"""
        if user_id in self.conversation_sessions:
            del self.conversation_sessions[user_id]
            logger.info(f"사용자 {user_id} 세션 정리 완료")
    
    def get_session_stats(self, user_id: str) -> Dict[str, Any]:
        """세션 통계 조회"""
        if user_id not in self.conversation_sessions:
            return {"message_count": 0, "session_duration": 0}
        
        session = self.conversation_sessions[user_id]
        message_count = len(session["messages"])
        
        created_at = datetime.fromisoformat(session["created_at"])
        session_duration = (datetime.now() - created_at).total_seconds()
        
        return {
            "message_count": message_count,
            "session_duration": session_duration,
            "code_snapshots": len(session["code_history"]),
            "created_at": session["created_at"]
        }
