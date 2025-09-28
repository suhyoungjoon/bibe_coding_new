from typing import List, Dict
from .state import AgentState
from ..llm import LLMClient
SYSTEM = "You are a helpful, concise assistant. Use retrieved snippets to justify answers with short citations (file names)."

def _format_context(ctxs: List[Dict[str, str]], max_chars=800) -> str:
    parts = []
    for c in ctxs[:5]:
        chunk = c["chunk"]
        if len(chunk) > max_chars:
            chunk = chunk[:max_chars] + "..."
        parts.append(f"[{c['source']}] score={c['score']}\n{chunk}")
    return "\n\n".join(parts) if parts else "(no context found)"

def _critic_fix(draft: str, context_text: str) -> str:
    llm = LLMClient()
    msgs = [
        {"role":"user","content":(
            "You are a strict reviewer. Check the following answer for:\n"
            "1) factual claims unsupported by provided context\n"
            "2) missing citations to files\n"
            "3) unclear steps to implement\n"
            "Return an improved final answer (concise), adding file citations like (File.java)."
        )},
        {"role":"assistant","content":f"Context:\n{context_text}"},
        {"role":"assistant","content":f"Draft:\n{draft}"},
        {"role":"user","content":"Return just the improved answer."}
    ]
    try:
        return llm.chat(msgs, system="Be precise, actionable, concise.")
    except Exception:
        return draft

def draft_and_refine(state: AgentState) -> AgentState:
    llm = LLMClient()
    q = state.get("question", "")
    ctxs = state.get("contexts", [])
    tools = state.get("tool_results", {})

    context_text = _format_context(ctxs)
    tool_text = "\\n".join(f"{k}: {v}" for k, v in tools.items()) if tools else "(no tools used)"

    messages = [
        {"role": "user", "content": f"Question: {q}"},
        {"role": "assistant", "content": f"Plan: {'; '.join(state.get('plan', []))}"},
        {"role": "assistant", "content": f"Context:\\n{context_text}"},
        {"role": "assistant", "content": f"Tool results:\\n{tool_text}"},
        {"role": "user", "content": "Write a final, self-contained answer. If you used context, mention the file names where appropriate."},
    ]
    draft = llm.chat(messages, system=SYSTEM)
    improved = _critic_fix(draft, context_text)
    state["final"] = improved or draft
    return state
