# app_sections/overview/components/intro.py

import streamlit as st

def intro_section(text: str = None):
    """
    If `text` is provided → render a small intro box for a section.
    If `text` is None → render the full long project overview.
    """

    # Short version
    if text:
        html = f"""
        <div style="
            max-width:800px;
            margin:auto;
            padding:18px;
            background-color:rgba(255,255,255,0.04);
            border-radius:10px;
            margin-bottom:25px;
        ">
            <p style='text-align:center; color:#CCCCCC; margin:0;'>
                {text}
            </p>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        return

