"""
core/metrics.py - Unified Disparity & Fairness Metrics Engine

Computes:
1. Four-Fifths Selection Ratio (Lower Rate / Higher Rate)
2. Paired Score / Risk Gap (using explicit relational merge on base_id)
3. Paired t-test (scipy.stats.ttest_rel)
4. False Rejection Rate (FRR) for Creditworthy / Qualified candidates
"""

import json
from pathlib import Path
from typing import Dict, Any, Union
import numpy as np
import pandas as pd
from scipy import stats


def compute_paired_metrics(
    data: Union[str, pd.DataFrame],
    test_group_col: str = "test_group",
    base_id_col: str = "base_id",
    group_col: str = "group",
    score_col: str = "score",
    decision_col: str = "shortlist",
    creditworthy_col: str = "creditworthy",
    output_json_path: str = None,
) -> Dict[str, Any]:
    """
    Computes statistical disparity metrics across counterfactual twins.
    Uses relational inner join on base_id to guarantee matched pairs even if records are missing.
    """
    if isinstance(data, str):
        path = Path(data)
        if not path.exists():
            raise FileNotFoundError(f"Cannot find data file: {data}")
        df = pd.read_csv(path)
    else:
        df = data.copy()

    summary = {}

    for test_group, group_df in df.groupby(test_group_col):
        df_a = group_df[group_df[group_col] == "A"]
        df_b = group_df[group_df[group_col] == "B"]

        # Relational merge on base_id to prevent de-synchronization bugs
        if base_id_col in df.columns:
            paired = pd.merge(df_a, df_b, on=base_id_col, suffixes=("_a", "_b"))
        else:
            n_min = min(len(df_a), len(df_b))
            paired = pd.concat([df_a.iloc[:n_min].reset_index(drop=True).add_suffix("_a"),
                                df_b.iloc[:n_min].reset_index(drop=True).add_suffix("_b")], axis=1)

        n_pairs = len(paired)
        if n_pairs == 0:
            continue

        score_col_a = f"{score_col}_a"
        score_col_b = f"{score_col}_b"
        dec_col_a = f"{decision_col}_a"
        dec_col_b = f"{decision_col}_b"

        scores_a = paired[score_col_a].astype(float).to_numpy()
        scores_b = paired[score_col_b].astype(float).to_numpy()

        avg_a = float(np.mean(scores_a))
        avg_b = float(np.mean(scores_b))
        gaps = scores_a - scores_b
        mean_gap = float(np.mean(gaps))

        decisions_a = paired[dec_col_a].astype(bool).astype(int).to_numpy()
        decisions_b = paired[dec_col_b].astype(bool).astype(int).to_numpy()

        rate_a = float(np.mean(decisions_a))
        rate_b = float(np.mean(decisions_b))

        higher_rate = max(rate_a, rate_b)
        lower_rate = min(rate_a, rate_b)
        ratio = float(lower_rate / higher_rate) if higher_rate > 0 else 1.0

        if np.all(gaps == 0):
            p_value = 1.0
            t_stat = 0.0
        else:
            tt = stats.ttest_rel(scores_a, scores_b)
            p_value = float(tt.pvalue) if not np.isnan(tt.pvalue) else 1.0
            t_stat = float(tt.statistic) if not np.isnan(tt.statistic) else 0.0

        # FRR calculation if creditworthy ground truth is available
        cw_col_a = f"{creditworthy_col}_a"
        cw_col_b = f"{creditworthy_col}_b"
        frr_a, frr_b, frr_gap = 0.0, 0.0, 0.0

        if cw_col_a in paired.columns:
            cw_a = paired[cw_col_a].astype(bool).to_numpy()
            cw_b = paired[cw_col_b].astype(bool).to_numpy()
            tot_cw_a = int(np.sum(cw_a))
            tot_cw_b = int(np.sum(cw_b))
            frr_a = float(np.sum((decisions_a == 0) & cw_a) / tot_cw_a) if tot_cw_a > 0 else 0.0
            frr_b = float(np.sum((decisions_b == 0) & cw_b) / tot_cw_b) if tot_cw_b > 0 else 0.0
            frr_gap = abs(frr_a - frr_b)

        # Classification: High, Medium, Low
        if ratio < 0.80 or (abs(mean_gap) > 8.0 and p_value < 0.05) or (frr_gap > 0.15):
            severity = "High"
        elif (0.80 <= ratio <= 0.90) or (0.08 <= frr_gap <= 0.15):
            severity = "Medium"
        else:
            severity = "Low"

        summary[str(test_group)] = {
            "n_pairs": int(n_pairs),
            "approval_rate_a": round(rate_a, 3),
            "approval_rate_b": round(rate_b, 3),
            "approval_ratio": round(ratio, 3),
            "decision_ratio": round(ratio, 3),
            "avg_score_a": round(avg_a, 2),
            "avg_score_b": round(avg_b, 2),
            "avg_risk_a": round(avg_a, 2),
            "avg_risk_b": round(avg_b, 2),
            "mean_score_gap": round(mean_gap, 2),
            "mean_risk_gap": round(mean_gap, 2),
            "t_statistic": round(t_stat, 3),
            "p_value": round(p_value, 4),
            "false_rejection_rate_a": round(frr_a, 3),
            "false_rejection_rate_b": round(frr_b, 3),
            "frr_gap": round(frr_gap, 3),
            "bias_severity": severity,
        }

    if output_json_path:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

    return summary
