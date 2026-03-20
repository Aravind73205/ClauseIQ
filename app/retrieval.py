from app.model import model
import numpy as np


def retrieve(query, index, chunks, top_k=10, verbose =False):
    """
    Retrieve top_k relevant chunks for a given query.
    """
    if verbose: # for debugging retrieval quality
        print("\nGenerating query embedding...\n")

    query_embedding = model.encode([query])

    if verbose:
        print("\nSearching FAISS index...\n")

    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []

    for idx in indices[0]:
        results.append(chunks[idx])

    return results