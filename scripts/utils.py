"""Shared utilities for the When I Was in School data pipeline."""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

CPI_FACTORS_PATH = os.path.join(PROCESSED_DIR, 'cpi_adjustment_factors.json')
INFLATION_BASE_YEAR = 2024

GRAD_YEAR_MIN = 1926
GRAD_YEAR_MAX = 2025


def grad_year_to_school_year(grad_year: int) -> str:
    """Convert graduation year to school year string.
    Grad year 2005 -> '2004-2005' (the SY the student was a senior).
    """
    return f"{grad_year - 1}-{grad_year}"


def grad_year_to_fiscal_year(grad_year: int) -> int:
    """Map graduation year to fiscal year for finance data.
    FY typically aligns with the spring of the school year.
    Grad year 2005 -> FY 2005.
    """
    return grad_year


def grad_year_to_ccd_year(grad_year: int) -> int:
    """Map graduation year to the CCD data year.
    CCD enrollment year refers to the fall of the school year.
    Grad year 2005 (SY 2004-2005) -> CCD year 2004 (fall 2004 enrollment).
    """
    return grad_year - 1


def load_cpi_factors() -> dict:
    """Load CPI adjustment factors from processed JSON.
    Returns dict of {year(int): multiplier_to_2024_dollars(float)}.
    """
    with open(CPI_FACTORS_PATH, 'r') as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}


def inflate_to_2024(amount, year: int, cpi_factors: dict):
    """Adjust a dollar amount from `year` to 2024 dollars.
    Returns rounded int, or None if amount is None/missing.
    """
    if amount is None or year not in cpi_factors:
        return None
    try:
        return round(float(amount) * cpi_factors[year])
    except (ValueError, TypeError):
        return None


def safe_div(numerator, denominator, digits=1):
    """Safe division returning rounded float or None."""
    if numerator is None or denominator is None:
        return None
    try:
        d = float(denominator)
        if d == 0:
            return None
        return round(float(numerator) / d, digits)
    except (ValueError, TypeError):
        return None


def safe_pct(part, total, digits=1):
    """Compute percentage (0-100 scale), or None if inputs are missing."""
    if part is None or total is None:
        return None
    try:
        t = float(total)
        if t == 0:
            return None
        return round(float(part) / t * 100, digits)
    except (ValueError, TypeError):
        return None


def safe_round(value, digits=0):
    """Round a value, returning None if input is None."""
    if value is None:
        return None
    try:
        return round(float(value), digits) if digits > 0 else int(round(float(value)))
    except (ValueError, TypeError):
        return None
