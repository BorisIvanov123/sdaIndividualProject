"""
sessions.py
-----------
Builds the sessions dimension from abandoned basket data.

Includes:
- build_sessions_dim()
- compute_conversion_flags()
"""
import pandas as pd


def build_sessions_dim(abandoned: pd.DataFrame) -> pd.DataFrame:
    """
    Build the session-level dimension table:
    - session metadata
    - language/country
    - processed (reached checkout)
    """
    sessions = (
        abandoned.groupby("sessionid")
        .agg({
            "email": "first",
            "createdate": "first",
            "language": "first",
            "country": "first",
            "processed": "max",
            "total": "first"
        })
        .reset_index()
    )
    return sessions


def compute_conversion_flags(sessions_df: pd.DataFrame, orders_df: pd.DataFrame) -> pd.DataFrame:
    """Add converted=True/False based on sessionid overlap."""
    sessions_df = sessions_df.copy()
    session_set = set(orders_df["sessionid"].dropna().unique())
    sessions_df["converted"] = sessions_df["sessionid"].isin(session_set)
    return sessions_df
