"""Extract state-level assessment data from KDE School Report Card files.

Reads: data/raw/kde_assessment/KYRC25_*.csv
Produces: data/processed/kde_assessment.json
"""

import csv
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw', 'kde_assessment')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')


def extract_summative_assessment():
    """Extract state-level proficiency from KSA summative assessment."""
    path = os.path.join(RAW_DIR, 'KYRC25_ACCT_Kentucky_Summative_Assessment.csv')
    if not os.path.exists(path):
        return None

    # State-level = District Number "999", Demographic "All Students"
    reading_scores = []
    math_scores = []

    with open(path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dist = row.get('District Number', '').strip()
            demo = row.get('Demographic', '').strip()
            suppressed = row.get('Suppressed', '').strip()

            if dist != '999' or demo != 'All Students' or suppressed == 'Y':
                continue

            subject = row.get('Subject', '').strip()
            level = row.get('Level', '').strip()
            prof_dist = row.get('Proficient / Distinguished', '').strip()

            if not prof_dist:
                continue

            try:
                pct = float(prof_dist)
            except ValueError:
                continue

            if subject == 'Reading' and level in ('Elementary School', 'Middle School', 'High School'):
                reading_scores.append(pct)
            elif subject == 'Mathematics' and level in ('Elementary School', 'Middle School', 'High School'):
                math_scores.append(pct)

    reading_avg = round(sum(reading_scores) / len(reading_scores), 1) if reading_scores else None
    math_avg = round(sum(math_scores) / len(math_scores), 1) if math_scores else None

    return {
        'reading_proficient_distinguished_pct': reading_avg,
        'math_proficient_distinguished_pct': math_avg,
        'reading_by_level': {
            'elementary': reading_scores[0] if len(reading_scores) > 0 else None,
            'middle': reading_scores[1] if len(reading_scores) > 1 else None,
            'high': reading_scores[2] if len(reading_scores) > 2 else None,
        } if reading_scores else None,
        'math_by_level': {
            'elementary': math_scores[0] if len(math_scores) > 0 else None,
            'middle': math_scores[1] if len(math_scores) > 1 else None,
            'high': math_scores[2] if len(math_scores) > 2 else None,
        } if math_scores else None,
    }


def extract_act():
    """Extract state-level ACT composite from KDE data."""
    path = os.path.join(RAW_DIR, 'KYRC25_ASMT_The_ACT.csv')
    if not os.path.exists(path):
        return None

    with open(path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dist = row.get('District Number', '').strip()
            demo = row.get('Demographic', '').strip()

            if dist != '999' or demo != 'All Students':
                continue

            composite = row.get('Composite Score', '').strip()
            if composite:
                try:
                    return round(float(composite), 1)
                except ValueError:
                    pass
    return None


def main():
    print("Processing KDE assessment data...")
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    ksa = extract_summative_assessment()
    act = extract_act()

    if ksa:
        print(f"  KSA Reading (avg): {ksa['reading_proficient_distinguished_pct']}%")
        print(f"  KSA Math (avg): {ksa['math_proficient_distinguished_pct']}%")
        if ksa.get('reading_by_level'):
            print(f"    Reading by level: {ksa['reading_by_level']}")
        if ksa.get('math_by_level'):
            print(f"    Math by level: {ksa['math_by_level']}")
    else:
        print("  No KSA data found")

    if act:
        print(f"  ACT Composite: {act}")
    else:
        print("  No ACT data found")

    result = {
        'source': 'KDE School Report Card (KYRC25, SY 2024-2025)',
        'school_year': '2024-2025',
        'assessment_system': 'KSA',
        'ksa': ksa,
        'act_composite_avg': act,
    }

    out_path = os.path.join(PROCESSED_DIR, 'kde_assessment.json')
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"  Wrote {out_path}")


if __name__ == '__main__':
    main()
