"""Chunk PDF page text into retrieval-sized passages."""

from __future__ import annotations

import re

from src.utils import slugify


DEFAULT_CHUNK_SIZE = 900
DEFAULT_CHUNK_OVERLAP = 150
DEFAULT_SECTION_TITLE = "General"


def detect_section_title(line: str) -> str | None:
    """Detect markdown-like or numbered section headings."""

    stripped = line.strip()
    if not stripped:
        return None

    markdown_match = re.match(r"^#{1,6}\s+(.+)$", stripped)
    if markdown_match:
        return markdown_match.group(1).strip()

    numbered_match = re.match(r"^(\d+(?:\.\d+)*\.?\s+[A-Z][A-Za-z0-9 ,&()/:-]+)$", stripped)
    if numbered_match and len(stripped) <= 90:
        return numbered_match.group(1).strip()

    return None


def _section_positions(text: str) -> list[tuple[int, str]]:
    positions: list[tuple[int, str]] = [(0, DEFAULT_SECTION_TITLE)]
    for match in re.finditer(r"^(.+)$", text, flags=re.MULTILINE):
        section_title = detect_section_title(match.group(1))
        if section_title:
            positions.append((match.start(), section_title))
    return positions


def _section_for_offset(positions: list[tuple[int, str]], offset: int) -> str:
    section_title = DEFAULT_SECTION_TITLE
    for position, title in positions:
        if position > offset:
            break
        section_title = title
    return section_title


def _choose_chunk_end(text: str, start: int, max_end: int, chunk_size: int) -> int:
    if max_end >= len(text):
        return len(text)

    min_break = start + max(chunk_size // 2, 1)
    newline_break = text.rfind("\n", min_break, max_end)
    if newline_break > start:
        return newline_break

    space_break = text.rfind(" ", min_break, max_end)
    if space_break > start:
        return space_break

    return max_end


def chunk_pages(
    pages: list[dict],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict]:
    """Create metadata-rich chunks from extracted PDF pages."""

    chunks: list[dict] = []

    for page in pages:
        text = page.get("text", "").strip()
        if not text:
            continue

        metadata = page.get("metadata", {})
        document_name = metadata.get("document_name", "unknown_document.pdf")
        page_number = int(metadata.get("page_number", 0))
        source_path = metadata.get("source_path", "")
        positions = _section_positions(text)

        start = 0
        chunk_index = 0
        while start < len(text):
            max_end = min(start + chunk_size, len(text))
            end = _choose_chunk_end(text, start, max_end, chunk_size)
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk_id = (
                    f"{slugify(document_name)}_p{page_number:03d}_c{chunk_index:03d}"
                )
                section_title = _section_for_offset(positions, start)
                chunk_metadata = {
                    "chunk_id": chunk_id,
                    "document_name": document_name,
                    "page_number": page_number,
                    "section_title": section_title,
                    "source_path": source_path,
                }
                chunks.append(
                    {
                        "id": chunk_id,
                        "text": chunk_text,
                        "metadata": chunk_metadata,
                    }
                )
                chunk_index += 1

            if end >= len(text):
                break

            next_start = max(end - overlap, start + 1)
            start = next_start

    return chunks
