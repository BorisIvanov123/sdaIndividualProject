"""
currency.py
-----------
Handles FX normalization and revenue conversion.

Includes:
- FX_RATES (dict)
- validate_currencies(df)
- add_fx_rates(df)
- convert_amounts_to_eur(df)
"""
import pandas as pd
from typing import Dict

# --------------------------------------------
# Exchange Rates (ECB averages 2021–2025)
# --------------------------------------------
FX_RATES: Dict[str, float] = {
    "EUR": 1.00,
    "GBP": 1.17,
    "USD": 0.92,
    "SEK": 0.095,
}


# --------------------------------------------
# Validate that all currencies have FX rates
# --------------------------------------------
def validate_currencies(df: pd.DataFrame, currency_col: str = "currency") -> None:
    """Check that all currencies in the dataset exist in FX_RATES."""
    unique = set(df[currency_col].dropna().unique())
    missing = unique - set(FX_RATES.keys())

    if missing:
        raise ValueError(f"Missing FX rates for currencies: {missing}")


# --------------------------------------------
# Add fx_rate and amount_eur columns
# --------------------------------------------
def add_fx_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Add fx_rate column based on currency column."""
    df = df.copy()
    df["fx_rate"] = df["currency"].map(FX_RATES).fillna(1.0)
    return df


def convert_amounts_to_eur(df: pd.DataFrame, amount_col: str = "order_amount") -> pd.DataFrame:
    """
    Add amount_eur column using fx_rate * amount.
    Assumes fx_rate already exists.
    """
    df = df.copy()
    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
    df["amount_eur"] = df[amount_col] * df["fx_rate"]
    return df
