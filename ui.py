import streamlit as st
import tempfile
import os, signal
from pypdf import PdfReader

from app.chunking import chunk_documents
from app.embeddings import create_embeddings, build_vector_store
from app.retrieval import retrieve
from app.llm import generate_answer


st.set_page_config(
    page_title="ClauseIQ",
    page_icon="📄",
    layout="wide"
)

# CSS for input bar
st.markdown("""
<style>
.stChatInputContainer,
div[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 1.5rem !important;
    left: calc(50vw + 122px) !important;
    transform: translateX(-50%) !important;
    width: calc((100vw - 244px) * 0.52) !important;
    z-index: 999 !important;
}
.main .block-container {
    padding-bottom: 6rem !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📂 Upload Document")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips")
st.sidebar.markdown("""
- Ask clear questions  
- Try: *"What is KYC?"*  
- Ask summaries or definitions  
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚠️ Note")
st.sidebar.markdown("""
- Answers are based ONLY on uploaded document  
- No external knowledge used  
""")

st.sidebar.markdown("---")
if st.sidebar.button("⏹️ End Chat"):
    os.kill(os.getpid(), signal.SIGTERM)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_file" not in st.session_state:
    st.session_state.current_file = None
if "index" not in st.session_state:
    st.session_state.index = None
    st.session_state.chunks = None

# File upload + processing
if uploaded_file:
    if uploaded_file.name != st.session_state.current_file:
        st.session_state.current_file = uploaded_file.name
        st.session_state.messages = []

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

        with st.spinner("Processing document..."):
            reader = PdfReader(temp_path)
            text = "".join(page.extract_text() or "" for page in reader.pages)

            if not text.strip():
                st.error("Could not extract text from this PDF. It may be a scanned image based file.")
                st.stop()

            documents = [{"doc_name": uploaded_file.name, "text": text}]
            chunks = chunk_documents(documents)
            embeddings = create_embeddings(chunks)
            index = build_vector_store(embeddings)

            st.session_state.index = index
            st.session_state.chunks = chunks

# Center layout
_, center, _ = st.columns([1, 2, 1])

with center:
    st.markdown("# 📄 ClauseIQ")
    st.markdown("### Chat with your documents using AI")
    st.markdown("<br>", unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if st.session_state.get("thinking"):
        last_user_msg = next(
            (m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"),
            None
        )
        if last_user_msg:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    results = retrieve(last_user_msg, st.session_state.index, st.session_state.chunks)
                    answer = generate_answer(last_user_msg, results)

            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer
            })
        st.session_state.thinking = False
        st.rerun()

# Input bar
query = st.chat_input("Ask a question about your document...")

if query and st.session_state.index:

    st.session_state.messages.append({
        "role": "user", 
        "content": query
    })
    st.session_state.thinking = True
    st.rerun()