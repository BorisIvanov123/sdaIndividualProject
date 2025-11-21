import streamlit as st
import pandas as pd

# Global components
from app_components.layout import centered_title
from app_components.tables import data_table

# Local components
from .components.charts.monthly_chart import prepare_monthly_data, monthly_chart
from .components.charts.yoy_mom_charts import yoy_chart, mom_chart
from .components.charts.seasonal_decomposition_chart import seasonal_decomposition_chart
from .components.charts.seasonal_heatmap import seasonal_heatmap
from .components.charts.anomaly_detection_chart import anomaly_detection_chart
from .components.seasonality_intro_html import FULL_SEASONALITY_HTML


def render(order_header_df: pd.DataFrame):

    # =======================
    # HEADER + INTRO
    # =======================
    centered_title("📆 Seasonality & Trends")
    st.markdown(FULL_SEASONALITY_HTML, unsafe_allow_html=True)

    # =======================
    # PREPARE MONTHLY AGG DATA
    # =======================
    monthly = prepare_monthly_data(order_header_df)

    st.markdown("<br>", unsafe_allow_html=True)

    # =======================
    # TABLE VIEW
    # =======================
    st.markdown("### 📋 Monthly Table")
    data_table(monthly, title=None)

    st.markdown("<br>", unsafe_allow_html=True)

    # =======================
    # TOP SECTION — Monthly Trend
    # =======================
    st.markdown("### 🔍 Choose Main Metric")
    main_metric = st.selectbox(
        "Metric for Monthly Trend",
        ["Revenue", "Orders"],
        index=0
    )

    monthly_chart(monthly, main_metric)

    st.markdown("<br>", unsafe_allow_html=True)

    # =======================
    # SEASONAL DECOMPOSITION
    # =======================
    st.markdown("### 🧩 Seasonal Decomposition")
    seasonal_decomposition_chart(monthly, main_metric)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # =======================
    # SECOND SELECTOR — YoY / MoM / Heatmap / Anomaly Detection
    # =======================
    st.markdown("### 📊 Additional Seasonal Analysis")

    second_choice = st.selectbox(
        "Additional Analysis",
        ["YoY Comparison", "MoM % Change", "Seasonal Heatmap", "Anomaly Detection"],
        index=0
    )

    if second_choice == "YoY Comparison":
        yoy_chart(monthly, main_metric)

    elif second_choice == "MoM % Change":
        mom_chart(monthly, main_metric)

    elif second_choice == "Seasonal Heatmap":
        seasonal_heatmap(monthly, main_metric)

    elif second_choice == "Anomaly Detection":
        anomaly_detection_chart(monthly, main_metric)

    st.markdown("<br>", unsafe_allow_html=True)
