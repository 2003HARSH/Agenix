# Agenix/agents/researcher.py
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from langgraph.graph import  MessagesState
from config.llm_tools import search_llm, tavily_search
from langgraph.types import Command
from typing import Literal


def research_node(state: MessagesState) -> Command[Literal["validator"]]:
    """
    Research agent node that gathers information using Tavily search.
    Takes the current task state, performs relevant research,
    and returns findings for validation.
    """
    system_prompt = (
        "You are an Information Specialist with expertise in comprehensive research. Your responsibilities include:\n\n"
        "0. If you don't know anything you can do google search to find relevant information.\n"
        "1. Identifying key information needs based on the query context\n"
        "2. Gathering relevant, accurate, and up-to-date information from reliable sources\n"
        "3. Organizing findings in a structured, easily digestible format\n"
        "4. Citing sources when possible to establish credibility\n"
        "5. Focusing exclusively on information gathering - avoid analysis or implementation\n\n"
        "Provide thorough, factual responses without speculation where information is unavailable."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{messages}"),
        ]
    )
    
    research_agent = create_react_agent(
        search_llm,  
        tools=[tavily_search],  
        prompt=prompt
    )

    result = research_agent.invoke(state)

    print(f"--- Workflow Transition: Researcher → Validator ---")

    return Command(
        update={
            "messages": [ 
                HumanMessage(
                    content=result["messages"][-1].content,  
                    name="researcher"  
                )
            ]
        },
        goto="validator", 
    )