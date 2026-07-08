"""JSONL interaction logging for evaluation and demo feedback."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from src.config import ensure_directories, get_config
from src.utils import utc_now_iso


def _log_path() -> Path:
    ensure_directories()
    return get_config().log_file_path


def _source_field(sources: list[dict], key: str) -> list:
    values = []
    for source in sources:
        value = source.get(key)
        if value and value not in values:
            values.append(value)
    return values


def log_interaction(
    *,
    question: str,
    risk_category: str,
    answer: str,
    refused: bool,
    sources: list[dict] | None = None,
    used_context: list[dict] | None = None,
    feedback: str | None = None,
) -> str:
    """Append one interaction to the JSONL log and return its log ID."""

    sources = sources or []
    used_context = used_context or []
    log_id = str(uuid.uuid4())
    entry = {
        "log_id": log_id,
        "timestamp": utc_now_iso(),
        "question": question,
        "risk_category": risk_category,
        "answer": answer,
        "refused": refused,
        "source_documents_used": _source_field(sources, "document_name"),
        "source_sections_used": _source_field(sources, "section_title"),
        "chunk_ids_used": [
            chunk.get("metadata", {}).get("chunk_id", chunk.get("id"))
            for chunk in used_context
            if chunk.get("metadata", {}).get("chunk_id", chunk.get("id"))
        ],
        "sources": sources,
        "feedback": feedback,
    }

    path = _log_path()
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=True) + "\n")

    return log_id


def update_feedback(log_id: str, feedback: str) -> bool:
    """Update feedback for an existing log entry."""

    path = _log_path()
    if not path.exists():
        return False

    updated = False
    entries: list[dict] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("log_id") == log_id:
                entry["feedback"] = feedback
                entry["feedback_timestamp"] = utc_now_iso()
                updated = True
            entries.append(entry)

    if updated:
        with path.open("w", encoding="utf-8") as file:
            for entry in entries:
                file.write(json.dumps(entry, ensure_ascii=True) + "\n")

    return updated
