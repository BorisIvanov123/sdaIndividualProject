import streamlit as st

def intro_section():
    html = """
<div style="max-width:900px; margin:auto; padding:25px;
            background-color:rgba(255,255,255,0.04);
            border-radius:12px; margin-bottom:25px;">

<h1 style="text-align:center; color:#FFFFFF; margin-bottom:5px;">
    📘 Project Overview
</h1>

<p style="text-align:center; color:#CCCCCC; max-width:850px; margin:auto;">
    This dashboard summarizes the end-to-end sales analytics pipeline built for the
    <b>OriginalPeople 2025/2026 Sales Analytics Individual Project</b>.
    It transforms raw e-commerce and marketing data into a clean analytical model
    including normalized orders, attribution, funnel metrics, and buyer cohorts.
</p>

<br/>

<h3 style="color:#AAAAAA;">Data Sources</h3>
<ul style="color:#DDDDDD;">
    <li><b>orders</b> — raw orders with JSON basket</li>
    <li><b>app_clicks</b> — website/app events (sessions)</li>
    <li><b>dm_clicks</b> — paid traffic for attribution</li>
    <li><b>abandonedbasket</b> — checkout intent signals</li>
</ul>

<h3 style="color:#AAAAAA;">Key Processing Steps</h3>
<ul style="color:#DDDDDD;">
    <li>Flatten JSON basket → order header + line items</li>
    <li>Normalize all amounts to EUR via FX table</li>
    <li>Join orders ↔ sessions ↔ marketing clicks</li>
    <li>Apply last-touch attribution rules</li>
    <li>Compute funnel stages & conversion rates</li>
    <li>Generate buyer classification and cohorts</li>
</ul>

<h3 style="color:#AAAAAA;">Dashboard Sections</h3>
<ul style="color:#DDDDDD;">
    <li>Sales by Area (Revenue, Orders, CVR)</li>
    <li>Product Mix / SKU Performance</li>
    <li>Seasonality & Monthly Trends</li>
    <li>Conversion Funnel & Exit Pages</li>
    <li>Repeat Buyers & Cohort Retention</li>
    <li>Forecasting (Simple TS Model)</li>
</ul>

<h3 style="color:#AAAAAA;">🔧 Data Processing Pipeline (Summary)</h3>
<ul style="color:#DDDDDD;">
    <li>Load raw O50, H50, clicks, abandoned basket</li>
    <li>Clean and merge orders</li>
    <li>Parse basket JSON → itemized rows</li>
    <li>Extract order header (final EUR amounts)</li>
    <li>Extract line items (SKU, qty, price)</li>
    <li>Build sessions dimension + conversion flags</li>
    <li>Prepare dm_clicks for attribution</li>
    <li>Last-click attribution calculation</li>
    <li>Build funnel from app_clicks + dm_clicks + orders</li>
    <li>Analyze exit events and top exit pages</li>
    <li>Identify customers + repeat buyer logic</li>
    <li>Build cohort retention table (3–6 month windows)</li>
</ul>

</div>
"""
    st.markdown(html, unsafe_allow_html=True)
