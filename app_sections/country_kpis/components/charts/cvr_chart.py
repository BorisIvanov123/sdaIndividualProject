import streamlit as st
import pandas as pd


def cvr_chart(df: pd.DataFrame):
    """
    Renders the CVR percentage line chart.

    Args:
        df: DataFrame indexed by country with a 'cvr' column
    """
    st.markdown("### 📈 Conversion Rate (CVR) by Country")

    if "cvr" not in df.columns:
        st.warning("CVR column not found in the dataset.")
        return

    if df.empty:
        st.warning("No data available for CVR chart.")
        return

    cvr_df = df[["cvr"]].copy()
    cvr_df["CVR %"] = cvr_df["cvr"] * 100

    # Sort to match revenue ordering if present
    if "revenue_eur" in df.columns:
        cvr_df = cvr_df.sort_values("CVR %", ascending=False)

    st.line_chart(cvr_df[["CVR %"]])
