import streamlit as st
import pandas as pd
import altair as alt


# ============================================
# YoY COMPARISON CHART
# ============================================
def yoy_chart(monthly: pd.DataFrame, metric: str):

    st.markdown(f"### 📊 Year-over-Year Comparison — {metric}")

    df = monthly.copy()
    df["Year"] = df["YearMonth"].dt.year
    df["Month"] = df["YearMonth"].dt.month

    # Pivot: rows = Month, columns = Year
    pivot = df.pivot(index="Month", columns="Year", values=metric).reset_index()

    melted = pivot.melt(id_vars="Month", var_name="Year", value_name=metric)

    chart = (
        alt.Chart(melted)
        .mark_line(point=True)
        .encode(
            x=alt.X("Month:O", title="Month (1-12)"),
            y=alt.Y(f"{metric}:Q", title=metric),
            color="Year:N",
            tooltip=["Year:N", "Month:O", alt.Tooltip(f"{metric}:Q", format=",.0f")],
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)


# ============================================
# MOM CHANGE CHART
# ============================================
def mom_chart(monthly: pd.DataFrame, metric: str):

    st.markdown(f"### 🔥 Month-over-Month % Change — {metric}")

    df = monthly.copy()
    df = df.sort_values("YearMonth")
    df["MoM_Change"] = df[metric].pct_change() * 100

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("YearMonth:T", title="Month"),
            y=alt.Y("MoM_Change:Q", title="MoM % Change"),
            color=alt.condition(
                alt.datum.MoM_Change >= 0,
                alt.value("#4CAF50"),
                alt.value("#EF5350"),
            ),
            tooltip=[
                alt.Tooltip("YearMonth:T", title="Month"),
                alt.Tooltip("MoM_Change:Q", title="MoM %", format=".2f"),
            ],
        )
        .properties(height=350)
    )

    st.altair_chart(chart, use_container_width=True)
