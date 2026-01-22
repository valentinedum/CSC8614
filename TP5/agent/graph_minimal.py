# TP5/agent/graph_minimal.py
from langgraph.graph import StateGraph, END

from TP5.agent.state import AgentState
from TP5.agent.routing import route
from TP5.agent.nodes.classify_email import classify_email
from TP5.agent.nodes.stubs import (
    stub_reply,
    stub_ask_clarification,
    stub_escalate,
    stub_ignore,
)
from TP5.agent.nodes.maybe_retrieve import maybe_retrieve


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("classify_email", classify_email)
    g.add_node("reply", stub_reply)
    g.add_node("ask_clarification", stub_ask_clarification)
    g.add_node("escalate", stub_escalate)
    g.add_node("ignore", stub_ignore)
    g.add_node("maybe_retrieve", maybe_retrieve)
    

    g.set_entry_point("classify_email")  # TODO: point d'entrée

    # TODO: routing conditionnel après classify_email
    g.add_conditional_edges(
        "classify_email",
        route,
        {
            "reply": "maybe_retrieve",
            "ask_clarification": "ask_clarification",
            "escalate": "escalate",
            "ignore": "ignore",
        },
    )

    # TODO: chaque branche termine le graphe
    g.add_edge("maybe_retrieve", "reply")
    g.add_edge("reply", END)
    g.add_edge("ask_clarification", END)
    g.add_edge("escalate", END)
    g.add_edge("ignore", END)

    return g.compile()