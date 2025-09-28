from typing import TypedDict, List, Dict, Any, Optional
class AgentState(TypedDict, total=False):
    question: str
    intent: str
    plan: List[str]
    need_rag: bool
    need_calc: bool
    use_sqlite: bool
    contexts: List[Dict[str, str]]
    tool_results: Dict[str, Any]
    draft: str
    final: str
