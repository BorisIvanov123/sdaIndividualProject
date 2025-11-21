import streamlit as st

# Global components
from app_components.cards import metric_card
from app_components.tables import data_table

# Local components (overview page)
from .components.layout import centered_title
from .components.intro import intro_section


def render(order_header_df, sessions):

    # =======================
    # PAGE HEADER
    # =======================
    centered_title("📊 Overview")
    intro_section()

    # =======================
    # KPI CARDS
    # =======================
    total_rev = (
        order_header_df[order_header_df["status"] == "COMPLETED"]["amount_eur"]
        .sum()
    )
    total_orders = order_header_df["order_id"].nunique()
    total_sessions = sessions["sessionid"].nunique()

    col_spacer_l, col1, col2, col3, col_spacer_r = st.columns([1, 2, 2, 2, 1])

    with col1:
        metric_card("Revenue (EUR)", f"{total_rev:,.0f}", "#4CAF50")

    with col2:
        metric_card("Orders", f"{total_orders:,}", "#29B6F6")

    with col3:
        metric_card("Sessions", f"{total_sessions:,}", "#FFB300")

    st.markdown("<br>", unsafe_allow_html=True)

    # =======================
    # DATA PREVIEW
    # =======================
    st.markdown("### 📋 Data Preview")

    col1, col2 = st.columns(2)

    with col1:
        data_table(order_header_df.head(), title="Orders Sample")

    with col2:
        data_table(sessions.head(), title="Sessions Sample")
