import re
from typing import Dict, Any
from .state import AgentState
from .tools.calculator import safe_calculate
from .tools.sqlite_tool import run_sql
from .tools.exec_tool import run_python, run_javac

def _extract_after(prefix: str, q: str) -> str | None:
    idx = q.lower().find(prefix)
    if idx == -1: return None
    return q[idx+len(prefix):].strip()

def exec_tools(state: AgentState) -> AgentState:
    q = state.get("question", "")
    results: Dict[str, Any] = {}

    if state.get("need_calc"):
        m = re.search(r"(\d+\s*[+\-*/^]\s*\d+(?:\s*[+\-*/^]\s*\d+)*)", q)
        if m:
            expr = m.group(1)
            try:
                results["calculator"] = {"expr": expr, "result": safe_calculate(expr)}
            except Exception as e:
                results["calculator"] = {"expr": expr, "error": str(e)}

    # explicit SQL
    sql = _extract_after("sql:", q) or _extract_after("query:", q)
    if sql:
        results["sqlite"] = run_sql(sql)

    # code execution
    py = _extract_after("python:", q)
    if py:
        results["python_exec"] = run_python(py)

    jv = _extract_after("java:", q)
    if jv:
        results["java_exec"] = run_javac(jv)

    state["tool_results"] = results
    return state
