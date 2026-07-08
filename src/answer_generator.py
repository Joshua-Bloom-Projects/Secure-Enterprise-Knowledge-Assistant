"""Grounded answer generation using retrieved policy context."""

from __future__ import annotations

from src.config import get_config
from src.utils import format_source, unique_sources


NOT_ENOUGH_INFORMATION = (
    "I could not find enough information in the approved policy documents to "
    "answer that confidently."
)

SYSTEM_PROMPT = """You are the Secure Enterprise Knowledge Assistant for Northstar Operations Group.

You answer employee questions using only the approved policy context provided to you.

Rules:
1. Use only the retrieved context.
2. Do not use outside knowledge.
3. Do not guess.
4. If the retrieved context does not contain enough information, say:
"I could not find enough information in the approved policy documents to answer that confidently."
5. Always cite the source document, section title, and page number when available.
6. Do not approve requests, grant exceptions, sign contracts, authorize purchases, approve PTO, approve access, or make employment decisions.
7. For approval-related questions, explain the policy requirement and direct the user to the appropriate team.
8. Do not reveal confidential, restricted, personal, medical, payroll, credential, or private employee information.
9. If a user asks for legal advice, summarize the relevant policy if available and direct the user to Legal.
10. Keep answers clear, concise, and business-professional.

Answer format:
- Direct answer
- Relevant policy details
- Sources
- Escalation, if needed
"""


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


def _context_block(context_chunks: list[dict]) -> str:
    parts: list[str] = []
    for index, chunk in enumerate(context_chunks, start=1):
        metadata = chunk.get("metadata", {})
        source = format_source(metadata)
        chunk_id = metadata.get("chunk_id", chunk.get("id", f"chunk_{index}"))
        parts.append(
            f"[Context {index}]\n"
            f"Chunk ID: {chunk_id}\n"
            f"Source: {source}\n"
            f"Text:\n{chunk.get('text', '').strip()}"
        )
    return "\n\n".join(parts)


def _response_text(response) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text.strip()

    # Fallback for older SDK response shapes.
    chunks: list[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                chunks.append(text)
    return "\n".join(chunks).strip()


def generate_answer(question: str, context_chunks: list[dict]) -> dict:
    """Generate a grounded answer and return structured display data."""

    sources = unique_sources(context_chunks)

    if not context_chunks:
        return {
            "answer": NOT_ENOUGH_INFORMATION,
            "sources": [],
            "used_context": [],
            "refused": False,
        }

    config = get_config()
    client = _client()
    user_input = (
        "Question:\n"
        f"{question.strip()}\n\n"
        "Retrieved policy context:\n"
        f"{_context_block(context_chunks)}\n\n"
        "Write the answer using only the retrieved policy context."
    )

    try:
        response = client.responses.create(
            model=config.answer_model,
            instructions=SYSTEM_PROMPT,
            input=user_input,
        )
        answer = _response_text(response)
    except Exception as exc:
        raise RuntimeError(f"OpenAI answer generation failed: {exc}") from exc

    if not answer:
        answer = NOT_ENOUGH_INFORMATION

    return {
        "answer": answer,
        "sources": sources,
        "used_context": context_chunks,
        "refused": False,
    }
