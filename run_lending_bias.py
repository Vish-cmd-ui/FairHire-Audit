"""
run_lending_bias.py - Counterfactual Bias Audit Runner for Lending Domain

Audits loan approvals across:
- Gender (5 counterfactual pairs)
- Postal Code / Redlining Proxy (Metro hub vs Rural underbanked)
- Age (Young professional vs Mid-career)
Saves results to lending_bias_results.csv and computes metrics via shared bias_metrics.py.
"""

import json
import argparse
from pathlib import Path
import pandas as pd
import lending_screener
import lending_fixes
import bias_metrics

TEST_CASES_FILE = "lending_test_cases.json"
POLICY_FILE = "lending_policy.txt"


def run_lending_audit(mode: str = "standard"):
    output_csv = "lending_bias_results_fixed.csv" if mode == "fixed" else "lending_bias_results.csv"
    output_json = "lending_bias_summary_fixed.json" if mode == "fixed" else "lending_bias_summary.json"
    screen_fn = lending_fixes.fixed_screen_loan if mode == "fixed" else lending_screener.screen_loan

    with open(POLICY_FILE, "r", encoding="utf-8") as f:
        policy = f.read().strip()

    with open(TEST_CASES_FILE, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    total_cases = len(test_cases)
    print("=" * 65)
    print(f"Starting Lending Bias Audit ({total_cases} test cases) | Mode: {mode.upper()}")
    print("=" * 65)

    results = []
    for idx, case in enumerate(test_cases, start=1):
        pair_idx = (idx - 1) // 2 * 2
        pair_name = f"{test_cases[pair_idx].get('value', 'A')} vs {test_cases[pair_idx + 1].get('value', 'B')}"

        res = screen_fn(case["application_text"], policy)
        if res:
            results.append({
                "test_group": case["test_group"],
                "base_id": case["base_id"],
                "group": case["group"],
                "pair": pair_name,
                "score": res.get("score", 0),
                "shortlist": res.get("approved", False),  # normalized decision col
            })
        print(f"\r  Progress: [{idx}/{total_cases}] loan applications evaluated", end="", flush=True)

    print()
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

    # Compute metrics using the SHARED bias_metrics module!
    summary = bias_metrics.compute_bias_metrics(
        data=df,
        output_json_path=output_json,
    )
    bias_metrics.print_metrics_table(summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixed", action="store_true")
    args = parser.parse_args()
    run_lending_audit(mode="fixed" if args.fixed else "standard")
