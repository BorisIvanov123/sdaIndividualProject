from pathlib import Path

# Resolve project root (directory where config.py lives)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_RAW = PROJECT_ROOT / "data" / "raw_data"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed_data"

FX_RATES = {
    'EUR': 1.00,    # Base
    'GBP': 1.15,    # GBP/EUR averaged ~1.12–1.18
    'USD': 0.90,    # USD/EUR averaged ~0.85–0.95
    'SEK': 0.095    # EUR/SEK averaged ~10–11.5 → ~0.087–0.10 EUR
}
