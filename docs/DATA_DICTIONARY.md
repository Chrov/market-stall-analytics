# Diccionario / Data dictionary

| Archivo / File | Grano / Grain | Clave / Key | Uso / Use |
|---|---|---|---|
| reviewed_batch_cohorts.csv | Lote de compra / purchase batch | BatchID | 3,825 lotes simulados / synthetic batches |
| reviewed_category_economics.csv | Categoría / category | Category | Merma y rentabilidad / waste and profitability |
| bi_Monthly.csv | Mes de compra / purchase month | month | Cohortes, no ventas mensuales / cohorts, not monthly sales |

`Revenue_CLP`: ingreso de cierre del lote; `BatchCost_CLP`: costo comprado; `GrossProfit_CLP = Revenue_CLP - BatchCost_CLP`; `WasteCost_CLP`: cantidad perdida × costo unitario. Razón de merma = suma de costo perdido / suma de costo comprado. Margen = suma de utilidad bruta / suma de ingreso. No promediar porcentajes de filas ni sumar kg con frascos.

Revenue is recorded at batch closure. Gross profit subtracts acquisition cost; waste values lost quantity at acquisition cost. Ratios use sums, not averages of row percentages. Physical units are not comparable across SKUs.

`PurchaseCohort`: mes de compra. Corte: 2025-06-30; 498 cierres ocurren después, hasta 2035. Los cierres futuros se conservan como característica de la simulación y se separan en el Excel. No se reemplazan por fechas inventadas. Los CSV originales se conservan; no hay evidencia de ventas reales ni de ahorros implementados.

Purchase cohorts are separated from actual closure dates. Future simulated closures are retained and disclosed, never replaced with fabricated dates. Original CSV inputs are preserved. No realized business savings are asserted.
