"""Reproducible review of the supplied project snapshots; source CSVs stay intact."""
from pathlib import Path
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
p=Path(__file__).resolve().parents[1]
if not (p/'data/batch_outcomes.csv').exists():p=ROOT/'market-stall-analytics-main'
b=pd.read_csv(p/'data/batch_outcomes.csv'); u=pd.read_csv(p/'data/purchases.csv')
m=b.merge(u[['BatchID','ProductID','UnitCost_CLP','Quantity','PurchaseDate','Unit']],on='BatchID',suffixes=('','_purchase'),validate='one_to_one')
assert (m.ProductID==m.ProductID_purchase).all()
assert (b.BatchID.to_numpy()==u.BatchID.to_numpy()).all(), 'Workbook pairwise formulas require matched row order'
assert ((m.QtyPurchased-m.QtySold-m.QtyWasted).abs()<.011).all()
assert ((u.Quantity*u.UnitCost_CLP-u.BatchCost_CLP).abs()<=1).all()
assert ((b.Revenue_CLP-b.BatchCost_CLP-b.GrossProfit_CLP).abs()<=1).all()
m['WasteCost_CLP']=m.QtyWasted*m.UnitCost_CLP
m['ClosureScope']=m.CloseDate.le('2025-06-30').map({True:'Closed by cutoff',False:'After cutoff'})
m['PurchaseCohort']=m.PurchaseDate.str[:7]
out=p/'analysis_export';out.mkdir(exist_ok=True)
m.to_csv(out/'reviewed_batch_cohorts.csv',index=False)
g=m.groupby('Category').agg(revenue_clp=('Revenue_CLP','sum'),gross_profit_clp=('GrossProfit_CLP','sum'),purchase_cost_clp=('BatchCost_CLP','sum'),waste_cost_clp=('WasteCost_CLP','sum'))
g['gross_margin']=g.gross_profit_clp/g.revenue_clp
g['waste_cost_rate']=g.waste_cost_clp/g.purchase_cost_clp
g.sort_values('waste_cost_clp',ascending=False).to_csv(out/'reviewed_category_economics.csv')
metrics={'batch_count':len(m),'future_closures':int((m.ClosureScope=='After cutoff').sum()),'latest_close_date':m.CloseDate.max(),'cohort_revenue_clp':int(m.Revenue_CLP.sum()),'closed_by_cutoff_revenue_clp':int(m.loc[m.ClosureScope=='Closed by cutoff','Revenue_CLP'].sum()),'cohort_gross_profit_clp':int(m.GrossProfit_CLP.sum()),'waste_cost_clp':float(m.WasteCost_CLP.sum()),'waste_cost_rate':float(m.WasteCost_CLP.sum()/m.BatchCost_CLP.sum()),'checks':'unique batch joins, matching product/order, quantity conservation, purchase cost and gross profit reconciliation passed'}
(out/'review_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
memo='''# Revisión de decisión / Decision review

## ES

**Propósito:** priorizar reducción de merma y mejorar el control de reposición en un puesto de feria. Todos los datos son simulados. El análisis permite diseñar un piloto, sin atribuir ahorros reales a una empresa.

Se conservaron los 3.825 lotes originales: cantidades, costo y utilidad cuadran. El problema principal es temporal: 498 cierres ocurren después del 30 de junio de 2025 y llegan hasta 2035. Los CLP 412.926.945 corresponden al resultado completo de las cohortes compradas entre julio de 2023 y junio de 2025, no a ventas realizadas durante ese período. Los lotes cerrados hasta el corte suman CLP 366.555.045 de ingresos de lote; tampoco son ventas diarias porque no existen fechas de venta. No se inventaron fechas ni se eliminaron lotes para mejorar indicadores.

La merma valorada al costo de adquisición es CLP 8.992.168 (2,90% del costo comprado), sobre todas las cohortes. Permite agregar productos con unidades distintas. El antiguo 3,4% mezclaba kg, frascos y paquetes. El margen bruto agregado es 25,03%; el promedio del margen del catálogo no mide rentabilidad realizada. Ambos son resultados simulados de cohortes.

**Decisión:** iniciar un piloto de control de merma en aceitunas (CLP 2.984.432 de costo de merma de cohortes, el mayor por categoría), seguido de frutos secos y granos. Registrar durante al menos un ciclo de reposición comparable: fecha de venta, SKU, unidad, cantidad, merma y motivo, inventario contado, entradas y costo. Comparar costo de merma por kg comprado, margen y faltantes con períodos equivalentes. El diseño debe controlar estacionalidad y mezcla de productos.

**Congelador:** no aprobar la compra con el antiguo payback. La fracción de merma evitable, aptitud de cada producto, electricidad, mantenimiento y capacidad no están observadas. Beneficio incremental mensual = costo de merma elegible evitado menos costos operativos adicionales. Payback = inversión / beneficio mensual positivo. Obtener cotizaciones gratuitas y medir el piloto antes de completar esos parámetros. El costo histórico de merma no es automáticamente ahorro recuperable.

**Reposición:** High/Medium/Low es una alerta para contar inventario, no una orden. Faltan inventario numérico, tránsito, pedidos comprometidos, ventas diarias, vida útil remanente y restricciones de proveedor. Una política debe usar posición de inventario = disponible + tránsito − compromisos, y limitar compras por vida útil. El pronóstico de compras no valida demanda; EOQ y stock de seguridad derivados de compras siguen siendo ilustrativos.

El tipo de cambio 935 CLP/USD es una hipótesis ilustrativa sin verificación como cotización observada. Priorizar CLP. Los análisis anteriores de notebooks y documentos deben leerse con estas correcciones; no constituyen evidencia de impacto realizado.

## EN

**Purpose:** prioritize waste reduction and improve replenishment control for a simulated market stall. All 3,825 source batches are retained and quantities, purchase costs and gross profit reconcile. There are 498 closures after 2025-06-30, extending to 2035. CLP 412,926,945 is full purchase-cohort revenue, not revenue earned within two years. Batches closed by the cutoff total CLP 366,555,045; these are batch outcomes, not dated daily sales.

Acquisition-cost waste totals CLP 8,992,168, or 2.90% of purchase cost. This monetary denominator avoids adding kilograms, jars and packs. Aggregate gross margin is 25.03%. Prioritize an olives waste pilot (CLP 2,984,432 cohort waste cost), then nuts and grains. Capture dated sales, waste reasons, counted stock and receipts. Compare waste cost per kilogram purchased, gross margin and stockouts over comparable replenishment cycles, controlling seasonality and product mix.

Do not approve freezer investment from the previous payback estimate. Establish product eligibility, incremental avoided waste, energy, maintenance and capacity first. Payback requires positive incremental monthly benefit. Qualitative stock labels only trigger physical counts. Replenishment quantities require inventory position, actual daily demand, shelf life and supplier constraints. Purchase forecasts are not demand validation. The 935 CLP/USD conversion is illustrative. Legacy notebooks and the memoir need this qualification; no realized business savings have been established.
'''
(p/'DECISION_REVIEW.md').write_text(memo,encoding='utf-8')
for path in [p/'README.md',p/'ASSUMPTIONS.md']:
 text=path.read_text(encoding='utf-8')
 notice='> **Revisión 2026-09-08:** Consulte [DECISION_REVIEW.md](DECISION_REVIEW.md). Las cifras siguientes son resultados de cohortes simuladas, con cierres hasta 2035. El payback y la reposición no están validados para operación real. / See the corrected decision review before using legacy results.\n\n'
 if not text.startswith('> **Revisión'):path.write_text(notice+text,encoding='utf-8')
for path in (p/'notebooks').glob('*.ipynb'):
 n=json.loads(path.read_text(encoding='utf-8'))
 warning='Revisión metodológica / Method review: ver ../DECISION_REVIEW.md. Cierres hasta 2035; cohortes no equivalen a ventas de dos años. Compras no equivalen a demanda. Ahorros y políticas requieren validación.'
 if not any(warning in ''.join(c.get('source',[])) for c in n['cells']):
  n['cells'].insert(0,{'cell_type':'markdown','metadata':{},'source':[warning]})
  path.write_text(json.dumps(n,ensure_ascii=False,indent=1),encoding='utf-8')
print(json.dumps(metrics,indent=2))
