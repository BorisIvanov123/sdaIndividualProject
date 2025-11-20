import pandas as pd


def build_funnel(app_clicks: pd.DataFrame, clicks_dm: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    """
    Build a conversion funnel: clicks → checkout intent → order

    According to task 2D:
    - Start with ALL sessions from app_clicks
    - Sessions missing in dm_clicks are labeled as "organic"
    - Track: sessions → checkout intent → orders
    """

    # Make copies
    app_clicks_clean = app_clicks.copy()
    clicks_dm_clean = clicks_dm.copy()
    order_header_clean = orders.copy()

    # Rename 'sid' to 'sessionid' in both datasets
    if 'sid' in app_clicks_clean.columns:
        app_clicks_clean = app_clicks_clean.rename(columns={'sid': 'sessionid'})

    if 'sid' in clicks_dm_clean.columns:
        clicks_dm_clean = clicks_dm_clean.rename(columns={'sid': 'sessionid'})

    # Ensure sessionids are strings
    app_clicks_clean['sessionid'] = app_clicks_clean['sessionid'].astype(str)
    clicks_dm_clean['sessionid'] = clicks_dm_clean['sessionid'].astype(str)
    order_header_clean['sessionid'] = order_header_clean['sessionid'].astype(str)

    # Stage 1: Count clicks per session (from app_clicks)
    clicks_per_session = app_clicks_clean.groupby('sessionid').size().reset_index(name='clicks')

    # Stage 2: Identify checkout intent
    # Use dm_clicks to identify sessions that clicked paid ads
    dm_sessions = set(clicks_dm_clean['sessionid'].unique())

    # Label sessions as 'paid' or 'organic'
    clicks_per_session['channel'] = clicks_per_session['sessionid'].apply(
        lambda x: 'paid' if x in dm_sessions else 'organic'
    )

    # Count DM clicks per session (for paid sessions)
    dm_per_session = clicks_dm_clean.groupby('sessionid').size().reset_index(name='dm_clicks')
    clicks_per_session = clicks_per_session.merge(dm_per_session, on='sessionid', how='left')
    clicks_per_session['dm_clicks'] = clicks_per_session['dm_clicks'].fillna(0).astype(int)

    # Stage 3: Count orders per session
    orders_per_session = order_header_clean.groupby('sessionid').size().reset_index(name='orders')

    # Merge orders into funnel
    funnel = clicks_per_session.merge(orders_per_session, on='sessionid', how='left')
    funnel['orders'] = funnel['orders'].fillna(0).astype(int)

    # Add conversion flags
    funnel['had_checkout_intent'] = (funnel['dm_clicks'] > 0).astype(int)
    funnel['converted'] = (funnel['orders'] > 0).astype(int)

    return funnel


def calculate_funnel_metrics(funnel: pd.DataFrame) -> dict:
    """
    Calculate funnel metrics: sessions, checkout intent, orders, conversion rates
    """
    total_sessions = len(funnel)
    checkout_intent = funnel['had_checkout_intent'].sum()
    orders = funnel['converted'].sum()

    # Conversion rates
    checkout_rate = (checkout_intent / total_sessions * 100) if total_sessions > 0 else 0
    conversion_rate = (orders / total_sessions * 100) if total_sessions > 0 else 0
    purchase_rate = (orders / checkout_intent * 100) if checkout_intent > 0 else 0

    metrics = {
        'total_sessions': total_sessions,
        'checkout_intent': checkout_intent,
        'orders': orders,
        'sessions_to_checkout_rate': checkout_rate,
        'sessions_to_order_rate': conversion_rate,
        'checkout_to_order_rate': purchase_rate,
        'organic_sessions': (funnel['channel'] == 'organic').sum(),
        'paid_sessions': (funnel['channel'] == 'paid').sum(),
    }

    return metrics


def funnel_by_dimension(funnel: pd.DataFrame, app_clicks: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """
    Break down funnel by a dimension (e.g., country, language)

    Args:
        funnel: The funnel dataframe
        app_clicks: Original app_clicks to get dimension values
        dimension: Column name to group by (e.g., 'country', 'language')
    """
    # Rename sid to sessionid if needed
    app_clicks_clean = app_clicks.copy()
    if 'sid' in app_clicks_clean.columns:
        app_clicks_clean = app_clicks_clean.rename(columns={'sid': 'sessionid'})
    app_clicks_clean['sessionid'] = app_clicks_clean['sessionid'].astype(str)

    # Get dimension value for each session (take first occurrence)
    session_dimension = app_clicks_clean.groupby('sessionid')[dimension].first().reset_index()

    # Merge with funnel
    funnel_with_dim = funnel.merge(session_dimension, on='sessionid', how='left')

    # Calculate metrics by dimension
    breakdown = funnel_with_dim.groupby(dimension).agg({
        'sessionid': 'count',
        'had_checkout_intent': 'sum',
        'converted': 'sum'
    }).reset_index()

    breakdown.columns = [dimension, 'sessions', 'checkout_intent', 'orders']

    # Calculate conversion rates
    breakdown['checkout_rate_%'] = (breakdown['checkout_intent'] / breakdown['sessions'] * 100).round(2)
    breakdown['conversion_rate_%'] = (breakdown['orders'] / breakdown['sessions'] * 100).round(2)
    breakdown['purchase_rate_%'] = (
            breakdown['orders'] / breakdown['checkout_intent'] * 100
    ).fillna(0).round(2)

    # Sort by sessions descending
    breakdown = breakdown.sort_values('sessions', ascending=False)

    return breakdown