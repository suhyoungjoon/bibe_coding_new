"""
AI 학습 서비스
사용자 패턴 학습 및 개인화된 AI 제안
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from ..core.database import db_manager

logger = logging.getLogger(__name__)

class AILearningService:
    """AI 학습 서비스"""
    
    def __init__(self):
        self.learning_weights = {
            'naming_style': 0.3,
            'code_structure': 0.4,
            'error_pattern': 0.2,
            'preference_style': 0.1
        }
    
    async def record_learning_session(self, user_id: str, learning_type: str, 
                                    input_data: Dict[str, Any], ai_response: Dict[str, Any],
                                    user_feedback: Optional[Dict[str, Any]] = None) -> str:
        """AI 학습 세션 기록"""
        try:
            async with db_manager.get_connection() as conn:
                # 학습 점수 계산
                learning_score = await self._calculate_learning_score(
                    learning_type, input_data, ai_response, user_feedback
                )
                
                # 학습 세션 저장
                session_id = await conn.fetchval("""
                    INSERT INTO ai_learning_sessions 
                    (user_id, learning_type, input_data, ai_response, user_feedback, learning_score)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                """, user_id, learning_type, json.dumps(input_data), 
                    json.dumps(ai_response), json.dumps(user_feedback) if user_feedback else None,
                    learning_score)
                
                # 사용자 패턴 업데이트
                await self._update_user_patterns(user_id, learning_type, input_data, ai_response)
                
                logger.info(f"AI 학습 세션 기록 완료: {session_id} (점수: {learning_score:.2f})")
                return str(session_id)
                
        except Exception as e:
            logger.error(f"AI 학습 세션 기록 실패: {e}")
            raise
    
    async def get_user_patterns(self, user_id: str) -> Dict[str, Any]:
        """사용자 코딩 패턴 조회"""
        try:
            async with db_manager.get_connection() as conn:
                patterns = await conn.fetch("""
                    SELECT pattern_type, pattern_data, confidence_score, frequency
                    FROM user_coding_patterns
                    WHERE user_id = $1
                    ORDER BY confidence_score DESC
                """, user_id)
                
                result = {}
                for pattern in patterns:
                    result[pattern['pattern_type']] = {
                        'data': json.loads(pattern['pattern_data']),
                        'confidence': pattern['confidence_score'],
                        'frequency': pattern['frequency']
                    }
                
                return result
                
        except Exception as e:
            logger.error(f"사용자 패턴 조회 실패: {e}")
            return {}
    
    async def get_personalized_suggestions(self, user_id: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """개인화된 AI 제안 생성"""
        try:
            # 사용자 패턴 조회
            user_patterns = await self.get_user_patterns(user_id)
            
            # 제안 히스토리 분석
            suggestion_history = await self._get_suggestion_history(user_id)
            
            # 개인화된 제안 생성
            suggestions = await self._generate_personalized_suggestions(
                user_patterns, suggestion_history, context
            )
            
            return suggestions
            
        except Exception as e:
            logger.error(f"개인화된 제안 생성 실패: {e}")
            return []
    
    async def record_suggestion_feedback(self, user_id: str, suggestion_id: str,
                                       is_accepted: bool, feedback_rating: Optional[int] = None,
                                       modifications: Optional[str] = None):
        """제안 피드백 기록"""
        try:
            async with db_manager.get_connection() as conn:
                await conn.execute("""
                    UPDATE ai_suggestions_history
                    SET is_accepted = $1, feedback_rating = $2, user_modifications = $3
                    WHERE id = $4 AND user_id = $5
                """, is_accepted, feedback_rating, modifications, suggestion_id, user_id)
                
                # 피드백 기반 패턴 업데이트
                if is_accepted:
                    await self._update_acceptance_patterns(user_id, suggestion_id)
                
                logger.info(f"제안 피드백 기록 완료: {suggestion_id}")
                
        except Exception as e:
            logger.error(f"제안 피드백 기록 실패: {e}")
    
    async def analyze_coding_style(self, user_id: str, code_samples: List[str]) -> Dict[str, Any]:
        """코딩 스타일 분석"""
        try:
            analysis = {
                'naming_conventions': await self._analyze_naming_conventions(code_samples),
                'code_structure': await self._analyze_code_structure(code_samples),
                'error_patterns': await self._analyze_error_patterns(user_id),
                'preferences': await self._analyze_preferences(user_id)
            }
            
            # 분석 결과를 패턴으로 저장
            await self._save_coding_style_analysis(user_id, analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"코딩 스타일 분석 실패: {e}")
            return {}
    
    async def _calculate_learning_score(self, learning_type: str, input_data: Dict[str, Any],
                                      ai_response: Dict[str, Any], user_feedback: Optional[Dict[str, Any]]) -> float:
        """학습 점수 계산"""
        base_score = 0.5
        
        # 사용자 피드백이 있는 경우
        if user_feedback:
            if user_feedback.get('positive', False):
                base_score += 0.3
            if user_feedback.get('implemented', False):
                base_score += 0.2
        
        # AI 응답 품질 평가
        if ai_response.get('confidence', 0) > 0.8:
            base_score += 0.1
        
        # 학습 타입별 가중치 적용
        weight = self.learning_weights.get(learning_type, 0.1)
        
        return min(1.0, base_score * weight)
    
    async def _update_user_patterns(self, user_id: str, learning_type: str,
                                  input_data: Dict[str, Any], ai_response: Dict[str, Any]):
        """사용자 패턴 업데이트"""
        try:
            async with db_manager.get_connection() as conn:
                # 기존 패턴 조회
                existing = await conn.fetchrow("""
                    SELECT pattern_data, frequency, confidence_score
                    FROM user_coding_patterns
                    WHERE user_id = $1 AND pattern_type = $2
                """, user_id, learning_type)
                
                if existing:
                    # 기존 패턴 업데이트
                    old_data = json.loads(existing['pattern_data'])
                    new_data = self._merge_pattern_data(old_data, input_data, ai_response)
                    
                    # 신뢰도 및 빈도 업데이트
                    new_confidence = min(1.0, existing['confidence_score'] + 0.1)
                    new_frequency = existing['frequency'] + 1
                    
                    await conn.execute("""
                        UPDATE user_coding_patterns
                        SET pattern_data = $1, confidence_score = $2, frequency = $3,
                            last_updated = CURRENT_TIMESTAMP
                        WHERE user_id = $4 AND pattern_type = $5
                    """, json.dumps(new_data), new_confidence, new_frequency, user_id, learning_type)
                else:
                    # 새 패턴 생성
                    pattern_data = self._create_new_pattern(input_data, ai_response)
                    
                    await conn.execute("""
                        INSERT INTO user_coding_patterns
                        (user_id, pattern_type, pattern_data, confidence_score, frequency)
                        VALUES ($1, $2, $3, $4, $5)
                    """, user_id, learning_type, json.dumps(pattern_data), 0.6, 1)
                    
        except Exception as e:
            logger.error(f"사용자 패턴 업데이트 실패: {e}")
    
    def _merge_pattern_data(self, old_data: Dict[str, Any], input_data: Dict[str, Any],
                          ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """패턴 데이터 병합"""
        # 간단한 병합 로직 (실제로는 더 복잡한 알고리즘 사용)
        merged = old_data.copy()
        
        # 입력 데이터 병합
        for key, value in input_data.items():
            if key in merged:
                if isinstance(merged[key], list) and isinstance(value, list):
                    merged[key].extend(value)
                elif isinstance(merged[key], dict) and isinstance(value, dict):
                    merged[key].update(value)
                else:
                    merged[key] = value
            else:
                merged[key] = value
        
        # AI 응답 정보 추가
        merged['ai_responses'] = merged.get('ai_responses', [])
        merged['ai_responses'].append(ai_response)
        
        return merged
    
    def _create_new_pattern(self, input_data: Dict[str, Any], ai_response: Dict[str, Any]) -> Dict[str, Any]:
        """새 패턴 생성"""
        return {
            'input_data': input_data,
            'ai_responses': [ai_response],
            'created_at': datetime.now().isoformat(),
            'pattern_confidence': 0.6
        }
    
    async def _get_suggestion_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """제안 히스토리 조회"""
        try:
            async with db_manager.get_connection() as conn:
                history = await conn.fetch("""
                    SELECT suggestion_type, is_accepted, feedback_rating, confidence_score
                    FROM ai_suggestions_history
                    WHERE user_id = $1
                    ORDER BY created_at DESC
                    LIMIT $2
                """, user_id, limit)
                
                return [dict(record) for record in history]
                
        except Exception as e:
            logger.error(f"제안 히스토리 조회 실패: {e}")
            return []
    
    async def _generate_personalized_suggestions(self, user_patterns: Dict[str, Any],
                                               suggestion_history: List[Dict[str, Any]],
                                               context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """개인화된 제안 생성"""
        suggestions = []
        
        # 사용자 패턴 기반 제안
        if 'naming_style' in user_patterns:
            naming_suggestions = self._generate_naming_suggestions(
                user_patterns['naming_style'], context
            )
            suggestions.extend(naming_suggestions)
        
        # 히스토리 기반 제안
        if suggestion_history:
            history_suggestions = self._generate_history_based_suggestions(
                suggestion_history, context
            )
            suggestions.extend(history_suggestions)
        
        return suggestions[:5]  # 상위 5개만 반환
    
    def _generate_naming_suggestions(self, naming_pattern: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """네이밍 스타일 기반 제안"""
        # 실제로는 더 복잡한 로직 구현
        return [{
            'type': 'naming_suggestion',
            'suggestion': f"'{naming_pattern['data'].get('preferred_style', 'camelCase')} 스타일로 변수명을 수정하세요'",
            'confidence': naming_pattern['confidence']
        }]
    
    def _generate_history_based_suggestions(self, history: List[Dict[str, Any]], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """히스토리 기반 제안"""
        # 사용자가 자주 수락하는 제안 타입 분석
        accepted_types = [h['suggestion_type'] for h in history if h.get('is_accepted')]
        
        if accepted_types:
            return [{
                'type': 'history_based',
                'suggestion': f"이전에 좋아하셨던 {max(set(accepted_types), key=accepted_types.count)} 유형의 제안을 드립니다",
                'confidence': 0.7
            }]
        
        return []
    
    async def _analyze_naming_conventions(self, code_samples: List[str]) -> Dict[str, Any]:
        """네이밍 컨벤션 분석"""
        # 간단한 분석 로직 (실제로는 AST 파싱 등 사용)
        conventions = {
            'variable_style': 'snake_case',  # 기본값
            'function_style': 'snake_case',
            'class_style': 'PascalCase',
            'constant_style': 'UPPER_CASE'
        }
        
        # 코드 샘플 분석 로직 구현
        for code in code_samples:
            # 실제 분석 로직
            pass
        
        return conventions
    
    async def _analyze_code_structure(self, code_samples: List[str]) -> Dict[str, Any]:
        """코드 구조 분석"""
        return {
            'preferred_indentation': 4,
            'line_length_preference': 80,
            'import_style': 'grouped',
            'function_length_preference': 'short'
        }
    
    async def _analyze_error_patterns(self, user_id: str) -> Dict[str, Any]:
        """에러 패턴 분석"""
        try:
            async with db_manager.get_connection() as conn:
                errors = await conn.fetch("""
                    SELECT ai_response
                    FROM ai_learning_sessions
                    WHERE user_id = $1 AND learning_type = 'error_pattern'
                    ORDER BY created_at DESC
                    LIMIT 10
                """, user_id)
                
                error_patterns = {}
                for error in errors:
                    # 에러 패턴 분석 로직
                    pass
                
                return error_patterns
                
        except Exception as e:
            logger.error(f"에러 패턴 분석 실패: {e}")
            return {}
    
    async def _analyze_preferences(self, user_id: str) -> Dict[str, Any]:
        """사용자 선호도 분석"""
        return {
            'preferred_languages': ['python', 'javascript'],
            'code_style': 'functional',
            'documentation_preference': 'detailed'
        }
    
    async def _save_coding_style_analysis(self, user_id: str, analysis: Dict[str, Any]):
        """코딩 스타일 분석 결과 저장"""
        try:
            async with db_manager.get_connection() as conn:
                await conn.execute("""
                    INSERT INTO user_coding_patterns
                    (user_id, pattern_type, pattern_data, confidence_score)
                    VALUES ($1, 'coding_style', $2, $3)
                    ON CONFLICT (user_id, pattern_type)
                    DO UPDATE SET pattern_data = $2, last_updated = CURRENT_TIMESTAMP
                """, user_id, json.dumps(analysis), 0.8)
                
        except Exception as e:
            logger.error(f"코딩 스타일 분석 저장 실패: {e}")
    
    async def _update_acceptance_patterns(self, user_id: str, suggestion_id: str):
        """수락 패턴 업데이트"""
        # 제안 수락 시 관련 패턴의 신뢰도 증가
        try:
            async with db_manager.get_connection() as conn:
                suggestion = await conn.fetchrow("""
                    SELECT suggestion_type, confidence_score
                    FROM ai_suggestions_history
                    WHERE id = $1 AND user_id = $2
                """, suggestion_id, user_id)
                
                if suggestion:
                    # 해당 타입의 패턴 신뢰도 증가
                    await conn.execute("""
                        UPDATE user_coding_patterns
                        SET confidence_score = LEAST(1.0, confidence_score + 0.1)
                        WHERE user_id = $1 AND pattern_type = $2
                    """, user_id, suggestion['suggestion_type'])
                    
        except Exception as e:
            logger.error(f"수락 패턴 업데이트 실패: {e}")
