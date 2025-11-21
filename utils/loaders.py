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

    # ----- Load Parquet files -----
    order_header_df = pd.read_parquet(base_processed / "order_header.parquet")
    funnel_df = pd.read_parquet(base_processed / "funnel.parquet")
    line_items = pd.read_parquet(base_processed / "line_items.parquet")
    sessions = pd.read_parquet(base_processed / "sessions.parquet")
    cohorts = pd.read_parquet(base_processed / "cohorts.parquet")
    country_kpis = pd.read_parquet(base_processed / "country_kpis.parquet")
    forecast_df = pd.read_parquet(base_processed / "xgb_forecast_ci.parquet")
    weekly_history = pd.read_parquet(base_processed / "weekly_history.parquet")

    return (
        order_header_df,
        funnel_df,
        line_items,
        sessions,
        cohorts,
        country_kpis,
        forecast_df,
        weekly_history,
    )

