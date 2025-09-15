from langchain.agents import Tool
from langchain_tavily import TavilySearch
from arxiv_search import search_arxiv
from dotenv import load_dotenv
load_dotenv()


# 1. Tavily Search Tool for general web searches
# This tool will use the TAVILY_API_KEY from the .env file
try:
    tavily_tool = TavilySearch(
    max_results=5,
    topic="general",
)
except Exception as e:
    print(f"Could not initialize Tavily Search Tool: {e}")
    tavily_tool = None

# 2. Arxiv Search Tool for academic paper lookups
arxiv_tool = Tool(
    name="ArxivSearch",
    func=search_arxiv,
    description="Use this tool to search for academic papers on Arxiv.org. The input should be a specific search query, like a paper title or topic."
)