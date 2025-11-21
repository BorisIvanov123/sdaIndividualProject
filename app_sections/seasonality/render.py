import streamlit as st
import pandas as pd

# Global components
from app_components.layout import centered_title
from app_components.tables import data_table

# Local components
from .components.monthly_chart import monthly_chart
from .components.seasonality_intro_html import FULL_SEASONALITY_HTML


def render(order_header_df: pd.DataFrame):

    # =======================
    # HEADER + INTRO
    # =======================
    centered_title("📆 Seasonality & Trends")
    st.markdown(FULL_SEASONALITY_HTML, unsafe_allow_html=True)

    # =======================
    # MONTHLY TREND CHART
    # =======================
    monthly = monthly_chart(order_header_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # =======================
    # TABLE VIEW
    # =======================
    st.markdown("### 📋 Monthly Table")
    data_table(monthly, title=None)
