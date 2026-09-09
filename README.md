# Market Stall Analytics

**ES:** Control de merma y reposición para una feria con 128 productos y 22 proveedores. Caso simulado con Excel, SQL y Python, orientado a decidir dónde iniciar un piloto de mejora.

**EN:** Waste and replenishment analysis for a market stall with 128 products and 22 suppliers. A synthetic Excel, SQL and Python case supporting the selection of an improvement pilot.

## Hallazgos revisados / Reviewed findings

| Métrica de cohortes simuladas / Synthetic cohort metric | Resultado |
|---|---:|
| Lotes de compra / Purchase batches | 3,825 |
| Costo de merma / Waste at acquisition cost | CLP 8,992,168 |
| Merma / costo comprado — Waste / purchase cost | 2.90% |
| Margen bruto agregado / Aggregate gross margin | 25.03% |
| Cierres posteriores al corte / Closures after cutoff | 498 |

Las compras abarcan julio de 2023–junio de 2025, pero los cierres llegan hasta 2035. Los resultados completos son de cohortes, no ventas realizadas en dos años. El Excel separa cierres hasta el 30 de junio de 2025 y posteriores. La merma monetaria evita mezclar kg, frascos y paquetes.

Purchases span July 2023–June 2025, but batch closures extend to 2035. Full outcomes represent purchase cohorts, not two-year realized sales. The workbook separates closures by the 2025-06-30 cutoff. Monetary waste avoids combining incompatible physical units.

## Decisión / Decision

Priorizar un piloto en aceitunas, la categoría con mayor costo de merma (CLP 2,984,432). Medir ventas y pérdidas por SKU, registrar motivos y comparar períodos equivalentes. La inversión en congelación y las cantidades de reposición requieren datos adicionales. No hay ahorro real demostrado.

Prioritize an olives pilot, the largest category by waste cost (CLP 2,984,432). Capture dated SKU sales, loss reasons and comparable periods. Freezer investment and order quantities require further inputs. No realized savings are claimed.

Consulte [DECISION_REVIEW.md](DECISION_REVIEW.md) para definiciones, hipótesis y criterios de avance en ambos idiomas.

## Excel y análisis / Workbook and analysis

- [Market_Stall_Management.xlsx](excel/Market_Stall_Management.xlsx): catálogo, proveedores, compras, resultados, ocho gráficos y tabla dinámica nativa. `Decision` presenta el alcance y la recomendación; `Cohort_Pivot` permite explorar resultados por categoría y cierre.
- `data/`: registros simulados originales conservados.
- `analysis_export/reviewed_batch_cohorts.csv`: lotes enlazados y alcance temporal.
- `analysis_export/reviewed_category_economics.csv`: rentabilidad y merma monetaria.
- `analysis_export/review_metrics.json`: conciliaciones y métricas.
- `notebooks/`: análisis Python y SQL anteriores, con advertencia de revisión.
- `ASSUMPTIONS.md`: hipótesis de simulación. La conversión de 935 CLP/USD es ilustrativa.

Para actualizar el análisis revisado, ejecutar `python scripts/review_projects.py` (pandas). En Excel, actualizar las tablas dinámicas después de cambiar datos. No usar los antiguos EOQ, payback o pronósticos de compras como política validada de demanda.

Run `python scripts/review_projects.py` to rebuild reviewed exports. Refresh PivotTables after editing Excel data. Legacy EOQ, payback and purchase forecasts are illustrative, not validated demand policies.
