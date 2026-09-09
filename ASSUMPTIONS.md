# Supuestos de la simulación / Simulation assumptions

El caso representa 3,825 lotes comprados entre julio de 2023 y junio de 2025. Sus cierres llegan hasta 2035: no representa dos años de ventas observadas. Catálogo, proveedores, transacciones y resultados son material de portafolio simulado. No hay una inversión en congelación ni mejoras comerciales verificadas.

The case contains synthetic purchase cohorts, not observed business transactions. Purchase dates and closure dates have different meanings. No freezer purchase or realized commercial improvements have been verified.

## Moneda y precios / Currency and prices

- Moneda principal: CLP. La conversión fija 935 CLP/USD es ilustrativa, sin fuente que la valide como cotización observada.
- Redondeo de precios, márgenes por categoría y recargos de proveedor son parámetros del generador, no cotizaciones profesionales verificadas.
- CLP is the reporting currency. The legacy fixed USD conversion is an illustrative assumption, not an observed exchange-rate claim. Prices and margins are synthetic parameters.

## Generación / Generation

Los parámetros heredados incluyen multiplicadores estacionales de 1.6/0.6, incrementos de septiembre/diciembre de 25%/30%, crecimiento simulado de 8% y factores de calor para pérdidas. Describen reglas del generador, no efectos medidos ni causalidad. El crecimiento no demuestra el beneficio de modernizar medios de pago. Vida útil y vencimientos son supuestos; validar aptitud del producto antes de cualquier prueba de conservación.

Legacy seasonal, holiday, growth and spoilage factors are generator assumptions, not measured business effects. Shelf life is unvalidated. A synthetic growth factor cannot prove a modernization benefit.

## Inventario / Inventory

Las compras no son demanda observada. High/Medium/Low no es stock numérico. Los EOQ, puntos de reorden y stocks de seguridad heredados usan compras y supuestos de costos, por lo que no están validados para emitir pedidos. Faltan posición de inventario, faltantes, ventas fechadas, tránsito, restricciones y lead times observados.

Purchase history is not observed demand. Qualitative stock labels only trigger a count. Legacy EOQ and safety-stock values are illustrative; they cannot support actual orders without validated inventory and supplier inputs.

## Inversión y pronóstico / Investment and forecasting

Los escenarios de prevención de merma y precios de congeladores heredados no tienen cotizaciones o efectos observados que los respalden. Evaluar inversión solo con producto apto, ahorro incremental, capacidad, energía y mantenimiento verificados. El pronóstico anterior de compras suma unidades incompatibles: no se presenta como precisión válida de demanda.

Legacy freezer scenarios are unvalidated assumptions, not a business case. The previous aggregate purchase forecast combines incompatible units and is not valid demand evidence. The current recommendation and monetary measures are documented in DECISION_REVIEW.md.
