from pathlib import Path
import pandas as pd
import os

DATA_ROOT = Path("data")

def load_all_data():
    print("=== STREAMLIT DEBUG START ===")
    print("PWD:", os.getcwd())
    print("ROOT FILES:", os.listdir("."))
    if os.path.exists("data"):
        print("data/:", os.listdir("data"))
    if os.path.exists("data/processed_data"):
        print("processed_data/:", os.listdir("data/processed_data"))
    print("=== STREAMLIT DEBUG END ===")
    base_processed = DATA_ROOT / "processed_data"
    base_raw = DATA_ROOT / "raw_data"

    order_header_df = pd.read_csv(base_processed / "order_header.csv")
    funnel_df = pd.read_csv(base_processed / "funnel.csv")
    line_items = pd.read_csv(base_processed / "line_items.csv")
    sessions = pd.read_csv(base_processed / "sessions.csv")
    cohorts = pd.read_csv(base_processed / "cohorts.csv")
    country_kpis = pd.read_csv(base_processed / "country_kpis.csv")   # ← NEW

    return (
        order_header_df,
        funnel_df,
        line_items,
        sessions,
        cohorts,
        country_kpis,
    )
