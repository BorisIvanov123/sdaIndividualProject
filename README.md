# Sales Management Analytics – Project README

A full end-to-end analytics project that processes raw e-commerce data into clean analytical tables and visualizes insights in a Streamlit dashboard. The project covers data ingestion, JSON parsing, order & item extraction, attribution modeling, funnel analytics, country-level KPIs, exit behavior, and repeat-buyer analysis.

**Live dashboard:** https://sdaindividualproject.onrender.com/  
**Repository:** https://github.com/BorisIvanov123/sdaIndividualProject

---

## 🚀 1. Project Features

### Complete ETL Pipeline
- Load raw CSV datasets
- Clean & merge order sources
- Parse nested basket JSON
- Extract order headers + product-level line items
- Build sessions and funnel metrics
- Apply 7-day last-click marketing attribution
- Generate country KPIs, exit events, repeat buyer cohorts
- Export fully processed parquet files

### Interactive Streamlit Dashboard
- Overview KPIs
- Conversion funnel
- Attribution breakdown
- Country performance
- Repeat buyer analytics
- Seasonality & forecasting (if applicable)

---

## 📦 2. Installation

Clone the repository:
```bash
git clone https://github.com/BorisIvanov123/sdaIndividualProject
cd sdaIndividualProject
```

Install dependencies:
```bash
pip install -r requirements.txt
```

💡 **Python 3.10+ is recommended.**

---

## ⚙️ 3. Run the Data Processing Pipeline

Before launching the dashboard, generate the processed datasets:
```bash
python pipeline.py
```

This will create all analytical tables and save them to:
```
data/processed_data/
```

These parquet tables are used directly by the Streamlit dashboard.

---

## 📊 4. Run the Streamlit Dashboard

After processing the data:
```bash
streamlit run app.py
```

This loads the dashboard locally at:
```
http://localhost:8501
```

To see the online version:  
🔗 **Deployed Dashboard:** https://sdaindividualproject.onrender.com/

---

## 📁 5. Repository Structure
```
sdaIndividualProject/
├── app_components/              # UI building blocks for the dashboard
│   ├── styles/                  # CSS & style helpers
│   ├── cards.py
│   ├── charts.py
│   ├── intro.py
│   ├── layout.py
│   └── tables.py
│
├── app_sections/                # Dashboard page sections
│   ├── country_kpis/
│   ├── forecast/
│   ├── funnel/
│   ├── overview/
│   ├── repeat_buyers/
│   ├── seasonality/
│   └── __init__.py
│
├── data/
│   ├── raw_data/                # Input data (not on GitHub)
│   └── processed_data/          # Output parquet tables
│
├── modules/                     # Full ETL pipeline logic
│   ├── analytics/
│   ├── attribution/
│   ├── extract/
│   ├── load/
│   ├── output/
│   └── transform/
│
├── notebooks/                   # Exploratory work
├── utils/                       # Helper utilities
│
├── app.py                       # Main Streamlit dashboard
├── pipeline.py                  # Full ETL pipeline
├── requirements.txt             
└── README.md
```

---

## 🧠 6. How the Project Works (Summary)

1. **You run `pipeline.py`**, which:
   - Loads raw CSVs
   - Parses basket JSON
   - Extracts item-level details
   - Creates order headers
   - Builds sessions, funnel, attribution & KPIs
   - Saves cleaned parquet files

2. **You run the Streamlit dashboard**, which automatically loads the processed parquet tables and presents interactive visualizations.

3. **You explore insights** such as:
   - Revenue, orders, conversion rate
   - Paid vs organic attribution
   - Exit events & funnel analysis
   - Repeat buyer cohorts
   - Country performance

---

## 🖥️ 7. Deployment

The dashboard is deployed on Render:  
➡️ https://sdaindividualproject.onrender.com/

The deployment loads the processed parquet files stored in the repo.
