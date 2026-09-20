import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="BuildCost",
    page_icon="🏗️",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 24px 28px;
        border-radius: 18px;
        background: linear-gradient(135deg, #18222f, #31455d);
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.4rem;
    }

    .hero p {
        margin: .4rem 0 0;
        opacity: .88;
    }

    [data-testid="stMetric"] {
        background: rgba(120,120,120,.08);
        border: 1px solid rgba(120,120,120,.18);
        padding: 16px;
        border-radius: 14px;
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
            Construction Cost Estimator • Quantities,
            unit pricing, markups, and project totals.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
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

st.title(project_name)

st.caption(
    f"{client} • {location}"
)


# --------------------------------------------------
# DEFAULT ESTIMATE DATA
# --------------------------------------------------

DEFAULT_ITEMS = pd.DataFrame(

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
        ]

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

st.markdown(
    "### Estimate Items"
)

st.caption(
    "Edit cells directly. Use the table controls to add or delete rows."
)


edited = st.data_editor(

    DEFAULT_ITEMS,

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
                step=1.0,
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
                step=1.0,
                format="$%.2f"
            )

    },

    key="estimate_editor"

)


# --------------------------------------------------
# CLEAN DATA
# --------------------------------------------------

df = edited.copy()


# Clean text columns
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


# Clean numeric columns
for column in [
    "Quantity",
    "Unit Cost ($)"
]:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0.0)


# --------------------------------------------------
# CALCULATE ITEM COSTS
# --------------------------------------------------

df["Total Cost"] = (
    df["Quantity"]
    *
    df["Unit Cost ($)"]
)


# --------------------------------------------------
# PROJECT COST CALCULATIONS
# --------------------------------------------------

direct_cost = float(
    df["Total Cost"].sum()
)


contingency_cost = (
    direct_cost
    *
    contingency
    /
    100.0
)


overhead_cost = (
    direct_cost
    *
    overhead
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
    profit
    /
    100.0
)


grand_total = (
    subtotal
    +
    profit_cost
)


# --------------------------------------------------
# PROJECT SUMMARY
# --------------------------------------------------

st.markdown(
    "### Project Summary"
)


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
# CHART AND DETAILS
# --------------------------------------------------

left, right = st.columns(
    [1.15, 1]
)


# --------------------------------------------------
# COST BREAKDOWN CHART
# --------------------------------------------------

with left:

    st.markdown(
        "### Cost Breakdown"
    )


    if direct_cost > 0 and not df.empty:

        chart_df = df.copy()


        chart_df["Category"] = (
            chart_df["Category"]
            .replace(
                "",
                "Uncategorized"
            )
        )


        chart_df = (
            chart_df
            .groupby(
                "Category",
                as_index=False
            )["Total Cost"]
            .sum()
        )


        chart_df = (
            chart_df
            .sort_values(
                "Total Cost",
                ascending=False
            )
        )


        fig = px.bar(

            chart_df,

            x="Category",

            y="Total Cost",

            text_auto=".2s"

        )


        fig.update_layout(

            height=390,

            xaxis_title="",

            yaxis_title="Cost ($)",

            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            )

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    else:

        st.info(
            "Enter quantities and unit costs to generate the chart."
        )


# --------------------------------------------------
# ESTIMATE DETAILS
# --------------------------------------------------

with right:

    st.markdown(
        "### Estimate Details"
    )


    st.dataframe(

        df[
            [
                "Category",
                "Item",
                "Quantity",
                "Unit",
                "Unit Cost ($)",
                "Total Cost"
            ]
        ],

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


# --------------------------------------------------
# COST SUMMARY
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

    hide_index=True,

    use_container_width=True,

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
    "### Export"
)


csv = df.to_csv(
    index=False
).encode(
    "utf-8"
)


st.download_button(

    "⬇️ Download Estimate CSV",

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
    BuildCost v1.1 • Unit costs are user-provided estimates
    and should be verified for the project location and date.
    """
)
