"""Master processing script: reads all raw data and generates the 5 output JSON files.

Generates:
  data/output/finance.json
  data/output/enrollment.json
  data/output/teachers.json
  data/output/assessment.json
  data/output/meta.json
"""

import csv
import json
import os
from datetime import datetime

from utils import (
    RAW_DIR, OUTPUT_DIR, PROCESSED_DIR,
    GRAD_YEAR_MIN, GRAD_YEAR_MAX, INFLATION_BASE_YEAR,
    grad_year_to_school_year, grad_year_to_fiscal_year, grad_year_to_ccd_year,
    load_cpi_factors, inflate_to_2024, safe_div, safe_pct, safe_round,
)

UI_DIR = os.path.join(RAW_DIR, 'urban_institute')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def load_csv_dict(path, key_col, val_col):
    """Load a CSV into a dict mapping key_col -> val_col (as float)."""
    out = {}
    if not os.path.exists(path):
        return out
    with open(path) as f:
        for row in csv.DictReader(f):
            k = row.get(key_col, '').strip()
            v = row.get(val_col, '').strip()
            if k and v:
                try:
                    out[k] = float(v)
                except ValueError:
                    pass
    return out


def save_output(data, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"  Wrote {path}")


# ---------------------------------------------------------------------------
# Finance
# ---------------------------------------------------------------------------

def generate_finance(cpi_factors):
    print("\nGenerating finance.json...")
    finance_raw = load_json(os.path.join(UI_DIR, 'finance_by_year.json'))

    # KDE finance data for years beyond Urban Institute coverage
    kde_finance_path = os.path.join(PROCESSED_DIR, 'kde_finance_statewide.json')
    kde_finance = {}
    if os.path.exists(kde_finance_path):
        kde_raw = load_json(kde_finance_path)
        kde_finance = kde_raw.get('by_fiscal_year', {})
        print(f"  Loaded KDE finance data: {len(kde_finance)} fiscal years")

    # SEEK data: keyed by fiscal year string
    seek_path = os.path.join(RAW_DIR, 'seek', 'seek_base_guarantee.csv')
    seek_data = load_csv_dict(seek_path, 'fiscal_year', 'base_guarantee_per_pupil')

    by_grad_year = {}

    for grad_year in range(GRAD_YEAR_MIN, GRAD_YEAR_MAX + 1):
        fy = grad_year_to_fiscal_year(grad_year)
        fy_str = str(fy)
        sy = grad_year_to_school_year(grad_year)

        # CCD finance data (keyed by fiscal year in Urban Institute data)
        fin = finance_raw.get(fy_str, {})

        enrollment = fin.get('enrollment_fall_responsible')
        exp_total = fin.get('exp_total')
        exp_instruction = fin.get('exp_current_instruction_total')
        exp_transport = fin.get('exp_student_transport')
        exp_facilities = fin.get('outlay_capital_total')

        pp_total = safe_round(safe_div(exp_total, enrollment, 0))
        pp_instruction = safe_round(safe_div(exp_instruction, enrollment, 0))
        pp_transportation = safe_round(safe_div(exp_transport, enrollment, 0))
        pp_facilities = safe_round(safe_div(exp_facilities, enrollment, 0))

        finance_source = 'urban_institute'

        # If no Urban Institute data, try KDE data
        if pp_total is None and fy_str in kde_finance:
            kde = kde_finance[fy_str]
            pp_total = kde.get('per_pupil_total')
            pp_instruction = kde.get('per_pupil_instruction')
            pp_transportation = kde.get('per_pupil_transportation')
            pp_facilities = kde.get('per_pupil_facilities')
            finance_source = 'kde'

        seek_nominal = seek_data.get(fy_str)
        if seek_nominal is not None:
            seek_nominal = int(seek_nominal)

        has_finance = pp_total is not None
        has_seek = seek_nominal is not None

        entry = {
            'school_year': sy,
            'fiscal_year': fy,
            'per_pupil_total_nominal': pp_total,
            'per_pupil_total': inflate_to_2024(pp_total, fy, cpi_factors),
            'per_pupil_instruction_nominal': pp_instruction,
            'per_pupil_instruction': inflate_to_2024(pp_instruction, fy, cpi_factors),
            'per_pupil_transportation_nominal': pp_transportation,
            'per_pupil_transportation': inflate_to_2024(pp_transportation, fy, cpi_factors),
            'per_pupil_facilities_nominal': pp_facilities,
            'per_pupil_facilities': inflate_to_2024(pp_facilities, fy, cpi_factors),
            'seek_base_guarantee_nominal': seek_nominal,
            'seek_base_guarantee': inflate_to_2024(seek_nominal, fy, cpi_factors),
            'data_available': has_finance or has_seek,
            'source': _finance_source(has_finance, finance_source, has_seek),
        }
        by_grad_year[str(grad_year)] = entry

    # Current year: use the most recent available data
    current = _find_most_recent(by_grad_year, 'per_pupil_total')

    result = {
        'metadata': {
            'sources': [
                'NCES CCD F-33 School District Finance Survey via Urban Institute Education Data Portal',
                'Kentucky Department of Education Annual Financial Reports (AFR)',
                'Bureau of Labor Statistics CPI-U (FRED CPIAUCNS)',
            ],
            'inflation_base_year': INFLATION_BASE_YEAR,
            'cpi_source': 'FRED CPIAUCNS - Consumer Price Index for All Urban Consumers, Not Seasonally Adjusted',
            'notes': 'All adjusted dollar amounts are in 2024 dollars. CCD F-33 data through FY 2020; KDE AFR per-pupil data for FY 2021-2024.',
        },
        'current_year': current,
        'by_grad_year': by_grad_year,
    }

    save_output(result, 'finance.json')
    populated = sum(1 for v in by_grad_year.values() if v['data_available'])
    kde_count = sum(1 for v in by_grad_year.values() if v.get('source') and 'KDE AFR' in (v.get('source') or ''))
    print(f"  {populated} grad years with data out of {len(by_grad_year)} ({kde_count} from KDE AFR)")
    return result


def _finance_source(has_finance, finance_source, has_seek):
    parts = []
    if has_finance:
        if finance_source == 'kde':
            parts.append('KDE Annual Financial Reports')
        else:
            parts.append('NCES CCD via Urban Institute')
    if has_seek:
        parts.append('KY LRC / KDE (SEEK)')
    return '; '.join(parts) if parts else None


# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------

def generate_enrollment(cpi_factors):
    print("\nGenerating enrollment.json...")
    enrollment_raw = load_json(os.path.join(UI_DIR, 'enrollment_by_year.json'))
    race_raw = load_json(os.path.join(UI_DIR, 'enrollment_by_race_year.json'))

    # KDE FRL data
    kde_frl_path = os.path.join(PROCESSED_DIR, 'kde_frl_statewide.json')
    kde_frl = {}
    if os.path.exists(kde_frl_path):
        kde_frl_raw = load_json(kde_frl_path)
        kde_frl = kde_frl_raw.get('by_school_year', {})
        print(f"  Loaded KDE FRL data: {len(kde_frl)} school years")

    by_grad_year = {}

    for grad_year in range(GRAD_YEAR_MIN, GRAD_YEAR_MAX + 1):
        ccd_year = grad_year_to_ccd_year(grad_year)
        ccd_str = str(ccd_year)
        sy = grad_year_to_school_year(grad_year)

        enr = enrollment_raw.get(ccd_str, {})
        race = race_raw.get(ccd_str, {}).get('enrollment_by_race', {})

        total = enr.get('total_enrollment')
        race_total = race.get('total', total)

        demographics = {
            'pct_white': safe_pct(race.get('white'), race_total),
            'pct_black': safe_pct(race.get('black'), race_total),
            'pct_hispanic': safe_pct(race.get('hispanic'), race_total),
            'pct_asian': safe_pct(race.get('asian'), race_total),
            'pct_two_or_more': safe_pct(race.get('two_or_more'), race_total),
            'pct_other': safe_pct(
                (race.get('aian', 0) or 0) + (race.get('nhpi', 0) or 0) + (race.get('unknown', 0) or 0) + (race.get('other', 0) or 0),
                race_total
            ) if race_total else None,
        }

        # FRL data from KDE
        frl_entry = kde_frl.get(sy, {})
        pct_frl = frl_entry.get('pct_free_reduced_lunch')

        has_data = total is not None

        sources = []
        if has_data:
            sources.append('NCES CCD via Urban Institute')
        if pct_frl is not None:
            sources.append('KDE Qualifying Data Report')

        entry = {
            'school_year': sy,
            'total_enrollment': total,
            'demographics': demographics,
            'pct_free_reduced_lunch': pct_frl,
            'pct_ell': None,                 # requires KDE SRC data
            'pct_disability': None,          # requires KDE SRC data
            'data_available': has_data or pct_frl is not None,
            'source': '; '.join(sources) if sources else None,
        }
        by_grad_year[str(grad_year)] = entry

    current = _find_most_recent(by_grad_year, 'total_enrollment')

    result = {
        'metadata': {
            'sources': [
                'NCES Common Core of Data via Urban Institute Education Data Portal',
                'Kentucky Department of Education School Report Card',
            ],
            'notes': 'Enrollment is fall membership count. Race categories changed in 2008 (Two or More Races added). FRL/ELL/disability data requires KDE SRC files.',
        },
        'current_year': current,
        'by_grad_year': by_grad_year,
    }

    save_output(result, 'enrollment.json')
    populated = sum(1 for v in by_grad_year.values() if v['data_available'])
    print(f"  {populated} grad years with data out of {len(by_grad_year)}")
    return result


# ---------------------------------------------------------------------------
# Teachers
# ---------------------------------------------------------------------------

def generate_teachers(cpi_factors):
    print("\nGenerating teachers.json...")
    directory_raw = load_json(os.path.join(UI_DIR, 'directory_by_year.json'))

    # KDE salary data (preferred source — direct from KY Dept of Education)
    kde_salary_path = os.path.join(PROCESSED_DIR, 'kde_salary_statewide.json')
    kde_salary = {}
    if os.path.exists(kde_salary_path):
        kde_raw = load_json(kde_salary_path)
        kde_salary = kde_raw.get('by_school_year', {})
        print(f"  Loaded KDE salary data: {len(kde_salary)} years")

    # NEA salary data as fallback: keyed by school year string like "2004-2005"
    nea_path = os.path.join(RAW_DIR, 'nea', 'ky_teacher_salary.csv')
    nea_salary = {}
    if os.path.exists(nea_path):
        with open(nea_path) as f:
            for row in csv.DictReader(f):
                sy = row.get('school_year', '').strip()
                sal = row.get('avg_salary', '').strip()
                if sy and sal:
                    try:
                        nea_salary[sy] = float(sal)
                    except ValueError:
                        pass

    by_grad_year = {}

    for grad_year in range(GRAD_YEAR_MIN, GRAD_YEAR_MAX + 1):
        ccd_year = grad_year_to_ccd_year(grad_year)
        ccd_str = str(ccd_year)
        sy = grad_year_to_school_year(grad_year)
        fy = grad_year_to_fiscal_year(grad_year)

        dir_data = directory_raw.get(ccd_str, {})
        teachers_fte = dir_data.get('total_teachers_fte')
        enrollment = dir_data.get('total_enrollment')
        ratio = dir_data.get('student_teacher_ratio')

        # Prefer KDE salary data over NEA
        salary_nominal = kde_salary.get(sy)
        salary_source = 'KDE'
        if salary_nominal is None:
            salary_nominal = nea_salary.get(sy)
            salary_source = 'NEA' if salary_nominal is not None else None
        if salary_nominal is not None:
            salary_nominal = int(salary_nominal)
        salary_adjusted = inflate_to_2024(salary_nominal, fy, cpi_factors)

        has_data = teachers_fte is not None or salary_nominal is not None

        sources = []
        if teachers_fte is not None:
            sources.append('NCES CCD via Urban Institute')
        if salary_source == 'KDE':
            sources.append('KDE Average Classroom Teacher Salaries')
        elif salary_source == 'NEA':
            sources.append('NEA Rankings & Estimates')

        entry = {
            'school_year': sy,
            'total_teachers_fte': teachers_fte,
            'student_teacher_ratio': ratio,
            'avg_salary_nominal': salary_nominal,
            'avg_salary': salary_adjusted,
            'data_available': has_data,
            'source': '; '.join(sources) if sources else None,
        }
        by_grad_year[str(grad_year)] = entry

    # Current year: prefer the entry with the most data (salary + FTE)
    current = _find_most_recent_teacher(by_grad_year)

    result = {
        'metadata': {
            'sources': [
                'NCES CCD Directory via Urban Institute Education Data Portal',
                'Kentucky Department of Education, Average Classroom Teacher Salaries',
                'NEA Rankings & Estimates (fallback for years without KDE data)',
            ],
            'inflation_base_year': INFLATION_BASE_YEAR,
            'notes': 'Teacher FTE from CCD directory. Salary from KDE (average of district-level average classroom teacher salaries), inflation-adjusted to 2024 dollars. NEA data used as fallback where KDE unavailable.',
        },
        'current_year': current,
        'by_grad_year': by_grad_year,
    }

    save_output(result, 'teachers.json')
    populated = sum(1 for v in by_grad_year.values() if v['data_available'])
    kde_count = sum(1 for v in by_grad_year.values() if v.get('source') and 'KDE' in v['source'])
    print(f"  {populated} grad years with data out of {len(by_grad_year)} ({kde_count} from KDE)")
    return result


def _find_most_recent_teacher(by_grad_year):
    """Find the best 'current year' for teachers — prioritize having both salary + FTE."""
    best = None
    for gy in range(GRAD_YEAR_MAX, GRAD_YEAR_MIN - 1, -1):
        entry = by_grad_year.get(str(gy), {})
        if entry.get('avg_salary') is not None and entry.get('total_teachers_fte') is not None:
            return entry
        if best is None and (entry.get('avg_salary') is not None or entry.get('total_teachers_fte') is not None):
            best = entry
    return best or by_grad_year.get(str(GRAD_YEAR_MAX), {})


# ---------------------------------------------------------------------------
# Assessment (stub — mostly requires manual KDE data)
# ---------------------------------------------------------------------------

def generate_assessment(cpi_factors):
    print("\nGenerating assessment.json...")

    # Load KDE assessment data if available
    kde_asmt_path = os.path.join(PROCESSED_DIR, 'kde_assessment.json')
    kde_asmt = load_json(kde_asmt_path) if os.path.exists(kde_asmt_path) else {}
    if kde_asmt:
        print(f"  Loaded KDE assessment data: {kde_asmt.get('school_year', 'unknown')}")

    by_grad_year = {}

    for grad_year in range(GRAD_YEAR_MIN, GRAD_YEAR_MAX + 1):
        sy = grad_year_to_school_year(grad_year)

        # Determine which assessment system was active
        if grad_year <= 1992:
            system = None
        elif grad_year <= 1999:
            system = 'KIRIS'
        elif grad_year <= 2012:
            system = 'CATS/KCCT'
        elif grad_year <= 2022:
            system = 'K-PREP'
        else:
            system = 'KSA'

        # ACT was required for all KY 11th graders 2008-2024
        act_era = 2008 <= grad_year <= 2024

        reading_pct = None
        math_pct = None
        act_avg = None
        source = None
        data_available = False

        # Check if we have KDE data for this grad year (currently only 2025 = SY 2024-2025)
        if kde_asmt and sy == kde_asmt.get('school_year'):
            ksa = kde_asmt.get('ksa', {})
            if ksa:
                reading_pct = ksa.get('reading_proficient_distinguished_pct')
                math_pct = ksa.get('math_proficient_distinguished_pct')
            act_avg = kde_asmt.get('act_composite_avg')
            if reading_pct is not None or math_pct is not None or act_avg is not None:
                data_available = True
                source = 'KDE School Report Card (KYRC25)'

        entry = {
            'school_year': sy,
            'assessment_system': system,
            'reading_proficient_distinguished_pct': reading_pct,
            'math_proficient_distinguished_pct': math_pct,
            'act_composite_avg': act_avg,
            'act_note': 'ACT required for all 11th graders' if act_era else (
                'ACT not required statewide' if grad_year < 2008 else 'Kentucky switched to SAT'
            ) if system else None,
            'naep_grade4_math': None,
            'naep_grade4_reading': None,
            'naep_grade8_math': None,
            'naep_grade8_reading': None,
            'data_available': data_available,
            'source': source,
        }
        by_grad_year[str(grad_year)] = entry

    # Build current_year from KDE data
    current_year = {
        'school_year': '2024-2025',
        'assessment_system': 'KSA',
        'reading_proficient_distinguished_pct': None,
        'math_proficient_distinguished_pct': None,
        'act_composite_avg': None,
        'data_available': False,
        'source': None,
    }
    if kde_asmt and kde_asmt.get('ksa'):
        ksa = kde_asmt['ksa']
        current_year['reading_proficient_distinguished_pct'] = ksa.get('reading_proficient_distinguished_pct')
        current_year['math_proficient_distinguished_pct'] = ksa.get('math_proficient_distinguished_pct')
        current_year['act_composite_avg'] = kde_asmt.get('act_composite_avg')
        current_year['data_available'] = True
        current_year['source'] = 'KDE School Report Card (KYRC25)'

    result = {
        'metadata': {
            'sources': [
                'Kentucky Department of Education School Report Card',
                'NAEP Data Explorer (National Center for Education Statistics)',
            ],
            'assessment_eras': {
                'KIRIS': {'years': '1992-1998', 'note': 'Kentucky Instructional Results Information System. Limited digital data available.'},
                'CATS_KCCT': {'years': '1999-2011', 'note': 'Commonwealth Accountability Testing System. Moderate data availability.'},
                'K-PREP': {'years': '2012-2021', 'note': 'Kentucky Performance Rating for Educational Progress. Full data from KDE SRC.'},
                'KSA': {'years': '2022-present', 'note': 'Kentucky Summative Assessment. Full data from KDE SRC.'},
            },
            'comparability_caveat': "Kentucky has changed its state test several times, so direct comparisons across eras aren't apples-to-apples. But the trends tell a story.",
            'notes': 'Assessment data requires manual download from KDE School Report Card historical datasets. ACT was required for all KY 11th graders from 2008-2024; Kentucky switched to SAT in 2025.',
        },
        'current_year': current_year,
        'by_grad_year': by_grad_year,
    }

    save_output(result, 'assessment.json')
    populated = sum(1 for v in by_grad_year.values() if v['data_available'])
    print(f"  {populated} grad years with assessment data" if populated else "  Assessment: current year populated, historical still needs manual KDE downloads")
    return result


# ---------------------------------------------------------------------------
# Districts
# ---------------------------------------------------------------------------

def generate_districts_json():
    """Generate the district lookup list for the dropdown."""
    print("\nGenerating districts.json...")
    raw_path = os.path.join(UI_DIR, 'district_list.json')
    raw = load_json(raw_path)

    if not raw:
        print("  No district list data found — skipping")
        save_output([], 'districts.json')
        return []

    # raw is a list of {leaid, name}
    districts = sorted(raw, key=lambda d: d.get('name', ''))
    save_output(districts, 'districts.json')
    print(f"  {len(districts)} districts")
    return districts


def generate_district_finance(cpi_factors):
    """Generate district-level finance data keyed by leaid and grad year."""
    print("\nGenerating district_finance.json...")
    raw_path = os.path.join(UI_DIR, 'district_finance_by_year.json')
    raw = load_json(raw_path)

    if not raw:
        print("  No district finance data found — skipping")
        save_output({'by_district': {}}, 'district_finance.json')
        return

    # Build a name lookup from the most common name per leaid
    name_lookup = {}
    for year_str, districts in raw.items():
        for d in districts:
            leaid = d.get('leaid')
            name = d.get('lea_name')
            if leaid and name:
                name_lookup[str(leaid)] = name.strip()

    # Also try the district list for canonical names
    list_path = os.path.join(UI_DIR, 'district_list.json')
    district_list = load_json(list_path)
    if district_list:
        for d in district_list:
            name_lookup[str(d['leaid'])] = d['name']

    # Build per-district, per-grad-year structure
    by_district = {}

    for year_str, districts in raw.items():
        fy = int(year_str)
        grad_year = fy  # fiscal year = graduation year
        sy = grad_year_to_school_year(grad_year)

        for d in districts:
            leaid = str(d.get('leaid', ''))
            if not leaid:
                continue

            exp_total = d.get('exp_total')
            enrollment = d.get('enrollment_fall_responsible')
            rev_total = d.get('rev_total')
            rev_local = d.get('rev_local_total')
            rev_state = d.get('rev_state_total')
            rev_fed = d.get('rev_fed_total')

            # Per-pupil
            pp_nominal = None
            if exp_total is not None and enrollment is not None and enrollment > 0:
                pp_nominal = round(exp_total / enrollment)

            pp_adjusted = inflate_to_2024(pp_nominal, fy, cpi_factors)

            # Revenue percentages
            rev_local_pct = None
            rev_state_pct = None
            rev_fed_pct = None
            if rev_total and rev_total > 0:
                if rev_local is not None:
                    rev_local_pct = round(rev_local / rev_total * 100, 1)
                if rev_state is not None:
                    rev_state_pct = round(rev_state / rev_total * 100, 1)
                if rev_fed is not None:
                    rev_fed_pct = round(rev_fed / rev_total * 100, 1)

            has_data = pp_nominal is not None

            if not has_data:
                continue

            if leaid not in by_district:
                by_district[leaid] = {
                    'name': name_lookup.get(leaid, f'District {leaid}'),
                    'by_grad_year': {},
                }

            by_district[leaid]['by_grad_year'][str(grad_year)] = {
                'school_year': sy,
                'fiscal_year': fy,
                'enrollment': enrollment,
                'per_pupil_total_nominal': pp_nominal,
                'per_pupil_total': pp_adjusted,
                'rev_local_pct': rev_local_pct,
                'rev_state_pct': rev_state_pct,
                'rev_fed_pct': rev_fed_pct,
                'data_available': True,
            }

    result = {'by_district': by_district}
    save_output(result, 'district_finance.json')
    district_count = len(by_district)
    year_count = sum(len(d['by_grad_year']) for d in by_district.values())
    print(f"  {district_count} districts, {year_count} total district-year records")
    return result


# ---------------------------------------------------------------------------
# Meta
# ---------------------------------------------------------------------------

def generate_meta(cpi_factors, finance, enrollment, teachers, assessment):
    print("\nGenerating meta.json...")

    data_availability = {}
    for grad_year in range(GRAD_YEAR_MIN, GRAD_YEAR_MAX + 1):
        gy_str = str(grad_year)
        fin_avail = finance['by_grad_year'].get(gy_str, {}).get('data_available', False)
        enr_avail = enrollment['by_grad_year'].get(gy_str, {}).get('data_available', False)
        tch_avail = teachers['by_grad_year'].get(gy_str, {}).get('data_available', False)
        asmt_avail = assessment['by_grad_year'].get(gy_str, {}).get('data_available', False)

        data_availability[gy_str] = {
            'finance': fin_avail,
            'enrollment': enr_avail,
            'teachers': tch_avail,
            'assessment': asmt_avail,
            'any_data': fin_avail or enr_avail or tch_avail or asmt_avail,
        }

    # Find earliest available year per category
    def earliest_year(category):
        for gy in range(GRAD_YEAR_MIN, GRAD_YEAR_MAX + 1):
            if data_availability.get(str(gy), {}).get(category, False):
                return gy
        return None

    # CPI factors for the relevant range only
    cpi_subset = {str(y): cpi_factors.get(y) for y in range(GRAD_YEAR_MIN, GRAD_YEAR_MAX + 1) if y in cpi_factors}

    result = {
        'project': 'When I Was in School',
        'organization': 'Kentucky Student Voice Team',
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'graduation_year_range': [GRAD_YEAR_MIN, GRAD_YEAR_MAX],
        'inflation_base_year': INFLATION_BASE_YEAR,
        'cpi_source': 'FRED CPIAUCNS - Consumer Price Index for All Urban Consumers, Not Seasonally Adjusted',
        'cpi_factors': cpi_subset,
        'earliest_available': {
            'finance': earliest_year('finance'),
            'enrollment': earliest_year('enrollment'),
            'teachers': earliest_year('teachers'),
            'assessment': earliest_year('assessment'),
        },
        'data_availability_by_grad_year': data_availability,
        'data_sources': {
            'finance': {
                'primary': 'NCES CCD F-33 via Urban Institute (1991-2020)',
                'secondary': 'KDE Annual Financial Reports (2001-2024)',
                'seek': 'KY Legislative Research Commission / KDE',
            },
            'enrollment': {
                'primary': 'NCES CCD via Urban Institute (1986-2023)',
                'secondary': 'KDE School Report Card (2012-2025)',
            },
            'teachers': {
                'primary': 'NCES CCD Directory via Urban Institute (1986-2023)',
                'salary': 'NEA Rankings & Estimates',
            },
            'assessment': {
                'primary': 'KDE School Report Card (2012-2025)',
                'secondary': 'NAEP Data Explorer (biennial, 1992-2024)',
            },
        },
        'assessment_eras': [
            {'name': 'KIRIS', 'start_grad_year': 1993, 'end_grad_year': 1999},
            {'name': 'CATS/KCCT', 'start_grad_year': 2000, 'end_grad_year': 2012},
            {'name': 'K-PREP', 'start_grad_year': 2013, 'end_grad_year': 2022},
            {'name': 'KSA', 'start_grad_year': 2023, 'end_grad_year': 2025},
        ],
    }

    save_output(result, 'meta.json')
    any_data_count = sum(1 for v in data_availability.values() if v['any_data'])
    print(f"  {any_data_count} grad years have at least some data")
    return result


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _find_most_recent(by_grad_year, key_field):
    """Find the most recent grad year entry that has a non-null value for key_field."""
    for gy in range(GRAD_YEAR_MAX, GRAD_YEAR_MIN - 1, -1):
        entry = by_grad_year.get(str(gy), {})
        if entry.get(key_field) is not None:
            return entry
    # Fallback to most recent entry
    return by_grad_year.get(str(GRAD_YEAR_MAX), {})


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("When I Was in School — Data Processing Pipeline")
    print("=" * 60)

    # Load CPI factors
    cpi_factors = load_cpi_factors()
    print(f"Loaded CPI adjustment factors for {len(cpi_factors)} years")

    finance = generate_finance(cpi_factors)
    enrollment = generate_enrollment(cpi_factors)
    teachers = generate_teachers(cpi_factors)
    assessment = generate_assessment(cpi_factors)
    generate_districts_json()
    generate_district_finance(cpi_factors)
    meta = generate_meta(cpi_factors, finance, enrollment, teachers, assessment)

    print("\n" + "=" * 60)
    print("Pipeline complete. Output files in data/output/:")
    for f in ['finance.json', 'enrollment.json', 'teachers.json', 'assessment.json', 'meta.json', 'districts.json', 'district_finance.json']:
        path = os.path.join(OUTPUT_DIR, f)
        size = os.path.getsize(path) if os.path.exists(path) else 0
        print(f"  {f}: {size:,} bytes")
    print("=" * 60)


if __name__ == '__main__':
    main()
