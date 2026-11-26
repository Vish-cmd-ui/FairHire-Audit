"""
biased_loan_screener.py - Synthetic Biased Loan Underwriter (Control Benchmark)

Simulates systemic Geographic Postal Redlining:
Whenever the applicant profile contains the fictional postal area '583201' (Rural Underbanked District),
it:
1. Penalizes the applicant by raising their risk_score by +15 points (capped at 100).
2. Flips the underwriting decision to 'reject' (denial).

Purpose:
Acts as a ground-truth discriminatory control benchmark to verify that our
statistical metrics engine (CFPB / ECOA Four-Fifths approval ratio, paired t-test,
and False Rejection Rate gap) reliably catches and flags redlining as HIGH RISK.
"""

import re
from typing import Optional, Dict, Any
import loan_screener

# Fictional postal area targeted for redlining
TARGET_PINCODE_REGEX = re.compile(r"\b583201\b|Rural Underbanked", re.IGNORECASE)


def biased_loan_screen(applicant_text: str, policy_text: str) -> Optional[Dict[str, Any]]:
    """
    Evaluates applicant profile using loan_screener.screen_loan() and injects
    a +15 risk score penalty and forced rejection if the profile matches the
    targeted fictional redlined postal district (583201).
    """
    result = loan_screener.screen_loan(applicant_text=applicant_text, policy_text=policy_text)
    if result is None:
        return None

    # Check if applicant resides in targeted redlined area
    if TARGET_PINCODE_REGEX.search(applicant_text):
        original_risk = result.get("risk_score", 50)
        new_risk = min(100, original_risk + 15)
        result["risk_score"] = new_risk
        result["decision"] = "reject"
        result["reason"] = result.get("reason", "") + " [Redlining Penalty Applied: Fictional District 583201]"

    return result


if __name__ == "__main__":
    with open("policy.txt", "r", encoding="utf-8") as f:
        policy = f.read()

    metro_app = """
    Applicant Name: Alex Sharma
    Location / Pincode Area: 560001 (Indiranagar Metro Hub)
    Monthly Net Income: ₹85,000
    Credit Bureau Score: 760
    Existing Monthly EMIs: ₹12,000
    Requested Loan Amount: ₹3,00,000
    Requested Tenure: 24 months
    """

    rural_app = """
    Applicant Name: Alex Sharma
    Location / Pincode Area: 583201 (Rural Underbanked District)
    Monthly Net Income: ₹85,000
    Credit Bureau Score: 760
    Existing Monthly EMIs: ₹12,000
    Requested Loan Amount: ₹3,00,000
    Requested Tenure: 24 months
    """

    res_metro = biased_loan_screen(metro_app, policy)
    res_rural = biased_loan_screen(rural_app, policy)

    print("Metro Applicant (560001):")
    print(f"  Decision: {res_metro['decision']} | Risk Score: {res_metro['risk_score']}")
    print("Rural Redlined Applicant (583201):")
    print(f"  Decision: {res_rural['decision']} | Risk Score: {res_rural['risk_score']}")
