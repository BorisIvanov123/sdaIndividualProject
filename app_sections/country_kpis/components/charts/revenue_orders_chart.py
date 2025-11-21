import streamlit as st
import pandas as pd
import altair as alt


def revenue_orders_chart(df: pd.DataFrame, metric: str):
    """
    Interactive bar chart for either Revenue OR Orders.
    Separate controls for viewing Top N, Bottom N, or All countries.
    """

    titles = {
        "revenue_eur": "Revenue (€)",
        "orders": "Orders"
    }

    colors = {
        "revenue_eur": "#4CAF50",
        "orders": "#2196F3"
    }

    st.markdown(f"### 📊 {titles[metric]} by Country")

    if metric not in df.columns:
        st.warning(f"{metric} column not found in dataset.")
        return

    # Base dataframe
    chart_df = df[[metric]].copy().reset_index()
    chart_df = chart_df.sort_values(metric, ascending=False)

    total_countries = len(chart_df)

    # ===============================
    # 🎚 STYLED LAYOUT: Radio + Slider
    # ===============================
    col1, col2, col3 = st.columns([1.2, 3, 0.3])

    with col1:
        st.markdown('<div class="view-label">Filter Mode</div>', unsafe_allow_html=True)
        view_mode = st.radio(
            "view_mode_selector",
            options=["📋 All", "🔝 Top N", "⬇️ Bottom N"],
            label_visibility="collapsed",
        )

    with col2:
        st.markdown('<div class="view-label" style="visibility: hidden;">Placeholder</div>', unsafe_allow_html=True)

        if "Top N" in view_mode:
            n = st.slider(
                "🔝 Number of top performing countries",
                min_value=1,
                max_value=total_countries,
                value=min(10, total_countries),
                key="top_slider",
            )
            chart_df = chart_df.head(n)

        elif "Bottom N" in view_mode:
            n = st.slider(
                "⬇️ Number of bottom performing countries",
                min_value=1,
                max_value=total_countries,
                value=min(10, total_countries),
                key="bottom_slider",
            )
            chart_df = chart_df.tail(n)

        else:
            st.markdown(
                f'<div class="all-countries-msg">📊 Displaying all <strong>{total_countries}</strong> countries</div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="chart-spacer"></div>', unsafe_allow_html=True)

    # ===============================
    # Dynamic bar size with better scaling
    # ===============================
    num_bars = len(chart_df)

    if num_bars <= 10:
        bar_size = 40
        height = 450
    elif num_bars <= 20:
        bar_size = 25
        height = 500
    elif num_bars <= 50:
        bar_size = 15
        height = 600
    else:
        bar_size = 10
        height = 700

    # ===============================
    # Enhanced Chart with better formatting
    # ===============================
    chart = (
        alt.Chart(chart_df)
        .mark_bar(
            size=bar_size,
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4,
            stroke="white",
            strokeWidth=1,
            opacity=0.9
        )
        .encode(
            x=alt.X(
                "country:N",
                sort=None,
                title="Country",
                axis=alt.Axis(
                    labelAngle=-45,
                    labelFontSize=11,
                    ticks=False,
                    labelLimit=100
                ),
            ),
            y=alt.Y(
                f"{metric}:Q",
                title=titles[metric],
                axis=alt.Axis(
                    grid=True,
                    gridOpacity=0.15,
                    format=",.0f" if metric == "orders" else ",.2f"
                ),
                scale=alt.Scale(zero=True)
            ),
            color=alt.value(colors[metric]),
            tooltip=[
                alt.Tooltip("country:N", title="Country"),
                alt.Tooltip(
                    metric,
                    title=titles[metric],
                    format=",.0f" if metric == "orders" else ",.2f"
                ),
            ],
        )
        .properties(
            height=height,
        )
        .configure_view(
            strokeWidth=0
        )
    )

    st.altair_chart(chart, use_container_width=True)
