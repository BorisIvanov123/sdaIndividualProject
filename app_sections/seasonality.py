import streamlit as st
import pandas as pd

def render(order_header_df):
    st.header("📆 Seasonality & Trends")

    df = order_header_df.copy()
    df['createdate'] = pd.to_datetime(df['createdate'], errors='coerce')
    df = df[df['status'] == "COMPLETED"].dropna(subset=['createdate'])
    df['YearMonth'] = df['createdate'].dt.to_period('M')

    monthly = df.groupby('YearMonth').agg(
        Orders=('order_id', 'nunique'),
        Revenue=('amount_eur', 'sum')
    ).reset_index()

    monthly['YearMonth'] = monthly['YearMonth'].dt.to_timestamp()

    st.line_chart(monthly.set_index("YearMonth")[["Revenue", "Orders"]])

    st.subheader("Monthly Table")
    st.dataframe(monthly)
