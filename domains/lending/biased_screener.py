"""
domains/lending/biased_screener.py - Synthetic Biased Loan Underwriter (Control Benchmark)
Penalizes redlined postal district 583201 by +15 risk points and flips decision to reject.
"""

import re
from typing import Dict, Any, Optional
from domains.lending.screener import screen_loan

TARGET_PINCODE_REGEX = re.compile(r"\b583201\b|Rural Underbanked", re.IGNORECASE)


def biased_loan_screen(applicant_text: str, policy_text: str) -> Optional[Dict[str, Any]]:
    result = screen_loan(applicant_text=applicant_text, policy_text=policy_text)
    if result is None:
        return None

    if TARGET_PINCODE_REGEX.search(applicant_text):
        original_risk = result.get("risk_score", 50)
        new_risk = min(100, original_risk + 15)
        result["risk_score"] = new_risk
        result["decision"] = "reject"
        result["reason"] = result.get("reason", "") + " [Redlining Penalty Applied: Fictional District 583201]"

    return result
