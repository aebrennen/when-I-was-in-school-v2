# WHEN I WAS IN SCHOOL — V2 Implementation Brief

**Date:** 2026-03-16
**Purpose:** Prioritized implementation plan for Claude Code. Transforms the site from a three-role salary comparison into a teacher-focused advocacy tool designed for sharing and virality.

**Reference:** Read `CURRENT-STATE.md` for full technical details of the existing build.

---

## Design Philosophy

The site should feel like a punch in the gut, then hand you a megaphone. Every section exists to make one point land harder: **Kentucky teachers are losing ground, and the people in charge aren't fixing it.** Every design decision should optimize for screenshottability — assume the user will take a screenshot of whatever section they're looking at and text it to someone.

---

## New Page Structure (in scroll order)

### 1. Session Banner (keep as-is)
No changes. Orange bar, legislative session awareness.

### 2. Landing Page (simplify)
- **Remove district dropdown.** District selection was only for email collection context, not data. It adds friction. Keep: graduation year dropdown + optional email.
- **Keep:** KSVT logo, "WHEN I WAS IN SCHOOL" title, tagline, privacy note, "SHOW ME" button.
- If district-level data gets added later (see Phase 2 backlog), re-add district as a second step after results load.

### 3. Hero Stat (NEW — most important section)
**This is the screenshot.** One giant number, above the fold on every device.

```
Layout:
┌─────────────────────────────────────┐
│         YOU GRADUATED IN 2005.      │  (Oswald, white)
│                                     │
│              -17%                   │  (Giant, 120px+, gold if positive, orange if negative)
│                                     │
│   That's how much Kentucky teacher  │  (EB Garamond italic, white)
│   pay has fallen since you walked   │
│   the halls.                        │
│                                     │
│   In [YEAR], a Kentucky teacher     │  (smaller body text)
│   earned $64,891 (in today's        │
│   dollars). Today: $53,947.         │
│                                     │
│   Background: Navy                  │
└─────────────────────────────────────┘
```

- Merge the old "Hook Section" and "Educator Pay Section" hero stat into one.
- The percent change number should animate from 0 on load (count-up/count-down effect, ~1.5s, use CSS or lightweight JS — no libraries).
- For years with positive change, use green and adjust copy: "That's how much Kentucky teacher pay has grown..."
- For years with no teacher data (pre-1990), show: "We don't have salary data from back then — but here's what we do know about what's happened since."

### 4. Then vs. Now Detail Cards (REVISED)
**Desktop (>768px):** Two-column layout. Percent change hero on the left (sticky or fixed within section), THEN/NOW comparison cards on the right.
**Mobile:** Stack vertically — percent change on top, cards below.

Keep the existing THEN/NOW card design (pink left border for THEN, gold for NOW) but now only for teachers. Include: school year, adjusted salary, original dollars note, hourly rate.

Hours note: "Based on 1,402 contractual hours/year (187 days x 7.5 hrs)"

### 5. vs. The Nation (NEW)
**Heading:** "HOW KENTUCKY COMPARES" (Oswald)
**Subheading:** "Kentucky vs. the national average" (EB Garamond italic)

Two-stat comparison, side by side on desktop, stacked on mobile:

```
┌──────────────────┬──────────────────┐
│  KENTUCKY        │  NATIONAL AVG    │
│  -17%            │  +3%             │  (or whatever the real numbers are)
│  $53,947         │  $72,030         │
│  Rank: 42nd      │                  │
└──────────────────┴──────────────────┘
```

Below the comparison: one narrative sentence. E.g., "Since you graduated, the average American teacher saw a 3% raise. Kentucky teachers lost 17%. Kentucky now ranks 42nd out of 50 states."

**Data source:** NEA Rankings & Estimates, published annually. National average teacher salary available from NCES Digest of Education Statistics Table 211.60 going back to 1969-70 (same source/format as existing KDE teacher data). Current national average: $72,030 (2023-24).

**Data pipeline task:** Create `data/output/national-teacher-salary.json` with same structure as `teacher-salary.json`:
```json
[
  {
    "grad_year": 2005,
    "school_year": "2004-2005",
    "salary_adjusted": 62145,
    "salary_nominal": 47750,
    "hourly_rate_adjusted": 44.33
  }
]
```

Source data (NCES Table 211.60, nominal dollars — need CPI adjustment):
| Year | US Average |
|------|-----------|
| 1969-70 | $8,626 |
| 1979-80 | $15,970 |
| 1989-90 | $31,367 |
| 1999-00 | $41,807 |
| 2009-10 | $55,370 |
| 2019-20 | $64,133 |
| 2020-21 | $65,293 |
| 2021-22 | $66,397 |
| 2023-24 | $72,030 |
| 2024-25 | $74,177 (est.) |

Gap years will need interpolation or sourcing from annual NEA reports. The existing Python pipeline in `scripts/` already handles CPI adjustment — extend it for this data.

### 6. vs. Your Neighbors (NEW — interactive)
**Heading:** "YOUR NEIGHBORS" (Oswald)
**Subheading:** "How Kentucky teacher pay stacks up against bordering states" (EB Garamond italic)

**Interactive state selector:** Row of clickable buttons/pills at top of section:
```
[ OH ] [ IN ] [ IL ] [ MO ] [ TN ] [ VA ] [ WV ]
```
Default: highlight all, show a ranked bar chart or list. When user clicks a single state, show a detailed KY-vs-that-state comparison card (same THEN/NOW format). Clicking again deselects.

**Current salary data (2023-24, nominal):**
| State | Avg Salary | Rank |
|-------|-----------|------|
| Illinois | $75,978 | 12th |
| Ohio | $68,236 | 21st |
| Virginia | $66,327 | 25th |
| Indiana | $58,620 | 32nd |
| Tennessee | $58,630 | 34th |
| **Kentucky** | **$58,325** | **42nd** |
| West Virginia | $55,516 | 47th |
| Missouri | $55,132 | 48th |

**Historical data available (NCES Table 211.60, nominal):**
| State | 1969-70 | 1989-90 | 1999-00 | 2009-10 | 2019-20 | 2021-22 |
|-------|---------|---------|---------|---------|---------|---------|
| KY | $6,953 | $26,292 | $36,380 | $49,543 | $53,907 | $54,574 |
| OH | $8,300 | $31,218 | $41,436 | $55,958 | $61,406 | $63,153 |
| IN | $8,833 | $30,902 | $41,850 | $49,986 | $51,745 | $54,126 |
| IL | $9,569 | $32,794 | $46,486 | $62,077 | $68,083 | $72,301 |
| MO | $7,799 | $27,094 | $35,656 | $45,317 | $50,817 | $52,481 |
| TN | $7,050 | $27,052 | $36,328 | $46,290 | $51,862 | $53,619 |
| VA | $8,070 | $30,938 | $38,744 | $50,015 | $57,665 | $59,965 |
| WV | $7,650 | $22,842 | $35,009 | $45,959 | $50,238 | $50,315 |

**Data pipeline task:** Create `data/output/state-teacher-salary.json`:
```json
{
  "OH": [
    { "grad_year": 2005, "school_year": "2004-2005", "salary_adjusted": 58200, "salary_nominal": 44700 }
  ],
  "IN": [...],
  ...
}
```

Annual state-by-state data is available from NCES Digest tables and NEA Rankings & Estimates (published annually since 1960s). For the data pipeline: download NCES Table 211.60 from the most recent Digest edition, extract KY + 7 border states + US average, apply CPI adjustment using existing pipeline.

### 7. What Your Pay Actually Buys (NEW — cost of living)
**Heading:** "WHAT YOUR PAY ACTUALLY BUYS" (Oswald)
**Subheading:** "A teacher's salary, measured in real life" (EB Garamond italic)

Show what percentage of a teacher's annual salary goes to key expenses, THEN vs. NOW. Use emoji icons for visual punch and screenshottability.

```
Layout (each row):
🏠 Rent     THEN: 22% of salary → NOW: 31% of salary   [▰▰▰▰▰▰▰▱▱▱]
⛽ Gas       THEN: 4% of salary  → NOW: 5% of salary    [▰▰▱▱▱▱▱▱▱▱]
🔌 Utilities THEN: 6% of salary → NOW: 9% of salary     [▰▰▰▱▱▱▱▱▱▱]
🛒 Groceries THEN: 14% of salary → NOW: 19% of salary   [▰▰▰▰▰▱▱▱▱▱]
```

End with a total: "In [YEAR], these basics cost X% of a teacher's salary. Today: Y%."

The progress bars / percentage bars should be colorful and visual — this section needs to be the most shareable part of the page after the hero stat.

**Data sources:**

All available from FRED (Federal Reserve Economic Data) with free API access and CSV downloads:

| Item | FRED Series | Coverage | Notes |
|------|------------|----------|-------|
| Rent | CUSR0000SEHA (Rent of primary residence, CPI-U, US City Avg) | 1981-present | Use as index, anchor to KY median rent ($1,071/mo current) |
| Gas | CUSR0000SETB01 (Gasoline all types, CPI-U) | 1967-present | Or use average price series APU000074714 |
| Electricity/Utilities | CUSR0000SEHF01 (Electricity, CPI-U) | 1957-present | KY avg utility bill ~$465/mo |
| Food at home | CUSR0000SAF11 (Food at home, CPI-U) | 1952-present | |

**Methodology note:** These are national CPI indices, not Kentucky-specific (BLS doesn't publish state-level CPI, only regional — KY is in "South" region). Use national CPI indices to calculate relative price change, then anchor to current Kentucky-specific dollar amounts. This is methodologically sound and standard practice.

**Data pipeline task:** Create `data/output/cost-of-living.json`:
```json
[
  {
    "grad_year": 2005,
    "rent_annual_adjusted": 10800,
    "rent_pct_of_salary": 0.22,
    "gas_annual_adjusted": 2400,
    "gas_pct_of_salary": 0.04,
    "utilities_annual_adjusted": 3600,
    "utilities_pct_of_salary": 0.06,
    "food_annual_adjusted": 8400,
    "food_pct_of_salary": 0.14,
    "total_pct": 0.46
  }
]
```

### 8. The Legislator Comparison (REVISED — reframed)
**Heading:** "WHO SETS THE BUDGET?" (Oswald)

Don't lead with magnitude. Lead with the framing: "Kentucky legislators decide how much teachers get paid. Here's how they've treated their own compensation."

Show two numbers side by side:
- Teacher hourly rate: $38.48/hr (1,402 hrs/yr)
- Legislator hourly rate: $71.20/hr (480 hrs/yr, 60 session days)

Narrative: "Legislators work 60 days a year and earn $71.20 per hour. Teachers work 187 days and earn $38.48. The people who set the budget made sure their own pay kept up."

This section is now a supporting beat, not a headline. Keep it tight — no THEN/NOW cards, just the two hourly rates side by side and the narrative.

### 9. CTA Section (ENHANCED)
**Heading:** "THINK THIS SHOULD CHANGE?" (Oswald)
**Background:** Gold

**Enhancements:**
- **Auto-generated share image:** Use `html2canvas` to capture the Hero Stat section as a 1200x630 PNG. Store in memory. Use as the image for native share API / OG meta tag.
- **Short-form share message** (tweetable, <280 chars): "Since I graduated in [YEAR], Kentucky teacher pay dropped [X%]. Meanwhile, the national average went up. See your year: [URL] #WhenIWasInSchool"
- **Long-form message** (email/letter): Keep existing legislator message template but update with new comparison data.
- **Three buttons:** SHARE YOUR RESULTS, SUPPORT THE FIGHT, CONTACT YOUR LEGISLATOR (keep existing links)
- **Sticky bottom bar:** Once user scrolls past hero stat, show a pinned bar at bottom: "[X% decline] · Share this →" with share button. CSS `position: sticky` on mobile, fixed on desktop. Dismissable with X.

### 10. Footer (keep as-is)
KSVT logo + site title.

---

## Implementation Priority Order

### Phase 1: Core Restructure (do first)
1. **Remove bus driver and legislator sections from primary flow.** Gut the three-section comparison. Keep teacher data as the spine.
2. **Build the Hero Stat section.** Giant animated percent change, narrative text, THEN/NOW summary. This replaces the old Hook + Educator sections.
3. **Remove district dropdown** from landing page. Simplify to year + email.
4. **Implement two-column layout** for THEN/NOW detail cards (desktop: side-by-side, mobile: stacked). CSS grid with `@media (min-width: 768px)`.
5. **Add count-up animation** on the hero percent change number. Pure JS, no dependencies. Use `requestAnimationFrame` for smooth animation over ~1.5 seconds.

### Phase 2: New Comparison Sections (do second)
6. **Build "vs. The Nation" section.** Create `national-teacher-salary.json` data file. Render KY vs. national side-by-side comparison with ranking badge.
7. **Build "vs. Your Neighbors" section.** Create `state-teacher-salary.json` data file. Build interactive state pill buttons. Default view: ranked list of all 7 states + KY. Click state: detailed comparison card. Use CSS transitions for smooth swap.
8. **Build "What Your Pay Actually Buys" section.** Create `cost-of-living.json` data file. Emoji-labeled rows with animated progress bars showing percent of salary. THEN vs. NOW side by side.

### Phase 3: Sharing & Virality (do third)
9. **Implement `html2canvas` share card generation.** Capture hero stat as 1200x630 image on results load. Cache in memory. Wire to Share API.
10. **Add short-form share message** (Twitter/social optimized, <280 chars, includes #WhenIWasInSchool hashtag).
11. **Add sticky bottom share bar.** Appears on scroll past hero, dismissable, mobile-friendly.
12. **Update OG meta tags** to use generated share image dynamically (may need server-side for full OG support — evaluate whether to do client-side fallback with a static default image).

### Phase 4: Legislator Reframe (do fourth)
13. **Rebuild legislator section** as compact "Who Sets The Budget?" supporting section. Two hourly rates side by side + narrative paragraph. No cards.

### Phase 5: Polish & Stretch Goals
14. **Scroll-triggered reveals.** Use `IntersectionObserver` to fade/slide sections in as user scrolls. Lightweight, no dependencies.
15. **"Try a different year" quick-select** — after seeing results, surface a small year picker that lets users compare without scrolling back to top.
16. **Explore district-level data.** KDE publishes average classroom teacher salary by district, 1989-present, in a downloadable spreadsheet. This could power a "Your District" section — but adds significant data pipeline work and reintroduces the district dropdown. Backlog for v3.

---

## Data Pipeline Summary

All new data files go in `data/output/`. The existing Python pipeline in `scripts/` handles CPI adjustment using BLS CPI-U (FRED CPIAUCNS). Extend it for these new sources:

| File | Source | Format | Priority |
|------|--------|--------|----------|
| `national-teacher-salary.json` | NCES Digest Table 211.60 + NEA annual reports | Same as teacher-salary.json | Phase 2 |
| `state-teacher-salary.json` | NCES Digest Table 211.60 + NEA annual reports | Keyed by state abbreviation | Phase 2 |
| `cost-of-living.json` | FRED CPI series (rent, gas, electricity, food) | Per grad year, pct of salary | Phase 2 |

**NCES data access:** https://nces.ed.gov/programs/digest/d22/tables/dt22_211.60.asp — downloadable table with state-by-state average teacher salary, selected years 1969-70 through 2021-22. Gap years need interpolation or sourcing from annual NEA Rankings & Estimates PDFs.

**FRED data access:** All CPI series downloadable as CSV via `https://fred.stlouisfed.org/series/[SERIES_ID]`. No API key needed for CSV download.

**District-level data (future):** KDE School District Personnel Information page publishes average classroom teacher salary by district, 1989-present. URL: https://www.education.ky.gov/districts/FinRept/Pages/School%20District%20Personnel%20Information.aspx (may need manual download — the page returned 403 on automated fetch).

---

## Technical Notes

- **No new dependencies** except `html2canvas` (CDN, ~40KB gzipped) for share card generation. Everything else is vanilla JS/CSS.
- **Cache busters:** Bump `?v=5` to `?v=6` on all CSS/JS references after changes.
- **Responsive breakpoint:** Keep 600px for card stacking, add 768px for two-column detail layout.
- **Accessibility:** All animated elements should respect `prefers-reduced-motion`. Provide `aria-live` region for dynamically loaded comparison data.
- **Performance:** New JSON files are small (< 50KB each). Continue fetching all in parallel on page load via `loadAllData()`.

---

## Key Design Constraints

- **Screenshottable:** Every section should look complete and compelling in a phone screenshot. No section should require scrolling to get the point.
- **Mobile-first:** Majority of social sharing happens on phones. Design for 375px width first, then enhance for desktop.
- **Emoji usage:** Cost of living section uses emoji (🏠⛽🔌🛒) as visual anchors. These render natively on all modern devices and make screenshots pop.
- **Brand tokens:** All existing brand tokens (navy, gold, pink, orange, green) remain. No new colors.
- **Fonts:** Oswald (display), Plus Jakarta Sans (body), EB Garamond (editorial accent) — no changes.

---

*This brief supersedes the original `CLAUDE-CODE-IMPLEMENTATION-PLAN.md`. Reference `CURRENT-STATE.md` for the existing codebase.*
