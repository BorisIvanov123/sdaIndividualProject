import streamlit as st
import pandas as pd

def render(order_header_df):
    st.header("🔮 Forecasting (Deep Learning Coming Soon)")

    df = order_header_df.copy()
    df['createdate'] = pd.to_datetime(df['createdate'], errors='coerce')
    df = df[df['status'] == 'COMPLETED']
    df['YearMonth'] = df['createdate'].dt.to_period('M')

    monthly = df.groupby('YearMonth').agg(Revenue=('amount_eur','sum')).reset_index()
    monthly['YearMonth'] = monthly['YearMonth'].dt.to_timestamp()

    st.write("Current trend (will feed DL model):")
    st.line_chart(monthly.set_index("YearMonth"))
