from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
import os
    

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Converting text chunks into embedding vectors.
    """
    print("\nGenerating embeddings..\n")

    #extracting only the txt content from chunk objects.
    texts = [chunk["chunk_text"] for chunk in chunks] 
    embeddings = model.encode(texts)

    return np.array(embeddings)


def build_vector_store(embeddings):
    """
    Create FAISS index from embeddings
    """
    
    print("\nBuilding vector store...\n")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index

def save_vector_store(index, chunks):
    """
    Save the FAISS vector index and corresponding chunk metadata to disk.
    """

    os.makedirs("vector_store", exist_ok=True)

    faiss.write_index(index, "vector_store/index.faiss")

    with open("vector_store/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print("\nVector store saved successfully.\n")

def load_vector_store():
    """
    Load the FAISS vector index and chunk metadata from disk
    """

    if not os.path.exists("vector_store/index.faiss"):
        return None, None

    index = faiss.read_index("vector_store/index.faiss")

    with open("vector_store/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    print("\nLoaded existing vector store.\n")

    return index, chunks