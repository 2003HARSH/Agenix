# Agenix/agents/researcher.py
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
from langgraph.graph import  MessagesState
from langgraph.types import Command
from typing import Literal
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI



def research_node(state: MessagesState) -> Command[Literal["passthrough"]]:
    """
    Research agent node that gathers information using Tavily search.
    Takes the current task state, performs relevant research,
    and returns findings for validation.
    """
    # --- START OF CORRECTED PROMPT ---
    system_prompt = (
        "You are an Information Specialist. Your primary purpose is to find information on the internet. "
        "You must use the tavily_search tool to answer questions. "
        "Do not rely on your internal knowledge. If the user asks for any information, especially real-time data like weather or current events, "
        "you must call the search tool."
    )
    # --- END OF CORRECTED PROMPT ---

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{messages}"),
        ]
    )
    llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    tavily_search = TavilySearchResults(llm=llm, max_results=3)
    
    research_agent = create_react_agent(
        llm=llm,  
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
        goto="passthrough", 
    )