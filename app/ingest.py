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
        if page_text:         # sometimes empty
            text += page_text + "\n"

    return text


def read_all_documents():
    docs_path = Path("data/documents")

    for pdf_file in docs_path.glob("*.pdf"):
        print(f"\n--- Reading: {pdf_file.name} ---")

        text = read_extract_pdf(pdf_file)

        # just preview
        print(text[:1000])


if __name__ == "__main__":
    print("Reading pdfs in data/documents ...\n")
    read_all_documents()
