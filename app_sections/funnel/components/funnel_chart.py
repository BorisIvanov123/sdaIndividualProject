import streamlit as st
import pandas as pd
import altair as alt


def funnel_chart(df: pd.DataFrame):
    """
    Builds:
    - Funnel step metrics
    - Clean Altair funnel line chart with correct step ordering
    """

    # =======================
    # FUNNEL DEFINITIONS
    # =======================
    funnel_counts = {
        "Sessions": df["sessionid"].nunique(),
        "Checkout Intent": df[df["processed"] == True]["sessionid"].nunique(),
        "Orders": df[df["converted"] == True]["sessionid"].nunique(),
    }

    # Show KPI dictionary
    st.markdown("#### Funnel Summary")
    st.json(funnel_counts)

    # =======================
    # CHART PREP
    # =======================
    steps = ["Sessions", "Checkout Intent", "Orders"]
    values = [funnel_counts[s] for s in steps]

    chart_df = pd.DataFrame({"step": steps, "value": values})

    # =======================
    # CHART
    # =======================
    chart = (
        alt.Chart(chart_df)
        .mark_line(point=alt.OverlayMarkDef(size=200, filled=True))
        .encode(
            x=alt.X(
                "step:N",
                sort=steps,                           # << THE FIX
                title="Funnel Step"
            ),
            y=alt.Y("value:Q", title="Count"),
            color=alt.value("#29B6F6"),
            tooltip=[
                alt.Tooltip("step:N"),
                alt.Tooltip("value:Q", format=",.0f")
            ],
        )
        .properties(height=400)
    )

    st.altair_chart(chart, use_container_width=True)
