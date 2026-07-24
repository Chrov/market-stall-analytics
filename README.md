# Market Stall Analytics — Portfolio Project

**Portfolio note:** this project is a full English adaptation/translation of an original Spanish project
built for a real family market-stall (*feria*) business. All supplier names, contacts and locations are
**fictitious**, and all monetary amounts are **approximate** — grounded in real reference ranges from
Chilean fairs and wholesale suppliers (2025–2026), converted at 1 USD = 935 CLP (observed rate).

## What this is

An end-to-end analytics project for a small artisanal/bulk-goods market stall: a 128-product catalog, a
supply chain with **primary + backup suppliers** for every product, two years of simulated purchase and
sell-through history (with real seasonality, summer-heat spoilage and holiday demand), and three layers of
analysis on top of it — spreadsheet, Python, and SQL.

# Market Stall Analytics — Portfolio Project

**Portfolio note:** this project is a full English adaptation/translation of an original Spanish project
built for a real family market-stall (*feria*) business. All supplier names, contacts and locations are
**fictitious**, and all monetary amounts are **approximate** — grounded in real reference ranges from
Chilean fairs and wholesale suppliers (2025–2026), converted at 1 USD = 935 CLP (observed rate).

## What this is

An end-to-end analytics project for a small artisanal/bulk-goods market stall: a 128-product catalog, a
supply chain with **primary + backup suppliers** for every product, two years of simulated purchase and
sell-through history (with real seasonality, summer-heat spoilage and holiday demand), and four layers of
analysis on top of it — spreadsheet, Python, SQL, and (soon) published BI dashboards.

## Repository structure

```
market-stall-analytics/
├── README.md                    <- you are here
├── ASSUMPTIONS.md               <- every non-obvious assumption, in one place
├── PUBLISHING_ROADMAP.md        <- how this project is segmented across GitHub/Kaggle/Power BI/Tableau
├── LICENSE
├── data/                        <- raw source CSVs (products, suppliers, supply_links, purchases, batch_outcomes)
├── analysis_export/             <- 7 clean, analysis-ready CSVs — the direct source for BI tools
├── sql/                         <- market_stall.duckdb & market_stall.sqlite (the SQL export layer)
├── notebooks/
│   ├── Market_Stall_Analysis.ipynb   <- main analysis (Python)
│   └── SQL_Analysis.ipynb            <- same KPIs, rebuilt as SQL (DuckDB, joins/CTEs/window functions)
├── excel/
│   └── Market_Stall_Management.xlsx  <- operational spreadsheet system (catalog, supply chain, dashboards)
└── docs/
    └── Process_Memoir.docx           <- the operational story behind the data
```

## Repository contents

| File / folder | What it is |
|---|---|
| `excel/Market_Stall_Management.xlsx` | The operational spreadsheet system: catalog, suppliers, supply links, 2 years of purchases & outcomes, and two live dashboards (general + supply chain), all formula-driven. |
| `notebooks/Market_Stall_Analysis.ipynb` | The main analysis notebook. Installs its own dependencies. Covers descriptive stats, profitability, ABC/Pareto, seasonality, supply-chain concentration (HHI), hypothesis testing, **freezer ROI**, **EOQ / reorder point / safety stock**, and a **demand forecast** with a walk-forward backtest. |
| `notebooks/SQL_Analysis.ipynb` | The same core KPIs rewritten as SQL (DuckDB) — joins, CTEs, window functions (`RANK`, running `SUM() OVER`). |
| `sql/market_stall.duckdb` / `sql/market_stall.sqlite` | The data persisted as real SQL databases (raw tables + materialized analytical tables), built via Python — the tangible "export to SQL" step. `.sqlite` is there for BI tools with a native SQLite connector (e.g. Power BI). |
| `docs/Process_Memoir.docx` | The narrative behind the project: site diagnosis, the freezer, payment terminal, crate logistics, and supplier organization that this data model represents. |
| `analysis_export/` | Seven flat CSVs, ready to load into a BI tool: `analysis_products`, `analysis_supply_links`, `analysis_purchases`, `analysis_batches`, `analysis_suppliers`, `analysis_monthly`, `analysis_inventory_optimization`. |
| `ASSUMPTIONS.md` | Every non-obvious assumption behind the simulated data and the inventory-optimization formulas, in one place. |
| `PUBLISHING_ROADMAP.md` | How this same project is deliberately segmented across GitHub, Kaggle, Power BI and Tableau Public, and in what order — with a table of which source table/field feeds which chart. |

## How to run it

```bash
# Excel: open directly, no add-ins required (all formulas are Excel-standard, no XLOOKUP/FILTER)

# Notebooks: each installs its own Python dependencies on first run
jupyter execute notebooks/Market_Stall_Analysis.ipynb --output=notebooks/Market_Stall_Analysis.ipynb
jupyter execute notebooks/SQL_Analysis.ipynb --output=notebooks/SQL_Analysis.ipynb

# SQL databases: query directly, e.g.
python3 -c "import duckdb; print(duckdb.connect('sql/market_stall.duckdb').sql('SELECT * FROM supplier_scorecard').df())"
```

## Headline findings

- **2-year revenue:** ~US$ 442,000 · **gross profit:** ~US$ 111,000 · **overall waste rate:** 3.4%.
- **Freezer business case:** annualized waste in the two categories it targets (Olives, Grains/mote) is
  ~US$ 3,460/year; across conservative-to-optimistic scenarios the freezer (~US$ 270–340) pays for itself
  in roughly **1.2–2.4 months**.
- **Supply chain:** every product has a documented backup supplier; the supplier base's HHI concentration
  index is ~1,430 (low), and using a backup costs ~13% more on average — the price of resilience.
- **Forecast:** a Holt-Winters model on 24 months of purchase volume backtests at ~5% MAPE one month
  ahead — treated as a first pass, not a guarantee, given the short history.

## Live dashboards & other platforms

Per `PUBLISHING_ROADMAP.md`, this project is deliberately split by audience: light EDA on Kaggle, deeper
operational analysis in Power BI, and the revenue/trend story in Tableau Public. Links go here once each
is published:

- Kaggle dataset & notebooks: _link pending_
- Power BI report (supply chain & inventory): _link pending_
- Tableau Public dashboard (revenue, trend & forecast): _link pending_

## What's next

- Publish the three links above.
- Extend the demand forecast per top-selling product instead of only at the total-catalog level, once more
  months of history are available.
- Replace the illustrative holding-cost/ordering-cost assumptions in the EOQ calculation with real figures
  if the business starts tracking them.

## Author

Camilo Vergara Salas — Data Analyst / Analyst Programmer. [linkedin.com/in/camilo-evs](https://linkedin.com/in/camilo-evs) · [github.com/Chrov](https://github.com/Chrov)
