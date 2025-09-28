"""
코드 분석 서비스
실시간 코드 분석, 제안 생성, 품질 검사
"""

import ast
import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class CodeAnalysisService:
    """코드 분석 서비스"""
    
    def __init__(self):
        self.analysis_cache = {}  # 분석 결과 캐시
    
    async def analyze_code(self, code: str, file_path: str) -> Dict[str, Any]:
        """코드 종합 분석"""
        try:
            # 캐시 확인
            cache_key = f"{file_path}:{hash(code)}"
            if cache_key in self.analysis_cache:
                return self.analysis_cache[cache_key]
            
            # 언어 감지
            language = self._detect_language(file_path)
            
            # 언어별 분석 실행
            if language == "python":
                analysis = await self._analyze_python_code(code, file_path)
            elif language == "javascript":
                analysis = await self._analyze_javascript_code(code, file_path)
            elif language == "java":
                analysis = await self._analyze_java_code(code, file_path)
            else:
                analysis = await self._analyze_generic_code(code, file_path)
            
            # 공통 분석 추가
            analysis.update(await self._analyze_common(code, file_path, language))
            
            # 캐시 저장
            self.analysis_cache[cache_key] = analysis
            
            return analysis
            
        except Exception as e:
            logger.error(f"코드 분석 실패: {e}")
            return {
                "success": False,
                "error": str(e),
                "language": "unknown",
                "analysis_time": 0
            }
    
    def _detect_language(self, file_path: str) -> str:
        """파일 확장자로 언어 감지"""
        extension = file_path.lower().split('.')[-1] if '.' in file_path else ''
        
        language_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'java': 'java',
            'go': 'go',
            'cpp': 'cpp',
            'c': 'c',
            'cs': 'csharp',
            'rb': 'ruby',
            'php': 'php',
            'rs': 'rust'
        }
        
        return language_map.get(extension, 'unknown')
    
    async def _analyze_python_code(self, code: str, file_path: str) -> Dict[str, Any]:
        """Python 코드 분석"""
        analysis = {
            "language": "python",
            "success": True,
            "syntax_valid": True,
            "issues": [],
            "metrics": {},
            "suggestions": []
        }
        
        try:
            # AST 파싱
            tree = ast.parse(code)
            
            # 기본 메트릭 계산
            analysis["metrics"] = {
                "lines_of_code": len(code.splitlines()),
                "functions": len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
                "classes": len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
                "imports": len([node for node in ast.walk(tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]),
                "complexity": self._calculate_cyclomatic_complexity(tree)
            }
            
            # 코드 품질 검사
            issues = []
            
            # 함수 길이 검사
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 1
                    if lines > 50:
                        issues.append({
                            "type": "warning",
                            "message": f"함수 '{node.name}'이 너무 깁니다 ({lines}줄)",
                            "line": node.lineno,
                            "suggestion": "함수를 더 작은 단위로 분할하세요"
                        })
            
            # 변수명 검사
            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    if len(node.id) == 1 and node.id.islower():
                        issues.append({
                            "type": "style",
                            "message": f"변수명 '{node.id}'이 너무 짧습니다",
                            "line": getattr(node, 'lineno', 0),
                            "suggestion": "의미를 명확히 하는 변수명을 사용하세요"
                        })
            
            # 예외 처리 검사
            has_try_except = any(isinstance(node, ast.Try) for node in ast.walk(tree))
            if not has_try_except and analysis["metrics"]["functions"] > 0:
                issues.append({
                    "type": "info",
                    "message": "예외 처리를 고려해보세요",
                    "line": 0,
                    "suggestion": "try-except 블록을 사용하여 오류를 처리하세요"
                })
            
            analysis["issues"] = issues
            
            # 개선 제안 생성
            suggestions = []
            
            if analysis["metrics"]["complexity"] > 10:
                suggestions.append({
                    "type": "refactor",
                    "title": "복잡도 감소",
                    "description": "함수의 복잡도가 높습니다. 로직을 분할하거나 추상화를 고려하세요."
                })
            
            if analysis["metrics"]["functions"] == 0 and analysis["metrics"]["lines_of_code"] > 20:
                suggestions.append({
                    "type": "structure",
                    "title": "함수 분할",
                    "description": "코드를 함수로 분할하여 재사용성과 가독성을 높이세요."
                })
            
            analysis["suggestions"] = suggestions
            
        except SyntaxError as e:
            analysis.update({
                "success": False,
                "syntax_valid": False,
                "error": f"구문 오류: {e.msg}",
                "error_line": e.lineno
            })
        except Exception as e:
            analysis.update({
                "success": False,
                "error": str(e)
            })
        
        return analysis
    
    async def _analyze_javascript_code(self, code: str, file_path: str) -> Dict[str, Any]:
        """JavaScript 코드 분석"""
        analysis = {
            "language": "javascript",
            "success": True,
            "syntax_valid": True,
            "issues": [],
            "metrics": {},
            "suggestions": []
        }
        
        try:
            lines = code.splitlines()
            analysis["metrics"] = {
                "lines_of_code": len(lines),
                "functions": len(re.findall(r'function\s+\w+|const\s+\w+\s*=\s*\(|let\s+\w+\s*=\s*\(', code)),
                "classes": len(re.findall(r'class\s+\w+', code)),
                "imports": len(re.findall(r'import\s+.*from|require\s*\(', code))
            }
            
            issues = []
            
            # var 사용 검사
            if 'var ' in code:
                issues.append({
                    "type": "warning",
                    "message": "var 대신 let 또는 const를 사용하세요",
                    "line": 0,
                    "suggestion": "ES6+ 문법을 사용하여 변수 스코프를 명확히 하세요"
                })
            
            # 세미콜론 누락 검사
            lines_without_semicolon = []
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if (line and not line.startswith('//') and not line.startswith('*') and 
                    not line.startswith('/*') and not line.endswith(';') and 
                    not line.endswith('{') and not line.endswith('}') and
                    not line.startswith('if') and not line.startswith('for') and
                    not line.startswith('while') and not line.startswith('switch')):
                    lines_without_semicolon.append(i)
            
            if lines_without_semicolon:
                issues.append({
                    "type": "style",
                    "message": f"세미콜론이 누락된 줄: {lines_without_semicolon[:5]}",
                    "line": lines_without_semicolon[0],
                    "suggestion": "일관성을 위해 세미콜론을 추가하세요"
                })
            
            analysis["issues"] = issues
            
        except Exception as e:
            analysis.update({
                "success": False,
                "error": str(e)
            })
        
        return analysis
    
    async def _analyze_java_code(self, code: str, file_path: str) -> Dict[str, Any]:
        """Java 코드 분석"""
        analysis = {
            "language": "java",
            "success": True,
            "syntax_valid": True,
            "issues": [],
            "metrics": {},
            "suggestions": []
        }
        
        try:
            lines = code.splitlines()
            analysis["metrics"] = {
                "lines_of_code": len(lines),
                "methods": len(re.findall(r'(public|private|protected)?\s*(static)?\s*\w+\s+\w+\s*\(', code)),
                "classes": len(re.findall(r'(public|private|protected)?\s*class\s+\w+', code)),
                "imports": len(re.findall(r'import\s+', code))
            }
            
            issues = []
            
            # 접근 제어자 검사
            if 'public class' not in code and 'class ' in code:
                issues.append({
                    "type": "style",
                    "message": "클래스에 접근 제어자를 명시하세요",
                    "line": 0,
                    "suggestion": "public, private, protected 중 하나를 선택하세요"
                })
            
            # 주석 검사
            comment_lines = len([line for line in lines if line.strip().startswith('//') or line.strip().startswith('/*')])
            if comment_lines < len(lines) * 0.1:  # 10% 미만
                issues.append({
                    "type": "info",
                    "message": "코드에 주석을 추가하세요",
                    "line": 0,
                    "suggestion": "복잡한 로직에 대한 설명을 추가하세요"
                })
            
            analysis["issues"] = issues
            
        except Exception as e:
            analysis.update({
                "success": False,
                "error": str(e)
            })
        
        return analysis
    
    async def _analyze_generic_code(self, code: str, file_path: str) -> Dict[str, Any]:
        """일반적인 코드 분석"""
        lines = code.splitlines()
        
        return {
            "language": "unknown",
            "success": True,
            "syntax_valid": True,
            "issues": [],
            "metrics": {
                "lines_of_code": len(lines),
                "non_empty_lines": len([line for line in lines if line.strip()]),
                "comment_lines": len([line for line in lines if line.strip().startswith('#') or line.strip().startswith('//')])
            },
            "suggestions": []
        }
    
    async def _analyze_common(self, code: str, file_path: str, language: str) -> Dict[str, Any]:
        """공통 분석 항목"""
        lines = code.splitlines()
        
        common_analysis = {
            "analysis_time": datetime.now().isoformat(),
            "file_info": {
                "name": file_path.split('/')[-1],
                "size_bytes": len(code.encode('utf-8')),
                "encoding": "utf-8"
            },
            "quality_score": 0
        }
        
        # 품질 점수 계산
        quality_score = 100
        if len(lines) > 100:
            quality_score -= 10
        if len([line for line in lines if len(line) > 100]) > 0:
            quality_score -= 5
        if language == "python" and 'print(' in code and 'logging' not in code:
            quality_score -= 5
        
        common_analysis["quality_score"] = max(0, quality_score)
        
        return common_analysis
    
    def _calculate_cyclomatic_complexity(self, tree) -> int:
        """순환 복잡도 계산 (Python)"""
        complexity = 1
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    async def generate_suggestions(self, code: str, file_path: str, position: Dict[str, int] = None) -> List[Dict[str, Any]]:
        """코드 제안 생성"""
        suggestions = []
        
        try:
            language = self._detect_language(file_path)
            current_line = position.get('line', 0) if position else 0
            lines = code.splitlines()
            
            if current_line < len(lines):
                current_line_content = lines[current_line]
                
                # 자동완성 제안
                if language == "python":
                    suggestions.extend(self._get_python_suggestions(current_line_content, current_line))
                elif language == "javascript":
                    suggestions.extend(self._get_javascript_suggestions(current_line_content, current_line))
                
                # 공통 제안
                suggestions.extend(self._get_common_suggestions(current_line_content, current_line, language))
            
        except Exception as e:
            logger.error(f"제안 생성 실패: {e}")
        
        return suggestions
    
    def _get_python_suggestions(self, line: str, line_num: int) -> List[Dict[str, Any]]:
        """Python 코드 제안"""
        suggestions = []
        
        if 'import' in line and 'from' not in line:
            suggestions.append({
                "type": "import",
                "text": "import os\nimport sys\nimport json",
                "description": "자주 사용되는 모듈 import",
                "line": line_num
            })
        
        if 'def ' in line:
            suggestions.append({
                "type": "function",
                "text": "def function_name():\n    \"\"\"함수 설명\"\"\"\n    pass",
                "description": "함수 템플릿",
                "line": line_num
            })
        
        if 'class ' in line:
            suggestions.append({
                "type": "class",
                "text": "class ClassName:\n    \"\"\"클래스 설명\"\"\"\n    def __init__(self):\n        pass",
                "description": "클래스 템플릿",
                "line": line_num
            })
        
        return suggestions
    
    def _get_javascript_suggestions(self, line: str, line_num: int) -> List[Dict[str, Any]]:
        """JavaScript 코드 제안"""
        suggestions = []
        
        if 'function' in line:
            suggestions.append({
                "type": "function",
                "text": "function functionName() {\n    // 함수 내용\n}",
                "description": "함수 템플릿",
                "line": line_num
            })
        
        if 'const ' in line or 'let ' in line:
            suggestions.append({
                "type": "variable",
                "text": "const variableName = value;",
                "description": "변수 선언 템플릿",
                "line": line_num
            })
        
        return suggestions
    
    def _get_common_suggestions(self, line: str, line_num: int, language: str) -> List[Dict[str, Any]]:
        """공통 제안"""
        suggestions = []
        
        if 'TODO' in line.upper() or 'FIXME' in line.upper():
            suggestions.append({
                "type": "todo",
                "text": f"// TODO: {line.strip()}",
                "description": "TODO 항목 추가",
                "line": line_num
            })
        
        if 'print(' in line and language == "python":
            suggestions.append({
                "type": "logging",
                "text": "import logging\nlogging.info('메시지')",
                "description": "print 대신 logging 사용",
                "line": line_num
            })
        
        return suggestions
    
    def clear_cache(self):
        """분석 캐시 정리"""
        self.analysis_cache.clear()
        logger.info("코드 분석 캐시 정리 완료")
