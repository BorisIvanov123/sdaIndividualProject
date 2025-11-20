import streamlit as st

def centered_title(text: str):
    html = f"""
<h1 style="text-align:center; color:#FFFFFF; margin-bottom:20px;">
    {text}
</h1>
"""
    st.markdown(html, unsafe_allow_html=True)
