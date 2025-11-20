import pandas as pd
from modules.config import DATA_RAW

def load_orders():
    o50 = pd.read_csv(DATA_RAW / "op-orders-o50k.csv", low_memory=False)
    h50 = pd.read_csv(DATA_RAW / "op-orders-h50k.csv", low_memory=False)
    return o50, h50

def load_abandoned():
    return pd.read_csv(DATA_RAW / "op-abandonedbasket.csv")

def load_app_clicks():
    return pd.read_csv(DATA_RAW / "op-app_clicks.csv")

def load_dm_clicks():
    return pd.read_csv(DATA_RAW / "op-dm_clicks.csv")

# ----------------------------------------------------
# Combined raw loader
# ----------------------------------------------------
def load_raw_data():
    """
    Load all raw CSVs at once.
    Returns:
        orders_o50, orders_h50, abandoned, clicks_app, clicks_dm
    """
    orders_o50, orders_h50 = load_orders()
    abandoned = load_abandoned()
    clicks_app = load_app_clicks()
    clicks_dm = load_dm_clicks()
    return orders_o50, orders_h50, abandoned, clicks_app, clicks_dm
