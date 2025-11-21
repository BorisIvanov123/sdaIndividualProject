import streamlit as st
import pandas as pd
import altair as alt


def prepare_monthly_data(order_header_df: pd.DataFrame) -> pd.DataFrame:
    df = order_header_df.copy()
    df["createdate"] = pd.to_datetime(df["createdate"], errors="coerce")

    df = df[df["status"] == "COMPLETED"].dropna(subset=["createdate"])
    df["YearMonth"] = df["createdate"].dt.to_period("M")

    monthly = df.groupby("YearMonth").agg(
        Orders=("order_id", "nunique"),
        Revenue=("amount_eur", "sum"),
    ).reset_index()

    monthly["YearMonth"] = monthly["YearMonth"].dt.to_timestamp()
    return monthly



def monthly_chart(monthly: pd.DataFrame, metric: str):

    titles = {
        "Revenue": "💶 Monthly Revenue Trend",
        "Orders": "📦 Monthly Orders Trend",
    }

    colors = {
        "Revenue": "#4CAF50",
        "Orders": "#2196F3",
    }

    st.markdown(f"### {titles[metric]}")

    # ======================================================
    # ⭐ EVENTS — ONLY CHRISTMAS
    # ======================================================
    recurring_events = [
        {"month": 12, "day": 25, "label": "Christmas"},
    ]

    years = sorted(monthly["YearMonth"].dt.year.unique())
    events_list = []

    for yr in years:
        for ev in recurring_events:
            dt = pd.Timestamp(year=yr, month=ev["month"], day=ev["day"])
            if monthly["YearMonth"].min() <= dt <= monthly["YearMonth"].max():
                events_list.append({
                    "date": dt,
                    "label": ev["label"],
                    "offset": -25,   # nice single offset
                })

    events_df = pd.DataFrame(events_list)

    # ======================================================
    # MAIN CHART
    # ======================================================
    base = alt.Chart(monthly)

    line = (
        base.mark_line(strokeWidth=3, interpolate="monotone")
        .encode(
            x=alt.X("YearMonth:T", title="Month"),
            y=alt.Y(f"{metric}:Q", title=metric),
            color=alt.value(colors[metric]),
        )
    )

    points = (
        base.mark_circle(size=180, filled=True, opacity=0.9)
        .encode(
            x="YearMonth:T",
            y=f"{metric}:Q",
            color=alt.value(colors[metric]),
            tooltip=[
                alt.Tooltip("YearMonth:T", title="Month"),
                alt.Tooltip(f"{metric}:Q", format=",.0f"),
            ],
        )
    )

    # ======================================================
    # EVENT MARKERS — ONLY CHRISTMAS
    # ======================================================
    if not events_df.empty:

        event_line = (
            alt.Chart(events_df)
            .mark_rule(
                stroke="red",
                strokeDash=[4, 4],
                strokeWidth=1.5,
                opacity=0.7,
            )
            .encode(x="date:T")
        )

        event_label = (
            alt.Chart(events_df)
            .mark_text(
                fontSize=12,
                fontWeight=600,
                color="red",
                align="center",
                baseline="bottom",
                dy=-25,  # simple offset for a single label
            )
            .encode(
                x="date:T",
                text="label:N",
            )
        )

        chart = (line + points + event_line + event_label).properties(
            height=450,
            padding={"top": 60, "left": 10, "right": 10, "bottom": 10},
        )

    else:
        chart = (line + points).properties(height=450)

    st.altair_chart(chart, use_container_width=True)
