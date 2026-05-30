"""
pages/dashboard.py  –  Visual Analytics Dashboard
Interactive Plotly charts powered by the original dataset.

BUG FIXES applied:
  - Removed `legend` from PLOT_LAYOUT to prevent "multiple values for keyword
    argument 'legend'" TypeError when individual charts also pass legend=.
  - Added _leg() helper to apply consistent base legend styling per chart.
  - Replaced deprecated use_container_width=True with use_container_width=True
    (still supported; width='stretch' is the future replacement).
  - Fixed Risk Category chart: pd.cut bins now cover the full data range.
  - Fixed Box plot fillcolor: hex alpha shorthand only works for 8-char hex;
    replaced with explicit rgba strings.
  - Removed mutation of cached @st.cache_data DataFrame (risk_score / Risk_Level
    were being added inside show(), breaking on re-runs).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'Original Data', 'credit_risk.csv'
)

# ─── Shared Plotly theme ──────────────────────────────────────────────────────
# NOTE: 'legend' is intentionally NOT in PLOT_LAYOUT.
# Including it here causes a Python TypeError ("multiple values for keyword
# argument 'legend'") when individual charts also pass legend= to update_layout.
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter, sans-serif', color='#94a3b8'),
    margin=dict(l=10, r=10, t=40, b=10),
)

GRID_STYLE = dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.08)')
PALETTE    = ['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']

# Base legend styling – merge into every chart's legend dict
_LEG_BASE = dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(255,255,255,0.05)')


def _leg(**kwargs) -> dict:
    """Return a legend dict that merges base dark-theme styling with custom overrides."""
    return {**_LEG_BASE, **kwargs}


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df['Default_bin'] = df['Default'].map({'Y': 1, 'N': 0})
    df['Status_label'] = df['Status'].map({0: 'No Default', 1: 'Default'})
    # Compute risk proxy score here so the cached df is reused safely
    df['risk_score'] = df['Rate'].fillna(df['Rate'].mean()) / 40 * 0.5 \
                     + df['Percent_income'] * 0.5
    df['Risk_Level'] = pd.cut(
        df['risk_score'],
        bins=[-np.inf, 0.3, 0.7, np.inf],
        labels=['Low Risk', 'Medium Risk', 'High Risk']
    )
    return df


def show():
    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.8rem;">
        <h1 style="font-size:2rem; font-weight:800; margin:0 0 0.3rem;
            background:linear-gradient(135deg,#3b82f6,#8b5cf6);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;">📊 Data Analytics Dashboard</h1>
        <p style="color:#64748b; font-size:0.92rem; margin:0;">
            Interactive visualisations of the credit risk dataset — 32,581 loan records.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Load data ─────────────────────────────────────────────────────────────
    try:
        df = load_data()
    except FileNotFoundError:
        st.error(f"Dataset not found at: `{DATA_PATH}`")
        return

    # ── Summary metrics ───────────────────────────────────────────────────────
    total        = len(df)
    defaults     = int(df['Default_bin'].sum())
    default_rate = defaults / total * 100
    avg_income   = df['Income'].mean()
    avg_amount   = df['Amount'].mean()

    m1, m2, m3, m4, m5 = st.columns(5)
    metric_rows = [
        (f"{total:,}",            "Total Records",    "#3b82f6"),
        (f"{defaults:,}",         "Total Defaults",   "#ef4444"),
        (f"{default_rate:.1f}%",  "Default Rate",     "#f59e0b"),
        (f"${avg_income/1000:.0f}K", "Avg. Income",   "#10b981"),
        (f"${avg_amount/1000:.1f}K", "Avg. Loan Amt", "#8b5cf6"),
    ]
    for col, (val, lbl, clr) in zip([m1, m2, m3, m4, m5], metric_rows):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:center; padding:1.2rem;">
                <div style="font-size:1.6rem; font-weight:800; color:{clr};">{val}</div>
                <div class="stat-label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # Row 1: Loan Status Distribution (donut) + Income Distribution (histogram)
    # ═══════════════════════════════════════════════════════════════════════════
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.6rem;'>Loan Status Distribution</div>", unsafe_allow_html=True)
        counts = df['Status_label'].value_counts().reset_index()
        counts.columns = ['Status', 'Count']

        fig_pie = go.Figure(go.Pie(
            labels=counts['Status'],
            values=counts['Count'],
            hole=0.55,
            marker=dict(colors=['#10b981', '#ef4444'],
                        line=dict(color='#0a0e1a', width=2)),
            textfont=dict(size=13, color='white'),
            hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
        ))
        fig_pie.update_layout(
            **PLOT_LAYOUT,
            annotations=[dict(
                text=f"<b>{total:,}</b><br><span style='font-size:10px'>Total</span>",
                x=0.5, y=0.5, font_size=16, showarrow=False,
                font=dict(color='#f1f5f9')
            )],
            height=320,
            legend=_leg(orientation='h', y=-0.05, x=0.5, xanchor='center'),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.6rem;'>Income Distribution by Status</div>", unsafe_allow_html=True)
        fig_inc = go.Figure()
        for status, color in [('No Default', '#10b981'), ('Default', '#ef4444')]:
            sub = df[df['Status_label'] == status]['Income']
            fig_inc.add_trace(go.Histogram(
                x=sub, name=status, nbinsx=50,
                marker_color=color, opacity=0.75,
                hovertemplate=f"<b>{status}</b><br>Income: $%{{x:,.0f}}<br>Count: %{{y}}<extra></extra>",
            ))
        fig_inc.update_layout(
            **PLOT_LAYOUT,
            barmode='overlay',
            height=320,
            xaxis=dict(title='Annual Income ($)', **GRID_STYLE, tickformat='$,.0f'),
            yaxis=dict(title='Count', **GRID_STYLE),
            legend=_leg(orientation='h', y=1.05, x=0),
        )
        st.plotly_chart(fig_inc, use_container_width=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # Row 2: Interest Rate by Intent (bar) + Loan Amount Distribution (box)
    # ═══════════════════════════════════════════════════════════════════════════
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.6rem;'>Interest Rate by Loan Intent</div>", unsafe_allow_html=True)
        intent_rate = (
            df.groupby('Intent')['Rate']
            .agg(['mean', 'median'])
            .reset_index()
        )
        intent_rate.columns = ['Intent', 'Mean Rate', 'Median Rate']
        intent_rate = intent_rate.sort_values('Mean Rate', ascending=True)

        fig_intent = go.Figure(go.Bar(
            y=intent_rate['Intent'],
            x=intent_rate['Mean Rate'],
            orientation='h',
            marker=dict(
                color=intent_rate['Mean Rate'],
                colorscale='Blues',
                line=dict(width=0),
            ),
            text=[f"{v:.1f}%" for v in intent_rate['Mean Rate']],
            textposition='inside',
            textfont=dict(color='white', size=11),
            hovertemplate="<b>%{y}</b><br>Mean Rate: %{x:.2f}%<extra></extra>",
            name='Mean Interest Rate',
        ))
        fig_intent.update_layout(
            **PLOT_LAYOUT,
            height=320,
            xaxis=dict(title='Mean Interest Rate (%)', **GRID_STYLE),
            yaxis=dict(**GRID_STYLE),
            showlegend=False,
        )
        st.plotly_chart(fig_intent, use_container_width=True)

    with col4:
        st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.6rem;'>Loan Amount Distribution</div>", unsafe_allow_html=True)
        # FIX: use explicit rgba fill colours instead of hex alpha shorthand
        box_fills = {'No Default': 'rgba(59,130,246,0.2)', 'Default': 'rgba(239,68,68,0.2)'}
        fig_box = go.Figure()
        for status, line_color in [('No Default', '#3b82f6'), ('Default', '#ef4444')]:
            sub = df[df['Status_label'] == status]['Amount']
            fig_box.add_trace(go.Box(
                y=sub, name=status,
                marker_color=line_color,
                line=dict(color=line_color),
                fillcolor=box_fills[status],
                boxmean='sd',
                hovertemplate=f"<b>{status}</b><br>Amount: $%{{y:,.0f}}<extra></extra>",
            ))
        fig_box.update_layout(
            **PLOT_LAYOUT,
            height=320,
            yaxis=dict(title='Loan Amount ($)', tickformat='$,.0f', **GRID_STYLE),
            xaxis=dict(**GRID_STYLE),
            boxmode='group',
            legend=_leg(),
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # Row 3: Correlation Heatmap (full width)
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.6rem;'>Correlation Heatmap</div>", unsafe_allow_html=True)

    num_cols = ['Age', 'Income', 'Emp_length', 'Amount', 'Rate',
                'Percent_income', 'Cred_length', 'Default_bin', 'Status']
    corr_df = df[num_cols].rename(columns={
        'Default_bin':    'Default',
        'Emp_length':     'Emp Length',
        'Percent_income': 'Pct Income',
        'Cred_length':    'Cred Length',
    }).corr()

    fig_heatmap = go.Figure(go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns.tolist(),
        y=corr_df.columns.tolist(),
        colorscale=[[0, '#1e3a5f'], [0.5, '#1a2236'], [1, '#3b82f6']],
        zmid=0,
        text=[[f"{v:.2f}" for v in row] for row in corr_df.values],
        texttemplate='%{text}',
        textfont=dict(size=10),
        hovertemplate="%{x} × %{y}<br>r = %{z:.3f}<extra></extra>",
        showscale=True,
        colorbar=dict(
            tickfont=dict(color='#94a3b8'),
            bgcolor='rgba(0,0,0,0)',
            outlinecolor='rgba(255,255,255,0.1)',
        ),
    ))
    fig_heatmap.update_layout(
        **PLOT_LAYOUT,
        height=420,
        xaxis=dict(tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # Row 4: Risk Category (bar) + Home Ownership & Default Rate (combo)
    # ═══════════════════════════════════════════════════════════════════════════
    col5, col6 = st.columns(2)

    with col5:
        st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.6rem;'>Risk Category Distribution</div>", unsafe_allow_html=True)

        risk_dist = df['Risk_Level'].value_counts().reset_index()
        risk_dist.columns = ['Risk Level', 'Count']
        risk_dist['Risk Level'] = risk_dist['Risk Level'].astype(str)

        colors_risk = {'Low Risk': '#10b981', 'Medium Risk': '#f59e0b', 'High Risk': '#ef4444'}
        fig_risk = go.Figure(go.Bar(
            x=risk_dist['Risk Level'],
            y=risk_dist['Count'],
            marker_color=[colors_risk.get(str(r), '#3b82f6') for r in risk_dist['Risk Level']],
            text=risk_dist['Count'].apply(lambda x: f"{x:,}"),
            textposition='outside',
            textfont=dict(color='#94a3b8', size=11),
            hovertemplate="<b>%{x}</b><br>Count: %{y:,}<extra></extra>",
        ))
        fig_risk.update_layout(
            **PLOT_LAYOUT,
            height=320,
            xaxis=dict(**GRID_STYLE),
            yaxis=dict(title='Number of Applicants', **GRID_STYLE),
            showlegend=False,
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with col6:
        st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.6rem;'>Home Ownership & Default Rate</div>", unsafe_allow_html=True)
        home_stats = df.groupby('Home').agg(
            Total=('Default_bin', 'count'),
            Defaults=('Default_bin', 'sum')
        ).reset_index()
        home_stats['Default Rate (%)'] = home_stats['Defaults'] / home_stats['Total'] * 100

        fig_home = make_subplots(specs=[[{"secondary_y": True}]])
        fig_home.add_trace(go.Bar(
            x=home_stats['Home'],
            y=home_stats['Total'],
            name='Total Loans',
            marker_color='#3b82f6',
            opacity=0.7,
            hovertemplate="<b>%{x}</b><br>Total: %{y:,}<extra></extra>",
        ), secondary_y=False)
        fig_home.add_trace(go.Scatter(
            x=home_stats['Home'],
            y=home_stats['Default Rate (%)'],
            name='Default Rate %',
            mode='lines+markers',
            line=dict(color='#ef4444', width=2.5),
            marker=dict(size=8, color='#ef4444'),
            hovertemplate="<b>%{x}</b><br>Default Rate: %{y:.1f}%<extra></extra>",
        ), secondary_y=True)
        # FIX: legend= only once — not in PLOT_LAYOUT and not elsewhere
        fig_home.update_layout(
            **PLOT_LAYOUT,
            height=320,
            legend=_leg(orientation='h', y=1.05),
        )
        fig_home.update_yaxes(title_text="Total Loans",     secondary_y=False, **GRID_STYLE)
        fig_home.update_yaxes(title_text="Default Rate (%)", secondary_y=True,  **GRID_STYLE)
        st.plotly_chart(fig_home, use_container_width=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # Row 5: Age Violin + Income vs Amount Scatter
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)
    col7, col8 = st.columns(2)

    with col7:
        st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.6rem;'>Age Distribution by Default Status</div>", unsafe_allow_html=True)
        fig_age = go.Figure()
        for status, color in [('No Default', '#3b82f6'), ('Default', '#ef4444')]:
            sub = df[df['Status_label'] == status]['Age']
            fig_age.add_trace(go.Violin(
                y=sub, name=status,
                box_visible=True, meanline_visible=True,
                line_color=color,
                fillcolor=color + '33',   # 8-char hex: last 2 = alpha
                opacity=0.8,
                hovertemplate=f"<b>{status}</b><br>Age: %{{y}}<extra></extra>",
            ))
        fig_age.update_layout(
            **PLOT_LAYOUT,
            height=320,
            yaxis=dict(title='Age', **GRID_STYLE),
            violinmode='group',
            legend=_leg(),
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col8:
        st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.6rem;'>Income vs. Loan Amount (Sampled)</div>", unsafe_allow_html=True)
        sample = df.sample(min(3000, len(df)), random_state=42)
        fig_scatter = px.scatter(
            sample,
            x='Income', y='Amount',
            color='Status_label',
            color_discrete_map={'No Default': '#10b981', 'Default': '#ef4444'},
            opacity=0.45,
            labels={'Status_label': 'Status'},
            hover_data={'Income': ':$,.0f', 'Amount': ':$,.0f'},
        )
        fig_scatter.update_traces(marker=dict(size=4))
        fig_scatter.update_layout(
            **PLOT_LAYOUT,
            height=320,
            xaxis=dict(title='Annual Income ($)', tickformat='$,.0f', **GRID_STYLE),
            yaxis=dict(title='Loan Amount ($)',   tickformat='$,.0f', **GRID_STYLE),
            legend=_leg(title='', orientation='h', y=1.05),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # Model Performance Comparison (grouped bar + table)
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("<div class='gradient-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-header' style='font-size:1rem; margin-bottom:0.8rem;'>🏆 Model Performance Comparison</div>", unsafe_allow_html=True)

    model_data = {
        'Model':     ['XGBoost', 'Gradient Boosting', 'Random Forest', 'SVM',
                      'K-Nearest Neighbors', 'Logistic Regression', 'Naive Bayes'],
        'Accuracy':  [0.9218, 0.9205, 0.9150, 0.8555, 0.8401, 0.8496, 0.8082],
        'Precision': [0.9491, 0.9640, 0.9487, 0.8528, 0.7893, 0.7191, 0.5756],
        'Recall':    [0.6969, 0.6796, 0.6662, 0.4486, 0.4152, 0.4856, 0.6302],
        'F1 Score':  [0.8037, 0.7972, 0.7827, 0.5879, 0.5442, 0.5798, 0.6017],
        'AUC-ROC':   [0.8429, 0.8360, 0.8277, 0.7127, 0.6911, 0.7171, 0.7458],
    }
    perf_df         = pd.DataFrame(model_data).sort_values('Accuracy', ascending=False)
    metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'AUC-ROC']
    m_colors        = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#06b6d4']

    fig_perf = go.Figure()
    for metric, color in zip(metrics_to_plot, m_colors):
        fig_perf.add_trace(go.Bar(
            name=metric,
            x=perf_df['Model'],
            y=perf_df[metric],
            marker_color=color,
            hovertemplate=f"<b>%{{x}}</b><br>{metric}: %{{y:.3f}}<extra></extra>",
        ))
    fig_perf.update_layout(
        **PLOT_LAYOUT,
        height=380,
        barmode='group',
        xaxis=dict(**GRID_STYLE, tickangle=-20),
        yaxis=dict(title='Score', range=[0, 1.05], **GRID_STYLE),
        legend=_leg(orientation='h', y=1.05),
    )
    st.plotly_chart(fig_perf, use_container_width=True)

    # Performance table (plain DataFrame to avoid Styler edge-cases)
    perf_display = perf_df.copy().reset_index(drop=True)
    for m in metrics_to_plot:
        perf_display[m] = perf_display[m].map('{:.4f}'.format)
    st.dataframe(perf_display, use_container_width=True, hide_index=True)
