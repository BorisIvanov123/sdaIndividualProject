import streamlit as st
import pandas as pd
import altair as alt


def repeat_share_chart(order_header_df: pd.DataFrame):
    """Beautiful first-time vs repeat buyer share chart."""

    completed = order_header_df[order_header_df["status"] == "COMPLETED"]

    # Compute %
    share = (
        completed["is_first_purchase"]
        .value_counts(normalize=True)
        .rename({True: "First-time", False: "Repeat"})
        * 100
    ).reset_index()
    share.columns = ["Type", "Percent"]

    st.subheader("🧭 First-Time vs Repeat Order Share")

    # --- Build nicer chart ---
    chart = (
        alt.Chart(share)
        .mark_bar(size=60, cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X("Type:N", axis=alt.Axis(labelFontSize=14)),
            y=alt.Y("Percent:Q",
                    axis=alt.Axis(format="~%"),  # 0.25 → "25%"
                    title="Share of Orders",
                    scale=alt.Scale(domain=[0, max(share['Percent']) * 1.2])
            ),
            color=alt.Color(
                "Type:N",
                scale=alt.Scale(
                    domain=["First-time", "Repeat"],
                    range=["#4C78A8", "#72B7B2"],   # nice modern blues/greens
                ),
                legend=None
            ),
            tooltip=[
                alt.Tooltip("Type:N"),
                alt.Tooltip("Percent:Q", format=".1f")
            ]
        )
        .properties(width=500, height=350)
    )

    # Add labels above bars
    labels = (
        chart.mark_text(
            dy=-15, size=18, color="#ffffff", fontWeight="bold"
        ).encode(text=alt.Text("Percent:Q", format=".1f"))
    )

    st.altair_chart(chart + labels, use_container_width=True)
