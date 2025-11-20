import streamlit as st
import pandas as pd

def render(sessions):
    st.header("🪜 Funnel & Exit Behavior")

    sessions["createdate"] = pd.to_datetime(sessions["createdate"], errors='coerce')
    sessions = sessions.dropna(subset=['createdate'])

    funnel_counts = {
        "Sessions": sessions["sessionid"].nunique(),
        "Checkout Intent": sessions[sessions["processed"] == True]["sessionid"].nunique(),
        "Orders": sessions[sessions["converted"] == True]["sessionid"].nunique(),
    }

    st.write(funnel_counts)

    steps = list(funnel_counts.keys())
    values = list(funnel_counts.values())
    df_plot = pd.DataFrame({"step": steps, "value": values}).set_index("step")

    st.line_chart(df_plot)
