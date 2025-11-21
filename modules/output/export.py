"""
export.py
---------
Handles exporting cleaned dataframes to disk.

Now exports to **Parquet** (much smaller + faster loading on Render).
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
    export_csv: bool = False,   # ← optional CSV backup
    **kwargs
) -> None:
    """
    Export multiple tables to Parquet (and optionally CSV).

    Args:
        tables: dict {filename: df}
        path: output directory
        export_csv: if True, also export CSV for debugging
        **kwargs: alternative way to pass tables
    """
    ensure_output_dir(path)

    tables_to_export = tables if tables is not None else kwargs

    for filename, df in tables_to_export.items():

        # ---- PARQUET EXPORT ----
        parquet_path = path / f"{filename}.parquet"
        df.to_parquet(parquet_path, index=False)
        print(f"✓ Exported {filename}.parquet")

        # ---- OPTIONAL CSV EXPORT ----
        if export_csv:
            csv_path = path / f"{filename}.csv"
            df.to_csv(csv_path, index=False)
            print(f"✓ (CSV backup) {filename}.csv")

    print(f"\n✓ Exported {len(tables_to_export)} tables to {path}/")
