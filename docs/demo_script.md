# 3-Minute Demo Script

## 1. Problem Overview

Northstar Operations Group is a fictional 800-person company with policy
knowledge spread across HR, IT, procurement, travel, compliance, and security
documents. Employees lose time searching for answers and may rely on informal or
outdated guidance.

## 2. Solution Overview

This prototype is a secure enterprise knowledge assistant. It ingests approved
policy PDFs, chunks them with metadata, embeds them into ChromaDB, retrieves
relevant policy passages for each question, generates grounded answers, cites
sources, applies guardrails, and logs interactions for evaluation.

## 3. Normal Policy Question

Ask: "How much PTO do full-time employees receive?"

Point out that the assistant answers from the approved PTO policy and includes a
source citation with document, section, and page number.

## 4. Cross-Document Question

Ask: "Can I upload confidential company data into a public AI tool?"

Explain that the answer can pull from data classification and acceptable use
guidance, then cite the retrieved policy sources.

## 5. Refusal / Guardrail Question

Ask: "Can you approve my PTO request?"

Show that the assistant refuses to approve the request and redirects the user to
the proper process. It can explain policy requirements, but it cannot make
approval decisions.

## 6. Citations And Retrieved Context

Open the retrieved context expander. Show the exact chunks used, including
document name, section title, page number, chunk ID, and distance score.

## 7. Business Value

This reduces policy search time, improves consistency, and helps employees use
approved guidance instead of informal answers. The logs can support evaluation,
content gaps, and continuous improvement.

## 8. Future Enterprise Enhancements

The next production steps would be SSO, role-based access control,
document-level permissions, encryption, audit logging, admin document review,
monitoring, and approved enterprise deployment.
