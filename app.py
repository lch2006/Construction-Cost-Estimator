import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote


# ============================================================
# BUILDCOST
# Construction Cost Intelligence
# ============================================================

st.set_page_config(
    page_title="BuildCost | Construction Cost Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SETTINGS
# ============================================================

# CHANGE THIS TO YOUR EMAIL
CONTACT_EMAIL = "lchen07@vt.edu"

PAGES = [
    "Home",
    "Cost Estimator",
    "Cost Analytics",
    "Project Information",
    "About BuildCost",
    "Contact",
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


# ============================================================
# WEBSITE DESIGN
# ============================================================

st.markdown(
    """
<style>

:root {
    --navy: #0F172A;
    --navy2: #1E293B;
    --slate: #64748B;
    --border: #E2E8F0;
    --background: #F8FAFC;
    --orange: #F97316;
    --orange-dark: #EA580C;
}


/* ---------------------------------------------------------
   MAIN WEBSITE
--------------------------------------------------------- */

.stApp {
    background: var(--background);
}

.block-container {
    max-width: 1420px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}

[data-testid="stHeader"] {
    background: rgba(248, 250, 252, 0.94);
}


/* ---------------------------------------------------------
   PULL-OUT SIDEBAR
--------------------------------------------------------- */

[data-testid="stSidebar"] {
    background: var(--navy);
    border-right: 1px solid #243047;
}

[data-testid="stSidebar"] hr {
    border-color: #334155;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #CBD5E1;
}


/* All sidebar navigation buttons */

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 48px;

    border-radius: 12px;

    font-weight: 700;

    justify-content: flex-start;

    padding-left: 16px;

    transition: 0.18s ease;
}


/* Non-selected sidebar buttons */

[data-testid="stSidebar"]
.stButton > button[kind="secondary"] {

    background: #1E293B !important;

    border:
        1px solid
        #334155 !important;

    color:
        #FFFFFF !important;
}

[data-testid="stSidebar"]
.stButton > button[kind="secondary"] * {

    color:
        #FFFFFF !important;
}


/* Hover */

[data-testid="stSidebar"]
.stButton > button[kind="secondary"]:hover {

    background:
        #334155 !important;

    border-color:
        #F97316 !important;

    color:
        #FFFFFF !important;
}


/* Selected page */

[data-testid="stSidebar"]
.stButton > button[kind="primary"] {

    background:
        #F97316 !important;

    border:
        1px solid
        #F97316 !important;

    color:
        #FFFFFF !important;
}

[data-testid="stSidebar"]
.stButton > button[kind="primary"] * {

    color:
        #FFFFFF !important;
}


/* Selected page hover */

[data-testid="stSidebar"]
.stButton > button[kind="primary"]:hover {

    background:
        #EA580C !important;

    border-color:
        #EA580C !important;
}


/* ---------------------------------------------------------
   HOME HERO
--------------------------------------------------------- */

.hero {

    padding:
        72px 60px;

    border-radius:
        26px;

    background:
        radial-gradient(
            circle at 88% 12%,
            rgba(249, 115, 22, 0.28),
            transparent 27%
        ),
        linear-gradient(
            135deg,
            #0F172A 0%,
            #172033 55%,
            #1E293B 100%
        );

    color:
        white;

    margin-bottom:
        26px;

    box-shadow:
        0 22px 48px
        rgba(15, 23, 42, 0.13);
}


.hero-badge {

    display:
        inline-block;

    padding:
        7px 13px;

    border-radius:
        999px;

    background:
        rgba(249, 115, 22, 0.14);

    border:
        1px solid
        rgba(249, 115, 22, 0.45);

    color:
        #FDBA74;

    font-size:
        0.78rem;

    font-weight:
        800;

    letter-spacing:
        0.08em;

    margin-bottom:
        20px;
}


.hero h1 {

    margin:
        0;

    font-size:
        clamp(
            2.7rem,
            6vw,
            5rem
        );

    line-height:
        1;

    letter-spacing:
        -0.05em;
}


.hero p {

    max-width:
        790px;

    margin:
        22px 0 0;

    color:
        #CBD5E1;

    font-size:
        1.1rem;

    line-height:
        1.7;
}


/* ---------------------------------------------------------
   PAGE HEADERS
--------------------------------------------------------- */

.page-header {

    padding:
        34px 38px;

    border-radius:
        22px;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #1E293B
        );

    color:
        white;

    margin-bottom:
        28px;
}


.page-header h1 {

    margin:
        0;

    font-size:
        2.35rem;

    letter-spacing:
        -0.035em;
}


.page-header p {

    margin:
        9px 0 0;

    color:
        #CBD5E1;

    max-width:
        840px;

    line-height:
        1.6;
}


/* ---------------------------------------------------------
   SECTIONS
--------------------------------------------------------- */

.section-title {

    margin-top:
        30px;

    margin-bottom:
        5px;

    color:
        #0F172A;

    font-size:
        1.9rem;

    font-weight:
        800;

    letter-spacing:
        -0.035em;
}


.section-subtitle {

    color:
        #64748B;

    margin-bottom:
        22px;
}


/* ---------------------------------------------------------
   CARDS
--------------------------------------------------------- */

.feature-card,
.info-card {

    padding:
        28px;

    background:
        white;

    border:
        1px solid
        #E2E8F0;

    border-radius:
        20px;

    box-shadow:
        0 7px 24px
        rgba(15, 23, 42, 0.05);

    margin-bottom:
        16px;
}


.feature-card {

    min-height:
        215px;
}


.feature-card .label {

    color:
        #F97316;

    font-size:
        0.78rem;

    font-weight:
        800;

    letter-spacing:
        0.09em;
}


.feature-card h3,
.info-card h3 {

    color:
        #0F172A;

    margin:
        14px 0 9px;

    font-size:
        1.35rem;
}


.feature-card p,
.info-card p {

    color:
        #64748B;

    line-height:
        1.65;

    margin:
        0;
}


.callout {

    padding:
        24px 28px;

    border-radius:
        18px;

    background:
        #FFF7ED;

    border:
        1px solid
        #FED7AA;

    margin-top:
        18px;

    color:
        #7C2D12;
}


/* ---------------------------------------------------------
   METRIC CARDS
--------------------------------------------------------- */

[data-testid="stMetric"] {

    background:
        white;

    border:
        1px solid
        #E2E8F0;

    padding:
        21px;

    border-radius:
        18px;

    box-shadow:
        0 5px 18px
        rgba(15, 23, 42, 0.04);
}


/* ---------------------------------------------------------
   NORMAL BUTTONS
--------------------------------------------------------- */

.stButton > button,
.stDownloadButton > button {

    min-height:
        46px;

    border-radius:
        12px;

    font-weight:
        700;
}


.stButton > button[kind="primary"] {

    background:
        #F97316;

    border-color:
        #F97316;

    color:
        white;
}


.stButton > button[kind="primary"]:hover {

    background:
        #EA580C;

    border-color:
        #EA580C;
}


.stDownloadButton > button {

    background:
        #0F172A;

    border-color:
        #0F172A;

    color:
        white;
}


/* ---------------------------------------------------------
   FOOTER
--------------------------------------------------------- */

.footer {

    margin-top:
        55px;

    padding-top:
        22px;

    border-top:
        1px solid
        #E2E8F0;

    color:
        #94A3B8;

    font-size:
        0.86rem;
}


/* ---------------------------------------------------------
   MOBILE
--------------------------------------------------------- */

@media (max-width: 800px) {

    .hero {
        padding:
            48px 28px;
    }

    .page-header {
        padding:
            28px 24px;
    }

}

</style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DEFAULT ESTIMATE
# ============================================================

def create_default_estimate():

    return pd.DataFrame(
        [
            [
                "Earthwork",
                "Excavation",
                800.0,
                "CY",
                12.50,
            ],

            [
                "Concrete",
                "Concrete",
                120.0,
                "CY",
                165.00,
            ],

            [
                "Paving",
                "Asphalt",
                500.0,
                "TON",
                95.00,
            ],

            [
                "Utilities",
                "Storm Pipe",
                600.0,
                "LF",
                42.00,
            ],

            [
                "Utilities",
                "Sanitary Sewer Pipe",
                350.0,
                "LF",
                55.00,
            ],

            [
                "Site",
                "Curb & Gutter",
                900.0,
                "LF",
                24.00,
            ],
        ],

        columns=[
            "Category",
            "Item",
            "Quantity",
            "Unit",
            "Unit Cost ($)",
        ],
    )


# ============================================================
# SESSION STATE
# ============================================================

STATE_DEFAULTS = {

    "page":
        "Home",

    "project_name":
        "Residential Site Development",

    "client":
        "Example Client",

    "project_location":
        "Blacksburg, VA",

    "project_type":
        "Land Development",

    "project_notes":
        "",

    "contingency":
        10.0,

    "overhead":
        5.0,

    "profit":
        8.0,
}


for key, value in STATE_DEFAULTS.items():

    if key not in st.session_state:

        st.session_state[key] = value


if "estimate_data" not in st.session_state:

    st.session_state.estimate_data = (
        create_default_estimate()
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def set_page(page_name):

    st.session_state.page = page_name


def clean_estimate(data):

    required_columns = [
        "Category",
        "Item",
        "Quantity",
        "Unit",
        "Unit Cost ($)",
    ]


    df = pd.DataFrame(
        data
    ).copy()


    for column in required_columns:

        if column not in df.columns:

            if column in [
                "Quantity",
                "Unit Cost ($)",
            ]:

                df[column] = 0.0

            else:

                df[column] = ""


    df = df[
        required_columns
    ]


    for column in [
        "Category",
        "Item",
        "Unit",
    ]:

        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
        )


    for column in [
        "Quantity",
        "Unit Cost ($)",
    ]:

        df[column] = (
            pd.to_numeric(
                df[column],
                errors="coerce",
            )
            .fillna(0.0)
        )


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

        float(
            st.session_state.contingency
        )

        /

        100.0
    )


    overhead_cost = (

        direct_cost

        *

        float(
            st.session_state.overhead
        )

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

        float(
            st.session_state.profit
        )

        /

        100.0
    )


    grand_total = (

        subtotal

        +

        profit_cost
    )


    return (
        direct_cost,
        contingency_cost,
        overhead_cost,
        profit_cost,
        grand_total,
    )


def show_page_header(
    title,
    description,
):

    html = (

        '<div class="page-header">'

        f'<h1>{title}</h1>'

        f'<p>{description}</p>'

        '</div>'
    )


    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def show_section(
    title,
    subtitle=None,
):

    html = (

        '<div class="section-title">'

        f'{title}'

        '</div>'
    )


    if subtitle:

        html += (

            '<div class="section-subtitle">'

            f'{subtitle}'

            '</div>'
        )


    st.markdown(
        html,
        unsafe_allow_html=True,
    )


def show_footer():

    st.markdown(

        '<div class="footer">'

        '<strong>'
        'BuildCost'
        '</strong>'

        ' • Construction Cost Intelligence'

        '<br>'

        'Estimates are planning tools. '
        'Verify quantities, unit costs, scope, '
        'location, and date before using them '
        'for project decisions.'

        '</div>',

        unsafe_allow_html=True,
    )


# ============================================================
# PULL-OUT NAVIGATION MENU
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


    for page_name in PAGES:

        if (
            st.session_state.page
            ==
            page_name
        ):

            button_type = "primary"

        else:

            button_type = "secondary"


        st.button(

            page_name,

            key=
                f"nav_{page_name}",

            type=
                button_type,

            use_container_width=
                True,

            on_click=
                set_page,

            args=
                (page_name,),
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
        "BuildCost v6.0"
    )


# ============================================================
# CURRENT PROJECT COSTS
# ============================================================

page = (
    st.session_state.page
)


current_df = clean_estimate(
    st.session_state.estimate_data
)


(
    direct_cost,
    contingency_cost,
    overhead_cost,
    profit_cost,
    grand_total,
) = calculate_costs(
    current_df
)


# ============================================================
# HOME PAGE
# ============================================================

if page == "Home":

    hero_html = (

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

        'BuildCost is a construction cost planning '
        'platform for contractors, engineers, '
        'developers, and project teams. '

        'Create estimates, organize quantities and '
        'unit prices, analyze where project money '
        'is being spent, and understand early-stage '
        'construction costs in one clear workspace.'

        '</p>'

        '</div>'
    )


    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )


    button1, button2, spacer = (
        st.columns(
            [
                1.25,
                1.25,
                4,
            ]
        )
    )


    with button1:

        st.button(

            "Create an Estimate →",

            type=
                "primary",

            use_container_width=
                True,

            on_click=
                set_page,

            args=
                ("Cost Estimator",),

            key=
                "home_create_estimate",
        )


    with button2:

        st.button(

            "Learn About BuildCost",

            use_container_width=
                True,

            on_click=
                set_page,

            args=
                ("About BuildCost",),

            key=
                "home_about_buildcost",
        )


    show_section(

        "From quantities to project cost.",

        "A streamlined workflow for "
        "early construction cost planning.",
    )


    c1, c2, c3 = (
        st.columns(
            3
        )
    )


    with c1:

        st.markdown(

            '<div class="feature-card">'

            '<div class="label">'
            '01 — ESTIMATE'
            '</div>'

            '<h3>'
            'Build your estimate'
            '</h3>'

            '<p>'
            'Enter construction activities, '
            'quantities, units, and unit pricing '
            'in an editable project estimate.'
            '</p>'

            '</div>',

            unsafe_allow_html=True,
        )


    with c2:

        st.markdown(

            '<div class="feature-card">'

            '<div class="label">'
            '02 — ANALYZE'
            '</div>'

            '<h3>'
            'Understand project costs'
            '</h3>'

            '<p>'
            'See which construction categories '
            'drive your project cost using '
            'visual analytics and project metrics.'
            '</p>'

            '</div>',

            unsafe_allow_html=True,
        )


    with c3:

        st.markdown(

            '<div class="feature-card">'

            '<div class="label">'
            '03 — EXPORT'
            '</div>'

            '<h3>'
            'Take your estimate with you'
            '</h3>'

            '<p>'
            'Export organized estimate data '
            'for documentation, additional '
            'analysis, and project planning.'
            '</p>'

            '</div>',

            unsafe_allow_html=True,
        )


    show_section(
        "Current project snapshot"
    )


    m1, m2, m3, m4 = (
        st.columns(
            4
        )
    )


    m1.metric(
        "Estimated Total",
        f"${grand_total:,.0f}",
    )


    m2.metric(
        "Direct Cost",
        f"${direct_cost:,.0f}",
    )


    m3.metric(
        "Estimate Items",
        len(current_df),
    )


    category_count = (

        current_df[
            "Category"
        ]

        .replace(
            "",
            pd.NA,
        )

        .dropna()

        .nunique()
    )


    m4.metric(
        "Categories",
        category_count,
    )


    show_footer()


# ============================================================
# COST ESTIMATOR
# ============================================================

elif page == "Cost Estimator":

    show_page_header(

        "Cost Estimator",

        "Build an early-stage project estimate "
        "using construction quantities, units, "
        "unit pricing, contingency, overhead, "
        "and profit.",
    )


    show_section(

        "Project markups",

        "Adjust the percentages applied "
        "to your project estimate.",
    )


    markup1, markup2, markup3 = (
        st.columns(
            3
        )
    )


    with markup1:

        st.number_input(

            "Contingency (%)",

            min_value=
                0.0,

            max_value=
                100.0,

            step=
                0.5,

            key=
                "contingency",
        )


    with markup2:

        st.number_input(

            "Overhead (%)",

            min_value=
                0.0,

            max_value=
                100.0,

            step=
                0.5,

            key=
                "overhead",
        )


    with markup3:

        st.number_input(

            "Profit (%)",

            min_value=
                0.0,

            max_value=
                100.0,

            step=
                0.5,

            key=
                "profit",
        )


    show_section(

        "Estimate items",

        "Edit existing rows or add your "
        "own construction activities.",
    )


    edited_df = st.data_editor(

        st.session_state.estimate_data,

        num_rows=
            "dynamic",

        hide_index=
            True,

        use_container_width=
            True,

        key=
            "estimate_editor",

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

                    min_value=
                        0.0,

                    format=
                        "%.2f",
                ),

            "Unit":
                st.column_config.TextColumn(
                    "Unit"
                ),

            "Unit Cost ($)":
                st.column_config.NumberColumn(

                    "Unit Cost ($)",

                    min_value=
                        0.0,

                    format=
                        "$%.2f",
                ),
        },
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
                "Unit Cost ($)",
            ]
        ]

        .copy()
    )


    (
        direct_cost,
        contingency_cost,
        overhead_cost,
        profit_cost,
        grand_total,
    ) = calculate_costs(
        estimate_df
    )


    show_section(
        "Estimate summary"
    )


    m1, m2, m3, m4 = (
        st.columns(
            4
        )
    )


    m1.metric(

        "Direct Cost",

        f"${direct_cost:,.2f}",
    )


    m2.metric(

        "Contingency",

        f"${contingency_cost:,.2f}",

        f"{st.session_state.contingency:.1f}%",
    )


    m3.metric(

        "Overhead",

        f"${overhead_cost:,.2f}",

        f"{st.session_state.overhead:.1f}%",
    )


    m4.metric(

        "Project Total",

        f"${grand_total:,.2f}",
    )


    st.markdown(
        "#### Detailed Estimate"
    )


    st.dataframe(

        estimate_df,

        hide_index=
            True,

        use_container_width=
            True,

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


    csv_data = (

        estimate_df

        .to_csv(
            index=False
        )

        .encode(
            "utf-8"
        )
    )


    export_col, spacer = (
        st.columns(
            [
                1.4,
                4,
            ]
        )
    )


    with export_col:

        st.download_button(

            "⬇ Download Estimate CSV",

            data=
                csv_data,

            file_name=
                "BuildCost_Estimate.csv",

            mime=
                "text/csv",

            use_container_width=
                True,
        )


    show_footer()


# ============================================================
# COST ANALYTICS
# ============================================================

elif page == "Cost Analytics":

    show_page_header(

        "Cost Analytics",

        "See where project money is being spent "
        "and identify the categories driving "
        "your construction estimate.",
    )


    analytics_df = clean_estimate(
        st.session_state.estimate_data
    )


    (
        direct_cost,
        contingency_cost,
        overhead_cost,
        profit_cost,
        grand_total,
    ) = calculate_costs(
        analytics_df
    )


    category_df = (
        analytics_df.copy()
    )


    category_df["Category"] = (

        category_df["Category"]

        .replace(
            "",
            "Uncategorized",
        )
    )


    category_df = (

        category_df

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


    if not category_df.empty:

        largest_category = (
            category_df.iloc[0]["Category"]
        )

    else:

        largest_category = "N/A"


    if not analytics_df.empty:

        average_cost = float(
            analytics_df["Total Cost"].mean()
        )

    else:

        average_cost = 0.0


    a1, a2, a3, a4 = (
        st.columns(
            4
        )
    )


    a1.metric(

        "Project Total",

        f"${grand_total:,.0f}",
    )


    a2.metric(

        "Largest Category",

        largest_category,
    )


    a3.metric(

        "Cost Items",

        len(
            analytics_df
        ),
    )


    a4.metric(

        "Average Item Cost",

        f"${average_cost:,.0f}",
    )


    show_section(

        "Cost by category",

        "Compare the direct cost of "
        "each construction category.",
    )


    if (
        direct_cost > 0
        and
        not category_df.empty
    ):

        fig = px.bar(

            category_df,

            x=
                "Total Cost",

            y=
                "Category",

            orientation=
                "h",

            text_auto=
                ".2s",
        )


        fig.update_layout(

            height=
                470,

            xaxis_title=
                "Cost ($)",

            yaxis_title=
                "",

            margin=
                dict(
                    l=10,
                    r=20,
                    t=20,
                    b=10,
                ),
        )


        fig.update_yaxes(

            categoryorder=
                "total ascending"
        )


        st.plotly_chart(

            fig,

            use_container_width=
                True,
        )


    else:

        st.info(

            "Enter quantities and unit costs "
            "in the Cost Estimator to "
            "generate analytics."
        )


        st.button(

            "Go to Cost Estimator →",

            type=
                "primary",

            on_click=
                set_page,

            args=
                ("Cost Estimator",),

            key=
                "analytics_go_estimator",
        )


    summary1, summary2 = (
        st.columns(
            2
        )
    )


    with summary1:

        st.markdown(
            "#### Category Summary"
        )


        st.dataframe(

            category_df,

            hide_index=
                True,

            use_container_width=
                True,

            column_config={

                "Total Cost":
                    st.column_config.NumberColumn(
                        format="$%.2f"
                    )
            },
        )


    with summary2:

        st.markdown(
            "#### Project Cost Summary"
        )


        cost_summary = (
            pd.DataFrame(
                {
                    "Description": [

                        "Direct Cost",

                        "Contingency",

                        "Overhead",

                        "Profit",

                        "Estimated Total",
                    ],

                    "Amount": [

                        direct_cost,

                        contingency_cost,

                        overhead_cost,

                        profit_cost,

                        grand_total,
                    ],
                }
            )
        )


        st.dataframe(

            cost_summary,

            hide_index=
                True,

            use_container_width=
                True,

            column_config={

                "Amount":
                    st.column_config.NumberColumn(
                        format="$%.2f"
                    )
            },
        )


    show_footer()


# ============================================================
# PROJECT INFORMATION
# ============================================================

elif page == "Project Information":

    show_page_header(

        "Project Information",

        "Keep the information associated "
        "with your construction estimate "
        "organized in one place.",
    )


    left, right = (
        st.columns(
            2
        )
    )


    with left:

        st.text_input(

            "Project name",

            key=
                "project_name",
        )


        st.text_input(

            "Client",

            key=
                "client",
        )


    with right:

        st.text_input(

            "Project location",

            key=
                "project_location",
        )


        st.selectbox(

            "Project type",

            PROJECT_TYPES,

            key=
                "project_type",
        )


    st.text_area(

        "Project notes",

        key=
            "project_notes",

        height=
            170,

        placeholder=
            "Enter project scope, assumptions, "
            "estimate notes, or other important "
            "information...",
    )


    st.info(

        "Project information is kept "
        "for the current app session."
    )


    show_section(
        "Project snapshot"
    )


    project_df = clean_estimate(
        st.session_state.estimate_data
    )


    (
        _direct,
        _contingency,
        _overhead,
        _profit,
        project_total,
    ) = calculate_costs(
        project_df
    )


    p1, p2, p3 = (
        st.columns(
            3
        )
    )


    p1.metric(

        "Estimated Cost",

        f"${project_total:,.0f}",
    )


    p2.metric(

        "Estimate Items",

        len(
            project_df
        ),
    )


    p3.metric(

        "Project Type",

        st.session_state.project_type,
    )


    show_footer()


# ============================================================
# ABOUT BUILDCOST
# ============================================================

elif page == "About BuildCost":

    show_page_header(

        "About BuildCost",

        "A simpler approach to "
        "early-stage construction "
        "cost planning.",
    )


    about_html = (

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

        'BuildCost was created to make '
        'construction cost estimating easier '
        'to organize and understand. '

        'The platform turns project quantities '
        'and unit pricing into useful '
        'early-stage cost information.'

        '</p>'

        '</div>'
    )


    st.markdown(

        about_html,

        unsafe_allow_html=
            True,
    )


    c1, c2, c3 = (
        st.columns(
            3
        )
    )


    with c1:

        st.markdown(

            '<div class="feature-card">'

            '<div class="label">'
            'MISSION'
            '</div>'

            '<h3>'
            'Simplify estimating'
            '</h3>'

            '<p>'
            'Make it easier to organize '
            'construction quantities, '
            'unit pricing, and project '
            'cost assumptions.'
            '</p>'

            '</div>',

            unsafe_allow_html=True,
        )


    with c2:

        st.markdown(

            '<div class="feature-card">'

            '<div class="label">'
            'INSIGHT'
            '</div>'

            '<h3>'
            'Make costs understandable'
            '</h3>'

            '<p>'
            'Turn cost information into '
            'useful project metrics, '
            'summaries, and visualizations.'
            '</p>'

            '</div>',

            unsafe_allow_html=True,
        )


    with c3:

        st.markdown(

            '<div class="feature-card">'

            '<div class="label">'
            'FUTURE'
            '</div>'

            '<h3>'
            'Grow the platform'
            '</h3>'

            '<p>'
            'Expand into saved projects, '
            'location-based pricing, labor '
            'and equipment costs, and '
            'professional reports.'
            '</p>'

            '</div>',

            unsafe_allow_html=True,
        )


    show_section(
        "Technology"
    )


    st.write(

        "**Python** · "
        "**Streamlit** · "
        "**Pandas** · "
        "**Plotly** · "
        "**GitHub**"
    )


    st.markdown(

        '<div class="callout">'

        '<strong>'

        'BuildCost is currently an '
        'early-stage estimating tool.'

        '</strong> '

        'Future versions can add saved accounts, '
        'regional pricing databases, '
        'labor/material/equipment breakdowns, '
        'and professional reports.'

        '</div>',

        unsafe_allow_html=True,
    )


    show_footer()


# ============================================================
# CONTACT
# ============================================================

elif page == "Contact":

    show_page_header(

        "Contact BuildCost",

        "Questions, product feedback, "
        "feature ideas, or collaboration "
        "opportunities.",
    )


    left, right = (
        st.columns(
            [
                1.3,
                0.7,
            ]
        )
    )


    with left:

        show_section(

            "Let's talk construction.",

            "Choose what you want to "
            "discuss and prepare an email.",
        )


        with st.form(
            "contact_form",
            clear_on_submit=False,
        ):

            contact_name = (
                st.text_input(
                    "Name"
                )
            )


            contact_email = (
                st.text_input(
                    "Email"
                )
            )


            contact_topic = (
                st.selectbox(

                    "What would you like to discuss?",

                    [
                        "General Question",

                        "Product Feedback",

                        "Feature Request",

                        "Collaboration",

                        "Technical Issue",

                        "Other",
                    ],
                )
            )


            contact_message = (
                st.text_area(

                    "Message",

                    height=
                        180,

                    placeholder=
                        "How can we help?",
                )
            )


            submitted = (
                st.form_submit_button(

                    "Prepare Email →",

                    use_container_width=
                        True,
                )
            )


        if submitted:

            if (

                not contact_name.strip()

                or

                not contact_email.strip()

                or

                not contact_message.strip()
            ):

                st.warning(

                    "Please enter your name, "
                    "email, and message."
                )


            elif (
                CONTACT_EMAIL
                ==
                "your-email@example.com"
            ):

                st.warning(

                    "Replace CONTACT_EMAIL "
                    "near the top of app.py "
                    "with the email address "
                    "you want BuildCost "
                    "messages sent to."
                )


            else:

                subject = quote(

                    f"BuildCost - "
                    f"{contact_topic}"
                )


                body = quote(

                    f"Name: "
                    f"{contact_name}\n"

                    f"Email: "
                    f"{contact_email}\n"

                    f"Topic: "
                    f"{contact_topic}\n\n"

                    f"Message:\n"
                    f"{contact_message}"
                )


                mailto_url = (

                    f"mailto:"
                    f"{CONTACT_EMAIL}"

                    f"?subject="
                    f"{subject}"

                    f"&body="
                    f"{body}"
                )


                st.success(
                    "Your email is ready."
                )


                st.markdown(

                    f'<a href="{mailto_url}">'

                    'Open your email app '
                    'to send the message'

                    '</a>',

                    unsafe_allow_html=True,
                )


    with right:

        st.markdown(

            '<div class="info-card">'

            '<h3>'
            '🏗️ BuildCost'
            '</h3>'

            '<p>'
            'Construction cost intelligence '
            'designed for clearer early-stage '
            'project planning.'
            '</p>'

            '</div>',

            unsafe_allow_html=True,
        )


        st.markdown(

            '<div class="info-card">'

            '<h3>'
            'Product feedback'
            '</h3>'

            '<p>'
            'Have an idea for estimating, '
            'analytics, reporting, or another '
            'construction workflow? '
            'Send it our way.'
            '</p>'

            '</div>',

            unsafe_allow_html=True,
        )


    show_footer()
