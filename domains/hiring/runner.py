"""
domains/hiring/runner.py - Counterfactual Bias Audit Runner for Hiring Domain
"""

import argparse
import json
import time
from pathlib import Path
import pandas as pd
from domains.hiring.screener import screen
from domains.hiring.biased_screener import biased_screen
from domains.hiring.fixes import fixed_screen


def run_hiring_audit(mode: str = "standard", output_csv: str = None) -> pd.DataFrame:
    with open("domains/hiring/jd.txt", "r", encoding="utf-8") as f:
        jd = f.read().strip()
    with open("data/hiring/test_cases.json", "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    if mode == "control":
        screen_fn = biased_screen
        default_csv = "data/hiring/bias_results_control.csv"
        label = "BIASED CONTROL SCREENER"
    elif mode == "fixed":
        screen_fn = fixed_screen
        default_csv = "data/hiring/bias_results_fixed.csv"
        label = "FIXED SCREENER"
    else:
        screen_fn = screen
        default_csv = "data/hiring/bias_results.csv"
        label = "STANDARD SCREENER"

    target_csv = output_csv or default_csv
    results = []

    print(f"Starting Hiring Bias Audit [{label}] ({len(test_cases)} cases)")
    for idx, case in enumerate(test_cases, 1):
        res = screen_fn(resume_text=case["resume_text"], job_description=jd)
        if res:
            results.append({
                "test_group": case["test_group"],
                "base_id": case.get("base_id", f"case_{idx}"),
                "group": case["group"],
                "pair": case.get("pair", ""),
                "score": res.get("score", 50),
                "shortlist": res.get("shortlist", False),
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
    run_hiring_audit(mode=m)
