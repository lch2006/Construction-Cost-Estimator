import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote


# ============================================================
# BUILDCOST V2.1
# ============================================================

st.set_page_config(
    page_title="BuildCost",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

CONTACT_EMAIL = "your-email@example.com"

PAGES = [
    "Home",
    "Cost Estimator",
    "Cost Analytics",
    "Project Information",
    "About BuildCost",
    "Contact"
]


# ------------------------------------------------------------
# DESIGN / CSS
# ------------------------------------------------------------

st.markdown(
    """
<style>

.stApp {
    background: #F8FAFC;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

[data-testid="stHeader"] {
    background: rgba(248, 250, 252, 0.94);
}

[data-testid="stSidebar"] {
    background: #0F172A;
}

[data-testid="stSidebar"] * {
    color: #F8FAFC;
}

.hero {
    padding: 70px 58px;
    border-radius: 26px;
    background: linear-gradient(135deg, #0F172A, #1E293B);
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 20px 45px rgba(15, 23, 42, 0.12);
}

.hero-badge {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(249, 115, 22, 0.14);
    border: 1px solid rgba(249, 115, 22, 0.45);
    color: #FDBA74;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    margin-bottom: 18px;
}

.hero h1 {
    font-size: clamp(2.6rem, 6vw, 5rem);
    line-height: 1;
    margin: 0;
    letter-spacing: -0.05em;
}

.hero p {
    max-width: 760px;
    color: #CBD5E1;
    font-size: 1.08rem;
    line-height: 1.7;
    margin: 22px 0 0;
}

.page-head {
    padding: 32px 36px;
    border-radius: 22px;
    background: #0F172A;
    color: white;
    margin-bottom: 26px;
}

.page-head h1 {
    margin: 0;
    font-size: 2.3rem;
}

.page-head p {
    color: #CBD5E1;
    margin: 8px 0 0;
    max-width: 800px;
}

.card {
    min-height: 205px;
    padding: 27px;
    border-radius: 19px;
    background: white;
    border: 1px solid #E2E8F0;
    box-shadow: 0 7px 25px rgba(15, 23, 42, 0.05);
    margin-bottom: 16px;
}

.card .eyebrow {
    color: #F97316;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.09em;
}

.card h3 {
    color: #0F172A;
    margin: 14px 0 8px;
    font-size: 1.3rem;
}

.card p {
    color: #64748B;
    line-height: 1.6;
    margin: 0;
}

.section-title {
    font-size: 1.85rem;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.03em;
    margin: 28px 0 4px;
}

.section-sub {
    color: #64748B;
    margin-bottom: 20px;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E2E8F0;
    padding: 20px;
    border-radius: 17px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
}

.stButton > button {
    border-radius: 11px;
    min-height: 45px;
    font-weight: 700;
}

.stButton > button[kind="primary"] {
    background: #F97316;
    border-color: #F97316;
    color: white;
}

.stDownloadButton > button {
    border-radius: 11px;
    min-height: 45px;
    font-weight: 700;
    background: #0F172A;
    color: white;
    border-color: #0F172A;
}

.footer {
    margin-top: 48px;
    padding-top: 20px;
    border-top: 1px solid #E2E8F0;
    color: #94A3B8;
    font-size: 0.85rem;
}

</style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# DEFAULT ESTIMATE
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

defaults = {
    "page": "Home",
    "project_name": "Residential Site Development",
    "client": "Example Client",
    "project_location": "Blacksburg, VA",
    "project_type": "Land Development",
    "project_notes": "",
    "contingency": 10.0,
    "overhead": 5.0,
    "profit": 8.0
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


if "current_estimate" not in st.session_state:

    st.session_state.current_estimate = default_items()


# ------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------

def clean_estimate(data):

    required = [
        "Category",
        "Item",
        "Quantity",
        "Unit",
        "Unit Cost ($)"
    ]

    df = pd.DataFrame(data).copy()

    for column in required:

        if column not in df.columns:

            if column in ["Quantity", "Unit Cost ($)"]:
                df[column] = 0.0

            else:
                df[column] = ""

    df = df[required]

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

    direct = float(
        df["Total Cost"].sum()
    )

    contingency_cost = (
        direct
        *
        float(st.session_state.contingency)
        /
        100
    )

    overhead_cost = (
        direct
        *
        float(st.session_state.overhead)
        /
        100
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
        float(st.session_state.profit)
        /
        100
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

    html = (
        '<div class="page-head">'
        f'<h1>{title}</h1>'
        f'<p>{description}</p>'
        '</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def footer():

    st.markdown(
        '<div class="footer">'
        '<strong>BuildCost</strong> • Construction Cost Intelligence'
        '<br>'
        'Planning estimates should be verified for project scope, '
        'location, and date.'
        '</div>',
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# NAVIGATION
# ------------------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div style="font-size:1.6rem;font-weight:900;'
        'margin:8px 0 2px;">'
        '🏗️ BUILDCOST'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "CONSTRUCTION COST INTELLIGENCE"
    )

    selected_page = st.radio(
        "Navigation",
        PAGES,
        index=PAGES.index(
            st.session_state.page
        ),
        label_visibility="collapsed"
    )

    st.session_state.page = selected_page

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
        "BuildCost v2.1"
    )


# ------------------------------------------------------------
# CURRENT COST INFORMATION
# ------------------------------------------------------------

current_df = clean_estimate(
    st.session_state.current_estimate
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
# HOME
# ============================================================

if st.session_state.page == "Home":

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
        'BuildCost helps contractors, engineers, developers, '
        'and project teams turn construction quantities and unit '
        'pricing into clear early-stage project estimates.'
        '</p>'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True
    )

    button1, button2, spacer = st.columns(
        [1.2, 1.1, 4]
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
        '<div class="section-title">'
        'From quantities to project cost.'
        '</div>'
        '<div class="section-sub">'
        'One workspace for early construction cost planning.'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    cards = [
        (
            "01 — ESTIMATE",
            "Build your estimate",
            "Organize construction activities, quantities, units, "
            "and unit prices in an editable estimate."
        ),
        (
            "02 — ANALYZE",
            "Understand your costs",
            "See which construction categories drive project cost "
            "with interactive visualizations and metrics."
        ),
        (
            "03 — EXPORT",
            "Take your data with you",
            "Export organized estimate data for documentation, "
            "analysis, and project planning."
        )
    ]

    for column, card in zip(
        [c1, c2, c3],
        cards
    ):

        with column:

            card_html = (
                '<div class="card">'
                f'<div class="eyebrow">{card[0]}</div>'
                f'<h3>{card[1]}</h3>'
                f'<p>{card[2]}</p>'
                '</div>'
            )

            st.markdown(
                card_html,
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="section-title">'
        'Current project snapshot'
        '</div>',
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

    footer()


# ============================================================
# COST ESTIMATOR
# ============================================================

elif st.session_state.page == "Cost Estimator":

    page_header(
        "Cost Estimator",
        "Build an early-stage estimate using construction "
        "quantities, units, and unit pricing."
    )

    st.markdown(
        '<div class="section-title">'
        'Project markups'
        '</div>'
        '<div class="section-sub">'
        'Configure the percentages applied to your estimate.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.session_state.contingency = st.number_input(
            "Contingency (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                st.session_state.contingency
            ),
            step=0.5
        )

    with col2:

        st.session_state.overhead = st.number_input(
            "Overhead (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                st.session_state.overhead
            ),
            step=0.5
        )

    with col3:

        st.session_state.profit = st.number_input(
            "Profit (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                st.session_state.profit
            ),
            step=0.5
        )

    st.markdown(
        '<div class="section-title">'
        'Estimate items'
        '</div>'
        '<div class="section-sub">'
        'Edit existing items or add new construction activities.'
        '</div>',
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
        }
    )

    working_df = clean_estimate(
        edited
    )

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
        '<div class="section-title">'
        'Estimate summary'
        '</div>',
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

    st.markdown(
        "#### Detailed estimate"
    )

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

    csv = working_df.to_csv(
        index=False
    ).encode(
        "utf-8"
    )

    st.download_button(
        "⬇ Download Estimate CSV",
        csv,
        "BuildCost_Estimate.csv",
        "text/csv"
    )

    footer()


# ============================================================
# COST ANALYTICS
# ============================================================

elif st.session_state.page == "Cost Analytics":

    page_header(
        "Cost Analytics",
        "Understand where project money is being spent and "
        "which categories drive your estimate."
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

        largest_category = (
            category_df.iloc[0]["Category"]
        )

    else:

        largest_category = "N/A"

    if len(analytics_df) > 0:

        average_item_cost = float(
            analytics_df[
                "Total Cost"
            ].mean()
        )

    else:

        average_item_cost = 0.0

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Project Total",
        f"${grand_total:,.0f}"
    )

    m2.metric(
        "Largest Category",
        largest_category
    )

    m3.metric(
        "Cost Items",
        len(analytics_df)
    )

    m4.metric(
        "Average Item Cost",
        f"${average_item_cost:,.0f}"
    )

    st.markdown(
        '<div class="section-title">'
        'Cost by category'
        '</div>',
        unsafe_allow_html=True
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

        fig.update_yaxes(
            categoryorder="total ascending"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "Add project costs in the Cost Estimator "
            "to generate analytics."
        )

    left, right = st.columns(2)

    with left:

        st.markdown(
            "#### Category summary"
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
            "#### Markup summary"
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
        "Keep the information associated with your construction "
        "estimate organized in one place."
    )

    left, right = st.columns(2)

    with left:

        st.session_state.project_name = st.text_input(
            "Project name",
            st.session_state.project_name
        )

        st.session_state.client = st.text_input(
            "Client",
            st.session_state.client
        )

    with right:

        st.session_state.project_location = st.text_input(
            "Project location",
            st.session_state.project_location
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
            if st.session_state.project_type
            in project_types
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
        st.session_state.project_notes,
        height=160,
        placeholder=(
            "Scope, assumptions, estimate notes, "
            "or other project information..."
        )
    )

    st.success(
        "Project information is saved for your current session."
    )

    st.markdown(
        '<div class="section-title">'
        'Project snapshot'
        '</div>',
        unsafe_allow_html=True
    )

    s1, s2, s3 = st.columns(3)

    s1.metric(
        "Estimated Cost",
        f"${grand_total:,.0f}"
    )

    s2.metric(
        "Estimate Items",
        len(current_df)
    )

    s3.metric(
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
        "A simpler approach to early-stage "
        "construction cost planning."
    )

    about_html = (
        '<div class="hero">'
        '<div class="hero-badge">'
        'OUR PURPOSE'
        '</div>'
        '<h1 style="font-size:3.4rem;">'
        'Better cost visibility.'
        '<br>'
        '<span style="color:#FB923C;">'
        'Better project planning.'
        '</span>'
        '</h1>'
        '<p>'
        'BuildCost was created to make construction cost '
        'estimating more accessible, organized, and visual. '
        'It turns quantities and unit pricing into an '
        'understandable early-stage project estimate.'
        '</p>'
        '</div>'
    )

    st.markdown(
        about_html,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    about_cards = [
        (
            "MISSION",
            "Simplify estimating",
            "Reduce the friction involved in organizing quantities, "
            "unit pricing, and project cost assumptions."
        ),
        (
            "DESIGN",
            "Make costs understandable",
            "Transform cost information into summaries and "
            "visualizations that are easier to interpret."
        ),
        (
            "FUTURE",
            "Build a smarter platform",
            "Expand into saved projects, location-based pricing, "
            "labor and equipment breakdowns, and reporting."
        )
    ]

    for column, card in zip(
        [c1, c2, c3],
        about_cards
    ):

        with column:

            card_html = (
                '<div class="card">'
                f'<div class="eyebrow">{card[0]}</div>'
                f'<h3>{card[1]}</h3>'
                f'<p>{card[2]}</p>'
                '</div>'
            )

            st.markdown(
                card_html,
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="section-title">'
        'Built with'
        '</div>',
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
        "Prepare a message here."
    )

    left, right = st.columns(
        [1.3, 0.7]
    )

    with left:

        st.markdown(
            '<div class="section-title">'
            "Let's talk construction."
            '</div>'
            '<div class="section-sub">'
            'Tell us what you are interested in.'
            '</div>',
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

            elif CONTACT_EMAIL == "your-email@example.com":

                st.warning(
                    "Replace CONTACT_EMAIL near the top "
                    "of app.py with your email first."
                )

            else:

                subject = quote(
                    f"BuildCost - {contact_topic}"
                )

                body = quote(
                    f"Name: {contact_name}\n"
                    f"Email: {contact_email}\n"
                    f"Topic: {contact_topic}\n\n"
                    f"Message:\n{contact_message}"
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
                    f'<a href="{mailto_link}">'
                    'Open your email app to send the message'
                    '</a>',
                    unsafe_allow_html=True
                )

    with right:

        st.markdown(
            '<div class="card">'
            '<div class="eyebrow">BUILDCOST</div>'
            '<h3>Construction cost intelligence</h3>'
            '<p>'
            'Built for clearer early-stage project '
            'planning and cost analysis.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="card">'
            '<div class="eyebrow">FEEDBACK</div>'
            '<h3>Help improve BuildCost</h3>'
            '<p>'
            'Share ideas for estimating, analytics, '
            'reporting, or future project workflows.'
            '</p>'
            '</div>',
            unsafe_allow_html=True
        )

    footer()
