"""
views/about.py  –  About page
"""

import streamlit as st


def show():
    st.markdown("""
    <div style="margin-bottom:1.8rem;">
        <h1 style="font-size:2rem; font-weight:800; margin:0 0 0.3rem;
            background:linear-gradient(135deg,#3b82f6,#8b5cf6);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;">ℹ️ About This Project</h1>
        <p style="color:#64748b; font-size:0.92rem; margin:0;">
            A deep dive into the methodology, model architecture, and data behind the Credit Risk Analyser.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Project summary ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="metric-card" style="padding:2rem 2.5rem; margin-bottom:1.5rem;">
        <div style="display:flex; gap:1rem; align-items:flex-start;">
            <span style="font-size:2.5rem; line-height:1;">🏦</span>
            <div>
                <div style="font-size:1.3rem; font-weight:800; color:#f1f5f9; margin-bottom:0.5rem;">
                    Credit Risk Analysis & Loan Default Prediction
                </div>
                <p style="color:#94a3b8; line-height:1.8; font-size:0.92rem; margin:0 0 0.8rem;">
                    This project demonstrates the application of supervised machine learning to a real-world
                    financial problem: predicting whether a loan applicant will default on their loan.
                    The analysis follows a rigorous data science pipeline including data cleaning, feature
                    engineering, model selection, and hyperparameter optimisation.
                </p>
                <p style="color:#94a3b8; line-height:1.8; font-size:0.92rem; margin:0;">
                    The final XGBoost model achieves <strong style="color:#10b981;">92.18% accuracy</strong>
                    and an <strong style="color:#3b82f6;">AUC-ROC of 0.843</strong> on the held-out test set,
                    making it suitable for real-world credit decision support.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Model architecture ────────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="metric-card" style="height:100%;">
            <div style="font-size:1rem; font-weight:700; color:#f1f5f9; margin-bottom:1rem;">
                ⚡ Final Model: XGBoost
            </div>
            <div style="display:flex; flex-direction:column; gap:0.6rem;">
        """, unsafe_allow_html=True)

        params = [
            ("Algorithm", "XGBoost (eXtreme Gradient Boosting)", "#3b82f6"),
            ("Learning Rate", "0.2", "#8b5cf6"),
            ("Max Depth", "5", "#06b6d4"),
            ("N Estimators", "200", "#10b981"),
            ("Eval Metric", "Log Loss", "#f59e0b"),
            ("Random State", "42", "#94a3b8"),
        ]
        for key, val, color in params:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                padding:0.5rem 0.8rem; background:rgba(255,255,255,0.03);
                border-radius:8px; border:1px solid rgba(255,255,255,0.05);">
                <span style="font-size:0.82rem; color:#64748b;">{key}</span>
                <span style="font-size:0.82rem; font-weight:600; color:{color};">{val}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card" style="height:100%;">
            <div style="font-size:1rem; font-weight:700; color:#f1f5f9; margin-bottom:1rem;">
                📈 Test Set Performance
            </div>
        """, unsafe_allow_html=True)

        perf = [
            ("Accuracy", "92.18%", "#10b981"),
            ("Precision", "94.91%", "#3b82f6"),
            ("Recall", "69.69%", "#8b5cf6"),
            ("F1 Score", "80.37%", "#f59e0b"),
            ("AUC-ROC", "0.8429", "#06b6d4"),
            ("Test Set Size", "3,259 records", "#94a3b8"),
        ]
        for metric, value, color in perf:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                padding:0.5rem 0.8rem; background:rgba(255,255,255,0.03);
                border-radius:8px; border:1px solid rgba(255,255,255,0.05); margin-bottom:0.4rem;">
                <span style="font-size:0.82rem; color:#64748b;">{metric}</span>
                <span style="font-size:0.88rem; font-weight:700; color:{color};">{value}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── Preprocessing pipeline ────────────────────────────────────────────────
    st.markdown("<div class='section-header' style='font-size:1.05rem; margin-bottom:1rem;'>🔧 Preprocessing Pipeline</div>", unsafe_allow_html=True)

    steps = [
        ("1", "One-Hot Encoding", "Applied pd.get_dummies() to convert categorical columns Home (4 categories) and Intent (6 categories) into binary indicator variables — preserving all information without ordinal assumptions.", "#3b82f6"),
        ("2", "Binary Encoding", "Converted the Default column from Y/N strings to binary 0/1 integer values for model compatibility.", "#8b5cf6"),
        ("3", "Rate Imputation", "Imputed 3,116 missing Rate values using the mean rate calculated per loan Intent group — context-aware and bias-minimising.", "#06b6d4"),
        ("4", "Emp_length Cleaning", "Replaced implausible outlier values (Emp_length = 123 for borrowers aged 21–22) with age-group averages, then filled remaining 895 NaN values by age-group mean.", "#10b981"),
        ("5", "Log Transformation", "Applied np.log() to right-skewed features Age, Income, Amount, and np.log(Emp_length + 1) to achieve near-normal distributions, improving gradient-based learning.", "#f59e0b"),
        ("6", "Train/Val/Test Split", "80% training, 10% validation, 10% test with random_state=42 ensuring reproducibility. All 32,581 rows used — no data leakage.", "#ef4444"),
    ]

    for num, title, desc, color in steps:
        st.markdown(f"""
        <div class="metric-card" style="display:flex; gap:1.2rem; align-items:flex-start;
            margin-bottom:0.7rem; padding:1.2rem 1.5rem;">
            <div style="
                min-width:36px; height:36px; border-radius:50%;
                background:{color}22; border:2px solid {color};
                display:flex; align-items:center; justify-content:center;
                font-size:0.85rem; font-weight:800; color:{color}; flex-shrink:0;
            ">{num}</div>
            <div>
                <div style="font-size:0.9rem; font-weight:700; color:#e2e8f0;
                    margin-bottom:0.3rem;">{title}</div>
                <div style="font-size:0.82rem; color:#94a3b8; line-height:1.6;">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── Risk categories ───────────────────────────────────────────────────────
    st.markdown("<div class='section-header' style='font-size:1.05rem; margin-bottom:1rem;'>🚦 Risk Category Definitions</div>", unsafe_allow_html=True)

    risk_cols = st.columns(3)
    risks = [
        ("🟢", "Low Risk", "0% – 30%", "#10b981", "rgba(16,185,129,0.1)",
         "Loan Recommended", "Strong applicant profile. Low probability of default. Approval is supported with standard terms."),
        ("🟡", "Medium Risk", "31% – 70%", "#f59e0b", "rgba(245,158,11,0.1)",
         "Further Review Required", "Moderate risk detected. Consider requesting additional documentation, guarantors, or reduced loan amount."),
        ("🔴", "High Risk", "71% – 100%", "#ef4444", "rgba(239,68,68,0.1)",
         "Loan Not Recommended", "High probability of default. Loan should be declined unless exceptional compensating factors are present."),
    ]
    for col, (icon, level, range_, color, bg, action, desc) in zip(risk_cols, risks):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="background:{bg}; border-color:{color}44;
                text-align:center; padding:1.8rem 1.2rem;">
                <div style="font-size:2.2rem; margin-bottom:0.5rem;">{icon}</div>
                <div style="font-size:1.1rem; font-weight:800; color:{color};
                    margin-bottom:0.2rem;">{level}</div>
                <div style="font-size:0.75rem; font-weight:700; letter-spacing:0.1em;
                    color:#64748b; margin-bottom:0.8rem;">{range_}</div>
                <div style="font-size:0.82rem; font-weight:600; color:{color};
                    background:{color}22; padding:0.3rem 0.8rem; border-radius:20px;
                    display:inline-block; margin-bottom:0.8rem;">{action}</div>
                <div style="font-size:0.78rem; color:#94a3b8; line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── Dataset info ──────────────────────────────────────────────────────────
    st.markdown("<div class='section-header' style='font-size:1.05rem; margin-bottom:1rem;'>📦 Dataset Information</div>", unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size:0.88rem; font-weight:700; color:#3b82f6; margin-bottom:0.8rem;">
                📊 Dataset Overview
            </div>
            <ul style="color:#94a3b8; font-size:0.83rem; line-height:1.9; padding-left:1.2rem; margin:0;">
                <li><strong>Source:</strong> credit_risk.csv</li>
                <li><strong>Records:</strong> 32,581 loan applications</li>
                <li><strong>Features:</strong> 12 original → 18 after encoding</li>
                <li><strong>Target:</strong> Status (0 = No Default, 1 = Default)</li>
                <li><strong>Class Balance:</strong> ~77% No Default / 23% Default</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size:0.88rem; font-weight:700; color:#8b5cf6; margin-bottom:0.8rem;">
                🔑 Key Variables
            </div>
            <ul style="color:#94a3b8; font-size:0.83rem; line-height:1.9; padding-left:1.2rem; margin:0;">
                <li><strong>Age:</strong> 20–144 (outlier-cleaned)</li>
                <li><strong>Income:</strong> $4K – $6M annual</li>
                <li><strong>Amount:</strong> $500 – $35,000</li>
                <li><strong>Rate:</strong> 5.42% – 23.22%</li>
                <li><strong>Emp_length:</strong> 0 – 41 years</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with d3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size:0.88rem; font-weight:700; color:#10b981; margin-bottom:0.8rem;">
                🔬 Modelling Details
            </div>
            <ul style="color:#94a3b8; font-size:0.83rem; line-height:1.9; padding-left:1.2rem; margin:0;">
                <li><strong>Framework:</strong> Scikit-Learn + XGBoost</li>
                <li><strong>Tuning:</strong> GridSearchCV (3-fold CV)</li>
                <li><strong>Train set:</strong> 26,064 records</li>
                <li><strong>Val set:</strong> 3,259 records</li>
                <li><strong>Test set:</strong> 3,258 records</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── Limitations ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="metric-card" style="border-color:rgba(245,158,11,0.3);
        background:rgba(245,158,11,0.05);">
        <div style="font-size:0.9rem; font-weight:700; color:#f59e0b; margin-bottom:0.8rem;">
            ⚠️ Limitations & Disclaimer
        </div>
        <p style="color:#94a3b8; font-size:0.84rem; line-height:1.7; margin:0 0 0.5rem;">
            This application is intended for <strong style="color:#e2e8f0;">educational and portfolio demonstration purposes only</strong>.
            Predictions should not be used as the sole basis for real lending decisions. The model has limitations:
        </p>
        <ul style="color:#94a3b8; font-size:0.83rem; line-height:1.8; margin:0; padding-left:1.2rem;">
            <li>Trained on a specific dataset that may not represent all demographics or geographies</li>
            <li>Does not incorporate macroeconomic factors (interest rate environment, unemployment rates)</li>
            <li>Recall of ~70% means ~30% of actual defaults may go undetected</li>
            <li>Real credit decisions require compliance with fair lending laws (ECOA, FCRA, etc.)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
