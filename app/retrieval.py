from app.model import model
import numpy as np


def retrieve(query, index, chunks, top_k=3):
    """
    Retrieve top_k relevant chunks for a given query.
    """

    print("\nGenerating query embedding...\n")

    query_embedding = model.encode([query])

    print("\nSearching FAISS index...\n")

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []

    for idx in indices[0]:
        results.append(chunks[idx])

    return results