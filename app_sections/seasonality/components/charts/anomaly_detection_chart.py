import streamlit as st
import pandas as pd
import altair as alt
from statsmodels.tsa.seasonal import STL


def anomaly_detection_chart(monthly: pd.DataFrame, metric: str, z_threshold: float = 2.5):
    """
    Detect anomalies using STL residuals and flag them on the original time series.
    - monthly: DataFrame with 'YearMonth' (datetime) and metric ('Revenue' or 'Orders')
    - metric: column name to analyze
    - z_threshold: threshold on residual z-score for anomaly flagging
    """

    st.markdown(f"### 🔥 Anomaly Detection — {metric}")

    # Ensure we have data
    if monthly.empty or metric not in monthly.columns:
        st.warning(f"No data available for anomaly detection on '{metric}'.")
        return

    # Prepare time series
    df = monthly.copy().sort_values("YearMonth")
    ts = df.set_index("YearMonth")[metric].astype(float)

    # STL decomposition (monthly seasonality -> period=12)
    try:
        stl = STL(ts, period=12, robust=True)
        result = stl.fit()
    except Exception as e:
        st.error(f"STL decomposition failed: {e}")
        return

    # Build dataframe with residuals and z-scores
    dec_df = pd.DataFrame({
        "Date": ts.index,
        "Value": ts.values,
        "Residual": result.resid
    })

    resid_mean = dec_df["Residual"].mean()
    resid_std = dec_df["Residual"].std(ddof=0) or 1e-9  # avoid division by zero

    dec_df["Z_Score"] = (dec_df["Residual"] - resid_mean) / resid_std
    dec_df["Is_Anomaly"] = dec_df["Z_Score"].abs() >= z_threshold

    anomalies_df = dec_df[dec_df["Is_Anomaly"]]

    # Summary text
    st.markdown(
        f"- Using **STL residual z-score** with threshold **|z| ≥ {z_threshold}**  \n"
        f"- Flagged **{len(anomalies_df)}** anomalies"
    )

    # Base line chart of the metric
    base = (
        alt.Chart(dec_df)
        .mark_line()
        .encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("Value:Q", title=metric),
            tooltip=[alt.Tooltip("Date:T"), alt.Tooltip("Value:Q", format=",.0f")],
        )
        .properties(height=350)
    )

    # Overlay anomaly points
    points = (
        alt.Chart(dec_df[dec_df["Is_Anomaly"]])
        .mark_point(size=120, filled=True)
        .encode(
            x="Date:T",
            y="Value:Q",
            color=alt.value("#EF5350"),
            tooltip=[
                alt.Tooltip("Date:T", title="Date"),
                alt.Tooltip("Value:Q", title=metric, format=",.0f"),
                alt.Tooltip("Z_Score:Q", title="z-score", format=".2f"),
            ],
        )
    )

    chart = base + points

    st.altair_chart(chart, use_container_width=True)

    if not anomalies_df.empty:
        st.markdown("#### 🚩 Flagged Anomalies")

        # Expand container width fully
        st.markdown(
            """
            <style>
                .big-table .stDataFrame { 
                    height: 450px !important; 
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        with st.container():
            st.markdown('<div class="big-table">', unsafe_allow_html=True)

            st.dataframe(
                anomalies_df[["Date", "Value", "Z_Score"]]
                .sort_values("Date")
                .rename(columns={"Value": metric}),
                use_container_width=True,
                height=450  # 👈 bigger table height
            )

            st.markdown('</div>', unsafe_allow_html=True)

