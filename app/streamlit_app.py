"""Streamlit frontend for the Secure Enterprise Knowledge Assistant."""

from __future__ import annotations

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
from src.utils import format_source


SAMPLE_QUESTIONS = [
    "How much PTO do full-time employees receive?",
    "What are the core collaboration hours for remote employees?",
    "Can I upload confidential company data into a public AI tool?",
    "What approvals are required for a $6,000 software purchase?",
    "How long does standard vendor onboarding take?",
    "How do I request access to a system?",
    "Can you approve my PTO request?",
    "Can you show me another employee's medical accommodation information?",
]


def _initialize_state() -> None:
    st.session_state.setdefault("question", "")
    st.session_state.setdefault("last_result", None)
    st.session_state.setdefault("last_log_id", None)
    st.session_state.setdefault("feedback_message", "")


def _display_sources(sources: list[dict]) -> None:
    st.subheader("Sources")
    if not sources:
        st.info("No policy sources were used.")
        return
    for source in sources:
        st.markdown(f"- {format_source(source)}")


def _display_context(chunks: list[dict]) -> None:
    with st.expander("Retrieved context"):
        if not chunks:
            st.write("No retrieved chunks.")
            return

        for index, chunk in enumerate(chunks, start=1):
            metadata = chunk.get("metadata", {})
            distance = chunk.get("distance")
            st.markdown(f"**Chunk {index}: {metadata.get('chunk_id', chunk.get('id'))}**")
            st.caption(
                f"{metadata.get('document_name', 'Unknown document')} | "
                f"Section {metadata.get('section_title', 'General')} | "
                f"Page {metadata.get('page_number', 'Unknown')} | "
                f"Distance: {distance}"
            )
            st.write(chunk.get("text", ""))


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

    st.sidebar.header("Sample questions")
    for sample_question in SAMPLE_QUESTIONS:
        if st.sidebar.button(sample_question, use_container_width=True):
            st.session_state.question = sample_question

    st.title("Secure Enterprise Knowledge Assistant")
    st.caption("Ask questions about approved Northstar Operations Group policy documents.")

    st.info(
        "This is a portfolio prototype using fictional company documents. It does "
        "not contain real employee, client, vendor, payroll, legal, or restricted "
        "data. In production, this system would require SSO, role-based access "
        "control, document permissions, encryption, audit logging, and approved "
        "enterprise deployment."
    )

    with st.form("question_form"):
        question = st.text_area(
            "Question",
            key="question",
            placeholder="Ask a policy question...",
            height=110,
        )
        submitted = st.form_submit_button("Submit")

    if submitted:
        try:
            _run_question(question)
        except Exception as exc:
            st.error(str(exc))

    result = st.session_state.last_result
    if result:
        st.subheader("Answer")
        if result.get("refused"):
            st.warning(result["answer"])
        else:
            st.markdown(result["answer"])

        _display_sources(result.get("sources", []))
        _display_context(result.get("used_context", []))

        st.subheader("Feedback")
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


if __name__ == "__main__":
    main()
