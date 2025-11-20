"""
extract_order_header.py

Extracts order-level fields from the parsed basket JSON.
Builds the order_header dataframe.
"""

import pandas as pd
from typing import Dict, Any
from modules.config import FX_RATES


# ------------------------------------------------------
# Extract fields from a single row
# ------------------------------------------------------
def extract_order_header(row: pd.Series) -> Dict[str, Any]:
    """Extract high-level order fields from JSON basket + original table fields."""

    basket = row["basket_parsed"]
    shipment = basket.get("shipment", {})
    receiver_list = basket.get("receiverList", [])
    receiver = receiver_list[0] if receiver_list else {}

    return {
        "order_id": row["id"],
        "purchaseid": row["purchaseid"],
        "createdate": row["createdate"],
        "status": row["status"],

        # Correct session field
        "sessionid": basket.get("sessionId"),
        "tracking_id": basket.get("trackingId"),

        # Meta
        "currency": basket.get("currency", "EUR"),
        "language": basket.get("language"),
        "locale": basket.get("locale"),
        "country": basket.get("country"),
        "referrer": basket.get("referrer"),

        # Shipment
        "ship_name": shipment.get("name"),
        "ship_surname": shipment.get("surname"),
        "ship_address": shipment.get("address"),
        "ship_address2": shipment.get("address2"),
        "ship_country": shipment.get("country"),
        "ship_province": shipment.get("province"),
        "ship_postalcode": shipment.get("postalcode"),
        "ship_city": shipment.get("postaddress"),

        # Receiver
        "rcv_email": receiver.get("email"),
        "order_amount": receiver.get("amount"),

        # Sender
        "sender_email": basket.get("senderEmail"),
        "sender_firstname": basket.get("senderFirstName"),
        "sender_lastname": basket.get("senderLastName"),
        "invoice_fee": basket.get("invoiceFee"),

        # From raw orders table
        "processed": row.get("processed"),
        "shipped": row.get("shipped"),
        "delivered": row.get("delivered"),
        "cust_email": row.get("cust_email"),
        "is_shipped": row.get("is_shipped"),
    }


# ------------------------------------------------------
# Build full header table
# ------------------------------------------------------
def build_order_header(df: pd.DataFrame) -> pd.DataFrame:
    """Loop over rows and construct order_header dataframe."""

    records = df.apply(extract_order_header, axis=1)
    header_df = pd.DataFrame(records.tolist())

    # Clean numeric fields
    header_df["order_amount"] = pd.to_numeric(header_df["order_amount"], errors="coerce")

    # FX conversion
    header_df["fx_rate"] = header_df["currency"].map(FX_RATES).fillna(1.0)
    header_df["amount_eur"] = header_df["order_amount"] * header_df["fx_rate"]

    return header_df
