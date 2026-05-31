"""
app.py  –  Credit Risk Analysis & Loan Default Prediction
Main Streamlit entry point with sidebar navigation.
"""

import streamlit as st

# ─── Page config (MUST be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="Credit Risk Analyzer | Loan Default Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root variables ── */
:root {
    --bg-primary:    #0a0e1a;
    --bg-secondary:  #111827;
    --bg-card:       #1a2236;
    --bg-card-hover: #1e2d45;
    --accent-blue:   #3b82f6;
    --accent-purple: #8b5cf6;
    --accent-teal:   #06b6d4;
    --accent-green:  #10b981;
    --accent-red:    #ef4444;
    --accent-amber:  #f59e0b;
    --text-primary:  #f1f5f9;
    --text-secondary:#94a3b8;
    --border:        rgba(255,255,255,0.07);
    --gradient-main: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
}

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Main area ── */
.main .block-container {
    padding: 1.5rem 2.5rem 3rem !important;
    max-width: 1400px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.2rem !important;
}

/* ── Sidebar navigation items ── */
[data-testid="stSidebar"] .stRadio > label {
    color: var(--text-secondary) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    display: flex !important;
    align-items: center !important;
    padding: 0.65rem 1rem !important;
    border-radius: 10px !important;
    margin-bottom: 4px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    border: 1px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background: rgba(59,130,246,0.15) !important;
    color: var(--text-primary) !important;
    border-color: rgba(59,130,246,0.3) !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked),
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[aria-checked="true"] {
    background: rgba(59,130,246,0.2) !important;
    color: var(--accent-blue) !important;
    border-color: rgba(59,130,246,0.5) !important;
}

/* ── Cards ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--gradient-main);
}

/* ── Stat numbers ── */
.stat-number {
    font-size: 2.2rem;
    font-weight: 800;
    background: var(--gradient-main);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.stat-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}

/* ── Section headers ── */
.section-header {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.3rem;
}
.section-sub {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
}

/* ── Divider ── */
.gradient-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(59,130,246,0.5), transparent);
    margin: 2rem 0;
    border: none;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--gradient-main) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(59,130,246,0.4) !important;
}

/* ── Form inputs ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stSlider {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
}

/* ── Streamlit metrics ── */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}

/* ── Plot backgrounds ── */
.js-plotly-plot .plotly .bg { fill: transparent !important; }

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / branding
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1.5rem;">
        <div style="font-size:2.8rem; margin-bottom:0.3rem;">🏦</div>
        <div style="font-size:1.1rem; font-weight:800; background:linear-gradient(135deg,#3b82f6,#8b5cf6);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; letter-spacing:0.02em;">Credit Risk</div>
        <div style="font-size:0.72rem; color:#64748b; font-weight:500;
                    letter-spacing:0.12em; text-transform:uppercase; margin-top:2px;">
            AI-Powered Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size:0.68rem;color:#64748b;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.5rem;'>Navigation</div>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠  Home", "🔮  Prediction", "📊  Dashboard", "ℹ️  About"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem; color:#475569; text-align:center; line-height:1.6;">
        <div style="margin-bottom:0.3rem;">Powered by <strong style="color:#64748b;">XGBoost</strong></div>
        <div>Accuracy <strong style="color:#10b981;">92.18%</strong></div>
        <div style="margin-top:0.5rem; font-size:0.65rem; color:#334155;">
            Dataset: 32,581 loan records
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Route to pages ───────────────────────────────────────────────────────────
if "Home" in page:
    from views.home import show
    show()
elif "Prediction" in page:
    from views.prediction import show
    show()
elif "Dashboard" in page:
    from views.dashboard import show
    show()
elif "About" in page:
    from views.about import show
    show()
