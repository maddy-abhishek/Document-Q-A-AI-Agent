# Document Q&A AI Agent with Groq and Tavily Search

This is a Streamlit web application that allows you to chat with your PDF documents, search the web, and find research papers on Arxiv, powered by the high-speed Groq API.

# Features
  - Chat with Documents: Upload multiple PDF documents and ask questions about their content.

  - Web Search: Ask general questions, and the agent will use Tavily to search the web for answers.

  - Academic Search: Ask the agent to find papers on Arxiv on a specific topic.

  - High-Speed Responses: Powered by the Groq API for fast language model inference.


# Setup and Installation

1. Create a virtual environment:                  python -m venv venv

2. activate venv                                  venv\Scripts\activate

3. Install the required libraries:                pip install -r requirements.txt

4. Set up your API Keys:
   
   - Create a .env file in the project root directory.
  
   - Add your API keys to the .env file. You will need keys from both Groq and Tavily AI.

# How to Run the Application

1. Run the Streamlit app from your terminal:      streamlit run app.py

2. Open your web browser and go to the local URL provided by Streamlit (usually http://localhost:8501).

3. Using the App:

  - Use the sidebar to upload your PDF documents.

  - Click the "Process Documents" button to enable the agent.

  - Use the single chat input to ask questions. The agent will decide whether to answer from your documents, search the web, or look for papers on Arxiv.

  - Example prompts:

      - "What is the main conclusion of the document I uploaded?"

      - "What is the weather in London today?"

      - "Search Arxiv for papers on large language models."
