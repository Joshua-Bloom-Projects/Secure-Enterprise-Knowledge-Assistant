"""Small shared helpers."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def utc_now_iso() -> str:
    """Return a UTC timestamp safe for logs."""

    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    """Create a stable lowercase identifier from a file or section name."""

    stem = Path(value).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "_", stem)
    return stem.strip("_") or "document"


def clean_text(value: str) -> str:
    """Normalize repeated whitespace while preserving paragraph breaks."""

    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def unique_sources(chunks: Iterable[dict]) -> list[dict]:
    """Return unique source citations from retrieved chunks."""

    seen: set[tuple[str, str, int | str]] = set()
    sources: list[dict] = []
    for chunk in chunks:
        metadata = chunk.get("metadata", {})
        document_name = metadata.get("document_name", "Unknown document")
        section_title = metadata.get("section_title", "General")
        page_number = metadata.get("page_number", "Unknown")
        key = (document_name, section_title, page_number)
        if key in seen:
            continue
        seen.add(key)
        sources.append(
            {
                "document_name": document_name,
                "section_title": section_title,
                "page_number": page_number,
                "chunk_id": metadata.get("chunk_id", chunk.get("id", "")),
            }
        )
    return sources


def format_source(source: dict) -> str:
    """Format a source citation for display."""

    document_name = source.get("document_name", "Unknown document")
    section_title = source.get("section_title", "General")
    page_number = source.get("page_number", "Unknown")
    return f"{document_name}, Section {section_title}, page {page_number}"
