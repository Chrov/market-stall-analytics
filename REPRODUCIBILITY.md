# Reproducir / Reproduce

Python con pandas. Desde la raíz / from the repository root:

```bash
pip install pandas
python scripts/review_projects.py
```

El script concilia los CSV originales y regenera `analysis_export`. El Excel usa fórmulas y tabla dinámica nativa: actualizar la tabla dinámica tras editar tablas. El script no reconstruye el diseño del Excel. Los reportes y Power BI publicados son snapshots revisados; regenerar sus agregados antes de actualizar visuales. No sobrescribir documentación con conclusiones heredadas.

The script reconciles original CSVs and rebuilds analytical exports. Refresh the native Excel PivotTable after changing tables. The script does not recreate workbook styling. Reports and Power BI are reviewed snapshots; regenerate aggregates before refreshing visuals. Legacy notebooks are exploratory and do not supersede DECISION_REVIEW.
