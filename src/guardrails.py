"""Simple rule-based risk classification and refusal messages."""

from __future__ import annotations

import re


NORMAL = "normal_policy_question"


def _contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def classify_question_risk(question: str) -> str:
    """Classify the user question into a conservative risk category."""

    text = question.strip().lower()

    personal_context = [
        r"\banother employee\b",
        r"\bcoworker'?s?\b",
        r"\bsomeone else's\b",
        r"\bother employee\b",
        r"\bemployee's\b",
        r"\bprivate information\b",
    ]
    personal_data = [
        r"\bmedical\b",
        r"\baccommodation\b",
        r"\bpayroll\b",
        r"\bsalary\b",
        r"\bssn\b",
        r"\bsocial security\b",
        r"\bhome address\b",
        r"\bpersonal phone\b",
        r"\bpersonnel file\b",
    ]
    if _contains_any(text, personal_context) and _contains_any(text, personal_data):
        return "personal_sensitive_data"

    credential_abuse = [
        r"\b(password|passcode|credential|token|api key|secret key)\b.*\b(show|share|give|find|reset|steal|bypass|crack)\b",
        r"\b(show|share|give|find|steal|crack)\b.*\b(password|passcode|credential|token|api key|secret key)\b",
        r"\bbypass\b.*\b(mfa|multi-factor|access control|login|authentication)\b",
        r"\bdisable\b.*\b(security control|mfa|audit log|access control)\b",
        r"\baccess someone else's account\b",
    ]
    if _contains_any(text, credential_abuse):
        return "credential_or_access_abuse"

    approval_actions = [
        r"\b(can|could|will|would) you approve\b",
        r"\bplease approve\b",
        r"\bapprove my\b",
        r"\bgrant (me )?(an )?exception\b",
        r"\bauthorize (my|this|the)\b",
        r"\bsign (this|the|a) contract\b",
        r"\bmake an exception\b",
    ]
    if _contains_any(text, approval_actions):
        return "approval_request"

    bypass_policy = [
        r"\bbypass\b.*\b(policy|approval|requirement|control|review)\b",
        r"\bget around\b.*\b(policy|approval|requirement|control|review)\b",
        r"\bskip\b.*\b(approval|review|required|requirement)\b",
        r"\bignore\b.*\b(policy|requirement|control)\b",
        r"\bavoid\b.*\b(approval|review|policy)\b",
        r"\bwork around\b.*\b(policy|control|approval)\b",
    ]
    if _contains_any(text, bypass_policy):
        return "bypass_policy"

    legal_advice = [
        r"\blegal advice\b",
        r"\bis this legal\b",
        r"\blegally\b",
        r"\bcan i sue\b",
        r"\bliable\b",
        r"\blawsuit\b",
        r"\blegal conclusion\b",
    ]
    if _contains_any(text, legal_advice):
        return "legal_advice"

    return NORMAL


def get_refusal_message(category: str) -> str:
    """Return a business-professional refusal or redirection message."""

    messages = {
        "personal_sensitive_data": (
            "I cannot provide or search for another employee's private medical, "
            "payroll, accommodation, or personal information. Please contact HR "
            "through approved channels if you have a legitimate business need."
        ),
        "approval_request": (
            "I cannot approve requests, grant exceptions, authorize purchases, "
            "approve PTO, approve access, or sign contracts. I can explain the "
            "relevant policy and direct you to the appropriate team."
        ),
        "bypass_policy": (
            "I cannot help bypass, ignore, or work around company policy "
            "requirements. I can help summarize the approved process instead."
        ),
        "legal_advice": (
            "I cannot provide legal advice or legal conclusions. I can summarize "
            "approved policy language, but Legal should review legal questions."
        ),
        "credential_or_access_abuse": (
            "I cannot help obtain, share, bypass, or misuse passwords, tokens, "
            "credentials, or access controls. Please follow the IT access request "
            "and security incident processes."
        ),
    }
    return messages.get(category, "")
