# Agenix/graph.py
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState as BaseMessagesState
from langgraph.checkpoint.postgres import PostgresSaver
from database import pool
from langchain_core.messages import AIMessage

# Agent nodes
from agents.supervisor import supervisor_node
from agents.enhancer import enhancer_node
from agents.researcher import research_node
from agents.coder import code_node
from agents.validator import validator_node
from agents.normal import normal_node

class MessagesState(BaseMessagesState):
    pass

def passthrough_node(state: MessagesState):
    """
    Takes the last message from a specialist and adds it to the history
    as a clean AIMessage for the user to see.
    """
    last_message_content = state["messages"][-1].content
    return {"messages": [AIMessage(content=last_message_content, name="assistant")]}

def create_graph():
    """Creates and compiles the LangGraph agent."""
    memory = PostgresSaver(conn=pool)
    graph = StateGraph(MessagesState)

    # Add all nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("enhancer", enhancer_node)
    graph.add_node("researcher", research_node)
    graph.add_node("coder", code_node)
    graph.add_node("passthrough", passthrough_node)
    graph.add_node("validator", validator_node)
    graph.add_node("normal", normal_node)

    # Set all edges for the graph
    graph.add_edge(START, "supervisor")
    graph.add_edge("enhancer", "supervisor")
    graph.add_edge("researcher", "passthrough")
    graph.add_edge("coder", "passthrough")
    graph.add_edge("normal", "passthrough")
    graph.add_edge("passthrough", "validator")

    # Set conditional edges
    graph.add_conditional_edges(
        "supervisor",
        lambda state: state["messages"][-1].name,
        {
            "enhancer": "enhancer",
            "researcher": "researcher",
            "coder": "coder",
            "normal": "normal",
        }
    )
    graph.add_conditional_edges(
        "validator",
        lambda state: "supervisor" if state["messages"][-1].name == "supervisor" else END,
        {
            "supervisor": "supervisor",
            END: END,
        }
    )

    runnable = graph.compile(checkpointer=memory)
    return runnable

runnable = create_graph()