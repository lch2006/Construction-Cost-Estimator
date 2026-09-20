import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote


# ============================================================
# BUILDCOST
# Construction Cost Intelligence
# ============================================================

st.set_page_config(
    page_title="BuildCost",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SETTINGS
# ============================================================

CONTACT_EMAIL = "your-email@example.com"

PAGES = [
    "Home",
    "Cost Estimator",
    "Cost Analytics",
    "Project Information",
    "About BuildCost",
    "Contact"
]


# ============================================================
# DESIGN
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #F8FAFC;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

[data-testid="stHeader"] {
    background-color: rgba(248, 250, 252, 0.95);
}

[data-testid="stSidebar"] {
    background-color: #0F172A;
}

[data-testid="stSidebar"] * {
    color: #F8FAFC;
}

[data-testid="stSidebar"] hr {
    border-color: #334155;
}

.hero {
    padding: 72px 60px;
    border-radius: 26px;
    background:
        radial-gradient(
            circle at 88% 12%,
            rgba(249, 115, 22, 0.25),
            transparent 26%
        ),
        linear-gradient(
            135deg,
            #0F172A 0%,
            #172033 55%,
            #1E293B 100%
        );
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 20px 45px rgba(15, 23, 42, 0.12);
}

.hero-badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background-color: rgba(249, 115, 22, 0.14);
    border: 1px solid rgba(249, 115, 22, 0.45);
    color: #FDBA74;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    margin-bottom: 20px;
}

.hero h1 {
    margin: 0;
    font-size: clamp(2.8rem, 6vw, 5rem);
    line-height: 1;
    letter-spacing: -0.05em;
}

.hero p {
    max-width: 760px;
    margin: 22px 0 0;
    color: #CBD5E1;
    font-size: 1.1rem;
    line-height: 1.7;
}

.page-header {
    padding: 34px 38px;
    border-radius: 22px;
    background-color: #0F172A;
    color: white;
    margin-bottom: 28px;
}

.page-header h1 {
    margin: 0;
    font-size: 2.35rem;
    letter-spacing: -0.035em;
}

.page-header p {
    margin: 9px 0 0;
    color: #CBD5E1;
    max-width: 820px;
    line-height: 1.6;
}

.section-title {
    margin-top: 30px;
    margin-bottom: 5px;
    color: #0F172A;
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -0.035em;
}

.section-subtitle {
    color: #64748B;
    margin-bottom: 22px;
}

.feature-card {
    min-height: 215px;
    padding: 28px;
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 20px;
    box-shadow: 0 7px 24px rgba(15, 23, 42, 0.05);
    margin-bottom: 16px;
}

.feature-card .label {
    color: #F97316;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.09em;
}

.feature-card h3 {
    color: #0F172A;
    margin: 14px 0 9px;
    font-size: 1.35rem;
}

.feature-card p {
    color: #64748B;
    line-height: 1.65;
    margin: 0;
}

.info-card {
    padding: 26px;
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
    margin-bottom: 18px;
}

.info-card h3 {
    margin-top: 0;
    color: #0F172A;
}

.info-card p {
    color: #64748B;
    line-height: 1.65;
    margin-bottom: 0;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    padding: 21px;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
}

.stButton > button {
    min-height: 46px;
    border-radius: 12px;
    font-weight: 700;
}

.stButton > button[kind="primary"] {
    background-color: #F97316;
    border-color: #F97316;
    color: white;
}

.stDownloadButton > button {
    min-height: 46px;
    border-radius: 12px;
    font-weight: 700;
    background-color: #0F172A;
    border-color: #0F172A;
    color: white;
}

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


# ============================================================
# DEFAULT DATA
# ============================================================

def create_default_estimate():

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


# ============================================================
# INITIALIZE SESSION DATA
# ============================================================

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

if "estimate_data" not in st.session_state:
    st.session_state.estimate_data = create_default_estimate()

if "navigation" not in st.session_state:
    st.session_state.navigation = "Home"


# ============================================================
# FUNCTIONS
# ============================================================

def clean_estimate(data):

    df = pd.DataFrame(data).copy()

    columns = [
        "Category",
        "Item",
        "Quantity",
        "Unit",
        "Unit Cost ($)"
    ]

    for column in columns:

        if column not in df.columns:

            if column in ["Quantity", "Unit Cost ($)"]:
                df[column] = 0.0

            else:
                df[column] = ""

    df = df[columns]

    for column in [
        "Category",
        "Item",
        "Unit"
    ]:

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
        )

    for column in [
        "Quantity",
        "Unit Cost ($)"
    ]:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0.0)

    df["Total Cost"] = (
        df["Quantity"]
        *
        df["Unit Cost ($)"]
    )

    return df


def calculate_costs(df):

    direct_cost = float(
        df["Total Cost"].sum()
    )

    contingency_cost = (
        direct_cost
        *
        float(st.session_state.contingency)
        /
        100.0
    )

    overhead_cost = (
        direct_cost
        *
        float(st.session_state.overhead)
        /
        100.0
    )

    subtotal = (
        direct_cost
        +
        contingency_cost
        +
        overhead_cost
    )

    profit_cost = (
        subtotal
        *
        float(st.session_state.profit)
        /
        100.0
    )

    total_cost = (
        subtotal
        +
        profit_cost
    )

    return (
        direct_cost,
        contingency_cost,
        overhead_cost,
        profit_cost,
        total_cost
    )


def show_page_header(title, description):

    html = (
        '<div class="page-header">'
        f'<h1>{title}</h1>'
        f'<p>{description}</p>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def show_section(title, subtitle=None):

    html = (
        f'<div class="section-title">{title}</div>'
    )

    if subtitle:

        html += (
            f'<div class="section-subtitle">'
            f'{subtitle}'
            f'</div>'
        )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def show_footer():

    st.markdown(
        '<div class="footer">'
        '<strong>BuildCost</strong> • Construction Cost Intelligence'
        '<br>'
        'Unit costs and estimates should be verified for the '
        'specific project, location, scope, and date.'
        '</div>',
        unsafe_allow_html=True
    )


def go_to(page_name):

    st.session_state.navigation = page_name


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
        '<div style="font-size:1.65rem;'
        'font-weight:900;margin-top:8px;">'
        '🏗️ BUILDCOST'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "CONSTRUCTION COST INTELLIGENCE"
    )

    st.divider()

    st.radio(
        "Navigation",
        PAGES,
        key="navigation",
        label_visibility="collapsed"
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
        "BuildCost v3.0"
    )


# ============================================================
# CURRENT DATA / CALCULATIONS
# ============================================================

page = st.session_state.navigation

current_df = clean_estimate(
    st.session_state.estimate_data
)

(
    direct_cost,
    contingency_cost,
    overhead_cost,
    profit_cost,
    grand_total
) = calculate_costs(
    current_df
)


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    hero = (
        '<div class="hero">'
        '<div class="hero-badge">'
        'CONSTRUCTION COST INTELLIGENCE'
        '</div>'
        '<h1>'
        'Build smarter.'
        '<br>'
        '<span style="color:#FB923C;">'
        'Estimate faster.'
        '</span>'
        '</h1>'
        '<p>'
        'BuildCost is a construction cost planning platform '
        'designed for contractors, engineers, developers, and '
        'project teams. Build estimates, organize quantities and '
        'unit prices, analyze project spending, and understand '
        'early-stage construction costs in one workspace.'
        '</p>'
        '</div>'
    )

    st.markdown(
        hero,
        unsafe_allow_html=True
    )

    button1, button2, empty = st.columns(
        [1.25, 1.15, 4]
    )

    with button1:

        if st.button(
            "Create an Estimate →",
            type="primary",
            use_container_width=True
        ):

            go_to("Cost Estimator")
            st.rerun()

    with button2:

        if st.button(
            "Learn About BuildCost",
            use_container_width=True
        ):

            go_to("About BuildCost")
            st.rerun()

    show_section(
        "From quantities to project cost.",
        "A streamlined workflow for early construction cost planning."
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            '<div class="feature-card">'
            '<div class="label">01 — ESTIMATE</div>'
            '<h3>Build your estimate</h3>'
            '<p>'
            'Enter construction activities, quantities, units, '
            'and unit pricing using an editable project estimate.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            '<div class="feature-card">'
            '<div class="label">02 — ANALYZE</div>'
            '<h3>Understand project costs</h3>'
            '<p>'
            'Identify the construction categories driving your '
            'project cost through visual analytics and summaries.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            '<div class="feature-card">'
            '<div class="label">03 — EXPORT</div>'
            '<h3>Take your estimate with you</h3>'
            '<p>'
            'Export your estimate as organized data for '
            'documentation, additional analysis, and planning.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    show_section(
        "Current project"
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
        "Estimate Items",
        len(current_df)
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

    show_footer()


# ============================================================
# COST ESTIMATOR
# ============================================================

elif page == "Cost Estimator":

    show_page_header(
        "Cost Estimator",
        "Build your project estimate using quantities, units, "
        "unit pricing, contingency, overhead, and profit."
    )

    show_section(
        "Project markups",
        "Adjust the percentages applied to the project estimate."
    )

    markup1, markup2, markup3 = st.columns(3)

    with markup1:

        contingency_input = st.number_input(
            "Contingency (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                st.session_state.contingency
            ),
            step=0.5
        )

    with markup2:

        overhead_input = st.number_input(
            "Overhead (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                st.session_state.overhead
            ),
            step=0.5
        )

    with markup3:

        profit_input = st.number_input(
            "Profit (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                st.session_state.profit
            ),
            step=0.5
        )

    st.session_state.contingency = contingency_input
    st.session_state.overhead = overhead_input
    st.session_state.profit = profit_input

    show_section(
        "Estimate items",
        "Edit the existing rows or add your own construction activities."
    )

    edited_df = st.data_editor(
        st.session_state.estimate_data,
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
        }
    )

    estimate_df = clean_estimate(
        edited_df
    )

    st.session_state.estimate_data = (
        estimate_df[
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
        estimate_df
    )

    show_section(
        "Estimate summary"
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

    st.markdown(
        "#### Detailed Estimate"
    )

    st.dataframe(
        estimate_df,
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

    csv_data = estimate_df.to_csv(
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

    show_footer()


# ============================================================
# COST ANALYTICS
# ============================================================

elif page == "Cost Analytics":

    show_page_header(
        "Cost Analytics",
        "See where project money is being spent and identify "
        "the categories driving your construction estimate."
    )

    analytics_df = clean_estimate(
        st.session_state.estimate_data
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

    category_df = analytics_df.copy()

    category_df["Category"] = (
        category_df["Category"]
        .replace(
            "",
            "Uncategorized"
        )
    )

    category_df = (
        category_df
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

    if len(category_df) > 0:
        largest_category = category_df.iloc[0]["Category"]

    else:
        largest_category = "N/A"

    if len(analytics_df) > 0:
        average_cost = float(
            analytics_df["Total Cost"].mean()
        )

    else:
        average_cost = 0.0

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
        f"${average_cost:,.0f}"
    )

    show_section(
        "Cost by category",
        "Compare the direct cost of each construction category."
    )

    if (
        direct_cost > 0
        and
        len(category_df) > 0
    ):

        fig = px.bar(
            category_df,
            x="Total Cost",
            y="Category",
            orientation="h",
            text_auto=".2s"
        )

        fig.update_layout(
            height=470,
            xaxis_title="Cost ($)",
            yaxis_title="",
            margin=dict(
                l=10,
                r=20,
                t=20,
                b=10
            )
        )

        fig.update_yaxes(
            categoryorder="total ascending"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Enter project costs in the Cost Estimator "
            "to generate analytics."
        )

    summary1, summary2 = st.columns(2)

    with summary1:

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
            }
        )

    with summary2:

        st.markdown(
            "#### Project Cost Summary"
        )

        cost_summary = pd.DataFrame(
            {
                "Description": [
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
            cost_summary,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Amount":
                    st.column_config.NumberColumn(
                        format="$%.2f"
                    )
            }
        )

    show_footer()


# ============================================================
# PROJECT INFORMATION
# ============================================================

elif page == "Project Information":

    show_page_header(
        "Project Information",
        "Organize the basic information associated with your "
        "construction estimate."
    )

    left, right = st.columns(2)

    with left:

        project_name_input = st.text_input(
            "Project name",
            value=st.session_state.project_name
        )

        client_input = st.text_input(
            "Client",
            value=st.session_state.client
        )

    with right:

        location_input = st.text_input(
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

        if st.session_state.project_type in project_types:
            type_index = project_types.index(
                st.session_state.project_type
            )

        else:
            type_index = 0

        type_input = st.selectbox(
            "Project type",
            project_types,
            index=type_index
        )

    notes_input = st.text_area(
        "Project notes",
        value=st.session_state.project_notes,
        height=170,
        placeholder=(
            "Enter project scope, assumptions, estimate notes, "
            "or other important information..."
        )
    )

    st.session_state.project_name = project_name_input
    st.session_state.client = client_input
    st.session_state.project_location = location_input
    st.session_state.project_type = type_input
    st.session_state.project_notes = notes_input

    st.success(
        "Project information is saved for this session."
    )

    show_section(
        "Project snapshot"
    )

    p1, p2, p3 = st.columns(3)

    p1.metric(
        "Estimated Cost",
        f"${grand_total:,.0f}"
    )

    p2.metric(
        "Estimate Items",
        len(current_df)
    )

    p3.metric(
        "Project Type",
        st.session_state.project_type
    )

    show_footer()


# ============================================================
# ABOUT BUILDCOST
# ============================================================

elif page == "About BuildCost":

    show_page_header(
        "About BuildCost",
        "A simpler approach to early-stage construction "
        "cost planning."
    )

    about_hero = (
        '<div class="hero">'
        '<div class="hero-badge">'
        'OUR PURPOSE'
        '</div>'
        '<h1 style="font-size:3.5rem;">'
        'Better cost visibility.'
        '<br>'
        '<span style="color:#FB923C;">'
        'Better project planning.'
        '</span>'
        '</h1>'
        '<p>'
        'BuildCost was created to make construction cost '
        'estimating easier to organize and understand. '
        'The platform turns project quantities and unit pricing '
        'into useful early-stage cost information.'
        '</p>'
        '</div>'
    )

    st.markdown(
        about_hero,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            '<div class="feature-card">'
            '<div class="label">MISSION</div>'
            '<h3>Simplify estimating</h3>'
            '<p>'
            'Make it easier to organize construction quantities, '
            'unit pricing, and project cost assumptions.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            '<div class="feature-card">'
            '<div class="label">INSIGHT</div>'
            '<h3>Make costs understandable</h3>'
            '<p>'
            'Turn cost information into useful project metrics, '
            'summaries, and visualizations.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            '<div class="feature-card">'
            '<div class="label">FUTURE</div>'
            '<h3>Grow the platform</h3>'
            '<p>'
            'Expand into saved projects, location-based pricing, '
            'labor and equipment costs, and professional reports.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    show_section(
        "Technology"
    )

    st.write(
        "**Python** · **Streamlit** · **Pandas** · "
        "**Plotly** · **GitHub**"
    )

    show_footer()


# ============================================================
# CONTACT
# ============================================================

elif page == "Contact":

    show_page_header(
        "Contact BuildCost",
        "Questions, product feedback, feature ideas, "
        "or collaboration opportunities."
    )

    left, right = st.columns(
        [1.3, 0.7]
    )

    with left:

        show_section(
            "Let's talk construction.",
            "Choose what you want to discuss and prepare a message."
        )

        contact_name = st.text_input(
            "Name"
        )

        contact_email = st.text_input(
            "Email"
        )

        contact_topic = st.selectbox(
            "What would you like to discuss?",
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

            elif CONTACT_EMAIL == "your-email@example.com":

                st.warning(
                    "Replace CONTACT_EMAIL at the top of app.py "
                    "with the email you want to use."
                )

            else:

                subject = quote(
                    f"BuildCost - {contact_topic}"
                )

                message_body = (
                    f"Name: {contact_name}\n"
                    f"Email: {contact_email}\n"
                    f"Topic: {contact_topic}\n\n"
                    f"Message:\n{contact_message}"
                )

                encoded_body = quote(
                    message_body
                )

                mailto_url = (
                    f"mailto:{CONTACT_EMAIL}"
                    f"?subject={subject}"
                    f"&body={encoded_body}"
                )

                st.success(
                    "Your message is ready."
                )

                st.markdown(
                    f'<a href="{mailto_url}">'
                    'Open your email app to send the message'
                    '</a>',
                    unsafe_allow_html=True
                )

    with right:

        st.markdown(
            '<div class="info-card">'
            '<h3>🏗️ BuildCost</h3>'
            '<p>'
            'Construction cost intelligence designed for '
            'clearer early-stage project planning.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="info-card">'
            '<h3>Product Feedback</h3>'
            '<p>'
            'Have an idea for estimating, analytics, reporting, '
            'or another construction workflow? Send it our way.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    show_footer()
