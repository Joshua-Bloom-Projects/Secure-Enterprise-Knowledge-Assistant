"""ChromaDB persistence and query helpers."""

from __future__ import annotations

from src.config import ensure_directories, get_config


def _chromadb():
    try:
        import chromadb
    except ImportError as exc:
        raise RuntimeError(
            "ChromaDB is not installed. Run `pip install -r requirements.txt` first."
        ) from exc
    return chromadb


def get_client():
    """Return a persistent ChromaDB client."""

    ensure_directories()
    chromadb = _chromadb()
    config = get_config()
    return chromadb.PersistentClient(path=str(config.chroma_db_dir))


def get_or_create_collection(reset: bool = False):
    """Return the policy collection, optionally rebuilding it from scratch."""

    config = get_config()
    client = get_client()

    if reset:
        try:
            client.delete_collection(config.collection_name)
            print(f"[store] Deleted existing collection: {config.collection_name}")
        except Exception:
            pass

    return client.get_or_create_collection(
        name=config.collection_name,
        metadata={"hnsw:space": "cosine"},
    )


def upsert_chunks(chunks: list[dict], embeddings: list[list[float]]) -> int:
    """Store chunk text, metadata, embeddings, and IDs in ChromaDB."""

    if len(chunks) != len(embeddings):
        raise ValueError("Chunk count and embedding count do not match.")
    if not chunks:
        return 0

    collection = get_or_create_collection(reset=True)
    collection.upsert(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks],
        embeddings=embeddings,
    )
    return len(chunks)


def query_by_embedding(embedding: list[float], top_k: int = 5) -> list[dict]:
    """Query ChromaDB by embedding and return clean result dictionaries."""

    config = get_config()
    client = get_client()

    try:
        collection = client.get_collection(config.collection_name)
    except Exception:
        return []

    try:
        if collection.count() == 0:
            return []
        results = collection.query(query_embeddings=[embedding], n_results=top_k)
    except Exception as exc:
        raise RuntimeError(f"ChromaDB query failed: {exc}") from exc

    ids = results.get("ids", [[]])[0]
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    clean_results: list[dict] = []
    for index, chunk_id in enumerate(ids):
        clean_results.append(
            {
                "id": chunk_id,
                "text": documents[index] if index < len(documents) else "",
                "metadata": metadatas[index] if index < len(metadatas) else {},
                "distance": distances[index] if index < len(distances) else None,
            }
        )

    return clean_results
