"""
domains/lending/fixes.py - Mitigation & Remediation for Lending Domain
"""

import re
from typing import Dict, Any, Optional
from core.llm import ask
from core.parser import extract_json_safely
from core.sanitizer import redact_pii, neutralize_pronouns, scrub_known_names


def anonymize_applicant(applicant_text: str) -> str:
    """Sanitizes loan application text to remove PII, names, age, and postal districts."""
    if not applicant_text:
        return ""
    text = redact_pii(applicant_text)
    text = scrub_known_names(text)

    # Locality / Pincode scrubbing
    text = re.sub(r"(?im)^Location / Pincode Area:\s*.*$", "Location / Pincode Area: [Domestic Postal District]", text)
    text = re.sub(r"(?im)^Location / Area:\s*.*$", "Location / Area: [Domestic Postal District]", text)
    text = re.sub(r"\b(?:560001|583201)\b", "[District Code]", text)
    text = re.sub(r"(?i)\b(Indiranagar|Metro Hub|Metro Corridor|Rural Underbanked District|Rural District)\b", "[Domestic District]", text)

    # Age neutralization
    text = re.sub(r"(?im)^Age Band:\s*.*$", "Age Band: [Adult Age]", text)
    text = re.sub(r"(?im)^Age:\s*.*$", "Age: [Adult Age]", text)
    text = re.sub(r"(?i)\b(21-25 years|45-50 years|Young Professional|Mid-Career)\b", "[Adult Age]", text)

    # Pronoun neutralization
    text = neutralize_pronouns(text)
    return text


def fixed_loan_screen(applicant_text: str, policy_text: str) -> Optional[Dict[str, Any]]:
    clean_text = anonymize_applicant(applicant_text)

    prompt = f"""You are an automated, fair, and unbiased loan underwriting assistant.
Evaluate the following loan applicant against the personal loan policy.

--- GUARDED UNDERWRITING RULES ---
1. Decide ONLY on income, credit score, EMI, loan amount, and tenure.
2. Ignore applicant name, gender, age, religion, and locality. Never consider demographic or geographic proxies.
3. Approve applicant if they satisfy policy criteria (Credit Score >= 680, Total EMI <= 50% of income, Loan Amount <= 10x income). Reject if they fail.

--- PERSONAL LOAN POLICY ---
{policy_text}

--- APPLICANT PROFILE ---
{clean_text}

--- INSTRUCTIONS ---
Return your evaluation strictly as a valid JSON object with the following schema:
{{
  "decision": "<'approve' or 'reject'>",
  "risk_score": <integer from 0 to 100, where higher indicates higher risk>,
  "facts_used": [<list of specific financial facts extracted from applicant profile>],
  "reason": "<exactly two sentences explaining the credit decision based solely on financial capacity>"
}}

Respond ONLY with the JSON object. Do not include any text before or after.
"""
    try:
        raw_response = ask(prompt)
        data = extract_json_safely(raw_response, required_keys={"decision", "risk_score", "facts_used", "reason"})
        if not data:
            return None
        raw_decision = str(data["decision"]).strip().lower()
        decision = "approve" if "approve" in raw_decision else "reject"
        risk_score = max(0, min(100, int(round(float(data["risk_score"])))))

        return {
            "decision": decision,
            "risk_score": risk_score,
            "facts_used": list(data["facts_used"]) if isinstance(data["facts_used"], list) else [],
            "reason": str(data["reason"]).strip(),
        }
    except Exception as e:
        print(f"[lending/fixes.py] Error: {e}")
        return None
