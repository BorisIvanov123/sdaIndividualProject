import streamlit as st
import pandas as pd

from .components.repeat_intro_html import FULL_REPEAT_HTML
from .components.repeat_share_chart import repeat_share_chart
from .components.cohort_retention_chart import cohort_retention_chart


def render(order_header_df: pd.DataFrame, cohorts: pd.DataFrame):

    # Header & intro
    st.header("🔁 Repeat Buyers & Cohorts")
    st.markdown(FULL_REPEAT_HTML, unsafe_allow_html=True)

    # First-time vs repeat share chart
    repeat_share_chart(order_header_df)

    # Cohort retention table + charts
    cohort_retention_chart(cohorts)
