import streamlit as st
import pandas as pd

# Global components
from app_components.layout import centered_title
from app_components.tables import data_table

# Local components
from .components.funnel_intro_html import FULL_FUNNEL_HTML
from .components.funnel_chart import funnel_chart


def render(sessions: pd.DataFrame):

    # =======================
    # HEADER + INTRO
    # =======================
    centered_title("🪜 Funnel & Exit Behavior")
    st.markdown(FULL_FUNNEL_HTML, unsafe_allow_html=True)

    # =======================
    # CLEAN DATA
    # =======================
    df = sessions.copy()
    df["createdate"] = pd.to_datetime(df["createdate"], errors="coerce")
    df = df.dropna(subset=["createdate"])

    # =======================
    # FUNNEL CHART
    # =======================
    st.markdown("### 🔻 Funnel Performance")
    funnel_chart(df)

    # =======================
    # RAW TABLE
    # =======================
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📋 Funnel Raw Data Sample")
    data_table(df.head(50), title=None)
