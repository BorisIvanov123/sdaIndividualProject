# app.py

import streamlit as st
from pathlib import Path

from utils.loaders import load_all_data

# Section imports
from app_sections.overview.render import render as overview_render
from app_sections.country_kpis.render import render as country_render
from app_sections.seasonality.render import render as seasonality_render
from app_sections.funnel.render import render as funnel_render
from app_sections.repeat_buyers.render import render as repeat_render
from app_sections.forecast.render import render as forecast_render   # <-- takes (history, forecast_df)

# Streamlit page settings
st.set_page_config(page_title="Sales Management Dashboard", layout="wide")

# Page router
PAGES = {
    "Overview": overview_render,
    "Country KPIs": country_render,
    "Seasonality": seasonality_render,
    "Funnel": funnel_render,
    "Repeat Buyers": repeat_render,
    "Forecast (DL)": forecast_render,
}

# --- Global CSS loader ---
def load_global_css():
    css_path = Path("app_components/styles/global.css")
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():

    load_global_css()

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to:", list(PAGES.keys()))

    # Load EVERYTHING including forecast data now
    (
        order_header_df,
        funnel_df,
        line_items,
        sessions,
        cohorts,
        country_kpis,
        forecast_df,
        weekly_history,
    ) = load_all_data()

    # ROUTER
    if selection == "Overview":
        PAGES[selection](order_header_df, sessions)

    elif selection == "Country KPIs":
        PAGES[selection](country_kpis)

    elif selection == "Seasonality":
        PAGES[selection](order_header_df)

    elif selection == "Funnel":
        PAGES[selection](sessions)

    elif selection == "Repeat Buyers":
        PAGES[selection](order_header_df, cohorts)

    elif selection == "Forecast (DL)":
        # Forecast takes two arguments now
        PAGES[selection](weekly_history, forecast_df)


if __name__ == "__main__":
    main()
