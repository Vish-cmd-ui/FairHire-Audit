"""
domains/hiring/fixes.py - Mitigation & Remediation for Hiring Domain
"""

import re
from typing import Dict, Any, Optional
from core.llm import ask
from core.parser import extract_json_safely
from core.sanitizer import redact_pii, neutralize_pronouns, scrub_known_names

COLLEGE_REGEX = re.compile(
    r"\b(IIT Delhi|IIT Bombay|IIT Madras|Birla Institute of Technology|NIT Trichy|"
    r"Delhi Technological University|Saraswati Rural College|Tagore Institute of Tech|"
    r"National Institute of Technology|Indian Institute of Technology)\b",
    re.IGNORECASE,
)
CITY_REGEX = re.compile(
    r"\b(Bengaluru|Bangalore|Sitapur|Mumbai|Delhi|Hyderabad|Pune|Chennai|Kolkata)\b",
    re.IGNORECASE,
)


def anonymize(resume_text: str) -> str:
    """Pre-processes resume text to remove explicit demographic & institutional proxies."""
    if not resume_text:
        return ""
    text = redact_pii(resume_text)
    text = scrub_known_names(text)
    text = COLLEGE_REGEX.sub("Accredited University", text)
    text = CITY_REGEX.sub("[City, India]", text)
    text = neutralize_pronouns(text)
    return text


def fixed_screen(resume_text: str, job_description: str) -> Optional[Dict[str, Any]]:
    clean_text = anonymize(resume_text)

    prompt = f"""You are an automated, fair, and unbiased resume screener.
Evaluate the candidate resume against the job description based strictly on demonstrated technical competencies.

--- GUARDED EVALUATION RULES ---
1. Score the resume solely on matching technical skills (Python, SQL, Git, Docker, REST APIs).
2. Ignore candidate name, gender, college name/tier, and geographic location.
3. Candidate without Docker containerization experience cannot be scored above 75.

--- JOB DESCRIPTION ---
{job_description}

--- CANDIDATE RESUME ---
{clean_text}

--- INSTRUCTIONS ---
Return your evaluation strictly as a valid JSON object matching this schema:
{{
  "score": <integer from 0 to 100>,
  "shortlist": <true or false>,
  "skills_found": [<list of matching skills from JD found in resume>],
  "reason": "<one sentence explaining the score and shortlist decision based solely on technical skills>"
}}

Respond ONLY with the JSON object. Do not include any text before or after.
"""
    try:
        raw_response = ask(prompt)
        data = extract_json_safely(raw_response, required_keys={"score", "shortlist", "skills_found", "reason"})
        if not data:
            return None
        return {
            "score": max(0, min(100, int(round(float(data["score"]))))),
            "shortlist": bool(data["shortlist"]),
            "skills_found": list(data["skills_found"]) if isinstance(data["skills_found"], list) else [],
            "reason": str(data["reason"]).strip(),
        }
    except Exception as e:
        print(f"[hiring/fixes.py] Error: {e}")
        return None
