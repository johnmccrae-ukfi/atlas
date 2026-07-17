# Atlas Enterprise AI Intelligence Platform

# Release History

This document summarises the evolution of the Atlas Enterprise AI Intelligence Platform from the initial project foundation through the v1.0.0 Minimum Viable Product (MVP) and subsequent platform releases.

The project has been developed incrementally using a milestone-based approach, with each release introducing a clearly defined architectural capability.

---

# v1.3.0 — Multi-Instrument Architecture

**Release Date:** July 2026  
**Status:** Implementation complete; release consolidation in progress

Introduced Atlas’s first governed multi-instrument historical architecture.

This milestone expands Atlas beyond the original CQG historical dataset by adding a second provider-specific Lakehouse pathway for Massive Futures historical minute aggregates.

The implemented historical architecture now includes:

```text
CQG legacy Futures events
→ CQG Bronze
→ silver_cqg_ticks
→ CQG minute and daily Gold candles
```

and:

```text
Massive Futures Flat Files
→ bronze_massive_futures_minute_aggregates
→ silver_massive_futures_minute_aggregates
→ Massive minute and daily Gold candles
```

Both historical paths are exposed through the existing Direct Lake semantic model while retaining separate physical fact tables appropriate to their different source grains and activity semantics.

Highlights:

- Massive Futures historical Flat File discovery and controlled ingestion
- Azure Key Vault-backed provider credentials
- Initial governed contracts:
  - `MESU6`
  - `MNQU6`
- Stable Atlas product and contract keys
- Provider-neutral contract business identity
- New governed instrument dimension:
  - `gold_dim_instrument`
- New Massive historical tables:
  - `bronze_massive_futures_minute_aggregates`
  - `silver_massive_futures_minute_aggregates`
  - `gold_massive_futures_minute_candles`
  - `gold_massive_futures_daily_candles`
- New Fabric notebooks for:
  - instrument-dimension generation;
  - Massive Bronze ingestion;
  - Massive Silver validation and enrichment;
  - Massive Gold candle generation.
- Expansion of `sm_atlas_gold_reporting` from three to six tables
- New Date relationships to both Massive fact tables
- New Instrument relationships to both Massive fact tables
- Guarded daily and intraday price measures
- Massive activity measures for:
  - Volume;
  - Transactions;
  - Dollar Volume;
  - minute-bar counts.
- Governed measure display folders
- Hidden technical relationship and provider fields
- Deterministic contract display ordering
- New development semantic-model validation report:
  - `rpt_atlas_semantic_model_validation_dev`
- Updated public README and architecture visuals

Controlled validation results:

```text
Massive Bronze rows:
2,760

Massive Silver rows:
2,760

Massive Gold minute rows:
2,760

Massive Gold daily rows:
2
```

Per-contract coverage:

```text
MESU6:
1,380 minute rows

MNQU6:
1,380 minute rows
```

Controlled session:

```text
TradingDate:
2026-07-14

Session start:
2026-07-13 22:00:00 UTC

Session end:
2026-07-14 20:59:00 UTC
```

Semantic-model validation confirmed:

- active one-to-many Date relationships;
- active one-to-many Instrument relationships;
- single-direction filtering;
- consistent daily and intraday contract filtering;
- correct `MESU6` results;
- correct `MNQU6` results;
- blank guarded price measures under zero or multiple contract selections;
- preserved CQG relationships and measures.

Validated `MESU6` values:

```text
Open:      7,558.25
High:      7,613.75
Low:       7,531.75
Close:     7,590.50
Return:    0.43%
Range:     82.00
Volume:    958,226
```

Validated `MNQU6` values:

```text
Open:      29,440.00
High:      29,922.00
Low:       29,303.25
Close:     29,794.75
Return:    1.20%
Range:     618.75
Volume:    2,726,737
```

The release preserves:

- the validated CQG historical path;
- deterministic CQG event ordering;
- `Decimal(18,5)` OHLC precision;
- `gold_dim_date`;
- existing CQG selected-period and previous-trading-day measures;
- the existing five-trading-day moving average;
- the separate v1.1.0 Eventstream and Eventhouse pathway.

Current limitations:

- Massive historical coverage currently includes one controlled trading session
- Only `MESU6` and `MNQU6` are included
- Multiple contract months and expired contract chains are not yet modelled
- Automatic Futures rollover is not implemented
- Continuous contracts are not implemented
- CQG facts are not yet mapped into `gold_dim_instrument`
- Massive and CQG facts remain physically separate
- Historical and near-real-time Massive data are not reconciled
- Provider correction precedence is not yet defined
- Streaming Silver and Gold models are not implemented
- Production orchestration and incremental historical loading remain future work
- Hosted AI inference remains environment-limited

---

# v1.2.0 — Reporting Navigation and Time Intelligence

**Release Date:** July 2026

Introduced a governed date dimension, reusable time-intelligence measures, and a more consistent historical reporting experience.

This milestone strengthens the existing Direct Lake reporting architecture without redesigning the underlying Bronze, Silver, or Gold candle pipelines.

The historical reporting path now includes:

```text
gold_dim_date
→ Direct Lake relationships
→ shared daily and intraday filtering
→ reusable selected-period measures
→ previous-trading-day comparisons
→ improved report navigation and KPI presentation
```

Highlights:

- New governed Gold date dimension:
  - `gold_dim_date`
  - one row per calendar date
  - dynamic minimum-to-maximum Gold date range
  - continuous date coverage including weekends
  - deterministic year, quarter, month, weekday, and sort attributes
- New Fabric notebook:
  - `nb_gold_dim_date`
  - dynamic Gold date-range discovery
  - continuous calendar generation
  - pre-write and persisted-table validation
  - relationship-key validation
- New Direct Lake relationships from `gold_dim_date` to:
  - daily candle data
  - minute candle data
- Shared Date filtering across Market Overview and Intraday Analysis
- Reusable selected-period measures for:
  - Open
  - High
  - Low
  - Close
  - Range
  - Range percentage
  - Return percentage
- Reusable trading-day measures for:
  - selected trading date
  - previous trading date
  - selected trading-day close
  - previous trading-day close
  - absolute trading-day change
  - percentage trading-day change
- Multi-instrument-safe distinct Trading Days measure
- Preserved five-trading-day moving average
- Explicit page-navigation controls between Market Overview and Intraday Analysis
- Consistent KPI-card styling and spacing across both report pages
- Updated Gold layer contract and validation rules

Validation results:

- 30 continuous calendar rows generated from `2012-03-01` through `2012-03-30`
- No null or duplicate Date values
- No unmatched daily or minute candle trading dates
- No null candle `TradingDate` values
- Active one-to-many, single-direction relationships confirmed
- Daily and intraday report filtering confirmed
- Expected weekend behaviour confirmed
- Selected-period Open confirmed as `1.33550`
- Selected-period Close confirmed as `1.33460`
- Selected-period Return confirmed as approximately `-0.07%`
- Selected-period Range confirmed as `0.03830`
- Selected-period Range percentage confirmed as approximately `2.87%`
- Trading Days confirmed as `26`
- Previous trading-day close confirmed as `1.33610`
- Selected trading-day close confirmed as `1.33460`
- Trading Day Change confirmed as `-0.00150`
- Trading Day Change percentage confirmed as approximately `-0.11%`
- Moving-average behaviour confirmed after report refresh
- Page navigation confirmed in edit and reading modes

Current limitations:

- The date dimension currently spans only the governed date range present in the current Gold candle tables
- Formal exchange calendars and holiday classifications are not implemented
- `IsTradingDay` is not inferred from historical candle presence
- Multi-instrument filtering and instrument dimensions remain part of `v1.3.0`
- Daily-to-intraday drill-through was evaluated but deferred
- The current free candlestick custom visual does not expose compatible Power BI drill-through context
- Explicit page navigation is used instead of candle-level drill-through
- Historical Lakehouse reporting remains separate from the near-real-time Eventhouse pathway

---

# v1.1.0 — Near-Real-Time Market Data Foundation

**Release Date:** July 2026

Introduced Atlas’s first governed near-real-time futures market-data pathway.

This milestone extends the historical Lakehouse architecture with a controlled Microsoft Fabric Real-Time Intelligence vertical slice:

```text
Massive delayed Futures WebSocket
→ Atlas Python streaming adapter
→ Microsoft Fabric Eventstream
→ Eventhouse and KQL Database
→ raw futures minute aggregates
→ KQL validation
→ Real-Time Dashboard
```

Highlights:

- Massive Futures contract discovery and REST aggregate diagnostics
- Delayed Futures WebSocket authentication and subscription
- Initial `AM.MESU6` minute-aggregate stream
- Atlas streaming event-envelope transformation
- Required-field, timestamp, interval, OHLC, and measure validation
- Deterministic Atlas event identifiers
- Raw Massive provider-payload preservation
- Event Hubs-compatible Fabric Eventstream publishing
- Fabric Eventstream custom endpoint ingestion
- Eventhouse direct ingestion
- Governed KQL table schema
- Explicit JSON ingestion mapping
- KQL validation, monitoring, and dashboard-source queries
- Live-refreshing Real-Time Dashboard
- Close-price and volume visualisation
- Near-real-time architecture documentation
- Development-hosted local streaming adapter

Validation results:

- Successful Massive WebSocket connection and authentication
- Successful subscription to `AM.MESU6`
- Genuine delayed minute-aggregate receipt
- Successful Eventstream publication
- Successful Eventhouse ingestion
- No duplicate live Atlas event identifiers
- 60-second continuity while the local adapter was active
- No invalid OHLC or negative-measure rows
- Preserved nested raw provider payload
- Average provider delay of approximately 603.9 seconds
- Average Fabric ingestion latency of approximately 0.47 seconds
- Automatic Real-Time Dashboard refresh confirmed

Current limitations:

- The streaming adapter must currently run locally
- Scope is limited to delayed `AM.MESU6` minute aggregates
- Automatic futures contract rollover is not implemented
- Durable buffering, replay, correction handling, and destination-level deduplication remain future work
- Historical Lakehouse and near-real-time Eventhouse pathways remain intentionally separate
- Production cloud hosting is deferred to a later release

---

# v1.0.0 — Atlas Enterprise AI Intelligence Platform MVP

**Release Date:** July 2026

The first complete portfolio release of Atlas.

This milestone delivers an end-to-end Microsoft Fabric Data Engineering and AI platform demonstrating:

- Microsoft Fabric Lakehouse
- Bronze, Silver and Gold Medallion Architecture
- AI Intelligence Layer
- Provider-agnostic AI abstraction
- Microsoft Fabric AI integration
- Direct Lake Semantic Model
- Interactive Power BI reporting
- Professional GitHub workflow
- Comprehensive engineering documentation

---

# v0.9.1 — Fabric AI Provider Integration

Implemented the Microsoft Fabric AI Provider abstraction layer.

Highlights:

- Provider abstraction interface
- Fabric AI implementation
- Structured inference metadata
- Graceful AI failure handling
- Gold AI commentary persistence
- Support for future AI provider expansion

---

# v0.9.0 — AI Market Commentary Framework

Introduced the enterprise AI Intelligence layer.

Highlights:

- Prompt generation
- Session summary generation
- AI commentary framework
- Prompt templates
- AI-ready Gold datasets
- Separation of deterministic analytics from AI inference

---

# v0.8.0 — AI Trading Intelligence Foundation

Established the architectural foundation for AI integration.

Highlights:

- AI architecture
- Feature engineering
- Session classification
- Volatility analytics
- Activity bands
- AI-ready Gold layer outputs

---

# v0.7.0 — Trading Analytics & Report UX

Extended the Power BI reporting experience.

Highlights:

- Improved report design
- Enhanced user experience
- Additional KPIs
- Improved navigation
- Interactive analytics

---

# v0.6.0 — Interactive Trading Dashboard

Delivered the first interactive reporting solution.

Highlights:

- Direct Lake Semantic Model
- Power BI dashboard
- Candlestick chart
- KPI cards
- Date filtering
- Instrument selection

---

# v0.5.0 — Reporting Foundation

Created the reporting layer.

Highlights:

- Gold semantic model
- Power BI foundation
- Report architecture
- Reporting standards

---

# v0.4.0 — Gold Analytics

Introduced curated analytical datasets.

Highlights:

- Minute OHLC candles
- Daily OHLC candles
- Gold analytics tables
- Market aggregation
- Derived metrics

---

# v0.3.0 — Silver Layer

Implemented business-ready transformations.

Highlights:

- Data cleansing
- Tick normalisation
- Schema standardisation
- Quality validation

---

# v0.2.0 — Bronze Layer

Implemented raw data ingestion.

Highlights:

- CQG legacy data ingestion
- Delta storage
- Immutable raw data
- Bronze Lakehouse tables

---

# v0.1.0 — Foundation

Initial project setup.

Highlights:

- Repository creation
- GitHub integration
- Microsoft Fabric workspace
- Project structure
- Python solution
- Development workflow

---

# Development Philosophy

Atlas has been developed using an incremental engineering approach.

Each release introduces a self-contained architectural capability while preserving the integrity of previous work.

The project deliberately separates:

- Data ingestion
- Data engineering
- Analytics
- Artificial Intelligence
- Reporting
- Documentation

This enables the platform to evolve in a controlled, enterprise-style manner while maintaining a clean and understandable architecture.

---

# Looking Ahead

Following the v1.3.0 Multi-Instrument Architecture release, the next planned phase is:

> **v1.4.0 — Production-Style AI Inference**

Planned focus includes:

- Azure AI Foundry or Azure OpenAI integration;
- secure provider configuration;
- prompt versioning;
- structured model outputs;
- inference logging;
- provider and model traceability;
- validation and fallback behaviour;
- cost and capacity awareness;
- multi-instrument commentary built from trusted Gold analytics.

Later Real-Time Intelligence work may include:

- production-style streaming hosting;
- multiple simultaneous instruments;
- resilient WebSocket recovery;
- durable buffering and replay;
- duplicate and correction handling;
- streaming Silver and Gold models;
- governed contract rollover;
- Real-Time Dashboard expansion;
- alerts and Fabric Activator;
- historical and streaming reconciliation;
- operational monitoring and deployment controls.

Atlas will continue to evolve through small, governed releases rather than broad unsupported claims.

---

**Current Stable Release**

**v1.2.0 — Reporting Navigation and Time Intelligence**

**Current Development Release**

**v1.3.0 — Multi-Instrument Architecture**