import streamlit as st
import pandas as pd

def data_table(df: pd.DataFrame, title: str = ""):

    # Optional title
    if title:
        st.markdown(f"<h4 style='margin-bottom:10px;'>{title}</h4>", unsafe_allow_html=True)

    # Custom CSS for styling dataframe
    st.markdown("""
        <style>

        /* --- Table Container Styling --- */
        .stDataFrame > div {
            border-radius: 12px !important;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.08);
        }

        /* --- Header Row --- */
        .stDataFrame table thead tr th {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            padding: 10px 6px !important;
            border-bottom: 1px solid rgba(255,255,255,0.15) !important;
        }

        /* --- Body Cells --- */
        .stDataFrame table tbody tr td {
            padding: 10px 6px !important;
            border-bottom: 1px solid rgba(255,255,255,0.05) !important;
        }

        /* --- Zebra Striping --- */
        .stDataFrame table tbody tr:nth-child(even) td {
            background-color: rgba(255,255,255,0.03) !important;
        }

        /* --- Hover Effect --- */
        .stDataFrame table tbody tr:hover td {
            background-color: rgba(255,255,255,0.12) !important;
        }

        </style>
    """, unsafe_allow_html=True)

    # Render table
    st.dataframe(df, use_container_width=True)
