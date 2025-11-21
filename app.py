# app.py

import streamlit as st
from utils.loaders import load_all_data

# Correct imports: import the render function from each section's render.py file
from app_sections.overview.render import render as overview_render
from app_sections.country_kpis.render import render as country_render
from app_sections.seasonality import render as seasonality_render
from app_sections.funnel import render as funnel_render
from app_sections.repeat_buyers import render as repeat_render
from app_sections.forecast import render as forecast_render

st.set_page_config(page_title="Sales Management Dashboard", layout="wide")

PAGES = {
    "Overview": overview_render,
    "Country KPIs": country_render,
    "Seasonality": seasonality_render,
    "Funnel": funnel_render,
    "Repeat Buyers": repeat_render,
    "Forecast (DL)": forecast_render,
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    (
        order_header_df,
        funnel_df,
        line_items,
        sessions,
        cohorts,
        country_kpis
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
        PAGES[selection](order_header_df)


if __name__ == "__main__":
    main()