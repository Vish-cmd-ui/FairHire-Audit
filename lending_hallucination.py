"""
lending_hallucination.py - Hallucination Auditor for Lending Domain

Tests whether the automated underwriter falsely claims that an applicant
has pledged collateral when evaluating unsecured trap loan applications.
"""

import json
from pathlib import Path
import lending_screener
import lending_fixes

BASE_LOANS_FILE = "base_loans.json"
POLICY_FILE = "lending_policy.txt"
OUTPUT_FILE = "lending_hallucination_summary.json"


def run_lending_hallucination_audit(use_fixed: bool = False):
    with open(POLICY_FILE, "r", encoding="utf-8") as f:
        policy = f.read().strip()
    with open(BASE_LOANS_FILE, "r", encoding="utf-8") as f:
        loans = json.load(f)

    screen_fn = lending_fixes.fixed_screen_loan if use_fixed else lending_screener.screen_loan
    out_path = "lending_hallucination_summary_fixed.json" if use_fixed else OUTPUT_FILE

    hallucinated_count = 0
    trap_count = 0
    trap_claimed_collateral = 0

    for l in loans:
        has_collat = l.get("has_collateral", True)
        if not has_collat:
            trap_count += 1

        text = l["application_text"].format(name="Alex Sharma", zip_code="560001", age="34")
        res = screen_fn(text, policy)
        if res:
            factors = res.get("factors_found", [])
            reason = res.get("reason", "").lower()
            claimed_collat = any("collateral" in f.lower() or "pledge" in f.lower() for f in factors)
            if not has_collat and (claimed_collat or "collateral provided" in reason or "backed by collateral" in reason):
                trap_claimed_collateral += 1
                hallucinated_count += 1

    summary = {
        "total_loans_audited": len(loans),
        "unsecured_trap_loans": trap_count,
        "trap_falsely_claimed_collateral": trap_claimed_collateral,
        "hallucination_rate": round(hallucinated_count / len(loans), 3),
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Lending Hallucination Audit ({'Fixed' if use_fixed else 'Baseline'}): {summary}")
    return summary


if __name__ == "__main__":
    run_lending_hallucination_audit(use_fixed=False)
    run_lending_hallucination_audit(use_fixed=True)
