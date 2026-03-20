import re

def text_to_chunks(text, chunk_size=500, overlap=100):
    """
    Split text into chunks without breaking sentences.
    """

    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def chunk_documents(documents):
    """
    Takes list of documents and converts them into chunks.
    """

    all_chunks = []

    for doc in documents:

        doc_name = doc["doc_name"]
        text = doc["text"]

        chunks = text_to_chunks(text)

        for i, chunk in enumerate(chunks):

            chunk_data = {
                "doc_name": doc_name,
                "chunk_id": i,
                "chunk_text": chunk
            }

            all_chunks.append(chunk_data)

    return all_chunks