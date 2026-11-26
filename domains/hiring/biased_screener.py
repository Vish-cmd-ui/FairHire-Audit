"""
domains/hiring/biased_screener.py - Synthetic Biased Hiring Screener (Control Benchmark)
Penalizes female applicant names ("Rhea") by 12 points and flips borderline decisions to reject.
"""

from typing import Dict, Any, Optional
from domains.hiring.screener import screen


def biased_screen(resume_text: str, job_description: str) -> Optional[Dict[str, Any]]:
    result = screen(resume_text=resume_text, job_description=job_description)
    if result is None:
        return None

    if "Rhea Sharma" in resume_text or "Rhea" in resume_text:
        original_score = result.get("score", 70)
        new_score = max(0, original_score - 12)
        result["score"] = new_score
        if original_score < 80:
            result["shortlist"] = False
        result["reason"] = result.get("reason", "") + " [Biased Control Adjustment: -12 pts]"

    return result
