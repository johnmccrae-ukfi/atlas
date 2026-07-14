# Changelog

All notable changes to the Atlas Enterprise AI Intelligence Platform are documented in this file.

The format is based on the principles of **Keep a Changelog**, with releases organised by version.

---

# v1.2.0 — Reporting Navigation and Time Intelligence

## Added

- Governed Gold date dimension:
  - `gold_dim_date`
  - one row per calendar date
  - dynamically generated from the minimum and maximum Gold `TradingDate`
  - continuous date coverage including weekends
  - year, quarter, month, weekday and chronological sort attributes
- Fabric notebook:
  - `nb_gold_dim_date`
  - dynamic Gold date-range discovery
  - continuous calendar generation
  - pre-write and persisted-table validation
  - relationship-key validation against daily and minute candle tables
- Direct Lake semantic-model relationships:
  - `gold_dim_date[Date]` to daily candles
  - `gold_dim_date[Date]` to minute candles
- Reusable selected-period measures:
  - `Selected Period Open`
  - `Selected Period High`
  - `Selected Period Low`
  - `Selected Period Close`
  - `Selected Period Return %`
- Reusable trading-day time-intelligence measures:
  - `Selected Trading Date`
  - `Previous Trading Date`
  - `Selected Trading Day Close`
  - `Previous Trading Day Close`
  - `Trading Day Change`
  - `Trading Day Change %`
- Explicit report-page navigation between:
  - Market Overview
  - Intraday Analysis
- Trading Days KPI on Market Overview
- Consistent KPI card styling across the two historical report pages

## Changed

- Replaced fact-table date slicer fields with the governed `gold_dim_date[Date]` field
- Standardised semantic-model date formatting to date-only values
- Added chronological sort metadata for:
  - month names
  - abbreviated month names
  - quarter labels
  - weekday names
  - year-month labels
- Hid technical date sort columns from report authors
- Changed `Trading Days` from a fact-row count to a distinct trading-date count, improving future multi-instrument behaviour
- Refactored `Daily Range` to reuse selected-period High and Low measures
- Refactored `Daily Range (%)` to use the selected-period opening price
- Replaced the previous range-based Daily Return calculation with a true selected-period return
- Renamed `Daily Return %` to `Selected Period Return %`
- Retained the proven five-trading-day moving-average implementation after validating custom-visual evaluation behaviour
- Improved Market Overview KPI spacing and visual consistency
- Added compact directional page-navigation controls
- Updated the Gold layer contract to include the governed reporting dimension, relationships, measures and validation rules

## Validation

- Confirmed 30 continuous calendar rows from `2012-03-01` through `2012-03-30`
- Confirmed no null or duplicate Date values
- Confirmed minimum and maximum date alignment with governed Gold data
- Confirmed weekend classification
- Confirmed zero unmatched daily candle trading dates
- Confirmed zero unmatched minute candle trading dates
- Confirmed zero null trading dates in both candle tables
- Confirmed active one-to-many, single-direction relationships from `gold_dim_date`
- Confirmed shared Date filtering on Market Overview and Intraday Analysis
- Confirmed expected blank report behaviour for calendar dates with no market data
- Confirmed artificial slicer blank members can be excluded without removing weekends
- Confirmed selected-period calculations:
  - Open: `1.33550`
  - Close: `1.33460`
  - Return: approximately `-0.07%`
  - Range: `0.03830`
  - Range percentage: approximately `2.87%`
- Confirmed distinct Trading Days count of `26`
- Confirmed previous trading-day close of `1.33610`
- Confirmed selected trading-day close of `1.33460`
- Confirmed Trading Day Change of `-0.00150`
- Confirmed Trading Day Change percentage of approximately `-0.11%`
- Confirmed the five-day moving-average line remained correct after refresh
- Confirmed page navigation in edit and reading modes
- Confirmed both report pages respond correctly after semantic-model refresh

## Known Limitations

- The date dimension currently spans only the minimum-to-maximum date range present in the governed Gold candle tables
- Formal exchange calendars and holiday classifications are not implemented
- `IsTradingDay` is not inferred from historical candle presence
- Multi-instrument date and instrument filtering will be expanded in `v1.3.0`
- Daily-to-intraday drill-through was evaluated but deferred
- The current free candlestick custom visual does not expose a selected candle as compatible Power BI drill-through context
- Explicit page navigation is used instead of candle-level drill-through
- The historical Lakehouse reporting path remains separate from the v1.1.0 near-real-time Eventhouse path

---

# v1.1.0 — Near-Real-Time Market Data Foundation

## Added

- Massive Futures contract discovery utility
- Massive delayed Futures REST aggregate diagnostics
- Massive delayed Futures WebSocket authentication and subscription testing
- Support for the `AM.MESU6` minute-aggregate subscription
- Atlas Massive Futures minute-aggregate transformer
- Required-field, timestamp, interval, OHLC, and non-negative measure validation
- Deterministic Atlas streaming event identifiers
- Raw Massive provider payload preservation
- Fabric Eventstream writer using the Event Hubs-compatible custom endpoint
- End-to-end local Python streaming adapter
- One-event Fabric Eventstream diagnostic sender
- Microsoft Fabric Eventstream:
  - `es_atlas_massive_futures_dev`
  - `src_atlas_massive_futures`
  - `dest_atlas_massive_futures_raw`
- Microsoft Fabric Eventhouse:
  - `eh_atlas_realtime_dev`
- Raw KQL table:
  - `raw_massive_futures_minute_aggregates`
- Explicit JSON ingestion mapping:
  - `raw_massive_futures_minute_aggregates_json_mapping`
- Reusable KQL validation, monitoring, and dashboard-source queries
- Real-Time Dashboard:
  - `rtd_atlas_massive_futures_dev`
  - recent MESU6 minute-aggregate table
  - delayed close-price line chart
  - delayed volume column chart
  - live refresh
- Near-real-time market-data architecture documentation
- Fabric Eventstream and Eventhouse configuration variables in `.env.example`
- Azure Event Hubs Python dependency

## Changed

- Extended Atlas from a historical-only analytics platform to include a governed near-real-time ingestion pathway
- Updated the Atlas master context with the implemented v1.1.0 architecture and asset inventory
- Updated Python dependency management for Fabric Eventstream publishing
- Updated environment configuration to support Massive Futures and Fabric Eventstream connectivity
- Standardised streaming timestamps on UTC while preserving provider epoch-millisecond values
- Separated provider WebSocket handling, Atlas transformation, and Fabric delivery responsibilities
- Adopted explicit KQL schema governance instead of automatic schema inference
- Enabled ingestion-aware live refresh for the Real-Time Dashboard

## Validation

- Confirmed successful Massive Futures WebSocket connection and authentication
- Confirmed successful subscription to `AM.MESU6`
- Confirmed genuine delayed minute-aggregate receipt
- Confirmed successful publication through Fabric Eventstream
- Confirmed successful direct ingestion into Eventhouse
- Confirmed exact KQL schema and decimal handling
- Confirmed nested raw provider payload preservation
- Confirmed no duplicate live Atlas event identifiers
- Confirmed 60-second continuity while the local adapter was running
- Confirmed no invalid OHLC or negative-measure rows
- Confirmed automatic Real-Time Dashboard refresh after Eventhouse ingestion
- Observed average provider delay of approximately 603.9 seconds
- Observed average Fabric ingestion latency of approximately 0.47 seconds
- Observed average end-to-end latency of approximately 604.4 seconds

## Known Limitations

- The streaming adapter is development-hosted and must currently run locally
- Only delayed `AM.MESU6` minute aggregates are supported
- Automatic futures contract rollover is not implemented
- Durable buffering and replay are not implemented
- Duplicate suppression is validated but not enforced at the destination
- Provider correction handling is not implemented
- Advanced WebSocket reconnect and recovery behaviour remains future work
- Production cloud hosting and managed secret integration are deferred
- Historical Lakehouse and near-real-time Eventhouse pathways remain intentionally separate
- Streaming Silver and Gold models are not yet implemented

---

# v1.0.0 — Atlas Enterprise AI Intelligence Platform MVP

## Added

- Professional GitHub repository landing page
- Comprehensive installation guide (`INSTALLATION.md`)
- Curated Python dependency management (`requirements.txt`)
- Release history documentation
- Enterprise architecture documentation
- AI architecture documentation
- Professional architecture diagrams
- GitHub development workflow documentation
- Project screenshots and visual assets
- Portfolio-oriented repository structure

## Changed

- README completely redesigned as the project landing page
- Project branding updated to **Atlas Enterprise AI Intelligence Platform**
- Documentation standardised across the repository
- Architecture diagrams aligned with the implemented solution
- Repository prepared for public portfolio release

## Known Limitations

- Microsoft Fabric Trial capacities currently do not support AI Functions
- AI inference metadata is captured correctly despite Trial capacity restrictions

---

# v0.9.1 — Fabric AI Provider Integration

## Added

- Microsoft Fabric AI Provider implementation
- Provider abstraction layer
- AI inference metadata capture
- AI failure handling
- AI provider configuration
- Commentary persistence

## Changed

- AI architecture updated to support future provider expansion

---

# v0.9.0 — AI Market Commentary Framework

## Added

- AI commentary notebook
- Prompt generation
- Session summary generation
- Commentary storage
- AI Gold tables

---

# v0.8.0 — AI Trading Intelligence Foundation

## Added

- AI Intelligence architecture
- Feature engineering
- Market session analytics
- Volatility metrics
- Activity bands

---

# v0.7.0 — Trading Analytics & Report UX

## Added

- Enhanced Power BI user experience
- Additional analytics
- Improved report navigation

## Changed

- Dashboard layout
- Report usability

---

# v0.6.0 — Interactive Trading Dashboard

## Added

- Direct Lake Semantic Model
- Interactive Power BI report
- Candlestick visualisation
- KPI cards
- Date filtering

---

# v0.5.0 — Reporting Foundation

## Added

- Reporting architecture
- Semantic model
- Power BI reporting foundation

---

# v0.4.0 — Gold Analytics

## Added

- Minute OHLC candle generation
- Daily OHLC candle generation
- Gold analytics tables
- Derived market metrics

---

# v0.3.0 — Silver Layer

## Added

- Standardised tick processing
- Data quality validation
- Business transformations

---

# v0.2.0 — Bronze Layer

## Added

- CQG legacy file ingestion
- Bronze Delta tables
- Metadata enrichment
- Source provenance
- Event ordering

## Changed

- Development workflow standardised around GitHub `dev` branch
- Bronze layer preserves complete source lineage

---

# v0.1.0 — Foundation

## Added

- Initial repository
- Project structure
- Microsoft Fabric workspace
- GitHub integration
- Python solution
- Development workflow