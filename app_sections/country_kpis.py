import streamlit as st
import pandas as pd


def render(country_kpis: pd.DataFrame):

    # ---------------------------------------------
    # TITLE — Centered & polished
    # ---------------------------------------------
    st.markdown("""
        <h1 style='text-align:center; margin-bottom: 5px;'>🌍 Country KPIs</h1>
        <p style='text-align:center; color:#BBBBBB; margin-top:-5px;'>
            Performance overview across countries: revenue, orders & conversion rates.
        </p>
        <br>
    """, unsafe_allow_html=True)

    if country_kpis is None or country_kpis.empty:
        st.warning("⚠️ Country KPI dataset is empty or missing.")
        return

    # Work on a copy
    df = country_kpis.copy()

    # Default ordering (Revenue desc)
    if "revenue_eur" in df.columns:
        df = df.sort_values("revenue_eur", ascending=False)

    # ==============================================
    # KPI CARDS
    # ==============================================
    total_revenue = df["revenue_eur"].sum()
    total_orders = df["orders"].sum()
    avg_cvr = df["cvr"].mean()

    col_spacer_l, col1, col2, col3, col_spacer_r = st.columns([1,2,2,2,1])

    with col1:
        st.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.05);
                        padding:20px; border-radius:12px; text-align:center;">
                <h4 style="color:#AAAAAA;">Total Revenue</h4>
                <h2 style="color:#4CAF50;">€{total_revenue:,.0f}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.05);
                        padding:20px; border-radius:12px; text-align:center;">
                <h4 style="color:#AAAAAA;">Total Orders</h4>
                <h2 style="color:#29B6F6;">{total_orders:,.0f}</h2>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.05);
                        padding:20px; border-radius:12px; text-align:center;">
                <h4 style="color:#AAAAAA;">Average CVR</h4>
                <h2 style="color:#FFB300;">{avg_cvr*100:,.2f}%</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==============================================
    # TABLE (Full dataset)
    # ==============================================
    st.markdown("### 📋 Country Detail Table")
    st.dataframe(df.reset_index(drop=True), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==============================================
    # CHARTS
    # ==============================================
    st.markdown("### 📊 Revenue & Orders by Country")

    chart_df = df.set_index("country")
    cols_for_bar = [c for c in ["revenue_eur", "orders"] if c in chart_df.columns]

    if cols_for_bar:
        st.bar_chart(chart_df[cols_for_bar])

    st.markdown("<br>", unsafe_allow_html=True)

    if "cvr" in chart_df.columns:
        st.markdown("### 📈 Conversion Rate (CVR) by Country")
        cvr_chart = chart_df[["cvr"]].copy()
        cvr_chart["CVR %"] = cvr_chart["cvr"] * 100
        st.line_chart(cvr_chart[["CVR %"]])
