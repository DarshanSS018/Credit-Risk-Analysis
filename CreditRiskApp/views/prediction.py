"""
views/prediction.py  –  Loan Risk Prediction page
"""

import streamlit as st
import numpy as np
import pickle
import os
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.pkl')


@st.cache_resource
def load_model():
    """Load the trained model bundle (cached so it is loaded once)."""
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)


def preprocess_input(raw: dict, bundle: dict) -> pd.DataFrame:
    """
    Apply the same preprocessing pipeline used during training.
    Returns a single-row DataFrame aligned to the model's feature columns.
    """
    age        = raw['age']
    income     = raw['income']
    emp_length = raw['emp_length']
    amount     = raw['amount']
    rate       = raw['rate']
    percent_income = amount / income if income > 0 else 0
    default    = 1 if raw['default'] == 'Yes' else 0
    cred_length = raw['cred_length']
    home       = raw['home']     # e.g. 'RENT'
    intent     = raw['intent']   # e.g. 'PERSONAL'

    # Log-transform (mirrors notebook feature engineering)
    log_age        = np.log(age)
    log_income     = np.log(income)
    log_emp_length = np.log(emp_length + 1)
    log_amount     = np.log(amount)

    # Build one-hot encoded row
    home_options   = ['MORTGAGE', 'OTHER', 'OWN', 'RENT']
    intent_options = ['DEBTCONSOLIDATION', 'EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE']

    row = {
        'Age':            log_age,
        'Income':         log_income,
        'Emp_length':     log_emp_length,
        'Amount':         log_amount,
        'Rate':           rate,
        'Percent_income': percent_income,
        'Default':        default,
        'Cred_length':    cred_length,
    }
    for h in home_options:
        row[f'Home_{h}'] = (home == h)
    for i in intent_options:
        row[f'Intent_{i}'] = (intent == i)

    df_row = pd.DataFrame([row])

    # Align columns to what the model was trained on (drop 'Status' already excluded)
    feature_cols = bundle['feature_columns']
    # Drop any extra cols and add any missing ones as False/0
    for c in feature_cols:
        if c not in df_row.columns:
            df_row[c] = 0
    df_row = df_row[feature_cols]
    return df_row


def risk_badge(prob: float):
    """Return (label, color, bg_color, icon, recommendation) based on probability."""
    if prob <= 0.30:
        return ("Low Risk", "#10b981", "rgba(16,185,129,0.15)", "✅",
                "Loan Recommended", "rgba(16,185,129,0.1)", "#10b981")
    elif prob <= 0.70:
        return ("Medium Risk", "#f59e0b", "rgba(245,158,11,0.15)", "⚠️",
                "Further Review Required", "rgba(245,158,11,0.1)", "#f59e0b")
    else:
        return ("High Risk", "#ef4444", "rgba(239,68,68,0.15)", "🚨",
                "Loan Not Recommended", "rgba(239,68,68,0.1)", "#ef4444")


def show():
    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.8rem;">
        <h1 style="font-size:2rem; font-weight:800; margin:0 0 0.3rem;
            background:linear-gradient(135deg,#3b82f6,#8b5cf6);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;">🔮 Loan Risk Prediction</h1>
        <p style="color:#64748b; font-size:0.92rem; margin:0;">
            Enter applicant details below to get an instant AI-powered default risk assessment.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Model check ───────────────────────────────────────────────────────────
    bundle = load_model()
    if bundle is None:
        st.error("⚠️ **Model not found.** Please run `python train_model.py` inside the CreditRiskApp directory first.")
        st.code("cd CreditRiskApp\npython train_model.py", language="bash")
        return

    # ── Input form ────────────────────────────────────────────────────────────
    with st.form("prediction_form"):
        st.markdown("<div class='section-header' style='font-size:1.1rem;'>📝 Applicant Information</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            age = st.number_input("Age (years)", min_value=18, max_value=100, value=30, step=1,
                                  help="Applicant's age in years")
        with r1c2:
            income = st.number_input("Annual Income ($)", min_value=1000, max_value=10_000_000,
                                     value=55_000, step=500,
                                     help="Gross annual income in USD")
        with r1c3:
            home = st.selectbox("Home Ownership",
                                ["RENT", "OWN", "MORTGAGE", "OTHER"],
                                help="Current home ownership status")

        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            emp_length = st.number_input("Employment Length (years)", min_value=0.0, max_value=50.0,
                                         value=3.0, step=0.5,
                                         help="Years of current employment")
        with r2c2:
            intent = st.selectbox("Loan Intent",
                                  ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE",
                                   "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"],
                                  help="Purpose of the loan")
        with r2c3:
            amount = st.number_input("Loan Amount ($)", min_value=100, max_value=500_000,
                                     value=10_000, step=100,
                                     help="Requested loan amount in USD")

        r3c1, r3c2, r3c3 = st.columns(3)
        with r3c1:
            rate = st.number_input("Interest Rate (%)", min_value=1.0, max_value=40.0,
                                   value=12.5, step=0.1, format="%.1f",
                                   help="Annual interest rate offered")
        with r3c2:
            default = st.selectbox("Past Default History",
                                   ["No", "Yes"],
                                   help="Has the applicant defaulted on a loan before?")
        with r3c3:
            cred_length = st.number_input("Credit History Length (years)", min_value=0, max_value=50,
                                          value=5, step=1,
                                          help="Length of applicant's credit history")

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔮 Predict Default Risk", use_container_width=True)

    # ── Derived stats preview ─────────────────────────────────────────────────
    percent_income = (amount / income * 100) if income > 0 else 0
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Loan-to-Income Ratio", f"{percent_income:.1f}%",
                  delta="High" if percent_income > 40 else "Moderate" if percent_income > 20 else "Low",
                  delta_color="inverse" if percent_income > 40 else "off")
    with col_b:
        monthly_payment = (amount * (rate / 100 / 12)) / (1 - (1 + rate / 100 / 12) ** -60) if rate > 0 else amount / 60
        st.metric("Est. Monthly Payment", f"${monthly_payment:,.0f}",
                  help="Estimated 5-year loan monthly payment")
    with col_c:
        dti = (monthly_payment / (income / 12) * 100) if income > 0 else 0
        st.metric("Debt-to-Income Ratio", f"{dti:.1f}%",
                  delta="Elevated" if dti > 43 else "Normal",
                  delta_color="inverse" if dti > 43 else "off")

    # ── Prediction result ─────────────────────────────────────────────────────
    if submitted:
        raw_input = {
            'age': age, 'income': income, 'home': home,
            'emp_length': emp_length, 'intent': intent, 'amount': amount,
            'rate': rate, 'default': default, 'cred_length': cred_length,
        }

        with st.spinner("Analysing credit risk..."):
            X_input = preprocess_input(raw_input, bundle)
            model = bundle['model']
            prob = float(model.predict_proba(X_input)[0][1])
            pred = int(model.predict(X_input)[0])

        label, color, bg, icon, recommendation, rec_bg, rec_color = risk_badge(prob)
        prob_pct = prob * 100
        loan_status = "Default" if pred == 1 else "No Default"

        st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-header' style='font-size:1.2rem; margin-bottom:1rem;'>📋 Risk Assessment Results</div>", unsafe_allow_html=True)

        # Main result cards
        rc1, rc2, rc3 = st.columns(3)

        with rc1:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center; padding:2rem 1.5rem;">
                <div style="font-size:0.7rem; font-weight:700; letter-spacing:0.12em;
                    text-transform:uppercase; color:#64748b; margin-bottom:0.8rem;">
                    Default Probability
                </div>
                <div style="font-size:3.5rem; font-weight:900; color:{color};
                    line-height:1; margin-bottom:0.5rem;">
                    {prob_pct:.1f}%
                </div>
                <div style="
                    background:#1e293b; border-radius:100px; height:8px;
                    overflow:hidden; margin:0.8rem auto; max-width:140px;
                ">
                    <div style="
                        width:{min(prob_pct, 100):.0f}%; height:100%;
                        background:{color}; border-radius:100px;
                        transition: width 0.6s ease;
                    "></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with rc2:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center; padding:2rem 1.5rem;
                border-color:{color}; background:{bg};">
                <div style="font-size:0.7rem; font-weight:700; letter-spacing:0.12em;
                    text-transform:uppercase; color:#64748b; margin-bottom:0.8rem;">
                    Risk Level
                </div>
                <div style="font-size:2.2rem; margin-bottom:0.4rem;">{icon}</div>
                <div style="font-size:1.6rem; font-weight:800; color:{color};">{label}</div>
                <div style="font-size:0.8rem; color:#64748b; margin-top:0.4rem;">
                    Confidence: {max(prob, 1-prob)*100:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        with rc3:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center; padding:2rem 1.5rem;
                background:{rec_bg}; border-color:{rec_color};">
                <div style="font-size:0.7rem; font-weight:700; letter-spacing:0.12em;
                    text-transform:uppercase; color:#64748b; margin-bottom:0.8rem;">
                    Recommendation
                </div>
                <div style="font-size:1.15rem; font-weight:800; color:{rec_color};
                    line-height:1.3;">{recommendation}</div>
                <div style="margin-top:0.8rem; font-size:0.82rem; color:#94a3b8;">
                    Predicted Status: <strong style="color:#e2e8f0;">{loan_status}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Risk breakdown ────────────────────────────────────────────────────
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        # Risk scale visual
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size:0.82rem; font-weight:600; color:#94a3b8;
                margin-bottom:1rem; letter-spacing:0.05em;">
                RISK SCALE
            </div>
            <div style="position:relative; margin-bottom:0.5rem;">
                <!-- Background track -->
                <div style="background:linear-gradient(90deg,#10b981,#f59e0b,#ef4444);
                    height:12px; border-radius:6px; position:relative; overflow:visible;">
                    <!-- Marker -->
                    <div style="
                        position:absolute; left:{min(prob_pct,98):.0f}%;
                        top:50%; transform:translate(-50%,-50%);
                        width:20px; height:20px; border-radius:50%;
                        background:white; border:3px solid {color};
                        box-shadow:0 0 10px {color};
                    "></div>
                </div>
                <div style="display:flex; justify-content:space-between;
                    font-size:0.72rem; color:#64748b; margin-top:0.5rem;">
                    <span>0% – Low Risk</span>
                    <span>30%</span>
                    <span>70%</span>
                    <span>High Risk – 100%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Key risk factors ──────────────────────────────────────────────────
        st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.8rem;'>🔍 Key Risk Factors</div>", unsafe_allow_html=True)

        factors = []
        if percent_income > 40:
            factors.append(("🔴", "Loan-to-Income Ratio", f"{percent_income:.1f}% – Very high relative to income", "high"))
        elif percent_income > 20:
            factors.append(("🟡", "Loan-to-Income Ratio", f"{percent_income:.1f}% – Moderate", "medium"))
        else:
            factors.append(("🟢", "Loan-to-Income Ratio", f"{percent_income:.1f}% – Healthy", "low"))

        if default == "Yes":
            factors.append(("🔴", "Past Default History", "Previous default recorded – significant risk flag", "high"))
        else:
            factors.append(("🟢", "Past Default History", "No previous defaults – positive indicator", "low"))

        if rate > 20:
            factors.append(("🔴", "Interest Rate", f"{rate:.1f}% – Very high rate increases repayment burden", "high"))
        elif rate > 13:
            factors.append(("🟡", "Interest Rate", f"{rate:.1f}% – Above average", "medium"))
        else:
            factors.append(("🟢", "Interest Rate", f"{rate:.1f}% – Competitive rate", "low"))

        if emp_length < 1:
            factors.append(("🔴", "Employment Length", f"{emp_length:.1f} yrs – Very limited employment history", "high"))
        elif emp_length < 3:
            factors.append(("🟡", "Employment Length", f"{emp_length:.1f} yrs – Short employment history", "medium"))
        else:
            factors.append(("🟢", "Employment Length", f"{emp_length:.1f} yrs – Stable employment", "low"))

        if cred_length < 2:
            factors.append(("🔴", "Credit History", f"{cred_length} yrs – Very thin credit file", "high"))
        elif cred_length < 5:
            factors.append(("🟡", "Credit History", f"{cred_length} yrs – Limited history", "medium"))
        else:
            factors.append(("🟢", "Credit History", f"{cred_length} yrs – Established credit profile", "low"))

        factor_cols = st.columns(len(factors))
        severity_colors = {"high": "#ef4444", "medium": "#f59e0b", "low": "#10b981"}
        severity_bg = {"high": "rgba(239,68,68,0.08)", "medium": "rgba(245,158,11,0.08)", "low": "rgba(16,185,129,0.08)"}

        for col, (dot, name, desc, severity) in zip(factor_cols, factors):
            with col:
                c = severity_colors[severity]
                bg_c = severity_bg[severity]
                st.markdown(f"""
                <div class="metric-card" style="background:{bg_c}; border-color:{c}33; padding:1rem;">
                    <div style="font-size:1.4rem; margin-bottom:0.4rem;">{dot}</div>
                    <div style="font-size:0.78rem; font-weight:700; color:{c};
                        margin-bottom:0.3rem;">{name}</div>
                    <div style="font-size:0.72rem; color:#94a3b8; line-height:1.4;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
