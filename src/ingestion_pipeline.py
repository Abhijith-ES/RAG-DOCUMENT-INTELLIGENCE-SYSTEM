from pathlib import Path
from src.pdf_loader import extract_text_from_pdf
from src.chunker import create_chunks
from src.embeddings import embed_text
from src.vector_store import create_faiss_index, save_faiss_index, save_metadata


VECTOR_DB_DIR = Path("vector_db")
VECTOR_DB_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def process_document(pdf_path: Path, document_id, embedding_model):
    # Extracting Pages From the PDF Document, the user uploads.
    extracted_pages = extract_text_from_pdf(pdf_path)

    # Creating Chunks of Extracted text.
    chunks = create_chunks(pages=extracted_pages, chunk_size=500, chunk_overlap=50)

    if not chunks:
        raise ValueError(
            "No text could be extracted from the PDF."
        )

    # Extract Texts From the chunks to create embeddings
    texts = [chunk["chunk"] for chunk in chunks]

    # Create Embeddings Of the Chunks created.
    embeddings = embed_text(texts, embedding_model)

    # The Embeddings are stored in faiss index.
    index = create_faiss_index(embeddings)

    # saving faiss index to the folder: /vector_db
    index_path = VECTOR_DB_DIR / f"{document_id}.faiss"

    save_faiss_index(index, index_path)

    # Saving Metadata
    metadata_path = VECTOR_DB_DIR / f"{document_id}.pkl"
    save_metadata(chunks, metadata_path)

    return {
        "document_id" : document_id,
        "chunks" : len(chunks)
    }