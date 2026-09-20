import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote


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
    "Scenario Comparison",
    "Cost Analytics",
    "Cost Library",
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


BASE_COLUMNS = [
    "Category",
    "Item",
    "Quantity",
    "Unit",
    "Unit Cost ($)",
]


# ============================================================
# WEBSITE DESIGN
# ============================================================

st.markdown(
    """
<style>

:root {
    --navy:#0F172A;
    --navy2:#1E293B;
    --slate:#64748B;
    --border:#E2E8F0;
    --background:#F8FAFC;
    --orange:#F97316;
    --orange-dark:#EA580C;
}


/* MAIN APP */

.stApp {
    background:var(--background);
}


.block-container {
    max-width:1420px;
    padding-top:1.4rem;
    padding-bottom:4rem;
}


[data-testid="stHeader"] {
    background:rgba(248,250,252,.94);
}


/* SIDEBAR */

[data-testid="stSidebar"] {
    background:var(--navy);
    border-right:1px solid #243047;
}


[data-testid="stSidebar"] hr {
    border-color:#334155;
}


[data-testid="stSidebar"]
[data-testid="stCaptionContainer"] {
    color:#CBD5E1;
}


/* ALL SIDEBAR BUTTONS */

[data-testid="stSidebar"]
.stButton > button {

    width:100%;

    min-height:46px;

    justify-content:flex-start;

    padding-left:15px;

    border-radius:11px;

    font-weight:700;

    background:#1E293B !important;

    border:1px solid #334155 !important;

    color:#FFFFFF !important;

    transition:.18s ease;
}


[data-testid="stSidebar"]
.stButton > button * {

    color:#FFFFFF !important;
}


[data-testid="stSidebar"]
.stButton > button:hover {

    background:#334155 !important;

    border-color:#F97316 !important;
}


/* CURRENT SIDEBAR PAGE */

[data-testid="stSidebar"]
.stButton > button[kind="primary"] {

    background:#F97316 !important;

    border-color:#F97316 !important;
}


[data-testid="stSidebar"]
.stButton > button[kind="primary"]:hover {

    background:#EA580C !important;

    border-color:#EA580C !important;
}


/* HERO */

.hero {

    padding:72px 60px;

    border-radius:26px;

    background:
        radial-gradient(
            circle at 88% 12%,
            rgba(249,115,22,.28),
            transparent 27%
        ),

        linear-gradient(
            135deg,
            #0F172A 0%,
            #172033 55%,
            #1E293B 100%
        );

    color:white;

    margin-bottom:26px;

    box-shadow:
        0 22px 48px
        rgba(15,23,42,.13);
}


.hero-badge {

    display:inline-block;

    padding:7px 13px;

    border-radius:999px;

    background:
        rgba(249,115,22,.14);

    border:
        1px solid
        rgba(249,115,22,.45);

    color:#FDBA74;

    font-size:.78rem;

    font-weight:800;

    letter-spacing:.08em;

    margin-bottom:20px;
}


.hero h1 {

    margin:0;

    font-size:
        clamp(
            2.7rem,
            6vw,
            5rem
        );

    line-height:1;

    letter-spacing:-.05em;
}


.hero p {

    max-width:820px;

    margin:22px 0 0;

    color:#CBD5E1;

    font-size:1.08rem;

    line-height:1.7;
}


/* PAGE HEADER */

.page-header {

    padding:34px 38px;

    border-radius:22px;

    background:
        linear-gradient(
            135deg,
            #0F172A,
            #1E293B
        );

    color:white;

    margin-bottom:28px;
}


.page-header h1 {

    margin:0;

    font-size:2.35rem;

    letter-spacing:-.035em;
}


.page-header p {

    margin:9px 0 0;

    color:#CBD5E1;

    max-width:880px;

    line-height:1.6;
}


/* SECTION HEADERS */

.section-title {

    margin-top:30px;

    margin-bottom:5px;

    color:#0F172A;

    font-size:1.9rem;

    font-weight:800;

    letter-spacing:-.035em;
}


.section-subtitle {

    color:#64748B;

    margin-bottom:22px;
}


/* CARDS */

.feature-card,
.info-card {

    padding:28px;

    background:white;

    border:
        1px solid
        #E2E8F0;

    border-radius:20px;

    box-shadow:
        0 7px 24px
        rgba(15,23,42,.05);

    margin-bottom:16px;
}


.feature-card {
    min-height:210px;
}


.feature-card .label {

    color:#F97316;

    font-size:.78rem;

    font-weight:800;

    letter-spacing:.09em;
}


.feature-card h3,
.info-card h3 {

    color:#0F172A;

    margin:14px 0 9px;

    font-size:1.35rem;
}


.feature-card p,
.info-card p {

    color:#64748B;

    line-height:1.65;

    margin:0;
}


/* ORANGE INFORMATION BOX */

.callout {

    padding:22px 26px;

    border-radius:18px;

    background:#FFF7ED;

    border:
        1px solid
        #FED7AA;

    color:#7C2D12;

    margin:18px 0;
}


/* METRICS */

[data-testid="stMetric"] {

    background:white;

    border:
        1px solid
        #E2E8F0;

    padding:21px;

    border-radius:18px;

    box-shadow:
        0 5px 18px
        rgba(15,23,42,.04);
}


/* NORMAL BUTTONS */

.stButton > button,
.stDownloadButton > button {

    min-height:46px;

    border-radius:12px;

    font-weight:700;
}


.stButton > button[kind="primary"] {

    background:#F97316;

    border-color:#F97316;

    color:white;
}


.stButton > button[kind="primary"]:hover {

    background:#EA580C;

    border-color:#EA580C;
}


.stDownloadButton > button {

    background:#0F172A;

    border-color:#0F172A;

    color:white;
}


/* FOOTER */

.footer {

    margin-top:55px;

    padding-top:22px;

    border-top:
        1px solid
        #E2E8F0;

    color:#94A3B8;

    font-size:.86rem;
}


/* MOBILE */

@media (max-width:800px) {

    .hero {
        padding:48px 28px;
    }

    .page-header {
        padding:28px 24px;
    }
}

</style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DEFAULT PROJECT ESTIMATE
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

        columns=
            BASE_COLUMNS,
    )


# ============================================================
# DEMO COST LIBRARY
# ============================================================

def create_cost_library():

    return pd.DataFrame(
        [

            [
                "Earthwork",
                "Excavation",
                "CY",
                12.50,
            ],

            [
                "Earthwork",
                "Fine Grading",
                "SY",
                2.75,
            ],

            [
                "Concrete",
                "Concrete",
                "CY",
                165.00,
            ],

            [
                "Paving",
                "Asphalt",
                "TON",
                95.00,
            ],

            [
                "Utilities",
                "Storm Pipe",
                "LF",
                42.00,
            ],

            [
                "Utilities",
                "Sanitary Sewer Pipe",
                "LF",
                55.00,
            ],

            [
                "Utilities",
                "Water Line",
                "LF",
                48.00,
            ],

            [
                "Site",
                "Curb & Gutter",
                "LF",
                24.00,
            ],

            [
                "Site",
                "Topsoil",
                "CY",
                32.00,
            ],

            [
                "Erosion Control",
                "Silt Fence",
                "LF",
                4.50,
            ],

            [
                "Erosion Control",
                "Construction Entrance",
                "EA",
                1450.00,
            ],

            [
                "Landscaping",
                "Seed & Mulch",
                "AC",
                2400.00,
            ],

        ],

        columns=[
            "Category",
            "Item",
            "Unit",
            "Baseline Unit Cost ($)",
        ],
    )


COST_LIBRARY = (
    create_cost_library()
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


if "estimate_base" not in st.session_state:

    st.session_state.estimate_base = (
        create_default_estimate()
    )


if "estimate_current" not in st.session_state:

    st.session_state.estimate_current = (
        create_default_estimate()
    )


# ============================================================
# DATA FUNCTIONS
# ============================================================

def clean_estimate(data):

    df = pd.DataFrame(
        data
    ).copy()


    for column in BASE_COLUMNS:

        if column not in df.columns:

            if column in [
                "Quantity",
                "Unit Cost ($)",
            ]:

                df[column] = 0.0

            else:

                df[column] = ""


    df = df[
        BASE_COLUMNS
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

            .fillna(
                0.0
            )
        )


    df["Total Cost"] = (

        df["Quantity"]

        *

        df["Unit Cost ($)"]
    )


    return df


def base_only(df):

    return (

        clean_estimate(
            df
        )[BASE_COLUMNS]

        .copy()
    )


def calculate_costs(df):

    cleaned = clean_estimate(
        df
    )


    direct = float(

        cleaned[
            "Total Cost"
        ].sum()
    )


    contingency_cost = (

        direct

        *

        float(
            st.session_state.contingency
        )

        /

        100.0
    )


    overhead_cost = (

        direct

        *

        float(
            st.session_state.overhead
        )

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

        float(
            st.session_state.profit
        )

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

        total,
    )


def active_estimate():

    return clean_estimate(

        st.session_state.estimate_current
    )


# ============================================================
# ESTIMATE STATE FUNCTIONS
# ============================================================

def commit_estimate():

    st.session_state.estimate_base = (

        base_only(
            st.session_state.estimate_current
        )
    )


    st.session_state.pop(
        "estimate_editor",
        None,
    )


def commit_scenario_b():

    if (
        "scenario_b_current"
        in
        st.session_state
    ):

        st.session_state.scenario_b_base = (

            base_only(
                st.session_state.scenario_b_current
            )
        )


    st.session_state.pop(
        "scenario_b_editor",
        None,
    )


# ============================================================
# NAVIGATION
# ============================================================

def set_page(
    page_name
):

    current_page = (

        st.session_state.get(
            "page",
            "Home",
        )
    )


    if (
        current_page
        ==
        "Cost Estimator"
    ):

        commit_estimate()


    elif (
        current_page
        ==
        "Scenario Comparison"
    ):

        commit_scenario_b()


    st.session_state.page = (
        page_name
    )


# ============================================================
# COST LIBRARY ACTIONS
# ============================================================

def add_library_item(
    item_name
):

    commit_estimate()


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
                    row[
                        "Category"
                    ],

                "Item":
                    row[
                        "Item"
                    ],

                "Quantity":
                    1.0,

                "Unit":
                    row[
                        "Unit"
                    ],

                "Unit Cost ($)":
                    float(
                        row[
                            "Baseline Unit Cost ($)"
                        ]
                    ),
            }
        ]
    )


    st.session_state.estimate_base = (

        pd.concat(
            [
                st.session_state.estimate_base,
                new_row,
            ],

            ignore_index=True,
        )
    )


    st.session_state.estimate_current = (

        clean_estimate(
            st.session_state.estimate_base
        )
    )


    st.session_state.pop(
        "estimate_editor",
        None,
    )


def reset_estimate():

    st.session_state.estimate_base = (
        create_default_estimate()
    )


    st.session_state.estimate_current = (
        create_default_estimate()
    )


    st.session_state.pop(
        "estimate_editor",
        None,
    )


# ============================================================
# SCENARIO ACTIONS
# ============================================================

def copy_current_to_scenario_b():

    current = (
        active_estimate()
    )


    st.session_state.scenario_b_base = (

        base_only(
            current
        )
    )


    st.session_state.scenario_b_current = (

        clean_estimate(
            current
        )
    )


    st.session_state.pop(
        "scenario_b_editor",
        None,
    )


# ============================================================
# UI HELPERS
# ============================================================

def show_page_header(
    title,
    description,
):

    st.markdown(

        '<div class="page-header">'

        f"<h1>{title}</h1>"

        f"<p>{description}</p>"

        "</div>",

        unsafe_allow_html=True,
    )


def show_section(
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


def show_card(
    label,
    title,
    body,
):

    st.markdown(

        '<div class="feature-card">'

        f'<div class="label">'
        f'{label}'
        f'</div>'

        f'<h3>'
        f'{title}'
        f'</h3>'

        f'<p>'
        f'{body}'
        f'</p>'

        '</div>',

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

        'BuildCost is an early-stage planning tool. '
        'Verify quantities, unit costs, scope, location, '
        'and date before using an estimate for project decisions.'

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


    for page_name in PAGES:

        if (
            st.session_state.page
            ==
            page_name
        ):

            button_type = (
                "primary"
            )

        else:

            button_type = (
                "secondary"
            )


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
        "BuildCost v7.0"
    )


# ============================================================
# CURRENT PROJECT VALUES
# ============================================================

page = (
    st.session_state.page
)


current_df = (
    active_estimate()
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
# HOME
# ============================================================

if page == "Home":

    st.markdown(

        '<div class="hero">'

        '<div class="hero-badge">'
        'CONSTRUCTION COST INTELLIGENCE'
        '</div>'

        '<h1>'

        'Plan smarter.'

        '<br>'

        '<span style="color:#FB923C;">'

        'Understand the cost before you build.'

        '</span>'

        '</h1>'

        '<p>'

        'BuildCost is an early-stage construction estimating '
        'and cost-comparison platform. Contractors, engineers, '
        'developers, and project teams can build estimates, '
        'use a starter cost library, analyze cost drivers, '
        'and compare project alternatives in one workspace.'

        '</p>'

        '</div>',

        unsafe_allow_html=True,
    )


    b1, b2, b3, spacer = (
        st.columns(
            [
                1.2,
                1.2,
                1.2,
                3,
            ]
        )
    )


    with b1:

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
                "home_estimator",
        )


    with b2:

        st.button(

            "Compare Scenarios",

            use_container_width=
                True,

            on_click=
                set_page,

            args=
                ("Scenario Comparison",),

            key=
                "home_scenarios",
        )


    with b3:

        st.button(

            "Explore Cost Library",

            use_container_width=
                True,

            on_click=
                set_page,

            args=
                ("Cost Library",),

            key=
                "home_library",
        )


    show_section(

        "One workflow. Better cost visibility.",

        "Build the estimate, understand what drives it, "
        "and compare alternatives before construction begins.",
    )


    c1, c2, c3, c4 = (
        st.columns(
            4
        )
    )


    with c1:

        show_card(

            "01 — ESTIMATE",

            "Build project costs",

            "Enter quantities and unit prices "
            "or start from the demo construction cost library.",
        )


    with c2:

        show_card(

            "02 — COMPARE",

            "Test alternatives",

            "Create a second scenario and see how design "
            "or pricing changes affect the overall project.",
        )


    with c3:

        show_card(

            "03 — ANALYZE",

            "Find cost drivers",

            "See which categories contribute the most "
            "to direct cost using interactive analytics.",
        )


    with c4:

        show_card(

            "04 — EXPORT",

            "Take the data with you",

            "Download the estimate as a CSV "
            "for documentation or additional analysis.",
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

        len(
            current_df
        ),
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

        "Build an estimate using project quantities and unit prices. "
        "The editor now keeps its source data stable, so a cell edit "
        "is processed the first time instead of resetting and making "
        "you type it again.",
    )


    show_section(

        "Quick add from the cost library",

        "Baseline prices are illustrative demo values. "
        "Adjust them for the real project and location.",
    )


    library_left, library_right = (

        st.columns(
            [
                2.5,
                1,
            ]
        )
    )


    with library_left:

        library_choice = (

            st.selectbox(

                "Construction item",

                COST_LIBRARY[
                    "Item"
                ].tolist(),

                key=
                    "estimator_library_choice",
            )
        )


    with library_right:

        st.write("")

        st.write("")


        st.button(

            "Add selected item",

            type=
                "primary",

            use_container_width=
                True,

            on_click=
                add_library_item,

            args=
                (library_choice,),

            key=
                "estimator_add_library",
        )


    show_section(

        "Project markups",

        "Adjust contingency, overhead, "
        "and profit percentages.",
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

        "Edit any cell directly. "
        "The first edit is retained and used immediately.",
    )


    edited_df = (
        st.data_editor(

            st.session_state.estimate_base,

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
    )


    estimate_df = (
        clean_estimate(
            edited_df
        )
    )


    # IMPORTANT:
    # Keep a snapshot for all other pages.
    #
    # DO NOT overwrite estimate_base here.
    #
    # estimate_base stays stable while the user edits.
    # That is what prevents the previous "type it twice"
    # and first-entry-reset problem.

    st.session_state.estimate_current = (
        estimate_df.copy()
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


    m1, m2, m3, m4, m5 = (

        st.columns(
            5
        )
    )


    m1.metric(

        "Direct Cost",

        f"${direct_cost:,.2f}",
    )


    m2.metric(

        "Contingency",

        f"${contingency_cost:,.2f}",
    )


    m3.metric(

        "Overhead",

        f"${overhead_cost:,.2f}",
    )


    m4.metric(

        "Profit",

        f"${profit_cost:,.2f}",
    )


    m5.metric(

        "Project Total",

        f"${grand_total:,.2f}",
    )


    controls1, controls2, spacer = (

        st.columns(
            [
                1.4,
                1.1,
                4,
            ]
        )
    )


    with controls1:

        csv_data = (

            estimate_df

            .to_csv(
                index=False
            )

            .encode(
                "utf-8"
            )
        )


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


    with controls2:

        st.button(

            "Reset Estimate",

            use_container_width=
                True,

            on_click=
                reset_estimate,

            key=
                "reset_estimate_button",
        )


    show_footer()


# ============================================================
# SCENARIO COMPARISON
# ============================================================

elif page == "Scenario Comparison":

    show_page_header(

        "Scenario Comparison",

        "Compare your current estimate with an alternative "
        "design, material choice, quantity plan, or pricing scenario.",
    )


    scenario_a = (
        active_estimate()
    )


    if (
        "scenario_b_base"
        not in
        st.session_state
    ):

        st.session_state.scenario_b_base = (

            base_only(
                scenario_a
            )
        )


    if (
        "scenario_b_current"
        not in
        st.session_state
    ):

        st.session_state.scenario_b_current = (

            clean_estimate(
                st.session_state.scenario_b_base
            )
        )


    top1, top2, spacer = (

        st.columns(
            [
                1.6,
                2.1,
                3,
            ]
        )
    )


    with top1:

        st.button(

            "Copy Current Estimate to B",

            type=
                "primary",

            use_container_width=
                True,

            on_click=
                copy_current_to_scenario_b,

            key=
                "copy_to_scenario_b",
        )


    with top2:

        st.caption(

            "Scenario A is your current estimate. "
            "Edit Scenario B without changing the main estimate."
        )


    show_section(

        "Scenario B",

        "Change quantities or unit costs "
        "to test an alternative.",
    )


    scenario_b_edited = (

        st.data_editor(

            st.session_state.scenario_b_base,

            num_rows=
                "dynamic",

            hide_index=
                True,

            use_container_width=
                True,

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
    )


    scenario_b = (

        clean_estimate(
            scenario_b_edited
        )
    )


    st.session_state.scenario_b_current = (

        scenario_b.copy()
    )


    (
        a_direct,
        a_contingency,
        a_overhead,
        a_profit,
        a_total,
    ) = calculate_costs(
        scenario_a
    )


    (
        b_direct,
        b_contingency,
        b_overhead,
        b_profit,
        b_total,
    ) = calculate_costs(
        scenario_b
    )


    difference = (

        b_total

        -

        a_total
    )


    if (
        a_total
        !=
        0
    ):

        percentage_difference = (

            difference

            /

            a_total

            *

            100.0
        )

    else:

        percentage_difference = (
            0.0
        )


    show_section(
        "Comparison summary"
    )


    s1, s2, s3, s4 = (

        st.columns(
            4
        )
    )


    s1.metric(

        "Scenario A",

        f"${a_total:,.2f}",
    )


    s2.metric(

        "Scenario B",

        f"${b_total:,.2f}",
    )


    s3.metric(

        "B − A Difference",

        f"${difference:,.2f}",

        f"{percentage_difference:+.1f}%",
    )


    if (
        a_total
        <
        b_total
    ):

        lower_cost = "A"


    elif (
        b_total
        <
        a_total
    ):

        lower_cost = "B"


    else:

        lower_cost = "Same"


    s4.metric(

        "Lower Cost",

        lower_cost,
    )


    a_categories = (

        scenario_a

        .assign(

            Category=
                scenario_a[
                    "Category"
                ].replace(
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
                scenario_b[
                    "Category"
                ].replace(
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


    comparison_df = (

        pd.merge(

            a_categories,

            b_categories,

            on=
                "Category",

            how=
                "outer",
        )

        .fillna(
            0.0
        )
    )


    comparison_df[
        "Difference (B - A)"
    ] = (

        comparison_df[
            "Scenario B"
        ]

        -

        comparison_df[
            "Scenario A"
        ]
    )


    show_section(

        "Category comparison",

        "See which categories caused "
        "the cost difference.",
    )


    if (
        not
        comparison_df.empty
    ):

        chart_df = (

            comparison_df

            .melt(

                id_vars=
                    "Category",

                value_vars=[
                    "Scenario A",
                    "Scenario B",
                ],

                var_name=
                    "Scenario",

                value_name=
                    "Cost",
            )
        )


        fig = (

            px.bar(

                chart_df,

                x=
                    "Category",

                y=
                    "Cost",

                color=
                    "Scenario",

                barmode=
                    "group",
            )
        )


        fig.update_layout(

            height=
                480,

            xaxis_title=
                "",

            yaxis_title=
                "Direct Cost ($)",

            margin=
                dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10,
                ),
        )


        st.plotly_chart(

            fig,

            use_container_width=
                True,
        )


    st.dataframe(

        comparison_df,

        hide_index=
            True,

        use_container_width=
            True,

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


    show_footer()


# ============================================================
# COST ANALYTICS
# ============================================================

elif page == "Cost Analytics":

    show_page_header(

        "Cost Analytics",

        "Understand where project money is being spent "
        "and identify the categories driving the estimate.",
    )


    analytics_df = (
        active_estimate()
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


    category_df[
        "Category"
    ] = (

        category_df[
            "Category"
        ]

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


    if (
        not
        category_df.empty
    ):

        largest_category = (

            category_df
            .iloc[0]["Category"]
        )

    else:

        largest_category = (
            "N/A"
        )


    if (
        not
        analytics_df.empty
    ):

        average_cost = float(

            analytics_df[
                "Total Cost"
            ].mean()
        )

    else:

        average_cost = (
            0.0
        )


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
        "Cost by category"
    )


    if (

        direct_cost
        >
        0

        and

        not
        category_df.empty
    ):

        fig = (

            px.bar(

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
        )


        fig.update_layout(

            height=
                470,

            xaxis_title=
                "Direct Cost ($)",

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


    with right:

        st.markdown(
            "#### Project Cost Summary"
        )


        summary_df = (

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

            summary_df,

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
# COST LIBRARY
# ============================================================

elif page == "Cost Library":

    show_page_header(

        "Cost Library",

        "Start estimates faster with a small demo library "
        "of common construction activities and baseline unit costs.",
    )


    st.markdown(

        '<div class="callout">'

        '<strong>'
        'Important:'
        '</strong> '

        'These are illustrative demo values for the BuildCost '
        'prototype, not verified current market prices. '
        'Always replace them with project-specific local pricing.'

        '</div>',

        unsafe_allow_html=True,
    )


    st.dataframe(

        COST_LIBRARY,

        hide_index=
            True,

        use_container_width=
            True,

        column_config={

            "Baseline Unit Cost ($)":
                st.column_config.NumberColumn(
                    format="$%.2f"
                )
        },
    )


    library_choice = (

        st.selectbox(

            "Add an item to your current estimate",

            COST_LIBRARY[
                "Item"
            ].tolist(),

            key=
                "library_page_choice",
        )
    )


    st.button(

        "Add to Estimate",

        type=
            "primary",

        on_click=
            add_library_item,

        args=
            (library_choice,),

        key=
            "library_page_add_button",
    )


    show_footer()


# ============================================================
# PROJECT INFORMATION
# ============================================================

elif page == "Project Information":

    show_page_header(

        "Project Information",

        "Keep the basic information associated "
        "with your construction estimate organized in one place.",
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
            "estimate notes, or other important information...",
    )


    show_section(
        "Project snapshot"
    )


    project_df = (
        active_estimate()
    )


    (
        project_direct,
        project_contingency,
        project_overhead,
        project_profit,
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

        "A construction-tech prototype focused on early-stage "
        "estimating, cost visibility, and alternative comparison.",
    )


    st.markdown(

        '<div class="hero">'

        '<div class="hero-badge">'
        'WHY BUILDCOST'
        '</div>'

        '<h1 style="font-size:3.5rem;">'

        'Estimate the project.'

        '<br>'

        '<span style="color:#FB923C;">'

        'Then challenge the assumptions.'

        '</span>'

        '</h1>'

        '<p>'

        'BuildCost brings the estimate, cost analytics, '
        'a starter cost library, and scenario comparison '
        'into one lightweight web application.'

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

        show_card(

            "PROBLEM",

            "Early estimates change",

            "Quantities, materials, and pricing assumptions "
            "can shift quickly during planning and design.",
        )


    with c2:

        show_card(

            "SOLUTION",

            "Make changes visible",

            "BuildCost shows the estimate and the categories "
            "responsible for cost differences.",
        )


    with c3:

        show_card(

            "NEXT",

            "Grow the platform",

            "Future versions could add regional price data, "
            "saved projects, accounts, reports, and collaboration.",
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


    show_footer()


# ============================================================
# CONTACT
# ============================================================

elif page == "Contact":

    show_page_header(

        "Contact BuildCost",

        "Questions, product feedback, feature ideas, "
        "or collaboration opportunities.",
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

            "Prepare an email directly "
            "from the BuildCost website.",
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

                not
                contact_name.strip()

                or

                not
                contact_email.strip()

                or

                not
                contact_message.strip()
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

                    "Replace CONTACT_EMAIL near the top "
                    "of app.py with the email address "
                    "you want BuildCost messages sent to."
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
            'for clearer early-stage planning '
            'and alternative comparison.'
            '</p>'

            '</div>',

            unsafe_allow_html=True,
        )


        st.markdown(

            '<div class="info-card">'

            '<h3>'
            'Hackathon prototype'
            '</h3>'

            '<p>'
            'Feedback on estimating, scenario analysis, '
            'construction data, and future workflows '
            'is welcome.'
            '</p>'

            '</div>',

            unsafe_allow_html=True,
        )


    show_footer()
