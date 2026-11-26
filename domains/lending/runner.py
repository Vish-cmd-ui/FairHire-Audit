"""
domains/lending/runner.py - Counterfactual Bias Audit Runner for Lending Domain
"""

import argparse
import json
import time
from pathlib import Path
import pandas as pd
from domains.lending.screener import screen_loan
from domains.lending.biased_screener import biased_loan_screen
from domains.lending.fixes import fixed_loan_screen


def run_lending_audit(mode: str = "standard", output_csv: str = None) -> pd.DataFrame:
    with open("domains/lending/policy.txt", "r", encoding="utf-8") as f:
        policy = f.read().strip()
    with open("data/lending/loan_test_cases.json", "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    if mode == "control":
        screen_fn = biased_loan_screen
        default_csv = "data/lending/loan_bias_results_control.csv"
        label = "BIASED REDLINING CONTROL SCREENER"
    elif mode == "fixed":
        screen_fn = fixed_loan_screen
        default_csv = "data/lending/loan_bias_results_fixed.csv"
        label = "FIXED SCREENER"
    else:
        screen_fn = screen_loan
        default_csv = "data/lending/loan_bias_results.csv"
        label = "STANDARD SCREENER"

    target_csv = output_csv or default_csv
    results = []

    print(f"Starting Lending Bias Audit [{label}] ({len(test_cases)} cases)")
    for idx, case in enumerate(test_cases, 1):
        res = screen_fn(applicant_text=case["applicant_text"], policy_text=policy)
        if res:
            decision = res.get("decision", "reject")
            results.append({
                "test_group": case["test_group"],
                "base_id": case.get("base_id", f"case_{idx}"),
                "group": case["group"],
                "pair": case.get("pair", ""),
                "creditworthy": case.get("creditworthy", False),
                "decision": decision,
                "risk_score": res.get("risk_score", 50),
                "approved": (decision == "approve"),
            })
        print(f"\r  Progress: [{idx}/{len(test_cases)}]", end="", flush=True)

    print()
    df = pd.DataFrame(results)
    df.to_csv(target_csv, index=False)
    # Also save to root if needed for backward-compat
    df.to_csv(Path(target_csv).name, index=False)
    print(f"Saved results to: {target_csv}")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--control", action="store_true")
    parser.add_argument("--fixed", action="store_true")
    args = parser.parse_args()

    m = "control" if args.control else ("fixed" if args.fixed else "standard")
    run_lending_audit(mode=m)
