"""
parquet_sanitize.py
-------------------
Utility functions to clean DataFrames before exporting to Parquet.

Parquet (PyArrow) requires strict column typing. Mixed object columns
(strings + ints + None) will cause ArrowTypeError.

This module ensures:
- All problematic object columns are converted to strings
- Export becomes stable and fast
"""

import pandas as pd


def fix_parquet_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all object columns to strings to avoid Parquet type conflicts.
    """
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str)
    return df


def sanitize_all_for_parquet(dfs: dict) -> dict:
    """
    Takes a dict of {name: df} and returns the same dict
    with all dfs sanitized for Parquet export.
    """
    cleaned = {}
    for name, df in dfs.items():
        cleaned[name] = fix_parquet_types(df)
    return cleaned
