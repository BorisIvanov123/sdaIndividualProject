# app_sections/country_kpis.py

import streamlit as st
import pandas as pd


def render(country_kpis: pd.DataFrame):
    st.header("🌍 Country KPIs")

    if country_kpis is None or country_kpis.empty:
        st.warning("No country KPI data available.")
        return

    # Work on a copy
    df = country_kpis.copy()

    # Basic cleaning / ordering
    if "revenue_eur" in df.columns:
        df = df.sort_values("revenue_eur", ascending=False)

    # ------------------------------------------------------------------
    # High-level metrics
    # ------------------------------------------------------------------
    total_revenue = df["revenue_eur"].sum()
    total_orders = df["orders"].sum() if "orders" in df.columns else None
    avg_cvr = df["cvr"].mean() if "cvr" in df.columns else None

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue (EUR)", f"{total_revenue:,.0f}")
    if total_orders is not None:
        col2.metric("Total Orders", f"{total_orders:,.0f}")
    if avg_cvr is not None:
        col3.metric("Avg CVR", f"{avg_cvr * 100:,.2f}%")

    # ------------------------------------------------------------------
    # Filters
    # ------------------------------------------------------------------
    st.subheader("Filters")

    countries = df["country"].dropna().unique().tolist()
    default_selection = countries[:10] if len(countries) > 10 else countries

    selected_countries = st.multiselect(
        "Select countries to display",
        options=countries,
        default=default_selection,
    )

    if selected_countries:
        df = df[df["country"].isin(selected_countries)]

    # Allow sorting by metric
    sort_by = st.selectbox(
        "Sort by",
        options=["revenue_eur", "orders", "cvr"],
        index=0 if "revenue_eur" in df.columns else 1,
    )
    sort_ascending = st.checkbox("Sort ascending", value=False)

    if sort_by in df.columns:
        df = df.sort_values(sort_by, ascending=sort_ascending)

    # ------------------------------------------------------------------
    # Table
    # ------------------------------------------------------------------
    st.subheader("Country Detail Table")
    st.dataframe(df.reset_index(drop=True))

    # ------------------------------------------------------------------
    # Charts
    # ------------------------------------------------------------------
    st.subheader("Revenue & Orders by Country")

    chart_df = df.set_index("country")

    # Only plot columns that exist
    cols_for_bar = [c for c in ["revenue_eur", "orders"] if c in chart_df.columns]
    if cols_for_bar:
        st.bar_chart(chart_df[cols_for_bar])

    if "cvr" in chart_df.columns:
        st.subheader("Conversion Rate by Country")
        # Show CVR as percentage
        cvr_chart = chart_df[["cvr"]].copy()
        cvr_chart["cvr_pct"] = cvr_chart["cvr"] * 100
        st.line_chart(cvr_chart[["cvr_pct"]])
