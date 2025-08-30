from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

search_llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
# llm = ChatGroq(model="llama-3.3-70b-versatile")
tavily_search = TavilySearchResults(max_results=5)
python_repl_tool = PythonREPLTool()