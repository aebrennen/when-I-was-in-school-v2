"""Build district_salary.json for the frontend.

Maps KDE district salary data to Urban Institute LEAIDs so the frontend
can look up district-level average classroom teacher salaries when a user
selects a district.

Produces:
  data/output/district_salary.json
"""

import json
import os
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

from utils import (
    GRAD_YEAR_MIN, GRAD_YEAR_MAX,
    load_cpi_factors, inflate_to_2024,
    grad_year_to_school_year, grad_year_to_fiscal_year,
)


def build_kde_to_leaid_map():
    """Build mapping from KDE 3-digit district codes to 7-digit LEAIDs."""
    with open(os.path.join(OUTPUT_DIR, 'districts.json')) as f:
        ui_districts = json.load(f)

    with open(os.path.join(PROCESSED_DIR, 'kde_salary_by_district.json')) as f:
        kde_data = json.load(f)

    # Name-based lookup for UI districts
    ui_by_exact = {}
    for d in ui_districts:
        ui_by_exact[d['name'].upper().strip()] = d['leaid']

    # Verified manual mappings for districts with truncated/abbreviated names in KDE
    manual = {
        '133': '2101320',  # Corbin Independent
        '134': '2101350',  # Covington Independent
        '146': '2101500',  # Dawson Springs Independent
        '149': '2101590',  # East Bernstadt Independent
        '157': '2101740',  # Erlanger-Elsmere Independent
        '176': '2102040',  # Fort Thomas Independent
        '225': '2102460',  # Hancock County
        '341': '2103480',  # Lincoln County
        '502': '2104980',  # Raceland-Worthington Independent
        '525': '2105460',  # Southgate Independent (appears as 'STT' in KDE)
        '567': '2105700',  # Walton-Verona Independent
    }

    # Districts that exist in KDE but not in CCD/Urban Institute (very small, possibly consolidated)
    kde_only = {'242', '436', '496', '533', '586'}  # Harrodsburg, Monticello, Providence, Silver Grove, West Point

    mapping = {}
    unmatched = []

    for kde_num, info in kde_data['districts'].items():
        kde_name = info['name'].upper().strip()

        if kde_num in manual:
            mapping[kde_num] = manual[kde_num]
        elif kde_num in kde_only:
            continue  # Skip — no matching LEAID
        elif kde_name in ui_by_exact:
            mapping[kde_num] = ui_by_exact[kde_name]
        elif kde_name + ' COUNTY' in ui_by_exact:
            mapping[kde_num] = ui_by_exact[kde_name + ' COUNTY']
        elif kde_name + ' INDEPENDENT' in ui_by_exact:
            mapping[kde_num] = ui_by_exact[kde_name + ' INDEPENDENT']
        else:
            unmatched.append((kde_num, kde_name))

    if unmatched:
        print(f"  WARNING: {len(unmatched)} unmatched KDE districts:")
        for code, name in unmatched:
            print(f"    {code}: {name}")

    return mapping, kde_data


def main():
    print("Building district_salary.json...")
    cpi_factors = load_cpi_factors()
    mapping, kde_data = build_kde_to_leaid_map()
    print(f"  Mapped {len(mapping)} KDE districts to LEAIDs")

    # Build output: keyed by LEAID, containing salary by graduation year
    by_district = {}

    for kde_num, leaid in mapping.items():
        info = kde_data['districts'].get(kde_num, {})
        salaries = info.get('salaries_by_school_year', {})

        by_grad_year = {}
        for sy, salary_nom in salaries.items():
            # Parse school year to get graduation year
            # sy format: "2004-2005" -> grad year 2005
            parts = sy.split('-')
            if len(parts) == 2:
                try:
                    grad_year = int(parts[1])
                except ValueError:
                    continue

                if grad_year < GRAD_YEAR_MIN or grad_year > GRAD_YEAR_MAX:
                    continue

                fy = grad_year_to_fiscal_year(grad_year)
                adjusted = inflate_to_2024(salary_nom, fy, cpi_factors)

                by_grad_year[str(grad_year)] = {
                    'school_year': sy,
                    'avg_salary_nominal': int(salary_nom),
                    'avg_salary': adjusted,
                }

        if by_grad_year:
            by_district[leaid] = {
                'name': info.get('name', ''),
                'kde_code': kde_num,
                'by_grad_year': by_grad_year,
            }

    result = {
        'source': 'Kentucky Department of Education, Average Classroom Teacher Salaries',
        'methodology': 'Average classroom teacher salary per district',
        'by_district': by_district,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, 'district_salary.json')
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2)

    total_records = sum(len(d['by_grad_year']) for d in by_district.values())
    print(f"  Wrote {out_path}")
    print(f"  {len(by_district)} districts, {total_records} district-year records")

    # Spot check
    sample_leaid = '2100030'  # Adair County
    if sample_leaid in by_district:
        d = by_district[sample_leaid]
        print(f"\n  Spot check: {d['name']} ({sample_leaid})")
        for gy in ['1990', '2005', '2024']:
            entry = d['by_grad_year'].get(gy)
            if entry:
                print(f"    {gy}: nom=${entry['avg_salary_nominal']:,}, adj=${entry['avg_salary']:,}")


if __name__ == '__main__':
    main()
