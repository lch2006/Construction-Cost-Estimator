import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="BuildCost | Construction Cost Estimator",
    page_icon="🏗️",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stMetric"] {
        background: rgba(120, 120, 120, 0.08);
        border: 1px solid rgba(120, 120, 120, 0.18);
        padding: 18px;
        border-radius: 14px;
    }

    .hero {
        padding: 22px 26px;
        border-radius: 18px;
        background: linear-gradient(135deg, #18222f, #31455d);
        color: white;
        margin-bottom: 22px;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.2rem;
    }

    .hero p {
        margin: 0.35rem 0 0;
        opacity: 0.85;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🏗️ BuildCost</h1>
        <p>
            Construction Cost Estimator • Plan quantities,
            pricing, markups, and total project cost.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR - PROJECT SETTINGS
# --------------------------------------------------

with st.sidebar:

    st.header("Project Settings")

    project_name = st.text_input(
        "Project name",
        "Residential Site Development"
    )

    client = st.text_input(
        "Client",
        "Example Client"
    )

    location = st.text_input(
        "Project location",
        "Blacksburg, VA"
    )

    st.divider()

    st.subheader("Project Markups")

    contingency = st.number_input(
        "Contingency (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.5
    )

    overhead = st.number_input(
        "Overhead (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.5
    )

    profit = st.number_input(
        "Profit (%)",
        min_value=0.0,
        max_value=100.0,
        value=8.0,
        step=0.5
    )


# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

st.subheader(project_name)

st.caption(
    f"{client} • {location}"
)


# --------------------------------------------------
# DEFAULT ESTIMATE ITEMS
# --------------------------------------------------

if "items" not in st.session_state:

    st.session_state.items = pd.DataFrame(
        [
            [
                "Earthwork",
                "Excavation",
                800.0,
                "CY",
                12.50
            ],

            [
                "Concrete",
                "Concrete",
                120.0,
                "CY",
                165.00
            ],

            [
                "Paving",
                "Asphalt",
                500.0,
                "TON",
                95.00
            ],

            [
                "Utilities",
                "Storm Pipe",
                600.0,
                "LF",
                42.00
            ],

            [
                "Utilities",
                "Sanitary Sewer Pipe",
                350.0,
                "LF",
                55.00
            ],

            [
                "Site",
                "Curb & Gutter",
                900.0,
                "LF",
                24.00
            ],
        ],

        columns=[
            "Category",
            "Item",
            "Quantity",
            "Unit",
            "Unit Cost ($)"
        ]
    )


# --------------------------------------------------
# ESTIMATE TABLE
# --------------------------------------------------

st.markdown("### Estimate Items")

st.caption(
    "Edit cells directly. Add or delete rows using the table controls."
)


# Make sure session data is always a DataFrame
st.session_state.items = pd.DataFrame(
    st.session_state.items,
    columns=[
        "Category",
        "Item",
        "Quantity",
        "Unit",
        "Unit Cost ($)"
    ]
)


# --------------------------------------------------
# CLEAN DATA TYPES
# --------------------------------------------------

# Text columns
for column in [
    "Category",
    "Item",
    "Unit"
]:

    st.session_state.items[column] = (
        st.session_state.items[column]
        .fillna("")
        .astype(str)
    )


# Numeric columns
for column in [
    "Quantity",
    "Unit Cost ($)"
]:

    st.session_state.items[column] = pd.to_numeric(
        st.session_state.items[column],
        errors="coerce"
    ).fillna(0.0)


# --------------------------------------------------
# EDITABLE TABLE
# --------------------------------------------------

edited = st.data_editor(

    st.session_state.items,

    num_rows="dynamic",

    use_container_width=True,

    hide_index=True,

    column_config={

        "Category": st.column_config.TextColumn(
            "Category"
        ),

        "Item": st.column_config.TextColumn(
            "Item"
        ),

        "Quantity": st.column_config.NumberColumn(
            "Quantity",
            min_value=0.0,
            format="%.2f"
        ),

        "Unit": st.column_config.TextColumn(
            "Unit"
        ),

        "Unit Cost ($)": st.column_config.NumberColumn(
            "Unit Cost ($)",
            min_value=0.0,
            format="$%.2f"
        ),
    },

    key="cost_editor"
)


# Save edited table
st.session_state.items = edited


# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------

df = edited.copy()


# Make sure numeric columns stay numeric
for column in [
    "Quantity",
    "Unit Cost ($)"
]:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0.0)


# Calculate each item's total cost
df["Total Cost"] = (
    df["Quantity"]
    *
    df["Unit Cost ($)"]
)


# --------------------------------------------------
# PROJECT TOTALS
# --------------------------------------------------

direct_cost = df["Total Cost"].sum()


contingency_cost = (
    direct_cost
    *
    contingency
    /
    100
)


overhead_cost = (
    direct_cost
    *
    overhead
    /
    100
)


base_with_markup = (
    direct_cost
    +
    contingency_cost
    +
    overhead_cost
)


profit_cost = (
    base_with_markup
    *
    profit
    /
    100
)


grand_total = (
    base_with_markup
    +
    profit_cost
)


# --------------------------------------------------
# PROJECT SUMMARY
# --------------------------------------------------

st.markdown("### Project Summary")


col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Direct Cost",
    f"${direct_cost:,.2f}"
)


col2.metric(
    "Contingency",
    f"${contingency_cost:,.2f}",
    f"{contingency:.1f}%"
)


col3.metric(
    "Overhead",
    f"${overhead_cost:,.2f}",
    f"{overhead:.1f}%"
)


col4.metric(
    "Estimated Total",
    f"${grand_total:,.2f}"
)


# --------------------------------------------------
# CHART + ESTIMATE DETAILS
# --------------------------------------------------

left, right = st.columns(
    [1.25, 1]
)


# --------------------------------------------------
# COST BREAKDOWN CHART
# --------------------------------------------------

with left:

    st.markdown(
        "### Cost Breakdown"
    )

    if (
        not df.empty
        and
        direct_cost > 0
    ):

        category_costs = (
            df.groupby(
                "Category",
                dropna=False
            )["Total Cost"]
            .sum()
            .reset_index()
        )


        category_costs["Category"] = (
            category_costs["Category"]
            .replace("", "Uncategorized")
            .fillna("Uncategorized")
        )


        category_costs = (
            category_costs
            .sort_values(
                "Total Cost",
                ascending=False
            )
        )


        fig = px.bar(

            category_costs,

            x="Category",

            y="Total Cost",

            text_auto=".2s"
        )


        fig.update_layout(

            yaxis_title="Cost ($)",

            xaxis_title="",

            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),

            height=390
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    else:

        st.info(
            "Add estimate items to generate a chart."
        )


# --------------------------------------------------
# ESTIMATE DETAILS
# --------------------------------------------------

with right:

    st.markdown(
        "### Estimate Details"
    )


    display_df = df[
        [
            "Category",
            "Item",
            "Quantity",
            "Unit",
            "Unit Cost ($)",
            "Total Cost"
        ]
    ]


    st.dataframe(

        display_df,

        use_container_width=True,

        hide_index=True,

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
        }
    )


# --------------------------------------------------
# MARKUP DETAILS
# --------------------------------------------------

st.markdown(
    "### Cost Summary"
)


summary = pd.DataFrame(
    {

        "Description": [

            "Direct Cost",

            f"Contingency ({contingency:.1f}%)",

            f"Overhead ({overhead:.1f}%)",

            f"Profit ({profit:.1f}%)",

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

    summary,

    use_container_width=True,

    hide_index=True,

    column_config={

        "Amount":
            st.column_config.NumberColumn(
                format="$%.2f"
            )
    }
)


# --------------------------------------------------
# EXPORT
# --------------------------------------------------

st.markdown(
    "### Export Estimate"
)


export_df = df.copy()


csv = export_df.to_csv(
    index=False
).encode(
    "utf-8"
)


st.download_button(

    label="⬇️ Download Estimate CSV",

    data=csv,

    file_name="construction_estimate.csv",

    mime="text/csv"
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()


st.caption(
    """
    BuildCost v1.0 • Unit costs are user-provided estimates
    and should be verified for the specific project,
    location, and date.
    """
)
