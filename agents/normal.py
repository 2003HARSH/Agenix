from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.types import Command
from typing import Literal
from langgraph.graph import END
from langchain_google_genai import ChatGoogleGenerativeAI


def normal_node(state: MessagesState) -> Command[Literal["passthrough"]]:
    llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

    result = llm.invoke(state['messages'])

    print(f"--- Workflow Transition: Normal → Passthrough ---")

    return Command(
        update={
            "messages": [
                HumanMessage(content=result.content, name="normal")
            ]
        },
        goto='passthrough',
    )