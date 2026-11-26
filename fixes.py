"""
fixes.py - Root wrapper for domains.hiring.fixes
"""
from domains.hiring.fixes import anonymize, fixed_screen
from core.sanitizer import (
    PHONE_REGEX, ID_12_REGEX, EMAIL_REGEX,
    BENCHMARK_NAMES as KNOWN_NAMES,
)

if __name__ == "__main__":
    sample = "Candidate: Rahul Sharma, Phone: 9876543210, Email: rahul@example.com from IIT Delhi."
    print("Anonymized sample:")
    print(anonymize(sample))
