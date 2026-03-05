from pypdf import PdfReader
from pathlib import Path


def read_extract_pdf(file_path):
    """
    Read and Extract all txt from a Pdf file.
    """
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        # sometimes pdf pgs may empty
        if page_text:         
            text += page_text + "\n"

    return text


def load_documents():
    """
    Loads all pdfs from the folder.
    return a list of dictionaries with document name and text.
    """

    docs_path = Path("data/documents")
    documents = []

    for pdf_file in docs_path.glob("*.pdf"):

        print(f"\n--- Reading: {pdf_file.name} ---")

        text = read_extract_pdf(pdf_file)

        document_data = {
            "doc_name": pdf_file.name,
            "text": text
        }

        documents.append(document_data)

        # just preview
        print(text[:500])


    return documents

if __name__ == "__main__":
   
    print("\nLoading pdfs from documents...\n")
 
    docs = load_documents()

    print("\nTotal documents loaded:", len(docs))
