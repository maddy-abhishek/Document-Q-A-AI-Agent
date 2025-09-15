import streamlit as st
from dotenv import load_dotenv
from document_ingestion import process_uploaded_files
from qa_agent import get_vector_store, get_agent_executor
from langchain_core.messages import HumanMessage, AIMessage

def handle_user_input(user_question):
    """
    Handles user input by passing it to the agent executor and displaying the response.
    """
    if st.session_state.agent_executor:
        with st.spinner("Thinking..."):
            response = st.session_state.agent_executor.invoke({
                "input": user_question,
                "chat_history": st.session_state.chat_history
            })

        st.session_state.chat_history.append(HumanMessage(content=user_question))
        st.session_state.chat_history.append(AIMessage(content=response.get("output", "Sorry, I encountered an error.")))

        # Rerun to display the latest messages
        st.rerun()
    else:
        st.warning("Agent not available. Please check your API keys in the .env file.")

def main():
    """
    Main function to run the Streamlit application.
    """
    load_dotenv()
    st.set_page_config(page_title="Document Q&A AI Agent", page_icon=":robot_face:")

    st.title("🤖 AI Agent by MADDY")
    st.write("I can search the web, find papers on Arxiv, and response answer from your documents.")

    # Initialize session state variables
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Initialize the agent executor on first run
    if "agent_executor" not in st.session_state:
        st.session_state.agent_executor = get_agent_executor() # Initialize without documents

    # Sidebar for Document Upload
    with st.sidebar:
        st.header("Your Documents")
        pdf_docs = st.file_uploader(
            "Upload PDFs to add document Q&A to the agent's abilities",
            type="pdf",
            accept_multiple_files=True
        )

        if st.button("Process Documents"):
            if pdf_docs:
                with st.spinner("Processing documents..."):
                    text_chunks = process_uploaded_files(pdf_docs)
                    if text_chunks:
                        vector_store = get_vector_store(text_chunks)
                        # Re-create the agent executor with the new document tool
                        st.session_state.agent_executor = get_agent_executor(vector_store)
                        st.success("Documents processed! The agent can now answer questions about them.")
                    else:
                        st.error("Could not extract text from the documents.")
            else:
                st.warning("Please upload at least one PDF file.")

    # Display chat history
    for message in st.session_state.chat_history:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

    # Chat input
    if user_question := st.chat_input("Ask about your documents or the web..."):
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_question)
        handle_user_input(user_question)

if __name__ == '__main__':
    main()