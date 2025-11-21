# app_components/cards.py

import streamlit as st

def metric_card(title: str, value, color: str = "#4CAF50"):
    """
    Reusable KPI card with title + value.
    """
    st.markdown(f"""
        <div style="
            background-color: rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.08);
        ">
            <h4 style="color:#AAAAAA; margin-bottom:5px;">{title}</h4>
            <h2 style="color:{color}; margin-top:0px;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)
