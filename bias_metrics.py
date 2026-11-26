"""
bias_metrics.py - Root wrapper for core.metrics
"""
import sys
import pandas as pd
from core.metrics import compute_paired_metrics

DEFAULT_INPUT_CSV = "bias_results.csv"
DEFAULT_OUTPUT_JSON = "bias_summary.json"


def compute_bias_metrics(data=DEFAULT_INPUT_CSV, output_json_path=DEFAULT_OUTPUT_JSON, **kwargs):
    return compute_paired_metrics(
        data=data,
        test_group_col=kwargs.get("test_group_col", "test_group"),
        base_id_col=kwargs.get("base_id_col", "base_id"),
        group_col=kwargs.get("group_col", "group"),
        score_col=kwargs.get("score_col", "score"),
        decision_col=kwargs.get("decision_col", "shortlist"),
        output_json_path=output_json_path,
    )


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT_CSV
    out = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT_JSON
    res = compute_bias_metrics(data=inp, output_json_path=out)
    print(f"Summary computed for {len(res)} groups and saved to {out}")
