import streamlit as st
import pandas as pd

# Global components
from app_components.cards import metric_card
from app_components.tables import data_table
from app_components.layout import centered_title

# Local intro HTML
from .components.country_kpis_intro_html import FULL_COUNTRY_KPIS_HTML

# Local chart components
from .components.charts.revenue_orders_chart import revenue_orders_chart
from .components.charts.cvr_chart import cvr_chart


def render(country_kpis: pd.DataFrame):
    """
    Render the Country KPIs section using modular components.
    """

    # =======================
    # PAGE HEADER
    # =======================
    centered_title("🌍 Country KPIs")
    st.markdown(FULL_COUNTRY_KPIS_HTML, unsafe_allow_html=True)

    # =======================
    # VALIDATE INPUT
    # =======================
    if country_kpis is None or country_kpis.empty:
        st.warning("⚠️ Country KPI dataset is empty or missing.")
        return

    # Work on copy
    df = country_kpis.copy()

    if "revenue_eur" in df.columns:
        df = df.sort_values("revenue_eur", ascending=False)

    # =======================
    # KPI CARDS
    # =======================
    total_revenue = df["revenue_eur"].sum()
    total_orders = df["orders"].sum()
    avg_cvr = df["cvr"].mean() * 100

    col_spacer_l, col1, col2, col3, col_spacer_r = st.columns([1, 2, 2, 2, 1])

    with col1:
        metric_card("Total Revenue", f"€{total_revenue:,.0f}", "#4CAF50")

    with col2:
        metric_card("Total Orders", f"{total_orders:,.0f}", "#29B6F6")

    with col3:
        metric_card("Average CVR", f"{avg_cvr:.2f}%", "#FFB300")

    st.markdown("<br>", unsafe_allow_html=True)

    # =======================
    # DATA TABLE
    # =======================
    data_table(df.reset_index(drop=True), title="📋 Country Detail Table")

    st.markdown("<br>", unsafe_allow_html=True)

    # =======================
    # CHARTS (modularised)
    # =======================
    # =======================
    # CHARTS (modularised)
    # =======================
    df_indexed = df.set_index("country")

    st.markdown("### 📊 Choose Metric to Visualize")
    metric_choice = st.selectbox(
        "Select a metric:",
        options=["revenue_eur", "orders"],
        format_func=lambda x: "Revenue (€)" if x == "revenue_eur" else "Orders"
    )

    revenue_orders_chart(df_indexed, metric_choice)

    st.markdown("<br>", unsafe_allow_html=True)

    cvr_chart(df_indexed)

