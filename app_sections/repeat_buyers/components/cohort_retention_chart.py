import streamlit as st
import pandas as pd


def cohort_retention_chart(cohorts: pd.DataFrame):
    """Renders cohort table + retention line chart."""

    df = cohorts.copy()
    df["cohort_month"] = pd.to_datetime(df["cohort_month"])

    st.subheader("Cohort Retention Table")
    st.dataframe(df)

    st.subheader("3-Month & 6-Month Repeat Rates")
    st.line_chart(
        df.set_index("cohort_month")[["repeat_rate_3m_%", "repeat_rate_6m_%"]]
    )
