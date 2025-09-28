from typing import List
from .state import AgentState
def plan(state: AgentState) -> AgentState:
    q = state.get("question", "")
    steps: List[str] = [
        "1) Understand question and constraints",
        "2) Retrieve relevant context via Hybrid (FAISS + BM25) after Query Rewrite",
    ]
    if state.get("need_calc"):
        steps.append("3) Run calculator tool if math detected")
    if state.get("use_sqlite"):
        steps.append("4) Run SQLite tool for explicit 'sql:' or 'query:'")
    steps.append("5) Draft answer using LLM + contexts + tool results")
    steps.append("6) Self-critique & return")
    state["plan"] = steps
    state["need_rag"] = len(q) > 3
    return state
