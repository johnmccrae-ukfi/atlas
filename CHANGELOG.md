# Changelog

All notable changes to the Atlas Enterprise AI Intelligence Platform are documented in this file.

The format is based on the principles of **Keep a Changelog**, with releases organised by version.

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