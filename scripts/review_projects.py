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
print(json.dumps(metrics,indent=2))
