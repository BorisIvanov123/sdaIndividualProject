"""
exit_events.py
--------------
Extract the last event per session to identify exit points.
"""
import pandas as pd


def extract_exit_events(app_clicks: pd.DataFrame) -> pd.DataFrame:
    """
    Extract the last event for each session.

    This is used to identify where users exit the site/app.

    Args:
        app_clicks: App clicks dataframe with sessionid/sid and date columns

    Returns:
        DataFrame with one row per session (the last event)
    """
    # Make a copy
    clicks = app_clicks.copy()

    # Ensure sessionid column exists
    if 'sid' in clicks.columns and 'sessionid' not in clicks.columns:
        clicks = clicks.rename(columns={'sid': 'sessionid'})

    # Convert sessionid to string
    clicks['sessionid'] = clicks['sessionid'].astype(str)

    # Convert date to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(clicks['date']):
        clicks['date'] = pd.to_datetime(clicks['date'], utc=True, errors='coerce')

    # Sort by sessionid and date to get chronological order
    clicks_sorted = clicks.sort_values(['sessionid', 'date'])

    # Get the last event (tail) for each session
    last_events = clicks_sorted.groupby('sessionid', as_index=False).last()

    print(f"✓ Extracted {len(last_events):,} exit events (last event per session)")
    print(f"  From {clicks['sessionid'].nunique():,} unique sessions")

    return last_events


def identify_exit_sessions(exit_events: pd.DataFrame, funnel: pd.DataFrame) -> pd.DataFrame:
    """
    Filter exit events to only sessions that didn't convert.

    Args:
        exit_events: Last event per session (from extract_exit_events)
        funnel: Funnel dataframe with 'converted' flag

    Returns:
        Exit events for sessions that didn't convert
    """
    # Ensure sessionid is string in both dataframes
    exit_events = exit_events.copy()
    funnel_copy = funnel.copy()

    exit_events['sessionid'] = exit_events['sessionid'].astype(str)
    funnel_copy['sessionid'] = funnel_copy['sessionid'].astype(str)

    # Get sessions that didn't convert
    non_converted_sessions = funnel_copy[funnel_copy['converted'] == 0]['sessionid']

    # Filter exit events to only non-converted sessions
    exit_only = exit_events[exit_events['sessionid'].isin(non_converted_sessions)]

    print(f"✓ Identified {len(exit_only):,} exit sessions (sessions that didn't convert)")
    print(f"  Out of {len(non_converted_sessions):,} total non-converted sessions")

    return exit_only


def summarize_exit_points(exit_sessions: pd.DataFrame, top_n: int = 10) -> dict:
    """
    Summarize where users are exiting.

    Args:
        exit_sessions: Exit events for non-converted sessions
        top_n: Number of top items to return

    Returns:
        Dictionary with top exit app_sections, types, and URLs
    """
    summary = {
        'top_exit_pages': exit_sessions['page'].value_counts().head(top_n),
        'top_exit_types': exit_sessions['type'].value_counts().head(top_n),
        'top_exit_urls': exit_sessions['url'].value_counts().head(top_n),
        'top_exit_data_ids': exit_sessions['data_id'].value_counts().head(top_n),
        'total_exits': len(exit_sessions)
    }

    print(f"\n📊 EXIT POINTS SUMMARY:")
    print(f"   Total exit sessions: {summary['total_exits']:,}")
    print(f"\n   Top exit app_sections:")
    for i, (page, count) in enumerate(summary['top_exit_pages'].head(5).items(), 1):
        print(f"      {i}. {page}: {count:,}")

    print(f"\n   Top exit event types:")
    for i, (type_, count) in enumerate(summary['top_exit_types'].head(5).items(), 1):
        print(f"      {i}. {type_}: {count:,}")

    return summary