"""
extract_line_items.py

Extracts product-level line items from the basket JSON.
Excludes shipping items.
"""

import pandas as pd
from typing import Dict, Any, List
from modules.config import FX_RATES


SHIPPING_KEYWORDS = [
    "shipping", "envío", "livraison", "versand",
    "spedizione", "porto", "frakt", "levering"
]


# ------------------------------------------------------
# Extract items from a single order
# ------------------------------------------------------
def extract_line_items(row: pd.Series) -> List[Dict[str, Any]]:
    """Extract non-shipping items from a single order."""

    basket = row["basket_parsed"]
    items = basket.get("orderItemList", [])
    currency = basket.get("currency", "EUR")
    order_id = row["id"]

    results = []

    for item in items:
        sku = item.get("sku")
        desc = (item.get("description") or "").lower()

        # Skip shipping
        if sku == 100001 or any(kw in desc for kw in SHIPPING_KEYWORDS):
            continue

        results.append({
            "order_id": order_id,
            "sku": sku,
            "description": item.get("description"),
            "qty": item.get("quantity", 1),
            "unit_price": item.get("unitPrice"),
            "tax_percentage": item.get("taxPercentage"),
            "currency": currency,

            # product metadata
            "color": item.get("color"),
            "size": item.get("size"),
            "font": item.get("font"),
            "img_label": item.get("imgLabel"),
            "inverted": item.get("inverted", False),
            "align": item.get("align"),
        })

    return results


# ------------------------------------------------------
# Build full line item table
# ------------------------------------------------------
def extract_all_line_items(df: pd.DataFrame) -> pd.DataFrame:
    """Extract items for all orders."""

    collected = []

    for _, row in df.iterrows():
        collected.extend(extract_line_items(row))

    items_df = pd.DataFrame(collected)

    if items_df.empty:
        return items_df

    # Clean fields
    items_df["qty"] = pd.to_numeric(items_df["qty"], errors="coerce").fillna(1).astype(int)
    items_df["unit_price"] = pd.to_numeric(items_df["unit_price"], errors="coerce")
    items_df["subtotal"] = items_df["unit_price"] * items_df["qty"]

    # FX
    items_df["unit_price_eur"] = items_df.apply(
        lambda r: r["unit_price"] * FX_RATES.get(r["currency"], 1.0)
        if pd.notna(r["unit_price"]) else None,
        axis=1,
    )

    items_df["subtotal_eur"] = items_df.apply(
        lambda r: r["subtotal"] * FX_RATES.get(r["currency"], 1.0)
        if pd.notna(r["subtotal"]) else None,
        axis=1,
    )

    return items_df
