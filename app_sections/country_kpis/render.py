import streamlit as st
import pandas as pd

from app_components.cards import metric_card
from app_components.tables import data_table
from app_components.layout import centered_title
from app_components.intro import intro_section


def render(country_kpis: pd.DataFrame):
    """
    Render the Country KPIs section with metrics, table, and charts.

    Args:
        country_kpis: DataFrame containing country-level KPI data
    """

    # ---------------------------------------------
    # TITLE & INTRO
    # ---------------------------------------------
    centered_title("🌍 Country KPIs")

    intro_section(
        text="Performance overview across countries: revenue, orders & conversion rates."
    )

    # ---------------------------------------------
    # Validate Input
    # ---------------------------------------------
    if country_kpis is None or country_kpis.empty:
        st.warning("⚠️ Country KPI dataset is empty or missing.")
        return

    # Work on a copy
    df = country_kpis.copy()

    # Sort by revenue (default behavior)
    if "revenue_eur" in df.columns:
        df = df.sort_values("revenue_eur", ascending=False)

    # ==============================================
    # KPI CARDS (using global component)
    # ==============================================
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

    # ==============================================
    # DATA TABLE (reusable component)
    # ==============================================
    data_table(df.reset_index(drop=True), title="📋 Country Detail Table")

    st.markdown("<br>", unsafe_allow_html=True)

    # ==============================================
    # CHARTS
    # ==============================================
    st.markdown("### 📊 Revenue & Orders by Country")

    chart_df = df.set_index("country")

    # Revenue + Orders bar chart
    numeric_cols = [c for c in ["revenue_eur", "orders"] if c in chart_df.columns]
    if numeric_cols:
        st.bar_chart(chart_df[numeric_cols])

    st.markdown("<br>", unsafe_allow_html=True)

    # CVR Line Chart
    if "cvr" in chart_df.columns:
        st.markdown("### 📈 Conversion Rate (CVR) by Country")
        cvr_chart = chart_df[["cvr"]].copy()
        cvr_chart["CVR %"] = cvr_chart["cvr"] * 100
        st.line_chart(cvr_chart[["CVR %"]])