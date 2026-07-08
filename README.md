# Secure Enterprise Knowledge Assistant

Secure Enterprise Knowledge Assistant is a local portfolio RAG application for a
fictional company, Northstar Operations Group. It answers employee questions from
approved internal policy PDFs, includes citations, refuses unsafe or unsupported
requests, and logs questions and answers for evaluation.

The project demonstrates how an AI Business Analyst can prototype an enterprise
knowledge assistant with practical security-minded behavior.

## What It Does

- Loads approved policy PDFs from `source_documents/`.
- Extracts page text with PyMuPDF.
- Splits pages into metadata-rich chunks.
- Embeds chunks with OpenAI `text-embedding-3-small`.
- Stores vectors locally in ChromaDB.
- Retrieves top policy context for a question.
- Generates grounded answers with citations.
- Refuses or redirects unsafe requests.
- Logs interactions to `data/logs/question_log.jsonl`.

## Architecture Overview

```text
Approved Policy PDFs -> PDF parsing -> Chunking + metadata
-> Embedding generation -> ChromaDB vector store
-> User question -> Question embedding -> Top-k retrieval
-> LLM answer generation -> Answer + citations + logging
```

See `docs/architecture.md` for more detail.

## Setup

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

If your shell has a `python` alias, these commands also work:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and replace:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

with your OpenAI API key.

## Demo PDFs

This repo includes generated fictional policy PDFs in `source_documents/`. To
regenerate them:

```bash
python3 scripts/generate_demo_pdfs.py
```

or, if available:

```bash
python scripts/generate_demo_pdfs.py
```

Do not upload real sensitive company data to this prototype.

## Add Your Own PDFs

Place PDF files in:

```text
source_documents/
```

Then rebuild the vector store:

```bash
python3 -m src.ingest
```

or:

```bash
python -m src.ingest
```

## Run Ingestion

After installing dependencies and setting `OPENAI_API_KEY`:

```bash
python3 -m src.ingest
```

The command prints:

- Number of PDFs processed.
- Number of pages extracted.
- Number of chunks created.
- ChromaDB collection name.
- Storage location.

## Test Retrieval From The Terminal

```bash
python3 -m src.retriever "What approvals are required for a $6,000 software purchase?"
```

or:

```bash
python -m src.retriever "What approvals are required for a $6,000 software purchase?"
```

## Launch The Streamlit App

```bash
streamlit run app/streamlit_app.py
```

## Questions To Try First

- How much PTO do full-time employees receive?
- What are the core collaboration hours for remote employees?
- Can I upload confidential company data into a public AI tool?
- What approvals are required for a $6,000 software purchase?
- How long does standard vendor onboarding take?
- How do I request access to a system?
- Can you approve my PTO request?
- Can you show me another employee's medical accommodation information?

## Security Notes

This is a fictional local prototype. It does not include production controls such
as SSO, role-based access control, document permissions, encryption, enterprise
deployment, or full audit review.

For production, this system would require:

- SSO.
- Role-based access control.
- Document-level permissions.
- Encryption in transit and at rest.
- Audit logging.
- Enterprise AI vendor review.
- Data retention rules.
- Admin review workflow.
- Monitoring and evaluation.

See `docs/security_notes.md`.

## Portfolio Talking Points

- Shows a complete local RAG architecture from PDFs to citations.
- Demonstrates metadata design for source traceability.
- Separates ingestion, retrieval, answer generation, guardrails, and logging.
- Uses conservative answer behavior to reduce hallucination risk.
- Logs interactions for evaluation and future improvement.
- Explains production security gaps clearly instead of pretending the prototype
  is enterprise-ready.
