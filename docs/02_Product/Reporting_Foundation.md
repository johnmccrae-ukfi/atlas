# Atlas Reporting Foundation

## Release

v0.5.0 — Reporting Foundation

## Purpose

The Reporting Foundation release exposes the Gold analytical layer through Power BI.

The objective is to create the first business-facing visualization from the Atlas Medallion Architecture.

## Scope

This release focuses on a first interactive candlestick chart using Gold OHLC candle data.

## Source Tables

Power BI will consume Gold Delta tables from the Fabric Lakehouse:

- gold_cqg_minute_candles
- gold_cqg_daily_candles

## Initial Reporting Dataset

The first report will use:

- gold_cqg_daily_candles

This provides a clear month-level visual using one row per trading day.

## Report Visuals

Initial Power BI report:

- Daily candlestick chart
- Instrument slicer
- Trading date filter
- Trade count context

## Semantic Model Governance

Atlas will treat the semantic model as the governed reporting layer.

KPIs and business measures should be defined centrally in the semantic model rather than recreated independently in individual reports.

Future production versions may use certified semantic models to prevent multiple competing definitions of similar KPIs.

For v0.5.0, the first reporting model will be simple and focused on Gold candle reporting.

## Design Decision

For v0.5.0, Atlas will report directly from the Gold Lakehouse tables.

A dedicated Warehouse may be introduced later if required for:

- star schema modelling
- dimensional conformance
- enterprise semantic model governance
- broader cross-domain analytics

## Out of Scope

The following are out of scope for v0.5.0:

- trading signals
- AI commentary
- forecasting
- backtesting
- strategy performance
- real-time streaming
- custom visuals requiring paid/licensed dependencies unless explicitly approved

## Success Criteria

v0.5.0 is complete when:

1. Power BI can access the Gold tables.
2. A semantic model exists for Gold candle reporting.
3. A daily candlestick chart is created.
4. The report supports instrument and date filtering.
5. The report is driven entirely from the Gold layer.

## v0.5.0

Completed the first Direct Lake semantic model and production Power BI report.

Features:
- Direct Lake semantic model
- Reusable DAX measures
- Daily OHLC candlestick chart
- Executive KPI cards
- Display folders
- Column descriptions
- Professional formatting

## v0.7.0 – Trading Analytics and Report UX

This release enhanced the Atlas Power BI reporting layer with improved trading analytics and a cleaner report experience.

### Added

- Added `Session Trade Count` measure to the Minute Candles table.
- Replaced ambiguous `Session Volume` KPI with `Session Trade Count`.
- Added `Daily Range` measure.
- Added `Daily Range %` measure.
- Added `Daily Return %` measure.
- Added `5-Day MA Close` moving average indicator.
- Added moving average trend line to the Daily Candlestick visual.
- Refined Market Overview KPI row:
  - Daily Range
  - Total Trades
  - Daily Return %
- Refined Intraday Analysis KPI row:
  - Last Price
  - Session High
  - Session Low
  - Session Trade Count

### Design Notes

- Drillthrough from the candlestick visual was evaluated but deferred.
- The candlestick visual supports report filtering but does not expose the required categorical context for Power BI drillthrough.
- A shared `DimDate` and `DimInstrument` model will be considered after v1.0.0.