> **Revisión 2026-09-08:** Consulte [DECISION_REVIEW.md](DECISION_REVIEW.md). Las cifras siguientes son resultados de cohortes simuladas, con cierres hasta 2035. El payback y la reposición no están validados para operación real. / See the corrected decision review before using legacy results.

# Assumptions & Methodology

This project simulates two years of a market stall's operations. Every effort was made to ground the
numbers in real reference ranges rather than pure randomness (see below), but it's still a simulation, and
being explicit about what's assumed vs. what's derived is part of doing this honestly. This file collects
every non-obvious assumption in one place.

## Prices & currency

- **Exchange rate:** 1 USD = 935 CLP (observed rate, 21 Jul 2026). Applied uniformly; a real business would
  see this rate move daily.
- **Consumer sale prices** are rounded to the nearest 500 CLP (so they end in whole or half units), matching
  how prices are actually quoted at a fair.
- **Category margins** (34-58% depending on category) are grounded in the general spread between retail and
  wholesale prices for bulk/artisanal goods in Chile, not a specific supplier quote.
- **Backup supplier prices** are generated as the primary price plus a random markup (roughly 3-8 percentage
  points off the primary's margin), reflecting that a fallback option is usually a little more expensive —
  this is a plausible pattern, not observed data.

## Simulated purchase & outcome data (2 years)

- **Seasonality:** categories tagged "Spring-Summer" or "Fall-Winter" get a 1.6x demand multiplier in their
  season and 0.6x outside it; "All year" categories are flat. This is a simplification — real seasonal
  curves are smoother and vary by product, not a single step function.
- **Holiday bumps:** +25% in September (Fiestas Patrias), +30% in December — illustrative multipliers, not
  measured uplift.
- **Year-over-year growth:** +8% from 2025 onward, representing the business modernizing (card payments,
  fewer lost sales) — a modeling choice to reflect the Process Memoir's narrative, not a forecast.
- **Spoilage:** each category has a *baseline* spoilage rate if a batch isn't fully sold, multiplied by a
  *heat factor* (1.8x in Dec-Feb, 1.3x in shoulder months) for perishables (olives, grains/mote, honey,
  peanuts, trail mix). Packaging essentially never spoils. These rates are illustrative but internally
  consistent — e.g. grains/mote and olives come out as the top spoilers, which matches why the business
  bought a freezer in the first place.
- **Expiry dates:** concrete where shelf life is well-defined (most categories); marked "Estimated" for
  olives and grains, where real shelf life is more variable in practice.

## Inventory optimization (EOQ / reorder point / safety stock)

- **Empirical inputs (from the simulated 2-year purchase history, not assumed):** average daily demand and
  its variability per product, and each product's lead time from its primary supplier.
- **Assumed inputs (stated explicitly — replace with real figures if the business tracks them):**
  - Holding cost: 25% of purchase cost per year (a standard textbook default for small, low-turnover
    inventory when no real warehousing/insurance/capital cost is tracked).
  - Ordering cost: a flat US$ 3 per purchase order, representing the time/effort of placing an order at
    this scale — not a measured cost.
  - Service level: 95% (Z = 1.645) for the safety-stock calculation.
- Because EOQ is sensitive to the holding/ordering cost assumptions, treat its absolute value as directional
  rather than exact; the reorder point and safety stock lean more heavily on the empirical demand data and
  are comparatively more trustworthy.
- **Edge case:** a handful of products have a 0-day lead time from their primary supplier (same-day
  fulfillment in the simulated data), which mathematically drives their safety stock and reorder point to
  0 — expected given the formula, not a bug.

## Freezer ROI

- The "prevented waste fraction" (50% / 65% / 80% scenarios) is an assumption, since the simulation doesn't
  model the freezer's effect directly — it estimates a plausible range for how much of the *already
  observed* waste in Olives and Grains a freezer could realistically prevent, rather than claiming a single
  precise number.
- The freezer cost range (US$ 270-340) comes from the Process Memoir's investment table, itself grounded in
  real Chilean chest-freezer price ranges for a 200-250L unit.

## Demand forecast

- Holt-Winters exponential smoothing with additive trend and yearly seasonality, on total monthly purchase
  quantity across all products (not per-product, to keep the series long enough to be meaningful with only
  24 months of history).
- Backtested via 1-month-ahead walk-forward validation over the last 6 months (MAPE ~5%). Two years is short
  for a seasonal model — ideally 3+ full cycles — so this should be treated as a first pass to refine as
  more months of real or simulated data come in, not a firm commitment.

## What's real vs. simulated, at a glance

| Element | Status |
|---|---|
| Product names, categories, units | Realistic, manually curated |
| Reference prices (before rounding/margin) | Grounded in real Chilean market ranges |
| Supplier names, contacts, addresses | Fictitious |
| Town/region names | Real Chilean locations; businesses at them are invented |
| 2-year purchase & outcome history | Fully simulated, but rule-based (seasonality, heat, holidays, trend) |
| Exchange rate | Real, single point-in-time snapshot |
