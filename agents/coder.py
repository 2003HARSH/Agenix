# Agenix/agents/coder.py
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState
from config.llm_tools import llm, python_repl_tool
from langgraph.types import Command
from typing import Literal


def code_node(state: MessagesState) -> Command[Literal["validator"]]:
    # Define the system prompt for the agent
    system_prompt = (
        "You are a coder and analyst. Focus on mathematical calculations, analyzing, solving math questions, "
        "and executing code. Handle technical problem-solving and data tasks."
    )

    # Create a prompt template that includes the system message and a placeholder for the chat history
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{messages}"),
        ]
    )

    # Pass the prompt template to the 'prompt' argument
    code_agent = create_react_agent(
        llm,
        tools=[python_repl_tool],
        prompt=prompt
    )

    result = code_agent.invoke(state)

    print(f"--- Workflow Transition: Coder → Validator ---")

    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="coder")
            ]
        },
        goto="validator",
    )