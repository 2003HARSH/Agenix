from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command
from typing import Literal
from config.llm_tools import llm
from langgraph.graph import END


def normal_node(state: MessagesState) -> Command[Literal["validator"]]:

    result = llm.invoke(state['messages'])

    print(f"--- Workflow Transition: Normal → END ---")

    return Command(
        update={
            "messages": [
                HumanMessage(content=result.content, name="normal")
            ]
        },
        goto=END,
    )