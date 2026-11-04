import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GLOBAL CONSTANTS
# ============================================================

CURRENCY_SYMBOL = "£"  # Change to your currency, e.g. "$" or "€"

# One consistent color palette used across the whole dashboard
COLOR_SEQUENCE = [
    "#4f46e5", "#0ea5e9", "#14b8a6", "#f59e0b",
    "#ef4444", "#8b5cf6", "#ec4899", "#22c55e"
]

ACCENT = "#4f46e5"


def fmt_currency(value):
    return f"{CURRENCY_SYMBOL}{value:,.2f}"


def fmt_int(value):
    return f"{value:,.0f}"


def pct_delta(current, previous):
    if previous in (0, None) or pd.isna(previous):
        return None
    return (current - previous) / previous * 100


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GENERAL
       ======================================================== */

    .stApp {
        background-color: #f4f6f9;
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    * {
        font-family: "Inter", "Segoe UI", Arial, sans-serif;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #f9fafb !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #9ca3af !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #374151;
    }


    /* ========================================================
       RADIO BUTTONS
       ======================================================== */

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 8px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: transparent;
        border-radius: 8px;
        padding: 8px 10px;
        transition: background-color 0.2s ease;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #1f2937;
    }


    /* ========================================================
       PAGE TITLE
       ======================================================== */

    .page-title {
        font-size: 32px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 4px;
    }

    .page-subtitle {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 25px;
    }


    /* ========================================================
       KPI CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-left: 4px solid #4f46e5;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.08);
        transform: translateY(-2px);
    }

    div[data-testid="stMetric"] label {
        color: #6b7280 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }


    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .section-header {
        font-size: 20px;
        font-weight: 650;
        color: #111827;
        margin-top: 18px;
        margin-bottom: 5px;
    }

    .section-description {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 12px;
    }


    /* ========================================================
       CARD CONTAINER (used to wrap charts)
       ======================================================== */

    .chart-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px 20px 6px 20px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        margin-bottom: 18px;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #e5e7eb;
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton button, .stDownloadButton button {
        border-radius: 8px;
        border: 1px solid #d1d5db;
    }

    .stDownloadButton button {
        border-color: #4f46e5;
        color: #4f46e5;
    }


    /* ========================================================
       BADGES
       ======================================================== */

    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 600;
        background-color: #eef2ff;
        color: #4338ca;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-text {
        text-align: center;
        color: #9ca3af;
        font-size: 12px;
        padding-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

REQUIRED_FILES = {
    "kpis": "dashboard/kpis.csv",
    "monthly": "dashboard/monthly_revenue.csv",
    "countries": "dashboard/country_revenue.csv",
    "products": "dashboard/product_revenue.csv",
    "hourly": "dashboard/hourly_sales.csv",
    "segments": "dashboard/segment_distribution.csv",
    "segment_revenue": "dashboard/segment_revenue.csv",
    "rfm": "dashboard/rfm_customers.csv",
}


@st.cache_data(ttl=3600, show_spinner="Loading data...")
def load_data():
    data = {}
    missing = []

    for key, path in REQUIRED_FILES.items():
        try:
            data[key] = pd.read_csv(path)
        except FileNotFoundError:
            missing.append(path)
            data[key] = pd.DataFrame()

    return data, missing


data, missing_files = load_data()

if missing_files:
    st.error(
        "⚠️ Some data files could not be found:\n\n"
        + "\n".join(f"- `{f}`" for f in missing_files)
        + "\n\nPlease make sure the `dashboard/` folder is in the app directory."
    )
    st.stop()

kpis = data["kpis"]
monthly = data["monthly"]
countries = data["countries"]
products = data["products"]
hourly = data["hourly"]
segments = data["segments"]
segment_revenue = data["segment_revenue"]
rfm = data["rfm"]


# ============================================================
# DATA PREPARATION
# ============================================================

# Monthly data

if "YearMonth" not in monthly.columns:

    if (
        "Year" in monthly.columns
        and "Month" in monthly.columns
    ):

        monthly["YearMonth"] = (
            monthly["Year"].astype(str)
            + "-"
            + monthly["Month"].astype(str).str.zfill(2)
        )


HAS_YEAR_MONTH_COLS = (
    "Year" in monthly.columns
    and "Month" in monthly.columns
)

if HAS_YEAR_MONTH_COLS:

    monthly = monthly.sort_values(
        ["Year", "Month"]
    )

else:

    monthly = monthly.sort_values(
        "YearMonth"
    )


# Product descriptions

if "Description" in products.columns:

    products["Description"] = (
        products["Description"]
        .fillna("Unknown Product")
    )


# Consistent color mapping for segments (used in pie, bar, scatter)

if "Segment" in segments.columns:
    unique_segments = sorted(segments["Segment"].dropna().unique().tolist())
else:
    unique_segments = []

SEGMENT_COLOR_MAP = {
    seg: COLOR_SEQUENCE[i % len(COLOR_SEQUENCE)]
    for i, seg in enumerate(unique_segments)
}


# ============================================================
# PLOTLY SETTINGS
# ============================================================

PLOT_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "responsive": True
}


def apply_plot_style(fig, height=430):

    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color="#374151"
        ),
        margin=dict(
            l=45,
            r=25,
            t=30,
            b=45
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def card_start():
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)


def card_end():
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(" E-Commerce Analytics")

    st.caption(
        "Big Data Analytics Dashboard"
    )

    st.divider()

    st.subheader("Navigation")

    page = st.radio(
        "Select analysis",
        [
            "Overview",
            "Sales Analysis",
            "Customer Analysis"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.subheader("Technology")

    st.caption("Data Processing")
    st.write("PySpark")

    st.caption("Dashboard")
    st.write("Streamlit")

    st.caption("Visualization")
    st.write("Plotly")

    st.divider()

    st.caption(
        "Online Retail Analytics Project"
    )

    st.caption(
        f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="page-title">'
    'E-Commerce Big Data Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Interactive analysis of sales performance, '
    'customer behavior, and revenue trends'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "Overview":

    # --------------------------------------------------------
    # KPI VALUES
    # --------------------------------------------------------

    total_revenue = kpis.loc[0, "TotalRevenue"]
    total_orders = kpis.loc[0, "TotalOrders"]
    total_customers = kpis.loc[0, "TotalCustomers"]
    total_products = kpis.loc[0, "TotalProducts"]

    # Optional MoM revenue growth, if enough monthly history exists
    revenue_delta_label = None
    if len(monthly) >= 2:
        last_rev = monthly["Revenue"].iloc[-1]
        prev_rev = monthly["Revenue"].iloc[-2]
        delta = pct_delta(last_rev, prev_rev)
        if delta is not None:
            revenue_delta_label = f"{delta:+.1f}% vs prior month"

    # --------------------------------------------------------
    # KPI ROW
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Revenue",
            fmt_currency(total_revenue),
            # delta=revenue_delta_label
        )

    with col2:
        st.metric("Total Orders", fmt_int(total_orders))

    with col3:
        st.metric("Total Customers", fmt_int(total_customers))

    with col4:
        st.metric("Total Products", fmt_int(total_products))

    st.markdown("---")

    # --------------------------------------------------------
    # REVENUE TREND
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-header">Revenue Trend</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-description">'
        'Monthly revenue performance over time'
        '</div>',
        unsafe_allow_html=True
    )

    card_start()

    fig = px.line(
        monthly,
        x="YearMonth",
        y="Revenue",
        markers=True,
        color_discrete_sequence=[ACCENT]
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=7),
        fill="tozeroy",
        fillcolor="rgba(79, 70, 229, 0.08)"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title=f"Revenue ({CURRENCY_SYMBOL})",
        hovermode="x unified"
    )

    fig = apply_plot_style(fig, height=430)

    st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    card_end()

    # --------------------------------------------------------
    # COUNTRY + SEGMENTS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="section-header">Top Countries</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-description">'
            'Countries generating the highest revenue'
            '</div>',
            unsafe_allow_html=True
        )

        card_start()

        top_countries = countries.head(10).copy()

        fig = px.bar(
            top_countries,
            x="Revenue",
            y="Country",
            orientation="h",
            color_discrete_sequence=[ACCENT],
            text="Revenue"
        )

        fig.update_traces(
            texttemplate=f"{CURRENCY_SYMBOL}%{{text:,.0f}}",
            textposition="outside"
        )

        fig.update_yaxes(categoryorder="total ascending")
        fig.update_layout(xaxis_title=f"Revenue ({CURRENCY_SYMBOL})", yaxis_title="")

        fig = apply_plot_style(fig, height=450)

        st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

        card_end()

    with col2:
        st.markdown(
            '<div class="section-header">Customer Segments</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="section-description">'
            'Distribution of customers across RFM segments'
            '</div>',
            unsafe_allow_html=True
        )

        card_start()

        fig = px.pie(
            segments,
            names="Segment",
            values="count",
            hole=0.55,
            color="Segment",
            color_discrete_map=SEGMENT_COLOR_MAP
        )

        fig.update_traces(textinfo="percent+label")

        fig = apply_plot_style(fig, height=450)

        st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

        card_end()


# ============================================================
# SALES ANALYSIS
# ============================================================

elif page == "Sales Analysis":

    st.markdown(
        '<div class="section-header">Sales Performance</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-description">'
        'Detailed analysis of revenue, countries, products, '
        'and sales timing'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # MONTHLY REVENUE
    # --------------------------------------------------------

    st.subheader("Monthly Revenue")

    compare_years = False
    if HAS_YEAR_MONTH_COLS and monthly["Year"].nunique() > 1:
        compare_years = st.toggle(
            "Compare years side by side",
            value=False
        )

    card_start()

    if compare_years:
        fig = px.line(
            monthly,
            x="Month",
            y="Revenue",
            color="Year",
            markers=True,
            color_discrete_sequence=COLOR_SEQUENCE
        )
        fig.update_layout(xaxis=dict(dtick=1))
    else:
        fig = px.area(
            monthly,
            x="YearMonth",
            y="Revenue",
            color_discrete_sequence=[ACCENT]
        )
        fig.update_traces(line=dict(width=2))

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title=f"Revenue ({CURRENCY_SYMBOL})",
        hovermode="x unified"
    )

    fig = apply_plot_style(fig, height=450)

    st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    card_end()

    # --------------------------------------------------------
    # COUNTRY ANALYSIS
    # --------------------------------------------------------

    st.subheader("Geographic Sales Performance")

    country_limit = st.slider(
        "Number of countries",
        min_value=5,
        max_value=min(20, len(countries)),
        value=min(10, len(countries))
    )

    card_start()

    top_countries = countries.head(country_limit)

    fig = px.bar(
        top_countries,
        x="Revenue",
        y="Country",
        orientation="h",
        color_discrete_sequence=[ACCENT]
    )

    fig.update_yaxes(categoryorder="total ascending")
    fig.update_layout(xaxis_title=f"Revenue ({CURRENCY_SYMBOL})", yaxis_title="")

    fig = apply_plot_style(fig, height=550)

    st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    card_end()

    # --------------------------------------------------------
    # PRODUCT ANALYSIS
    # --------------------------------------------------------

    st.subheader("Top Performing Products")

    product_limit = st.slider(
        "Number of products",
        min_value=5,
        max_value=min(20, len(products)),
        value=min(10, len(products))
    )

    card_start()

    top_products = products.head(product_limit).copy()

    top_products["ShortDescription"] = (
        top_products["Description"].astype(str).str[:50]
    )

    fig = px.bar(
        top_products,
        x="Revenue",
        y="ShortDescription",
        orientation="h",
        color_discrete_sequence=[ACCENT]
    )

    fig.update_yaxes(categoryorder="total ascending")
    fig.update_layout(xaxis_title=f"Revenue ({CURRENCY_SYMBOL})", yaxis_title="")

    fig = apply_plot_style(fig, height=600)

    st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    card_end()

    # --------------------------------------------------------
    # HOURLY SALES
    # --------------------------------------------------------

    st.subheader("Revenue by Hour")

    card_start()

    fig = px.line(
        hourly,
        x="Hour",
        y="Revenue",
        markers=True,
        color_discrete_sequence=[ACCENT]
    )

    fig.update_traces(line=dict(width=3), marker=dict(size=7))
    fig.update_layout(
        xaxis=dict(dtick=1),
        xaxis_title="Hour of Day",
        yaxis_title=f"Revenue ({CURRENCY_SYMBOL})"
    )

    fig = apply_plot_style(fig, height=430)

    st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    card_end()


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

elif page == "Customer Analysis":

    st.markdown(
        '<div class="section-header">Customer Analytics</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-description">'
        'Customer segmentation and RFM-based behavioral analysis'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # REVENUE BY SEGMENT
    # --------------------------------------------------------

    st.subheader("Revenue by Customer Segment")

    card_start()

    fig = px.bar(
        segment_revenue,
        x="Segment",
        y="Revenue",
        color="Segment",
        color_discrete_map=SEGMENT_COLOR_MAP
    )

    fig.update_layout(
        xaxis_title="Customer Segment",
        yaxis_title=f"Revenue ({CURRENCY_SYMBOL})",
        showlegend=False
    )

    fig = apply_plot_style(fig, height=450)

    st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

    card_end()

    # --------------------------------------------------------
    # SEGMENT DISTRIBUTION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Distribution")

        card_start()

        fig = px.pie(
            segments,
            names="Segment",
            values="count",
            hole=0.55,
            color="Segment",
            color_discrete_map=SEGMENT_COLOR_MAP
        )

        fig.update_traces(textinfo="percent+label")

        fig = apply_plot_style(fig, height=430)

        st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

        card_end()

    with col2:
        st.subheader("Customers by Segment")

        card_start()

        fig = px.bar(
            segments,
            x="Segment",
            y="count",
            color="Segment",
            color_discrete_map=SEGMENT_COLOR_MAP
        )

        fig.update_layout(
            xaxis_title="Segment",
            yaxis_title="Customers",
            showlegend=False
        )

        fig = apply_plot_style(fig, height=430)

        st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

        card_end()

    # --------------------------------------------------------
    # RFM EXPLORER
    # --------------------------------------------------------

    st.subheader("RFM Customer Explorer")

    selected_segments = st.multiselect(
        "Customer Segment",
        options=sorted(rfm["Segment"].dropna().unique().tolist()),
        default=sorted(rfm["Segment"].dropna().unique().tolist())
    )

    filtered_rfm = rfm[rfm["Segment"].isin(selected_segments)].copy()

    # --------------------------------------------------------
    # RFM METRICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Customers", fmt_int(len(filtered_rfm)))

    with col2:
        avg_frequency = filtered_rfm["Frequency"].mean() if len(filtered_rfm) else 0
        st.metric("Average Frequency", f"{avg_frequency:.2f}")

    with col3:
        avg_monetary = filtered_rfm["Monetary"].mean() if len(filtered_rfm) else 0
        st.metric("Average Monetary Value", fmt_currency(avg_monetary))

    # --------------------------------------------------------
    # RFM SCATTER (Recency vs Monetary)
    # --------------------------------------------------------

    if {"Recency", "Monetary", "Frequency"}.issubset(filtered_rfm.columns) and len(filtered_rfm):

        card_start()

        fig = px.scatter(
            filtered_rfm,
            x="Recency",
            y="Monetary",
            size="Frequency",
            color="Segment",
            color_discrete_map=SEGMENT_COLOR_MAP,
            opacity=0.7,
            hover_data=["CustomerID"] if "CustomerID" in filtered_rfm.columns else None
        )

        fig.update_layout(
            xaxis_title="Recency (days)",
            yaxis_title=f"Monetary Value ({CURRENCY_SYMBOL})"
        )

        fig = apply_plot_style(fig, height=430)

        st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)

        card_end()

    # --------------------------------------------------------
    # RFM TABLE
    # --------------------------------------------------------

    display_columns = [
        "CustomerID", "Recency", "Frequency",
        "Monetary", "RFM_Score", "Segment"
    ]

    available_columns = [
        column for column in display_columns
        if column in filtered_rfm.columns
    ]

    customer_table = (
        filtered_rfm[available_columns]
        .sort_values("Monetary", ascending=False)
        .head(100)
    )

    st.dataframe(
        customer_table,
        use_container_width=True,
        hide_index=True,
        height=450
    )

    st.download_button(
        "Download filtered customer list (CSV)",
        data=filtered_rfm[available_columns].to_csv(index=False).encode("utf-8"),
        file_name="rfm_customers_filtered.csv",
        mime="text/csv"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-text">
        E-Commerce Big Data Analytics |
        PySpark | Streamlit | Plotly
    </div>
    """,
    unsafe_allow_html=True
)