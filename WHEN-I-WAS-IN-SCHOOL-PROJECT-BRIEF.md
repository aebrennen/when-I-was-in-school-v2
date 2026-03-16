# WHEN I WAS IN SCHOOL — Project Brief

## Project Overview

**Name:** When I Was in School
**Sub-brand of:** Kentucky Student Voice Team (KSVT)
**Sub-brand format:** `KSVT | WHEN I WAS IN SCHOOL` (Oswald, all caps, 2% tracking)
**Concept:** A personalized, data-driven web tool that challenges the assumption "I went to school, so I know what school is like." Users enter their high school graduation year and are shown a scrollable, single-page experience comparing **compensation for the people who keep Kentucky schools running** (teachers and bus drivers) **vs. the people who fund them** (state legislators) — from their graduation year to today.
**Undercurrent:** The legacy of *Rose v. Council for Better Education* (1989) and the Kentucky Education Reform Act (KERA, 1990). This is not prominently branded but informs the data narrative — showing what has changed (and what hasn't) since the landmark ruling that declared Kentucky's school system unconstitutional.
**Donate link:** https://bgcf.givingfuel.com/kentucky-student-voice-team-fund
**Primary audience:** Kentucky voters who are not education professionals
**Goal:** Collect contacts (email + district) for advocacy outreach, share results on social media, donate to support KSVT's lawsuit, contact legislators

---

## Brand Guidelines

### Colors (use KSVT brand palette)
| Name    | Hex       | RGB            | Use                          |
|---------|-----------|----------------|------------------------------|
| Gold    | `#FCB415` | 252, 180, 21   | Accent, highlights, CTAs     |
| Navy    | `#202C59` | 32, 44, 89     | Primary background, text     |
| Blue    | `#363AE8` | 54, 58, 232    | Interactive elements, links  |
| Pink    | `#F9CBCC` | 249, 203, 204  | Soft accents, "then" era     |
| Orange  | `#E25C05` | 226, 92, 5     | Emphasis, alerts             |

### Approved color combinations (high contrast only for body text)
- Navy on Gold, Gold on Navy
- White on Navy, White on Blue
- Navy on Pink, Navy on White
- Orange on White, White on Orange

### Typography
| Role              | Font              | Weight/Style           | Notes                                    |
|-------------------|-------------------|------------------------|------------------------------------------|
| Display/Headlines | **Oswald**        | All caps, Bold/SemiBold | Free Google Font stand-in for Heading Now |
| Body text         | **Plus Jakarta Sans** | Regular, Medium    | Google Font. Optimized for legibility     |
| Editorial accent  | **EB Garamond**   | Regular, SemiBold      | Google Font. Use sparingly for quotes     |

### Logo
- Use KSVT megaphone icon logo (circle mark) in the header
- Logotype switches between white and navy depending on background
- Never place logo on non-approved background colors

### Tone & Voice
- **Opening sections:** Playful, nostalgic, warm. "Remember when...?" energy.
- **Middle sections:** Increasingly factual, data-forward. Let the numbers do the talking.
- **Final section:** Serious. Direct. This is about kids today and what you can do.
- **Throughout:** Accessible to non-education audiences. No jargon. Plain language.
- Never condescending. The goal is to bridge a knowledge gap, not shame anyone.

---

## User Flow

### Step 1: Landing Page
- Hero with `WHEN I WAS IN SCHOOL` title in Oswald
- KSVT icon logo in top corner
- Brief tagline: something like "A lot has changed since you walked the halls. Let's find out how much."
- **Input fields (in order):**
  1. "What year did you graduate high school?" — dropdown, range: 1970-2025
  2. "What school district?" — searchable dropdown of all 173 Kentucky school districts
  3. "Your email (to stay connected)" — email input field
- **Privacy note:** Small text below the form: "We'll only use your email to share updates about Kentucky public education. We won't share it with anyone else."
- Big CTA button: "SHOW ME" (Gold #FCB415, navy text)
- Below the fold: brief explainer text about why this matters (2-3 sentences max)

**Note on the district field:** District selection is primarily for contact-building purposes (the compensation data is statewide, not district-level). But having district info makes follow-up outreach much more targeted.

### Step 2: Results Page (single scrollable page, section-by-section reveal)

The page should feel like a story unfolding. Each section is a "card" or full-width block that contrasts THEN vs NOW.

**Section order:**

#### A. The Hook (nostalgia)
- "You graduated in [YEAR]. Here's what's changed for the people who keep Kentucky schools running — and the people who decide how much they get paid."
- Subtle visual element: the year rendered large in the background, faded

#### B. Educator Compensation
- **Average teacher salary THEN vs NOW** (inflation-adjusted to current dollars)
- **Percent change** displayed prominently (e.g., "+12%" or "-3%" in large text)
- **Effective hourly rate THEN vs NOW**
  - Based on: 187 contract days x 7.5 hours/day = 1,402.5 hours/year (standard KY teacher contract)
  - Note: Real hours worked are much higher (planning, grading, etc.) — mention this in small text
- Visual: simple side-by-side cards, THEN on left, NOW on right

#### C. Bus Driver Compensation
- **Average bus driver annual pay THEN vs NOW** (inflation-adjusted)
- **Percent change** displayed prominently
- **Effective hourly rate THEN vs NOW**
  - Based on: 180 school days x ~5 hours/day (split shift: morning + afternoon routes) = 900 hours/year
  - Acknowledge this is part-time work with no summer pay
- Visual: same card layout as educators

#### D. Lawmaker Compensation
- **Total annual compensation THEN vs NOW** (salary + per diem + expenses, inflation-adjusted)
  - KY legislators receive: base salary + per diem for session days + interim committee per diem
  - Session length: 60 days (even years) or 30 days (odd years), plus interim committee days
- **Percent change** displayed prominently
- **Effective hourly rate THEN vs NOW**
  - Based on: 60 session days x 8 hours/day = 480 hours/year
  - Note: Some legislators have interim committee work; this is the minimum
- Visual: same card layout

#### E. The Gap (serious turn)
- Side-by-side summary of all three percent changes and hourly rates
- Framing copy: "The people who teach your kids, drive them to school, and keep buildings running have seen their pay [rise/fall] by X%. The people who set the budget? They've seen theirs [rise/fall] by Y%."
- Bold stat: the hourly rate comparison rendered large
- Brief mention: "In 1989, the Kentucky Supreme Court declared the entire system of public schools unconstitutional. The reforms that followed changed everything. But the fight for adequate funding isn't over."
- **Do not** deep-dive on Rose v. Council — just plant the seed

#### F. Call to Action
- "Share your results" button → social share with pre-filled text including key stats
- "Support students fighting for adequate funding" → links to https://bgcf.givingfuel.com/kentucky-student-voice-team-fund
- "Contact your legislator" → links to https://apps.legislature.ky.gov/findyourlegislator/findyourlegislator.html
- Pre-written copyable message template: "Since I graduated in [YEAR], teacher pay in Kentucky has changed by [X]% while legislator pay has changed by [Y]%."
- KSVT secondary logo at bottom

---

## Data Strategy

### Philosophy
Every number shown must be real, sourced, and accurate. No estimates, no fabrications, no interpolation. If data doesn't exist for a year, say so — don't fake it. All dollar amounts adjusted for inflation using BLS CPI data, displayed in current-year dollars.

### Data Sources

#### 1. Kentucky Teacher Salary (Historical) — MOST IMPORTANT
| Data Point | Source | Years Available | Notes |
|---|---|---|---|
| Average teacher salary by state | NCES Digest of Education Statistics, Table 211.60 | ~1969-present | **SINGLE BEST SOURCE** — one table, all states, multiple decades |
| Average teacher salary (recent) | NEA Rankings & Estimates | Current year | Supplement NCES for most recent year |
| District-level salary | KDE School District Personnel Information | ~1989-2026 | Can compute statewide averages from district data |

#### 2. Kentucky Bus Driver Compensation (Historical)
| Data Point | Source | Years Available | Notes |
|---|---|---|---|
| Annual mean wage, Bus Drivers School (SOC 53-3051) | BLS Occupational Employment & Wage Statistics (OEWS) | ~1997-present | State-level data for Kentucky |
| Current average | Salary.com / ZipRecruiter | Current | ~$18.29/hr or ~$36,870/yr — use for validation only |

**Known gap:** No historical bus driver salary data before ~1997. For pre-1997 graduation years, show earliest available year with explanation.

#### 3. Kentucky Legislator Compensation (Historical)
| Data Point | Source | Years Available | Notes |
|---|---|---|---|
| Current legislator salary + per diem | NCSL Legislator Compensation tables | Current + archived | https://www.ncsl.org/about-state-legislatures/2025-legislator-compensation |
| Historical salary | Ballotpedia | Some historical | https://ballotpedia.org/Kentucky_state_government_salary |
| Statutory salary | KRS 6.229 | Historical via revision history | https://apps.legislature.ky.gov/law/statutes/statute.aspx?id=45288 |
| Actual expenditures | KY LRC | Available | https://apps.legislature.ky.gov/Expenditures/default.aspx |
| Salary search | Kentucky Transparency Portal | Available | https://transparency.ky.gov/search/Pages/SalarySearch.aspx |

**Known gap:** No single clean historical table exists. Must reconstruct from multiple sources.

#### 4. CPI-U Inflation Data
| Data Point | Source | Years Available | Notes |
|---|---|---|---|
| CPI-U Annual Averages | Bureau of Labor Statistics | 1913-present | Already in pipeline (FRED CPIAUCNS) |

### Work Hours Assumptions

| Role | Basis | Annual Hours |
|------|-------|-------------|
| Teacher | 187 contract days x 7.5 hrs/day | **1,402 hours** |
| Bus driver | 180 school days x 5 hrs/day (split shift) | **900 hours** |
| Legislator | 60 session days x 8 hrs/day (even-year session) | **480 hours** |

**Important notes to display on the site:**
- Teacher hours are contractual minimums. Most teachers work significantly more (NEA surveys suggest 50+ hours/week during the school year).
- Bus driver hours reflect route time only. Pre-trip inspections, training, and field trips add hours.
- Legislator hours reflect session days only. Interim committee work and constituent services add hours, but are not required.

### Missing Data Strategy

**For graduation years where data exists:** Show it. Cite it subtly (small "Source: NCES" or "Source: BLS" below each data card).

**For graduation years where SOME data exists:** Show what you have. For missing roles, display: "This data wasn't tracked yet when you were in school." in a muted, smaller font.

**For graduation years where NO data exists (roughly pre-1990):** Show the cheeky fallback:
- Heading: "Well, you've got us there."
- Body: "Kentucky didn't start tracking this data until [earliest available year]. But here's what we do know..."
- Then show the earliest available data as the "THEN" comparison point

**For very old graduation years (pre-1970 — below dropdown range):** Not applicable; dropdown limited to 1970-2025.

---

## Technical Architecture

### Stack
- **Static site**: HTML/CSS/JS (vanilla)
- **Backend for email collection**: Google Apps Script → Google Sheet (recommended) or Netlify/Vercel serverless function
- **Hosting**: Netlify, Vercel, or GitHub Pages (all free tier)
- **Data format**: JSON files organized by year, loaded client-side
- **Inflation adjustment**: Pre-computed in the data files using CPI-U, not calculated at runtime

### File Structure
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

### Email Collection

1. User enters graduation year, district, and email on the landing page
2. On form submission (before showing results), POST data to a Google Apps Script endpoint
3. Data stored in a Google Sheet: Timestamp, Email, District, Graduation Year
4. Handle errors gracefully — don't block the user from seeing results if the email save fails
5. Display privacy note on the form

---

## Social Sharing

### Open Graph meta tags
```html
<meta property="og:title" content="When I Was in School | KSVT" />
<meta property="og:description" content="A lot has changed since you walked the halls. Find out how compensation has changed for Kentucky's teachers, bus drivers, and lawmakers." />
<meta property="og:image" content="/assets/share-card.png" />
<meta property="og:url" content="https://wheniwsinschool.org" />
<meta property="twitter:card" content="summary_large_image" />
```

### Share text (pre-filled)
"Since I graduated in [YEAR], Kentucky teacher pay changed [X]% while lawmaker pay changed [Y]%. See your numbers → [URL]"

### Share card design (static image, 1200x630px)
- Navy (#202C59) background
- "WHEN I WAS IN SCHOOL" in Oswald, gold (#FCB415), centered
- Subtext in Plus Jakarta Sans, white: "How much has changed since you graduated?"
- KSVT icon logo in corner
- URL at bottom in small white text

---

## Legislative Advocacy Enhancements

### 1. "Contact Your Legislator" Button
- Link to: https://apps.legislature.ky.gov/findyourlegislator/findyourlegislator.html
- Frame it: "Think this should change? Tell your legislator."

### 2. Pre-Written Message Template
- Provide a short, customizable template with the user's graduation year and key stats
- Copyable text block in the CTA section

### 3. Session-Aware Messaging
- If the General Assembly is in session (Jan-Mar/Apr), show: "The Kentucky General Assembly is in session RIGHT NOW. Your voice matters today."
- If not in session: "The next legislative session begins in January. Get informed now."
- Driven by date check in JavaScript

### 4. Social Share Optimization
- Share button copies pre-filled text with key stats
- Include Twitter and Facebook share links

---

## Shelved for Later (from original v1 concept)

These sections are removed from the current build but may be reintroduced in a future version. Data strategy and sources are preserved below for reference.

- Per-pupil spending / SEEK base guarantee comparisons
- Assessment score comparisons (KIRIS/CATS/K-PREP/KSA)
- Enrollment and demographic trends
- Student-to-teacher ratios
- ELL / disability / free-reduced lunch percentages
- Detailed budget line items (transportation, facilities, instructional materials)
- District-level data display (district dropdown currently collected for contact purposes only)
- Governor card in hook section

### Preserved Data Sources (for future reintroduction)

#### School Finance
| Data Point | Source | Years Available |
|---|---|---|
| Per-pupil expenditure | KDE Annual Financial Reports | ~2001-2024 |
| Revenue & expenditure by category | KDE Fund Balances & Revenues | 2014-2024 |
| SEEK base guarantee per pupil | KY Legislative Research Commission | 1990-present |
| Historical per-pupil funding | NCES CCD F-33 via Urban Institute | 1991-2020 |

#### Assessment Scores
| Data Point | Source | Years Available |
|---|---|---|
| K-PREP / KSA proficiency rates | KDE School Report Card datasets | 2012-present |
| CATS/KCCT proficiency rates | KDE archived reports | 1999-2011 |
| ACT composite scores | KDE / ACT Inc | 2008-present |

#### Enrollment & Demographics
| Data Point | Source | Years Available |
|---|---|---|
| Total enrollment, demographics | NCES CCD via Urban Institute | 1986-present |
| FRL, ELL, disability | KDE SRC + CRDC | 2012-present |

#### Teacher/Staffing Data
| Data Point | Source | Years Available |
|---|---|---|
| Teacher count, student-teacher ratio | NCES CCD | ~1990-present |
| Average teacher salary | KDE / NEA Rankings & Estimates | ~1989-present |

---

## v2 Roadmap (not for current build)

- District-level compensation comparison (teacher salary by district)
- Reintroduce shelved data sections (funding, assessment, enrollment, demographics)
- Dynamic personalized social share images
- Visitor counter ("X Kentuckians have looked back")
- News time capsule (historical headlines)
- Multi-screen storytelling with scroll-triggered animations
- Integration as subdomain of ksvt.org
- Teacher-specific view (for educators)
- Embeddable widget version for partner sites
- Bill tracker reference (education funding bills)

---

## Key Reminders for the Builder

1. **Accuracy is non-negotiable.** Every number must trace to a real source. If you can't verify it, don't show it.
2. **All dollar amounts in current-year dollars.** Always inflation-adjusted. Always.
3. **The tone is playful → serious.** Don't start serious. Don't end playful.
4. **This is for normal people.** No education jargon. No acronyms without explanation. Write like you're explaining to a smart friend who doesn't work in schools.
5. **Citations should be subtle.** Small text, muted color, below the data point. Not footnotes. Not a bibliography wall.
6. **The KSVT brand is bold and energetic.** Use the gold and navy. Make it feel alive, not like a government report.
7. **Heading Now is the ideal display font but it's paid.** Use Oswald (Google Fonts) as the approved stand-in, always in ALL CAPS.
8. **Test the cheeky fallback.** Enter graduation year 1975. Make sure it's charming, not broken.
9. **The compensation gap is the central argument.** Teachers and bus drivers vs. legislators. Let the numbers speak.
10. **Email collection is an advocacy tool.** Make it easy, not pushy. Don't block results if the save fails.
