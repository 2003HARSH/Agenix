from langgraph.graph import StateGraph, START, END, MessagesState
from agents.supervisor import supervisor_node
from agents.enhancer import enhancer_node
from agents.researcher import research_node
from agents.coder import code_node
from agents.validator import validator_node
from agents.normal import normal_node

from langgraph.checkpoint.memory import MemorySaver
from uuid import uuid4

memory=MemorySaver()

config={'configurable':{
    'thread_id':uuid4()
}}

# Create the graph
graph = StateGraph(MessagesState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("enhancer", enhancer_node)
graph.add_node("researcher", research_node)
graph.add_node("coder", code_node)
graph.add_node("validator", validator_node)
graph.add_node("normal",normal_node)

graph.add_edge(START, "supervisor")

app = graph.compile(checkpointer=memory)


while True:
    user_input=input("Enter your query")
    inputs = {
        "messages": [("user", user_input)]
    }
    for event in app.stream(inputs,config=config):
        for key, value in event.items():
            if value is None:
                continue
            last_message = value.get("messages", [])[-1] if "messages" in value else None
            print(last_message)
