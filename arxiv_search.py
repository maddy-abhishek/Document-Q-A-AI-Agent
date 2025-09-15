import arxiv
import streamlit as st

def search_arxiv(query: str, max_results=3) -> str:
    """
    Searches the Arxiv API for a given query and returns a formatted string with results.
    This function is designed to be used as a tool by a LangChain agent.

    Args:
        query (str): The search query.
        max_results (int): The maximum number of results to return.

    Returns:
        str: A formatted string containing the search results, or an error message.
    """
    if not query:
        return "Please provide a search query."

    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = list(client.results(search))

        if not results:
            return f"No papers found on Arxiv for the query: '{query}'."

        formatted_results = f"Here are the top {len(results)} papers I found on Arxiv for '{query}':\n\n"
        for i, result in enumerate(results):
            authors = ", ".join(author.name for author in result.authors)
            formatted_results += f"**{i+1}. {result.title}**\n"
            formatted_results += f"   - **Authors:** {authors}\n"
            formatted_results += f"   - **Published:** {result.published.strftime('%Y-%m-%d')}\n"
            formatted_results += f"   - **Abstract:** {result.summary[:400]}...\n"
            formatted_results += f"   - **PDF Link:** {result.pdf_url}\n\n"

        return formatted_results

    except Exception as e:
        # Avoid showing errors directly to the agent, just return a helpful message.
        print(f"An error occurred while searching Arxiv: {e}")
        return "Sorry, I couldn't perform the Arxiv search at the moment. There might be an issue with the service."

