# Publishing Roadmap — Where Everything Goes, and in What Order

This is the control-flow document: what lives on GitHub, Kaggle, Power BI and Tableau Public, why each
one gets what it gets, and the order to actually do it in. It assumes the artifacts already built in this
project: the Excel system, two notebooks, the Word memoir, the `analysis_export/` CSVs, and the two new
SQL database files (`market_stall.duckdb`, `market_stall.sqlite`).

## The logic behind the split

| Platform | Audience | What it's good at | What goes there |
|---|---|---|---|
| **GitHub** | Recruiters/technical reviewers clicking from a resume/LinkedIn | Code quality, structure, reproducibility | Everything, canonically. The hub every other link points back to. |
| **Kaggle** | Data science community, dataset discovery | Approachable EDA, dataset reuse | The cleaned dataset + 1-2 light, visual notebooks — general info, not the deep operational stuff. |
| **Power BI** | Business/operations-facing reviewers | Relational modeling, DAX, operational reporting | The supply-chain & inventory story: suppliers, backups, EOQ/reorder, restock alerts. |
| **Tableau Public** | General/public audience, no login needed | Visual storytelling, public shareability | The revenue/trend/forecast story: 2-year trend, seasonality, ABC/Pareto, freezer ROI. |

Your instinct to keep Kaggle "general + a couple of examples" and push the complex analysis into Power BI
and Tableau is the right call — Kaggle's audience rewards clarity and story over exhaustive depth, and
BI tools are literally built for the deeper, interactive layer.

**One practical constraint that shapes the order below:** Tableau **Public** (the free tier) can only
connect to flat files (CSV/Excel) or extracts — it cannot connect live to a SQL database. Power BI Desktop
can connect to a SQLite file directly. So the SQL database is real and demonstrable (and lives on GitHub as
proof of the pipeline + powers Power BI directly), but Tableau still reads from the flat `analysis_export/`
CSVs — which is normal practice, not a workaround.

## Order of action

### 1. GitHub first — it's the anchor everything else links back to
Repo structure:
```
market-stall-analytics/
├── README.md                  <- update with live links once steps 3-5 are done
├── ASSUMPTIONS.md
├── data/                      <- raw generator CSVs (products, suppliers, supply_links, purchases, batch_outcomes)
├── analysis_export/           <- the 7 analysis-ready CSVs
├── sql/
│   ├── market_stall.duckdb
│   └── market_stall.sqlite
├── notebooks/
│   ├── Market_Stall_Analysis.ipynb
│   └── SQL_Analysis.ipynb
├── excel/
│   └── Market_Stall_Management.xlsx
└── docs/
    └── Process_Memoir.docx
```
Push this before touching Kaggle/Power BI/Tableau — it's where you'll link back to from all three, and
having it live first means every other platform's description can say "full code & data: [GitHub link]"
from day one.

### 2. SQL export via Python — already done, verify and commit
`sql/market_stall.duckdb` and `sql/market_stall.sqlite` are built from the raw CSVs through real SQL
(joins, CTEs, window functions — see `SQL_Analysis.ipynb`), producing 4 materialized analytical tables
(`products_enriched`, `batches_full`, `supplier_scorecard`, `monthly_trend`) alongside the 5 raw ones.
Commit both files to `sql/` in the same push as step 1.

### 3. Kaggle — dataset + one or two example notebooks
1. **Dataset** first: upload the `analysis_export/` CSVs as a Kaggle Dataset. Write the description as the
   "what/why" (portfolio adaptation, fictitious suppliers, approximate amounts — same disclaimer as
   everywhere else), and fill in Kaggle's column descriptions using `ASSUMPTIONS.md` as the source.
2. **Notebook A — "Market Stall Catalog & Profitability" (EDA):** a trimmed version of
   `Market_Stall_Analysis.ipynb` Sections 1-6 (catalog overview, margin distribution, category ranking,
   seasonality). Keep it visual and light on assumptions/formulas.
3. **Notebook B — "Supply Chain Risk: Backup Suppliers & the HHI" (focused example):** just Section 8 —
   one clear, memorable idea (the concentration index) executed well, rather than the full pipeline.
4. Deliberately leave out: EOQ/reorder/safety stock, the demand forecast, and the SQL notebook. Those stay
   on GitHub/Power BI where the audience expects depth.

### 4. Power BI — the supply-chain & inventory dashboard
**Data source:** `Get Data > Text/CSV`, import `analysis_products.csv`, `analysis_supply_links.csv`,
`analysis_suppliers.csv`, `analysis_inventory_optimization.csv`, `analysis_batches.csv`. (Optional, to show
the SQL pipeline end-to-end: `Get Data > ODBC/SQLite` pointed at `market_stall.sqlite` instead — same
tables, sourced live from the database rather than the flat export.)

**Relationships (star schema):** `Products[ProductID]` 1-\* to `Supply_Links[ProductID]`,
`Purchases/Batches[ProductID]`, and `Inventory_Optimization[ProductID]`; `Suppliers[SupplierID]` 1-\* to
`Supply_Links[SupplierID]`.

**Suggested pages & what feeds them:**

| Page | Visuals | Source table(s) / fields |
|---|---|---|
| Supply Chain Overview | KPI cards: # suppliers, HHI, backup coverage %; bar of lead time by supplier; risk matrix | `analysis_suppliers.csv` (`hhi_contribution`, `dependency_risk`, `avg_lead_time`) |
| Inventory & Restocking | Table with conditional formatting on `reorder_point` vs `CurrentStock`; bar of EOQ by category; slicer by Essential | `analysis_inventory_optimization.csv` joined to `analysis_products.csv` |
| Waste & Freezer ROI | KPI cards for annualized waste $ and payback months; bar of waste % by category/season | `analysis_batches.csv` (derive Season from `PurchaseDate` in Power Query if not already present) |

**DAX starting points:** `Total Revenue = SUM(analysis_batches[Revenue_USD])`,
`Waste % = DIVIDE(SUM(analysis_batches[QtyWasted]), SUM(analysis_batches[Quantity]))`.

Publish via **Publish to Web** for a public, no-login link (fine here since the data is synthetic), or
share via Power BI Service if you'd rather keep it behind a login.

### 5. Tableau Public — the revenue/trend/forecast story
**Data source:** connect to `analysis_batches.csv`, `analysis_products.csv`, and `analysis_monthly.csv`
directly (flat files — remember, Tableau Public doesn't do live DB connections).

**Suggested sheets, combined into one dashboard/story:**

| Sheet | Chart type | Source table(s) / fields |
|---|---|---|
| 2-year revenue & waste trend | Dual-axis line + bar | `analysis_monthly.csv` (`revenue_usd`, `waste_pct`) |
| ABC / Pareto | Bar + cumulative line | `analysis_products.csv` (`Class`, revenue rolled up) |
| Category performance | Highlight table or bar-in-bar | `analysis_products.csv` / `analysis_batches.csv` grouped by `Category` |
| Seasonal demand heatmap | Heatmap, Category × Season | `analysis_batches.csv` (`Category`, `Season`, `Quantity`) |

Add Category and Season as dashboard-level filters so the story is explorable, not just static. Publish to
your Tableau Public profile — it needs no login to view, which makes it the easiest link to drop directly
into a resume or LinkedIn post.

### 6. Close the loop
Once steps 3-5 are live, go back to `README.md` (and the Kaggle notebook descriptions) and add the actual
links to the Kaggle dataset, the Power BI report, and the Tableau Public dashboard — so GitHub becomes the
single hub that ties every destination together.

## Quick checklist

- [ ] Push GitHub repo (structure above)
- [ ] Commit `market_stall.duckdb` / `market_stall.sqlite` to `sql/`
- [ ] Kaggle: publish dataset
- [ ] Kaggle: publish Notebook A (EDA)
- [ ] Kaggle: publish Notebook B (HHI focus)
- [ ] Power BI: build 3 pages, publish
- [ ] Tableau Public: build 4 sheets + dashboard, publish
- [ ] Update `README.md` with all live links
