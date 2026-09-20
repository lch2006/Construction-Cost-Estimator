import html
import json
import re
from datetime import date

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# BUILDCOST PRO
# Construction Cost Intelligence + Decision Support
# ============================================================

st.set_page_config(
    page_title="BuildCost | Construction Cost Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PAGES = [
    ("Dashboard", "⌂"),
    ("Estimate", "▦"),
    ("Risk Lab", "◒"),
    ("Scenario Studio", "⇄"),
    ("Optimize", "◎"),
    ("Analytics", "◫"),
    ("Report", "▤"),
]

PROJECT_TYPES = [
    "Land Development",
    "Commercial",
    "Residential",
    "Infrastructure",
    "Transportation",
    "Utilities",
    "Other",
]

BASE_COLUMNS = ["Category", "Item", "Quantity", "Unit", "Unit Cost ($)"]


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
<style>
:root{
    --ink:#0B1220;
    --navy:#0F172A;
    --navy-2:#182235;
    --slate:#64748B;
    --muted:#94A3B8;
    --line:#E2E8F0;
    --panel:#FFFFFF;
    --bg:#F6F8FB;
    --orange:#F97316;
    --orange-dark:#EA580C;
    --orange-soft:#FFF7ED;
    --green:#15803D;
    --red:#B91C1C;
}

.stApp{background:var(--bg)}
.block-container{max-width:1480px;padding-top:1.15rem;padding-bottom:4rem}
[data-testid="stHeader"]{background:rgba(246,248,251,.94)}

/* Sidebar */
[data-testid="stSidebar"]{background:var(--navy);border-right:1px solid #253147}
[data-testid="stSidebar"] hr{border-color:#334155}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:#CBD5E1}
[data-testid="stSidebar"] .stButton>button{
    width:100%;min-height:46px;justify-content:flex-start;padding-left:14px;
    border-radius:12px;font-weight:720;background:#1E293B!important;
    border:1px solid #334155!important;color:#fff!important;transition:.18s ease;
}
[data-testid="stSidebar"] .stButton>button *{color:#fff!important}
[data-testid="stSidebar"] .stButton>button:hover{background:#334155!important;border-color:var(--orange)!important}
[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:var(--orange)!important;border-color:var(--orange)!important}
[data-testid="stSidebar"] .stButton>button[kind="primary"]:hover{background:var(--orange-dark)!important;border-color:var(--orange-dark)!important}

/* Hero */
.hero{
    padding:66px 58px;border-radius:28px;color:#fff;margin-bottom:24px;
    background:
      radial-gradient(circle at 86% 5%,rgba(249,115,22,.34),transparent 28%),
      radial-gradient(circle at 70% 110%,rgba(37,99,235,.18),transparent 35%),
      linear-gradient(135deg,#0B1220 0%,#101B30 58%,#1B2940 100%);
    box-shadow:0 24px 60px rgba(15,23,42,.16);
}
.hero-badge{display:inline-block;padding:7px 13px;border-radius:999px;background:rgba(249,115,22,.14);border:1px solid rgba(249,115,22,.45);color:#FDBA74;font-size:.76rem;font-weight:850;letter-spacing:.09em;margin-bottom:18px}
.hero h1{margin:0;font-size:clamp(2.65rem,5.4vw,4.9rem);line-height:.99;letter-spacing:-.055em}
.hero p{max-width:860px;margin:22px 0 0;color:#CBD5E1;font-size:1.08rem;line-height:1.7}

/* Page headers */
.page-header{padding:30px 34px;border-radius:22px;background:linear-gradient(135deg,#0F172A,#1E293B);color:#fff;margin-bottom:24px}
.page-header .eyebrow{color:#FDBA74;font-size:.76rem;font-weight:850;letter-spacing:.09em;margin-bottom:8px}
.page-header h1{margin:0;font-size:2.25rem;letter-spacing:-.04em}
.page-header p{margin:8px 0 0;color:#CBD5E1;max-width:930px;line-height:1.6}

/* Sections and panels */
.section-title{margin-top:28px;margin-bottom:5px;color:var(--ink);font-size:1.78rem;font-weight:850;letter-spacing:-.035em}
.section-subtitle{color:var(--slate);margin-bottom:18px}
.panel,.feature-card,.metric-card,.total-card,.insight-card{
    background:var(--panel);border:1px solid var(--line);border-radius:20px;
    box-shadow:0 8px 26px rgba(15,23,42,.045);
}
.panel{padding:24px;margin-bottom:16px}
.feature-card{padding:25px;min-height:198px;margin-bottom:14px}
.feature-card .label{color:var(--orange);font-size:.76rem;font-weight:850;letter-spacing:.09em}
.feature-card h3{color:var(--ink);margin:13px 0 8px;font-size:1.25rem}
.feature-card p{color:var(--slate);line-height:1.62;margin:0}

/* Metric cards: deliberately flexible so large dollar amounts never clip */
.metric-card{padding:19px 19px 21px;min-height:114px;margin-bottom:12px;overflow:visible}
.metric-label{color:var(--slate);font-size:.83rem;font-weight:760;margin-bottom:7px}
.metric-value{color:var(--ink);font-size:clamp(1.02rem,1.45vw,1.72rem);line-height:1.15;font-weight:860;letter-spacing:-.035em;white-space:normal;overflow:visible;overflow-wrap:anywhere}
.metric-sub{color:var(--slate);font-size:.76rem;margin-top:7px;line-height:1.35}
.total-card{padding:25px 28px;border:2px solid var(--orange);background:var(--orange-soft);text-align:center;margin:8px 0 16px;overflow:visible}
.total-card .metric-label{color:#9A3412}
.total-card .metric-value{color:#7C2D12;font-size:clamp(1.35rem,2.2vw,2.5rem);white-space:normal;overflow-wrap:anywhere}

/* Insight cards */
.insight-card{padding:20px 22px;margin-bottom:12px}
.insight-kicker{color:var(--orange);font-size:.72rem;font-weight:850;letter-spacing:.08em}
.insight-title{color:var(--ink);font-size:1.05rem;font-weight:820;margin:6px 0}
.insight-body{color:var(--slate);font-size:.9rem;line-height:1.52}

.callout{padding:20px 23px;border-radius:17px;background:var(--orange-soft);border:1px solid #FED7AA;color:#7C2D12;margin:14px 0 18px}
.good{color:var(--green);font-weight:800}.bad{color:var(--red);font-weight:800}

/* Buttons */
.stButton>button,.stDownloadButton>button,.stFormSubmitButton>button{min-height:45px;border-radius:12px;font-weight:760}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:var(--orange);border-color:var(--orange);color:#fff}
.stButton>button[kind="primary"]:hover,.stFormSubmitButton>button[kind="primary"]:hover{background:var(--orange-dark);border-color:var(--orange-dark)}
.stDownloadButton>button{background:var(--navy);border-color:var(--navy);color:#fff}

.footer{margin-top:50px;padding-top:20px;border-top:1px solid var(--line);color:var(--muted);font-size:.84rem}

@media(max-width:820px){
    .hero{padding:44px 26px}.page-header{padding:25px 22px}
    .metric-value{font-size:1.1rem}.total-card .metric-value{font-size:1.45rem}
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATA
# ============================================================


def default_estimate():
    return pd.DataFrame(
        [
            ["Earthwork", "Excavation", 800.0, "CY", 12.50],
            ["Concrete", "Concrete", 120.0, "CY", 165.00],
            ["Paving", "Asphalt", 500.0, "TON", 95.00],
            ["Utilities", "Storm Pipe", 600.0, "LF", 42.00],
            ["Utilities", "Sanitary Sewer Pipe", 350.0, "LF", 55.00],
            ["Site", "Curb & Gutter", 900.0, "LF", 24.00],
        ],
        columns=BASE_COLUMNS,
    )


def cost_library():
    return pd.DataFrame(
        [
            ["Earthwork", "Excavation", "CY", 12.50],
            ["Earthwork", "Fine Grading", "SY", 2.75],
            ["Earthwork", "Rock Excavation", "CY", 58.00],
            ["Concrete", "Concrete", "CY", 165.00],
            ["Paving", "Asphalt", "TON", 95.00],
            ["Paving", "Aggregate Base", "TON", 39.00],
            ["Utilities", "Storm Pipe", "LF", 42.00],
            ["Utilities", "Sanitary Sewer Pipe", "LF", 55.00],
            ["Utilities", "Water Line", "LF", 48.00],
            ["Site", "Curb & Gutter", "LF", 24.00],
            ["Site", "Topsoil", "CY", 32.00],
            ["Erosion Control", "Silt Fence", "LF", 4.50],
            ["Erosion Control", "Construction Entrance", "EA", 1450.00],
            ["Landscaping", "Seed & Mulch", "AC", 2400.00],
        ],
        columns=["Category", "Item", "Unit", "Baseline Unit Cost ($)"],
    )


COST_LIBRARY = cost_library()


# ============================================================
# STATE
# ============================================================

DEFAULT_STATE = {
    "page": "Dashboard",
    "project_name": "Residential Site Development",
    "client": "Example Client",
    "project_location": "Blacksburg, VA",
    "project_type": "Land Development",
    "project_notes": "",
    "contingency": 10.0,
    "overhead": 5.0,
    "profit": 8.0,
    "risk_default_uncertainty": 10.0,
    "risk_simulations": 5000,
    "budget_target": 150000.0,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "estimate_data" not in st.session_state:
    st.session_state.estimate_data = default_estimate()

if "scenario_b_data" not in st.session_state:
    st.session_state.scenario_b_data = default_estimate()

if "risk_uncertainty" not in st.session_state:
    st.session_state.risk_uncertainty = {}


# ============================================================
# HELPERS
# ============================================================


def clean_estimate(data):
    df = pd.DataFrame(data).copy()
    for col in BASE_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0 if col in ["Quantity", "Unit Cost ($)"] else ""
    df = df[BASE_COLUMNS]
    for col in ["Category", "Item", "Unit"]:
        df[col] = df[col].fillna("").astype(str)
    for col in ["Quantity", "Unit Cost ($)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    df["Total Cost"] = df["Quantity"] * df["Unit Cost ($)"]
    return df


def calculate_costs(df):
    df = clean_estimate(df)
    direct = float(df["Total Cost"].sum())
    contingency = direct * float(st.session_state.contingency) / 100.0
    overhead = direct * float(st.session_state.overhead) / 100.0
    subtotal = direct + contingency + overhead
    profit = subtotal * float(st.session_state.profit) / 100.0
    return direct, contingency, overhead, profit, subtotal + profit


def money(value):
    value = float(value)
    return f"-${abs(value):,.2f}" if value < 0 else f"${value:,.2f}"


def safe_key(value):
    return re.sub(r"[^A-Za-z0-9]+", "_", str(value)).strip("_").lower() or "uncategorized"


def set_page(name):
    st.session_state.page = name


def add_library_item(item_name):
    row = COST_LIBRARY.loc[COST_LIBRARY["Item"] == item_name].iloc[0]
    new_row = pd.DataFrame(
        [{
            "Category": row["Category"],
            "Item": row["Item"],
            "Quantity": 1.0,
            "Unit": row["Unit"],
            "Unit Cost ($)": float(row["Baseline Unit Cost ($)"]),
        }]
    )
    base = clean_estimate(st.session_state.estimate_data)[BASE_COLUMNS]
    st.session_state.estimate_data = pd.concat([base, new_row], ignore_index=True)
    st.session_state.pop("estimate_editor", None)


def reset_estimate():
    st.session_state.estimate_data = default_estimate()
    st.session_state.pop("estimate_editor", None)


def copy_current_to_scenario_b():
    st.session_state.scenario_b_data = clean_estimate(st.session_state.estimate_data)[BASE_COLUMNS].copy()
    st.session_state.pop("scenario_b_editor", None)


def ensure_risk_categories(df):
    categories = (
        clean_estimate(df)["Category"]
        .replace("", "Uncategorized")
        .drop_duplicates()
        .tolist()
    )
    for category in categories:
        if category not in st.session_state.risk_uncertainty:
            st.session_state.risk_uncertainty[category] = float(st.session_state.risk_default_uncertainty)
    return categories


def run_monte_carlo(df, uncertainty_map, simulations, seed=42):
    df = clean_estimate(df)
    rng = np.random.default_rng(seed)
    simulated_direct = np.zeros(int(simulations), dtype=float)

    for _, row in df.iterrows():
        base_cost = float(row["Total Cost"])
        if base_cost <= 0:
            continue
        category = row["Category"] if row["Category"] else "Uncategorized"
        uncertainty = max(0.0, float(uncertainty_map.get(category, 10.0))) / 100.0
        if uncertainty == 0:
            simulated_direct += base_cost
        else:
            simulated_direct += base_cost * rng.triangular(
                1 - uncertainty,
                1.0,
                1 + uncertainty,
                size=int(simulations),
            )

    markup = (
        1 + st.session_state.contingency / 100.0 + st.session_state.overhead / 100.0
    ) * (1 + st.session_state.profit / 100.0)

    return simulated_direct * markup


def risk_results(df):
    categories = ensure_risk_categories(df)
    uncertainty_map = {
        category: float(st.session_state.risk_uncertainty.get(category, 10.0))
        for category in categories
    }
    samples = run_monte_carlo(
        df,
        uncertainty_map,
        int(st.session_state.risk_simulations),
    )
    return {
        "samples": samples,
        "p10": float(np.percentile(samples, 10)),
        "p50": float(np.percentile(samples, 50)),
        "p80": float(np.percentile(samples, 80)),
        "p90": float(np.percentile(samples, 90)),
        "mean": float(np.mean(samples)),
    }


def category_summary(df):
    return (
        clean_estimate(df)
        .assign(Category=lambda x: x["Category"].replace("", "Uncategorized"))
        .groupby("Category", as_index=False)["Total Cost"]
        .sum()
        .sort_values("Total Cost", ascending=False)
    )


def completeness_score(df):
    df = clean_estimate(df)
    if df.empty:
        return 0
    valid = (
        (df["Category"].str.strip() != "")
        & (df["Item"].str.strip() != "")
        & (df["Unit"].str.strip() != "")
        & (df["Quantity"] > 0)
        & (df["Unit Cost ($)"] > 0)
    )
    return int(round(valid.mean() * 100))


def html_escape(value):
    return html.escape(str(value))


# ============================================================
# UI HELPERS
# ============================================================


def page_header(title, description, eyebrow="BUILDCOST"): 
    st.markdown(
        '<div class="page-header">'
        f'<div class="eyebrow">{html_escape(eyebrow)}</div>'
        f'<h1>{html_escape(title)}</h1>'
        f'<p>{html_escape(description)}</p>'
        '</div>',
        unsafe_allow_html=True,
    )


def section(title, subtitle=None):
    body = f'<div class="section-title">{html_escape(title)}</div>'
    if subtitle:
        body += f'<div class="section-subtitle">{html_escape(subtitle)}</div>'
    st.markdown(body, unsafe_allow_html=True)


def feature(label, title, body):
    st.markdown(
        '<div class="feature-card">'
        f'<div class="label">{html_escape(label)}</div>'
        f'<h3>{html_escape(title)}</h3>'
        f'<p>{html_escape(body)}</p>'
        '</div>',
        unsafe_allow_html=True,
    )


def metric(label, value, subtext=""):
    sub = f'<div class="metric-sub">{html_escape(subtext)}</div>' if subtext else ""
    st.markdown(
        '<div class="metric-card">'
        f'<div class="metric-label">{html_escape(label)}</div>'
        f'<div class="metric-value">{html_escape(value)}</div>'
        f'{sub}'
        '</div>',
        unsafe_allow_html=True,
    )


def total_metric(label, value, subtext=""):
    sub = f'<div class="metric-sub">{html_escape(subtext)}</div>' if subtext else ""
    st.markdown(
        '<div class="total-card">'
        f'<div class="metric-label">{html_escape(label)}</div>'
        f'<div class="metric-value">{html_escape(value)}</div>'
        f'{sub}'
        '</div>',
        unsafe_allow_html=True,
    )


def insight(kicker, title, body):
    st.markdown(
        '<div class="insight-card">'
        f'<div class="insight-kicker">{html_escape(kicker)}</div>'
        f'<div class="insight-title">{html_escape(title)}</div>'
        f'<div class="insight-body">{html_escape(body)}</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        '<div class="footer"><strong>BuildCost</strong> • Construction Cost Intelligence'
        '<br>Hackathon prototype for early-stage planning. Verify quantities, pricing, scope, '
        'location, and assumptions before real project decisions.</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        '<div style="font-size:1.7rem;font-weight:900;margin-top:5px;color:white">🏗️ BUILDCOST</div>',
        unsafe_allow_html=True,
    )
    st.caption("CONSTRUCTION COST INTELLIGENCE")
    st.divider()

    for name, icon in PAGES:
        st.button(
            f"{icon}  {name}",
            key=f"nav_{name}",
            type="primary" if st.session_state.page == name else "secondary",
            use_container_width=True,
            on_click=set_page,
            args=(name,),
        )

    st.divider()
    st.caption("CURRENT PROJECT")
    st.write(f"**{st.session_state.project_name}**")
    st.caption(st.session_state.project_location)
    st.divider()
    st.caption("BuildCost Pro • Hackathon Edition")


# ============================================================
# GLOBAL CURRENT VALUES
# ============================================================

page = st.session_state.page
current_df = clean_estimate(st.session_state.estimate_data)
direct, contingency, overhead, profit, grand_total = calculate_costs(current_df)
risk_now = risk_results(current_df)
cat_df = category_summary(current_df)
readiness = completeness_score(current_df)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":
    st.markdown(
        '<div class="hero">'
        '<div class="hero-badge">CONSTRUCTION DECISION INTELLIGENCE</div>'
        '<h1>Know the cost.<br><span style="color:#FB923C">Know the risk. Know what to change.</span></h1>'
        '<p>BuildCost turns a construction estimate into a decision workspace: build the baseline, '
        'quantify uncertainty, compare alternatives, identify cost drivers, and plan toward a budget.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    b1, b2, b3, b4, spacer = st.columns([1.1, 1.1, 1.1, 1.1, 2.7])
    with b1:
        st.button("Build Estimate →", type="primary", use_container_width=True, on_click=set_page, args=("Estimate",), key="dash_est")
    with b2:
        st.button("Run Risk Lab", use_container_width=True, on_click=set_page, args=("Risk Lab",), key="dash_risk")
    with b3:
        st.button("Compare Options", use_container_width=True, on_click=set_page, args=("Scenario Studio",), key="dash_scenario")
    with b4:
        st.button("Hit a Budget", use_container_width=True, on_click=set_page, args=("Optimize",), key="dash_opt")

    section("Executive snapshot", "The numbers a project team needs before deciding what to do next.")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric("Base Estimate", money(grand_total))
    with c2:
        metric("P80 Risk Estimate", money(risk_now["p80"]), "80% of simulated outcomes are at or below this value")
    with c3:
        metric("Risk Buffer vs Base", money(risk_now["p80"] - grand_total))
    with c4:
        metric("Estimate Readiness", f"{readiness}%", "Rows with complete quantity + price data")
    with c5:
        metric("Cost Items", str(len(current_df)))

    if not cat_df.empty:
        top_category = cat_df.iloc[0]["Category"]
        top_category_cost = float(cat_df.iloc[0]["Total Cost"])
        top_share = 100 * top_category_cost / direct if direct else 0
    else:
        top_category, top_category_cost, top_share = "N/A", 0.0, 0.0

    section("Decision brief")
    i1, i2, i3 = st.columns(3)
    with i1:
        insight("TOP COST DRIVER", str(top_category), f"{money(top_category_cost)} of direct cost ({top_share:.1f}%).")
    with i2:
        risk_gap = risk_now["p80"] - grand_total
        insight("RISK EXPOSURE", "P80 planning buffer", f"A more conservative P80 plan adds {money(risk_gap)} above the current base estimate.")
    with i3:
        target = float(st.session_state.budget_target)
        gap = grand_total - target
        if gap > 0:
            insight("BUDGET STATUS", "Above target", f"Current estimate is {money(gap)} above the saved budget target of {money(target)}.")
        else:
            insight("BUDGET STATUS", "Within target", f"Current estimate is {money(abs(gap))} below the saved budget target of {money(target)}.")

    section("Cost concentration", "The categories responsible for most of the current direct cost.")
    if direct > 0 and not cat_df.empty:
        chart = px.bar(cat_df, x="Total Cost", y="Category", orientation="h", text_auto=".2s")
        chart.update_yaxes(categoryorder="total ascending")
        chart.update_layout(height=420, xaxis_title="Direct Cost ($)", yaxis_title="", margin=dict(l=10, r=20, t=15, b=10))
        st.plotly_chart(chart, use_container_width=True)

    section("Why BuildCost is different")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        feature("01 — BUILD", "Create the baseline", "Use editable quantities and pricing or start from the built-in demo cost library.")
    with f2:
        feature("02 — MODEL RISK", "Quantify uncertainty", "Run thousands of Monte Carlo simulations to understand likely cost ranges instead of relying on one number.")
    with f3:
        feature("03 — COMPARE", "Test alternatives", "Compare Scenario A and B and isolate the categories that created the cost change.")
    with f4:
        feature("04 — OPTIMIZE", "Work toward a budget", "Translate a budget gap into category-level savings targets so the next discussion has a clear starting point.")

    footer()


# ============================================================
# ESTIMATE
# ============================================================

elif page == "Estimate":
    page_header(
        "Estimate Builder",
        "Create the project baseline without the annoying double-entry reset. Inputs stay inside a form and only recalculate when you press Update Estimate.",
        "BASELINE ESTIMATE",
    )

    section("Quick add", "Use the demo cost library as a starting point, then replace values with project-specific pricing.")
    q1, q2 = st.columns([2.8, 1])
    with q1:
        library_choice = st.selectbox("Construction item", COST_LIBRARY["Item"].tolist(), key="library_choice")
    with q2:
        st.write("")
        st.write("")
        st.button("Add Selected Item", type="primary", use_container_width=True, on_click=add_library_item, args=(library_choice,), key="add_library")

    st.markdown(
        '<div class="callout"><strong>Stable editing:</strong> Make several edits in the table, then press '
        '<strong>Update Estimate</strong>. The page does not rerun after every cell entry.</div>',
        unsafe_allow_html=True,
    )

    with st.form("estimate_form", clear_on_submit=False):
        section("Project information")
        p1, p2 = st.columns(2)
        with p1:
            project_name_input = st.text_input("Project name", value=st.session_state.project_name)
            client_input = st.text_input("Client", value=st.session_state.client)
        with p2:
            project_location_input = st.text_input("Project location", value=st.session_state.project_location)
            type_index = PROJECT_TYPES.index(st.session_state.project_type) if st.session_state.project_type in PROJECT_TYPES else 0
            project_type_input = st.selectbox("Project type", PROJECT_TYPES, index=type_index)

        project_notes_input = st.text_area(
            "Project notes",
            value=st.session_state.project_notes,
            height=100,
            placeholder="Scope, assumptions, alternates, exclusions, or estimate notes...",
        )

        section("Markups")
        m1, m2, m3 = st.columns(3)
        with m1:
            contingency_input = st.number_input("Contingency (%)", 0.0, 100.0, float(st.session_state.contingency), 0.5)
        with m2:
            overhead_input = st.number_input("Overhead (%)", 0.0, 100.0, float(st.session_state.overhead), 0.5)
        with m3:
            profit_input = st.number_input("Profit (%)", 0.0, 100.0, float(st.session_state.profit), 0.5)

        section("Estimate items")
        edited_df = st.data_editor(
            st.session_state.estimate_data,
            num_rows="dynamic",
            hide_index=True,
            use_container_width=True,
            key="estimate_editor",
            column_config={
                "Category": st.column_config.TextColumn("Category"),
                "Item": st.column_config.TextColumn("Item"),
                "Quantity": st.column_config.NumberColumn("Quantity", min_value=0.0, format="%.2f"),
                "Unit": st.column_config.TextColumn("Unit"),
                "Unit Cost ($)": st.column_config.NumberColumn("Unit Cost ($)", min_value=0.0, format="$%.2f"),
            },
        )

        submitted = st.form_submit_button("Update Estimate", type="primary", use_container_width=True)

    if submitted:
        st.session_state.project_name = project_name_input
        st.session_state.client = client_input
        st.session_state.project_location = project_location_input
        st.session_state.project_type = project_type_input
        st.session_state.project_notes = project_notes_input
        st.session_state.contingency = float(contingency_input)
        st.session_state.overhead = float(overhead_input)
        st.session_state.profit = float(profit_input)
        st.session_state.estimate_data = clean_estimate(edited_df)[BASE_COLUMNS].copy()
        st.success("Estimate updated successfully.")

    estimate_df = clean_estimate(st.session_state.estimate_data)
    direct, contingency, overhead, profit, grand_total = calculate_costs(estimate_df)

    section("Estimate summary")
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        metric("Direct Cost", money(direct))
    with s2:
        metric("Contingency", money(contingency))
    with s3:
        metric("Overhead", money(overhead))
    with s4:
        metric("Profit", money(profit))

    t1, t2, t3 = st.columns([1, 2.2, 1])
    with t2:
        total_metric("Estimated Project Total", money(grand_total), "Full value is shown even for seven-figure estimates")

    e1, e2, spacer = st.columns([1.5, 1.0, 4])
    with e1:
        st.download_button(
            "⬇ Download Estimate CSV",
            estimate_df.to_csv(index=False).encode("utf-8"),
            "BuildCost_Estimate.csv",
            "text/csv",
            use_container_width=True,
        )
    with e2:
        st.button("Reset Estimate", use_container_width=True, on_click=reset_estimate, key="reset_estimate")

    footer()


# ============================================================
# RISK LAB
# ============================================================

elif page == "Risk Lab":
    page_header(
        "Risk Lab",
        "Replace the false precision of a single estimate with a probability range. BuildCost simulates cost movement by category and reports P50, P80, and P90 outcomes.",
        "MONTE CARLO COST RISK",
    )

    risk_df = clean_estimate(st.session_state.estimate_data)
    categories = ensure_risk_categories(risk_df)

    st.markdown(
        '<div class="callout"><strong>Model:</strong> each line item uses a triangular distribution centered on its current cost. '
        'The uncertainty percentage defines the potential downside and upside around that cost.</div>',
        unsafe_allow_html=True,
    )

    with st.form("risk_form", clear_on_submit=False):
        section("Risk assumptions")
        r1, r2 = st.columns(2)
        with r1:
            default_uncertainty = st.number_input(
                "Default uncertainty for new categories (%)",
                0.0,
                100.0,
                float(st.session_state.risk_default_uncertainty),
                1.0,
            )
        with r2:
            sim_options = [1000, 2500, 5000, 10000, 25000]
            current_sim = int(st.session_state.risk_simulations)
            sim_index = sim_options.index(current_sim) if current_sim in sim_options else 2
            simulations = st.selectbox("Number of simulations", sim_options, index=sim_index)

        inputs = {}
        cols = st.columns(3)
        for idx, category in enumerate(categories):
            with cols[idx % 3]:
                inputs[category] = st.number_input(
                    f"{category} uncertainty (%)",
                    0.0,
                    100.0,
                    float(st.session_state.risk_uncertainty.get(category, st.session_state.risk_default_uncertainty)),
                    1.0,
                    key=f"risk_{safe_key(category)}",
                )

        run_risk = st.form_submit_button("Run Risk Simulation", type="primary", use_container_width=True)

    if run_risk:
        st.session_state.risk_default_uncertainty = float(default_uncertainty)
        st.session_state.risk_simulations = int(simulations)
        st.session_state.risk_uncertainty = {k: float(v) for k, v in inputs.items()}
        st.success(f"Completed {st.session_state.risk_simulations:,} simulations.")

    results = risk_results(risk_df)
    _, _, _, _, base_total = calculate_costs(risk_df)

    section("Risk results")
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        metric("Base Estimate", money(base_total))
    with k2:
        metric("P50", money(results["p50"]), "Median simulated outcome")
    with k3:
        metric("P80", money(results["p80"]), "80% of simulated outcomes are at or below this value")
    with k4:
        metric("P90", money(results["p90"]))
    with k5:
        metric("P80 Buffer", money(results["p80"] - base_total), "Additional planning buffer over base")

    rr1, rr2, rr3 = st.columns([1, 2.2, 1])
    with rr2:
        total_metric(
            "Likely Cost Range (P10–P90)",
            f'{money(results["p10"])} – {money(results["p90"])}',
            f'{st.session_state.risk_simulations:,} simulations',
        )

    histogram_df = pd.DataFrame({"Simulated Project Cost": results["samples"]})
    hist = px.histogram(histogram_df, x="Simulated Project Cost", nbins=50)
    hist.update_layout(height=430, xaxis_title="Simulated Project Cost ($)", yaxis_title="Simulation Count", margin=dict(l=10, r=10, t=15, b=10))
    st.plotly_chart(hist, use_container_width=True)

    section("Risk concentration", "Categories with both high spend and high uncertainty deserve the most attention.")
    risk_table = category_summary(risk_df)
    risk_table["Uncertainty (%)"] = risk_table["Category"].map(
        lambda c: float(st.session_state.risk_uncertainty.get(c, st.session_state.risk_default_uncertainty))
    )
    risk_table["Risk Exposure Index"] = risk_table["Total Cost"] * risk_table["Uncertainty (%)"] / 100.0
    risk_table = risk_table.sort_values("Risk Exposure Index", ascending=False)
    st.dataframe(
        risk_table,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Total Cost": st.column_config.NumberColumn(format="$%.2f"),
            "Uncertainty (%)": st.column_config.NumberColumn(format="%.1f%%"),
            "Risk Exposure Index": st.column_config.NumberColumn(format="$%.2f"),
        },
    )

    footer()


# ============================================================
# SCENARIO STUDIO
# ============================================================

elif page == "Scenario Studio":
    page_header(
        "Scenario Studio",
        "Test a material, quantity, or pricing alternative without touching the baseline. BuildCost shows the total difference and the exact categories driving it.",
        "OPTION A VS OPTION B",
    )

    scenario_a = clean_estimate(st.session_state.estimate_data)
    s1, s2, spacer = st.columns([1.8, 2.4, 3])
    with s1:
        st.button("Copy Baseline to Scenario B", type="primary", use_container_width=True, on_click=copy_current_to_scenario_b, key="copy_scenario")
    with s2:
        st.caption("Scenario A is always the current baseline. Scenario B is your editable alternative.")

    with st.form("scenario_form", clear_on_submit=False):
        section("Scenario B")
        scenario_edit = st.data_editor(
            st.session_state.scenario_b_data,
            num_rows="dynamic",
            hide_index=True,
            use_container_width=True,
            key="scenario_b_editor",
            column_config={
                "Category": st.column_config.TextColumn("Category"),
                "Item": st.column_config.TextColumn("Item"),
                "Quantity": st.column_config.NumberColumn("Quantity", min_value=0.0, format="%.2f"),
                "Unit": st.column_config.TextColumn("Unit"),
                "Unit Cost ($)": st.column_config.NumberColumn("Unit Cost ($)", min_value=0.0, format="$%.2f"),
            },
        )
        scenario_submit = st.form_submit_button("Update Scenario B", type="primary", use_container_width=True)

    if scenario_submit:
        st.session_state.scenario_b_data = clean_estimate(scenario_edit)[BASE_COLUMNS].copy()
        st.success("Scenario B updated.")

    scenario_b = clean_estimate(st.session_state.scenario_b_data)
    *_, a_total = calculate_costs(scenario_a)
    *_, b_total = calculate_costs(scenario_b)
    difference = b_total - a_total
    percent_difference = difference / a_total * 100 if a_total else 0.0

    a_cat = category_summary(scenario_a).rename(columns={"Total Cost": "Scenario A"})
    b_cat = category_summary(scenario_b).rename(columns={"Total Cost": "Scenario B"})
    comparison = pd.merge(a_cat, b_cat, on="Category", how="outer").fillna(0.0)
    comparison["Difference (B - A)"] = comparison["Scenario B"] - comparison["Scenario A"]
    comparison["Absolute Change"] = comparison["Difference (B - A)"].abs()
    comparison = comparison.sort_values("Absolute Change", ascending=False)

    increases = comparison[comparison["Difference (B - A)"] > 0]
    decreases = comparison[comparison["Difference (B - A)"] < 0]
    biggest_increase = increases.iloc[0]["Category"] if not increases.empty else "None"
    biggest_savings = decreases.iloc[0]["Category"] if not decreases.empty else "None"

    section("Comparison summary")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric("Scenario A", money(a_total))
    with c2:
        metric("Scenario B", money(b_total))
    with c3:
        metric("B − A Difference", money(difference), f"{percent_difference:+.2f}%")
    with c4:
        lower = "Scenario A" if a_total < b_total else "Scenario B" if b_total < a_total else "Same Cost"
        metric("Lower-Cost Option", lower)

    section("What changed?")
    i1, i2, i3 = st.columns(3)
    with i1:
        insight("LARGEST INCREASE", str(biggest_increase), "Category with the largest positive change from A to B.")
    with i2:
        insight("LARGEST SAVINGS", str(biggest_savings), "Category with the largest negative change from A to B.")
    with i3:
        if difference > 0:
            insight("BOTTOM LINE", "Scenario B costs more", f"Scenario B adds {money(difference)} to the project total.")
        elif difference < 0:
            insight("BOTTOM LINE", "Scenario B saves money", f"Scenario B reduces the project total by {money(abs(difference))}.")
        else:
            insight("BOTTOM LINE", "No cost difference", "Both scenarios currently produce the same total.")

    if not comparison.empty:
        driver_chart = px.bar(
            comparison.sort_values("Difference (B - A)"),
            x="Difference (B - A)",
            y="Category",
            orientation="h",
            text_auto=".2s",
        )
        driver_chart.update_layout(height=440, xaxis_title="Cost Change from A to B ($)", yaxis_title="", margin=dict(l=10, r=20, t=15, b=10))
        st.plotly_chart(driver_chart, use_container_width=True)

    st.dataframe(
        comparison.drop(columns=["Absolute Change"]),
        hide_index=True,
        use_container_width=True,
        column_config={
            "Scenario A": st.column_config.NumberColumn(format="$%.2f"),
            "Scenario B": st.column_config.NumberColumn(format="$%.2f"),
            "Difference (B - A)": st.column_config.NumberColumn(format="$%.2f"),
        },
    )

    footer()


# ============================================================
# OPTIMIZE
# ============================================================

elif page == "Optimize":
    page_header(
        "Budget Optimizer",
        "Turn a budget target into a clear savings plan. BuildCost identifies the gap and allocates a mathematically proportional savings target across the largest cost categories.",
        "VALUE PLANNING",
    )

    optimize_df = clean_estimate(st.session_state.estimate_data)
    *_, current_total = calculate_costs(optimize_df)

    with st.form("budget_form", clear_on_submit=False):
        section("Set the target")
        target_input = st.number_input(
            "Target project budget ($)",
            min_value=0.0,
            value=float(st.session_state.budget_target),
            step=1000.0,
            format="%.2f",
        )
        budget_submit = st.form_submit_button("Update Budget Target", type="primary", use_container_width=True)

    if budget_submit:
        st.session_state.budget_target = float(target_input)
        st.success("Budget target updated.")

    target = float(st.session_state.budget_target)
    gap = current_total - target

    section("Budget status")
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        metric("Current Estimate", money(current_total))
    with b2:
        metric("Budget Target", money(target))
    with b3:
        metric("Gap", money(gap), "Positive means the estimate is above target")
    with b4:
        gap_pct = gap / current_total * 100 if current_total else 0.0
        metric("Required Reduction", f"{max(gap_pct, 0):.2f}%")

    if gap <= 0:
        st.markdown(
            f'<div class="callout"><strong>Within target:</strong> the current estimate is {money(abs(gap))} below the saved budget.</div>',
            unsafe_allow_html=True,
        )
    else:
        categories = category_summary(optimize_df)
        total_direct = float(categories["Total Cost"].sum())
        markup_multiplier = (current_total / total_direct) if total_direct else 1.0
        direct_savings_needed = gap / markup_multiplier if markup_multiplier else gap
        categories["Share of Direct Cost (%)"] = categories["Total Cost"] / total_direct * 100 if total_direct else 0.0
        categories["Proportional Direct-Cost Savings"] = categories["Total Cost"] / total_direct * direct_savings_needed if total_direct else 0.0
        categories["Target Category Direct Cost"] = (categories["Total Cost"] - categories["Proportional Direct-Cost Savings"]).clip(lower=0.0)

        section("Savings plan", "This is a mathematical prioritization, not an engineering recommendation. The total-budget gap is first converted to the equivalent direct-cost reduction after accounting for current markups.")
        top_three = categories.head(3)
        o1, o2, o3 = st.columns(3)
        for col, (_, row) in zip([o1, o2, o3], top_three.iterrows()):
            with col:
                insight(
                    "HIGH-LEVERAGE CATEGORY",
                    str(row["Category"]),
                    f"Current direct cost {money(row['Total Cost'])}; proportional direct-cost savings target {money(row['Proportional Direct-Cost Savings'])}.",
                )

        opt_chart = px.bar(
            categories.sort_values("Proportional Direct-Cost Savings"),
            x="Proportional Direct-Cost Savings",
            y="Category",
            orientation="h",
            text_auto=".2s",
        )
        opt_chart.update_layout(height=430, xaxis_title="Suggested Savings Allocation ($)", yaxis_title="", margin=dict(l=10, r=20, t=15, b=10))
        st.plotly_chart(opt_chart, use_container_width=True)

        st.dataframe(
            categories,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Total Cost": st.column_config.NumberColumn(format="$%.2f"),
                "Share of Direct Cost (%)": st.column_config.NumberColumn(format="%.1f%%"),
                "Proportional Direct-Cost Savings": st.column_config.NumberColumn(format="$%.2f"),
                "Target Category Direct Cost": st.column_config.NumberColumn(format="$%.2f"),
            },
        )

    footer()


# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":
    page_header(
        "Cost Analytics",
        "See where the project money is going, which items dominate the estimate, and how concentrated the current cost structure is.",
        "COST DRIVER ANALYSIS",
    )

    analytics_df = clean_estimate(st.session_state.estimate_data)
    direct, contingency, overhead, profit, total = calculate_costs(analytics_df)
    categories = category_summary(analytics_df)
    largest_category = categories.iloc[0]["Category"] if not categories.empty else "N/A"
    average_item = float(analytics_df["Total Cost"].mean()) if not analytics_df.empty else 0.0
    top5_share = (
        analytics_df.sort_values("Total Cost", ascending=False).head(5)["Total Cost"].sum() / direct * 100
        if direct else 0.0
    )

    a1, a2, a3, a4, a5 = st.columns(5)
    with a1:
        metric("Project Total", money(total))
    with a2:
        metric("Direct Cost", money(direct))
    with a3:
        metric("Largest Category", str(largest_category))
    with a4:
        metric("Average Item Cost", money(average_item))
    with a5:
        metric("Top 5 Concentration", f"{top5_share:.1f}%", "Share of direct cost in the five largest line items")

    section("Category breakdown")
    if direct > 0 and not categories.empty:
        chart = px.bar(categories, x="Total Cost", y="Category", orientation="h", text_auto=".2s")
        chart.update_yaxes(categoryorder="total ascending")
        chart.update_layout(height=450, xaxis_title="Direct Cost ($)", yaxis_title="", margin=dict(l=10, r=20, t=15, b=10))
        st.plotly_chart(chart, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.markdown("#### Category Summary")
        st.dataframe(
            categories,
            hide_index=True,
            use_container_width=True,
            column_config={"Total Cost": st.column_config.NumberColumn(format="$%.2f")},
        )
    with right:
        st.markdown("#### Project Cost Summary")
        summary_df = pd.DataFrame(
            {
                "Description": ["Direct Cost", "Contingency", "Overhead", "Profit", "Estimated Total"],
                "Amount": [direct, contingency, overhead, profit, total],
            }
        )
        st.dataframe(
            summary_df,
            hide_index=True,
            use_container_width=True,
            column_config={"Amount": st.column_config.NumberColumn(format="$%.2f")},
        )

    section("Highest-cost line items")
    top_items = analytics_df.sort_values("Total Cost", ascending=False).head(12)
    st.dataframe(
        top_items,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Quantity": st.column_config.NumberColumn(format="%.2f"),
            "Unit Cost ($)": st.column_config.NumberColumn(format="$%.2f"),
            "Total Cost": st.column_config.NumberColumn(format="$%.2f"),
        },
    )

    footer()


# ============================================================
# REPORT
# ============================================================

elif page == "Report":
    page_header(
        "Executive Report",
        "Package the current project into a concise decision brief for a judge, teammate, or stakeholder.",
        "SHAREABLE OUTPUT",
    )

    report_df = clean_estimate(st.session_state.estimate_data)
    direct, contingency, overhead, profit, total = calculate_costs(report_df)
    rr = risk_results(report_df)
    categories = category_summary(report_df)
    top_category = categories.iloc[0]["Category"] if not categories.empty else "N/A"
    top_category_cost = float(categories.iloc[0]["Total Cost"]) if not categories.empty else 0.0
    readiness = completeness_score(report_df)

    section("Executive brief")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        metric("Base Estimate", money(total))
    with r2:
        metric("P80 Estimate", money(rr["p80"]))
    with r3:
        metric("Top Cost Driver", str(top_category), money(top_category_cost))
    with r4:
        metric("Estimate Readiness", f"{readiness}%")

    report_date = date.today().isoformat()
    project_name = html_escape(st.session_state.project_name)
    client = html_escape(st.session_state.client)
    location = html_escape(st.session_state.project_location)
    project_type = html_escape(st.session_state.project_type)
    notes = html_escape(st.session_state.project_notes).replace("\n", "<br>")

    category_rows = "".join(
        f"<tr><td>{html_escape(row['Category'])}</td><td>${float(row['Total Cost']):,.2f}</td></tr>"
        for _, row in categories.iterrows()
    )
    item_rows = "".join(
        f"<tr><td>{html_escape(row['Category'])}</td><td>{html_escape(row['Item'])}</td><td>{float(row['Quantity']):,.2f}</td>"
        f"<td>{html_escape(row['Unit'])}</td><td>${float(row['Unit Cost ($)']):,.2f}</td><td>${float(row['Total Cost']):,.2f}</td></tr>"
        for _, row in report_df.iterrows()
    )

    html_report = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>BuildCost Report</title>
<style>
body{{font-family:Arial,sans-serif;margin:40px;color:#0F172A}}h1{{margin-bottom:4px}}.orange{{color:#F97316}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:24px 0}}.kpi{{border:1px solid #E2E8F0;border-radius:12px;padding:15px}}
.label{{color:#64748B;font-size:12px}}.value{{font-size:20px;font-weight:700;margin-top:5px}}table{{border-collapse:collapse;width:100%;margin:14px 0 28px}}
th,td{{border-bottom:1px solid #E2E8F0;text-align:left;padding:9px}}th{{background:#F8FAFC}}.note{{background:#FFF7ED;padding:14px;border:1px solid #FED7AA;border-radius:10px}}
</style></head><body>
<h1>BuildCost <span class='orange'>Executive Report</span></h1><div>{report_date}</div>
<h2>{project_name}</h2><p><b>Client:</b> {client}<br><b>Location:</b> {location}<br><b>Type:</b> {project_type}</p>
<div class='kpis'><div class='kpi'><div class='label'>Base Estimate</div><div class='value'>{money(total)}</div></div>
<div class='kpi'><div class='label'>P80 Risk Estimate</div><div class='value'>{money(rr['p80'])}</div></div>
<div class='kpi'><div class='label'>P80 Buffer</div><div class='value'>{money(rr['p80']-total)}</div></div>
<div class='kpi'><div class='label'>Estimate Readiness</div><div class='value'>{readiness}%</div></div></div>
<h3>Project Notes</h3><div class='note'>{notes or 'No notes provided.'}</div>
<h3>Cost by Category</h3><table><tr><th>Category</th><th>Direct Cost</th></tr>{category_rows}</table>
<h3>Estimate Items</h3><table><tr><th>Category</th><th>Item</th><th>Quantity</th><th>Unit</th><th>Unit Cost</th><th>Total</th></tr>{item_rows}</table>
<p><small>BuildCost is an early-stage planning prototype. Verify project quantities, pricing, scope, location, and assumptions before real project decisions.</small></p>
</body></html>"""

    project_backup = {
        "project_name": st.session_state.project_name,
        "client": st.session_state.client,
        "project_location": st.session_state.project_location,
        "project_type": st.session_state.project_type,
        "project_notes": st.session_state.project_notes,
        "contingency": st.session_state.contingency,
        "overhead": st.session_state.overhead,
        "profit": st.session_state.profit,
        "estimate_items": report_df[BASE_COLUMNS].to_dict(orient="records"),
    }

    d1, d2, d3 = st.columns([1.5, 1.5, 3])
    with d1:
        st.download_button(
            "⬇ Download HTML Report",
            data=html_report.encode("utf-8"),
            file_name="BuildCost_Executive_Report.html",
            mime="text/html",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            "⬇ Download Project Backup",
            data=json.dumps(project_backup, indent=2).encode("utf-8"),
            file_name="BuildCost_Project.json",
            mime="application/json",
            use_container_width=True,
        )

    section("Demo talking points")
    t1, t2, t3 = st.columns(3)
    with t1:
        insight("ESTIMATE", "Start with the baseline", f"Current total is {money(total)} across {len(report_df)} cost items.")
    with t2:
        insight("RISK", "Show uncertainty", f"P80 is {money(rr['p80'])}, which is {money(rr['p80']-total)} above the base estimate.")
    with t3:
        insight("DECISION", "Explain the driver", f"{top_category} is currently the largest direct-cost category at {money(top_category_cost)}.")

    footer()
