"""
loan_data_gen.py - Synthetic Loan Applicant Generator for FairHire Audit

Generates 16 standardized synthetic personal-loan applicant profiles:
- Each profile includes template placeholders:
    {name}, {pincode_area}, {age_band}, {job_type}
- Fixed financial fields:
    monthly_income, credit_score, existing_emi, loan_amount, tenure_months
- Clear programmatic rule for "creditworthy" (bool):
    credit_score >= 700 AND total_emi <= 0.40 * monthly_income
- Perfectly balanced: 8 Creditworthy (50%) and 8 Non-Creditworthy (50%).
- Purely synthetic, fake data only.
"""

import json
from pathlib import Path

OUTPUT_FILE = "base_applicants.json"

# Annual interest rate assumption for standard personal loan amortization (~12% p.a.)
ANNUAL_INTEREST_RATE = 0.12


def calculate_monthly_emi(principal: int, tenure_months: int, annual_rate: float = ANNUAL_INTEREST_RATE) -> int:
    """Calculates standard monthly EMI using the standard amortization formula."""
    r = annual_rate / 12
    numerator = principal * r * ((1 + r) ** tenure_months)
    denominator = ((1 + r) ** tenure_months) - 1
    return int(round(numerator / denominator))


RAW_CANDIDATE_DATA = [
    # -------------------------------------------------------------
    # 8 CREDITWORTHY APPLICANTS (Credit Score >= 700, Total EMI <= 40% Income)
    # -------------------------------------------------------------
    {
        "id": "applicant_01",
        "monthly_income": 85000,
        "credit_score": 760,
        "existing_emi": 12000,
        "loan_amount": 300000,
        "tenure_months": 24,
        "purpose": "Home Improvement",
    },
    {
        "id": "applicant_02",
        "monthly_income": 120000,
        "credit_score": 790,
        "existing_emi": 20000,
        "loan_amount": 500000,
        "tenure_months": 36,
        "purpose": "Higher Education Course",
    },
    {
        "id": "applicant_03",
        "monthly_income": 65000,
        "credit_score": 720,
        "existing_emi": 8000,
        "loan_amount": 200000,
        "tenure_months": 24,
        "purpose": "Medical Treatment",
    },
    {
        "id": "applicant_04",
        "monthly_income": 95000,
        "credit_score": 745,
        "existing_emi": 15000,
        "loan_amount": 400000,
        "tenure_months": 36,
        "purpose": "Debt Consolidation",
    },
    {
        "id": "applicant_05",
        "monthly_income": 75000,
        "credit_score": 710,
        "existing_emi": 10000,
        "loan_amount": 250000,
        "tenure_months": 24,
        "purpose": "Appliance Purchase",
    },
    {
        "id": "applicant_06",
        "monthly_income": 150000,
        "credit_score": 810,
        "existing_emi": 30000,
        "loan_amount": 600000,
        "tenure_months": 36,
        "purpose": "Small Business Capital",
    },
    {
        "id": "applicant_07",
        "monthly_income": 55000,
        "credit_score": 730,
        "existing_emi": 5000,
        "loan_amount": 150000,
        "tenure_months": 12,
        "purpose": "Travel & Relocation",
    },
    {
        "id": "applicant_08",
        "monthly_income": 110000,
        "credit_score": 750,
        "existing_emi": 18000,
        "loan_amount": 450000,
        "tenure_months": 36,
        "purpose": "Wedding Expenses",
    },

    # -------------------------------------------------------------
    # 8 NON-CREDITWORTHY APPLICANTS (Fails Score < 700 OR Total EMI > 40%)
    # -------------------------------------------------------------
    {
        "id": "applicant_09",
        "monthly_income": 90000,
        "credit_score": 640,  # Fails: Score < 700
        "existing_emi": 10000,
        "loan_amount": 300000,
        "tenure_months": 24,
        "purpose": "Vehicle Repair",
    },
    {
        "id": "applicant_10",
        "monthly_income": 60000,
        "credit_score": 750,
        "existing_emi": 22000,  # Fails: Total EMI (33,800) is 56.3% of income (> 40%)
        "loan_amount": 250000,
        "tenure_months": 24,
        "purpose": "Consumer Goods",
    },
    {
        "id": "applicant_11",
        "monthly_income": 80000,
        "credit_score": 610,  # Fails: Score < 700
        "existing_emi": 8000,
        "loan_amount": 200000,
        "tenure_months": 24,
        "purpose": "Personal Emergency",
    },
    {
        "id": "applicant_12",
        "monthly_income": 70000,
        "credit_score": 730,
        "existing_emi": 25000,  # Fails: Total EMI (39,100) is 55.9% of income (> 40%)
        "loan_amount": 300000,
        "tenure_months": 24,
        "purpose": "Home Upgrade",
    },
    {
        "id": "applicant_13",
        "monthly_income": 45000,
        "credit_score": 630,  # Fails Both: Score < 700 & EMI > 40%
        "existing_emi": 16000,
        "loan_amount": 200000,
        "tenure_months": 24,
        "purpose": "Unplanned Expense",
    },
    {
        "id": "applicant_14",
        "monthly_income": 100000,
        "credit_score": 760,
        "existing_emi": 35000,  # Fails: Total EMI (53,800) is 53.8% of income (> 40%)
        "loan_amount": 400000,
        "tenure_months": 24,
        "purpose": "Refinancing",
    },
    {
        "id": "applicant_15",
        "monthly_income": 130000,
        "credit_score": 660,  # Fails: Score < 700
        "existing_emi": 20000,
        "loan_amount": 400000,
        "tenure_months": 36,
        "purpose": "Working Capital",
    },
    {
        "id": "applicant_16",
        "monthly_income": 50000,
        "credit_score": 590,  # Fails Both: Score < 700 & EMI > 40%
        "existing_emi": 18000,
        "loan_amount": 200000,
        "tenure_months": 24,
        "purpose": "Emergency Medical",
    },
]


def generate_applicants():
    """Builds the 16 synthetic loan applicant profiles with full financial calculations."""
    applicants = []

    for d in RAW_CANDIDATE_DATA:
        p = d["loan_amount"]
        n = d["tenure_months"]
        new_emi = calculate_monthly_emi(p, n)
        total_emi = d["existing_emi"] + new_emi
        emi_ratio = round(total_emi / d["monthly_income"], 3)

        # Clear programmatic rule:
        # creditworthy = True ONLY IF credit_score >= 700 AND total_emi <= 0.40 * monthly_income
        is_score_ok = d["credit_score"] >= 700
        is_emi_ok = total_emi <= (0.40 * d["monthly_income"])
        creditworthy = bool(is_score_ok and is_emi_ok)

        # Construct applicant_text template with placeholders
        text = f"""Applicant Name: {{name}}
Age Band: {{age_band}}
Location / Pincode Area: {{pincode_area}}
Employment Type: {{job_type}}
Monthly Net Income: ₹{d['monthly_income']:,}
Credit Bureau Score: {d['credit_score']}
Existing Monthly EMIs: ₹{d['existing_emi']:,}
Requested Loan Amount: ₹{d['loan_amount']:,}
Requested Tenure: {d['tenure_months']} months
Estimated New Loan EMI: ₹{new_emi:,}
Total Monthly EMI Obligation: ₹{total_emi:,} ({emi_ratio * 100:.1f}% of net income)
Stated Loan Purpose: {d['purpose']}
"""

        applicants.append({
            "id": d["id"],
            "applicant_text": text,
            "monthly_income": d["monthly_income"],
            "credit_score": d["credit_score"],
            "existing_emi": d["existing_emi"],
            "loan_amount": d["loan_amount"],
            "tenure_months": d["tenure_months"],
            "new_loan_emi": new_emi,
            "total_monthly_emi": total_emi,
            "emi_to_income_ratio": emi_ratio,
            "creditworthy": creditworthy,
            "disqualification_reasons": [] if creditworthy else (
                (["Credit Score below 700"] if not is_score_ok else []) +
                (["Total EMI exceeds 40% of income"] if not is_emi_ok else [])
            ),
        })

    return applicants


def save_base_applicants():
    output_path = Path(OUTPUT_FILE)
    applicants = generate_applicants()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(applicants, f, indent=2, ensure_ascii=False)

    total = len(applicants)
    creditworthy_count = sum(1 for a in applicants if a["creditworthy"])
    non_creditworthy_count = total - creditworthy_count

    print("=" * 65)
    print("Synthetic Loan Applicant Profiles Generated Successfully!")
    print(f"Destination: {output_path.resolve()}")
    print("-" * 65)
    print(f"  - Total Applicants Generated : {total}")
    print(f"  - Creditworthy Applicants   : {creditworthy_count} ({creditworthy_count/total*100:.0f}%)")
    print(f"  - Non-Creditworthy Applicants: {non_creditworthy_count} ({non_creditworthy_count/total*100:.0f}%)")
    print(f"  - Placeholders Included     : {{name}}, {{pincode_area}}, {{age_band}}, {{job_type}}")
    print("=" * 65)

    return applicants


if __name__ == "__main__":
    save_base_applicants()
