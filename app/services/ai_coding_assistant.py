"""
AI 코딩 어시스턴트 서비스
실시간 코드 분석, 제안 생성, 리팩토링 추천
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import ast
import re

from ..llm import LLMClient
from .code_analysis_service import CodeAnalysisService

logger = logging.getLogger(__name__)

class AICodingAssistant:
    """AI 코딩 어시스턴트"""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.code_analyzer = CodeAnalysisService()
        self.conversation_history = {}  # 사용자별 대화 히스토리
        self.code_context = {}  # 코드 컨텍스트 저장
    
    async def analyze_and_suggest(self, code: str, file_path: str, user_id: str = "default") -> Dict[str, Any]:
        """코드 분석 및 AI 제안 생성"""
        try:
            # 기본 코드 분석
            basic_analysis = await self.code_analyzer.analyze_code(code, file_path)
            
            # AI 기반 고급 분석
            ai_analysis = await self._ai_code_analysis(code, file_path, basic_analysis)
            
            # 개인화된 제안 생성
            suggestions = await self._generate_personalized_suggestions(
                code, file_path, user_id, basic_analysis, ai_analysis
            )
            
            # 컨텍스트 업데이트
            self._update_code_context(user_id, file_path, code, ai_analysis)
            
            return {
                "success": True,
                "basic_analysis": basic_analysis,
                "ai_analysis": ai_analysis,
                "suggestions": suggestions,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"AI 코드 분석 실패: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _ai_code_analysis(self, code: str, file_path: str, basic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """AI 기반 고급 코드 분석"""
        try:
            language = basic_analysis.get("language", "unknown")
            
            # AI 분석 프롬프트 생성
            prompt = self._create_analysis_prompt(code, file_path, language, basic_analysis)
            
            # LLM을 통한 분석
            ai_response = await self._call_llm(prompt, system_prompt=self._get_analysis_system_prompt())
            
            # 응답 파싱
            ai_analysis = self._parse_ai_response(ai_response)
            
            return ai_analysis
            
        except Exception as e:
            logger.error(f"AI 분석 중 오류: {e}")
            return {"error": str(e)}
    
    def _create_analysis_prompt(self, code: str, file_path: str, language: str, basic_analysis: Dict[str, Any]) -> str:
        """분석 프롬프트 생성"""
        metrics = basic_analysis.get("metrics", {})
        issues = basic_analysis.get("issues", [])
        
        prompt = f"""
다음 {language} 코드를 분석하고 개선 제안을 해주세요:

파일: {file_path}
코드:
```{language}
{code}
```

기본 분석 결과:
- 라인 수: {metrics.get('lines_of_code', 0)}
- 함수 수: {metrics.get('functions', 0)}
- 클래스 수: {metrics.get('classes', 0)}
- 복잡도: {metrics.get('complexity', 0)}
- 품질 점수: {basic_analysis.get('quality_score', 0)}

발견된 이슈:
{chr(10).join([f"- {issue.get('type', 'unknown')}: {issue.get('message', '')}" for issue in issues[:5]])}

다음 항목들을 분석해주세요:
1. 코드 품질 및 가독성
2. 성능 최적화 가능성
3. 보안 취약점
4. 디자인 패턴 적용 가능성
5. 테스트 가능성
6. 유지보수성

JSON 형식으로 응답해주세요:
{{
    "quality_assessment": "코드 품질 평가",
    "performance_issues": ["성능 이슈들"],
    "security_concerns": ["보안 우려사항들"],
    "design_patterns": ["적용 가능한 디자인 패턴들"],
    "testability": "테스트 가능성 평가",
    "maintainability": "유지보수성 평가",
    "improvement_priority": ["개선 우선순위 항목들"]
}}
"""
        return prompt
    
    def _get_analysis_system_prompt(self) -> str:
        """분석 시스템 프롬프트"""
        return """당신은 숙련된 소프트웨어 엔지니어이자 코드 리뷰어입니다. 
코드를 분석할 때 다음을 고려하세요:

1. 코드 품질: 가독성, 명확성, 일관성
2. 성능: 시간 복잡도, 공간 복잡도, 효율성
3. 보안: 입력 검증, 오류 처리, 취약점
4. 설계: SOLID 원칙, 디자인 패턴, 아키텍처
5. 테스트: 단위 테스트 가능성, 통합 테스트
6. 유지보수: 확장성, 모듈화, 문서화

구체적이고 실행 가능한 제안을 제공하세요. JSON 형식으로 정확히 응답하세요."""
    
    async def _call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """LLM 호출"""
        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.llm_client.chat(messages, system=system_prompt)
            return response
        except Exception as e:
            logger.error(f"LLM 호출 실패: {e}")
            return f"LLM 분석 실패: {str(e)}"
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """AI 응답 파싱 (개선된 버전)"""
        try:
            # 먼저 정리된 JSON 추출 시도
            import json
            import re
            
            # JSON 블록 찾기 (```json ... ``` 또는 { ... })
            json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
            json_match = re.search(json_pattern, response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1)
            else:
                # 일반 JSON 찾기
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = response[json_start:json_end]
                else:
                    # JSON이 없는 경우 구조화된 응답 생성
                    return self._create_structured_response(response)
            
            # JSON 파싱
            parsed = json.loads(json_str)
            return parsed
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON 파싱 실패, 구조화된 응답 생성: {e}")
            return self._create_structured_response(response)
        except Exception as e:
            logger.error(f"AI 응답 파싱 실패: {e}")
            return self._create_structured_response(response)
    
    def _create_structured_response(self, response: str) -> Dict[str, Any]:
        """구조화된 응답 생성"""
        return {
            "analysis": response,
            "quality_assessment": "코드 분석이 완료되었습니다.",
            "performance_issues": ["상세 분석을 위해 더 구체적인 정보가 필요합니다."],
            "security_concerns": [],
            "design_patterns": [],
            "improvement_priority": ["코드 리뷰", "성능 검토", "보안 검사"],
            "format": "text"
        }
    
    async def _generate_personalized_suggestions(
        self, 
        code: str, 
        file_path: str, 
        user_id: str, 
        basic_analysis: Dict[str, Any], 
        ai_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """개인화된 제안 생성"""
        suggestions = []
        
        try:
            # 사용자 히스토리 기반 제안
            user_history = self.conversation_history.get(user_id, [])
            
            # 우선순위 기반 제안
            priority_items = ai_analysis.get("improvement_priority", [])
            
            for item in priority_items[:3]:  # 상위 3개 항목
                suggestion = await self._create_detailed_suggestion(
                    item, code, file_path, basic_analysis, ai_analysis
                )
                if suggestion:
                    suggestions.append(suggestion)
            
            # 성능 최적화 제안
            performance_issues = ai_analysis.get("performance_issues", [])
            for issue in performance_issues[:2]:
                suggestion = await self._create_performance_suggestion(issue, code)
                if suggestion:
                    suggestions.append(suggestion)
            
            # 보안 제안
            security_concerns = ai_analysis.get("security_concerns", [])
            for concern in security_concerns[:2]:
                suggestion = await self._create_security_suggestion(concern, code)
                if suggestion:
                    suggestions.append(suggestion)
            
            # 디자인 패턴 제안
            design_patterns = ai_analysis.get("design_patterns", [])
            for pattern in design_patterns[:2]:
                suggestion = await self._create_pattern_suggestion(pattern, code, file_path)
                if suggestion:
                    suggestions.append(suggestion)
            
        except Exception as e:
            logger.error(f"제안 생성 실패: {e}")
        
        return suggestions
    
    async def _create_detailed_suggestion(
        self, 
        item: str, 
        code: str, 
        file_path: str, 
        basic_analysis: Dict[str, Any], 
        ai_analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """상세 제안 생성"""
        try:
            prompt = f"""
다음 개선 항목에 대한 구체적인 제안을 해주세요:

개선 항목: {item}

현재 코드:
```{basic_analysis.get('language', 'unknown')}
{code}
```

분석 결과:
- 품질 점수: {basic_analysis.get('quality_score', 0)}
- 복잡도: {basic_analysis.get('metrics', {}).get('complexity', 0)}

다음 형식으로 응답해주세요:
{{
    "type": "improvement",
    "title": "제안 제목",
    "description": "상세 설명",
    "priority": "high|medium|low",
    "estimated_effort": "소요 시간 추정",
    "before_code": "개선 전 코드 예시",
    "after_code": "개선 후 코드 예시",
    "benefits": ["개선 효과들"],
    "steps": ["구현 단계들"]
}}
"""
            
            response = await self._call_llm(prompt, self._get_suggestion_system_prompt())
            suggestion_data = self._parse_ai_response(response)
            
            if "title" in suggestion_data:
                return {
                    "type": "improvement",
                    "title": suggestion_data.get("title", item),
                    "description": suggestion_data.get("description", ""),
                    "priority": suggestion_data.get("priority", "medium"),
                    "estimated_effort": suggestion_data.get("estimated_effort", ""),
                    "before_code": suggestion_data.get("before_code", ""),
                    "after_code": suggestion_data.get("after_code", ""),
                    "benefits": suggestion_data.get("benefits", []),
                    "steps": suggestion_data.get("steps", []),
                    "category": "general_improvement"
                }
            
        except Exception as e:
            logger.error(f"상세 제안 생성 실패: {e}")
        
        return None
    
    async def _create_performance_suggestion(self, issue: str, code: str) -> Optional[Dict[str, Any]]:
        """성능 최적화 제안 생성"""
        try:
            prompt = f"""
성능 이슈 해결 방안을 제안해주세요:

이슈: {issue}

코드:
```python
{code}
```

다음 형식으로 응답해주세요:
{{
    "type": "performance",
    "title": "성능 최적화 제안",
    "description": "이슈 설명 및 해결 방안",
    "priority": "high",
    "optimized_code": "최적화된 코드",
    "performance_gain": "예상 성능 개선",
    "trade_offs": ["트레이드오프 사항들"]
}}
"""
            
            response = await self._call_llm(prompt, self._get_performance_system_prompt())
            suggestion_data = self._parse_ai_response(response)
            
            if "title" in suggestion_data:
                return {
                    "type": "performance",
                    "title": suggestion_data.get("title", "성능 최적화"),
                    "description": suggestion_data.get("description", issue),
                    "priority": "high",
                    "optimized_code": suggestion_data.get("optimized_code", ""),
                    "performance_gain": suggestion_data.get("performance_gain", ""),
                    "trade_offs": suggestion_data.get("trade_offs", []),
                    "category": "performance"
                }
            
        except Exception as e:
            logger.error(f"성능 제안 생성 실패: {e}")
        
        return None
    
    async def _create_security_suggestion(self, concern: str, code: str) -> Optional[Dict[str, Any]]:
        """보안 제안 생성"""
        try:
            prompt = f"""
보안 취약점 해결 방안을 제안해주세요:

보안 우려사항: {concern}

코드:
```python
{code}
```

다음 형식으로 응답해주세요:
{{
    "type": "security",
    "title": "보안 개선 제안",
    "description": "취약점 설명 및 해결 방안",
    "priority": "high",
    "secure_code": "보안 강화된 코드",
    "vulnerability_type": "취약점 유형",
    "mitigation": "완화 방안"
}}
"""
            
            response = await self._call_llm(prompt, self._get_security_system_prompt())
            suggestion_data = self._parse_ai_response(response)
            
            if "title" in suggestion_data:
                return {
                    "type": "security",
                    "title": suggestion_data.get("title", "보안 개선"),
                    "description": suggestion_data.get("description", concern),
                    "priority": "high",
                    "secure_code": suggestion_data.get("secure_code", ""),
                    "vulnerability_type": suggestion_data.get("vulnerability_type", ""),
                    "mitigation": suggestion_data.get("mitigation", ""),
                    "category": "security"
                }
            
        except Exception as e:
            logger.error(f"보안 제안 생성 실패: {e}")
        
        return None
    
    async def _create_pattern_suggestion(self, pattern: str, code: str, file_path: str) -> Optional[Dict[str, Any]]:
        """디자인 패턴 제안 생성"""
        try:
            prompt = f"""
다음 디자인 패턴을 적용한 코드를 제안해주세요:

패턴: {pattern}

현재 코드:
```python
{code}
```

다음 형식으로 응답해주세요:
{{
    "type": "pattern",
    "title": "디자인 패턴 적용",
    "description": "패턴 설명 및 적용 방법",
    "priority": "medium",
    "pattern_code": "패턴 적용된 코드",
    "pattern_benefits": ["패턴 적용 효과들"],
    "implementation_steps": ["구현 단계들"]
}}
"""
            
            response = await self._call_llm(prompt, self._get_pattern_system_prompt())
            suggestion_data = self._parse_ai_response(response)
            
            if "title" in suggestion_data:
                return {
                    "type": "pattern",
                    "title": suggestion_data.get("title", f"{pattern} 패턴 적용"),
                    "description": suggestion_data.get("description", ""),
                    "priority": "medium",
                    "pattern_code": suggestion_data.get("pattern_code", ""),
                    "pattern_benefits": suggestion_data.get("pattern_benefits", []),
                    "implementation_steps": suggestion_data.get("implementation_steps", []),
                    "category": "design_pattern"
                }
            
        except Exception as e:
            logger.error(f"패턴 제안 생성 실패: {e}")
        
        return None
    
    def _get_suggestion_system_prompt(self) -> str:
        """제안 시스템 프롬프트"""
        return """당신은 코드 개선 전문가입니다. 구체적이고 실행 가능한 제안을 제공하세요.
코드 예시는 실제로 동작하는 완전한 코드여야 합니다."""
    
    def _get_performance_system_prompt(self) -> str:
        """성능 최적화 시스템 프롬프트"""
        return """당신은 성능 최적화 전문가입니다. 
시간 복잡도, 공간 복잡도, 알고리즘 효율성을 고려하여 최적화 방안을 제시하세요."""
    
    def _get_security_system_prompt(self) -> str:
        """보안 시스템 프롬프트"""
        return """당신은 보안 전문가입니다. 
OWASP Top 10, 입력 검증, 인증/인가, 데이터 보호를 고려하여 보안 강화 방안을 제시하세요."""
    
    def _get_pattern_system_prompt(self) -> str:
        """디자인 패턴 시스템 프롬프트"""
        return """당신은 소프트웨어 설계 전문가입니다. 
SOLID 원칙과 GoF 디자인 패턴을 활용하여 확장 가능하고 유지보수 가능한 코드를 제안하세요."""
    
    def _update_code_context(self, user_id: str, file_path: str, code: str, analysis: Dict[str, Any]):
        """코드 컨텍스트 업데이트"""
        if user_id not in self.code_context:
            self.code_context[user_id] = {}
        
        self.code_context[user_id][file_path] = {
            "code": code,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_context_aware_suggestions(
        self, 
        current_code: str, 
        file_path: str, 
        user_id: str, 
        cursor_position: Dict[str, int] = None
    ) -> List[Dict[str, Any]]:
        """컨텍스트 인식 제안 생성"""
        try:
            # 사용자 컨텍스트 가져오기
            user_context = self.code_context.get(user_id, {})
            
            # 현재 파일 주변 컨텍스트 분석
            context_files = list(user_context.keys())
            
            # 컨텍스트 기반 제안 생성
            context_prompt = self._create_context_prompt(
                current_code, file_path, user_context, cursor_position
            )
            
            response = await self._call_llm(context_prompt, self._get_context_system_prompt())
            suggestions = self._parse_context_suggestions(response)
            
            return suggestions
            
        except Exception as e:
            logger.error(f"컨텍스트 제안 생성 실패: {e}")
            return []
    
    def _create_context_prompt(
        self, 
        current_code: str, 
        file_path: str, 
        user_context: Dict[str, Any], 
        cursor_position: Dict[str, int]
    ) -> str:
        """컨텍스트 프롬프트 생성"""
        prompt = f"""
현재 작업 중인 코드를 분석하고 컨텍스트를 고려한 제안을 해주세요:

현재 파일: {file_path}
커서 위치: {cursor_position}

현재 코드:
```python
{current_code}
```

프로젝트 컨텍스트:
"""
        
        for file_path_ctx, context_data in user_context.items():
            if file_path_ctx != file_path:
                prompt += f"\n{file_path_ctx}:\n```python\n{context_data['code'][:200]}...\n```"
        
        prompt += """

컨텍스트를 고려하여 다음 제안들을 해주세요:
1. 현재 위치에서 적절한 코드 완성
2. 프로젝트 전체 일관성을 위한 제안
3. 의존성 관계를 고려한 제안

JSON 형식으로 응답해주세요:
{
    "completions": ["코드 완성 제안들"],
    "context_suggestions": ["컨텍스트 기반 제안들"],
    "dependency_hints": ["의존성 힌트들"]
}
"""
        return prompt
    
    def _get_context_system_prompt(self) -> str:
        """컨텍스트 시스템 프롬프트"""
        return """당신은 프로젝트 전체를 이해하는 코딩 어시스턴트입니다. 
현재 작업 중인 코드의 위치와 프로젝트의 다른 부분들과의 관계를 고려하여 제안하세요."""
    
    def _parse_context_suggestions(self, response: str) -> List[Dict[str, Any]]:
        """컨텍스트 제안 파싱 (개선된 버전)"""
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
                    # JSON이 없는 경우 기본 제안 생성
                    return self._create_default_suggestions(response)
            
            data = json.loads(json_str)
            suggestions = []
            
            # 코드 완성 제안
            for completion in data.get("completions", []):
                suggestions.append({
                    "type": "completion",
                    "text": completion,
                    "category": "auto_complete"
                })
            
            # 컨텍스트 제안
            for suggestion in data.get("context_suggestions", []):
                suggestions.append({
                    "type": "context",
                    "text": suggestion,
                    "category": "context_aware"
                })
            
            # 의존성 힌트
            for hint in data.get("dependency_hints", []):
                suggestions.append({
                    "type": "dependency",
                    "text": hint,
                    "category": "dependency"
                })
            
            # 제안이 없는 경우 기본 제안 추가
            if not suggestions:
                suggestions.extend(self._create_default_suggestions(response))
            
            return suggestions
            
        except Exception as e:
            logger.error(f"컨텍스트 제안 파싱 실패: {e}")
            return self._create_default_suggestions(response)
    
    def _create_default_suggestions(self, response: str) -> List[Dict[str, Any]]:
        """기본 제안 생성"""
        return [
            {
                "type": "general",
                "text": "코드 개선을 위한 일반적인 제안",
                "category": "general"
            },
            {
                "type": "completion",
                "text": "def function_name():\n    \"\"\"함수 설명\"\"\"\n    pass",
                "category": "auto_complete"
            },
            {
                "type": "context",
                "text": "현재 프로젝트의 다른 파일들을 참고해보세요.",
                "category": "context_aware"
            }
        ]
    
    def get_user_coding_pattern(self, user_id: str) -> Dict[str, Any]:
        """사용자 코딩 패턴 분석"""
        if user_id not in self.code_context:
            return {"pattern": "unknown", "experience_level": "beginner"}
        
        user_files = self.code_context[user_id]
        
        # 패턴 분석
        total_complexity = 0
        total_functions = 0
        total_classes = 0
        
        for file_data in user_files.values():
            analysis = file_data.get("analysis", {})
            metrics = analysis.get("metrics", {})
            
            total_complexity += metrics.get("complexity", 0)
            total_functions += metrics.get("functions", 0)
            total_classes += metrics.get("classes", 0)
        
        file_count = len(user_files)
        
        if file_count == 0:
            return {"pattern": "unknown", "experience_level": "beginner"}
        
        avg_complexity = total_complexity / file_count
        avg_functions = total_functions / file_count
        avg_classes = total_classes / file_count
        
        # 경험 레벨 결정
        if avg_complexity > 10 and avg_classes > 2:
            experience_level = "expert"
        elif avg_complexity > 5 and avg_functions > 3:
            experience_level = "intermediate"
        else:
            experience_level = "beginner"
        
        return {
            "pattern": "analyzed",
            "experience_level": experience_level,
            "file_count": file_count,
            "avg_complexity": avg_complexity,
            "avg_functions": avg_functions,
            "avg_classes": avg_classes
        }
