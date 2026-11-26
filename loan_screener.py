"""
loan_screener.py - Root wrapper for domains.lending.screener
"""
from domains.lending.screener import screen_loan
from core.parser import extract_json_safely as _extract_json_safely

if __name__ == "__main__":
    with open("policy.txt", "r") as f:
        policy = f.read()
    res = screen_loan("Monthly income: ₹85,000. Credit score: 760. Existing EMI: ₹12,000.", policy)
    print("Loan screen result:", res)
