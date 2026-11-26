"""
domains/hiring/screener.py - Resume Screener for Junior Python Developer
"""

from typing import Dict, Any, Optional
from core.llm import ask
from core.parser import extract_json_safely


def screen(resume_text: str, job_description: str) -> Optional[Dict[str, Any]]:
    prompt = f"""You are an automated resume screener. Evaluate the following candidate resume against the job description.

--- JOB DESCRIPTION ---
{job_description}

--- CANDIDATE RESUME ---
{resume_text}

--- INSTRUCTIONS ---
Return your evaluation strictly as a valid JSON object matching this exact schema:
{{
  "score": <integer from 0 to 100>,
  "shortlist": <true or false>,
  "skills_found": [<list of matching skills from JD found in resume>],
  "reason": "<one sentence explaining the score and shortlist decision>"
}}

Respond ONLY with the JSON object. Do not include any text before or after.
"""
    try:
        raw_response = ask(prompt)
        data = extract_json_safely(raw_response, required_keys={"score", "shortlist", "skills_found", "reason"})
        if not data:
            return None
        score = max(0, min(100, int(round(float(data["score"])))))
        return {
            "score": score,
            "shortlist": bool(data["shortlist"]),
            "skills_found": list(data["skills_found"]) if isinstance(data["skills_found"], list) else [],
            "reason": str(data["reason"]).strip(),
        }
    except Exception as e:
        print(f"[hiring/screener.py] Error: {e}")
        return None
