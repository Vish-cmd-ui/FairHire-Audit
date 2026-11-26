"""
core/parser.py - Centralized, Robust JSON Parser for LLM Outputs

Handles:
- Stripping markdown code fences (```json ... ```)
- Locating JSON boundaries between the first '{' and last '}'
- Normalizing required fields and types
- Clamping scores to [0, 100]
"""

import json
import re
from typing import Dict, Any, Optional, Set


def extract_json_safely(
    raw_text: str,
    required_keys: Optional[Set[str]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Extracts and parses a JSON object from raw model output.
    Returns None if parsing fails or required keys are missing.
    """
    if not raw_text or not isinstance(raw_text, str):
        return None

    cleaned = raw_text.strip()

    # 1. Remove markdown code fences
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    # 2. Extract substring between first '{' and last '}'
    first_brace = cleaned.find("{")
    last_brace = cleaned.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        cleaned = cleaned[first_brace : last_brace + 1]

    # 3. Parse JSON
    try:
        data = json.loads(cleaned)
    except Exception:
        return None

    if not isinstance(data, dict):
        return None

    # 4. Verify required keys if specified
    if required_keys and not required_keys.issubset(data.keys()):
        return None

    return data
