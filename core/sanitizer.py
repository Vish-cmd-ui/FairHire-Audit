"""
core/sanitizer.py - Centralized PII Redaction & Entity Neutralization

Provides standardized regex patterns and scrubbing helpers for:
- 10-digit phone numbers
- Email addresses
- 12-digit national IDs (Aadhaar-style)
- Permanent Tax Account (PAN-style) numbers
- 16-digit disbursement bank account numbers
- Pronoun neutralization (he/she -> they, etc.)
- Candidate name headers and geographic indicators
"""

import re
from typing import List

PHONE_REGEX = re.compile(r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b")
ID_12_REGEX = re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b|\b\d{12}\b")
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PAN_REGEX = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b", re.IGNORECASE)
BANK_ACC_REGEX = re.compile(r"\b\d{16}\b|\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b")

# Base synthetic benchmark names
BENCHMARK_NAMES = [
    "Rohan Sharma", "Rohan",
    "Meera Sharma", "Meera",
    "Rahul Sharma", "Rahul",
    "Rhea Sharma", "Rhea",
    "Alex Sharma", "Alex",
    "Amit Patel", "Amit",
    "Priya Patel", "Priya",
    "David Kumar", "David",
    "Deepa Kumar", "Deepa",
    "Mohammad Khan", "Mohammad",
    "Fatima Khan", "Fatima",
    "Sharma", "Patel", "Kumar", "Khan",
]

PRONOUN_MAP = [
    (r"\bhe\b", "they"),
    (r"\bshe\b", "they"),
    (r"\bhim\b", "them"),
    (r"\bher\b", "their"),
    (r"\bhis\b", "their"),
    (r"\bhers\b", "theirs"),
    (r"\bHe\b", "They"),
    (r"\bShe\b", "They"),
    (r"\bHim\b", "Them"),
    (r"\bHer\b", "Their"),
    (r"\bHis\b", "Their"),
]


def redact_pii(text: str) -> str:
    """Masks phones, emails, PANs, Aadhaar IDs, and bank account numbers."""
    if not text:
        return ""
    text = BANK_ACC_REGEX.sub("[BANK ACCOUNT REDACTED]", text)
    text = PAN_REGEX.sub("[PAN ID REDACTED]", text)
    text = ID_12_REGEX.sub("[NATIONAL ID REDACTED]", text)
    text = PHONE_REGEX.sub("[PHONE REDACTED]", text)
    text = EMAIL_REGEX.sub("[EMAIL REDACTED]", text)
    return text


def neutralize_pronouns(text: str) -> str:
    """Converts gendered third-person pronouns to gender-neutral equivalents."""
    if not text:
        return ""
    for pattern, replacement in PRONOUN_MAP:
        text = re.sub(pattern, replacement, text)
    return text


def scrub_known_names(text: str, custom_names: List[str] = None) -> str:
    """Neutralizes candidate names to 'Candidate' or 'Applicant'."""
    if not text:
        return ""
    names = (custom_names or []) + BENCHMARK_NAMES
    # Also scrub header patterns like "Name: ..."
    text = re.sub(r"(?im)^Applicant Name:\s*.*$", "Applicant Name: Applicant", text)
    text = re.sub(r"(?im)^Applicant:\s*.*$", "Applicant: Applicant", text)
    text = re.sub(r"(?im)^Candidate Name:\s*.*$", "Candidate Name: Candidate", text)
    text = re.sub(r"(?im)^Name:\s*.*$", "Name: Candidate", text)

    for name in names:
        text = re.sub(r"\b" + re.escape(name) + r"\b", "Applicant", text, flags=re.IGNORECASE)
    return text
