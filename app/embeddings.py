from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
    

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Converting text chunks into embedding vectors.
    """
    
    #extracting only the txt content from chunk objects.
    texts = [chunk["chunk_text"] for chunk in chunks] 

    embeddings = model.encode(texts)

    return np.array(embeddings)


def build_vector_store(embeddings):
    """
    Create FAISS index from embeddings.
    """
    
    print("\nBuilding vector store...\n")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index