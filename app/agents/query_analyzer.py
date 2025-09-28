import re
from .state import AgentState
def analyze(state: AgentState) -> AgentState:
    q = (state.get("question") or "").strip()
    state["intent"] = "qa" if q else "unknown"
    state["need_calc"] = bool(re.search(r"\d+\s*[+\-*/^]\s*\d+", q))
    # keep sqlite toggle so UI stays compatible
    state["use_sqlite"] = any(w in q.lower() for w in ["sql:", "query:"])
    return state
