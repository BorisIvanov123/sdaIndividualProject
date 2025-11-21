import streamlit as st
import pandas as pd


def repeat_share_chart(order_header_df: pd.DataFrame):
    """Renders first-time vs repeat buyers share."""

    completed = order_header_df[order_header_df["status"] == "COMPLETED"]

    share = (
        completed["is_first_purchase"]
        .value_counts(normalize=True)
        .rename({True: "First-time", False: "Repeat"})
        * 100
    )

    st.subheader("First-Time vs Repeat Order Share")
    st.bar_chart(share)
