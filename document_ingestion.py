import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from tempfile import NamedTemporaryFile

def process_uploaded_files(uploaded_files):
    """
    Processes a list of uploaded PDF files, extracts text, and splits it into chunks.

    Args:
        uploaded_files (list): A list of files uploaded via Streamlit's file_uploader.

    Returns:
        list: A list of document chunks.
    """
    if not uploaded_files:
        return None

    all_chunks = []
    for uploaded_file in uploaded_files:
        try:
            # Create a temporary file to store the uploaded content
            with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            # Use PyPDFLoader to load the document
            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()

            # Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(documents)
            all_chunks.extend(chunks)

        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
        finally:
            # Clean up the temporary file
            if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    st.success(f"Processed {len(uploaded_files)} documents and created {len(all_chunks)} text chunks.")
    return all_chunks
