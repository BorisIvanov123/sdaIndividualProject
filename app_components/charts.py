# app_components/charts.py

import streamlit as st
import pandas as pd

def bar_chart(df: pd.DataFrame, title: str = ""):
    if title:
        st.markdown(f"### {title}")
    st.bar_chart(df)

def line_chart(df: pd.DataFrame, title: str = ""):
    if title:
        st.markdown(f"### {title}")
    st.line_chart(df)
