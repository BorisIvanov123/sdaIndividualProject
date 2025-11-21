import streamlit as st
import pandas as pd
import altair as alt


def prepare_monthly_data(order_header_df: pd.DataFrame) -> pd.DataFrame:
    """Prepare monthly aggregated data for seasonal charts."""

    df = order_header_df.copy()
    df["createdate"] = pd.to_datetime(df["createdate"], errors="coerce")

    # Completed orders only
    df = df[df["status"] == "COMPLETED"].dropna(subset=["createdate"])
    df["YearMonth"] = df["createdate"].dt.to_period("M")

    monthly = df.groupby("YearMonth").agg(
        Orders=("order_id", "nunique"),
        Revenue=("amount_eur", "sum"),
    ).reset_index()

    monthly["YearMonth"] = monthly["YearMonth"].dt.to_timestamp()

    return monthly


def monthly_chart(monthly: pd.DataFrame, metric: str):
    """
    Renders a monthly trend chart based on selected metric (Revenue or Orders).
    """

    titles = {
        "Revenue": "💶 Monthly Revenue Trend",
        "Orders": "📦 Monthly Orders Trend",
    }

    colors = {
        "Revenue": "#4CAF50",
        "Orders": "#2196F3",
    }

    st.markdown(f"### {titles[metric]}")

    chart = (
        alt.Chart(monthly)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("YearMonth:T", title="Month"),
            y=alt.Y(metric + ":Q", title=metric),
            color=alt.value(colors[metric]),
            tooltip=[
                alt.Tooltip("YearMonth:T", title="Month"),
                alt.Tooltip(metric + ":Q", format=",.0f"),
            ],
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)
