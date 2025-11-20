# app_sections/overview/components/kpi_cards.py

import streamlit as st
import pandas as pd

def render_kpi_cards(order_header_df: pd.DataFrame, sessions: pd.DataFrame):

    total_rev = order_header_df[order_header_df["status"] == "COMPLETED"]["amount_eur"].sum()
    total_orders = order_header_df["order_id"].nunique()
    total_sessions = sessions["sessionid"].nunique()

    col_spacer_l, col1, col2, col3, col_spacer_r = st.columns([1, 2, 2, 2, 1])

    # Revenue
    with col1:
        st.markdown(
            f"""
            <div style='padding:20px; border-radius:12px; 
                        text-align:center; background:rgba(255,255,255,0.05);'>
                <h4 style='color:#ccc;'>Revenue (EUR)</h4>
                <h2 style='color:#4CAF50;'>{total_rev:,.0f}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Orders
    with col2:
        st.markdown(
            f"""
            <div style='padding:20px; border-radius:12px; 
                        text-align:center; background:rgba(255,255,255,0.05);'>
                <h4 style='color:#ccc;'>Orders</h4>
                <h2 style='color:#29B6F6;'>{total_orders:,}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Sessions
    with col3:
        st.markdown(
            f"""
            <div style='padding:20px; border-radius:12px; 
                        text-align:center; background:rgba(255,255,255,0.05);'>
                <h4 style='color:#ccc;'>Sessions</h4>
                <h2 style='color:#FFB300;'>{total_sessions:,}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
