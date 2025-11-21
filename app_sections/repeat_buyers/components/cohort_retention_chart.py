import streamlit as st
import pandas as pd
import altair as alt


def cohort_retention_chart(cohorts: pd.DataFrame):

    df = cohorts.copy()

    # --- Convert cohort month (safe) ---
    df["cohort_month"] = pd.to_datetime(df["cohort_month"], errors="coerce")
    df = df[df["cohort_month"].notna()].copy()  # drop invalid dates
    df["year"] = df["cohort_month"].dt.year
    df["cohort_month_str"] = df["cohort_month"].dt.strftime("%Y-%m")

    # --- Detect m1, m2, m3 ... ---
    retention_cols = [c for c in df.columns if c.startswith("m") and c[1:].isdigit()]
    retention_cols = sorted(retention_cols, key=lambda x: int(x[1:]))

    if not retention_cols:
        st.warning("⚠ No retention columns found (expected m1, m2, …).")
        return

    # ============================================================
    # 🟦 YEAR FILTER (slider)
    # ============================================================
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())

    st.subheader("📅 Select Cohort Year Range")

    year_range = st.slider(
        "Filter cohorts by year:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1,
    )

    df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]
    if df.empty:
        st.warning("No cohorts in this year range.")
        return

    # --- Melt into long format ---
    heatmap = df.melt(
        id_vars="cohort_month_str",
        value_vars=retention_cols,
        var_name="month",
        value_name="retention"
    )

    heatmap["month_num"] = heatmap["month"].apply(lambda x: int(x[1:]))
    heatmap["month"] = heatmap["month_num"].apply(lambda x: f"Month {x}")
    heatmap["retention"] = heatmap["retention"].fillna(0)

    # ================================
    # 📐 IMPROVED VISUAL DESIGN
    # ================================
    ROW_HEIGHT = 24  # bigger rows
    chart_height = ROW_HEIGHT * heatmap["cohort_month_str"].nunique()

    base = alt.Chart(heatmap).encode(
        x=alt.X(
            "month:N",
            sort=sorted(heatmap["month"].unique(), key=lambda x: int(x.split()[1])),
            axis=alt.Axis(labelFontSize=14, labelAngle=0, title="Period"),
        ),
        y=alt.Y(
            "cohort_month_str:N",
            sort="descending",
            axis=alt.Axis(labelFontSize=14, title="Cohort Month"),
        ),
    )

    rects = base.mark_rect().encode(
        color=alt.Color(
            "retention:Q",
            scale=alt.Scale(
                domain=[0, max(heatmap["retention"].max(), 8)],
                scheme="blues",
            ),
            title="Retention %"
        ),
        tooltip=[
            "cohort_month_str",
            "month",
            alt.Tooltip("retention:Q", format=".1f")
        ],
    )

    labels = base.mark_text(
        fontSize=12,
        color="black",
        baseline="middle"
    ).encode(
        text=alt.condition(
            "datum.retention > 0",
            alt.Text("retention:Q", format=".1f"),
            alt.value("")
        )
    )

    final_chart = (rects + labels).properties(
        height=chart_height,
        width="container",
        title="📊 Cohort Retention Heatmap"
    )

    st.altair_chart(final_chart, use_container_width=True)
