# Sales Management Analytics Project

## Overview

This project provides a comprehensive analytics pipeline for e-commerce sales data, focusing on order processing, customer behavior analysis, marketing attribution, and conversion funnel optimization.

## Project Structure

```
sales-management-project-op-analytics/
├── data/
│   ├── raw_data/              # Raw CSV files (not in git)
│   └── processed_data/        # Cleaned and processed data (not in git)
├── modules/
│   ├── load/
│   │   └── load_data.py       # Load raw data
│   ├── extract/
│   │   ├── extract_basket.py        # Parse JSON basket data
│   │   ├── extract_order_header.py  # Extract order-level fields
│   │   └── extract_line_items.py    # Extract product-level items
│   ├── transform/
│   │   ├── clean_orders.py          # Merge and clean orders
│   │   ├── currency.py              # Currency conversion
│   │   ├── sessions.py              # Session dimension
│   │   ├── funnel.py                # Conversion funnel
│   │   ├── exit_events.py           # Exit point analysis
│   │   └── repeat_buyers.py         # Customer repeat analysis
│   ├── attribution/
│   │   └── attribution.py     # Marketing attribution (7-day last-click)
│   ├── output/
│   │   └── export.py          # Export processed data
│   └── config.py              # Configuration (paths, FX rates)
├── notebooks/
│   └── main_pipeline.py       # Main processing pipeline
├── .gitignore
└── README.md
```

## Features

### 1. Data Loading & Cleaning
- **Merge Orders**: Combines two order datasets (o50k + h50k) spanning 2016-2025
- **Deduplication**: Removes duplicate orders based on order ID
- **Date Sorting**: Chronological ordering by creation date
- **Data Quality Reports**: Null value analysis and coverage verification

### 2. Order Processing
- **Basket Parsing**: Extracts structured data from JSON basket fields
- **Order Header**: Order-level information (customer, dates, amounts, shipping)
- **Line Items**: Product-level details (SKU, quantity, price, attributes)
- **Currency Conversion**: Normalizes all amounts to EUR using fixed exchange rates

### 3. Session Analysis
- **Session Dimension**: Built from abandoned basket data
- **Conversion Flags**: Identifies which sessions resulted in orders
- **Geographic Data**: Country and language tracking
- **Session Metrics**: Total sessions, conversion rates, average session value

### 4. Marketing Attribution (Task 2D)
- **7-Day Last-Click Attribution**: Assigns orders to marketing channels
- **DM Clicks Processing**: Paid ad click tracking
- **Organic vs Paid Classification**: Distinguishes traffic sources
- **Channel Performance**: Revenue and conversion by marketing channel

### 5. Conversion Funnel (Task 2D)
- **Three-Stage Funnel**:
  1. Sessions (app clicks)
  2. Checkout Intent (DM clicks)
  3. Orders (completed purchases)
- **Organic/Paid Segmentation**: Sessions labeled by traffic source
- **Step-wise Conversion Rates**: Metrics at each funnel stage
- **Geographic Breakdown**: Funnel analysis by country/language

### 6. Exit Point Analysis (Task 2D)
- **Last Event Tracking**: Identifies where users leave the site
- **Exit Pages**: Most common pages where users exit
- **Exit Events**: Types of interactions before leaving
- **Non-Converter Focus**: Analyzes sessions that didn't purchase

### 7. Repeat Buyer Analysis (Task 2F)
- **Customer Identification**: Uses anonymized email as customer proxy
- **First-Time vs Repeat Classification**: Labels each order
- **Cohort Analysis**: First purchase month vs repeat within 3/6 months
- **Retention Metrics**: Repeat customer rate, revenue split, AOV comparison

## Data Files

### Input Files (in `data/raw_data/`)
- `op-orders-o50k.csv` - Orders from 2016-2024 (~83K orders)
- `op-orders-h50k.csv` - Orders from 2021-2025 (~50K orders)
- `op-abandonedbasket.csv` - Abandoned sessions (~2.6K sessions)
- `op-app_clicks.csv` - Website/app event tracking (~966K events)
- `op-dm_clicks.csv` - Paid marketing clicks (~214K clicks)

### Output Files (in `data/processed_data/`)
- `order_header.csv` - Processed orders with all classifications
- `line_items.csv` - Product-level order items
- `sessions.csv` - Session dimension with conversion flags
- `attribution.csv` - Marketing attribution per session
- `funnel.csv` - Conversion funnel data
- `exit_events.csv` - Last event per session
- `exit_sessions.csv` - Exit events for non-converters
- `cohorts.csv` - Repeat buyer cohort analysis

## Setup & Installation

### Requirements
```bash
pandas>=1.5.0
numpy>=1.20.0
matplotlib>=3.5.0
```

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd sales-management-project-op-analytics

# Install dependencies
pip install pandas numpy matplotlib

# Ensure data files are in place
# Place raw CSV files in data/raw_data/
```

## Usage

### Running the Pipeline


# Run the main pipeline notebook
python notebooks/main_pipeline.py


Or execute in Jupyter:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load modules
from modules.load.load_data import load_raw_data
from modules.extract.extract_basket import parse_basket
# ... (see main_pipeline.py for full imports)

# Execute pipeline
orders_o50, orders_h50, abandoned, clicks_app, clicks_dm = load_raw_data()
orders_raw = clean_orders(orders_o50, orders_h50)
orders_raw = parse_basket(orders_raw)
# ... (continue with remaining steps)


### Key Processing Steps

1. **Load Data**

orders_o50, orders_h50, abandoned, clicks_app, clicks_dm = load_raw_data()


2. **Process Orders**

orders_raw = clean_orders(orders_o50, orders_h50)
orders_raw = parse_basket(orders_raw)
order_header_df = build_order_header(orders_raw)
order_line_items_df = extract_all_line_items(orders_raw)


3. **Build Dimensions**

sessions_dim = build_sessions_dim(abandoned)
sessions_dim = compute_conversion_flags(sessions_dim, order_header_df)


4. **Attribution & Funnel**

dm_prepared = prepare_dm_clicks(clicks_dm)
last_clicks = build_last_click_table(dm_prepared)
attribution = apply_attribution_window(order_header_df, last_clicks)
attribution_final = finalize_attribution(attribution)

funnel_df = build_funnel(clicks_app, clicks_dm, order_header_df)


5. **Exit Analysis**

exit_events_df = extract_exit_events(clicks_app)
exit_sessions_df = identify_exit_sessions(exit_events_df, funnel_df)


6. **Repeat Buyers**

order_header_df = identify_customers(order_header_df, customer_col='cust_email')
order_header_df = classify_orders(order_header_df)
repeat_metrics = calculate_repeat_metrics(order_header_df)
cohort_df = build_cohort_analysis(order_header_df, windows=[3, 6])


7. **Export**

export_tables(
    tables={
        'order_header': order_header_df,
        'line_items': order_line_items_df,
        'sessions': sessions_dim,
        'attribution': attribution_final,
        'funnel': funnel_df,
        'exit_events': exit_events_df,
        'exit_sessions': exit_sessions_df,
        'cohorts': cohort_df
    }
)


## Key Metrics & Outputs

### Order Metrics
- Total Orders: 132,961
- Date Range: 2016-09-26 to 2025-09-01
- Total Revenue: €2.79M
- Average Order Value: €21.01
- Shipped Orders: 94.4%

### Customer Metrics
- Unique Customers: 108,549
- Average Orders per Customer: 1.22
- First-Time Orders: ~81.7%
- Repeat Orders: ~18.3%
- Repeat Customer Rate: ~18%

### Funnel Metrics
- Total Sessions: 163,028
- Checkout Intent Rate: ~1-2%
- Conversion Rate: ~0.4-0.5%
- Organic Traffic: ~97%
- Paid Traffic: ~3%

### Attribution Metrics
- Organic/Direct: ~97% of orders
- Paid Channels: ~3% of orders
- 7-Day Attribution Window
- Last-Click Model

## Data Quality Notes

### Limitations
1. **Session ID Coverage**: Only ~97% of orders have session IDs, limiting funnel analysis
2. **Attribution Window**: 98% of orders show as Organic/Direct, suggesting:
   - Most traffic is truly organic
   - Session tracking may have gaps
   - Consider multi-touch attribution for better insights
3. **Customer Identification**: Uses anonymized email as proxy (industry standard)
4. **Time Zones**: Mixed timezone data handled with UTC normalization

### Data Quality Checks
- Null value reports at each processing stage
- Duplicate detection and removal
- Date range verification
- Currency conversion validation
- Session overlap analysis

## Configuration

### FX Rates (in `config.py`)

FX_RATES = {
    'EUR': 1.00,
    'GBP': 1.17,
    'USD': 0.92,
    'SEK': 0.095
}


### Paths (in `config.py`)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw_data"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed_data"


## Development

### Adding New Modules
1. Create module in appropriate directory (`modules/transform/`, etc.)
2. Import in main pipeline
3. Add to export if creating new datasets
4. Update this README

### Code Style
- Functions have docstrings with Args/Returns
- Print statements for progress tracking
- Error handling with informative messages
- Type hints where applicable

## Troubleshooting

### Common Issues

**Import Errors**

# Solution: Restart kernel
%load_ext autoreload
%autoreload 2


**Date Parsing Errors**

# Solution: Use utc=True
pd.to_datetime(df['date'], utc=True, errors='coerce')


**Memory Issues**
- Process data in chunks
- Use `dtype` specifications when loading CSVs
- Filter unnecessary columns early

**Export Path Issues**
- Ensure `data/processed_data/` directory exists
- Check `config.py` paths are correct
- Restart kernel after config changes

## Contact & Support

For questions or issues:
1. Check this README
2. Review code comments and docstrings
3. Examine print statements during execution
4. Check data quality reports in output

## License

[Specify your license here]

## Acknowledgments

- Data provided by OriginalPeople e-commerce platform
- Analytics framework designed for scalability and modularity
- Built with pandas, numpy, and matplotlib