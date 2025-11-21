import streamlit as st
import pandas as pd
from pathlib import Path

from app_sections.forecast.components.forecast_intro_html import forecast_intro_html
from app_sections.forecast.components.charts.forecast_chart import plot_forecast


def render():
    st.markdown(forecast_intro_html, unsafe_allow_html=True)

    # Automatically detect project root (project root = 2 levels above this file)
    BASE_DIR = Path(__file__).resolve().parents[2]

    # Correct path to your trained model directory
    MODELS_DIR = BASE_DIR / "notebooks" / "models"

    # Files inside notebooks/models/
    history_path = MODELS_DIR / "weekly_history.parquet"
    forecast_path = MODELS_DIR / "xgb_forecast_ci.parquet"
    metadata_path = MODELS_DIR / "forecast_metadata.json"

    # Load saved files
    history = pd.read_parquet(history_path)
    forecast_df = pd.read_parquet(forecast_path)

    st.success("Loaded weekly history + forecast.")

    # -------------------------
    # Plot forecast
    # -------------------------
    st.plotly_chart(
        plot_forecast(history, forecast_df),
        use_container_width=True
    )

    # -------------------------
    # Summary numbers
    # -------------------------
    last_hist = history["y"].iloc[-1]
    next_week = forecast_df["mean"].iloc[0]
    growth = (next_week - last_hist) / last_hist * 100

    st.metric(
        label="Next Week Forecast",
        value=f"{next_week:,.0f} €",
        delta=f"{growth:,.1f}%"
    )

    st.write("Forecast horizon:", len(forecast_df), "weeks")
