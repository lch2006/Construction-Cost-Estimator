import re
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="BuildCost | Construction Cost Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PAGES = ["Dashboard", "Estimate", "Risk Analysis", "Compare Scenarios", "Analytics", "About"]
PROJECT_TYPES = ["Land Development", "Commercial", "Residential", "Infrastructure", "Transportation", "Utilities", "Other"]
BASE_COLUMNS = ["Category", "Item", "Quantity", "Unit", "Unit Cost ($)"]

st.markdown(
    """
<style>
:root{--navy:#0F172A;--navy2:#1E293B;--orange:#F97316;--orange2:#EA580C;--slate:#64748B;--border:#E2E8F0;--bg:#F8FAFC}
.stApp{background:var(--bg)}
.block-container{max-width:1420px;padding-top:1.35rem;padding-bottom:4rem}
[data-testid="stHeader"]{background:rgba(248,250,252,.95)}
[data-testid="stSidebar"]{background:var(--navy);border-right:1px solid #243047}
[data-testid="stSidebar"] hr{border-color:#334155}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:#CBD5E1}
[data-testid="stSidebar"] .stButton>button{width:100%;min-height:46px;justify-content:flex-start;padding-left:15px;border-radius:11px;font-weight:700;background:#1E293B!important;border:1px solid #334155!important;color:#fff!important;transition:.18s ease}
[data-testid="stSidebar"] .stButton>button *{color:#fff!important}
[data-testid="stSidebar"] .stButton>button:hover{background:#334155!important;border-color:#F97316!important}
[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:#F97316!important;border-color:#F97316!important}
[data-testid="stSidebar"] .stButton>button[kind="primary"]:hover{background:#EA580C!important;border-color:#EA580C!important}
.hero{padding:72px 60px;border-radius:26px;background:radial-gradient(circle at 88% 12%,rgba(249,115,22,.28),transparent 27%),linear-gradient(135deg,#0F172A 0%,#172033 55%,#1E293B 100%);color:#fff;margin-bottom:26px;box-shadow:0 22px 48px rgba(15,23,42,.13)}
.hero-badge{display:inline-block;padding:7px 13px;border-radius:999px;background:rgba(249,115,22,.14);border:1px solid rgba(249,115,22,.45);color:#FDBA74;font-size:.78rem;font-weight:800;letter-spacing:.08em;margin-bottom:20px}
.hero h1{margin:0;font-size:clamp(2.7rem,6vw,5rem);line-height:1;letter-spacing:-.05em}
.hero p{max-width:840px;margin:22px 0 0;color:#CBD5E1;font-size:1.08rem;line-height:1.7}
.page-header{padding:34px 38px;border-radius:22px;background:linear-gradient(135deg,#0F172A,#1E293B);color:#fff;margin-bottom:28px}
.page-header h1{margin:0;font-size:2.35rem;letter-spacing:-.035em}.page-header p{margin:9px 0 0;color:#CBD5E1;max-width:900px;line-height:1.6}
.section-title{margin-top:30px;margin-bottom:5px;color:#0F172A;font-size:1.9rem;font-weight:800;letter-spacing:-.035em}.section-subtitle{color:#64748B;margin-bottom:22px}
.feature-card,.info-card,.metric-card,.total-card{background:#fff;border:1px solid #E2E8F0;border-radius:20px;box-shadow:0 7px 24px rgba(15,23,42,.05)}
.feature-card,.info-card{padding:28px;margin-bottom:16px}.feature-card{min-height:210px}.feature-card .label{color:#F97316;font-size:.78rem;font-weight:800;letter-spacing:.09em}.feature-card h3,.info-card h3{color:#0F172A;margin:14px 0 9px;font-size:1.35rem}.feature-card p,.info-card p{color:#64748B;line-height:1.65;margin:0}
.callout{padding:22px 26px;border-radius:18px;background:#FFF7ED;border:1px solid #FED7AA;color:#7C2D12;margin:18px 0}
.metric-card{padding:20px 20px 22px;min-height:118px;margin-bottom:12px}.metric-label{color:#64748B;font-size:.85rem;font-weight:700;margin-bottom:8px}.metric-value{color:#0F172A;font-size:clamp(1.05rem,1.55vw,1.8rem);line-height:1.15;font-weight:800;letter-spacing:-.035em;white-space:normal;overflow:visible}.metric-subtext{color:#64748B;font-size:.78rem;margin-top:7px}
.total-card{padding:26px 28px;border:2px solid #F97316;background:#FFF7ED;text-align:center;margin-top:10px;margin-bottom:18px}.total-card .metric-label{color:#9A3412}.total-card .metric-value{color:#7C2D12;font-size:clamp(1.45rem,2.2vw,2.55rem)}
.stButton>button,.stDownloadButton>button,.stFormSubmitButton>button{min-height:46px;border-radius:12px;font-weight:700}.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:#F97316;border-color:#F97316;color:#fff}.stButton>button[kind="primary"]:hover,.stFormSubmitButton>button[kind="primary"]:hover{background:#EA580C;border-color:#EA580C}.stDownloadButton>button{background:#0F172A;border-color:#0F172A;color:#fff}
.footer{margin-top:55px;padding-top:22px;border-top:1px solid #E2E8F0;color:#94A3B8;font-size:.86rem}
@media(max-width:800px){.hero{padding:48px 28px}.page-header{padding:28px 24px}.metric-value{font-size:1.15rem}}
</style>
""",
    unsafe_allow_html=True,
)


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
            ["Concrete", "Concrete", "CY", 165.00],
            ["Paving", "Asphalt", "TON", 95.00],
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

DEFAULTS = {
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
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

if "estimate_data" not in st.session_state:
    st.session_state.estimate_data = default_estimate()

if "scenario_b_data" not in st.session_state:
    st.session_state.scenario_b_data = default_estimate()

if "risk_uncertainty" not in st.session_state:
    st.session_state.risk_uncertainty = {}


def clean_estimate(data):
    df = pd.DataFrame(data).copy()

    for col in BASE_COLUMNS:
        if col not in df.columns:
            df[col] = 0.0 if col in ["Quantity", "Unit Cost ($)"] else ""

    df = df[BASE_COLUMNS]

    for col in ["Category", "Item", "Unit"]:
        df[col] = df[col].fillna("").astype(str)

    for col in ["Quantity", "Unit Cost ($)"]:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce",
        ).fillna(0.0)

    df["Total Cost"] = (
        df["Quantity"]
        *
        df["Unit Cost ($)"]
    )

    return df


def calc(df):
    df = clean_estimate(df)

    direct = float(
        df["Total Cost"].sum()
    )

    contingency = (
        direct
        *
        float(st.session_state.contingency)
        /
        100
    )

    overhead = (
        direct
        *
        float(st.session_state.overhead)
        /
        100
    )

    subtotal = (
        direct
        +
        contingency
        +
        overhead
    )

    profit = (
        subtotal
        *
        float(st.session_state.profit)
        /
        100
    )

    return (
        direct,
        contingency,
        overhead,
        profit,
        subtotal + profit,
    )


def money(value):
    value = float(value)

    if value < 0:
        return f"-${abs(value):,.2f}"

    return f"${value:,.2f}"


def safe_key(value):
    return (
        re.sub(
            r"[^A-Za-z0-9]+",
            "_",
            str(value),
        )
        .strip("_")
        .lower()
        or "uncategorized"
    )


def set_page(name):
    st.session_state.page = name


def add_library_item(item_name):
    row = (
        COST_LIBRARY.loc[
            COST_LIBRARY["Item"]
            ==
            item_name
        ]
        .iloc[0]
    )

    new_row = pd.DataFrame(
        [
            {
                "Category":
                    row["Category"],

                "Item":
                    row["Item"],

                "Quantity":
                    1.0,

                "Unit":
                    row["Unit"],

                "Unit Cost ($)":
                    float(
                        row[
                            "Baseline Unit Cost ($)"
                        ]
                    ),
            }
        ]
    )

    current = (
        clean_estimate(
            st.session_state.estimate_data
        )[BASE_COLUMNS]
    )

    st.session_state.estimate_data = (
        pd.concat(
            [
                current,
                new_row,
            ],
            ignore_index=True,
        )
    )

    st.session_state.pop(
        "estimate_editor",
        None,
    )


def reset_estimate():
    st.session_state.estimate_data = (
        default_estimate()
    )

    st.session_state.pop(
        "estimate_editor",
        None,
    )


def copy_current_to_b():
    st.session_state.scenario_b_data = (
        clean_estimate(
            st.session_state.estimate_data
        )[BASE_COLUMNS]
        .copy()
    )

    st.session_state.pop(
        "scenario_b_editor",
        None,
    )


def ensure_risk_categories(df):
    categories = (
        clean_estimate(df)["Category"]
        .replace(
            "",
            "Uncategorized",
        )
        .drop_duplicates()
        .tolist()
    )

    for category in categories:

        if (
            category
            not in
            st.session_state.risk_uncertainty
        ):

            st.session_state.risk_uncertainty[
                category
            ] = float(
                st.session_state.risk_default_uncertainty
            )

    return categories


def run_monte_carlo(
    df,
    uncertainty_map,
    simulations,
    seed=42,
):
    df = clean_estimate(df)

    rng = np.random.default_rng(
        seed
    )

    simulated_direct = np.zeros(
        int(simulations),
        dtype=float,
    )

    for _, row in df.iterrows():

        base_cost = float(
            row["Total Cost"]
        )

        if base_cost <= 0:
            continue

        category = (
            row["Category"]
            if row["Category"]
            else "Uncategorized"
        )

        uncertainty = (
            max(
                0.0,
                float(
                    uncertainty_map.get(
                        category,
                        10.0,
                    )
                ),
            )
            /
            100
        )

        if uncertainty == 0:

            simulated_direct += (
                base_cost
            )

        else:

            simulated_direct += (
                base_cost
                *
                rng.triangular(
                    1 - uncertainty,
                    1,
                    1 + uncertainty,
                    size=int(
                        simulations
                    ),
                )
            )

    markup = (
        (
            1
            +
            st.session_state.contingency / 100
            +
            st.session_state.overhead / 100
        )
        *
        (
            1
            +
            st.session_state.profit / 100
        )
    )

    return (
        simulated_direct
        *
        markup
    )


def get_risk(df):
    categories = (
        ensure_risk_categories(
            df
        )
    )

    uncertainty_map = {
        category:
            float(
                st.session_state.risk_uncertainty.get(
                    category,
                    10.0,
                )
            )
        for category in categories
    }

    samples = run_monte_carlo(
        df,
        uncertainty_map,
        int(
            st.session_state.risk_simulations
        ),
    )

    return {
        "samples":
            samples,

        "p10":
            float(
                np.percentile(
                    samples,
                    10,
                )
            ),

        "p50":
            float(
                np.percentile(
                    samples,
                    50,
                )
            ),

        "p80":
            float(
                np.percentile(
                    samples,
                    80,
                )
            ),

        "p90":
            float(
                np.percentile(
                    samples,
                    90,
                )
            ),

        "mean":
            float(
                np.mean(
                    samples
                )
            ),
    }


def header(
    title,
    description,
):
    st.markdown(
        f'<div class="page-header">'
        f'<h1>{title}</h1>'
        f'<p>{description}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


def section(
    title,
    subtitle=None,
):
    html = (
        f'<div class="section-title">'
        f'{title}'
        f'</div>'
    )

    if subtitle:

        html += (
            f'<div class="section-subtitle">'
            f'{subtitle}'
            f'</div>'
        )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def feature(
    label,
    title,
    body,
):
    st.markdown(
        f'<div class="feature-card">'
        f'<div class="label">{label}</div>'
        f'<h3>{title}</h3>'
        f'<p>{body}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )


def metric(
    label,
    value,
    subtext="",
):
    sub = (
        f'<div class="metric-subtext">'
        f'{subtext}'
        f'</div>'
        if subtext
        else ""
    )

    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'{sub}'
        f'</div>',
        unsafe_allow_html=True,
    )


def total_metric(
    label,
    value,
    subtext="",
):
    sub = (
        f'<div class="metric-subtext">'
        f'{subtext}'
        f'</div>'
        if subtext
        else ""
    )

    st.markdown(
        f'<div class="total-card">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'{sub}'
        f'</div>',
        unsafe_allow_html=True,
    )


def footer():
    st.markdown(
        '<div class="footer">'
        '<strong>BuildCost</strong> '
        '• Construction Cost Intelligence'
        '<br>'
        'Early-stage planning tool — verify project '
        'quantities, pricing, scope, location, and date '
        'before making project decisions.'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div style="'
        'font-size:1.75rem;'
        'font-weight:900;'
        'margin-top:6px;'
        'color:white;'
        '">'
        '🏗️ BUILDCOST'
        '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "CONSTRUCTION COST INTELLIGENCE"
    )

    st.divider()

    for name in PAGES:

        st.button(
            name,
            key=f"nav_{name}",
            type=(
                "primary"
                if st.session_state.page
                ==
                name
                else "secondary"
            ),
            use_container_width=True,
            on_click=set_page,
            args=(name,),
        )

    st.divider()

    st.caption(
        "CURRENT PROJECT"
    )

    st.write(
        f"**{st.session_state.project_name}**"
    )

    st.caption(
        st.session_state.project_location
    )

    st.divider()

    st.caption(
        "BuildCost v8.0"
    )


page = st.session_state.page

current_df = clean_estimate(
    st.session_state.estimate_data
)

(
    direct,
    contingency,
    overhead,
    profit,
    grand_total,
) = calc(
    current_df
)

risk_now = get_risk(
    current_df
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        '<div class="hero">'
        '<div class="hero-badge">'
        'CONSTRUCTION COST INTELLIGENCE'
        '</div>'
        '<h1>'
        'Understand what your project costs.'
        '<br>'
        '<span style="color:#FB923C;">'
        'And what could change it.'
        '</span>'
        '</h1>'
        '<p>'
        'BuildCost helps project teams create '
        'early-stage construction estimates, '
        'quantify cost uncertainty, compare '
        'alternatives, and identify the categories '
        'driving project cost before construction begins.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    b1, b2, b3, spacer = (
        st.columns(
            [
                1.15,
                1.15,
                1.15,
                3,
            ]
        )
    )

    with b1:

        st.button(
            "Build Estimate →",
            type="primary",
            use_container_width=True,
            on_click=set_page,
            args=("Estimate",),
            key="dash_est",
        )

    with b2:

        st.button(
            "Analyze Risk",
            use_container_width=True,
            on_click=set_page,
            args=("Risk Analysis",),
            key="dash_risk",
        )

    with b3:

        st.button(
            "Compare Scenarios",
            use_container_width=True,
            on_click=set_page,
            args=("Compare Scenarios",),
            key="dash_compare",
        )

    section(
        "Project snapshot",
        "The key numbers judges should understand immediately.",
    )

    m1, m2, m3, m4 = (
        st.columns(
            4
        )
    )

    with m1:
        metric(
            "Base Estimate",
            money(
                grand_total
            ),
        )

    with m2:
        metric(
            "P80 Risk Estimate",
            money(
                risk_now["p80"]
            ),
            "80% of simulated outcomes "
            "are at or below this value",
        )

    with m3:
        metric(
            "Direct Cost",
            money(
                direct
            ),
        )

    with m4:
        metric(
            "Estimate Items",
            str(
                len(
                    current_df
                )
            ),
        )

    category_df = (
        current_df
        .assign(
            Category=
                current_df["Category"]
                .replace(
                    "",
                    "Uncategorized",
                )
        )
        .groupby(
            "Category",
            as_index=False,
        )["Total Cost"]
        .sum()
        .sort_values(
            "Total Cost",
            ascending=False,
        )
    )

    section(
        "Cost drivers",
        "Where the current direct construction cost "
        "is concentrated.",
    )

    if (
        direct > 0
        and
        not category_df.empty
    ):

        fig = px.bar(
            category_df,
            x="Total Cost",
            y="Category",
            orientation="h",
            text_auto=".2s",
        )

        fig.update_yaxes(
            categoryorder=
                "total ascending"
        )

        fig.update_layout(
            height=430,
            xaxis_title=
                "Direct Cost ($)",
            yaxis_title="",
            margin=dict(
                l=10,
                r=20,
                t=15,
                b=10,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    section(
        "BuildCost workflow"
    )

    c1, c2, c3, c4 = (
        st.columns(
            4
        )
    )

    with c1:

        feature(
            "01 — ESTIMATE",
            "Build the baseline",
            "Enter quantities and unit prices "
            "or start from the built-in demo cost library.",
        )

    with c2:

        feature(
            "02 — QUANTIFY RISK",
            "Model uncertainty",
            "Run thousands of Monte Carlo simulations "
            "to understand likely project cost ranges.",
        )

    with c3:

        feature(
            "03 — COMPARE",
            "Test alternatives",
            "Compare Scenario A and B and see which "
            "categories created the difference.",
        )

    with c4:

        feature(
            "04 — DECIDE",
            "Focus on cost drivers",
            "Use analytics to understand which parts "
            "of the project deserve the most attention.",
        )

    footer()


# ============================================================
# ESTIMATE
# ============================================================

elif page == "Estimate":

    header(
        "Estimate",
        "Build the project baseline. The editor is inside "
        "a form, so typing in a cell no longer causes a "
        "rerun or makes you enter the value twice.",
    )

    section(
        "Quick add from the cost library",
        "Illustrative demo prices only — replace them "
        "with project-specific local pricing.",
    )

    q1, q2 = (
        st.columns(
            [
                2.6,
                1,
            ]
        )
    )

    with q1:

        library_choice = (
            st.selectbox(
                "Construction item",
                COST_LIBRARY[
                    "Item"
                ].tolist(),
                key=
                    "lib_choice",
            )
        )

    with q2:

        st.write("")
        st.write("")

        st.button(
            "Add Selected Item",
            type="primary",
            use_container_width=True,
            on_click=
                add_library_item,
            args=(
                library_choice,
            ),
            key="add_lib",
        )

    st.markdown(
        '<div class="callout">'
        '<strong>Tip:</strong> Make your edits, then press '
        '<strong>Update Estimate</strong>. The page will not '
        'restart after every cell entry.'
        '</div>',
        unsafe_allow_html=True,
    )

    section(
        "Project + estimate inputs"
    )

    with st.form(
        "estimate_form",
        clear_on_submit=False,
    ):

        p1, p2 = (
            st.columns(
                2
            )
        )

        with p1:

            project_name_input = (
                st.text_input(
                    "Project name",
                    value=
                        st.session_state.project_name,
                )
            )

            client_input = (
                st.text_input(
                    "Client",
                    value=
                        st.session_state.client,
                )
            )

        with p2:

            project_location_input = (
                st.text_input(
                    "Project location",
                    value=
                        st.session_state.project_location,
                )
            )

            project_type_input = (
                st.selectbox(
                    "Project type",
                    PROJECT_TYPES,
                    index=(
                        PROJECT_TYPES.index(
                            st.session_state.project_type
                        )
                        if
                        st.session_state.project_type
                        in
                        PROJECT_TYPES
                        else 0
                    ),
                )
            )

        project_notes_input = (
            st.text_area(
                "Project notes",
                value=
                    st.session_state.project_notes,
                height=110,
                placeholder=
                    "Scope, assumptions, estimate notes, "
                    "or design alternatives...",
            )
        )

        u1, u2, u3 = (
            st.columns(
                3
            )
        )

        with u1:

            contingency_input = (
                st.number_input(
                    "Contingency (%)",
                    0.0,
                    100.0,
                    float(
                        st.session_state.contingency
                    ),
                    0.5,
                )
            )

        with u2:

            overhead_input = (
                st.number_input(
                    "Overhead (%)",
                    0.0,
                    100.0,
                    float(
                        st.session_state.overhead
                    ),
                    0.5,
                )
            )

        with u3:

            profit_input = (
                st.number_input(
                    "Profit (%)",
                    0.0,
                    100.0,
                    float(
                        st.session_state.profit
                    ),
                    0.5,
                )
            )

        st.markdown(
            "#### Estimate Items"
        )

        edited_df = (
            st.data_editor(
                st.session_state.estimate_data,
                num_rows="dynamic",
                hide_index=True,
                use_container_width=True,
                key="estimate_editor",
                column_config={
                    "Category":
                        st.column_config.TextColumn(
                            "Category"
                        ),

                    "Item":
                        st.column_config.TextColumn(
                            "Item"
                        ),

                    "Quantity":
                        st.column_config.NumberColumn(
                            "Quantity",
                            min_value=0.0,
                            format="%.2f",
                        ),

                    "Unit":
                        st.column_config.TextColumn(
                            "Unit"
                        ),

                    "Unit Cost ($)":
                        st.column_config.NumberColumn(
                            "Unit Cost ($)",
                            min_value=0.0,
                            format="$%.2f",
                        ),
                },
            )
        )

        submitted = (
            st.form_submit_button(
                "Update Estimate",
                type="primary",
                use_container_width=True,
            )
        )

    if submitted:

        st.session_state.project_name = (
            project_name_input
        )

        st.session_state.client = (
            client_input
        )

        st.session_state.project_location = (
            project_location_input
        )

        st.session_state.project_type = (
            project_type_input
        )

        st.session_state.project_notes = (
            project_notes_input
        )

        st.session_state.contingency = (
            float(
                contingency_input
            )
        )

        st.session_state.overhead = (
            float(
                overhead_input
            )
        )

        st.session_state.profit = (
            float(
                profit_input
            )
        )

        st.session_state.estimate_data = (
            clean_estimate(
                edited_df
            )[BASE_COLUMNS]
            .copy()
        )

        st.success(
            "Estimate updated."
        )

    estimate_df = (
        clean_estimate(
            st.session_state.estimate_data
        )
    )

    (
        direct,
        contingency,
        overhead,
        profit,
        grand_total,
    ) = calc(
        estimate_df
    )

    section(
        "Estimate summary"
    )

    s1, s2, s3, s4 = (
        st.columns(
            4
        )
    )

    with s1:
        metric(
            "Direct Cost",
            money(
                direct
            ),
        )

    with s2:
        metric(
            "Contingency",
            money(
                contingency
            ),
        )

    with s3:
        metric(
            "Overhead",
            money(
                overhead
            ),
        )

    with s4:
        metric(
            "Profit",
            money(
                profit
            ),
        )

    left_total, middle_total, right_total = (
        st.columns(
            [
                1,
                2,
                1,
            ]
        )
    )

    with middle_total:

        total_metric(
            "Estimated Project Total",
            money(
                grand_total
            ),
            "Includes contingency, "
            "overhead, and profit",
        )

    e1, e2, spacer = (
        st.columns(
            [
                1.5,
                1.0,
                4,
            ]
        )
    )

    with e1:

        st.download_button(
            "⬇ Download Estimate CSV",
            estimate_df
            .to_csv(
                index=False
            )
            .encode(
                "utf-8"
            ),
            "BuildCost_Estimate.csv",
            "text/csv",
            use_container_width=True,
        )

    with e2:

        st.button(
            "Reset Estimate",
            use_container_width=True,
            on_click=
                reset_estimate,
            key=
                "reset_est",
        )

    footer()


# ============================================================
# RISK ANALYSIS
# ============================================================

elif page == "Risk Analysis":

    header(
        "Cost Risk & Uncertainty",
        "Move beyond a single-point estimate. BuildCost runs "
        "Monte Carlo simulations to show a range of possible "
        "project costs based on uncertainty in each category.",
    )

    risk_df = clean_estimate(
        st.session_state.estimate_data
    )

    categories = (
        ensure_risk_categories(
            risk_df
        )
    )

    st.markdown(
        '<div class="callout">'
        '<strong>How it works:</strong> Each line item is '
        'simulated with a triangular distribution centered '
        'on its current cost. The uncertainty percentage '
        'controls how far that cost can move above or below '
        'the estimate.'
        '</div>',
        unsafe_allow_html=True,
    )

    section(
        "Risk assumptions",
        "Set uncertainty by category, then run the simulation.",
    )

    with st.form(
        "risk_form",
        clear_on_submit=False,
    ):

        rtop1, rtop2 = (
            st.columns(
                2
            )
        )

        with rtop1:

            default_uncertainty = (
                st.number_input(
                    "Default uncertainty for new categories (%)",
                    0.0,
                    100.0,
                    float(
                        st.session_state.risk_default_uncertainty
                    ),
                    1.0,
                )
            )

        with rtop2:

            sim_options = [
                1000,
                2500,
                5000,
                10000,
            ]

            sim_index = (
                sim_options.index(
                    int(
                        st.session_state.risk_simulations
                    )
                )
                if
                int(
                    st.session_state.risk_simulations
                )
                in
                sim_options
                else 2
            )

            simulations = (
                st.selectbox(
                    "Number of simulations",
                    sim_options,
                    index=sim_index,
                )
            )

        inputs = {}

        cols = (
            st.columns(
                3
            )
        )

        for index, category in enumerate(
            categories
        ):

            with cols[
                index % 3
            ]:

                inputs[
                    category
                ] = (
                    st.number_input(
                        f"{category} uncertainty (%)",
                        0.0,
                        100.0,
                        float(
                            st.session_state.risk_uncertainty.get(
                                category,
                                st.session_state.risk_default_uncertainty,
                            )
                        ),
                        1.0,
                        key=
                            f"risk_{safe_key(category)}",
                    )
                )

        risk_submit = (
            st.form_submit_button(
                "Run Risk Simulation",
                type="primary",
                use_container_width=True,
            )
        )

    if risk_submit:

        st.session_state.risk_default_uncertainty = (
            float(
                default_uncertainty
            )
        )

        st.session_state.risk_simulations = (
            int(
                simulations
            )
        )

        st.session_state.risk_uncertainty = {
            key:
                float(
                    value
                )
            for key, value
            in inputs.items()
        }

        st.success(
            f"Completed "
            f"{st.session_state.risk_simulations:,} "
            f"simulations."
        )

    results = get_risk(
        risk_df
    )

    (
        base_direct,
        base_contingency,
        base_overhead,
        base_profit,
        base_total,
    ) = calc(
        risk_df
    )

    section(
        "Risk results"
    )

    r1, r2, r3, r4 = (
        st.columns(
            4
        )
    )

    with r1:

        metric(
            "Base Estimate",
            money(
                base_total
            ),
        )

    with r2:

        metric(
            "P50 Estimate",
            money(
                results["p50"]
            ),
            "Median outcome",
        )

    with r3:

        metric(
            "P80 Estimate",
            money(
                results["p80"]
            ),
            "80% of simulated outcomes "
            "are at or below this value",
        )

    with r4:

        metric(
            "P90 Estimate",
            money(
                results["p90"]
            ),
        )

    risk_left, risk_middle, risk_right = (
        st.columns(
            [
                1,
                2,
                1,
            ]
        )
    )

    with risk_middle:

        total_metric(
            "Likely Cost Range (P10–P90)",
            f'{money(results["p10"])} – '
            f'{money(results["p90"])}',
            f'{st.session_state.risk_simulations:,} '
            f'simulations',
        )

    histogram_df = (
        pd.DataFrame(
            {
                "Simulated Project Cost":
                    results["samples"]
            }
        )
    )

    fig = px.histogram(
        histogram_df,
        x=
            "Simulated Project Cost",
        nbins=45,
    )

    fig.update_layout(
        height=440,
        xaxis_title=
            "Simulated Project Cost ($)",
        yaxis_title=
            "Simulation Count",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    section(
        "Current uncertainty assumptions"
    )

    category_costs = (
        risk_df
        .assign(
            Category=
                risk_df["Category"]
                .replace(
                    "",
                    "Uncategorized",
                )
        )
        .groupby(
            "Category",
            as_index=False,
        )["Total Cost"]
        .sum()
    )

    category_costs[
        "Uncertainty (%)"
    ] = (
        category_costs[
            "Category"
        ]
        .map(
            lambda category:
                float(
                    st.session_state.risk_uncertainty.get(
                        category,
                        st.session_state.risk_default_uncertainty,
                    )
                )
        )
    )

    st.dataframe(
        category_costs,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Total Cost":
                st.column_config.NumberColumn(
                    format="$%.2f"
                ),

            "Uncertainty (%)":
                st.column_config.NumberColumn(
                    format="%.1f%%"
                ),
        },
    )

    footer()


# ============================================================
# COMPARE SCENARIOS
# ============================================================

elif page == "Compare Scenarios":

    header(
        "Compare Scenarios",
        "Compare the current estimate (Scenario A) with "
        "an alternative Scenario B, then identify exactly "
        "which categories are driving the difference.",
    )

    scenario_a = (
        clean_estimate(
            st.session_state.estimate_data
        )
    )

    top1, top2, spacer = (
        st.columns(
            [
                1.8,
                2.5,
                3,
            ]
        )
    )

    with top1:

        st.button(
            "Copy Current Estimate to B",
            type="primary",
            use_container_width=True,
            on_click=
                copy_current_to_b,
            key=
                "copy_b",
        )

    with top2:

        st.caption(
            "Scenario A stays unchanged. "
            "Edit Scenario B and press "
            "Update Scenario B."
        )

    section(
        "Scenario B",
        "Try a different material, quantity, "
        "unit price, or design alternative.",
    )

    with st.form(
        "scenario_form",
        clear_on_submit=False,
    ):

        scenario_edit = (
            st.data_editor(
                st.session_state.scenario_b_data,
                num_rows="dynamic",
                hide_index=True,
                use_container_width=True,
                key=
                    "scenario_b_editor",
                column_config={
                    "Category":
                        st.column_config.TextColumn(
                            "Category"
                        ),

                    "Item":
                        st.column_config.TextColumn(
                            "Item"
                        ),

                    "Quantity":
                        st.column_config.NumberColumn(
                            "Quantity",
                            min_value=0.0,
                            format="%.2f",
                        ),

                    "Unit":
                        st.column_config.TextColumn(
                            "Unit"
                        ),

                    "Unit Cost ($)":
                        st.column_config.NumberColumn(
                            "Unit Cost ($)",
                            min_value=0.0,
                            format="$%.2f",
                        ),
                },
            )
        )

        scenario_submit = (
            st.form_submit_button(
                "Update Scenario B",
                type="primary",
                use_container_width=True,
            )
        )

    if scenario_submit:

        st.session_state.scenario_b_data = (
            clean_estimate(
                scenario_edit
            )[BASE_COLUMNS]
            .copy()
        )

        st.success(
            "Scenario B updated."
        )

    scenario_b = (
        clean_estimate(
            st.session_state.scenario_b_data
        )
    )

    (
        a_direct,
        a_contingency,
        a_overhead,
        a_profit,
        a_total,
    ) = calc(
        scenario_a
    )

    (
        b_direct,
        b_contingency,
        b_overhead,
        b_profit,
        b_total,
    ) = calc(
        scenario_b
    )

    difference = (
        b_total
        -
        a_total
    )

    percentage_difference = (
        (
            difference
            /
            a_total
            *
            100
        )
        if a_total
        else 0.0
    )

    a_categories = (
        scenario_a
        .assign(
            Category=
                scenario_a["Category"]
                .replace(
                    "",
                    "Uncategorized",
                )
        )
        .groupby(
            "Category",
            as_index=False,
        )["Total Cost"]
        .sum()
        .rename(
            columns={
                "Total Cost":
                    "Scenario A"
            }
        )
    )

    b_categories = (
        scenario_b
        .assign(
            Category=
                scenario_b["Category"]
                .replace(
                    "",
                    "Uncategorized",
                )
        )
        .groupby(
            "Category",
            as_index=False,
        )["Total Cost"]
        .sum()
        .rename(
            columns={
                "Total Cost":
                    "Scenario B"
            }
        )
    )

    comparison = (
        pd.merge(
            a_categories,
            b_categories,
            on="Category",
            how="outer",
        )
        .fillna(
            0.0
        )
    )

    comparison[
        "Difference (B - A)"
    ] = (
        comparison[
            "Scenario B"
        ]
        -
        comparison[
            "Scenario A"
        ]
    )

    comparison[
        "Absolute Change"
    ] = (
        comparison[
            "Difference (B - A)"
        ]
        .abs()
    )

    comparison = (
        comparison
        .sort_values(
            "Absolute Change",
            ascending=False,
        )
    )

    increases = (
        comparison[
            comparison[
                "Difference (B - A)"
            ]
            >
            0
        ]
    )

    decreases = (
        comparison[
            comparison[
                "Difference (B - A)"
            ]
            <
            0
        ]
    )

    largest_increase = (
        increases
        .iloc[0]["Category"]
        if not increases.empty
        else "None"
    )

    largest_savings = (
        decreases
        .iloc[0]["Category"]
        if not decreases.empty
        else "None"
    )

    section(
        "Comparison summary"
    )

    c1, c2, c3, c4 = (
        st.columns(
            4
        )
    )

    with c1:

        metric(
            "Scenario A",
            money(
                a_total
            ),
        )

    with c2:

        metric(
            "Scenario B",
            money(
                b_total
            ),
        )

    with c3:

        metric(
            "Difference (B − A)",
            money(
                difference
            ),
            f"{percentage_difference:+.2f}%",
        )

    with c4:

        lower_cost = (
            "A"
            if a_total < b_total
            else
            "B"
            if b_total < a_total
            else
            "Same"
        )

        metric(
            "Lower-Cost Scenario",
            lower_cost,
        )

    section(
        "What caused the change?",
        "Categories are ranked by the "
        "size of their cost change.",
    )

    d1, d2 = (
        st.columns(
            2
        )
    )

    with d1:

        metric(
            "Largest Cost Increase",
            largest_increase,
        )

    with d2:

        metric(
            "Largest Savings",
            largest_savings,
        )

    if not comparison.empty:

        fig = px.bar(
            comparison
            .sort_values(
                "Difference (B - A)"
            ),
            x=
                "Difference (B - A)",
            y="Category",
            orientation="h",
            text_auto=".2s",
        )

        fig.update_layout(
            height=450,
            xaxis_title=
                "Cost Change from A to B ($)",
            yaxis_title="",
            margin=dict(
                l=10,
                r=20,
                t=20,
                b=10,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.dataframe(
        comparison.drop(
            columns=[
                "Absolute Change"
            ]
        ),
        hide_index=True,
        use_container_width=True,
        column_config={
            "Scenario A":
                st.column_config.NumberColumn(
                    format="$%.2f"
                ),

            "Scenario B":
                st.column_config.NumberColumn(
                    format="$%.2f"
                ),

            "Difference (B - A)":
                st.column_config.NumberColumn(
                    format="$%.2f"
                ),
        },
    )

    footer()


# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":

    header(
        "Analytics",
        "Identify the categories and line items "
        "driving the current project estimate.",
    )

    analytics_df = (
        clean_estimate(
            st.session_state.estimate_data
        )
    )

    (
        direct,
        contingency,
        overhead,
        profit,
        total,
    ) = calc(
        analytics_df
    )

    category_df = (
        analytics_df
        .assign(
            Category=
                analytics_df[
                    "Category"
                ]
                .replace(
                    "",
                    "Uncategorized",
                )
        )
        .groupby(
            "Category",
            as_index=False,
        )["Total Cost"]
        .sum()
        .sort_values(
            "Total Cost",
            ascending=False,
        )
    )

    largest_category = (
        category_df
        .iloc[0]["Category"]
        if not category_df.empty
        else "N/A"
    )

    average_item_cost = (
        float(
            analytics_df[
                "Total Cost"
            ].mean()
        )
        if not analytics_df.empty
        else 0.0
    )

    a1, a2, a3, a4 = (
        st.columns(
            4
        )
    )

    with a1:

        metric(
            "Project Total",
            money(
                total
            ),
        )

    with a2:

        metric(
            "Largest Category",
            largest_category,
        )

    with a3:

        metric(
            "Cost Items",
            str(
                len(
                    analytics_df
                )
            ),
        )

    with a4:

        metric(
            "Average Item Cost",
            money(
                average_item_cost
            ),
        )

    section(
        "Cost by category"
    )

    if (
        direct > 0
        and
        not category_df.empty
    ):

        fig = px.bar(
            category_df,
            x="Total Cost",
            y="Category",
            orientation="h",
            text_auto=".2s",
        )

        fig.update_yaxes(
            categoryorder=
                "total ascending"
        )

        fig.update_layout(
            height=470,
            xaxis_title=
                "Direct Cost ($)",
            yaxis_title="",
            margin=dict(
                l=10,
                r=20,
                t=20,
                b=10,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    left, right = (
        st.columns(
            2
        )
    )

    with left:

        st.markdown(
            "#### Category Summary"
        )

        st.dataframe(
            category_df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Total Cost":
                    st.column_config.NumberColumn(
                        format="$%.2f"
                    )
            },
        )

    with right:

        st.markdown(
            "#### Project Cost Summary"
        )

        summary = pd.DataFrame(
            {
                "Description": [
                    "Direct Cost",
                    "Contingency",
                    "Overhead",
                    "Profit",
                    "Estimated Total",
                ],

                "Amount": [
                    direct,
                    contingency,
                    overhead,
                    profit,
                    total,
                ],
            }
        )

        st.dataframe(
            summary,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Amount":
                    st.column_config.NumberColumn(
                        format="$%.2f"
                    )
            },
        )

    section(
        "Highest-cost line items"
    )

    top_items = (
        analytics_df
        .sort_values(
            "Total Cost",
            ascending=False,
        )
        .head(
            10
        )
    )

    st.dataframe(
        top_items,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Quantity":
                st.column_config.NumberColumn(
                    format="%.2f"
                ),

            "Unit Cost ($)":
                st.column_config.NumberColumn(
                    format="$%.2f"
                ),

            "Total Cost":
                st.column_config.NumberColumn(
                    format="$%.2f"
                ),
        },
    )

    footer()


# ============================================================
# ABOUT
# ============================================================

elif page == "About":

    header(
        "About BuildCost",
        "A construction-tech hackathon prototype "
        "focused on estimating, uncertainty, "
        "alternative comparison, and project cost visibility.",
    )

    st.markdown(
        '<div class="hero">'
        '<div class="hero-badge">'
        'THE IDEA'
        '</div>'
        '<h1 style="font-size:3.5rem;">'
        'Estimate the project.'
        '<br>'
        '<span style="color:#FB923C;">'
        'Then challenge the assumptions.'
        '</span>'
        '</h1>'
        '<p>'
        'BuildCost combines a project estimate, '
        'construction cost library, Monte Carlo risk analysis, '
        'scenario comparison, and cost-driver analytics '
        'in one lightweight web application.'
        '</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = (
        st.columns(
            3
        )
    )

    with c1:

        feature(
            "PROBLEM",
            "A single estimate hides uncertainty",
            "Construction quantities, unit prices, "
            "and design choices can change throughout planning.",
        )

    with c2:

        feature(
            "SOLUTION",
            "Make decisions visible",
            "BuildCost shows the baseline, the possible "
            "cost range, and the categories responsible for changes.",
        )

    with c3:

        feature(
            "FUTURE",
            "Connect better data",
            "Future versions could add regional price databases, "
            "saved projects, collaboration, and professional reporting.",
        )

    section(
        "Technology"
    )

    st.write(
        "**Python** · "
        "**Streamlit** · "
        "**Pandas** · "
        "**NumPy** · "
        "**Plotly** · "
        "**GitHub**"
    )

    st.markdown(
        '<div class="callout">'
        '<strong>Hackathon focus:</strong> '
        'BuildCost is a decision-support prototype, '
        'not a replacement for professional estimating '
        'software or verified construction cost databases.'
        '</div>',
        unsafe_allow_html=True,
    )

    footer()
