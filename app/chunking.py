def text_to_chunks(text, chunk_size=500, overlap=100):
    """
    Splits a large text string into overlapping chunks.
    """

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()

        if chunk:  # only add non empty chunks
            chunks.append(chunk)

        if end == text_length:
            break

        # move start forward with overlap
        start = end - overlap

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