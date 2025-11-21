import streamlit as st
import pandas as pd
import altair as alt
from statsmodels.tsa.seasonal import STL


def seasonal_decomposition_chart(monthly: pd.DataFrame, metric: str):
    """
    STL Seasonal decomposition chart for monthly Revenue or Orders.
    Uses statsmodels STL decomposition.
    """

    st.markdown(f"### 🔍 Seasonal Decomposition — {metric}")

    # Use only the selected metric
    ts = monthly.set_index("YearMonth")[metric]

    # STL decomposition (period=12 for monthly seasonality)
    stl = STL(ts, period=12, robust=True)
    result = stl.fit()

    # Build DataFrame for plotting
    dec_df = pd.DataFrame({
        "Date": ts.index,
        "Observed": result.observed.values,
        "Trend": result.trend.values,
        "Seasonal": result.seasonal.values,
        "Residual": result.resid.values
    })

    # Helper function to build each line chart
    def _chart(y, title, color):
        return (
            alt.Chart(dec_df)
            .mark_line()
            .encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y(f"{y}:Q", title=title),
                color=alt.value(color)
            )
            .properties(height=150)
        )

    # Build 4 stacked charts
    observed_chart = _chart("Observed", "Observed", "#29B6F6")
    trend_chart = _chart("Trend", "Trend", "#66BB6A")
    seasonal_chart = _chart("Seasonal", "Seasonal", "#FFA726")
    resid_chart = _chart("Residual", "Residual", "#EF5350")

    # Vertical concatenation
    final_chart = observed_chart & trend_chart & seasonal_chart & resid_chart

    st.altair_chart(final_chart, use_container_width=True)
