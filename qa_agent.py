import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from tools import tavily_tool, arxiv_tool
import os

@st.cache_resource
def get_vector_store(text_chunks):
    """
    Creates a vector store from text chunks using HuggingFace embeddings.
    """
    if not text_chunks:
        return None
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)
        return vector_store
    except Exception as e:
        st.error(f"Failed to create vector store: {e}")
        return None

def get_agent_executor(vector_store=None):
    """
    Creates a conversational agent that can use tools.
    If a vector_store is provided, it adds a document retriever tool.
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if not groq_api_key or not tavily_api_key:
        st.error("Groq or Tavily API key is not set. Please add them to your .env file.")
        return None

    try:
        # Initialize the LLM
        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.1-8b-instant",
            temperature=0.2,
        )

        # Define the base list of tools
        tools = [arxiv_tool]
        if tavily_tool:
            tools.append(tavily_tool)
        else:
             st.warning("Tavily Search Tool is not available.")

        # If a vector store is provided, create and add the retriever tool
        if vector_store:
            retriever_tool = create_retriever_tool(
                vector_store.as_retriever(),
                "document_retriever",
                "Searches and returns relevant information from the uploaded PDF documents. Use this for any questions specifically about the provided documents."
            )
            tools.append(retriever_tool)

        # Get the prompt template
        prompt = hub.pull("hwchase17/react-chat")

        # Create the agent
        agent = create_react_agent(llm, tools, prompt)

        # Create the agent executor
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )

        return agent_executor

    except Exception as e:
        st.error(f"Failed to create agent executor: {e}")
        return None