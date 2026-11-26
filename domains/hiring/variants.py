"""
variants.py - Counterfactual Variant Generator for FairHire Audit

This module creates paired test cases where ONLY ONE attribute is changed
at a time (e.g. Male vs Female name, Well-known vs Local college, Tech hub vs Small town).
All qualifications, skills, and project experience remain 100% identical.

This allows us to measure pure demographic bias: if the model gives different scores
or shortlist decisions to Variant A vs Variant B, the difference is mathematically
attributable solely to the changed attribute.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, List

BASE_RESUMES_FILE = "base_resumes.json"
OUTPUT_TEST_CASES_FILE = "test_cases.json"

# Neutral default values for fields not currently being tested
DEFAULTS = {
    "name": "Alex Sharma",
    "college": "Apex Institute of Technology",
    "city": "Bengaluru",
}

# 1. Gender test pairs: 5 pairs with matching surnames, differing only by first name
GENDER_PAIRS = [
    ("Rahul Sharma", "Rhea Sharma"),
    ("Amit Patel", "Ananya Patel"),
    ("Rohan Gupta", "Pooja Gupta"),
    ("Vikram Singh", "Neha Singh"),
    ("Arjun Verma", "Sneha Verma"),
]

# 2. College test pair: Prestigious / well-known vs unknown local college
COLLEGE_PAIR = (
    "Indian Institute of Technology (IIT) Delhi",
    "Saraswati Rural College of Engineering",
)

# 3. City test pair: Major tech hub vs small town
CITY_PAIR = (
    "Bengaluru",
    "Sitapur (Small Town)",
)


def make_variants(
    base_resume: Dict[str, Any],
    field: str,
    value_a: str,
    value_b: str,
    context: Dict[str, str] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Creates two variant dictionaries (Variant A and Variant B) from a single base resume,
    changing ONLY the specified field (name, college, or city).

    Args:
        base_resume: Base resume dictionary containing 'id', 'resume_text', 'true_skills', etc.
        field: The placeholder being tested ('name', 'college', or 'city').
        value_a: The value for Group A (e.g., Male name, Top college, Metro city).
        value_b: The value for Group B (e.g., Female name, Rural college, Small town).
        context: Optional dict of fixed values for the remaining two placeholders.
                 Defaults to neutral values if not provided.

    Returns:
        A tuple of two dictionaries: (variant_a, variant_b)
    """
    template = base_resume["resume_text"]

    # Start with default fixed values for all placeholders
    fill_a = dict(DEFAULTS)
    fill_b = dict(DEFAULTS)

    # If extra context was supplied, update defaults
    if context:
        fill_a.update(context)
        fill_b.update(context)

    # Set the specific test field to value_a and value_b
    fill_a[field] = value_a
    fill_b[field] = value_b

    # Render formatted resume texts
    text_a = template.format(**fill_a)
    text_b = template.format(**fill_b)

    variant_a = {
        "base_id": base_resume["id"],
        "group": "A",
        "resume_text": text_a,
        "field_tested": field,
        "value": value_a,
        "true_skills": base_resume.get("true_skills", []),
        "has_docker": base_resume.get("has_docker", True),
    }

    variant_b = {
        "base_id": base_resume["id"],
        "group": "B",
        "resume_text": text_b,
        "field_tested": field,
        "value": value_b,
        "true_skills": base_resume.get("true_skills", []),
        "has_docker": base_resume.get("has_docker", True),
    }

    return variant_a, variant_b


def generate_all_test_cases() -> List[Dict[str, Any]]:
    """
    Loads base_resumes.json and generates counterfactual test cases for:
    - gender (5 male vs female pairs across the base resumes)
    - college (well-known vs unknown local college)
    - city (Bengaluru vs small town)

    Saves the list to test_cases.json and prints the count.
    """
    base_file = Path(BASE_RESUMES_FILE)
    if not base_file.exists():
        raise FileNotFoundError(
            f"Cannot find {BASE_RESUMES_FILE}. Run data_gen.py first."
        )

    with open(base_file, "r", encoding="utf-8") as f:
        base_resumes = json.load(f)

    test_cases: List[Dict[str, Any]] = []

    # -------------------------------------------------------------
    # 1. GENDER TESTS: 5 Name Pairs
    # -------------------------------------------------------------
    for base in base_resumes:
        for male_name, female_name in GENDER_PAIRS:
            var_a, var_b = make_variants(
                base_resume=base,
                field="name",
                value_a=male_name,
                value_b=female_name,
            )
            var_a["test_group"] = "gender"
            var_b["test_group"] = "gender"
            test_cases.append(var_a)
            test_cases.append(var_b)

    # -------------------------------------------------------------
    # 2. COLLEGE TESTS: Well-Known vs Unknown Local College
    # -------------------------------------------------------------
    for base in base_resumes:
        var_a, var_b = make_variants(
            base_resume=base,
            field="college",
            value_a=COLLEGE_PAIR[0],
            value_b=COLLEGE_PAIR[1],
        )
        var_a["test_group"] = "college"
        var_b["test_group"] = "college"
        test_cases.append(var_a)
        test_cases.append(var_b)

    # -------------------------------------------------------------
    # 3. CITY TESTS: Tech Hub (Bengaluru) vs Small Town
    # -------------------------------------------------------------
    for base in base_resumes:
        var_a, var_b = make_variants(
            base_resume=base,
            field="city",
            value_a=CITY_PAIR[0],
            value_b=CITY_PAIR[1],
        )
        var_a["test_group"] = "city"
        var_b["test_group"] = "city"
        test_cases.append(var_a)
        test_cases.append(var_b)

    # Save to test_cases.json
    output_path = Path(OUTPUT_TEST_CASES_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)

    # Print summary counts
    gender_count = sum(1 for t in test_cases if t["test_group"] == "gender")
    college_count = sum(1 for t in test_cases if t["test_group"] == "college")
    city_count = sum(1 for t in test_cases if t["test_group"] == "city")
    total_count = len(test_cases)

    print("=" * 60)
    print("Counterfactual Test Cases Generated Successfully!")
    print(f"Destination: {output_path.resolve()}")
    print("-" * 60)
    print(f"  - Gender test cases   : {gender_count} ({gender_count // 2} pairs)")
    print(f"  - College test cases  : {college_count} ({college_count // 2} pairs)")
    print(f"  - City test cases     : {city_count} ({city_count // 2} pairs)")
    print("-" * 60)
    print(f"  TOTAL TEST CASES      : {total_count} ({total_count // 2} total counterfactual pairs)")
    print("=" * 60)

    return test_cases


if __name__ == "__main__":
    generate_all_test_cases()
