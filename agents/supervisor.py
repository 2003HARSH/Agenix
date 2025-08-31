# Agenix/agents/supervisor.py
from typing import Literal
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command
from langchain_google_genai import ChatGoogleGenerativeAI

class Supervisor(BaseModel):
    """Determines which specialist to activate next in the workflow."""
    next: Literal["enhancer", "researcher", "coder", "normal"]
    reason: str

def supervisor_node(state: MessagesState) -> Command[Literal["enhancer", "researcher", "coder", "normal"]]:
    
    # --- START OF CORRECTED PROMPT ---
    system_prompt = ('''
        You are a workflow supervisor managing a team of specialized agents. Your role is to analyze the user's request and route it to the most appropriate agent.

        **Team Members**:
        1. **Normal Agent**: For simple greetings, chit-chat, or conversational questions that don't require research or coding.
        2. **Prompt Enhancer**: Clarifies ambiguous requests or improves poorly defined queries.
        3. **Researcher**: Specializes in information gathering and fact-finding.
        4. **Coder**: Focuses on technical implementation, calculations, and coding solutions.

        **Your Responsibilities**:
        1. **Handle Greetings First**: If the user provides a simple greeting (e.g., 'hello', 'hi', 'how are you?'), route to the `normal` agent immediately.
        2. Analyze all other requests for completeness and route them to the best specialist.
        3. If a request is vague, route to the `enhancer`.
        4. If a request requires information, route to the `researcher`.
        5. If a request requires code or calculations, route to the `coder`.
    ''')
    # --- END OF CORRECTED PROMPT ---
    
    messages = [
        {"role": "system", "content": system_prompt},  
    ] + state["messages"] 

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

    response = llm.with_structured_output(Supervisor).invoke(messages)

    goto = response.next
    reason = response.reason

    print(f"--- Workflow Transition: Supervisor → {goto.upper()} ---")
    
    return Command(
        update={
            "messages": [
                HumanMessage(content=reason, name=goto)
            ]
        },
        goto=goto,  
    )