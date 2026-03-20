from app.ingest import load_documents
from app.chunking import chunk_documents
from app.embeddings import (
    create_embeddings,
    build_vector_store,
    save_vector_store,
    load_vector_store
)
from app.retrieval import retrieve
from app.llm import generate_answer


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

    while True:
        query = input("\nAsk a question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        results = retrieve(query, index, chunks)

        answer = generate_answer(query, results)

        print("\nFinal Answer:\n")
        print(answer)
        print("=" * 60)


if __name__ == "__main__":
    main()