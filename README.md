# Micron Under Pressure: Financial Impact of the 2026 AI Memory Chip Shortage

I built this project to explore how the 2026 AI/HBM memory chip shortage disrupted
Micron's revenue trajectory — and to see, concretely, how far a "business as usual"
forecast would have missed reality.

**[View my interactive Tableau dashboard →]([PASTE_YOUR_TABLEAU_PUBLIC_LINK_HERE](https://public.tableau.com/app/profile/syed.hasnain7947/viz/MicronUnderPressureFinancialImpactofthe2026AIMemoryChipShortage/Dashboard1))**

## The question I wanted to answer

Micron's revenue exploded starting in late 2025 as AI-driven demand for high-bandwidth
memory (HBM) collided with a global supply shortage. I wanted to know: if I'd built a
forecast using only pre-shortage growth trends, how wrong would that forecast have
been — and what does that gap actually look like in dollars?

## What's in this repo

| Folder | Contents |
|---|---|
| `sql/` | SQLite database (`micron_financials.db`) I built holding 22 real quarters of Micron revenue, gross profit, and EPS (Feb 2021–May 2026), plus the script I used to build it |
| `python/` | My forecasting script, which builds a naive pre-shortage trend line and compares it to shortage-era actuals; and the export script I used to generate the CSVs for Tableau |
| `excel/` | The driver-based financial model I built, with Bear/Base/Bull scenario toggles, a driver-based revenue and gross profit projection, and a price-vs-volume variance bridge |
| `data/` | Exported CSVs of the quarterly financials, the forecast-vs-actual comparison, and the three scenario projections |

## How I built it

1. **SQL** — I sourced and structured 22 quarters of Micron's real, publicly reported
   financials into a local database.
2. **Python** — I built a naive linear forecast using only pre-shortage quarters, then
   measured the gap between that forecast and actual shortage-era revenue. The gap
   grows from roughly 63% in the first shortage quarter to over 490% by the most
   recent quarter.
3. **Excel** — I built a driver-based model (volume growth, price growth, gross margin
   assumptions) with a scenario toggle for Bear, Base, and Bull cases, plus a
   price-vs-volume variance bridge.
4. **Tableau** — I assembled a three-part dashboard: the full 2021–2026 revenue trend,
   the forecast-vs-actual gap, and the three forward-looking scenarios.

## What I found

A pre-shortage trend line would have predicted roughly $7B in quarterly revenue for
Micron's most recent quarter. Actual revenue came in near $41.5B — a gap driven almost
entirely by shortage-era pricing power, not organic volume growth.

## Data source

All financial figures are Micron's real, publicly reported numbers, pulled from:
- [Micron Investor Relations](https://investors.micron.com)
- [Micron SEC filings (10-K/10-Q)](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000723125&type=10-K&dateb=&owner=include&count=10)
- [stockanalysis.com — MU quarterly financials](https://stockanalysis.com/stocks/mu/financials/?p=quarterly)
- [macrotrends.net — MU revenue, gross profit, and EPS](https://www.macrotrends.net/stocks/charts/MU/micron-technology/revenue)

No synthetic or placeholder data was used — every quarter in this analysis reflects
Micron's actual reported results.

## Tools I used
SQLite · Python (sqlite3, csv) · Excel · Tableau Public
