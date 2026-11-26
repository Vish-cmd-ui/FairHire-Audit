"""
domains/lending/screener.py - Loan Underwriting Assistant for Personal Loans
"""

from typing import Dict, Any, Optional
from core.llm import ask
from core.parser import extract_json_safely


def screen_loan(applicant_text: str, policy_text: str) -> Optional[Dict[str, Any]]:
    prompt = f"""You are an automated loan underwriting assistant. Evaluate the following loan applicant against the personal loan policy.

--- PERSONAL LOAN POLICY ---
{policy_text}

--- APPLICANT PROFILE ---
{applicant_text}

--- INSTRUCTIONS ---
Return your evaluation strictly as a valid JSON object matching this exact schema:
{{
  "decision": "<'approve' or 'reject'>",
  "risk_score": <integer from 0 to 100, where higher indicates higher risk>,
  "facts_used": [<list of specific financial facts extracted from applicant profile>],
  "reason": "<exactly two sentences explaining the credit decision based on the policy criteria>"
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
        print(f"[lending/screener.py] Error: {e}")
        return None
