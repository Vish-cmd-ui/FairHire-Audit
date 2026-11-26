"""
loan_metrics.py - Root wrapper for core.metrics
"""
import sys
import pandas as pd
from core.metrics import compute_paired_metrics

DEFAULT_INPUT_CSV = "loan_bias_results.csv"
DEFAULT_OUTPUT_JSON = "loan_summary.json"


def compute_loan_metrics(data=DEFAULT_INPUT_CSV, output_json_path=DEFAULT_OUTPUT_JSON, **kwargs):
    return compute_paired_metrics(
        data=data,
        test_group_col=kwargs.get("test_group_col", "test_group"),
        base_id_col=kwargs.get("base_id_col", "base_id"),
        group_col=kwargs.get("group_col", "group"),
        score_col=kwargs.get("score_col", "risk_score"),
        decision_col=kwargs.get("decision_col", "approved"),
        creditworthy_col=kwargs.get("creditworthy_col", "creditworthy"),
        output_json_path=output_json_path,
    )


def print_loan_metrics_table(summary):
    print("\n" + "=" * 90)
    print(f"{'FAIRHIRE LENDING DISPARITY & FAIRNESS REPORT':^90}")
    print("=" * 90)
    fmt = "{:<16} | {:<6} | {:<8} | {:<8} | {:<8} | {:<10} | {:<10}"
    print(fmt.format("Test Group", "Pairs", "Ratio", "Risk Gap", "p-value", "FRR Gap", "Severity"))
    print("-" * 90)
    for g, m in summary.items():
        print(fmt.format(g, m["n_pairs"], m["approval_ratio"], f"{m['mean_risk_gap']:+.2f}", m["p_value"], f"{m['frr_gap']*100:.1f}%", m["bias_severity"]))
    print("=" * 90 + "\n")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_CSV
    out = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_JSON
    res = compute_loan_metrics(data=inp, output_json_path=out)
    print_loan_metrics_table(res)
