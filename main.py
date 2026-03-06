from app.ingest import load_documents
from app.chunking import chunk_documents


def main():

    print("\nLoading documents...\n")
    documents = load_documents()

    print("\nCreating chunks...\n")
    chunks = chunk_documents(documents)

    print("\nTotal chunks created:", len(chunks))

    print("\nExample chunk:\n")
    print(chunks[0]["chunk_text"][:500])


if __name__ == "__main__":
    main()