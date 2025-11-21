import streamlit as st
import pandas as pd

from app_sections.forecast.components.forecast_intro_html import forecast_intro_html
from app_sections.forecast.components.charts.forecast_chart import plot_forecast


def render(history, forecast_df):
    """
    Renders the weekly revenue forecast section.
    Data (history + forecast_df) is provided by load_all_data() in app.py.
    """

    # Intro header
    st.markdown(forecast_intro_html, unsafe_allow_html=True)

    # Confirmation
    st.success("Loaded weekly history + forecast.")

    # -------------------------
    # Plot the forecast
    # -------------------------
    st.plotly_chart(
        plot_forecast(history, forecast_df),
        use_container_width=True
    )

    # -------------------------
    # KPIs
    # -------------------------
    last_hist = history["y"].iloc[-1]
    next_week = forecast_df["mean"].iloc[0]
    growth = (next_week - last_hist) / last_hist * 100

    st.metric(
        label="Next Week Forecast",
        value=f"{next_week:,.0f} €",
        delta=f"{growth:,.1f}%"
    )

    st.write(f"Forecast horizon: **{len(forecast_df)} weeks**")
