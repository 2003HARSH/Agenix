from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState
from config.llm_tools import llm, python_repl_tool
from langgraph.types import Command
from typing import Literal


def code_node(state: MessagesState) -> Command[Literal["validator"]]:

    code_agent = create_react_agent( #either u have created a subgraph here or use this method which creates a subgraph automatically
        llm,
        tools=[python_repl_tool],
        state_modifier=(
            "You are a coder and analyst. Focus on mathematical calculations, analyzing, solving math questions, "
            "and executing code. Handle technical problem-solving and data tasks."
        )
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