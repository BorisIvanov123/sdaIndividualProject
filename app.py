import streamlit as st
from utils.loaders import load_all_data

from app_sections import (
    overview,
    country_kpis,
    seasonality,
    funnel,
    repeat_buyers,
    forecast
)

st.set_page_config(page_title="Sales Management Dashboard", layout="wide")

PAGES = {
    "Overview": overview,
    "Country KPIs": country_kpis,
    "Seasonality": seasonality,
    "Funnel": funnel,
    "Repeat Buyers": repeat_buyers,
    "Forecast (DL)": forecast,
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    # UPDATED: now loads 7 datasets including country_kpis
    (
        order_header_df,
        app_clicks,
        funnel_df,
        line_items,
        sessions,
        cohorts,
        country_kpis
    ) = load_all_data()

    # dynamic dispatch
    if selection == "Overview":
        PAGES[selection].render(order_header_df, sessions)

    elif selection == "Country KPIs":
        # UPDATED: use precomputed dataset
        PAGES[selection].render(country_kpis)

    elif selection == "Seasonality":
        PAGES[selection].render(order_header_df)

    elif selection == "Funnel":
        PAGES[selection].render(sessions)

    elif selection == "Repeat Buyers":
        PAGES[selection].render(order_header_df, cohorts)

    elif selection == "Forecast (DL)":
        PAGES[selection].render(order_header_df)


if __name__ == "__main__":
    main()
