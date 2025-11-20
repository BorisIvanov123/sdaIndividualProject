"""
attribution.py
--------------
Handles 7-day last-click attribution using DM clicks.

Includes:
- prepare_dm_clicks()
- build_last_click_table()
- apply_attribution_window()
- finalize_attribution()
"""
import pandas as pd


def prepare_dm_clicks(clicks_dm: pd.DataFrame) -> pd.DataFrame:
    """
    Rename sid -> sessionid and sort chronologically.

    Args:
        clicks_dm: Raw DM clicks dataframe

    Returns:
        Cleaned DM clicks with sessionid column
    """
    df = clicks_dm.copy()

    # Rename sid to sessionid if it exists
    if 'sid' in df.columns and 'sessionid' not in df.columns:
        df = df.rename(columns={"sid": "sessionid"})

    # Convert sessionid to string for consistency
    df['sessionid'] = df['sessionid'].astype(str)

    # Sort by session and date
    df = df.sort_values(["sessionid", "date"])

    print(f"✓ DM clicks prepared")
    print(f"  Unique sessions with DM clicks: {df['sessionid'].nunique():,}")
    print(f"  Total DM clicks: {len(df):,}")

    return df


def build_last_click_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return last click per session (last-click attribution).

    Args:
        df: Prepared DM clicks dataframe

    Returns:
        One row per session with last click data
    """
    last_clicks = (
        df.groupby("sessionid")
        .agg({
            "date": "last",
            "ad": "last",
            "ad_type": "last",
            "ad_name": "last",
            "ad_country": "last",
            "platform": "last"
        })
        .reset_index()
        .rename(columns={"date": "last_click_date"})
    )

    print(f"✓ Last-click table built")
    print(f"  Sessions with last click: {len(last_clicks):,}")

    return last_clicks


def apply_attribution_window(order_df: pd.DataFrame, last_click_df: pd.DataFrame, days: int = 7) -> pd.DataFrame:
    """
    Join clicks to orders and apply attribution window.

    Args:
        order_df: Order header dataframe with sessionid
        last_click_df: Last click per session
        days: Attribution window in days (default: 7)

    Returns:
        Orders with attribution data
    """
    # Ensure sessionid is string in both dataframes
    order_df = order_df.copy()
    last_click_df = last_click_df.copy()

    order_df['sessionid'] = order_df['sessionid'].astype(str)
    last_click_df['sessionid'] = last_click_df['sessionid'].astype(str)

    # Join orders with last clicks
    df = order_df[["order_id", "sessionid", "createdate"]].merge(
        last_click_df, on="sessionid", how="left"
    )

    # Convert dates to datetime
    df["last_click_date"] = pd.to_datetime(df["last_click_date"], errors="coerce", utc=True).dt.tz_localize(None)
    df["createdate"] = pd.to_datetime(df["createdate"], errors="coerce", utc=True).dt.tz_localize(None)

    # Calculate days between click and order
    df["days_to_conversion"] = (df["createdate"] - df["last_click_date"]).dt.days

    # Assign channel based on attribution window
    df["channel"] = df.apply(
        lambda row: row["ad_type"]
        if (pd.notna(row["ad_type"]) and
            pd.notna(row["days_to_conversion"]) and
            0 <= row["days_to_conversion"] <= days)
        else "Organic/Direct",
        axis=1
    )

    # Print diagnostics
    print(f"✓ Attribution window applied ({days}-day)")
    print(f"  Total orders: {len(df):,}")
    print(f"  Orders with sessionid: {df['sessionid'].notna().sum():,}")
    print(f"  Orders matched to DM clicks: {df['ad_type'].notna().sum():,}")
    print(f"  Orders within {days}-day window: {(df['channel'] != 'Organic/Direct').sum():,}")
    print(f"  Orders attributed to Organic/Direct: {(df['channel'] == 'Organic/Direct').sum():,}")

    return df


def finalize_attribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return session-level attribution table.

    Args:
        df: Attribution dataframe with orders

    Returns:
        One row per session with final attribution
    """
    attribution = df[["sessionid", "channel", "ad", "ad_name", "platform", "ad_country"]] \
        .drop_duplicates(subset=["sessionid"])

    print(f"✓ Attribution finalized")
    print(f"  Unique sessions: {len(attribution):,}")
    print(f"\n  Channel distribution:")
    for channel, count in attribution['channel'].value_counts().head(10).items():
        print(f"    {channel}: {count:,}")

    return attribution


def attribution_summary(attribution_df: pd.DataFrame, order_df: pd.DataFrame) -> dict:
    """
    Generate attribution summary statistics.

    Args:
        attribution_df: Final attribution table
        order_df: Order header dataframe

    Returns:
        Dictionary with summary metrics
    """
    # Merge to get order amounts
    df = attribution_df.merge(
        order_df[['sessionid', 'amount_eur']],
        on='sessionid',
        how='left'
    )

    # Calculate metrics by channel
    channel_metrics = df.groupby('channel').agg({
        'sessionid': 'count',
        'amount_eur': 'sum'
    }).reset_index()
    channel_metrics.columns = ['channel', 'orders', 'revenue_eur']
    channel_metrics['avg_order_value'] = channel_metrics['revenue_eur'] / channel_metrics['orders']

    summary = {
        'total_orders': len(df),
        'attributed_to_paid': (df['channel'] != 'Organic/Direct').sum(),
        'organic_direct': (df['channel'] == 'Organic/Direct').sum(),
        'total_revenue': df['amount_eur'].sum(),
        'channel_breakdown': channel_metrics
    }

    print(f"\n📊 ATTRIBUTION SUMMARY:")
    print(f"   Total orders: {summary['total_orders']:,}")
    print(
        f"   Attributed to paid: {summary['attributed_to_paid']:,} ({summary['attributed_to_paid'] / summary['total_orders'] * 100:.1f}%)")
    print(
        f"   Organic/Direct: {summary['organic_direct']:,} ({summary['organic_direct'] / summary['total_orders'] * 100:.1f}%)")
    print(f"   Total revenue: €{summary['total_revenue']:,.2f}")

    return summary