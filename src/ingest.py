"""CLI ingestion pipeline for Northstar policy PDFs."""

from __future__ import annotations

from src.chunker import chunk_pages
from src.config import ensure_directories, get_config
from src.embeddings import embed_document_chunks
from src.pdf_loader import load_all_pdfs
from src.vector_store import get_or_create_collection, upsert_chunks


def main() -> None:
    ensure_directories()
    config = get_config()

    print("Secure Enterprise Knowledge Assistant ingestion")
    print(f"Source folder: {config.source_documents_dir}")
    print(f"ChromaDB folder: {config.chroma_db_dir}")
    print(f"Collection: {config.collection_name}")
    print("")

    pages, stats = load_all_pdfs(config.source_documents_dir)
    chunks = chunk_pages(pages)

    if not chunks:
        get_or_create_collection(reset=True)
        print("\nNo chunks were created. Add readable PDFs and run ingestion again.")
        print("\nSummary")
        print(f"- PDFs processed: {stats['pdfs_processed']} of {stats['pdfs_found']}")
        print("- Chunks created: 0")
        print(f"- Collection: {config.collection_name}")
        print(f"- Storage location: {config.chroma_db_dir}")
        return

    print(f"\n[embed] Creating embeddings for {len(chunks)} chunks...")
    embeddings = embed_document_chunks(chunks)

    print("[store] Writing chunks to ChromaDB...")
    stored_count = upsert_chunks(chunks, embeddings)

    print("\nSummary")
    print(f"- PDFs processed: {stats['pdfs_processed']} of {stats['pdfs_found']}")
    print(f"- Pages extracted: {stats['pages_extracted']}")
    print(f"- Chunks created: {len(chunks)}")
    print(f"- Chunks stored: {stored_count}")
    print(f"- Collection: {config.collection_name}")
    print(f"- Storage location: {config.chroma_db_dir}")


if __name__ == "__main__":
    main()
