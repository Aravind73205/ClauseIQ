from app.model import model
import numpy as np

def retrieve(query, index, chunks, top_k=10, threshold=2.0):
    """
    Retrieve relevant chunks with certain threshold.
    """

    query_embedding = model.encode([query])

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []

    for i, idx in enumerate(indices[0]):
        score = float(distances[0][i])

        if score < threshold:
            results.append({
                "chunk_text": chunks[idx]["chunk_text"],
                "doc_name": chunks[idx]["doc_name"],
                "score": score
            })

    return results