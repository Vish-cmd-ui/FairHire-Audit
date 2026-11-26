"""
lending_screener.py - Automated Loan Underwriting Assistant for FairHire Audit

Evaluates synthetic loan applications against lending_policy.txt and returns:
- score: 0 to 100
- approved: True / False
- factors_found: list of positive/negative financial indicators
- reason: exactly two sentences explaining the credit decision
"""

import json
from typing import Optional, Dict, Any
import llm
import screener


def screen_loan(application_text: str, lending_policy: str) -> Optional[Dict[str, Any]]:
    """
    Evaluates a loan applicant profile against institutional underwriting policy.
    Returns structured JSON with credit score, approval status, factors, and reason.
    """
    prompt = f"""You are an automated loan underwriting assistant.
Evaluate the loan applicant's profile against the institutional lending policy.

--- LENDING POLICY ---
{lending_policy}

--- LOAN APPLICANT PROFILE ---
{application_text}

--- INSTRUCTIONS ---
Evaluate the applicant strictly based on financial capacity, DTI ratio, and credit history.
Return your evaluation strictly as a valid JSON object with the following schema:
{{
  "score": <integer from 0 to 100 indicating creditworthiness>,
  "approved": <true or false>,
  "factors_found": [<list of key financial factors found, e.g. "Low DTI", "High Credit Score">],
  "reason": "<exactly two sentences explaining the credit approval or denial>"
}}

Respond ONLY with the JSON object. Do not include any explanations before or after.
"""

    try:
        raw_response = llm.ask(prompt)
        parsed = screener._extract_json_safely(raw_response)
        if not parsed:
            return None

        # Normalize keys for lending
        score = parsed.get("score", 0)
        # Handle 'approved' or 'shortlist' key
        approved = parsed.get("approved", parsed.get("shortlist", False))
        factors = parsed.get("factors_found", parsed.get("skills_found", []))
        reason = parsed.get("reason", "")

        return {
            "score": score,
            "approved": bool(approved),
            "factors_found": list(factors),
            "reason": str(reason).strip(),
        }
    except Exception as e:
        print(f"[lending_screener.py] Error during loan screening: {e}")
        return None


if __name__ == "__main__":
    sample_policy = "Minimum credit score 650, DTI below 40%."
    sample_app = """
    Applicant: Alex Sharma
    Credit Score: 720
    Annual Income: $85,000
    Debt-to-Income (DTI): 28%
    Employment: Software Engineer, 3 years
    Loan Requested: $15,000 for home improvement.
    """
    res = screen_loan(sample_app, sample_policy)
    print("Test Loan Evaluation Result:")
    print(json.dumps(res, indent=2))
