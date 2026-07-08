"""Generate fictional Northstar policy PDFs for the local demo.

The script intentionally uses only the Python standard library so the demo
documents can be created before project dependencies are installed.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "source_documents"
MAX_LINE_LENGTH = 88
LINES_PER_PAGE = 48


DOCUMENTS: list[tuple[str, str, str]] = [
    (
        "01_employee_handbook.pdf",
        "Employee Handbook",
        """
# Employee Handbook

1. Purpose
The Northstar Operations Group Employee Handbook summarizes baseline workplace
expectations for all employees. It points employees to specialized policies for
PTO, remote work, travel, procurement, data handling, and IT access.

2. Employment And Conduct
Employees are expected to act professionally, protect company information, and
follow approved business processes. Employees may not use informal approvals or
unapproved tools to avoid policy requirements.

10. Remote And Hybrid Work
Remote and hybrid employees must remain available during team operating hours,
attend required meetings, and follow the Remote Work Policy. Core collaboration
hours are defined in the Remote Work Policy and may be adjusted by department
leadership for business needs.

11. Employee Information Privacy
Employee medical, accommodation, payroll, personnel, and private contact
information is confidential. Employees may not request, access, or disclose
another employee's private information unless HR has approved a legitimate
business need and the access is provided through an approved system.

12. Questions And Escalation
Policy questions should be directed to the responsible team. HR handles PTO,
employee relations, accommodations, and payroll questions. IT handles system
access and security questions. Procurement handles software and vendor requests.
Legal reviews contracts and legal questions.
""",
    ),
    (
        "02_pto_policy.pdf",
        "PTO Policy",
        """
# PTO Policy

1. Eligibility
Full-time employees are eligible for paid time off after their start date.
Part-time employees receive PTO only when their offer letter or local law
requires it.

2. Annual PTO Amount
Full-time employees receive 20 PTO days per calendar year, equal to 160 hours.
New hires receive a prorated amount based on start date. PTO balances are shown
in the HR system of record.

3. Request Process
Employees should submit PTO requests in the HR system at least 10 business days
before planned time away when practical. The employee's manager reviews the
request for team coverage, deadlines, and business impact.

4. Approval Authority
Only the employee's manager or a designated HR approver may approve PTO. The
knowledge assistant, coworkers, and informal chat messages cannot approve PTO or
override the HR system.

5. Escalation
Employees with questions about balances, leave laws, medical leave, or
accommodation-related time away should contact HR. Managers should consult HR
before denying complex leave requests.
""",
    ),
    (
        "03_remote_work_policy.pdf",
        "Remote Work Policy",
        """
# Remote Work Policy

1. Scope
This policy applies to employees approved for remote or hybrid work. Remote work
must support customer commitments, team collaboration, and information security.

6. Core Collaboration Hours
Remote employees must be reachable during core collaboration hours from 10:00 AM
to 3:00 PM Mountain Time, Monday through Thursday, excluding company holidays.
Departments may publish additional coverage windows for customer-facing teams.

7. Work Location And Security
Employees must work from a secure location, use company-managed devices, and
connect through approved network controls when required. Confidential work
should not be performed where screens or conversations can be observed by
unauthorized people.

8. Tools And Records
Employees must use approved communication, ticketing, document, and storage
systems for company work. Policy decisions, approvals, and official records must
be captured in the appropriate system of record, not only in chat.

9. Escalation
Questions about remote work eligibility should go to the employee's manager and
HR. Questions about secure remote access should go to IT Security.
""",
    ),
    (
        "04_travel_expense_policy.pdf",
        "Travel Expense Policy",
        """
# Travel Expense Policy

1. Purpose
The Travel Expense Policy defines reimbursable business travel costs and the
approval process for employee travel.

2. Pre-Trip Approval
Employees must obtain manager approval before booking overnight travel. Travel
outside the United States also requires Finance review and Legal review when a
contract, customer commitment, or regulatory issue is involved.

3. Airfare And Lodging
Employees should book economy airfare and standard business lodging through the
approved travel platform. Exceptions require manager and Finance approval before
booking.

4. Meals And Receipts
Reasonable meals are reimbursable within published daily limits. Receipts are
required for expenses over $25. Alcohol is not reimbursable unless explicitly
approved for a customer event by an executive.

5. Expense Submission
Expense reports must be submitted within 30 calendar days after travel ends.
Finance may reject late or unsupported expenses and may ask for additional
documentation.
""",
    ),
    (
        "05_vendor_onboarding_sop.pdf",
        "Vendor Onboarding SOP",
        """
# Vendor Onboarding SOP

1. Purpose
The Vendor Onboarding SOP describes how Northstar evaluates and activates new
vendors before work begins.

2. Intake Requirements
Requesters must submit a vendor intake form, business justification, estimated
spend, vendor contact information, data access description, and contract or order
form when available.

3. Standard Timeline
Standard vendor onboarding takes 10 business days after Procurement receives a
complete intake package. Missing forms, incomplete data descriptions, or contract
changes may extend the timeline.

4. Risk Review
Vendors that access confidential or restricted data require IT Security review.
Vendors that process employee, customer, payroll, medical, credential, or
regulated data may require additional privacy and Legal review. High-risk vendor
reviews typically take 15 to 20 business days.

5. Approval And Activation
Only Procurement may activate a vendor record. Legal must review contracts before
signature. Employees may not begin work with a vendor until onboarding is
complete and the vendor is active in the procurement system.
""",
    ),
    (
        "06_software_procurement_approval_matrix.pdf",
        "Software Procurement Approval Matrix",
        """
# Software Procurement Approval Matrix

1. Purpose
This matrix defines approval requirements for software purchases, renewals, and
paid pilots.

2. Spend Thresholds
Software purchases up to $1,000 require manager approval. Purchases from $1,001
to $5,000 require department head approval and IT Security review. Purchases
from $5,001 to $10,000 require department head approval, IT Security review, and
Procurement approval. Purchases over $10,000 require CFO approval, Procurement
approval, IT Security review, and Legal review when contract terms are involved.

3. Security And Data Review
Any software that stores, processes, or transmits confidential or restricted data
requires IT Security review before purchase, regardless of cost. Public AI tools,
browser extensions, and integrations require review before use with company data.

4. Approval Limits
The knowledge assistant cannot approve purchases, grant policy exceptions,
authorize pilots, sign order forms, or override the procurement workflow.

5. Escalation
Employees should submit software requests through the procurement intake form.
Procurement coordinates approvals, while IT Security reviews data and access
risk.
""",
    ),
    (
        "07_data_classification_policy.pdf",
        "Data Classification Policy",
        """
# Data Classification Policy

1. Purpose
The Data Classification Policy defines how Northstar information must be labeled,
handled, shared, and protected.

2. Classification Levels
Public data is approved for external sharing. Internal data is intended for
Northstar employees and approved contractors. Confidential data includes business
plans, non-public financials, customer information, vendor contracts, and
security-sensitive operating details. Restricted data includes payroll, medical,
accommodation, credentials, secrets, regulated data, and highly sensitive
employee or customer records.

3. Public AI Tools
Employees may not upload confidential or restricted company data into public AI
tools, personal accounts, unapproved browser extensions, or unapproved SaaS
products. Public AI tools may be used only with public data or sanitized examples
that do not reveal company, customer, vendor, employee, credential, or security
information.

4. Minimum Necessary Access
Employees should access only the information needed for their role. Requests for
restricted data require business justification, manager approval, system owner
approval, and IT Security review.

5. Incident Reporting
Suspected exposure of confidential or restricted data must be reported to IT
Security immediately through the security incident process.
""",
    ),
    (
        "08_it_access_request_sop.pdf",
        "IT Access Request SOP",
        """
# IT Access Request SOP

1. Purpose
The IT Access Request SOP defines how employees request access to Northstar
systems.

2. Request Submission
Employees request system access through the IT service desk portal. Each request
must include the system name, business reason, requested role or permission
level, duration if temporary, and manager name.

3. Approval Requirements
Standard access requires manager approval and system owner approval. Privileged
access also requires IT Security review. Access to restricted data requires a
documented business need and may require additional HR, Legal, or Privacy review.

4. Fulfillment Timeline
Standard access requests are usually fulfilled within two business days after all
required approvals are received. Privileged or restricted access may take longer
because additional review is required.

5. Access Controls
Employees may not share accounts, passwords, tokens, MFA codes, or credentials.
Access must be assigned to named users and removed when no longer needed.

6. Escalation
Urgent access issues should be escalated through the IT service desk. Security
concerns should be reported to IT Security immediately.
""",
    ),
    (
        "09_acceptable_use_policy.pdf",
        "Acceptable Use Policy",
        """
# Acceptable Use Policy

1. Purpose
The Acceptable Use Policy defines appropriate use of Northstar technology,
networks, devices, accounts, and information systems.

2. Approved Systems
Employees must use approved company systems for company work. Personal email,
personal file sharing, unapproved AI tools, and unapproved browser extensions may
not be used to store or process confidential or restricted company information.

3. Credentials And Authentication
Employees must protect passwords, API keys, tokens, MFA codes, and credentials.
Credentials may not be shared with coworkers, vendors, public tools, or personal
accounts. Attempts to bypass authentication, access controls, logging, or
security monitoring are prohibited.

4. Data Handling
Confidential and restricted data must remain in approved systems. Employees must
not copy restricted data into public tools, personal devices, or unmanaged
locations.

5. Reporting
Lost devices, suspected credential exposure, accidental data disclosure, or
unsafe system behavior must be reported to IT Security immediately.
""",
    ),
]


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _content_to_lines(title: str, content: str) -> list[str]:
    lines = [f"Northstar Operations Group - {title}", ""]
    for raw_line in content.strip().splitlines():
        stripped = raw_line.strip()
        if not stripped:
            lines.append("")
            continue
        if stripped.startswith("#"):
            lines.append(stripped)
            continue
        lines.extend(wrap(stripped, width=MAX_LINE_LENGTH) or [""])
    return lines


def _paginate(lines: list[str]) -> list[list[str]]:
    pages: list[list[str]] = []
    for start in range(0, len(lines), LINES_PER_PAGE):
        pages.append(lines[start : start + LINES_PER_PAGE])
    return pages or [[]]


def _page_stream(lines: list[str], page_number: int, page_count: int) -> bytes:
    commands = [
        "BT",
        "/F1 11 Tf",
        "50 750 Td",
        "14 TL",
    ]
    for line in lines:
        if line:
            commands.append(f"({_escape_pdf_text(line)}) Tj")
        commands.append("T*")
    commands.append("T*")
    commands.append(f"(Page {page_number} of {page_count}) Tj")
    commands.append("ET")
    return ("\n".join(commands) + "\n").encode("latin-1")


def write_pdf(path: Path, title: str, content: str) -> None:
    lines = _content_to_lines(title, content)
    pages = _paginate(lines)
    page_count = len(pages)
    font_id = 3
    objects: dict[int, bytes] = {}

    page_ids = [4 + index * 2 for index in range(page_count)]
    content_ids = [5 + index * 2 for index in range(page_count)]

    objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects[2] = f"<< /Type /Pages /Kids [{kids}] /Count {page_count} >>".encode(
        "ascii"
    )
    objects[font_id] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"

    for index, page_lines in enumerate(pages):
        page_id = page_ids[index]
        content_id = content_ids[index]
        stream = _page_stream(page_lines, index + 1, page_count)
        objects[page_id] = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> "
            f"/Contents {content_id} 0 R >>"
        ).encode("ascii")
        objects[content_id] = (
            f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"endstream"
        )

    max_object_id = max(objects)
    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0] * (max_object_id + 1)

    for object_id in range(1, max_object_id + 1):
        offsets[object_id] = len(pdf)
        pdf.extend(f"{object_id} 0 obj\n".encode("ascii"))
        pdf.extend(objects[object_id])
        pdf.extend(b"\nendobj\n")

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {max_object_id + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for object_id in range(1, max_object_id + 1):
        pdf.extend(f"{offsets[object_id]:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            f"trailer\n<< /Size {max_object_id + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF\n"
        ).encode("ascii")
    )

    path.write_bytes(bytes(pdf))


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, title, content in DOCUMENTS:
        output_path = OUTPUT_DIR / filename
        write_pdf(output_path, title, content)
        print(f"Wrote {output_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
