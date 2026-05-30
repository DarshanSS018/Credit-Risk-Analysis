"""
pages/home.py  –  Home / Overview page
"""

import streamlit as st


def show():
    # ── Hero banner ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid rgba(139,92,246,0.2);
        border-radius: 20px;
        padding: 3rem 3.5rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position:absolute; top:-60px; right:-60px;
            width:300px; height:300px; border-radius:50%;
            background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
        "></div>
        <div style="
            position:absolute; bottom:-80px; left:-40px;
            width:250px; height:250px; border-radius:50%;
            background: radial-gradient(circle, rgba(139,92,246,0.1) 0%, transparent 70%);
        "></div>
        <div style="position:relative; z-index:1;">
            <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1rem;">
                <span style="font-size:2.5rem;">🏦</span>
                <span style="
                    font-size:0.72rem; font-weight:700; letter-spacing:0.14em;
                    text-transform:uppercase; color:#8b5cf6;
                    background:rgba(139,92,246,0.15); padding:0.3rem 0.8rem;
                    border-radius:20px; border:1px solid rgba(139,92,246,0.3);
                ">AI-Powered Platform</span>
            </div>
            <h1 style="
                font-size:2.8rem; font-weight:800; line-height:1.15;
                background: linear-gradient(135deg, #f1f5f9 0%, #94a3b8 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                background-clip: text; margin:0 0 0.8rem;
            ">Credit Risk Analysis &<br>Loan Default Prediction</h1>
            <p style="font-size:1.05rem; color:#94a3b8; max-width:620px; line-height:1.7; margin:0 0 1.5rem;">
                Harnessing the power of Machine Learning to evaluate creditworthiness,
                predict loan defaults, and help financial institutions make smarter,
                data-driven lending decisions.
            </p>
            <div style="display:flex; gap:0.8rem; flex-wrap:wrap;">
                <span style="background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3);
                    color:#60a5fa; padding:0.4rem 1rem; border-radius:20px; font-size:0.82rem; font-weight:600;">
                    ✓ 32,581 Loan Records
                </span>
                <span style="background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.3);
                    color:#34d399; padding:0.4rem 1rem; border-radius:20px; font-size:0.82rem; font-weight:600;">
                    ✓ 92.18% Accuracy
                </span>
                <span style="background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.3);
                    color:#a78bfa; padding:0.4rem 1rem; border-radius:20px; font-size:0.82rem; font-weight:600;">
                    ✓ Real-Time Predictions
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats row ─────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("32,581", "Total Loan Records", "#3b82f6"),
        ("92.18%", "Model Accuracy", "#10b981"),
        ("7", "ML Models Tested", "#8b5cf6"),
        ("9", "Input Features", "#f59e0b"),
    ]
    for col, (val, label, color) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center;">
                <div style="font-size:2rem; font-weight:800; color:{color};">{val}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── Two-column layout: Problem + Objective ────────────────────────────────
    left, right = st.columns([1.05, 1])

    with left:
        st.markdown("""
        <div class="metric-card" style="height:100%;">
            <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:1rem;">
                <span style="font-size:1.4rem;">🎯</span>
                <span style="font-size:1.1rem; font-weight:700; color:#f1f5f9;">Problem Statement</span>
            </div>
            <p style="color:#94a3b8; line-height:1.8; font-size:0.92rem; margin:0 0 1rem;">
                Financial institutions face significant risks from loan defaults. Traditional credit
                scoring methods often fail to capture the full complexity of a borrower's risk profile,
                resulting in either excessive loan rejections (opportunity loss) or poorly assessed
                approvals (credit losses).
            </p>
            <p style="color:#94a3b8; line-height:1.8; font-size:0.92rem; margin:0;">
                The challenge is to build a system that accurately identifies high-risk borrowers
                <em>before</em> loan approval, minimising default rates while supporting genuine applicants.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="metric-card" style="height:100%;">
            <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:1rem;">
                <span style="font-size:1.4rem;">🚀</span>
                <span style="font-size:1.1rem; font-weight:700; color:#f1f5f9;">Business Objective</span>
            </div>
            <ul style="color:#94a3b8; line-height:1.9; font-size:0.92rem; margin:0; padding-left:1.2rem;">
                <li>Build a <strong style="color:#60a5fa;">predictive model</strong> that identifies potential loan defaults</li>
                <li>Understand the <strong style="color:#a78bfa;">key risk variables</strong> affecting credit decisions</li>
                <li>Enable <strong style="color:#34d399;">data-driven lending</strong> for financial institutions</li>
                <li>Provide <strong style="color:#fbbf24;">real-time risk assessment</strong> at the point of application</li>
                <li>Quantify default probability with <strong style="color:#fb923c;">clear risk categories</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── ML Pipeline ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.2rem;">
        <div class="section-header">⚙️ Machine Learning Pipeline</div>
        <div class="section-sub">A structured data science workflow from raw data to deployment</div>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        ("01", "Data Ingestion", "Loaded 32,581 loan records with 12 features covering borrower demographics and loan attributes.", "#3b82f6"),
        ("02", "Data Cleaning", "Handled missing values in Emp_length (895 NaN) and Rate (3,116 NaN) using context-aware imputation strategies.", "#8b5cf6"),
        ("03", "Feature Engineering", "Applied log transformations to skewed features (Age, Income, Amount, Emp_length). One-hot encoded categorical variables.", "#06b6d4"),
        ("04", "Model Selection", "Evaluated 7 classifiers: Logistic Regression, Random Forest, Gradient Boosting, SVM, KNN, Naive Bayes, XGBoost.", "#10b981"),
        ("05", "Hyperparameter Tuning", "GridSearchCV with 3-fold cross-validation identified optimal parameters for each model.", "#f59e0b"),
        ("06", "Final Model", "XGBoost (lr=0.2, depth=5, n=200) achieved 92.18% accuracy, 94.9% precision, 69.7% recall on test set.", "#ef4444"),
    ]

    cols_a = st.columns(3)
    cols_b = st.columns(3)
    all_cols = cols_a + cols_b

    for col, (num, title, desc, color) in zip(all_cols, steps):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:1rem;">
                <div style="font-size:0.65rem; font-weight:800; letter-spacing:0.15em;
                    text-transform:uppercase; color:{color}; margin-bottom:0.5rem;">
                    Step {num}
                </div>
                <div style="font-size:0.95rem; font-weight:700; color:#f1f5f9; margin-bottom:0.5rem;">
                    {title}
                </div>
                <div style="font-size:0.82rem; color:#94a3b8; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ── Technologies ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.2rem;">
        <div class="section-header">🛠️ Technologies Used</div>
        <div class="section-sub">Industry-standard tools powering this platform</div>
    </div>
    """, unsafe_allow_html=True)

    techs = [
        ("🐍", "Python 3.10+", "Core programming language"),
        ("🐼", "Pandas & NumPy", "Data manipulation & numerical computing"),
        ("🤖", "Scikit-Learn", "ML algorithms, preprocessing & evaluation"),
        ("⚡", "XGBoost", "Gradient boosting – final production model"),
        ("📊", "Plotly", "Interactive data visualisations"),
        ("🌊", "Streamlit", "Web application framework"),
    ]

    tech_cols = st.columns(6)
    for col, (icon, name, desc) in zip(tech_cols, techs):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center; padding:1.2rem 0.8rem;">
                <div style="font-size:1.8rem; margin-bottom:0.4rem;">{icon}</div>
                <div style="font-size:0.82rem; font-weight:700; color:#e2e8f0;
                    margin-bottom:0.2rem;">{name}</div>
                <div style="font-size:0.7rem; color:#64748b;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Dataset features ─────────────────────────────────────────────────────
    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom:1.2rem;">
        <div class="section-header">📋 Dataset Features</div>
        <div class="section-sub">Variables used for loan default prediction</div>
    </div>
    """, unsafe_allow_html=True)

    features_data = {
        "Feature": ["Age", "Income", "Home", "Emp_length", "Intent", "Amount", "Rate", "Default", "Cred_length"],
        "Type": ["Numeric", "Numeric", "Categorical", "Numeric", "Categorical", "Numeric", "Numeric", "Binary", "Numeric"],
        "Description": [
            "Age of the loan applicant",
            "Annual income of the applicant",
            "Home ownership status (RENT / OWN / MORTGAGE)",
            "Employment length in years",
            "Loan purpose (EDUCATION / MEDICAL / PERSONAL / etc.)",
            "Loan amount applied for (USD)",
            "Interest rate on the loan (%)",
            "Previous default history (Y/N)",
            "Length of credit history (years)"
        ],
        "Role": ["Input", "Input", "Input", "Input", "Input", "Input", "Input", "Input", "Input"],
    }

    import pandas as pd
    df_features = pd.DataFrame(features_data)
    st.dataframe(
        df_features,
        use_container_width=True,
        hide_index=True,
    )
