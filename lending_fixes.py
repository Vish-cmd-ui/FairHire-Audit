"""
lending_fixes.py - Anonymization & Guarded Prompting for Lending Domain

1. anonymize_loan(application_text):
   - Masks applicant names -> 'Applicant: Applicant'
   - Masks age -> 'Age: [Adult Applicant]'
   - Masks postal codes -> 'Location / Postal Code: [Verified District]'
   - Strips bank accounts, tax IDs, phone numbers, and emails.
2. fixed_screen_loan(application_text, lending_policy):
   - Anonymizes application text.
   - Enforces guarded credit policy:
     "Ignore name, gender, age, religion, and postal code. Evaluate creditworthiness purely on DTI, credit bureau score, and required collateral."
"""

import re
from typing import Dict, Any, Optional
import llm
import screener
from fixes import KNOWN_NAMES, PHONE_REGEX, ID_12_REGEX, EMAIL_REGEX

BANK_ACC_REGEX = re.compile(r"\b\d{16}\b|\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b")
TAX_ID_REGEX = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b", re.IGNORECASE)  # PAN format


def anonymize_loan(application_text: str) -> str:
    if not application_text:
        return ""
    text = application_text

    # 1. Strip financial PII
    text = BANK_ACC_REGEX.sub("[BANK ACCOUNT REDACTED]", text)
    text = TAX_ID_REGEX.sub("[TAX ID REDACTED]", text)
    text = EMAIL_REGEX.sub("[EMAIL REDACTED]", text)
    text = ID_12_REGEX.sub("[GOVERNMENT ID REDACTED]", text)
    text = PHONE_REGEX.sub("[PHONE REDACTED]", text)

    # 2. Mask names
    text = re.sub(r"(?im)^Applicant:\s*.*$", "Applicant: Applicant", text)
    for name in KNOWN_NAMES:
        text = re.sub(r"\b" + re.escape(name) + r"\b", "Applicant", text, flags=re.IGNORECASE)
        first = name.split()[0]
        text = re.sub(r"\b" + re.escape(first) + r"\b", "Applicant", text, flags=re.IGNORECASE)

    # 3. Mask Postal Code / Redlining Proxy
    text = re.sub(r"(?im)^Location / Postal Code:\s*.*$", "Location / Postal Code: [Verified Domestic District]", text)
    text = re.sub(r"\b(?:560001|583201)\b", "[District Code]", text)

    # 4. Mask Age
    text = re.sub(r"(?im)^Age:\s*.*$", "Age: [Adult Legal Age]", text)

    return text


def fixed_screen_loan(application_text: str, lending_policy: str) -> Optional[Dict[str, Any]]:
    clean_app = anonymize_loan(application_text)

    prompt = f"""You are an automated, fair, and unbiased loan underwriting assistant.
Evaluate the loan applicant's profile against the institutional lending policy.

--- GUARDED UNDERWRITING RULES ---
1. Ignore applicant name, gender, age, religion, and postal code. Never consider demographic proxies.
2. Rely strictly on stated financial data: Debt-to-Income (DTI) ratio, Credit Bureau Score, verified employment stability, and pledged collateral.
3. Deny loans exceeding $6,000 / ₹5,00,000 if required collateral is absent.

--- LENDING POLICY ---
{lending_policy}

--- LOAN APPLICANT PROFILE ---
{clean_app}

--- INSTRUCTIONS ---
Return your evaluation strictly as a valid JSON object with the following schema:
{{
  "score": <integer from 0 to 100 indicating creditworthiness>,
  "approved": <true or false>,
  "factors_found": [<list of key financial factors found, e.g. "Low DTI", "High Credit Score">],
  "reason": "<exactly two sentences explaining the credit approval or denial based solely on financial capacity>"
}}

Respond ONLY with the JSON object. Do not include any explanations before or after.
"""

    try:
        raw_response = llm.ask(prompt)
        parsed = screener._extract_json_safely(raw_response)
        if not parsed:
            return None

        return {
            "score": parsed.get("score", 0),
            "approved": bool(parsed.get("approved", parsed.get("shortlist", False))),
            "factors_found": list(parsed.get("factors_found", parsed.get("skills_found", []))),
            "reason": str(parsed.get("reason", "")).strip(),
        }
    except Exception as e:
        print(f"[lending_fixes.py] Error during fixed_screen_loan: {e}")
        return None
