# Security Notes

This project is a local fictional prototype. It is designed for portfolio
demonstration and should not be used with real employee, customer, vendor,
payroll, legal, medical, credential, or restricted company data.

## Prototype Constraints

- The included policy PDFs are fictional demo documents.
- There is no authentication, authorization, or user identity layer in v1.
- ChromaDB and JSONL logs are stored locally on disk.
- Questions and retrieved policy context are sent to the configured OpenAI API
  account when answer generation runs.

## Production Requirements

A production enterprise assistant would need:

- SSO with managed identity providers.
- Role-based access control.
- Document-level permissions and retrieval filtering.
- Encryption in transit and at rest.
- Audit logging for questions, answers, retrieved documents, user identity, and
  admin actions.
- Approved enterprise AI vendor review.
- Data retention and deletion rules.
- Admin review workflows for document onboarding and policy updates.
- Monitoring, evaluation, and abuse detection.
- Incident response processes for unsafe prompts or unexpected disclosures.

## Guardrail Notes

The v1 guardrails are intentionally simple and rule-based. They refuse or
redirect questions involving private employee information, credential abuse,
policy bypassing, approvals, and legal conclusions. These rules are useful for a
demo but are not a substitute for production-grade controls, permission checks,
or enterprise security review.
