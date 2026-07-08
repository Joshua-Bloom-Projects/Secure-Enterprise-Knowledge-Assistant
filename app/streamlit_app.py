"""Streamlit frontend for the Secure Enterprise Knowledge Assistant."""

from __future__ import annotations

from html import escape
import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.answer_generator import generate_answer
from src.guardrails import NORMAL, classify_question_risk, get_refusal_message
from src.logger import log_interaction, update_feedback
from src.retriever import retrieve_context


SAMPLE_QUESTION_GROUPS = {
    "Normal policy": [
        "How much PTO do full-time employees receive?",
        "What are the core collaboration hours for remote employees?",
    ],
    "Security / cross-document": [
        "Can I upload confidential company data into a public AI tool?",
        "What approvals are required for a $6,000 software purchase?",
    ],
    "Process lookup": [
        "How long does standard vendor onboarding take?",
        "How do I request access to a system?",
    ],
    "Approval refusal": [
        "Can you approve my PTO request?",
    ],
    "Sensitive-data refusal": [
        "Can you show me another employee's medical accommodation information?",
    ],
}

PIPELINE_STEPS = [
    ("01", "Approved PDFs"),
    ("02", "Chunking"),
    ("03", "Embeddings"),
    ("04", "ChromaDB"),
    ("05", "Retrieval"),
    ("06", "Grounded answer + citations"),
]

RISK_LABELS = {
    NORMAL: "Grounded retrieval",
    "approval_request": "Approval request refused",
    "personal_sensitive_data": "Sensitive data refused",
    "credential_or_access_abuse": "Credential/access abuse refused",
    "bypass_policy": "Policy bypass refused",
    "legal_advice": "Legal advice redirected",
}

RISK_DETAILS = {
    NORMAL: (
        "The assistant searched approved policy documents and generated an "
        "answer from retrieved context."
    ),
    "approval_request": (
        "The assistant stopped before retrieval because it cannot approve "
        "requests or grant exceptions."
    ),
    "personal_sensitive_data": (
        "The assistant stopped before retrieval because the request asks for "
        "private employee information."
    ),
    "credential_or_access_abuse": (
        "The assistant stopped before retrieval because the request involves "
        "credentials or access misuse."
    ),
    "bypass_policy": (
        "The assistant stopped before retrieval because it asks to bypass "
        "policy controls."
    ),
    "legal_advice": (
        "The assistant redirected the user because legal conclusions require "
        "Legal review."
    ),
}


def _document_count() -> int:
    return len(list((PROJECT_ROOT / "source_documents").glob("*.pdf")))


def _initialize_state() -> None:
    st.session_state.setdefault("question", "")
    st.session_state.setdefault("last_result", None)
    st.session_state.setdefault("last_log_id", None)
    st.session_state.setdefault("feedback_message", "")


def _apply_theme() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f7f8fb;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3 {
            color: #172033;
        }
        .hero {
            background: #ffffff;
            border: 1px solid #dfe5ef;
            border-radius: 8px;
            padding: 1.25rem 1.35rem;
            margin-bottom: 1rem;
        }
        .hero h1 {
            margin-bottom: 0.25rem;
        }
        .hero p {
            margin: 0;
            color: #46546b;
            font-size: 1rem;
        }
        .safety-note {
            background: #eef5ff;
            border: 1px solid #c8dbff;
            border-radius: 8px;
            color: #243b63;
            padding: 0.85rem 1rem;
            margin: 0.75rem 0 1rem;
        }
        .pipeline-card {
            background: #ffffff;
            border: 1px solid #dfe5ef;
            border-radius: 8px;
            padding: 0.8rem 0.8rem;
            min-height: 96px;
        }
        .pipeline-step {
            color: #65748b;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        .pipeline-label {
            color: #172033;
            font-weight: 700;
            margin-top: 0.35rem;
            line-height: 1.2;
        }
        .status-badge {
            border-radius: 999px;
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            margin: 0.2rem 0 0.75rem;
            padding: 0.3rem 0.65rem;
            text-transform: uppercase;
        }
        .status-normal {
            background: #e7f6ef;
            color: #135c3b;
        }
        .status-refused {
            background: #fff3d6;
            color: #7a4f00;
        }
        .metric-note {
            color: #65748b;
            font-size: 0.86rem;
            line-height: 1.35;
        }
        .source-row {
            background: #ffffff;
            border: 1px solid #dfe5ef;
            border-radius: 8px;
            padding: 0.75rem 0.85rem;
            margin-bottom: 0.5rem;
        }
        .source-title {
            color: #172033;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .source-meta {
            color: #65748b;
            font-size: 0.9rem;
        }
        .context-copy {
            color: #46546b;
            font-size: 0.92rem;
            margin-top: -0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _display_sidebar() -> None:
    st.sidebar.title("Demo Controls")
    st.sidebar.caption("Select a sample question, then submit it in the main panel.")

    for group_name, questions in SAMPLE_QUESTION_GROUPS.items():
        expanded = group_name in {"Normal policy", "Security / cross-document"}
        with st.sidebar.expander(group_name, expanded=expanded):
            for question in questions:
                if st.button(question, use_container_width=True):
                    st.session_state.question = question

    st.sidebar.divider()
    st.sidebar.subheader("Local Prototype")
    col1, col2 = st.sidebar.columns(2)
    col1.metric("Demo PDFs", _document_count())
    col2.metric("Runtime", "Local")
    st.sidebar.markdown(
        """
        <p class="metric-note">
        Vector data and interaction logs stay on this machine. The included
        documents are fictional Northstar policy PDFs.
        </p>
        """,
        unsafe_allow_html=True,
    )


def _display_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <h1>Secure Enterprise Knowledge Assistant</h1>
            <p>
            A local RAG prototype that answers employee policy questions from
            approved fictional documents with citations, guardrails, and
            evaluation logging.
            </p>
        </div>
        <div class="safety-note">
            Portfolio demo only: this uses fictional Northstar Operations Group
            documents and does not include SSO, role-based access control,
            document permissions, encryption, or enterprise deployment.
        </div>
        """,
        unsafe_allow_html=True,
    )


def _display_pipeline() -> None:
    st.subheader("How it works")
    columns = st.columns(len(PIPELINE_STEPS))
    for column, (number, label) in zip(columns, PIPELINE_STEPS):
        with column:
            st.markdown(
                f"""
                <div class="pipeline-card">
                    <div class="pipeline-step">Step {escape(number)}</div>
                    <div class="pipeline-label">{escape(label)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _status_badge(result: dict) -> None:
    risk_category = result.get("risk_category", NORMAL)
    refused = result.get("refused", False)
    label = RISK_LABELS.get(risk_category, risk_category.replace("_", " ").title())
    css_class = "status-refused" if refused else "status-normal"
    st.markdown(
        f'<span class="status-badge {css_class}">{escape(label)}</span>',
        unsafe_allow_html=True,
    )
    st.caption(
        RISK_DETAILS.get(risk_category, "The request was handled by the assistant.")
    )


def _display_sources(sources: list[dict], refused: bool) -> None:
    st.subheader("Sources")
    if not sources:
        message = (
            "No policy sources were used because this request was handled by "
            "guardrails before retrieval."
            if refused
            else "No policy sources were returned for this question."
        )
        st.info(message)
        return
    for source in sources:
        document_name = source.get("document_name", "Unknown document")
        section_title = source.get("section_title", "General")
        page_number = source.get("page_number", "Unknown")
        chunk_id = source.get("chunk_id", "")
        chunk_text = f" | Chunk {chunk_id}" if chunk_id else ""
        st.markdown(
            f"""
            <div class="source-row">
                <div class="source-title">{escape(document_name)}</div>
                <div class="source-meta">
                    Section: {escape(str(section_title))} |
                    Page: {escape(str(page_number))}{escape(chunk_text)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _display_context(chunks: list[dict]) -> None:
    st.subheader("Retrieved Context")
    st.markdown(
        '<p class="context-copy">Demo evidence: the exact chunks used to ground the answer.</p>',
        unsafe_allow_html=True,
    )
    with st.expander("Show retrieved chunks and metadata"):
        if not chunks:
            st.write("No retrieved chunks were used.")
            return

        for index, chunk in enumerate(chunks, start=1):
            metadata = chunk.get("metadata", {})
            distance = chunk.get("distance")
            chunk_id = metadata.get("chunk_id", chunk.get("id"))
            st.markdown(f"**Chunk {index}: {chunk_id}**")
            st.caption(
                f"{metadata.get('document_name', 'Unknown document')} | "
                f"Section {metadata.get('section_title', 'General')} | "
                f"Page {metadata.get('page_number', 'Unknown')} | "
                f"Distance: {distance}"
            )
            st.write(chunk.get("text", ""))


def _display_result(result: dict) -> None:
    _status_badge(result)

    st.subheader("Answer")
    if result.get("refused"):
        st.warning(result["answer"])
    else:
        with st.container(border=True):
            st.markdown(result["answer"])

    _display_sources(result.get("sources", []), result.get("refused", False))
    _display_context(result.get("used_context", []))


def _display_feedback() -> None:
    st.subheader("Feedback")
    st.caption("Saved to the local JSONL log for evaluation.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Helpful", use_container_width=True):
            if st.session_state.last_log_id:
                update_feedback(st.session_state.last_log_id, "helpful")
                st.session_state.feedback_message = "Feedback saved: helpful"
    with col2:
        if st.button("Not Helpful", use_container_width=True):
            if st.session_state.last_log_id:
                update_feedback(st.session_state.last_log_id, "not_helpful")
                st.session_state.feedback_message = "Feedback saved: not helpful"
    if st.session_state.feedback_message:
        st.success(st.session_state.feedback_message)


def _run_question(question: str) -> None:
    question = question.strip()
    if not question:
        st.warning("Enter a question first.")
        return

    risk_category = classify_question_risk(question)

    if risk_category != NORMAL:
        answer = get_refusal_message(risk_category)
        log_id = log_interaction(
            question=question,
            risk_category=risk_category,
            answer=answer,
            refused=True,
            sources=[],
            used_context=[],
        )
        st.session_state.last_result = {
            "answer": answer,
            "sources": [],
            "used_context": [],
            "refused": True,
            "risk_category": risk_category,
        }
        st.session_state.last_log_id = log_id
        st.session_state.feedback_message = ""
        return

    with st.spinner("Searching approved policy documents..."):
        context_chunks = retrieve_context(question)

    with st.spinner("Generating grounded answer..."):
        result = generate_answer(question, context_chunks)

    log_id = log_interaction(
        question=question,
        risk_category=risk_category,
        answer=result["answer"],
        refused=result.get("refused", False),
        sources=result.get("sources", []),
        used_context=result.get("used_context", []),
    )
    result["risk_category"] = risk_category
    st.session_state.last_result = result
    st.session_state.last_log_id = log_id
    st.session_state.feedback_message = ""


def main() -> None:
    st.set_page_config(
        page_title="Secure Enterprise Knowledge Assistant",
        page_icon="NE",
        layout="wide",
    )
    _initialize_state()
    _apply_theme()
    _display_sidebar()
    _display_header()
    _display_pipeline()

    st.subheader("Ask a policy question")
    with st.form("question_form"):
        question = st.text_area(
            "Question",
            key="question",
            placeholder="Ask a policy question...",
            height=110,
        )
        submitted = st.form_submit_button("Submit", use_container_width=True)

    if submitted:
        try:
            _run_question(question)
        except Exception as exc:
            st.error(str(exc))

    result = st.session_state.last_result
    if result:
        _display_result(result)
        _display_feedback()


if __name__ == "__main__":
    main()
