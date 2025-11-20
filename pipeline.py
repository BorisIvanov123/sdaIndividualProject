"""
pipeline.py
-----------
Main data processing pipeline for sales management analytics.

This script processes raw e-commerce data through the following stages:
1. Load raw data
2. Clean and merge orders
3. Parse basket JSON
4. Extract order headers and line items
5. Build sessions dimension
6. Calculate marketing attribution
7. Build conversion funnel
8. Analyze exit events
9. Identify repeat buyers and cohorts
10. Export all processed data

Usage:
    python pipeline.py
"""

import pandas as pd
import numpy as np
import warnings
import sys
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import all required modules
from modules.load.load_data import load_raw_data
from modules.extract.extract_basket import parse_basket
from modules.extract.extract_order_header import build_order_header
from modules.extract.extract_line_items import extract_all_line_items

from modules.transform.clean_orders import clean_orders
from modules.transform.sessions import build_sessions_dim, compute_conversion_flags
from modules.transform.funnel import build_funnel, calculate_funnel_metrics
from modules.transform.exit_events import extract_exit_events, identify_exit_sessions, summarize_exit_points
from modules.transform.repeat_buyers import (
    identify_customers,
    classify_orders,
    calculate_repeat_metrics,
    build_cohort_analysis
)

from modules.attribution.attribution import (
    prepare_dm_clicks,
    build_last_click_table,
    apply_attribution_window,
    finalize_attribution,
    attribution_summary
)

from modules.output.export import export_tables
from modules.config import FX_RATES
from modules.analytics.country_kpis import compute_country_kpis



def main():
    """Execute the complete data processing pipeline."""

    print("=" * 80)
    print("SALES MANAGEMENT ANALYTICS PIPELINE")
    print("=" * 80)
    print()

    try:
        # ====================================================================
        # STAGE 1: LOAD DATA
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 1: LOADING RAW DATA")
        print("─" * 80)

        orders_o50, orders_h50, abandoned, clicks_app, clicks_dm = load_raw_data()
        print(f"✓ Loaded 5 datasets successfully")

        # ====================================================================
        # STAGE 2: CLEAN & MERGE ORDERS
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 2: CLEANING & MERGING ORDERS")
        print("─" * 80)

        orders_raw = clean_orders(orders_o50, orders_h50)
        print(f"✓ Orders cleaned and merged: {len(orders_raw):,} total orders")

        # ====================================================================
        # STAGE 3: PARSE BASKET
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 3: PARSING BASKET JSON")
        print("─" * 80)

        orders_raw = parse_basket(orders_raw)
        print(f"✓ Basket JSON parsed successfully")

        # ====================================================================
        # STAGE 4: EXTRACT ORDER HEADER
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 4: EXTRACTING ORDER HEADER")
        print("─" * 80)

        order_header_df = build_order_header(orders_raw)
        print(f"✓ Order header extracted: {len(order_header_df):,} orders")
        print(f"  Total revenue: €{order_header_df['amount_eur'].sum():,.2f}")

        # ====================================================================
        # STAGE 5: EXTRACT LINE ITEMS
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 5: EXTRACTING LINE ITEMS")
        print("─" * 80)

        order_line_items_df = extract_all_line_items(orders_raw)
        print(f"✓ Line items extracted: {len(order_line_items_df):,} items")
        print(f"  Unique SKUs: {order_line_items_df['sku'].nunique()}")

        # ====================================================================
        # STAGE 6: BUILD SESSIONS
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 6: BUILDING SESSIONS DIMENSION")
        print("─" * 80)

        sessions_dim = build_sessions_dim(abandoned)
        sessions_dim = compute_conversion_flags(sessions_dim, order_header_df)
        print(f"✓ Sessions dimension built: {len(sessions_dim):,} sessions")

        # ====================================================================
        # STAGE 7: BUILD ATTRIBUTION
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 7: CALCULATING MARKETING ATTRIBUTION")
        print("─" * 80)

        dm_prepared = prepare_dm_clicks(clicks_dm)
        last_clicks = build_last_click_table(dm_prepared)
        attribution = apply_attribution_window(order_header_df, last_clicks)
        attribution_final = finalize_attribution(attribution)

        # Get attribution summary
        attr_summary = attribution_summary(attribution_final, order_header_df)

        # ====================================================================
        # STAGE 8: BUILD FUNNEL
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 8: BUILDING CONVERSION FUNNEL")
        print("─" * 80)

        funnel_df = build_funnel(clicks_app, clicks_dm, order_header_df)
        print(f"✓ Funnel built: {len(funnel_df):,} sessions")

        # Calculate funnel metrics
        metrics = calculate_funnel_metrics(funnel_df)
        print(f"  Conversion rate: {metrics['sessions_to_order_rate']:.2f}%")

        # ====================================================================
        # STAGE 9: COUNTRY-LEVEL KPIs
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE X: COUNTRY-LEVEL KPIs")
        print("─" * 80)

        country_kpis_df = compute_country_kpis(order_header_df, clicks_app, funnel_df)
        print("✓ Country KPIs computed")
        print(country_kpis_df)

        # ====================================================================
        # STAGE 10: EXTRACT EXIT EVENTS
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 9: ANALYZING EXIT EVENTS")
        print("─" * 80)

        exit_events_df = extract_exit_events(clicks_app)
        exit_sessions_df = identify_exit_sessions(exit_events_df, funnel_df)
        exit_summary = summarize_exit_points(exit_sessions_df, top_n=10)

        # ====================================================================
        # STAGE 11: REPEAT BUYER ANALYSIS
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 10: ANALYZING REPEAT BUYERS")
        print("─" * 80)

        order_header_df = identify_customers(order_header_df, customer_col='cust_email')
        order_header_df = classify_orders(order_header_df)
        repeat_metrics = calculate_repeat_metrics(order_header_df)
        cohort_df = build_cohort_analysis(order_header_df, windows=[3, 6])

        # ====================================================================
        # STAGE 12: EXPORT ALL DATA
        # ====================================================================
        print("\n" + "─" * 80)
        print("STAGE 11: EXPORTING PROCESSED DATA")
        print("─" * 80)

        export_tables(
            tables={
                'order_header': order_header_df,
                'line_items': order_line_items_df,
                'sessions': sessions_dim,
                'attribution': attribution_final,
                'funnel': funnel_df,
                'exit_events': exit_events_df,
                'exit_sessions': exit_sessions_df,
                'cohorts': cohort_df,
                'country_kpis': country_kpis_df
            }
        )

        # ====================================================================
        # PIPELINE SUMMARY
        # ====================================================================
        print("\n" + "=" * 80)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print("\n📊 SUMMARY:")
        print(f"  • Orders processed: {len(order_header_df):,}")
        print(f"  • Line items: {len(order_line_items_df):,}")
        print(f"  • Sessions: {len(sessions_dim):,}")
        print(f"  • Unique customers: {order_header_df['customer_id'].nunique():,}")
        print(f"  • Total revenue: €{order_header_df['amount_eur'].sum():,.2f}")
        print(f"  • Conversion rate: {metrics['sessions_to_order_rate']:.2f}%")
        print(f"  • Repeat customer rate: {repeat_metrics['repeat_customer_rate']:.1f}%")
        print("\n All processed files exported to data/processed_data/")
        print()

        return 0

    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ PIPELINE FAILED")
        print("=" * 80)
        print(f"\nError: {str(e)}")
        print("\nPlease check:")
        print("  1. All raw data files are in data/raw_data/")
        print("  2. Required modules are installed (pandas, numpy)")
        print("  3. File permissions are correct")
        print()
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)