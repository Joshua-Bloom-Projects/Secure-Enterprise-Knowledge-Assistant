"""Question retrieval over the local ChromaDB collection."""

from __future__ import annotations

import argparse
import json

from src.embeddings import embed_query
from src.vector_store import query_by_embedding


def retrieve_context(question: str, top_k: int = 5) -> list[dict]:
    """Retrieve relevant chunks for a user question."""

    if not question.strip():
        return []

    question_embedding = embed_query(question)
    return query_by_embedding(question_embedding, top_k=top_k)


def main() -> None:
    parser = argparse.ArgumentParser(description="Test policy retrieval from the CLI.")
    parser.add_argument(
        "question",
        nargs="?",
        default="What approvals are required for a $6,000 software purchase?",
    )
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    results = retrieve_context(args.question, top_k=args.top_k)
    if not results:
        print("No chunks found. Run `python -m src.ingest` after adding PDFs.")
        return

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print(json.dumps(result["metadata"], indent=2))
        print(f"Distance: {result.get('distance')}")
        preview = result.get("text", "").replace("\n", " ")[:500]
        print(f"Text: {preview}")


if __name__ == "__main__":
    main()
