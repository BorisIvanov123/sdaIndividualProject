import streamlit as st
import pandas as pd

def render(order_header_df, cohorts):
    st.header("🔁 Repeat Buyers & Cohorts")

    completed = order_header_df[order_header_df['status'] == 'COMPLETED']
    share = (
        completed["is_first_purchase"]
        .value_counts(normalize=True)
        .rename({True: "first_time", False: "repeat"}) * 100
    )

    st.subheader("First-Time vs Repeat Order Share")
    st.bar_chart(share)

    cohorts["cohort_month"] = pd.to_datetime(cohorts["cohort_month"])
    st.subheader("Cohort Retention")
    st.dataframe(cohorts)

    st.line_chart(
        cohorts.set_index("cohort_month")[["repeat_rate_3m_%", "repeat_rate_6m_%"]]
    )
