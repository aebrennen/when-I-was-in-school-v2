"""Download Kentucky education data from the Urban Institute Education Data Portal API.

Fetches:
  A. Enrollment totals by year (1986-2023)
  B. Enrollment by race by year (1986-2023)
  C. District finance data by year (1991, 1994-2020)
  D. Directory/teacher counts by year (1986-2023)

All data is for Kentucky (FIPS=21), aggregated from district-level to state-level.
"""

import json
import os
import time
import urllib.request
import urllib.error

from utils import RAW_DIR

BASE_URL = "https://educationdata.urban.org/api/v1"
KY_FIPS = 21
DELAY = 0.5  # seconds between requests

OUT_DIR = os.path.join(RAW_DIR, 'urban_institute')

# Year ranges for each endpoint
ENROLLMENT_YEARS = range(1986, 2024)  # 1986-2023
FINANCE_YEARS = [1991] + list(range(1994, 2021))  # 1991, 1994-2020
DIRECTORY_YEARS = range(1986, 2024)  # 1986-2023


def api_get(url: str, retries=3) -> list:
    """Fetch all pages from the Urban Institute API. Returns list of result dicts."""
    all_results = []
    current_url = url

    while current_url:
        for attempt in range(retries):
            try:
                req = urllib.request.Request(current_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                break
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
                if attempt == retries - 1:
                    print(f"    FAILED after {retries} attempts: {e}")
                    return all_results
                time.sleep(2 ** attempt)

        results = data.get('results', [])
        all_results.extend(results)
        current_url = data.get('next')
        if current_url:
            time.sleep(DELAY)

    return all_results


def fetch_enrollment_totals():
    """Fetch total enrollment per year (all grades, all races, all sexes)."""
    print("Fetching enrollment totals (1986-2023)...")
    by_year = {}

    for year in ENROLLMENT_YEARS:
        url = f"{BASE_URL}/school-districts/ccd/enrollment/{year}/grade-99/?fips={KY_FIPS}&race=99&sex=99"
        results = api_get(url)

        total = 0
        district_count = 0
        for r in results:
            enrollment = r.get('enrollment')
            if enrollment is not None and enrollment >= 0:
                total += enrollment
                district_count += 1

        if district_count > 0:
            by_year[str(year)] = {
                'ccd_year': year,
                'total_enrollment': total,
                'district_count': district_count,
            }
            print(f"  {year}: {total:,} students across {district_count} districts")
        else:
            print(f"  {year}: no data")

        time.sleep(DELAY)

    return by_year


def fetch_enrollment_by_race():
    """Fetch enrollment broken down by race per year."""
    print("\nFetching enrollment by race (1986-2023)...")
    by_year = {}

    # Race codes in the Urban Institute API
    race_labels = {
        1: 'white', 2: 'black', 3: 'hispanic', 4: 'asian',
        5: 'aian', 6: 'nhpi', 7: 'two_or_more', 9: 'unknown',
        20: 'other', 99: 'total'
    }

    for year in ENROLLMENT_YEARS:
        url = f"{BASE_URL}/school-districts/ccd/enrollment/{year}/grade-99/race/?fips={KY_FIPS}&sex=99"
        results = api_get(url)

        race_totals = {}
        for r in results:
            race_code = r.get('race')
            enrollment = r.get('enrollment')
            if race_code is not None and enrollment is not None and enrollment >= 0:
                label = race_labels.get(race_code, f'race_{race_code}')
                race_totals[label] = race_totals.get(label, 0) + enrollment

        if race_totals:
            by_year[str(year)] = {
                'ccd_year': year,
                'enrollment_by_race': race_totals,
            }
            total = race_totals.get('total', sum(v for k, v in race_totals.items() if k != 'total'))
            print(f"  {year}: total={total:,}, {len(race_totals)} race categories")
        else:
            print(f"  {year}: no data")

        time.sleep(DELAY)

    return by_year


def fetch_finance():
    """Fetch district finance data and aggregate to state level."""
    print("\nFetching finance data (1991, 1994-2020)...")
    by_year = {}

    finance_fields = [
        'exp_total', 'exp_current_instruction_total', 'exp_student_transport',
        'outlay_capital_total', 'rev_total', 'rev_local_total',
        'rev_state_total', 'rev_fed_total', 'salaries_total',
        'salaries_instruction', 'enrollment_fall_responsible',
    ]

    for year in FINANCE_YEARS:
        url = f"{BASE_URL}/school-districts/ccd/finance/{year}/?fips={KY_FIPS}"
        results = api_get(url)

        if not results:
            print(f"  {year}: no data")
            time.sleep(DELAY)
            continue

        sums = {f: 0 for f in finance_fields}
        district_count = 0

        for r in results:
            has_data = False
            for field in finance_fields:
                val = r.get(field)
                if val is not None and val >= 0:
                    sums[field] += val
                    has_data = True
            if has_data:
                district_count += 1

        if district_count > 0:
            by_year[str(year)] = {
                'fiscal_year': year,
                'district_count': district_count,
                **sums,
            }
            enrollment = sums.get('enrollment_fall_responsible', 0)
            exp = sums.get('exp_total', 0)
            pp = round(exp / enrollment) if enrollment > 0 else None
            print(f"  {year}: {district_count} districts, exp_total=${exp:,.0f}, enrollment={enrollment:,}, per_pupil=${pp:,}" if pp else f"  {year}: {district_count} districts")
        else:
            print(f"  {year}: no data")

        time.sleep(DELAY)

    return by_year


def fetch_directory():
    """Fetch directory data for teacher FTE counts."""
    print("\nFetching directory/teacher data (1986-2023)...")
    by_year = {}

    for year in DIRECTORY_YEARS:
        url = f"{BASE_URL}/school-districts/ccd/directory/{year}/?fips={KY_FIPS}"
        results = api_get(url)

        total_teachers = 0
        total_enrollment = 0
        district_count = 0

        for r in results:
            teachers = r.get('teachers_total_fte')
            enrollment = r.get('enrollment')
            if teachers is not None and teachers >= 0:
                total_teachers += teachers
                district_count += 1
            if enrollment is not None and enrollment >= 0:
                total_enrollment += enrollment

        if district_count > 0:
            ratio = round(total_enrollment / total_teachers, 1) if total_teachers > 0 else None
            by_year[str(year)] = {
                'ccd_year': year,
                'total_teachers_fte': round(total_teachers, 1),
                'total_enrollment': total_enrollment,
                'student_teacher_ratio': ratio,
                'district_count': district_count,
            }
            print(f"  {year}: {total_teachers:,.1f} teachers FTE, ratio={ratio}")
        else:
            print(f"  {year}: no data")

        time.sleep(DELAY)

    return by_year


def fetch_district_list():
    """Fetch district names and IDs from the most recent directory year."""
    print("\nFetching district list from 2023 directory...")
    url = f"{BASE_URL}/school-districts/ccd/directory/2023/?fips={KY_FIPS}"
    results = api_get(url)

    districts = []
    for r in results:
        leaid = r.get('leaid')
        name = r.get('lea_name')
        if leaid and name:
            districts.append({
                'leaid': str(leaid),
                'name': name.strip(),
            })

    districts.sort(key=lambda d: d['name'])
    print(f"  Found {len(districts)} districts")
    return districts


def fetch_district_finance():
    """Fetch per-district finance data for all years, preserving individual records."""
    print("\nFetching district-level finance data (1991, 1994-2020)...")
    by_year = {}

    fields_to_keep = [
        'leaid', 'lea_name', 'exp_total', 'rev_total',
        'rev_local_total', 'rev_state_total', 'rev_fed_total',
        'enrollment_fall_responsible',
    ]

    for year in FINANCE_YEARS:
        url = f"{BASE_URL}/school-districts/ccd/finance/{year}/?fips={KY_FIPS}"
        results = api_get(url)

        if not results:
            print(f"  {year}: no data")
            time.sleep(DELAY)
            continue

        districts = []
        for r in results:
            leaid = r.get('leaid')
            exp_total = r.get('exp_total')
            enrollment = r.get('enrollment_fall_responsible')
            if not leaid or exp_total is None or exp_total < 0:
                continue
            record = {k: r.get(k) for k in fields_to_keep}
            record['leaid'] = str(record['leaid'])
            if record.get('lea_name'):
                record['lea_name'] = record['lea_name'].strip()
            districts.append(record)

        by_year[str(year)] = districts
        print(f"  {year}: {len(districts)} districts with finance data")
        time.sleep(DELAY)

    return by_year


def save_json(data, filename):
    path = os.path.join(OUT_DIR, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  Saved to {path}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    enrollment = fetch_enrollment_totals()
    save_json(enrollment, 'enrollment_by_year.json')

    enrollment_race = fetch_enrollment_by_race()
    save_json(enrollment_race, 'enrollment_by_race_year.json')

    finance = fetch_finance()
    save_json(finance, 'finance_by_year.json')

    directory = fetch_directory()
    save_json(directory, 'directory_by_year.json')

    district_list = fetch_district_list()
    save_json(district_list, 'district_list.json')

    district_finance = fetch_district_finance()
    save_json(district_finance, 'district_finance_by_year.json')

    print(f"\nDone. Data saved to {OUT_DIR}/")
    print(f"  Enrollment: {len(enrollment)} years")
    print(f"  Enrollment by race: {len(enrollment_race)} years")
    print(f"  Finance: {len(finance)} years")
    print(f"  Directory/teachers: {len(directory)} years")
    print(f"  District list: {len(district_list)} districts")
    print(f"  District finance: {len(district_finance)} years")


if __name__ == '__main__':
    main()
