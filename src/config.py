"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

try:
    from dotenv import load_dotenv

    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    # Dependencies may not be installed yet. Runtime commands will still show a
    # clear error if a required package is missing.
    pass


def _path_from_env(name: str, default: str) -> Path:
    value = os.getenv(name, default)
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


@dataclass(frozen=True)
class AppConfig:
    openai_api_key: str
    embedding_model: str
    answer_model: str
    chroma_db_dir: Path
    collection_name: str
    source_documents_dir: Path
    log_file_path: Path


def get_config() -> AppConfig:
    """Return current app config using environment variables and defaults."""

    return AppConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        answer_model=os.getenv("OPENAI_ANSWER_MODEL", "gpt-5.5"),
        chroma_db_dir=_path_from_env("CHROMA_DB_DIR", "data/chroma_db"),
        collection_name=os.getenv(
            "CHROMA_COLLECTION_NAME", "northstar_policy_documents"
        ),
        source_documents_dir=_path_from_env(
            "SOURCE_DOCUMENTS_DIR", "source_documents"
        ),
        log_file_path=_path_from_env("LOG_FILE_PATH", "data/logs/question_log.jsonl"),
    )


def ensure_directories() -> None:
    """Create local runtime directories used by ingestion and logging."""

    config = get_config()
    config.source_documents_dir.mkdir(parents=True, exist_ok=True)
    config.chroma_db_dir.mkdir(parents=True, exist_ok=True)
    config.log_file_path.parent.mkdir(parents=True, exist_ok=True)
