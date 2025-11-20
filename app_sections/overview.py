import streamlit as st

def render(order_header_df, sessions):

    # ---------------------------------------------
    # PAGE TITLE (Centered)
    # ---------------------------------------------
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: 10px;'>📊 Overview Dashboard</h1>
        <p style='text-align: center; color: #BBBBBB; margin-top: -10px;'>
            Key metrics & quick insights for your e-commerce performance
        </p>
    """, unsafe_allow_html=True)

    # ---------------------------------------------
    # METRICS — Beautiful centered metric cards
    # ---------------------------------------------
    total_rev = order_header_df[order_header_df["status"] == "COMPLETED"]["amount_eur"].sum()
    total_orders = order_header_df["order_id"].nunique()
    total_sessions = sessions["sessionid"].nunique()

    # Center align the metric row
    col_spacer_left, col1, col2, col3, col_spacer_right = st.columns([1, 2, 2, 2, 1])

    with col1:
        st.markdown("""
            <div style='text-align: center; padding: 20px; border-radius: 12px; background-color: rgba(255,255,255,0.05);'>
                <h3 style='color: #AAAAAA;'>Revenue (EUR)</h3>
                <h1 style='color: #4CAF50; margin-top: -10px;'>{:,}</h1>
            </div>
        """.format(int(total_rev)), unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 20px; border-radius: 12px; background-color: rgba(255,255,255,0.05);'>
                <h3 style='color: #AAAAAA;'>Orders</h3>
                <h1 style='color: #29B6F6; margin-top: -10px;'>{:,}</h1>
            </div>
        """.format(total_orders), unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style='text-align: center; padding: 20px; border-radius: 12px; background-color: rgba(255,255,255,0.05);'>
                <h3 style='color: #AAAAAA;'>Sessions</h3>
                <h1 style='color: #FFB300; margin-top: -10px;'>{:,}</h1>
            </div>
        """.format(total_sessions), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------
    # DATA PREVIEW — Side-by-Side Tables
    # ---------------------------------------------
    st.markdown("### 🔍 Quick Data Preview")
    st.markdown("<p style='color:#BBBBBB;'>A snapshot of your latest order & session data.</p>",
                unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("<h4 style='text-align:center;'>Order Header</h4>", unsafe_allow_html=True)
        st.dataframe(order_header_df.head(10), use_container_width=True)

    with right:
        st.markdown("<h4 style='text-align:center;'>Sessions</h4>", unsafe_allow_html=True)
        st.dataframe(sessions.head(10), use_container_width=True)
