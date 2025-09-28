import streamlit as st
from pathlib import Path
from app.graph import build_graph
from app.agents.state import AgentState
from app.config import DATA_DIR, INDEX_DIR, LLM_PROVIDER
from app.ingest import rebuild_index
from app.vectorstore.faiss_store import FaissStore
st.set_page_config(page_title="Agentic AI – Azure OpenAI + Hybrid RAG", layout="wide")
st.title("🕹️ Agentic AI – Azure OpenAI + FAISS ⊕ BM25 + Self-Critique + Code Exec")
st.caption("Upload docs → Rebuild index → Ask. Use prefixes: sql:, python:, java: to execute tools.")
with st.sidebar:
    st.header("Settings")
    st.markdown(f"**Provider:** `{LLM_PROVIDER}`")
    st.markdown("**Docs folder:**"); st.code(str(DATA_DIR))
    st.markdown("**Index folder:**"); st.code(str(INDEX_DIR))
with st.expander("📥 Upload documents (stored in app/data/docs)", expanded=False):
    files = st.file_uploader("Upload files (.txt, .md, .java, .py, .pdf, .csv, ...)", accept_multiple_files=True)
    if files:
        for f in files:
            (DATA_DIR / f.name).write_bytes(f.read())
        st.success(f"Saved {len(files)} file(s) to {DATA_DIR}")
colA, colB, colC = st.columns([1,1,1])
with colA:
    if st.button("🔁 Rebuild FAISS Index"):
        try:
            n_files, n_chunks = rebuild_index()
            st.success(f"Index built: {n_files} files, {n_chunks} chunks")
        except Exception as e:
            st.error(f"Index build failed: {e}")
with colB:
    if st.button("ℹ️ Show Index Stats"):
        fs = FaissStore()
        if fs.load():
            st.info(f"Index loaded. Meta entries: {len(fs.meta)}; dim={fs.dim}")
        else:
            st.warning("No index found. Build it first.")
with colC:
    clear = st.button("🗑️ Clear Output")
question = st.text_area("Ask a question", height=160, value=(
    "Explain the Strategy pattern in the docs and cite files.\n"
    "python: print('hello from python')\n"
    "java: public class Main { public static void main(String[] a){ System.out.println(1+2); } }"
))
if clear:
    st.session_state.pop("result", None)
run = st.button("▶️ Run Multi-Agent")
if run and question.strip():
    sg = build_graph(); app = sg.compile()
    state: AgentState = {"question": question}
    with st.spinner("Running graph..."):
        state = app.invoke(state, config={"recursion_limit": 1})
    st.session_state["result"] = state
if st.session_state.get("result"):
    R = st.session_state["result"]
    st.write("## ✅ Result")
    tabs = st.tabs(["Plan", "Contexts (Hybrid)", "Tool Results", "Final Answer", "Debug State"])
    with tabs[0]:
        st.write("**Plan**"); st.code("\n".join(R.get("plan", [])) or "(no plan)")
    with tabs[1]:
        st.write("**Retrieved Contexts (FAISS ⊕ BM25)**")
        ctxs = R.get("contexts") or []
        if not ctxs: st.info("No context.")
        else:
            for c in ctxs:
                st.markdown(f"- **{Path(c['source']).name}** (score {c['score']})")
                with st.expander(c["source"]):
                    st.code(c["chunk"][:1800])
    with tabs[2]:
        st.write("**Tool Results**")
        st.json(R.get("tool_results") or {})
    with tabs[3]:
        st.write("**Final Answer**"); st.write(R.get("final") or "(no output)")
    with tabs[4]:
        st.write("**Raw State**"); st.json(R)
st.divider()
st.caption("Tip: put code/docs into app/data/docs/, rebuild the index, then ask.")
