"""Download CPI-U annual averages from FRED and compute inflation adjustment factors."""

import csv
import json
import os
import urllib.request

from utils import RAW_DIR, PROCESSED_DIR, INFLATION_BASE_YEAR

FRED_URL = (
    "https://fred.stlouisfed.org/graph/fredgraph.csv"
    "?id=CPIAUCNS&freq=a&cosd=1913-01-01&coed=2025-12-31"
)
RAW_CSV_PATH = os.path.join(RAW_DIR, 'cpi', 'cpi_annual_1913_2025.csv')
FACTORS_PATH = os.path.join(PROCESSED_DIR, 'cpi_adjustment_factors.json')


def fetch_cpi():
    print("Downloading CPI-U annual averages from FRED...")
    req = urllib.request.Request(FRED_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode('utf-8')

    os.makedirs(os.path.dirname(RAW_CSV_PATH), exist_ok=True)
    with open(RAW_CSV_PATH, 'w') as f:
        f.write(raw)
    print(f"  Saved raw CSV to {RAW_CSV_PATH}")

    # Parse: columns are DATE (YYYY-MM-DD) and CPIAUCNS (float)
    cpi_by_year = {}
    reader = csv.DictReader(raw.strip().splitlines())
    for row in reader:
        date_str = row.get('DATE') or row.get('observation_date') or ''
        value_str = row.get('CPIAUCNS') or row.get('value') or ''
        if not date_str or not value_str or value_str == '.':
            continue
        year = int(date_str[:4])
        cpi_by_year[year] = float(value_str)

    if INFLATION_BASE_YEAR not in cpi_by_year:
        raise ValueError(f"CPI value for base year {INFLATION_BASE_YEAR} not found in FRED data")

    base_cpi = cpi_by_year[INFLATION_BASE_YEAR]
    print(f"  Base year {INFLATION_BASE_YEAR} CPI: {base_cpi}")

    # Compute adjustment factors
    factors = {}
    for year, cpi in sorted(cpi_by_year.items()):
        factors[str(year)] = round(base_cpi / cpi, 4)

    os.makedirs(os.path.dirname(FACTORS_PATH), exist_ok=True)
    with open(FACTORS_PATH, 'w') as f:
        json.dump(factors, f, indent=2)
    print(f"  Saved {len(factors)} CPI adjustment factors to {FACTORS_PATH}")

    # Sanity checks
    assert factors[str(INFLATION_BASE_YEAR)] == 1.0, "Base year factor should be 1.0"
    factor_1990 = factors.get('1990')
    if factor_1990:
        print(f"  Sanity check — 1990 factor: {factor_1990}x (expect ~2.3-2.5)")
    factor_2000 = factors.get('2000')
    if factor_2000:
        print(f"  Sanity check — 2000 factor: {factor_2000}x (expect ~1.7-1.9)")

    return factors


if __name__ == '__main__':
    fetch_cpi()
