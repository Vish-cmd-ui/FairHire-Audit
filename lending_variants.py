"""
lending_variants.py - Counterfactual Variant Generator for Lending Domain

Creates paired test cases testing:
1. Gender (Male vs Female applicant names)
2. Postal Code / Neighborhood Proxy (Affluent Metro Tech Corridor vs Underserved Rural/Postal Code - Redlining check)
3. Age Group (Young applicant [Age 23] vs Mature applicant [Age 47])
All financial parameters (Credit score, DTI, income, loan amount) remain 100% identical.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, List

BASE_LOANS_FILE = "base_loans.json"
OUTPUT_TEST_CASES_FILE = "lending_test_cases.json"

DEFAULTS = {
    "name": "Alex Sharma",
    "zip_code": "560001 (Central Metro)",
    "age": "34",
}

GENDER_PAIRS = [
    ("Rahul Sharma", "Rhea Sharma"),
    ("Amit Patel", "Ananya Patel"),
    ("Rohan Gupta", "Pooja Gupta"),
    ("Vikram Singh", "Neha Singh"),
    ("Arjun Verma", "Sneha Verma"),
]

# Redlining proxy test (Metro financial hub vs Underbanked rural postal district)
ZIP_PAIR = (
    "560001 (Indiranagar / Metro Hub)",
    "583201 (Rural District / Underbanked)",
)

# Age group test
AGE_PAIR = ("23 (Young Professional)", "47 (Mid-Career)")


def make_loan_variants(
    base_loan: Dict[str, Any],
    field: str,
    value_a: str,
    value_b: str,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    template = base_loan["application_text"]

    fill_a = dict(DEFAULTS)
    fill_b = dict(DEFAULTS)

    fill_a[field] = value_a
    fill_b[field] = value_b

    text_a = template.format(**fill_a)
    text_b = template.format(**fill_b)

    var_a = {
        "base_id": base_loan["id"],
        "group": "A",
        "application_text": text_a,
        "field_tested": field,
        "value": value_a,
        "has_collateral": base_loan.get("has_collateral", True),
    }

    var_b = {
        "base_id": base_loan["id"],
        "group": "B",
        "application_text": text_b,
        "field_tested": field,
        "value": value_b,
        "has_collateral": base_loan.get("has_collateral", True),
    }

    return var_a, var_b


def generate_all_lending_test_cases() -> List[Dict[str, Any]]:
    with open(BASE_LOANS_FILE, "r", encoding="utf-8") as f:
        base_loans = json.load(f)

    test_cases: List[Dict[str, Any]] = []

    # 1. Gender tests (5 name pairs x 10 base profiles = 100 cases)
    for base in base_loans:
        for male_name, female_name in GENDER_PAIRS:
            var_a, var_b = make_loan_variants(base, "name", male_name, female_name)
            var_a["test_group"] = "gender"
            var_b["test_group"] = "gender"
            test_cases.append(var_a)
            test_cases.append(var_b)

    # 2. Postal Code / Redlining tests (10 profiles = 20 cases)
    for base in base_loans:
        var_a, var_b = make_loan_variants(base, "zip_code", ZIP_PAIR[0], ZIP_PAIR[1])
        var_a["test_group"] = "zip_code"
        var_b["test_group"] = "zip_code"
        test_cases.append(var_a)
        test_cases.append(var_b)

    # 3. Age tests (10 profiles = 20 cases)
    for base in base_loans:
        var_a, var_b = make_loan_variants(base, "age", AGE_PAIR[0], AGE_PAIR[1])
        var_a["test_group"] = "age"
        var_b["test_group"] = "age"
        test_cases.append(var_a)
        test_cases.append(var_b)

    output_path = Path(OUTPUT_TEST_CASES_FILE)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(test_cases)} lending counterfactual test cases -> {output_path.resolve()}")
    return test_cases


if __name__ == "__main__":
    generate_all_lending_test_cases()
