from app.ingest import load_documents
from app.chunking import chunk_documents
from app.embeddings import create_embeddings, build_vector_store


def main():

    print("\nLoading documents...\n")
    documents = load_documents()

    print("\nCreating chunks...\n")
    chunks = chunk_documents(documents)

    print(f"\nTotal chunks: {len(chunks)}")

    print("\nGenerating embeddings..\n")
    embeddings = create_embeddings(chunks)

    print("\nBuilding vector store...\n")
    index = build_vector_store(embeddings)

    print("\nVector store created successfully..!")

if __name__ == "__main__":
    main()