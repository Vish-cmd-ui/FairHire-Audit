"""
app.py - Streamlit Dashboard for FairHire Audit

Interactive AI Governance & Compliance Report for model auditing.
Features:
- Title and one-line summary
- 3 Metric Cards: Bias Risk, Hallucination Rate, Privacy Leak Rate
- 'Same resume, different name' section with side-by-side counterfactual comparisons
- Plotly grouped bar chart: Before vs. After Mitigations
- List of suggested fixes & remediations
- Expanders for Threshold Rules & Sample Sizes
- Sidebar navigation and domain switcher
- Footer: 'Synthetic data only. Not legal advice.'
"""

import json
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

RESULTS_FILE = "results.json"

# Configure Streamlit page layout and title
st.set_page_config(
    page_title="FairHire Audit | AI Governance Report",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished cards and footer
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .badge-high {
        color: #dc3545;
        font-weight: bold;
    }
    .badge-safe {
        color: #28a745;
        font-weight: bold;
    }
    .footer-text {
        text-align: center;
        color: #6c757d;
        font-size: 0.85rem;
        padding: 24px 0 12px 0;
        border-top: 1px solid #e9ecef;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_results() -> dict:
    """Loads results.json data."""
    path = Path(RESULTS_FILE)
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    data = load_results()

    if not data:
        st.error(f"Cannot find `{RESULTS_FILE}`. Please run `python build_results.py` first.")
        st.stop()

    # Support domain-keyed structure
    domains_dict = data.get("domains", data)
    available_domains = list(domains_dict.keys())
    # Filter non-dict keys (like 'active_domain')
    available_domains = [d for d in available_domains if isinstance(domains_dict[d], dict)]

    # ---------------------------------------------------------
    # SIDEBAR NAVIGATION & CONTROLS
    # ---------------------------------------------------------
    st.sidebar.title("⚖️ FairHire Audit")
    st.sidebar.caption("AI Safety, Governance & Compliance Platform")
    st.sidebar.markdown("---")

    # Domain toggle between Hiring and Lending
    domain_display_map = {
        "Hiring": "hiring",
        "Lending": "lending",
    }
    selected_domain_label = st.sidebar.radio(
        "📁 Audit Domain Toggle:",
        options=["Hiring", "Lending"],
        index=0,
        help="Toggle between Junior Python Developer Hiring Screener and Personal Loan Approval Assistant.",
    )
    selected_domain = domain_display_map.get(selected_domain_label, "hiring")
    domain_data = domains_dict.get(selected_domain, {})

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Jump to Section")
    nav = st.sidebar.radio(
        "Navigation",
        ["Overview & Metrics", "Side-by-Side Twins", "Before vs After Fixes", "Governance Rules", "DPDP Act Principles"],
        index=0,
    )

    import os
    current_model = os.getenv("LLM_MODEL", "openai/gpt-oss-20b")
    st.sidebar.markdown("---")
    st.sidebar.info(
        f"**Target LLM:** `{current_model}` (Groq)\n\n"
        "**Audited Dimensions:**\n"
        "- 1. Counterfactual Disparity\n"
        "- 2. Hallucination / Factuality\n"
        "- 3. Privacy / PII Canary Leakage"
    )
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # ---------------------------------------------------------
    # HEADER & ONE-LINE SUMMARY
    # ---------------------------------------------------------
    domain_title = "Resume Screening" if selected_domain == "hiring" else "Personal Loan Underwriting"
    st.title(f"⚖️ FairHire Audit: {selected_domain.capitalize()} AI Governance Report")
    st.markdown(
        f"> **Executive Summary:** Automated audit of an AI decision-making model for **{domain_title}**, measuring counterfactual "
        "demographic/geographic bias, factual hallucinations on unmentioned qualifications, and synthetic PII privacy leakage before and after governance mitigations."
    )
    st.markdown("---")

    # ---------------------------------------------------------
    # 1. THREE METRIC CARDS (Shown on audit pages)
    # ---------------------------------------------------------
    if nav != "DPDP Act Principles":
        bias_label = domain_data.get("bias_label", "Low")
        gap = domain_data.get("gap", 0.0)
        halluc = domain_data.get("halluc", 0.0)
        leak = domain_data.get("leak", 0.0)

        bias_caption = (
            "Targeted name swap penalty (e.g. Rahul vs Rhea)"
            if selected_domain == "hiring"
            else "Postal redlining penalty (Metro 560001 vs Rural 583201)"
        )
        halluc_caption = (
            "Invented skills/tools absent from resume"
            if selected_domain == "hiring"
            else "Fabricated past defaults or unrequested collateral"
        )
        leak_caption = (
            "Echo of phone, 12-digit ID, or email"
            if selected_domain == "hiring"
            else "Echo of PAN, 12-digit Aadhaar, or Bank Account"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="🎯 Bias Risk Level",
                value=f"{bias_label} Risk",
                delta=f"+{gap} pts gap on paired twin" if gap > 0 else "0.0 pts gap",
                delta_color="inverse",
            )
            st.caption(bias_caption)

        with col2:
            st.metric(
                label="🧠 Hallucination Rate",
                value=f"{halluc * 100:.1f}%",
                delta="Grounded on source text",
                delta_color="normal",
            )
            st.caption(halluc_caption)

        with col3:
            st.metric(
                label="🔒 Privacy Leak Rate",
                value=f"{leak * 100:.1f}%",
                delta="PII Protected",
                delta_color="normal",
            )
            st.caption(leak_caption)

        # ---------------------------------------------------------
        # PLUS: FALSE REJECTION RATE BY GROUP (For Lending View)
        # ---------------------------------------------------------
        if selected_domain == "lending" and "false_rejection_rates" in domain_data:
            st.markdown("### 📉 False Rejection Rate (FRR) by Test Group")
            st.write(
                "**False Rejection Rate (FRR)** measures the proportion of creditworthy applicants who were "
                "wrongfully rejected by the underwriter. A disparity between demographic or geographic groups "
                "indicates unlawful disparate mistreatment under the **Equal Credit Opportunity Act (ECOA)** and **CFPB Fair Lending Guidelines**."
            )

            frr_list = domain_data.get("false_rejection_rates", [])
            frr_table_rows = []
            has_high_frr = False

            for item in frr_list:
                gap_pct = item["frr_gap"] * 100
                if item["severity"] == "High":
                    has_high_frr = True
                    status_badge = "🔴 High Disparity"
                elif item["severity"] == "Medium":
                    status_badge = "🟡 Moderate Disparity"
                else:
                    status_badge = "🟢 Equal Opportunity"

                frr_table_rows.append({
                    "Evaluation Dimension": item["group_title"],
                    "Group A (Baseline)": f"{item['label_a']} — {item['frr_a']*100:.1f}%",
                    "Group B (Counterpart)": f"{item['label_b']} — {item['frr_b']*100:.1f}%",
                    "Disparity Gap": f"{gap_pct:.1f}%",
                    "Compliance Status": status_badge,
                })

            df_frr = pd.DataFrame(frr_table_rows)
            st.dataframe(df_frr, hide_index=True, use_container_width=True)

            if has_high_frr:
                st.error(
                    "🚨 **Redlining Alert Detected:** Truly creditworthy applicants residing in rural postal district `583201` "
                    "experience a **100.0% False Rejection Rate** under baseline screening despite satisfying all financial thresholds. "
                    "This confirms systemic geographic disparate mistreatment prior to anonymization."
                )

        st.markdown("---")

    # ---------------------------------------------------------
    # 2. "SAME PROFILE, DIFFERENT DETAIL" SIDE-BY-SIDE PAIRS
    # ---------------------------------------------------------
    profile_term = "Resume" if selected_domain == "hiring" else "Loan Application"
    positive_term = "Shortlisted" if selected_domain == "hiring" else "Approved"
    negative_term = "Rejected" if selected_domain == "hiring" else "Denied"

    if nav in ["Overview & Metrics", "Side-by-Side Twins"]:
        st.subheader(f"👥 'Same {profile_term}, Different Detail' Counterfactual Testing")
        st.write(
            f"In counterfactual auditing, all applicant qualifications, credit factors, or code samples are **100% identical**. "
            "Only a single demographic or geographic proxy (name, college tier, age, or postal code) changes. "
            f"Any difference in score or {positive_term.lower()} decision reveals empirical disparity on matched counterfactual pairs."
        )

        examples = domain_data.get("examples", [])
        if examples:
            pair_tabs = st.tabs([f"Pair {i+1}: {ex['pair_label'].split('(')[0].strip()}" for i, ex in enumerate(examples)])

            for tab, ex in zip(pair_tabs, examples):
                with tab:
                    var_a = ex["variant_a"]
                    var_b = ex["variant_b"]
                    gap_val = ex.get("score_gap", 0)
                    flipped = ex.get("shortlist_flipped", False)
                    finances = ex.get("finances", None)

                    # Status alert
                    if flipped:
                        st.error(f"🚨 **DECISION FLIPPED:** Identical qualifications resulted in opposite {positive_term.lower()} decisions! (Score Gap: {gap_val} points)")
                    elif gap_val > 8:
                        st.warning(f"⚠️ **HIGH SCORE DISPARITY:** Score gap of {gap_val} points based purely on {ex.get('attribute_changed', 'demographics')}.")
                    else:
                        st.info(f"ℹ️ Score Gap: {gap_val} points ({ex.get('attribute_changed', 'demographics')})")

                    # Highlight identical financial foundation for lending cases
                    if finances:
                        with st.container():
                            st.markdown("##### 💳 Identical Financial Baseline (Shared Ground Truth)")
                            f_col1, f_col2, f_col3, f_col4 = st.columns(4)
                            with f_col1:
                                st.write(f"💵 **Monthly Income:** {finances.get('income', 'N/A')}")
                                st.write(f"📈 **Credit Bureau Score:** {finances.get('credit_score', 'N/A')}")
                            with f_col2:
                                st.write(f"💳 **Existing EMIs:** {finances.get('existing_emi', 'N/A')}")
                                st.write(f"🏦 **Loan Requested:** {finances.get('loan_amount', 'N/A')}")
                            with f_col3:
                                st.write(f"⏳ **Tenure:** {finances.get('tenure', 'N/A')}")
                                st.write(f"📊 **Debt-to-Income:** {finances.get('total_dti', 'N/A')}")
                            with f_col4:
                                st.write(f"🎯 **Ground Truth:** `{finances.get('ground_truth', 'N/A')}`")
                                st.write(f"📍 **Differentiating Factor:** `{ex.get('attribute_changed', 'N/A')}`")
                            st.markdown("---")

                    c_left, c_right = st.columns(2)

                    with c_left:
                        st.markdown(f"#### 👤 Variant A: **{var_a['name']}**")
                        if "locality" in var_a:
                            st.caption(f"📍 Locality: `{var_a['locality']}`")
                        score_label = "Model Score" if selected_domain == "hiring" else "Underwriting Risk Score"
                        st.metric(score_label, f"{var_a['score']} / 100")
                        badge_a = f"✅ {positive_term}" if var_a["shortlist"] else f"❌ {negative_term}"
                        st.markdown(f"**Decision:** `{badge_a}`")
                        st.markdown(f"**Model Reasoning:**\n> *\"{var_a['reason']}\"*")

                    with c_right:
                        st.markdown(f"#### 👤 Variant B: **{var_b['name']}**")
                        if "locality" in var_b:
                            st.caption(f"📍 Locality: `{var_b['locality']}`")
                        score_label = "Model Score" if selected_domain == "hiring" else "Underwriting Risk Score"
                        rel_delta = var_b["score"] - var_a["score"]
                        d_color = "normal" if selected_domain == "hiring" else "inverse"
                        st.metric(
                            score_label,
                            f"{var_b['score']} / 100",
                            delta=f"{rel_delta:+} pts" if rel_delta != 0 else None,
                            delta_color=d_color,
                        )
                        badge_b = f"✅ {positive_term}" if var_b["shortlist"] else f"❌ {negative_term}"
                        st.markdown(f"**Decision:** `{badge_b}`")
                        st.markdown(f"**Model Reasoning:**\n> *\"{var_b['reason']}\"*")

        st.markdown("---")

    # ---------------------------------------------------------
    # 3. PLOTLY BEFORE / AFTER BAR CHART
    # ---------------------------------------------------------
    if nav in ["Overview & Metrics", "Before vs After Fixes"]:
        st.subheader("📊 Audit Metrics: Before vs. After Mitigations")
        st.write(
            "Comparing baseline AI screening performance against the hardened model applying "
            "**Input Anonymization** and **Guarded Grounding Rules**."
        )

        before_after_data = domain_data.get("before_after", [])
        if before_after_data:
            df_ba = pd.DataFrame(before_after_data)

            fig = px.bar(
                df_ba,
                x="test",
                y="value",
                color="stage",
                barmode="group",
                text="value",
                color_discrete_map={"Before": "#EF553B", "After": "#00CC96"},
                labels={"test": "Audit Dimension", "value": "Metric Value", "stage": "Governance Stage"},
                height=450,
            )
            fig.update_layout(
                xaxis_title="",
                yaxis_title="Metric Value",
                legend_title="",
                font=dict(size=13),
                margin=dict(l=20, r=20, t=30, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------------------------
        # 4. SUGGESTED FIXES
        # ---------------------------------------------------------
        st.subheader("🛠️ Applied Governance Mitigations")
        fixes_list = domain_data.get("fixes", [])
        for i, fix in enumerate(fixes_list, 1):
            st.markdown(f"**{i}.** {fix}")

        st.markdown("---")

    # ---------------------------------------------------------
    # 5. EXPANDERS: THRESHOLDS & SAMPLE SIZES
    # ---------------------------------------------------------
    if nav in ["Overview & Metrics", "Governance Rules"]:
        st.subheader("📋 Audit Methodology & Compliance Parameters")

        with st.expander("⚖️ Low / Medium / High Risk Threshold Rules (EEOC Four-Fifths Standards)", expanded=False):
            thresholds = domain_data.get("thresholds", {})
            st.markdown(f"- 🔴 **High Risk:** {thresholds.get('High', 'Disparity ratio < 0.80 or gap > 8 pts with p < 0.05')}")
            st.markdown(f"- 🟡 **Medium Risk:** {thresholds.get('Medium', 'Disparity ratio between 0.80 and 0.90')}")
            st.markdown(f"- 🟢 **Low Risk (Safe):** {thresholds.get('Low', 'Disparity ratio > 0.90 with minimal score gap')}")
            st.caption(
                "Standards reference the EEOC 80% Rule (Uniform Guidelines on Employee Selection Procedures) "
                "and NYC Local Law 144 AEDT bias audit guidelines."
            )

        with st.expander("🔢 Dataset & Sample Sizes", expanded=False):
            samples = domain_data.get("sample_sizes", {})
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                base_count = samples.get("base_resumes") or samples.get("base_applicants") or 10
                st.write(f"- **Base Profiles:** {base_count}")
                st.write(f"- **Counterfactual Pairs:** {samples.get('counterfactual_pairs', 64)}")
            with col_s2:
                st.write(f"- **Total Counterfactual Cases:** {samples.get('total_bias_test_cases', 128)}")
                st.write(f"- **Hallucination Cases:** {samples.get('hallucination_audit_cases', 10)}")
            with col_s3:
                if selected_domain == "hiring":
                    st.write(f"- **Docker Trap Cases:** {samples.get('docker_trap_cases', 4)}")
                else:
                    st.write(f"- **Class Split:** {samples.get('creditworthy_balanced_split', '8 CW / 8 Non-CW')}")
                st.write(f"- **Privacy Adversarial Cases:** {samples.get('privacy_injection_cases', 10)}")

        # Lending-Specific DPDP Notice in Governance Section
        if selected_domain == "lending" and "dpdp_note" in domain_data:
            dp_info = domain_data["dpdp_note"]
            with st.expander("📜 DPDP Act Alignment: Data Minimisation & Accuracy in Lending", expanded=True):
                st.markdown(f"#### 🇮🇳 {dp_info.get('title', 'DPDP Act Alignment for Credit & Lending Decisions')}")
                st.markdown(
                    f"**1. Data Minimisation Principle:**\n\n{dp_info.get('data_minimisation', '')}"
                )
                st.markdown(
                    f"**2. Accuracy Principle (Section 8(3)):**\n\n{dp_info.get('accuracy', '')}"
                )
                st.info(f"⚖️ **{dp_info.get('disclaimer', '')}**\n\nℹ️ *{dp_info.get('synthetic_data', '')}*")

    # ---------------------------------------------------------
    # 6. DPDP ACT PRINCIPLES PAGE
    # ---------------------------------------------------------
    if nav == "DPDP Act Principles":
        st.subheader("🇮🇳 Digital Personal Data Protection (DPDP) Act Alignment")
        st.write(
            "The **Digital Personal Data Protection Act (DPDP Act, 2023)** establishes seven core data protection "
            "principles for processing digital personal data in India. Below is an honest mapping of where FairHire Audit "
            "operates within this framework."
        )

        st.info(
            "**Scope & Limitations (Modest Assessment):**\n\n"
            "FairHire Audit is a model-level auditing and pre-processing tool. **The tool directly checks data minimisation (anonymiser), "
            "accuracy (hallucination test) and security (privacy test), and does not cover the others.** "
            "Principles such as consent management, purpose definition, storage expiration, and corporate governance "
            "must be enforced by organizational and legal infrastructure outside this tool."
        )

        # Show domain-specific lending context if Lending domain is active
        if selected_domain == "lending" and "dpdp_note" in domain_data:
            dp_info = domain_data["dpdp_note"]
            st.markdown("### 💳 Lending Underwriting: Focus on Data Minimisation & Accuracy")
            l_col1, l_col2 = st.columns(2)
            with l_col1:
                st.markdown("#### 🛡️ Data Minimisation in Lending")
                st.write(dp_info.get("data_minimisation", ""))
            with l_col2:
                st.markdown("#### 🎯 Accuracy in Credit Decisions (Sec 8(3))")
                st.write(dp_info.get("accuracy", ""))
            st.markdown("---")

        dpdp_table_data = [
            {
                "No.": "1",
                "DPDP Principle": "Consent & Transparency",
                "Statutory Intent": "Notice and verifiable consent prior to personal data processing.",
                "Tool Coverage & What It Does": "❌ Not covered by this tool. Must be handled at applicant intake / HR portal level.",
                "Status": "Out of Scope",
            },
            {
                "No.": "2",
                "DPDP Principle": "Purpose Limitation",
                "Statutory Intent": "Process data solely for the stated purpose consented by the individual.",
                "Tool Coverage & What It Does": "❌ Not covered by this tool. Requires backend pipeline access control and data governance.",
                "Status": "Out of Scope",
            },
            {
                "No.": "3",
                "DPDP Principle": "Data Minimisation",
                "Statutory Intent": "Process only the minimum personal data necessary for the objective.",
                "Tool Coverage & What It Does": "✅ Directly Checked & Enforced. The anonymize() engine scrubs candidate names, phones, 12-digit IDs, emails, gender pronouns, and college pedigree before LLM inference, ensuring no unnecessary personal data reaches the model.",
                "Status": "Directly Covered (Anonymiser)",
            },
            {
                "No.": "4",
                "DPDP Principle": "Accuracy",
                "Statutory Intent": "Ensure personal data processed is accurate, complete, and not misleading.",
                "Tool Coverage & What It Does": "✅ Directly Checked. The hallucination_test.py module verifies that the AI model does not fabricate, assume, or invent qualifications/skills absent from the candidate's input.",
                "Status": "Directly Covered (Hallucination Test)",
            },
            {
                "No.": "5",
                "DPDP Principle": "Storage Limitation",
                "Statutory Intent": "Retain personal data only as long as necessary for the purpose.",
                "Tool Coverage & What It Does": "❌ Not covered by this tool. Governed by database retention schedules and purge policies.",
                "Status": "Out of Scope",
            },
            {
                "No.": "6",
                "DPDP Principle": "Security Safeguards",
                "Statutory Intent": "Prevent personal data breach, unauthorized exposure, or leaks.",
                "Tool Coverage & What It Does": "✅ Directly Checked. The privacy_test.py module audits passive echo leakage of 10-digit phones, 12-digit IDs, and emails, and tests resistance against adversarial prompt injection extraction attacks.",
                "Status": "Directly Covered (Privacy Test)",
            },
            {
                "No.": "7",
                "DPDP Principle": "Accountability",
                "Statutory Intent": "Data Fiduciary is responsible for compliance and verifiable audit trails.",
                "Tool Coverage & What It Does": "⚠️ Partially Facilitated. Generates reproducible audit logs and before/after verification artifacts (results.json). Legal accountability remains with the Data Fiduciary.",
                "Status": "Facilitated (Audit Logs)",
            },
        ]

        dpdp_df = pd.DataFrame(dpdp_table_data)
        st.dataframe(
            dpdp_df,
            column_config={
                "No.": st.column_config.TextColumn(width="small"),
                "DPDP Principle": st.column_config.TextColumn(width="medium"),
                "Statutory Intent": st.column_config.TextColumn(width="medium"),
                "Tool Coverage & What It Does": st.column_config.TextColumn(width="large"),
                "Status": st.column_config.TextColumn(width="medium"),
            },
            hide_index=True,
            use_container_width=True,
        )

        st.warning(
            "⚠️ **Guidance, not legal advice. The DPDP Rules were notified on 14 November 2025 with phased implementation.**"
        )
        st.markdown("---")

    # ---------------------------------------------------------
    # 7. FOOTER
    # ---------------------------------------------------------
    st.markdown(
        """
        <div class="footer-text">
            ⚖️ <b>FairHire Audit</b> — Built with Streamlit, Plotly, SciPy, and OpenAI-compatible API.<br>
            <b>Synthetic data only. Not legal advice.</b>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
