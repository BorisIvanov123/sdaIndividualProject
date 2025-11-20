"""
export.py
---------
Handles exporting cleaned dataframes to disk.

Includes:
- ensure_output_dir()
- export_tables()
"""
import pandas as pd
from typing import Dict, Optional
from pathlib import Path
from ..config import DATA_PROCESSED

def ensure_output_dir(path: Path = DATA_PROCESSED) -> Path:
    """Ensure output directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def export_tables(
    tables: Optional[Dict[str, pd.DataFrame]] = None,
    path: Path = DATA_PROCESSED,
    **kwargs
) -> None:
    """
    Export multiple tables to CSV in the processed_data directory.

    Can be called in two ways:
    1. export_tables(tables={'order_header': df1, 'line_items': df2})
    2. export_tables(order_header=df1, line_items=df2)

    Args:
        tables: Dictionary of {filename: DataFrame}
        path: Output directory path (defaults to DATA_PROCESSED from config)
        **kwargs: Alternative way to pass tables as keyword arguments
    """
    ensure_output_dir(path)

    # Use tables dict if provided, otherwise use kwargs
    tables_to_export = tables if tables is not None else kwargs

    # Export each table
    for filename, df in tables_to_export.items():
        output_path = path / f"{filename}.csv"
        df.to_csv(output_path, index=False)
        print(f"✓ Exported {filename}.csv")

    print(f"\n✓ All {len(tables_to_export)} tables exported to '{path}/'")