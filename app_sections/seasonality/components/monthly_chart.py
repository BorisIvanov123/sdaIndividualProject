import streamlit as st
import pandas as pd

def monthly_chart(order_header_df: pd.DataFrame):
    """
    Renders a monthly seasonality line chart for revenue and orders.
    """

    df = order_header_df.copy()
    df['createdate'] = pd.to_datetime(df['createdate'], errors='coerce')

    # Only completed orders
    df = df[df['status'] == "COMPLETED"].dropna(subset=['createdate'])
    df['YearMonth'] = df['createdate'].dt.to_period('M')

    monthly = df.groupby('YearMonth').agg(
        Orders=('order_id', 'nunique'),
        Revenue=('amount_eur', 'sum')
    ).reset_index()

    # Convert period → timestamp for chart compatibility
    monthly['YearMonth'] = monthly['YearMonth'].dt.to_timestamp()

    st.markdown("### 📈 Monthly Revenue & Orders Trend")

    st.line_chart(
        monthly.set_index("YearMonth")[["Revenue", "Orders"]]
    )

    return monthly
