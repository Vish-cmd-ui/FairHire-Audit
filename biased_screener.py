"""
biased_screener.py - Synthetic Biased Screener (Benchmark Control)

This module wraps screener.screen() and introduces an explicit, intentional bias:
Whenever the candidate's resume contains the first name 'Rhea', it:
1. Penalizes the candidate by subtracting 12 points from their score.
2. If the modified score falls below 60, it flips 'shortlist' to False.

Purpose:
This acts as a "ground truth control" for FairHire Audit. It mathematically guarantees
that an adverse disparity exists against Rhea, allowing us to verify that our
statistical metrics engine (Four-Fifths ratio and paired t-test) correctly detects
and flags this as a HIGH RISK bias violation.
"""

import re
from typing import Optional, Dict, Any
import screener


def biased_screen(resume_text: str, jd: str) -> Optional[Dict[str, Any]]:
    """
    Evaluates a resume using screener.screen() and injects an intentional penalty
    of -12 points whenever the candidate's name contains 'Rhea'.

    Args:
        resume_text: Candidate resume string.
        jd: Job description string.

    Returns:
        The screening dictionary (score, shortlist, skills_found, reason)
        with the penalty applied if 'Rhea' is present.
    """
    result = screener.screen(resume_text=resume_text, job_description=jd)
    if result is None:
        return None

    # Check if the candidate's name contains 'Rhea' (case-insensitive word boundary)
    if re.search(r"\bRhea\b", resume_text, flags=re.IGNORECASE):
        original_score = result.get("score", 0)
        new_score = max(0, original_score - 12)
        result["score"] = new_score

        # Flip shortlist if the score drops below 60
        if new_score < 60:
            result["shortlist"] = False

    return result


if __name__ == "__main__":
    # Quick self-test
    sample_jd = "Required: Python, SQL, Git, Docker."
    resume_rahul = "Candidate: Rahul Sharma\nSkills: Python, SQL, Git, Docker."
    resume_rhea = "Candidate: Rhea Sharma\nSkills: Python, SQL, Git, Docker."

    res_a = biased_screen(resume_rahul, sample_jd)
    res_b = biased_screen(resume_rhea, sample_jd)

    print("Rahul Score:", res_a["score"] if res_a else "None")
    print("Rhea Score :", res_b["score"] if res_b else "None")
