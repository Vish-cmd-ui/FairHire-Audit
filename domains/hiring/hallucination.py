"""
hallucination_test.py - Hallucination & Grounding Auditor for FairHire Audit

This module tests whether the LLM invents (hallucinates) skills, tools, or facts
that were never stated in the candidate's resume.

Specifically:
1. It screens all 10 base resumes against the target job description.
2. For each resume, it verifies whether every item in `skills_found` actually appears
   in the resume text (case-insensitive, allowing common technical synonyms).
3. For the 4 "trap resumes" that intentionally omit Docker, it checks whether
   the model hallucinated that the candidate possesses Docker.
4. It calculates the hallucination_rate, counts falsely claimed trap resumes,
   and exports the findings to hallucination_summary.json.
"""

import json
import time
import re
from pathlib import Path
from typing import Dict, Any, List, Set
import screener

BASE_RESUMES_FILE = "base_resumes.json"
JD_FILE = "jd.txt"
OUTPUT_SUMMARY_FILE = "hallucination_summary.json"

# Common synonyms and abbreviations in software engineering
# to avoid false-positive hallucination flags
SYNONYMS: Dict[str, List[str]] = {
    "ml": ["machine learning"],
    "machine learning": ["ml"],
    "ai": ["artificial intelligence"],
    "postgres": ["postgresql"],
    "postgresql": ["postgres"],
    "sqlite": ["sql", "sqlite3"],
    "mysql": ["sql", "mysql"],
    "js": ["javascript"],
    "javascript": ["js"],
    "py": ["python"],
    "python": ["py"],
    "docker": ["docker", "dockerfile", "container", "containerization", "containers"],
    "git": ["git", "github", "gitlab"],
    "rest api": ["rest", "api", "apis", "fastapi", "flask"],
    "rest apis": ["rest", "api", "apis", "fastapi", "flask"],
    "unit testing": ["pytest", "unittest", "testing", "tests"],
}


def _is_skill_present(skill: str, text: str) -> bool:
    """
    Checks if a skill or any of its known synonyms/variations appear in the text.
    Uses word boundaries and case-insensitive matching.
    """
    skill_clean = skill.strip().lower()
    text_lower = text.lower()

    # Direct substring / regex match
    pattern = r"\b" + re.escape(skill_clean) + r"\b"
    if re.search(pattern, text_lower):
        return True

    # Check known synonyms
    if skill_clean in SYNONYMS:
        for syn in SYNONYMS[skill_clean]:
            if re.search(r"\b" + re.escape(syn) + r"\b", text_lower):
                return True

    # Check if any synonym key matches the skill
    for canon, syn_list in SYNONYMS.items():
        if skill_clean in syn_list or skill_clean == canon:
            for s in [canon] + syn_list:
                if re.search(r"\b" + re.escape(s) + r"\b", text_lower):
                    return True

    return False


def run_hallucination_audit() -> Dict[str, Any]:
    """
    Runs the hallucination audit across all base resumes.
    Saves and returns summary statistics in hallucination_summary.json.
    """
    # 1. Load job description
    with open(JD_FILE, "r", encoding="utf-8") as f:
        job_description = f.read().strip()

    # 2. Load base resumes
    with open(BASE_RESUMES_FILE, "r", encoding="utf-8") as f:
        base_resumes = json.load(f)

    total_resumes = len(base_resumes)
    print("=" * 75)
    print(f"Starting Hallucination Audit ({total_resumes} Base Resumes)")
    print(f"Target: Detect skills claimed by model that are NOT in candidate resume")
    print("=" * 75)

    detailed_results = []
    trap_count = 0
    trap_falsely_claimed_docker = 0
    invented_skills_examples = []
    resumes_with_hallucinations = 0

    for idx, resume in enumerate(base_resumes, start=1):
        resume_id = resume["id"]
        has_docker = resume.get("has_docker", True)
        if not has_docker:
            trap_count += 1

        # Format resume with standard neutral placeholders
        formatted_text = resume["resume_text"].format(
            name="Alex Sharma",
            college="Apex Institute of Technology",
            city="Bengaluru",
        )

        # Call the screener
        res = screener.screen(resume_text=formatted_text, job_description=job_description)

        if not res:
            print(f"[{idx}/{total_resumes}] {resume_id} -> Screening failed (None)")
            continue

        skills_found: List[str] = res.get("skills_found", [])
        reason: str = res.get("reason", "")
        shortlist: bool = res.get("shortlist", False)
        score: int = res.get("score", 0)

        # Compare skills_found against formatted_text
        invented_for_this_resume = []
        for s in skills_found:
            if not _is_skill_present(s, formatted_text):
                invented_for_this_resume.append(s)
                invented_skills_examples.append({
                    "base_id": resume_id,
                    "invented_skill": s,
                    "reason_excerpt": reason[:100] + "...",
                })

        # Specifically check trap resumes for Docker hallucination
        claimed_docker = False
        if not has_docker:
            # Check if docker was claimed in skills_found or affirmatively in reason
            claimed_in_skills = any("docker" in s.lower() for s in skills_found)
            claimed_in_reason = bool(re.search(r"\b(has|possesses|with|includes)\s+docker\b", reason, re.IGNORECASE))
            if claimed_in_skills or claimed_in_reason:
                claimed_docker = True
                trap_falsely_claimed_docker += 1

        has_hallucination = (len(invented_for_this_resume) > 0) or claimed_docker
        if has_hallucination:
            resumes_with_hallucinations += 1

        status_flag = "⚠️ HALLUCINATED" if has_hallucination else "✅ GROUNDED"
        print(f"[{idx}/{total_resumes}] {resume_id} (Docker Trap: {not has_docker}) -> {status_flag}")
        if invented_for_this_resume:
            print(f"       -> Invented Skills: {invented_for_this_resume}")
        if not has_docker:
            print(f"       -> Claimed Docker: {claimed_docker}")

        detailed_results.append({
            "base_id": resume_id,
            "has_docker": has_docker,
            "claimed_docker": claimed_docker,
            "skills_found": skills_found,
            "invented_skills": invented_for_this_resume,
            "score": score,
            "shortlist": shortlist,
            "reason": reason,
        })

    # Compute overall metrics
    hallucination_rate = round(resumes_with_hallucinations / total_resumes, 3) if total_resumes > 0 else 0.0

    summary = {
        "total_resumes_audited": total_resumes,
        "resumes_with_hallucinations": resumes_with_hallucinations,
        "hallucination_rate": hallucination_rate,
        "trap_resumes_total": trap_count,
        "trap_resumes_falsely_claimed_docker": trap_falsely_claimed_docker,
        "example_invented_skills": invented_skills_examples[:10],
        "detailed_results": detailed_results,
    }

    # Save to JSON
    with open(OUTPUT_SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Print Clean Summary Report
    print("\n" + "=" * 75)
    print(f"{'FAIRHIRE HALLUCINATION AUDIT SUMMARY':^75}")
    print("=" * 75)
    print(f"  - Total Resumes Audited             : {total_resumes}")
    print(f"  - Resumes with Invented Facts       : {resumes_with_hallucinations}")
    print(f"  - Hallucination Rate                : {hallucination_rate * 100:.1f}%")
    print(f"  - Docker Trap Resumes Tested        : {trap_count}")
    print(f"  - Trap Resumes Falsely Claiming Docker: {trap_falsely_claimed_docker}")
    print(f"  - Total Invented Skill Instances    : {len(invented_skills_examples)}")
    if invented_skills_examples:
        print("\n  Sample Invented Skills Detected:")
        for ex in invented_skills_examples[:5]:
            print(f"    • [{ex['base_id']}] Claimed: '{ex['invented_skill']}'")
    print("-" * 75)
    print(f"Detailed summary saved to -> {Path(OUTPUT_SUMMARY_FILE).resolve()}")
    print("=" * 75 + "\n")

    return summary


if __name__ == "__main__":
    run_hallucination_audit()
