import streamlit as st
import pandas as pd
import altair as alt


def seasonal_heatmap(monthly: pd.DataFrame, metric: str):
    """
    Seasonal heatmap: Month × Year, colored by metric value.
    Fully fixed to avoid rendering issues.
    """

    st.markdown(f"### 📅 Seasonal Heatmap — {metric}")

    df = monthly.copy()

    # --- FIX 1: Extract Year + Month as integers ---
    df["Year"] = df["YearMonth"].dt.year.astype(int)
    df["Month"] = df["YearMonth"].dt.month.astype(int)

    # --- FIX 2: Ensure metric is numeric ---
    df[metric] = pd.to_numeric(df[metric], errors="coerce")

    # No data? Show warning.
    if df[metric].isna().all():
        st.warning(f"No numeric data available for metric '{metric}'")
        return

    heatmap = (
        alt.Chart(df)
        .mark_rect()
        .encode(
            x=alt.X("Month:O", title="Month (1–12)"),
            y=alt.Y("Year:O", title="Year"),
            color=alt.Color(
                f"{metric}:Q",
                scale=alt.Scale(scheme="blues"),
                title=metric
            ),
            tooltip=[
                alt.Tooltip("Year:O"),
                alt.Tooltip("Month:O"),
                alt.Tooltip(f"{metric}:Q", format=",.0f"),
            ],
        )
        .properties(
            height=350,
            width="container"
        )
    )

    st.altair_chart(heatmap, use_container_width=True)
