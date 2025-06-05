from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")
tavily_search = TavilySearchResults(max_results=2)
python_repl_tool = PythonREPLTool()