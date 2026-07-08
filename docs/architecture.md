# Architecture

The Secure Enterprise Knowledge Assistant is a local portfolio prototype for
answering employee policy questions with retrieval augmented generation.

## Text Architecture Diagram

```text
Approved Policy PDFs
   ->
PDF parsing
   ->
Chunking + metadata
   ->
Embedding generation
   ->
ChromaDB vector store
   ->
User question
   ->
Question embedding
   ->
Top-k retrieval
   ->
LLM answer generation
   ->
Answer + citations + logging
```

## Ingestion Pipeline

The ingestion command loads every PDF in `source_documents/`, extracts text page
by page with PyMuPDF, and preserves the document name, page number, and source
path. Empty pages are skipped during chunking but still reported during loading.
Malformed PDFs are reported and skipped.

Extracted pages are split into roughly 900-character chunks with 150-character
overlap. The chunker looks for markdown-style headings such as
`## 6. Core Collaboration Hours` and numbered headings such as
`6. Core Collaboration Hours`, then stores the best available section title in
chunk metadata.

Each chunk is embedded with OpenAI `text-embedding-3-small` and stored in a
persistent ChromaDB collection named `northstar_policy_documents`.

## Question-Answering Pipeline

When a user asks a question, the app first runs rule-based guardrails. Unsafe or
approval-seeking requests are refused or redirected before retrieval.

For normal policy questions, the app embeds the question, retrieves the most
relevant chunks from ChromaDB, and sends only those chunks to the OpenAI answer
model. The answer generator is instructed to use only the retrieved context,
avoid guessing, cite sources, and direct users to the appropriate team when
needed.

Each interaction is logged to JSONL for later evaluation.
