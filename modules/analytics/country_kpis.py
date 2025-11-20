import pandas as pd

def compute_country_kpis(order_header_df, app_clicks, funnel_df):
    """
    Compute revenue, orders, and conversion rate (CVR) by country.

    Parameters
    ----------
    order_header_df : DataFrame
        Processed order headers including amount_eur, status, createdate, country
    app_clicks : DataFrame
        Clickstream events including sid, country, date
    funnel_df : DataFrame
        Funnel results including sessionid and converted flag

    Returns
    -------
    DataFrame
        country_kpis (country, revenue_eur, orders, cvr)
    """

    # Ensure date fields parse correctly
    order_header_df['createdate'] = pd.to_datetime(order_header_df['createdate'], errors='ignore')
    app_clicks['date'] = pd.to_datetime(app_clicks['date'], errors='ignore')

    # ----------------------------------------------------
    # 1. Revenue & Orders by Country
    # ----------------------------------------------------
    orders_completed = order_header_df[order_header_df['status'] == 'COMPLETED']

    country_sales = (
        orders_completed
        .groupby('country', as_index=False)
        .agg(
            revenue_eur=('amount_eur', 'sum'),
            orders=('order_id', 'nunique')
        )
    )

    # ----------------------------------------------------
    # 2. Conversion Rate by Country
    # ----------------------------------------------------
    session_country = (
        app_clicks[['sid', 'country']]
        .drop_duplicates(subset=['sid'])
        .rename(columns={'sid': 'sessionid'})
    )

    funnel_with_country = funnel_df.merge(session_country, on='sessionid', how='left')

    cvr_country = (
        funnel_with_country
        .groupby('country', as_index=False)
        .agg(
            sessions=('sessionid', 'nunique'),
            converted_sessions=('converted', 'sum')
        )
    )

    cvr_country['cvr'] = (cvr_country['converted_sessions'] /
                          cvr_country['sessions']).fillna(0)

    # ----------------------------------------------------
    # 3. Merge all KPIs
    # ----------------------------------------------------
    country_kpis = (
        country_sales
        .merge(cvr_country[['country', 'cvr']], on='country', how='outer')
        .fillna(0)
        .sort_values(by='revenue_eur', ascending=False)
    )

    return country_kpis
