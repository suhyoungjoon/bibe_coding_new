from langgraph.graph import StateGraph, END
from .agents.state import AgentState
from .agents.query_analyzer import analyze
from .agents.planner import plan
from .agents.rag_agent import retrieve
from .agents.tool_agent import exec_tools
from .agents.report_agent import draft_and_refine
def build_graph() -> StateGraph:
    sg = StateGraph(AgentState)
    sg.add_node("analyze", analyze)
    sg.add_node("plan", plan)
    sg.add_node("rag", retrieve)
    sg.add_node("tools", exec_tools)
    sg.add_node("report", draft_and_refine)
    sg.set_entry_point("analyze")
    sg.add_edge("analyze", "plan")
    # Conditional branch could be added here; for now always RAG → tools
    sg.add_edge("plan", "rag")
    sg.add_edge("rag", "tools")
    sg.add_edge("tools", "report")
    sg.add_edge("report", END)
    return sg
