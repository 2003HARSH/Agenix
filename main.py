import streamlit as st
from langgraph.graph import StateGraph, START, MessagesState
from uuid import uuid4
import time 
from langgraph.graph import StateGraph, START, MessagesState
from agents.supervisor import supervisor_node
from agents.enhancer import enhancer_node
from agents.researcher import research_node
from agents.coder import code_node
from agents.validator import validator_node
from agents.normal import normal_node
import os
from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

os.environ["LANGCHAIN_TRACING_V2"] = "true"


sqlite_conn=sqlite3.connect("checkpoint.sqlite",check_same_thread=False)

memory=SqliteSaver(sqlite_conn)


if 'thread_id' not in st.session_state:
    st.session_state.thread_id = uuid4()

config = {
    'configurable': {
        'thread_id': st.session_state.thread_id
    }
}   

graph = StateGraph(MessagesState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("enhancer", enhancer_node)
graph.add_node("researcher", research_node)
graph.add_node("coder", code_node)
graph.add_node("validator", validator_node)
graph.add_node("normal", normal_node)

graph.add_edge(START, "supervisor")



app = graph.compile(checkpointer=memory)


st.set_page_config(page_title="Supervisor Based Multi-Agent Chatbot", page_icon="💬")
st.title("Supervisor Based Multi-Agent Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What do you want to do?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    inputs = {"messages": [("user", prompt)]}

    with st.chat_message("ai"):
        message_placeholder = st.empty()
        full_response = ""
        current_agent_status = st.empty() 

        for event in app.stream(inputs, config=config):
            for key, value in event.items():
                if value is None:
                    continue

                last_message = value.get("messages", [])[-1] if "messages" in value else None

                if last_message:
                    if hasattr(last_message, 'content'):
                        message_content = last_message.content
                        message_type = last_message.type 
                    elif isinstance(last_message, tuple):
                        message_type, message_content = last_message
                    else: 
                        message_content = str(last_message)
                        message_type = "tool" 

                    if "thinking..." in message_content.lower() or "working..." in message_content.lower() or "searching..." in message_content.lower():
                        current_agent_status.markdown(f"*{message_content}*")
                    else:
                        full_response += message_content + " " 
                        message_placeholder.markdown(full_response + "▌") 
                        current_agent_status.empty() 

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "ai", "content": full_response})