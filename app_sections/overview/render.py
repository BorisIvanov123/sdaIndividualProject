# app_sections/overview/render.py

import streamlit as st

from .components.layout import centered_title
from .components.intro import intro_section
from .components.kpi_cards import render_kpi_cards


def render(order_header_df, sessions):

    # Title
    centered_title("📊 Overview")

    # Intro
    intro_section()

    # KPI Cards
    render_kpi_cards(order_header_df, sessions)

    # Data preview
    st.markdown("### 📋 Data Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Orders Sample")
        st.dataframe(order_header_df.head(), use_container_width=True)

    with col2:
        st.markdown("#### Sessions Sample")
        st.dataframe(sessions.head(), use_container_width=True)
