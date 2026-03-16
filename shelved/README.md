# Shelved Data & Code — When I Was in School

This directory contains references to all the data processing code and output files that were built for the **original v1 site concept** (enrollment, finance, assessment, demographics, staffing) but are **not used in the current compensation-focused site**.

All of this code is **fully functional** and can be reintroduced by loading the output JSON files in `js/app.js` and adding corresponding render sections to `index.html`.

---

## Processing Scripts (in `/scripts/`)

| Script | What it does | Output |
|--------|-------------|--------|
| `process_all.py` | **Master pipeline** — generates all shelved output JSONs. Run this to regenerate everything. | `data/output/*.json` |
| `process_kde_assessment.py` | Extracts KSA Reading/Math proficiency + ACT composite from KYRC25 CSV files | `data/processed/kde_assessment.json` |
| `process_kde_finance.py` | Extracts per-pupil spending from KDE Annual Financial Report XLSX files (FY 2021+) | `data/processed/kde_finance_statewide.json` |
| `process_kde_salary.py` | Extracts statewide avg teacher salary from KDE district salary XLSX files | `data/processed/kde_salary_statewide.json` |
| `process_kde_frl.py` | Extracts statewide FRL % from KDE Qualifying Data XLSX files (SY 2021-2026) | `data/processed/kde_frl_statewide.json` |
| `build_district_salary.py` | Builds district-level teacher salary comparisons mapped to LEAIDs | `data/output/district_salary.json` |
| `fetch_cpi.py` | Fetches CPI-U annual averages from FRED API | `data/processed/cpi_adjustment_factors.json` |
| `fetch_urban_institute.py` | Fetches enrollment, finance, directory data from Urban Institute API | `data/raw/urban_institute/*.json` |
| `utils.py` | Shared utilities (CPI loading, inflation adjustment, year mapping) | — |

---

## Output JSON Files (in `/data/output/`)

### Currently Used by Site
| File | Description |
|------|-------------|
| `teacher-salary.json` | Teacher salary with hourly rate (1990-2025) |
| `bus-driver.json` | Bus driver wages from BLS OEWS (1997-2024) |
| `legislator.json` | KY legislator compensation from NCSL (1970-2025) |
| `districts.json` | District dropdown list (177 districts) |

### Shelved (fully generated, not loaded by site)
| File | Description | Data Coverage |
|------|-------------|---------------|
| `finance.json` | Per-pupil spending + SEEK base guarantee by grad year | 1992-2024 (35 years) |
| `enrollment.json` | Total enrollment + racial demographics + FRL % | 1987-2025 (39 years, FRL: 2022-2025) |
| `teachers.json` | Teacher FTE + salary by grad year | 1988-2025 (38 years) |
| `assessment.json` | Assessment system metadata + KSA/ACT scores | 2025 only (historical needs manual KDE data) |
| `district_finance.json` | Per-pupil spending by district and grad year | 176 districts, 4888 records |
| `district_salary.json` | District-level teacher salary comparisons | 176 districts |
| `meta.json` | Data availability map, sources, CPI factors | All years |
| `governors.json` | Governor by graduation year | 1987-2026 |

---

## Raw Data Files (in `/data/raw/`)

| Directory | Contents | File Count |
|-----------|----------|------------|
| `kde_salary/` | District avg classroom teacher salaries (1989-2026) | 5 XLSX |
| `kde_finance/` | Annual Financial Reports — Fund Balance + Receipts/Expenditures | 57 XLSX |
| `kde_assessment/` | KYRC24/25 School Report Card CSVs | 20 CSV |
| `kde_frl/` | FinalQualifyingData (2021-2026) | 5 XLSX |
| `kde_accountability/` | KDE accountability files | 58 files |
| `kde_personnel/` | KDE personnel files | 7 files |
| `nces/` | NCES state-level FRL table | 1 XLSX |
| `urban_institute/` | CCD data fetched from Urban Institute API | JSON files |
| `seek/` | SEEK base guarantee CSV | 1 CSV |

---

## How to Reintroduce

### Quick: Add a section to the current site
1. In `js/app.js`, add a `fetch()` call for the relevant JSON file (e.g., `data/output/enrollment.json`)
2. Write a `renderEnrollment(data, gradYear)` function following the pattern of `renderEducator()`
3. Add a `<section id="enrollment">` in `index.html`
4. Add corresponding CSS in `css/styles.css`

### Full: Restore the original multi-section site
1. The original site code is in git history (pre-rebuild commit)
2. All output JSON files are current and ready to use
3. Run `python3 scripts/process_all.py` to regenerate if needed

### Regenerate all data from scratch
```bash
# 1. Fetch latest CPI data
python3 scripts/fetch_cpi.py

# 2. Fetch latest Urban Institute data
python3 scripts/fetch_urban_institute.py

# 3. Process KDE raw files
python3 scripts/process_kde_salary.py
python3 scripts/process_kde_assessment.py
python3 scripts/process_kde_finance.py
python3 scripts/process_kde_frl.py

# 4. Run master pipeline (reads all processed data, generates output JSONs)
python3 scripts/process_all.py

# 5. Build compensation data (for current site)
python3 scripts/build_compensation_data.py
```

---

## Known Gaps Still Remaining

| Gap | What's Needed | Difficulty |
|-----|---------------|------------|
| **Assessment history** | Historical KDE SRC downloads (KIRIS/CATS/K-PREP data) — KDE blocks automated scraping | High — manual downloads + new processing code |
| **ELL / disability %** | KDE SRC special populations data | Medium — similar to FRL processing |
| **Pre-2021 KDE finance** | The Fund Balance XLSX files (2003-2019) have different sheet layout than Revenues & Expenditures | Medium — extend `process_kde_finance.py` |
| **NAEP scores** | NAEP Data Explorer exports for KY (grades 4, 8 — reading, math) | Low — straightforward CSV processing |
