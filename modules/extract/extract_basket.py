"""
extract_basket.py

Handles parsing the JSON `basket` column into a clean Python dictionary.
Adds: basket_parsed
"""

import json
import pandas as pd


def parse_basket(df: pd.DataFrame) -> pd.DataFrame:
    """Add a column 'basket_parsed' with JSON decoded dictionaries."""

    def _safe_parse(x):
        if pd.isna(x) or x == "":
            return {}
        try:
            return json.loads(x)
        except json.JSONDecodeError:
            return {}

    df = df.copy()
    df["basket_parsed"] = df["basket"].apply(_safe_parse)
    return df
