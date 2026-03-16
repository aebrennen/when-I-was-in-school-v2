#!/usr/bin/env python3
"""
Build Phase 2 data files for V2:
  - national-teacher-salary.json
  - state-teacher-salary.json
  - cost-of-living.json

Uses CPI adjustment factors and nominal salary data from NCES/NEA.
Gap years are linearly interpolated.
"""

import json
import os
import math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CPI_PATH = os.path.join(BASE_DIR, "data", "processed", "cpi_adjustment_factors.json")
TEACHER_PATH = os.path.join(BASE_DIR, "data", "output", "teacher-salary.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

HOURS_BASIS = 1402  # 187 days x 7.5 hrs

with open(CPI_PATH) as f:
    CPI = json.load(f)

with open(TEACHER_PATH) as f:
    TEACHER = json.load(f)


def cpi_adjust(nominal, year):
    """Adjust nominal dollars from `year` to 2024 dollars."""
    factor = CPI.get(str(year))
    if factor is None or nominal is None:
        return None
    return round(nominal * factor)


def interpolate(data_points, min_year, max_year):
    """Linear interpolation between known data points.
    data_points: dict of {year: value}
    Returns: dict of {year: value} for all years in range.
    """
    sorted_years = sorted(data_points.keys())
    result = {}
    for y in range(min_year, max_year + 1):
        if y in data_points:
            result[y] = data_points[y]
        else:
            # Find surrounding known points
            lower = max((k for k in sorted_years if k <= y), default=None)
            upper = min((k for k in sorted_years if k >= y), default=None)
            if lower is not None and upper is not None and lower != upper:
                frac = (y - lower) / (upper - lower)
                result[y] = round(data_points[lower] + frac * (data_points[upper] - data_points[lower]))
            elif lower is not None:
                result[y] = data_points[lower]
            elif upper is not None:
                result[y] = data_points[upper]
    return result


def school_year_str(grad_year):
    return f"{grad_year - 1}-{grad_year}"


# ============================================================
# 1. NATIONAL TEACHER SALARY
# ============================================================
# NCES Table 211.60 — US average teacher salary, nominal dollars
# Key benchmark years (school year end = fiscal year = grad year)
NATIONAL_NOMINAL = {
    1970: 8626,
    1972: 9705,
    1974: 10770,
    1976: 12070,
    1978: 13550,
    1980: 15970,
    1982: 19274,
    1984: 21935,
    1986: 25199,
    1988: 28034,
    1990: 31367,
    1992: 34063,
    1994: 35737,
    1996: 37642,
    1998: 39350,
    2000: 41807,
    2002: 44683,
    2004: 46752,
    2006: 49026,
    2008: 52800,
    2010: 55370,
    2012: 55418,
    2014: 56383,
    2016: 58064,
    2018: 60483,
    2020: 64133,
    2021: 65293,
    2022: 66397,
    2024: 72030,
    2025: 74177,
}

# Interpolate all years
national_interp = interpolate(NATIONAL_NOMINAL, 1970, 2025)

# Current year = latest available
nat_current_year = 2024
nat_current_nominal = NATIONAL_NOMINAL[nat_current_year]
nat_current_adjusted = cpi_adjust(nat_current_nominal, nat_current_year)
nat_current_hourly = round(nat_current_adjusted / HOURS_BASIS, 2) if nat_current_adjusted else None

national_salary = {
    "metadata": {
        "source": "NCES Digest of Education Statistics, Table 211.60; NEA Rankings & Estimates",
        "inflation_base_year": 2024,
        "hours_basis": HOURS_BASIS,
        "notes": "US average classroom teacher salary. Gap years linearly interpolated."
    },
    "current_year": {
        "school_year": school_year_str(nat_current_year),
        "nominal": nat_current_nominal,
        "adjusted": nat_current_adjusted,
        "hourly_rate": nat_current_hourly,
    },
    "by_grad_year": {}
}

for gy in range(1970, 2026):
    nom = national_interp.get(gy)
    adj = cpi_adjust(nom, gy)
    hourly = round(adj / HOURS_BASIS, 2) if adj else None
    national_salary["by_grad_year"][str(gy)] = {
        "school_year": school_year_str(gy),
        "nominal": nom,
        "adjusted": adj,
        "hourly_rate": hourly,
        "data_available": adj is not None,
    }

with open(os.path.join(OUTPUT_DIR, "national-teacher-salary.json"), "w") as f:
    json.dump(national_salary, f, indent=2)
print("Created national-teacher-salary.json")


# ============================================================
# 2. STATE TEACHER SALARY (KY + 7 border states)
# ============================================================
# NCES Table 211.60 — nominal dollars by state, selected years
STATE_NOMINAL = {
    "KY": {1970: 6953, 1990: 26292, 2000: 36380, 2010: 49543, 2020: 53907, 2022: 54574, 2024: 58325},
    "OH": {1970: 8300, 1990: 31218, 2000: 41436, 2010: 55958, 2020: 61406, 2022: 63153, 2024: 68236},
    "IN": {1970: 8833, 1990: 30902, 2000: 41850, 2010: 49986, 2020: 51745, 2022: 54126, 2024: 58620},
    "IL": {1970: 9569, 1990: 32794, 2000: 46486, 2010: 62077, 2020: 68083, 2022: 72301, 2024: 75978},
    "MO": {1970: 7799, 1990: 27094, 2000: 35656, 2010: 45317, 2020: 50817, 2022: 52481, 2024: 55132},
    "TN": {1970: 7050, 1990: 27052, 2000: 36328, 2010: 46290, 2020: 51862, 2022: 53619, 2024: 58630},
    "VA": {1970: 8070, 1990: 30938, 2000: 38744, 2010: 50015, 2020: 57665, 2022: 59965, 2024: 66327},
    "WV": {1970: 7650, 1990: 22842, 2000: 35009, 2010: 45959, 2020: 50238, 2022: 50315, 2024: 55516},
}

# 2023-24 ranks from the brief
STATE_RANKS = {
    "IL": 12, "OH": 21, "VA": 25, "IN": 32, "TN": 34, "KY": 42, "WV": 47, "MO": 48
}

state_salary = {
    "metadata": {
        "source": "NCES Digest of Education Statistics, Table 211.60; NEA Rankings & Estimates",
        "inflation_base_year": 2024,
        "hours_basis": HOURS_BASIS,
        "notes": "State average classroom teacher salary. Gap years linearly interpolated between NCES benchmark years.",
        "ranks": STATE_RANKS,
        "rank_year": "2023-2024",
    },
}

for state, benchmarks in STATE_NOMINAL.items():
    interp = interpolate(benchmarks, 1970, 2025)

    cur_year = 2024
    cur_nom = benchmarks.get(cur_year)
    cur_adj = cpi_adjust(cur_nom, cur_year)
    cur_hourly = round(cur_adj / HOURS_BASIS, 2) if cur_adj else None

    state_data = {
        "current_year": {
            "school_year": school_year_str(cur_year),
            "nominal": cur_nom,
            "adjusted": cur_adj,
            "hourly_rate": cur_hourly,
            "rank": STATE_RANKS.get(state),
        },
        "by_grad_year": {}
    }

    for gy in range(1970, 2026):
        nom = interp.get(gy)
        adj = cpi_adjust(nom, gy)
        hourly = round(adj / HOURS_BASIS, 2) if adj else None
        state_data["by_grad_year"][str(gy)] = {
            "school_year": school_year_str(gy),
            "nominal": nom,
            "adjusted": adj,
            "hourly_rate": hourly,
            "data_available": adj is not None,
        }

    state_salary[state] = state_data

with open(os.path.join(OUTPUT_DIR, "state-teacher-salary.json"), "w") as f:
    json.dump(state_salary, f, indent=2)
print("Created state-teacher-salary.json")


# ============================================================
# 3. COST OF LIVING
# ============================================================
# CPI sub-indices (national, annual averages) — base period varies but we
# only need relative change, anchored to current KY dollar amounts.
#
# FRED series used:
#   Rent:        CUSR0000SEHA   (Rent of primary residence)
#   Gas:         CUSR0000SETB01 (Gasoline, all types)
#   Electricity: CUSR0000SEHF01 (Electricity)
#   Food:        CUSR0000SAF11  (Food at home)
#
# We store CPI index values for benchmark years and interpolate.
# Then compute: cost_then = current_cost * (index_then / index_now)
# Current KY anchors (annual):
#   Rent: $12,852/yr ($1,071/mo)
#   Gas: $2,400/yr (est ~$200/mo)
#   Utilities: $5,580/yr ($465/mo)
#   Food: $7,200/yr ($600/mo)

CURRENT_ANCHOR_YEAR = 2024

# Annual KY costs (current dollars)
KY_ANNUAL = {
    "rent": 12852,
    "gas": 2400,
    "utilities": 5580,
    "food": 7200,
}

# CPI sub-index values (annual averages from FRED, approximate)
# These are index values, not dollars — only relative change matters.
CPI_SUBINDEX = {
    "rent": {
        1970: 30.6, 1975: 37.0, 1980: 51.5, 1985: 72.5, 1990: 93.0,
        1995: 108.6, 2000: 121.4, 2005: 143.2, 2010: 160.5, 2015: 178.2,
        2020: 207.2, 2021: 212.6, 2022: 226.3, 2023: 245.8, 2024: 259.4,
    },
    "gas": {
        1970: 23.1, 1975: 35.7, 1980: 73.7, 1985: 68.4, 1990: 65.7,
        1995: 61.4, 2000: 81.7, 2005: 119.5, 2010: 145.4, 2015: 115.6,
        2020: 111.2, 2021: 139.7, 2022: 177.5, 2023: 157.4, 2024: 153.8,
    },
    "utilities": {
        1970: 18.1, 1975: 25.0, 1980: 42.5, 1985: 63.3, 1990: 70.0,
        1995: 78.5, 2000: 82.1, 2005: 107.0, 2010: 120.4, 2015: 126.5,
        2020: 127.0, 2021: 132.0, 2022: 148.8, 2023: 152.0, 2024: 154.3,
    },
    "food": {
        1970: 28.0, 1975: 39.5, 1980: 55.2, 1985: 62.5, 1990: 74.7,
        1995: 82.7, 2000: 89.8, 2005: 97.2, 2010: 112.1, 2015: 117.0,
        2020: 122.7, 2021: 126.5, 2022: 141.8, 2023: 145.0, 2024: 148.2,
    },
}

# Interpolate all sub-indices
cpi_interp = {}
for cat, benchmarks in CPI_SUBINDEX.items():
    cpi_interp[cat] = interpolate(benchmarks, 1970, 2025)

# Get KY teacher salary for each grad year
ky_salary = {}
for gy_str, entry in TEACHER["by_grad_year"].items():
    if entry.get("data_available") and entry.get("adjusted"):
        ky_salary[int(gy_str)] = entry["adjusted"]
ky_salary_current = TEACHER["current_year"]["adjusted"]

cost_of_living = {
    "metadata": {
        "source": "FRED CPI sub-indices (CUSR0000SEHA, CUSR0000SETB01, CUSR0000SEHF01, CUSR0000SAF11), anchored to Kentucky costs",
        "inflation_base_year": 2024,
        "methodology": "National CPI indices to calculate relative price change, anchored to current Kentucky-specific dollar amounts",
        "categories": {
            "rent": {"label": "Rent", "emoji": "\U0001F3E0", "current_annual": KY_ANNUAL["rent"]},
            "gas": {"label": "Gas", "emoji": "\u26FD", "current_annual": KY_ANNUAL["gas"]},
            "utilities": {"label": "Utilities", "emoji": "\U0001F50C", "current_annual": KY_ANNUAL["utilities"]},
            "food": {"label": "Groceries", "emoji": "\U0001F6D2", "current_annual": KY_ANNUAL["food"]},
        },
    },
    "current_year": {
        "salary": ky_salary_current,
        "rent_annual": KY_ANNUAL["rent"],
        "gas_annual": KY_ANNUAL["gas"],
        "utilities_annual": KY_ANNUAL["utilities"],
        "food_annual": KY_ANNUAL["food"],
        "rent_pct": round(KY_ANNUAL["rent"] / ky_salary_current, 4),
        "gas_pct": round(KY_ANNUAL["gas"] / ky_salary_current, 4),
        "utilities_pct": round(KY_ANNUAL["utilities"] / ky_salary_current, 4),
        "food_pct": round(KY_ANNUAL["food"] / ky_salary_current, 4),
        "total_pct": round(sum(KY_ANNUAL.values()) / ky_salary_current, 4),
    },
    "by_grad_year": {},
}

for gy in range(1970, 2026):
    salary = ky_salary.get(gy)
    entry = {"grad_year": gy, "data_available": False}

    if salary is not None:
        costs = {}
        total = 0
        for cat in ["rent", "gas", "utilities", "food"]:
            idx_then = cpi_interp[cat].get(gy)
            idx_now = cpi_interp[cat].get(CURRENT_ANCHOR_YEAR)
            if idx_then is not None and idx_now is not None and idx_now > 0:
                # Cost in THEN year in THEN dollars, then CPI-adjust to 2024
                cost_then_nominal = KY_ANNUAL[cat] * (idx_then / idx_now)
                cost_then_adjusted = cpi_adjust(cost_then_nominal, gy)
                pct = round(cost_then_adjusted / salary, 4) if salary > 0 else 0
                costs[f"{cat}_annual_adjusted"] = cost_then_adjusted
                costs[f"{cat}_pct"] = pct
                total += cost_then_adjusted
            else:
                costs[f"{cat}_annual_adjusted"] = None
                costs[f"{cat}_pct"] = None

        entry.update(costs)
        entry["total_annual_adjusted"] = total
        entry["total_pct"] = round(total / salary, 4) if salary > 0 else None
        entry["salary_adjusted"] = salary
        entry["data_available"] = True

    cost_of_living["by_grad_year"][str(gy)] = entry

with open(os.path.join(OUTPUT_DIR, "cost-of-living.json"), "w") as f:
    json.dump(cost_of_living, f, indent=2)
print("Created cost-of-living.json")

print("\nDone! All Phase 2 data files created.")
