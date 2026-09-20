import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote


# ============================================================
# BUILDCOST V2
# Construction Cost Planning Platform
# ============================================================


# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="BuildCost | Construction Cost Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ------------------------------------------------------------
# BRAND / SETTINGS
# ------------------------------------------------------------

BRAND_NAME = "BuildCost"
CONTACT_EMAIL = "your-email@example.com"

NAV_OPTIONS = [
    "Home",
    "Cost Estimator",
    "Cost Analytics",
    "Project Information",
    "About BuildCost",
    "Contact"
]


# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #F8FAFC;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.6rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.025em;
    }

    /* ---------- STREAMLIT HEADER ---------- */

    [data-testid="stHeader"] {
        background: rgba(248, 250, 252, 0.92);
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #0F172A;
        border-right: 1px solid #1E293B;
    }

    [data-testid="stSidebar"] * {
        color: #F8FAFC;
    }

    [data-testid="stSidebar"] hr {
        border-color: #334155;
    }

    /* ---------- HERO ---------- */

    .hero {
        position: relative;
        overflow: hidden;
        padding: 76px 64px;
        border-radius: 26px;
        background:
            radial-gradient(
                circle at 90% 15%,
                rgba(249, 115, 22, 0.28),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #0F172A 0%,
                #172033 55%,
                #1E293B 100%
            );
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.14);
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(249, 115, 22, 0.15);
        border: 1px solid rgba(249, 115, 22, 0.4);
        color: #FDBA74;
        font-weight: 700;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        margin-bottom: 20px;
    }

    .hero h1 {
        font-size: clamp(2.6rem, 6vw, 5.2rem);
        line-height: 0.98;
        margin: 0;
        max-width: 850px;
        letter-spacing: -0.055em;
    }

    .hero p {
        max-width: 760px;
        color: #CBD5E1;
        font-size: 1.12rem;
        line-height: 1.7;
        margin-top: 24px;
        margin-bottom: 0;
    }

    /* ---------- PAGE HEADER ---------- */

    .page-header {
        padding: 34px 38px;
        border-radius: 22px;
        background: #0F172A;
        color: white;
        margin-bottom: 26px;
    }

    .page-header h1 {
        margin: 0;
        font-size: 2.3rem;
    }

    .page-header p {
        margin: 8px 0 0;
        color: #CBD5E1;
        max-width: 800px;
    }

    /* ---------- CARDS ---------- */

    .feature-card {
        min-height: 215px;
        padding: 28px;
        border-radius: 20px;
        background: white;
        border: 1px solid #E2E8F0;
        box-shadow: 0 8px 30px rgba(15, 23, 42, 0.05);
        margin-bottom: 18px;
    }

    .feature-number {
        color: #F97316;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.1em;
    }

    .feature-card h3 {
        color: #0F172A;
        margin-top: 15px;
        margin-bottom: 9px;
        font-size: 1.35rem;
    }

    .feature-card p {
        color: #64748B;
        line-height: 1.65;
        margin-bottom: 0;
    }

    .info-card {
        padding: 26px;
        border-radius: 18px;
        background: white;
        border: 1px solid #E2E8F0;
        box-shadow: 0 6px 22px rgba(15, 23, 42, 0.04);
        margin-bottom: 18px;
    }

    .info-card h3 {
        margin-top: 0;
        color: #0F172A;
    }

    .info-card p {
        color: #64748B;
        line-height: 1.65;
    }

    /* ---------- METRICS ---------- */

    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #E2E8F0;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B;
    }

    [data-testid="stMetricValue"] {
        color: #0F172A;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 12px;
        min-height: 46px;
        font-weight: 700;
        border: 1px solid #CBD5E1;
    }

    .stButton > button[kind="primary"] {
        background: #F97316;
        border-color: #F97316;
        color: white;
    }

    .stDownloadButton > button {
        border-radius: 12px;
        min-height: 46px;
        font-weight: 700;
        background: #0F172A;
        color: white;
        border: 1px solid #0F172A;
    }

    /* ---------- INPUTS ---------- */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    textarea {
        border-radius: 10px !important;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        margin-top: 20px;
        margin-bottom: 6px;
        font-size: 2rem;
        color: #0F172A;
        font-weight: 800;
        letter-spacing: -0.035em;
    }

    .section-subtitle {
        color: #64748B;
        margin-bottom: 24px;
        font-size: 1rem;
    }

    /* ---------- ACCENT ---------- */

    .accent {
        color: #F97316;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        margin-top: 55px;
        padding-top: 22px;
        border-top: 1px solid #E2E8F0;
        color: #94A3B8;
        font-size: 0.86rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# DEFAULT DATA
# ------------------------------------------------------------

def default_items():

    return pd.DataFrame(
        [
            ["Earthwork", "Excavation", 800.0, "CY", 12.50],
            ["Concrete", "Concrete", 120.0, "CY", 165.00],
            ["Paving", "Asphalt", 500.0, "TON", 95.00],
            ["Utilities", "Storm Pipe", 600.0, "LF", 42.00],
            ["Utilities", "Sanitary Sewer Pipe", 350.0, "LF", 55.00],
            ["Site", "Curb & Gutter", 900.0, "LF", 24.00]
        ],
        columns=[
            "Category",
            "Item",
            "Quantity",
            "Unit",
            "Unit Cost ($)"
        ]
    )


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "project_name" not in st.session_state:
    st.session_state.project_name = "Residential Site Development"

if "client" not in st.session_state:
    st.session_state.client = "Example Client"

if "project_location" not in st.session_state:
    st.session_state.project_location = "Blacksburg, VA"

if "project_type" not in st.session_state:
    st.session_state.project_type = "Land Development"

if "project_notes" not in st.session_state:
    st.session_state.project_notes = ""

if "contingency" not in st.session_state:
    st.session_state.contingency = 10.0

if "overhead" not in st.session_state:
    st.session_state.overhead = 5.0

if "profit" not in st.session_state:
    st.session_state.profit = 8.0


# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------

def clean_estimate(df):

    cleaned = df.copy()

    required_columns = [
        "Category",
        "Item",
        "Quantity",
        "Unit",
        "Unit Cost ($)"
    ]

    for column in required_columns:

        if column not in cleaned.columns:
            cleaned[column] = ""

    cleaned = cleaned[required_columns]

    for column in ["Category", "Item", "Unit"]:

        cleaned[column] = (
            cleaned[column]
            .fillna("")
            .astype(str)
        )

    for column in ["Quantity", "Unit Cost ($)"]:

        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="coerce"
        ).fillna(0.0)

    cleaned["Total Cost"] = (
        cleaned["Quantity"]
        *
        cleaned["Unit Cost ($)"]
    )

    return cleaned


def calculate_costs(df):

    direct = float(
        df["Total Cost"].sum()
    )

    contingency_cost = (
        direct
        *
        st.session_state.contingency
        /
        100.0
    )

    overhead_cost = (
        direct
        *
        st.session_state.overhead
        /
        100.0
    )

    subtotal = (
        direct
        +
        contingency_cost
        +
        overhead_cost
    )

    profit_cost = (
        subtotal
        *
        st.session_state.profit
        /
        100.0
    )

    total = (
        subtotal
        +
        profit_cost
    )

    return (
        direct,
        contingency_cost,
        overhead_cost,
        profit_cost,
        total
    )


def page_header(title, description):

    st.markdown(
        f"""
        <div class="page-header">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def footer():

    st.markdown(
        """
        <div class="footer">
            <strong>BuildCost</strong> • Construction Cost Intelligence
            <br>
            Estimates are planning tools. Unit costs should be verified
            for the specific project, location, scope, and date.
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# SIDEBAR / HAMBURGER MENU
# ------------------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:1.65rem;
            font-weight:900;
            padding-top:10px;
            margin-bottom:2px;
        ">
            🏗️ BUILDCOST
        </div>

        <div style="
            color:#94A3B8;
            font-size:.82rem;
            margin-bottom:22px;
        ">
            CONSTRUCTION COST INTELLIGENCE
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_page = st.radio(
        "Navigation",
        NAV_OPTIONS,
        index=NAV_OPTIONS.index(st.session_state.page),
        label_visibility="collapsed"
    )

    st.session_state.page = selected_page

    st.divider()

    st.caption("CURRENT PROJECT")

    st.write(
        f"**{st.session_state.project_name}**"
    )

    st.caption(
        st.session_state.project_location
    )

    st.divider()

    st.caption(
        "BuildCost v2.0"
    )


# ------------------------------------------------------------
# CURRENT ESTIMATE DATA
# ------------------------------------------------------------

# The estimator widget maintains its own state.
# This safely reads the current edited value when available.

if "estimate_editor" in st.session_state:

    editor_state = st.session_state["estimate_editor"]

# Use a stable starting DataFrame for calculations outside estimator.
# The current estimate is also stored separately after editor use.

if "current_estimate" not in st.session_state:

    st.session_state.current_estimate = default_items()


current_df = clean_estimate(
    st.session_state.current_estimate
)

(
    direct_cost,
    contingency_cost,
    overhead_cost,
    profit_cost,
    grand_total
) = calculate_costs(current_df)


# ============================================================
# HOME
# ============================================================

if st.session_state.page == "Home":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-badge">
                CONSTRUCTION COST INTELLIGENCE
            </div>

            <h1>
                Build smarter.<br>
                <span style="color:#FB923C;">
                    Estimate faster.
                </span>
            </h1>

            <p>
                BuildCost helps contractors, engineers, developers,
                and project teams transform construction quantities
                and unit pricing into clear, organized early-stage
                project estimates.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    button1, button2, spacer = st.columns(
        [1.1, 1.1, 4]
    )

    with button1:

        if st.button(
            "Create an Estimate →",
            type="primary",
            use_container_width=True
        ):

            st.session_state.page = "Cost Estimator"
            st.rerun()

    with button2:

        if st.button(
            "About BuildCost",
            use_container_width=True
        ):

            st.session_state.page = "About BuildCost"
            st.rerun()

    st.markdown(
        """
        <div class="section-title">
            From quantities to project cost.
        </div>

        <div class="section-subtitle">
            One workspace for early construction cost planning.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-number">01 — ESTIMATE</div>
                <h3>Build your estimate</h3>
                <p>
                    Organize construction activities, quantities,
                    units, and unit prices in an editable project
                    estimate.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-number">02 — ANALYZE</div>
                <h3>Understand your costs</h3>
                <p>
                    See which construction categories are driving
                    project cost using interactive visualizations
                    and project metrics.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-number">03 — EXPORT</div>
                <h3>Take your data with you</h3>
                <p>
                    Export organized estimate data for documentation,
                    additional analysis, and project planning.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="section-title">
            Current project snapshot
        </div>
        """,
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Estimated Total",
        f"${grand_total:,.0f}"
    )

    m2.metric(
        "Direct Cost",
        f"${direct_cost:,.0f}"
    )

    m3.metric(
        "Cost Items",
        f"{len(current_df)}"
    )

    category_count = (
        current_df["Category"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )

    m4.metric(
        "Categories",
        category_count
    )

    footer()


# ============================================================
# COST ESTIMATOR
# ============================================================

elif st.session_state.page == "Cost Estimator":

    page_header(
        "Cost Estimator",
        "Build an early-stage project estimate using construction "
        "quantities, units, and unit pricing."
    )

    st.markdown(
        """
        <div class="section-title">
            Project markups
        </div>

        <div class="section-subtitle">
            Configure the percentages applied to your project estimate.
        </div>
        """,
        unsafe_allow_html=True
    )

    markup1, markup2, markup3 = st.columns(3)

    with markup1:

        st.session_state.contingency = st.number_input(
            "Contingency (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.contingency),
            step=0.5
        )

    with markup2:

        st.session_state.overhead = st.number_input(
            "Overhead (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.overhead),
            step=0.5
        )

    with markup3:

        st.session_state.profit = st.number_input(
            "Profit (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.profit),
            step=0.5
        )

    st.markdown(
        """
        <div class="section-title">
            Estimate items
        </div>

        <div class="section-subtitle">
            Edit existing items or add new construction activities.
        </div>
        """,
        unsafe_allow_html=True
    )

    edited = st.data_editor(
        st.session_state.current_estimate,
        num_rows="dynamic",
        hide_index=True,
        use_container_width=True,
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
                    format="%.2f"
                ),

            "Unit":
                st.column_config.TextColumn(
                    "Unit"
                ),

            "Unit Cost ($)":
                st.column_config.NumberColumn(
                    "Unit Cost ($)",
                    min_value=0.0,
                    format="$%.2f"
                )
        },
        key="estimate_editor"
    )

    working_df = clean_estimate(
        edited
    )

    # Keep latest estimate available to other pages.
    st.session_state.current_estimate = (
        working_df[
            [
                "Category",
                "Item",
                "Quantity",
                "Unit",
                "Unit Cost ($)"
            ]
        ].copy()
    )

    (
        direct_cost,
        contingency_cost,
        overhead_cost,
        profit_cost,
        grand_total
    ) = calculate_costs(
        working_df
    )

    st.markdown(
        """
        <div class="section-title">
            Estimate summary
        </div>
        """,
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Direct Cost",
        f"${direct_cost:,.2f}"
    )

    m2.metric(
        "Contingency",
        f"${contingency_cost:,.2f}",
        f"{st.session_state.contingency:.1f}%"
    )

    m3.metric(
        "Overhead",
        f"${overhead_cost:,.2f}",
        f"{st.session_state.overhead:.1f}%"
    )

    m4.metric(
        "Project Total",
        f"${grand_total:,.2f}"
    )

    st.markdown("#### Detailed estimate")

    st.dataframe(
        working_df,
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
                )
        }
    )

    export_df = working_df.copy()

    csv_data = export_df.to_csv(
        index=False
    ).encode(
        "utf-8"
    )

    st.download_button(
        "⬇ Download Estimate CSV",
        data=csv_data,
        file_name="BuildCost_Estimate.csv",
        mime="text/csv"
    )

    footer()


# ============================================================
# COST ANALYTICS
# ============================================================

elif st.session_state.page == "Cost Analytics":

    page_header(
        "Cost Analytics",
        "Understand where project money is being spent and identify "
        "the categories driving your estimate."
    )

    analytics_df = clean_estimate(
        st.session_state.current_estimate
    )

    (
        direct_cost,
        contingency_cost,
        overhead_cost,
        profit_cost,
        grand_total
    ) = calculate_costs(
        analytics_df
    )

    if not analytics_df.empty:

        category_df = (
            analytics_df
            .assign(
                Category=analytics_df["Category"]
                .replace("", "Uncategorized")
            )
            .groupby(
                "Category",
                as_index=False
            )["Total Cost"]
            .sum()
            .sort_values(
                "Total Cost",
                ascending=False
            )
        )

        if not category_df.empty:

            largest_category = (
                category_df.iloc[0]["Category"]
            )

            largest_category_cost = float(
                category_df.iloc[0]["Total Cost"]
            )

        else:

            largest_category = "N/A"
            largest_category_cost = 0.0

    else:

        category_df = pd.DataFrame(
            columns=[
                "Category",
                "Total Cost"
            ]
        )

        largest_category = "N/A"
        largest_category_cost = 0.0

    average_item_cost = (
        float(
            analytics_df["Total Cost"].mean()
        )
        if len(analytics_df) > 0
        else 0.0
    )

    a1, a2, a3, a4 = st.columns(4)

    a1.metric(
        "Project Total",
        f"${grand_total:,.0f}"
    )

    a2.metric(
        "Largest Category",
        largest_category
    )

    a3.metric(
        "Cost Items",
        len(analytics_df)
    )

    a4.metric(
        "Average Item Cost",
        f"${average_item_cost:,.0f}"
    )

    st.markdown(
        """
        <div class="section-title">
            Cost by category
        </div>
        """,
        unsafe_allow_html=True
    )

    if (
        not category_df.empty
        and
        direct_cost > 0
    ):

        chart = px.bar(
            category_df,
            x="Total Cost",
            y="Category",
            orientation="h",
            text_auto=".2s"
        )

        chart.update_layout(
            height=460,
            xaxis_title="Cost ($)",
            yaxis_title="",
            margin=dict(
                l=10,
                r=20,
                t=20,
                b=10
            )
        )

        chart.update_yaxes(
            categoryorder="total ascending"
        )

        st.plotly_chart(
            chart,
            use_container_width=True
        )

    else:

        st.info(
            "Add project costs in the Cost Estimator to "
            "generate analytics."
        )

    left, right = st.columns(2)

    with left:

        st.markdown(
            """
            <div class="section-title">
                Category summary
            </div>
            """,
            unsafe_allow_html=True
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
            }
        )

    with right:

        st.markdown(
            """
            <div class="section-title">
                Markup summary
            </div>
            """,
            unsafe_allow_html=True
        )

        markup_df = pd.DataFrame(
            {
                "Cost": [
                    "Direct Cost",
                    "Contingency",
                    "Overhead",
                    "Profit",
                    "Estimated Total"
                ],
                "Amount": [
                    direct_cost,
                    contingency_cost,
                    overhead_cost,
                    profit_cost,
                    grand_total
                ]
            }
        )

        st.dataframe(
            markup_df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Amount":
                    st.column_config.NumberColumn(
                        format="$%.2f"
                    )
            }
        )

    footer()


# ============================================================
# PROJECT INFORMATION
# ============================================================

elif st.session_state.page == "Project Information":

    page_header(
        "Project Information",
        "Keep the basic information associated with your "
        "construction estimate organized in one place."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.session_state.project_name = st.text_input(
            "Project name",
            value=st.session_state.project_name
        )

        st.session_state.client = st.text_input(
            "Client",
            value=st.session_state.client
        )

    with col2:

        st.session_state.project_location = st.text_input(
            "Project location",
            value=st.session_state.project_location
        )

        project_types = [
            "Land Development",
            "Commercial",
            "Residential",
            "Infrastructure",
            "Transportation",
            "Utilities",
            "Other"
        ]

        current_type = (
            st.session_state.project_type
            if st.session_state.project_type in project_types
            else "Other"
        )

        st.session_state.project_type = st.selectbox(
            "Project type",
            project_types,
            index=project_types.index(
                current_type
            )
        )

    st.session_state.project_notes = st.text_area(
        "Project notes",
        value=st.session_state.project_notes,
        height=160,
        placeholder=(
            "Enter project scope, assumptions, estimate notes, "
            "or other important information..."
        )
    )

    st.success(
        "Project information is saved for your current session."
    )

    st.markdown(
        """
        <div class="section-title">
            Project snapshot
        </div>
        """,
        unsafe_allow_html=True
    )

    snapshot1, snapshot2, snapshot3 = st.columns(3)

    snapshot1.metric(
        "Estimated Cost",
        f"${grand_total:,.0f}"
    )

    snapshot2.metric(
        "Estimate Items",
        len(current_df)
    )

    snapshot3.metric(
        "Project Type",
        st.session_state.project_type
    )

    footer()


# ============================================================
# ABOUT
# ============================================================

elif st.session_state.page == "About BuildCost":

    page_header(
        "About BuildCost",
        "A simpler approach to early-stage construction cost planning."
    )

    st.markdown(
        """
        <div class="hero">

            <div class="hero-badge">
                OUR PURPOSE
            </div>

            <h1 style="font-size:3.4rem;">
                Better cost visibility.<br>
                Better project decisions.
            </h1>

            <p>
                BuildCost was created to make construction cost
                estimating more accessible, organized, and visual.
                The platform gives project teams a straightforward
                way to turn quantities and unit pricing into an
                understandable early-stage project estimate.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-number">MISSION</div>
                <h3>Simplify estimating</h3>
                <p>
                    Reduce the friction involved in organizing
                    quantities, unit pricing, and early project
                    cost assumptions.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-number">DESIGN</div>
                <h3>Make costs understandable</h3>
                <p>
                    Transform rows of cost information into
                    summaries and visualizations that are easier
                    to interpret.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-number">FUTURE</div>
                <h3>Build a smarter platform</h3>
                <p>
                    Expand into saved projects, location-based
                    pricing, labor and equipment breakdowns,
                    and professional reporting.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="section-title">
            Built with
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "**Python** · **Streamlit** · **Pandas** · "
        "**Plotly** · **GitHub**"
    )

    footer()


# ============================================================
# CONTACT
# ============================================================

elif st.session_state.page == "Contact":

    page_header(
        "Contact BuildCost",
        "Have feedback, questions, or an idea for BuildCost? "
        "Send us a message."
    )

    left, right = st.columns(
        [1.25, 0.75]
    )

    with left:

        st.markdown(
            """
            <div class="section-title">
                Let's talk construction.
            </div>

            <div class="section-subtitle">
                Tell us what you're interested in and we'll prepare
                your message.
            </div>
            """,
            unsafe_allow_html=True
        )

        contact_name = st.text_input(
            "Name"
        )

        contact_email = st.text_input(
            "Email"
        )

        contact_topic = st.selectbox(
            "I'm contacting BuildCost about",
            [
                "General Question",
                "Product Feedback",
                "Feature Request",
                "Collaboration",
                "Technical Issue",
                "Other"
            ]
        )

        contact_message = st.text_area(
            "Message",
            height=180,
            placeholder="How can we help?"
        )

        if st.button(
            "Prepare Message →",
            type="primary"
        ):

            if (
                not contact_name.strip()
                or
                not contact_email.strip()
                or
                not contact_message.strip()
            ):

                st.warning(
                    "Please enter your name, email, and message."
                )

            else:

                subject = quote(
                    f"BuildCost - {contact_topic}"
                )

                body = quote(
                    f"""
Name: {contact_name}
Email: {contact_email}
Topic: {contact_topic}

Message:
{contact_message}
                    """.strip()
                )

                mailto_link = (
                    f"mailto:{CONTACT_EMAIL}"
                    f"?subject={subject}"
                    f"&body={body}"
                )

                st.success(
                    "Your message is ready."
                )

                st.markdown(
                    f"""
                    <a href="{mailto_link}">
                        Open your email app to send the message
                    </a>
                    """,
                    unsafe_allow_html=True
                )

    with right:

        st.markdown(
            """
            <div class="info-card">
                <h3>BuildCost</h3>
                <p>
                    Construction cost intelligence for contractors,
                    engineers, developers, and project teams.
                </p>
            </div>

            <div class="info-card">
                <h3>Product feedback</h3>
                <p>
                    Have an idea that could improve estimating,
                    analytics, reporting, or project workflows?
                    We'd like to hear it.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    footer()
