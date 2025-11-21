import streamlit as st
import pandas as pd
import altair as alt

def cvr_chart(df: pd.DataFrame):
    """
    Renders a clean CVR dot plot with global average reference.
    """

    st.markdown("### 🎯 Conversion Rate (CVR) by Country")

    if "cvr" not in df.columns:
        st.warning("CVR column not found in the dataset.")
        return

    if df.empty:
        st.warning("No data available for CVR chart.")
        return

    # Prepare data
    cvr_df = df[["cvr"]].copy().reset_index()
    cvr_df["cvr_percent"] = cvr_df["cvr"] * 100
    cvr_df = cvr_df.rename(columns={"country": "Country"})

    # Compute global average
    avg_cvr = cvr_df["cvr_percent"].mean()

    # Classification for color
    cvr_df["Performance"] = cvr_df["cvr_percent"].apply(
        lambda x: "Above Avg" if x >= avg_cvr else "Below Avg"
    )

    # Sort for clarity
    cvr_df = cvr_df.sort_values("cvr_percent")

    # Dynamic sizing
    num_countries = len(cvr_df)
    height = min(max(40 * num_countries, 300), 900)

    # Reference line: global average
    ref_line = alt.Chart(pd.DataFrame({"avg": [avg_cvr]})).mark_rule(
        color="#AAAAAA",
        strokeDash=[4, 4],
        size=2
    ).encode(
        x="avg:Q"
    )

    # Dot plot
    dots = alt.Chart(cvr_df).mark_circle(size=180).encode(
        y=alt.Y(
            "Country:N",
            sort=cvr_df["Country"].tolist(),
            axis=alt.Axis(labelLimit=160, labelFontSize=12)
        ),
        x=alt.X(
            "cvr_percent:Q",
            title="CVR (%)",
            axis=alt.Axis(format=".1f")
        ),
        color=alt.Color(
            "Performance:N",
            scale=alt.Scale(
                domain=["Above Avg", "Below Avg"],
                range=["#4CAF50", "#FF7043"]
            ),
            legend=None
        ),
        tooltip=[
            alt.Tooltip("Country:N"),
            alt.Tooltip("cvr_percent:Q", title="CVR", format=".2f"),
            alt.Tooltip("Performance:N"),
        ]
    )

    # Combine
    chart = (ref_line + dots).properties(
        height=height
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        labelColor="rgba(255,255,255,0.9)",
        titleColor="rgba(255,255,255,0.95)"
    )

    st.altair_chart(chart, use_container_width=True)

    # Minimal styling
    st.markdown("""
        <style>
        div[data-testid="stVegaLiteChart"] {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.15);
        }
        </style>
    """, unsafe_allow_html=True)
