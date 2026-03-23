import streamlit as st

from app.chunking import chunk_documents
from app.embeddings import create_embeddings, build_vector_store
from app.retrieval import retrieve
from app.llm import generate_answer

from app.ingest import load_documents  

import tempfile
import os
from pypdf import PdfReader


st.set_page_config(page_title="ClauseIQ", layout="wide")

st.title("📄 ClauseIQ — Chat with your PDF")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:

    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    st.success("PDF uploaded successfully!")

    # extract text
    reader = PdfReader(temp_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    # convert to document format
    documents = [{
        "doc_name": uploaded_file.name,
        "text": text
    }]

    # chunking
    chunks = chunk_documents(documents)

    # embedding
    embeddings = create_embeddings(chunks)

    # vector store
    index = build_vector_store(embeddings)

    st.success("Document processed! You can now ask questions.")

    # query input
    query = st.text_input("Ask a question")

    if query:
        results = retrieve(query, index, chunks)
        answer = generate_answer(query, results)

        st.subheader("Answer")
        st.write(answer)