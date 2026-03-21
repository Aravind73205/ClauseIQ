from app.model import model
import numpy as np


def retrieve(query, index, chunks, top_k=10):
    """
    Retrieve top_k relevant chunks for a given query.
    """

    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []

    for i, idx in enumerate(indices[0]):
        results.append({
            "chunk_text": chunks[idx]["chunk_text"],
            "doc_name": chunks[idx]["doc_name"],
            "score": float(distances[0][i])
        })

    return results