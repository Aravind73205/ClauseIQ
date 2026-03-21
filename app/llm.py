from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash" 


def generate_answer(query, chunks):
    """
    Generate answer using retrieved chunks (RAG).
    """

    clean_chunks = []

    for chunk in chunks:
        text = chunk["chunk_text"].replace("\n", " ").strip() 

        if len(text) > 50:  # remove tiny useless chunks
            clean_chunks.append({
                "doc_name": chunk["doc_name"],
                "chunk_text": text
            })

    chunks = clean_chunks[:7] # limit to top 7 chunks

    context = "\n\n".join([
        f"[Source: {c['doc_name']}]\n{c['chunk_text']}"
        for c in chunks
    ])


    prompt = f"""
You are a financial compliance assistant.

Use ONLY the provided context to answer the question.

If the answer is clearly present in the context, answer confidently.

If the context contains partial information, answer based on it but mention that the information is limited.

If the answer is NOT present in the context, say:
"Not found in provided documents."

DO NOT use external knowledge.

After answering, include sources used.

Context:
{context}

Question:
{query}

Answer in a clear and simple way:
"""
    

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text