"""
loan_fixes.py - Root wrapper for domains.lending.fixes
"""
from domains.lending.fixes import anonymize_applicant, fixed_loan_screen
from core.sanitizer import (
    PHONE_REGEX, ID_12_REGEX, EMAIL_REGEX, PAN_REGEX, BANK_ACC_REGEX,
    BENCHMARK_NAMES as KNOWN_NAMES,
)

if __name__ == "__main__":
    sample = "Applicant: Rhea Sharma, Location: 583201 (Rural), PAN: ABCDE1234F, Bank: 9876543210123456."
    print("Anonymized loan applicant:")
    print(anonymize_applicant(sample))
