from .state import AgentState
from ..llm import LLMClient
from ..vectorstore.faiss_store import FaissStore
from .tools.file_search import LocalBM25
from ..config import DATA_DIR

_bm25 = None
def _bm25_index():
    global _bm25
    if _bm25 is None:
        _bm25 = LocalBM25(DATA_DIR)
        _bm25.index()
    return _bm25

def _rewrite(query: str) -> str:
    llm = LLMClient()
    msg = [{"role":"user","content":f"Rephrase or expand the search query focusing on key technical terms: {query}"}]
    try:
        return llm.chat(msg, system="You improve search queries for code RAG. Keep it short.") or query
    except Exception:
        return query

def retrieve(state: AgentState) -> AgentState:
    if not state.get("need_rag"):
        state["contexts"] = []; return state
    q = state.get("question","")
    rq = _rewrite(q)

    fs = FaissStore()
    ctx_vec = fs.search(rq or q, k=7)

    bm25 = _bm25_index()
    ctx_kw = bm25.search(rq or q, k=7)

    def norm(items):
        if not items: return []
        vals = [float(i.get("score",0)) for i in items]
        lo, hi = (min(vals), max(vals)) if vals else (0.0, 1.0)
        out=[]
        for it in items:
            s = float(it.get("score",0))
            ns = (s-lo)/(hi-lo+1e-9)
            out.append({**it,"score":f"{ns:.4f}"})
        return out

    fused = norm(ctx_vec) + norm(ctx_kw)
    fused.sort(key=lambda x: float(x["score"]), reverse=True)
    state["contexts"] = fused[:5]
    return state
