from pathlib import Path

# Resolve project root (directory where config.py lives)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = PROJECT_ROOT / "data" / "raw_data"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed_data"

FX_RATES = {
    'EUR': 1.00,
    'GBP': 1.17,
    'USD': 0.92,
    'SEK': 0.095
}
