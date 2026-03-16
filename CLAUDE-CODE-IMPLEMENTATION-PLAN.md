# WHEN I WAS IN SCHOOL — Claude Code Implementation Plan

## What This Document Is

This is a step-by-step implementation plan for Claude Code to rebuild the "When I Was in School" website with a tighter, more focused model. The site is an advocacy tool for the Kentucky legislative session, built by the Kentucky Student Voice Team (KSVT). The original project brief (`WHEN-I-WAS-IN-SCHOOL-PROJECT-BRIEF.md`) contains full brand guidelines, tone guidance, and technical architecture — **read that first** for context. This plan describes **what has changed** and how to build the new version.

---

## The New Focus

The original brief covered funding, assessments, enrollment, demographics, and staffing. We're narrowing to a single, punchy comparison:

**How has compensation changed for the people who work in schools vs. the people who fund them?**

Three roles, side by side:
1. **Educators** (Kentucky public school teachers)
2. **School bus drivers**
3. **Kentucky state legislators**

For each role, show:
- **Percent change** in compensation from the user's graduation year to today (inflation-adjusted)
- **Effective hourly rate** based on expected annual work hours

Everything else from the original brief (assessment scores, enrollment, demographics, detailed finance breakdowns) is **shelved for now** — keep the data strategy notes in the original brief for potential reintroduction later.

---

## What Stays From the Original Brief

- All brand guidelines (colors, typography, tone, logo usage)
- The landing page flow (graduation year input → results)
- The tone arc (playful → serious → call to action)
- The missing-data fallback strategy (cheeky messages for old years)
- The static site architecture (HTML/CSS/JS, flat JSON data files)
- Social sharing with Open Graph meta tags
- The donate CTA linking to KSVT's fund
- The "no jargon, no fabrication" data philosophy

## What Changes

- Results page shows **only** the three compensation comparisons (educator, bus driver, lawmaker)
- Add **email collection** on the landing page alongside graduation year and district name
- Save collected emails/districts/years to a downloadable spreadsheet
- Reframe the narrative arc around the compensation gap as the central argument
- Add hourly rate breakdowns for all three roles

---

## New User Flow

### Landing Page

Same as original brief, with these additions:

**Input fields (in order):**
1. "What year did you graduate high school?" — dropdown, range 1970–2025
2. "What school district?" — searchable dropdown of all Kentucky school districts (173 districts)
3. "Your email (to stay connected)" — email input field

**Note on the district field:** District selection is primarily for contact-building purposes (the compensation data is statewide, not district-level). But having district info makes follow-up outreach much more targeted.

**CTA button:** "SHOW ME" (same as before)

**Privacy note:** Small text below the form: "We'll only use your email to share updates about Kentucky public education. We won't share it with anyone else."

### Results Page

#### Section A: The Hook (same as before)
"You graduated in [YEAR]. Here's what's changed for the people who keep Kentucky schools running — and the people who decide how much they get paid."

#### Section B: Educator Compensation
- **Average teacher salary THEN vs NOW** (inflation-adjusted to current dollars)
- **Percent change** displayed prominently (e.g., "+12%" or "-3%" in large text)
- **Effective hourly rate THEN vs NOW**
  - Based on: 187 contract days × 7.5 hours/day = 1,402.5 hours/year (standard KY teacher contract)
  - Note: Real hours worked are much higher (planning, grading, etc.) — mention this in small text
- Visual: simple side-by-side cards, THEN on left, NOW on right

#### Section C: Bus Driver Compensation
- **Average bus driver annual pay THEN vs NOW** (inflation-adjusted)
- **Percent change** displayed prominently
- **Effective hourly rate THEN vs NOW**
  - Based on: 180 school days × ~5 hours/day (split shift: morning + afternoon routes) = 900 hours/year
  - Acknowledge this is part-time work with no summer pay
- Visual: same card layout as educators

#### Section D: Lawmaker Compensation
- **Total annual compensation THEN vs NOW** (salary + per diem + expenses, inflation-adjusted)
  - KY legislators receive: base salary + per diem for session days + interim committee per diem
  - Session length: 60 days (even years) or 30 days (odd years), plus interim committee days
- **Percent change** displayed prominently
- **Effective hourly rate THEN vs NOW**
  - Based on: session days × 8 hours/day (use 60-day session year for consistency)
  - 60 days × 8 hours = 480 hours/year for session work
  - Note: Some legislators have interim committee work; this is the minimum
- Visual: same card layout

#### Section E: The Gap (replaces "The Shift")
- Side-by-side summary of all three percent changes and hourly rates
- Framing copy: "The people who teach your kids, drive them to school, and keep buildings running have seen their pay [rise/fall] by X%. The people who set the budget? They've seen theirs [rise/fall] by Y%."
- Bold stat: the hourly rate comparison rendered large
- Brief Rose v. Council mention (same as original brief — plant the seed, don't deep-dive)

#### Section F: Call to Action (same as original, plus)
- "Share your results" → social share
- "Support students fighting for adequate funding" → donate link
- "Contact your legislator" → link to https://apps.legislature.ky.gov/findyourlegislator/findyourlegislator.html (new addition — strong advocacy move)

---

## Data Requirements & Sources

### 1. Kentucky Teacher Salary (Historical)

**What we need:** Average teacher salary by year, statewide, going back to at least 1990.

**Where to find it:**
- **NEA Rankings & Estimates reports** (published annually): Historical average salary by state. These go back decades. Search for "NEA Rankings and Estimates" PDFs — they're published each year and many are archived online.
  - Recent: https://www.nea.org/resource-library/educator-pay-and-student-spending-how-does-your-state-rank
  - The 2025 report shows KY average teacher salary at $58,325 (ranking 42nd)
- **KDE School District Personnel Information**: https://www.education.ky.gov/districts/FinRept/Pages/School%20District%20Personnel%20Information.aspx — has salary data by district, can compute statewide averages
- **NCES Digest of Education Statistics**: Table 211.60 has estimated average annual salary of teachers in public schools by state, going back to 1969-70. https://nces.ed.gov/programs/digest/d23/tables/dt23_211.60.asp
  - **THIS IS THE SINGLE BEST SOURCE** — one table, all states, multiple decades, both nominal and constant dollars

**What's missing:**
- NCES Digest table may lag 1-2 years behind current year. Supplement with most recent NEA report or KDE data for the latest year.
- Inflation adjustment: NCES provides constant-dollar figures, but verify the base year matches our needs. May need to re-adjust using CPI-U.

### 2. Kentucky Bus Driver Compensation (Historical)

**What we need:** Average bus driver salary or hourly wage by year, statewide.

**Where to find it:**
- **Bureau of Labor Statistics (BLS) Occupational Employment and Wage Statistics (OEWS)**: https://www.bls.gov/oes/tables.htm — has annual mean wage for "Bus Drivers, School" (SOC 53-3051) by state. Available from ~1997 to present.
  - Query: https://data.bls.gov/oes/#/occGeo/One%20occupation%20for%20one%20geographical%20area
  - State: Kentucky, Occupation: 53-3051
- **KDE Transportation Data**: KDE tracks transportation expenditures and may have driver salary data in annual financial reports.
- **Salary.com / ZipRecruiter**: Current average is ~$18.29/hour or ~$36,870/year. Useful for "NOW" figure but not historical.

**What's missing:**
- Historical bus driver salary data before ~1997 is sparse. BLS OEWS data starts mid-1990s.
- For graduation years before 1997, we'll need to either: (a) use the earliest available year as the baseline, or (b) try to find data in archived KDE transportation reports.
- **CRITICAL GAP**: This is the hardest dataset to get historically. Plan for a fallback message for pre-1997 graduation years.

### 3. Kentucky Legislator Compensation (Historical)

**What we need:** Total annual compensation (salary + per diem) by year.

**Where to find it:**
- **National Conference of State Legislatures (NCSL)**: https://www.ncsl.org/about-state-legislatures/2025-legislator-compensation — current figures. NCSL has published these tables going back years; archived versions exist.
  - Current KY legislator salary: check NCSL table
  - Per diem rates: listed separately
- **Ballotpedia**: https://ballotpedia.org/Kentucky_state_government_salary — has current and some historical salary info
- **Kentucky Revised Statutes**: KRS 6.229 sets legislator compensation. Historical versions of the statute show changes over time.
  - LRC statutory database: https://apps.legislature.ky.gov/law/statutes/statute.aspx?id=45288
- **Kentucky Legislative Research Commission**: https://apps.legislature.ky.gov/Expenditures/default.aspx — actual expenditure data
- **Kentucky Transparency Portal**: https://transparency.ky.gov/search/Pages/SalarySearch.aspx — searchable salary data for state employees including legislators
- **Key news source for 2023 raise**: Kentucky Lantern reported legislators voted themselves an 8% raise while not funding teacher raises: https://kentuckylantern.com/2023/01/19/kentucky-legislators-get-pay-hike-after-voting-increase-for-themselves-but-not-for-teachers/

**What's missing:**
- A single clean historical table of total legislator compensation by year doesn't exist in one place. You'll need to reconstruct it from NCSL archives, LRC data, and statutory history.
- Per diem rates have changed over time and need to be tracked separately from base salary.
- **Action item for Claude Code**: Check the Wayback Machine for archived NCSL compensation tables (they update annually and old versions get replaced). Also check LRC publications for historical salary schedules.

### 4. Inflation Data (CPI-U)

**What we need:** Annual CPI-U values to adjust all dollar figures to current-year dollars.

**Where to find it:**
- **BLS CPI-U Annual Averages**: https://data.bls.gov/timeseries/CUUR0000SA0
- Already referenced in the original brief. This is straightforward.

### 5. Work Hours Assumptions

These are not data-sourced — they're reasonable estimates based on published contract standards:

| Role | Basis | Annual Hours |
|------|-------|-------------|
| Teacher | 187 contract days × 7.5 hrs/day | **1,402 hours** |
| Bus driver | 180 school days × 5 hrs/day (split shift) | **900 hours** |
| Legislator | 60 session days × 8 hrs/day (even-year session) | **480 hours** |

**Important notes to display on the site:**
- Teacher hours are contractual minimums. Most teachers work significantly more (NEA surveys suggest 50+ hours/week during the school year).
- Bus driver hours reflect route time only. Pre-trip inspections, training, and field trips add hours.
- Legislator hours reflect session days only. Interim committee work and constituent services add hours, but are not required.
- Cite the source for each assumption in small text.

---

## Email Collection & Data Storage

### How It Works

1. User enters graduation year, district, and email on the landing page
2. On form submission (before showing results), send the data to a backend endpoint
3. Store the data in a Google Sheet or a flat CSV file

### Implementation Options (in order of recommendation)

**Option A: Google Sheets via Google Apps Script (recommended for advocacy use)**
- Create a Google Sheet with columns: Timestamp, Email, District, Graduation Year
- Deploy a Google Apps Script as a web app that accepts POST requests and appends rows
- The script URL becomes your endpoint — call it from the site's JavaScript on form submit
- Pros: Free, no server needed, advocacy team can access the spreadsheet directly, easy to filter/sort for outreach
- Cons: Rate limits (but fine for this traffic level)

**Option B: Netlify/Vercel Serverless Function → CSV**
- Write a small serverless function that appends to a CSV file or sends to a storage service
- Pros: Keeps everything in the same hosting stack
- Cons: More setup, team needs technical access to retrieve the data

**Option C: Third-party form service (Formspree, Airtable, etc.)**
- Route form submissions to a third-party service
- Pros: Zero backend code
- Cons: Free tiers have limits, adds a dependency

### Data Format (Google Sheet)

| Timestamp | Email | District | Graduation Year |
|-----------|-------|----------|----------------|
| 2026-03-16 14:22 | parent@email.com | Fayette County | 2001 |
| 2026-03-16 14:25 | voter@email.com | Jefferson County | 1995 |

### Privacy & Compliance
- Display a clear privacy statement on the form
- Only collect what you need (email, district, year)
- Don't sell or share the data
- Include an unsubscribe mechanism in any follow-up emails (CAN-SPAM compliance)

---

## Legislative Advocacy Enhancements

Since this is a tool for the Kentucky legislative session, here are additions that would make it more effective:

### 1. "Contact Your Legislator" Button
- Link to the KY General Assembly's legislator finder: https://apps.legislature.ky.gov/findyourlegislator/findyourlegislator.html
- Place it prominently in the CTA section
- Frame it: "Think this should change? Tell your legislator."

### 2. Pre-Written Message Template
- After the results, offer a "Send a message to your legislator" option
- Provide a short, customizable template that includes the user's graduation year and the key stat (e.g., "Since I graduated in [YEAR], teacher pay in Kentucky has changed by [X]% while legislator pay has changed by [Y]%.")
- Even a simple copyable text block would be powerful

### 3. Session-Aware Messaging
- If the General Assembly is currently in session, add a banner: "The Kentucky General Assembly is in session RIGHT NOW. Your voice matters today."
- If not in session, adjust: "The next legislative session begins in January. Get informed now."
- This can be driven by a simple date check in JavaScript (session runs Jan–Mar/Apr)

### 4. Bill Tracker Reference
- If KSVT has specific bills they're tracking (education funding bills), add a "Bills to Watch" section or link
- Link to the bill text on the LRC site: https://apps.legislature.ky.gov/record/current-session/bill-search

### 5. Social Share Optimization for Advocacy
- The share card should include a provocative stat, not just the site name
- Suggested share text: "Since I graduated in [YEAR], Kentucky teacher pay changed by [X]% while lawmaker pay changed by [Y]%. See your numbers → [URL]"
- Make the share button copy this text to clipboard or open Twitter/Facebook with it pre-filled

### 6. District-Level Data Display (Future Enhancement)
- The district dropdown is collected for contact purposes now, but in a future version, show district-specific salary data alongside statewide averages
- KDE publishes district-level salary data that could power this

---

## Step-by-Step Build Instructions for Claude Code

### Phase 0: Setup
1. Read `WHEN-I-WAS-IN-SCHOOL-PROJECT-BRIEF.md` for full brand guidelines, tone, and technical architecture
2. Create the project directory structure (see original brief for file structure, adapted below)
3. Set up the static site skeleton: `index.html`, `css/styles.css`, `js/app.js`

### Phase 1: Data Collection
**Do these in order. Each step should produce a JSON file.**

1. **Teacher salary data** → `data/teacher-salary.json`
   - Go to NCES Digest of Education Statistics Table 211.60
   - Extract Kentucky average teacher salary for every available year
   - Include both nominal and inflation-adjusted (current-year dollars) figures
   - If NCES doesn't have the most recent year, supplement with the latest NEA Rankings & Estimates report
   - Schema: `{ "by_year": { "1990": { "nominal": 24300, "adjusted": 56800, "source": "NCES Digest Table 211.60" }, ... }, "hours_basis": 1402 }`

2. **Bus driver wage data** → `data/bus-driver.json`
   - Go to BLS OEWS data for SOC 53-3051 (Bus Drivers, School) in Kentucky
   - Extract annual mean wage for every available year (~1997–present)
   - Adjust for inflation using CPI-U
   - Schema: same structure as teacher salary, with `"hours_basis": 900`

3. **Legislator compensation data** → `data/legislator.json`
   - This requires multiple sources:
     a. Check NCSL legislator compensation tables (current and archived)
     b. Check Ballotpedia for historical KY legislator salary
     c. Check KRS 6.229 revision history for statutory salary changes
     d. Check Kentucky Transparency Portal for actual salary figures
   - Compile: base salary + estimated per diem (per diem rate × average session days)
   - Adjust for inflation
   - Schema: `{ "by_year": { "2005": { "base_salary": 22000, "per_diem_rate": 175, "session_days": 60, "total_estimated": 32500, "adjusted": 50200, "source": "NCSL / KRS 6.229" }, ... }, "hours_basis": 480 }`

4. **CPI-U data** → `data/cpi.json`
   - Download annual CPI-U averages from BLS
   - Use to verify/compute all inflation adjustments
   - Schema: `{ "by_year": { "1990": 130.7, "1991": 136.2, ... } }`

5. **Kentucky school districts list** → `data/districts.json`
   - Get the list of all 173 Kentucky school districts for the dropdown
   - Source: KDE district directory or NCES CCD
   - Schema: `["Adair County", "Allen County", ... , "Woodford County"]`

### Phase 2: Data Validation
1. Spot-check at least 5 data points per dataset against original sources
2. Verify inflation adjustments are correct (pick 3 years, manually compute, compare)
3. Ensure no null values for years that should have data
4. Document any gaps in a `data/gaps.md` file

### Phase 3: Build the Landing Page
1. Create `index.html` with:
   - KSVT branding (logo, colors, fonts per brand guidelines)
   - `WHEN I WAS IN SCHOOL` hero title in Oswald, all caps
   - Tagline (e.g., "A lot has changed since you walked the halls.")
   - Three input fields: graduation year dropdown, district searchable dropdown, email input
   - Privacy note below form
   - "SHOW ME" button (Gold background, Navy text)
2. Style with `css/styles.css` using KSVT brand palette
3. Load Google Fonts: Oswald, Plus Jakarta Sans, EB Garamond
4. Make it mobile-responsive from the start

### Phase 4: Build the Results Page
1. On form submit:
   - Validate inputs (year required, email format check, district optional but encouraged)
   - Send email + district + year to the collection endpoint (Phase 6)
   - Load data files and compute comparisons
2. Render Section A: The Hook
   - Personalized with graduation year
3. Render Section B: Educator Compensation
   - Show THEN salary, NOW salary (both inflation-adjusted)
   - Compute and display percent change (large, bold)
   - Compute and display hourly rate (salary ÷ 1,402 hours)
   - Small text noting contractual hours vs. real hours
4. Render Section C: Bus Driver Compensation
   - Same layout as educator
   - Hourly rate based on 900 hours/year
   - Note part-time nature of the work
5. Render Section D: Lawmaker Compensation
   - Show total compensation THEN vs NOW
   - Percent change
   - Hourly rate based on 480 hours/year
   - Note this is session work only
6. Render Section E: The Gap
   - Side-by-side summary of all three
   - Bold comparison framing
   - Rose v. Council mention
7. Render Section F: Call to Action
   - Share button with pre-filled text
   - Donate link
   - "Contact your legislator" link
   - Pre-written message template (copyable)
8. Handle missing data gracefully:
   - If graduation year has no data for a role, show earliest available year with explanation
   - Use the cheeky fallback messages from the original brief for very old years

### Phase 5: Social Sharing
1. Set up Open Graph meta tags (see original brief)
2. Implement share button that copies a pre-filled message:
   "Since I graduated in [YEAR], Kentucky teacher pay changed [X]% while lawmaker pay changed [Y]%. See your numbers → [URL]"
3. Include Twitter and Facebook share links with pre-filled text

### Phase 6: Email Collection Backend
1. Create a Google Sheet: "WIWIS Contacts" with columns: Timestamp, Email, District, Graduation Year
2. Write a Google Apps Script web app:
   ```
   function doPost(e) {
     var sheet = SpreadsheetApp.openById('SHEET_ID').getActiveSheet();
     var data = JSON.parse(e.postData.contents);
     sheet.appendRow([new Date(), data.email, data.district, data.year]);
     return ContentService.createTextOutput(JSON.stringify({status: 'ok'}))
       .setMimeType(ContentService.MimeType.JSON);
   }
   ```
3. Deploy as web app (execute as you, accessible to anyone)
4. In the site's JavaScript, POST to the script URL on form submit
5. Handle errors gracefully — don't block the user from seeing results if the email save fails

### Phase 7: Legislative Session Enhancements
1. Add session-aware banner (check current date against typical session dates)
2. Add "Contact Your Legislator" prominent button linking to KY legislator finder
3. Add copyable message template in the CTA section
4. If KSVT has specific bills to reference, add a "Bills to Watch" link

### Phase 8: Testing & QA
1. Test with graduation years: 1975, 1985, 1995, 2005, 2015, 2025
2. Verify all dollar amounts trace back to sources
3. Verify percent changes and hourly rates compute correctly
4. Test the email collection flow end-to-end
5. Test on mobile (responsive design)
6. Test social sharing (check OG preview with https://www.opengraph.xyz/)
7. Verify all external links work (donate, legislator finder, etc.)
8. Test the missing-data fallback messages

---

## Data Gaps Summary

| Dataset | Available From | Gap | Mitigation |
|---------|---------------|-----|------------|
| Teacher salary | ~1969 (NCES) | Most recent 1-2 years may lag | Supplement with NEA report |
| Bus driver wage | ~1997 (BLS) | Nothing before 1997 | Show earliest available, explain gap |
| Legislator comp | Scattered | No single historical table | Reconstruct from NCSL + KRS + LRC |
| CPI-U | 1913 | None | Full coverage |
| District list | Current | None | KDE has current list |

**Biggest risk:** Bus driver historical data is the thinnest. If BLS OEWS doesn't have clean Kentucky-specific data going back far enough, consider using national averages with a note, or focusing the bus driver comparison on recent decades only.

**Second biggest risk:** Legislator compensation requires assembly from multiple sources. Budget extra time for this data collection step.

---

## Adapted File Structure

```
/
├── index.html
├── css/
│   └── styles.css
├── js/
│   ├── app.js              # Main logic: inputs, data loading, rendering
│   ├── share.js             # Social sharing
│   └── collect.js           # Email/district/year collection
├── data/
│   ├── teacher-salary.json
│   ├── bus-driver.json
│   ├── legislator.json
│   ├── cpi.json
│   ├── districts.json
│   └── gaps.md              # Documentation of data gaps
├── assets/
│   ├── ksvt-logo.svg
│   └── share-card.png
└── README.md
```

---

## Shelved for Later (from original brief)

These sections are removed from v1 but may be reintroduced:
- Per-pupil spending / SEEK base guarantee comparisons
- Assessment score comparisons (KIRIS/CATS/K-PREP/KSA)
- Enrollment and demographic trends
- Student-to-teacher ratios
- ELL / disability / free-reduced lunch percentages
- Detailed budget line items (transportation, facilities, instructional materials)

The data strategy and sources for these are preserved in the original project brief.
