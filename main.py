from app.ingest import load_documents
from app.chunking import chunk_documents
from app.embeddings import (
    create_embeddings,
    build_vector_store,
    save_vector_store,
    load_vector_store
)


def main():

    index, chunks = load_vector_store()

    if index is None:

        print("\nLoading documents...\n")
        documents = load_documents()

        print("\nCreating chunks...\n")
        chunks = chunk_documents(documents)

        print(f"\nTotal chunks: {len(chunks)}")

        embeddings = create_embeddings(chunks)

        index = build_vector_store(embeddings)

        save_vector_store(index, chunks)

    else:
        print("\nVector store already exists. Skipping embedding step.\n")


if __name__ == "__main__":
    main()