"""
repeat_buyers.py
----------------
Analyze first-time vs repeat buyers and cohort behavior.

Includes:
- identify_customers()
- classify_orders()
- calculate_repeat_metrics()
- build_cohort_analysis()
"""
import pandas as pd
import numpy as np

def identify_customers(order_df: pd.DataFrame, customer_col: str = 'cust_email') -> pd.DataFrame:
    """
    Define customer proxy and add customer_id.

    Uses cust_email as the primary customer identifier (already anonymized).

    Args:
        order_df: Order header dataframe
        customer_col: Column to use as customer identifier (default: 'cust_email')

    Returns:
        DataFrame with customer_id added
    """
    df = order_df.copy()

    # Check if customer column exists
    if customer_col not in df.columns:
        raise ValueError(f"Column '{customer_col}' not found. Available columns: {df.columns.tolist()}")

    # Use email as customer_id (it's already anonymized)
    df['customer_id'] = df[customer_col]

    # Check data quality
    null_customers = df['customer_id'].isna().sum()
    unique_customers = df['customer_id'].nunique()

    print(f"✓ Customer identification complete")
    print(f"  Customer proxy: {customer_col}")
    print(f"  Total orders: {len(df):,}")
    print(f"  Orders with customer_id: {(~df['customer_id'].isna()).sum():,} ({(~df['customer_id'].isna()).mean()*100:.1f}%)")
    print(f"  Unique customers: {unique_customers:,}")
    print(f"  Avg orders per customer: {len(df)/unique_customers:.2f}")

    if null_customers > 0:
        print(f" Warning: {null_customers:,} orders have no customer_id")

    return df


def classify_orders(order_df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify each order as first-time or repeat purchase.

    Args:
        order_df: Order dataframe with customer_id and createdate

    Returns:
        DataFrame with classification columns added:
        - first_purchase_date
        - order_number (1st, 2nd, 3rd, etc.)
        - is_first_purchase (True/False)
        - is_repeat_purchase (True/False)
    """
    df = order_df.copy()

    # Convert createdate to datetime with UTC, then remove timezone
    df['createdate'] = pd.to_datetime(df['createdate'], utc=True, errors='coerce')
    if df['createdate'].dt.tz is not None:
        df['createdate'] = df['createdate'].dt.tz_localize(None)

    # Drop rows with null createdate or customer_id (can't classify these)
    null_dates = df['createdate'].isna().sum()
    null_customers = df['customer_id'].isna().sum()

    if null_dates > 0:
        print(f"  Warning: {null_dates:,} orders have null createdate - excluding from classification")
    if null_customers > 0:
        print(f"  Warning: {null_customers:,} orders have null customer_id - excluding from classification")

    df_valid = df.dropna(subset=['createdate', 'customer_id'])

    # Sort by customer and date
    df_valid = df_valid.sort_values(['customer_id', 'createdate'])

    # Get first purchase date per customer
    first_purchases = df_valid.groupby('customer_id')['createdate'].min().reset_index()
    first_purchases.columns = ['customer_id', 'first_purchase_date']

    # Merge back to ALL rows (not just valid ones)
    df = df.merge(first_purchases, on='customer_id', how='left')

    # Assign order number per customer (1st, 2nd, 3rd order, etc.)
    df['order_number'] = df.groupby('customer_id').cumcount() + 1

    # For rows with null createdate, set order_number to NaN
    df.loc[df['createdate'].isna(), 'order_number'] = np.nan

    # Classify as first-time or repeat
    df['is_first_purchase'] = (df['order_number'] == 1)
    df['is_repeat_purchase'] = (df['order_number'] > 1)

    # Days since first purchase
    df['days_since_first_purchase'] = (df['createdate'] - df['first_purchase_date']).dt.days

    print(f"\n✓ Orders classified")
    print(f"  Valid orders for classification: {len(df_valid):,}")
    print(f"  First-time orders: {df['is_first_purchase'].sum():,} ({df['is_first_purchase'].mean()*100:.1f}%)")
    print(f"  Repeat orders: {df['is_repeat_purchase'].sum():,} ({df['is_repeat_purchase'].mean()*100:.1f}%)")
    print(f"  Customers with 2+ orders: {(df.groupby('customer_id').size() >= 2).sum():,}")
    print(f"  Max orders by single customer: {df['order_number'].max()}")

    return df


def calculate_repeat_metrics(order_df: pd.DataFrame) -> dict:
    """
    Calculate repeat buyer metrics.

    Args:
        order_df: Classified orders dataframe

    Returns:
        Dictionary with repeat buyer metrics
    """
    total_orders = len(order_df)
    first_time_orders = order_df['is_first_purchase'].sum()
    repeat_orders = order_df['is_repeat_purchase'].sum()

    unique_customers = order_df['customer_id'].nunique()
    repeat_customers = (order_df.groupby('customer_id').size() >= 2).sum()

    # Revenue split (only for orders with amount_eur)
    first_time_revenue = order_df[order_df['is_first_purchase']]['amount_eur'].sum()
    repeat_revenue = order_df[order_df['is_repeat_purchase']]['amount_eur'].sum()
    total_revenue = order_df['amount_eur'].sum()

    # Average order values
    first_time_aov = order_df[order_df['is_first_purchase']]['amount_eur'].mean()
    repeat_aov = order_df[order_df['is_repeat_purchase']]['amount_eur'].mean()

    metrics = {
        'total_orders': total_orders,
        'first_time_orders': first_time_orders,
        'repeat_orders': repeat_orders,
        'first_time_pct': (first_time_orders / total_orders * 100) if total_orders > 0 else 0,
        'repeat_pct': (repeat_orders / total_orders * 100) if total_orders > 0 else 0,

        'unique_customers': unique_customers,
        'repeat_customers': repeat_customers,
        'repeat_customer_rate': (repeat_customers / unique_customers * 100) if unique_customers > 0 else 0,

        'first_time_revenue': first_time_revenue,
        'repeat_revenue': repeat_revenue,
        'total_revenue': total_revenue,
        'first_time_revenue_pct': (first_time_revenue / total_revenue * 100) if total_revenue > 0 else 0,
        'repeat_revenue_pct': (repeat_revenue / total_revenue * 100) if total_revenue > 0 else 0,

        'first_time_aov': first_time_aov,
        'repeat_aov': repeat_aov,
    }

    print(f"\n📊 REPEAT BUYER METRICS:")
    print(f"   Total orders: {metrics['total_orders']:,}")
    print(f"   First-time orders: {metrics['first_time_orders']:,} ({metrics['first_time_pct']:.1f}%)")
    print(f"   Repeat orders: {metrics['repeat_orders']:,} ({metrics['repeat_pct']:.1f}%)")
    print(f"\n   Unique customers: {metrics['unique_customers']:,}")
    print(f"   Repeat customers: {metrics['repeat_customers']:,} ({metrics['repeat_customer_rate']:.1f}%)")
    print(f"\n   First-time revenue: €{metrics['first_time_revenue']:,.2f} ({metrics['first_time_revenue_pct']:.1f}%)")
    print(f"   Repeat revenue: €{metrics['repeat_revenue']:,.2f} ({metrics['repeat_revenue_pct']:.1f}%)")
    print(f"\n   First-time AOV: €{metrics['first_time_aov']:.2f}")
    print(f"   Repeat AOV: €{metrics['repeat_aov']:.2f}")

    return metrics

def build_cohort_analysis(order_df: pd.DataFrame, max_months: int = 12) -> pd.DataFrame:
    """
    Build a full month-by-month retention matrix (Stripe/ChartMogul style).
    Returns:
        cohort_month | size | m1 | m2 | ... | m12
    """

    df = order_df.copy()

    # Ensure datetime
    df["createdate"] = pd.to_datetime(df["createdate"], errors="coerce")
    df["first_purchase_date"] = pd.to_datetime(df["first_purchase_date"], errors="coerce")

    # Cohort month
    df["cohort_month"] = df["first_purchase_date"].dt.to_period("M")

    # VALID rows only
    df = df[df["createdate"].notna() & df["first_purchase_date"].notna()]

    # 🔥 FIXED: Proper month difference
    df["months_since_first"] = (
        (df["createdate"].dt.year - df["first_purchase_date"].dt.year) * 12 +
        (df["createdate"].dt.month - df["first_purchase_date"].dt.month)
    )

    # Keep only non-negative months
    df = df[df["months_since_first"] >= 0]

    # Cohort size = users who made Month 0 purchase
    cohort_sizes = (
        df[df["months_since_first"] == 0]
        .groupby("cohort_month")["customer_id"]
        .nunique()
    )

    cohort_matrix = pd.DataFrame({"size": cohort_sizes})

    # Build m1, m2, m3, … m12 retention
    for m in range(1, max_months + 1):
        retained = (
            df[df["months_since_first"] == m]
            .groupby("cohort_month")["customer_id"]
            .nunique()
        )

        cohort_matrix[f"m{m}"] = (
            (retained / cohort_sizes) * 100
        ).round(1)

    cohort_matrix.index = cohort_matrix.index.astype(str)

    print(f"✓ Full cohort analysis built ({max_months} months)")

    return cohort_matrix.reset_index().rename(columns={"index": "cohort_month"})
