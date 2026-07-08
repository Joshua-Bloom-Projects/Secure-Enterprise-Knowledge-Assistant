"""OpenAI embedding helpers."""

from __future__ import annotations

from collections.abc import Sequence

from src.config import get_config


def _client():
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "The OpenAI SDK is not installed. Run `pip install -r requirements.txt` first."
        ) from exc

    config = get_config()
    if not config.openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return OpenAI(api_key=config.openai_api_key)


def embed_texts(texts: Sequence[str], batch_size: int = 96) -> list[list[float]]:
    """Embed multiple texts using the configured OpenAI embedding model."""

    if not texts:
        return []

    config = get_config()
    client = _client()
    embeddings: list[list[float]] = []

    try:
        for start in range(0, len(texts), batch_size):
            batch = list(texts[start : start + batch_size])
            response = client.embeddings.create(
                model=config.embedding_model,
                input=batch,
            )
            sorted_items = sorted(response.data, key=lambda item: item.index)
            embeddings.extend([item.embedding for item in sorted_items])
    except Exception as exc:
        raise RuntimeError(f"OpenAI embedding request failed: {exc}") from exc

    return embeddings


def embed_query(question: str) -> list[float]:
    """Embed one user question."""

    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")
    return embed_texts([question])[0]


def embed_document_chunks(chunks: Sequence[dict]) -> list[list[float]]:
    """Embed chunk dictionaries by their text field."""

    return embed_texts([chunk["text"] for chunk in chunks])
