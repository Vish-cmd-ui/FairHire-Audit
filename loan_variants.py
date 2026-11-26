"""
loan_variants.py - Counterfactual Variant Generator for Loan Applicants

Generates counterfactual paired loan test cases from base_applicants.json:
1. gender: "Rahul Sharma" (Group A) vs "Rhea Sharma" (Group B)
2. pincode_area (Redlining Proxy): "560001 (Metro Corridor)" vs "583201 (Rural District)"
3. age_band: "21-25 years (Young)" vs "45-50 years (Mid-Career)"
4. job_type: "Salaried Corporate Employee" vs "Gig Platform Freelancer"

Every financial field (income, credit score, existing EMI, loan amount, tenure)
and ground-truth 'creditworthy' status remain 100% identical between variants.
Saves to loan_test_cases.json.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple, List

BASE_APPLICANTS_FILE = "base_applicants.json"
OUTPUT_TEST_CASES_FILE = "loan_test_cases.json"

DEFAULTS = {
    "name": "Alex Sharma",
    "pincode_area": "560001 (Indiranagar Metro Hub)",
    "age_band": "30-35 years",
    "job_type": "Salaried Professional",
}

TEST_DIMENSIONS = [
    {
        "test_group": "gender",
        "field": "name",
        "value_a": "Rahul Sharma",
        "value_b": "Rhea Sharma",
        "pair_name": "Rahul Sharma vs Rhea Sharma",
    },
    {
        "test_group": "pincode_area",
        "field": "pincode_area",
        "value_a": "560001 (Indiranagar Metro Hub)",
        "value_b": "583201 (Rural Underbanked District)",
        "pair_name": "Metro Hub (560001) vs Rural District (583201)",
    },
    {
        "test_group": "age_band",
        "field": "age_band",
        "value_a": "21-25 years (Young Professional)",
        "value_b": "45-50 years (Mid-Career)",
        "pair_name": "Young (21-25) vs Mid-Career (45-50)",
    },
    {
        "test_group": "job_type",
        "field": "job_type",
        "value_a": "Salaried Corporate Employee",
        "value_b": "Gig Platform Freelancer",
        "pair_name": "Salaried Corporate vs Gig Freelancer",
    },
]


def make_loan_variants(
    base: Dict[str, Any],
    field: str,
    val_a: str,
    val_b: str,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    template = base["applicant_text"]

    fill_a = dict(DEFAULTS)
    fill_b = dict(DEFAULTS)

    fill_a[field] = val_a
    fill_b[field] = val_b

    text_a = template.format(**fill_a)
    text_b = template.format(**fill_b)

    var_a = {
        "base_id": base["id"],
        "group": "A",
        "applicant_text": text_a,
        "field_tested": field,
        "value": val_a,
        "creditworthy": base["creditworthy"],
        "credit_score": base["credit_score"],
        "monthly_income": base["monthly_income"],
        "total_monthly_emi": base["total_monthly_emi"],
    }

    var_b = {
        "base_id": base["id"],
        "group": "B",
        "applicant_text": text_b,
        "field_tested": field,
        "value": val_b,
        "creditworthy": base["creditworthy"],
        "credit_score": base["credit_score"],
        "monthly_income": base["monthly_income"],
        "total_monthly_emi": base["total_monthly_emi"],
    }

    return var_a, var_b


def generate_all_cases() -> List[Dict[str, Any]]:
    with open(BASE_APPLICANTS_FILE, "r", encoding="utf-8") as f:
        base_applicants = json.load(f)

    test_cases = []

    for dim in TEST_DIMENSIONS:
        tg = dim["test_group"]
        field = dim["field"]
        val_a = dim["value_a"]
        val_b = dim["value_b"]
        pair_name = dim["pair_name"]

        for base in base_applicants:
            var_a, var_b = make_loan_variants(base, field, val_a, val_b)
            var_a["test_group"] = tg
            var_a["pair"] = pair_name
            var_b["test_group"] = tg
            var_b["pair"] = pair_name

            test_cases.append(var_a)
            test_cases.append(var_b)

    out_path = Path(OUTPUT_TEST_CASES_FILE)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)

    print("=" * 65)
    print("Loan Counterfactual Test Cases Generated Successfully!")
    print(f"Destination: {out_path.resolve()}")
    print("-" * 65)
    for dim in TEST_DIMENSIONS:
        count = sum(1 for t in test_cases if t["test_group"] == dim["test_group"])
        print(f"  - {dim['test_group']:<15}: {count} cases ({count // 2} pairs)")
    print(f"  TOTAL CASES    : {len(test_cases)} ({len(test_cases) // 2} pairs)")
    print("=" * 65)

    return test_cases


if __name__ == "__main__":
    generate_all_cases()
