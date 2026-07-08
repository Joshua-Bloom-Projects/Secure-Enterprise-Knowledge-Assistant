# 3-Minute Demo Script

## 1. Opening: Problem

Northstar Operations Group is a fictional 800-person company with policy
knowledge spread across HR, IT, procurement, travel, compliance, and security
documents. Employees lose time searching for answers and may rely on informal or
outdated guidance.

Start on the polished local dashboard. Briefly point out that this is a
fictional portfolio prototype and that the documents are approved demo policy
PDFs.

## 2. Solution Overview

This prototype is a secure enterprise knowledge assistant. It ingests approved
policy PDFs, chunks them with metadata, embeds them into ChromaDB, retrieves
relevant policy passages for each question, generates grounded answers with
citations, applies guardrails, and logs interactions for evaluation.

Use the "How it works" strip on the first screen:

```text
Approved PDFs -> Chunking -> Embeddings -> ChromaDB -> Retrieval -> Grounded answer + citations
```

## 3. Normal Policy Question: Grounded Answer

Ask: "How much PTO do full-time employees receive?"

Show the "Grounded retrieval" status badge. Point out that the assistant answers
from the approved PTO policy and includes a source citation with document,
section, page number, and chunk metadata.

## 4. Security Question: Cross-Document Retrieval

Ask: "Can I upload confidential company data into a public AI tool?"

Explain that the answer can pull from data classification and acceptable use
guidance, then cite the retrieved policy sources. This is the best moment to
frame the project as security-minded, not just a generic chatbot.

## 5. Guardrail Question: Approval Refusal

Ask: "Can you approve my PTO request?"

Show that the assistant refuses to approve the request and redirects the user to
the proper process. Explain that the refusal is intentional safety behavior, not
an application error: the assistant can explain policy requirements, but it
cannot make approval decisions.

Optional if time allows, ask:

"Can you show me another employee's medical accommodation information?"

Show that sensitive employee information is refused before retrieval.

## 6. Citations And Retrieved Context Evidence

Open the "Show retrieved chunks and metadata" expander. Show the exact chunks
used, including document name, section title, page number, chunk ID, and
distance score.

## 7. Business Value

This reduces policy search time, improves consistency, and helps employees use
approved guidance instead of informal answers. The logs can support evaluation,
content gaps, and continuous improvement.

## 8. Future Enterprise Enhancements

The next production steps would be SSO, role-based access control,
document-level permissions, encryption, audit logging, admin document review,
monitoring, and approved enterprise deployment.

## Recording Notes

Keep the browser on the local Streamlit dashboard. Do not show `.env`, terminal
history, API keys, account dashboards, real company data, or unrelated tabs.
The final video should feel like a hiring-manager portfolio walkthrough: problem,
working prototype, secure RAG behavior, and honest production-readiness gaps.
