# Changelog

All notable changes to the Atlas Enterprise AI Intelligence Platform are documented in this file.

The format is based on the principles of **Keep a Changelog**, with releases organised by version.

---

# v1.3.0 — Multi-Instrument Architecture

**Status:** Implementation complete; release consolidation in progress

## Added

- Massive Futures historical Flat File ingestion through the provider’s S3-compatible endpoint
- Controlled historical scope covering:
  - `MESU6` — Micro E-mini S&P 500 September 2026
  - `MNQU6` — Micro E-mini Nasdaq-100 September 2026
  - trading session ending `2026-07-14`
- Azure Key Vault-backed Massive credentials:
  - Key Vault: `kv-atlas-dev-ukfi`
  - secrets:
    - `massive-s3-access-key`
    - `massive-s3-secret-key`
- Governed Atlas Futures identity model separating:
  - provider;
  - provider ticker;
  - trading venue;
  - product;
  - dated Futures contract;
  - Atlas product identity;
  - Atlas contract identity.
- Stable Atlas product keys:
  - `1001` → `FUT-XCME-MES`
  - `1002` → `FUT-XCME-MNQ`
- Stable Atlas contract keys:
  - `2001` → `FUT-XCME-MES-2026-09`
  - `2002` → `FUT-XCME-MNQ-2026-09`
- Governed Gold instrument dimension:
  - `gold_dim_instrument`
  - one row per governed dated Futures contract
  - provider-neutral contract relationships
  - deterministic contract display ordering
  - validated provider and contract metadata
- Fabric notebook:
  - `nb_atlas_gold_dim_instrument`
  - explicit governed seed mappings
  - contract and product identity validation
  - provider-reference metadata
  - pre-write and persisted-table validation
- Massive historical Bronze table:
  - `bronze_massive_futures_minute_aggregates`
  - one row per physical Massive CSV source row
  - source object and row-level lineage
  - raw provider values preserved
- Fabric notebook:
  - `nb_atlas_bronze_massive_futures_minute_aggregates`
  - Massive Flat File retrieval
  - exchange-wide source-object inspection
  - controlled ticker filtering
  - Azure Key Vault secret retrieval
  - physical source identity validation
- Massive historical Silver table:
  - `silver_massive_futures_minute_aggregates`
  - strongly typed provider-generated minute aggregates
  - Atlas product and contract enrichment
  - UTC minute timestamps
  - provider session-date preservation
  - OHLC and activity validation
  - exact and conflicting duplicate detection
  - physical source lineage retention
- Fabric notebook:
  - `nb_atlas_silver_massive_futures_minute_aggregates`
  - trusted-row quality rules
  - provider-to-contract mapping
  - duplicate and conflict checks
  - pre-write and persisted-table validation
- Massive historical Gold tables:
  - `gold_massive_futures_minute_candles`
  - `gold_massive_futures_daily_candles`
- Fabric notebook:
  - `nb_atlas_gold_massive_futures_candles`
  - reporting-friendly minute projection
  - deterministic daily OHLC generation
  - Volume, Transaction and Dollar Volume aggregation
  - session timestamp derivation
  - minute-to-daily reconciliation
  - persisted-table validation
- Massive Direct Lake semantic-model tables:
  - `gold_massive_futures_daily_candles`
  - `gold_massive_futures_minute_candles`
  - `gold_dim_instrument`
- Four new active semantic-model relationships:
  - `gold_dim_date[Date]` → `gold_massive_futures_daily_candles[TradingDate]`
  - `gold_dim_date[Date]` → `gold_massive_futures_minute_candles[TradingDate]`
  - `gold_dim_instrument[AtlasContractKey]` → `gold_massive_futures_daily_candles[AtlasContractKey]`
  - `gold_dim_instrument[AtlasContractKey]` → `gold_massive_futures_minute_candles[AtlasContractKey]`
- Massive daily semantic-model measures covering:
  - selected-period Open, High, Low and Close;
  - selected-period Return and Range;
  - selected and previous trading dates;
  - selected and previous trading-day Close;
  - trading-day Change and Change percentage;
  - five-trading-day moving average;
  - Volume, Transactions, Dollar Volume and minute-bar activity.
- Massive intraday semantic-model measures covering:
  - Last Price;
  - Session Open, High, Low and Close;
  - Session Change and Range;
  - Volume, Transactions and Dollar Volume;
  - minute-bar count;
  - first and last minute timestamps.
- Governed Massive measure display folders:
  - `Massive\Daily Price`
  - `Massive\Daily Time Intelligence`
  - `Massive\Daily Activity`
  - `Massive\Intraday Price`
  - `Massive\Intraday Activity`
  - `Massive\Intraday Time`
- Single-contract guards for Massive price and point-in-time measures
- Development semantic-model validation report:
  - `rpt_atlas_semantic_model_validation_dev`
- Updated portfolio visuals:
  - `multi_instrument_semantic_model.png`
  - revised `architecture_overview.png`
  - revised `medallion_architecture.png`
- Architecture and contract documentation:
  - `Atlas_Multi_Instrument_Identity_and_Grain_Design.md`
  - `Massive_Futures_Bronze_Contract.md`
  - `Massive_Futures_Silver_Contract.md`
  - `Massive_Futures_Gold_Contract.md`

## Changed

- Extended Atlas historical processing from a single CQG source path to two provider-appropriate historical paths:
  - CQG event-level historical data;
  - Massive provider-generated historical minute aggregates.
- Expanded `sm_atlas_gold_reporting` from three to six tables
- Introduced governed Instrument filtering alongside the existing governed Date filtering
- Retained separate CQG and Massive physical fact tables because their source grains and activity semantics differ
- Preserved the existing CQG historical implementation without adding `AtlasContractKey` to CQG facts
- Preserved the separate v1.1.0 Eventstream and Eventhouse pathway
- Changed the historical reporting architecture from fact-table instrument text filtering to governed Massive contract filtering through `gold_dim_instrument`
- Added deterministic `ContractDisplayName` sorting through `InstrumentSortOrder`
- Hid technical contract, product, provider and load fields from normal report authors
- Prevented price measures from silently combining unrelated Futures contracts
- Retained additive Massive activity behaviour where clearly labelled
- Preserved `Decimal(18,5)` OHLC precision for the selected contracts
- Preserved provider-supplied `session_end_date` as the governed Massive `TradingDate`
- Preserved provider symbols as source attributes rather than canonical relationship keys
- Updated the Atlas Master Context to reflect the completed controlled v1.3.0 implementation
- Rewrote the public README as a shorter, visual-first portfolio landing page
- Moved the strongest Power BI, semantic-model and Real-Time Intelligence visuals closer to the top of the README
- Updated architecture diagrams to show:
  - CQG and Massive historical paths;
  - Massive Real-Time Intelligence;
  - `gold_dim_date`;
  - `gold_dim_instrument`;
  - separate provider-specific facts;
  - Direct Lake and Power BI;
  - environment-limited hosted AI inference.

## Validation

### Source Discovery

- Confirmed all documented Massive Futures Flat File dataset prefixes were listable
- Confirmed the selected CME minute-aggregate object:
  - `us_futures_cme/minute_aggs_v1/2026/07/2026-07-14.csv.gz`
- Confirmed source-object content:
  - `89,951` physical rows
  - `937` unique provider tickers
  - `1,380` `MESU6` rows
  - `1,380` `MNQU6` rows
- Confirmed the source object was exchange-wide rather than instrument-specific
- Confirmed the selected contracts had no conflicting duplicate minute records

### Instrument Dimension

- Confirmed exactly two governed contract rows
- Confirmed unique and non-null:
  - `AtlasContractKey`
  - `AtlasContractBusinessKey`
  - provider and ticker mapping
  - `InstrumentSortOrder`
- Confirmed each contract maps to exactly one product
- Confirmed stable key allocation:
  - `MESU6` → `AtlasContractKey 2001`
  - `MNQU6` → `AtlasContractKey 2002`
- Confirmed trade, settlement and spread tick sizes
- Confirmed first-trade, last-trade and settlement dates
- Confirmed `ContractDisplayName` sorting
- Confirmed technical fields are hidden in the semantic model

### Bronze

- Confirmed `2,760` persisted Bronze rows
- Confirmed:
  - `1,380` `MESU6` rows
  - `1,380` `MNQU6` rows
- Confirmed physical source identity uniqueness using:
  - source provider;
  - source dataset;
  - source object key;
  - source row number.
- Confirmed complete source lineage
- Confirmed no source row was introduced or lost during persistence

### Silver

- Confirmed `2,760` trusted Silver rows
- Confirmed every row maps to one Atlas contract and one Atlas product
- Confirmed valid UTC minute-boundary timestamps
- Confirmed provider session-date preservation
- Confirmed valid OHLC relationships
- Confirmed non-negative Volume, Transactions and Dollar Volume
- Confirmed zero conflicting duplicate business keys for the selected contracts
- Confirmed unique trusted Silver grain
- Confirmed no invalid row entered trusted Silver
- Confirmed persisted row counts and schema

### Gold

- Confirmed `2,760` Massive Gold minute rows
- Confirmed:
  - `1,380` `MESU6` minute rows
  - `1,380` `MNQU6` minute rows
- Confirmed two Massive Gold daily rows
- Confirmed unique minute grain:
  - `AtlasContractKey + MinuteTimestamp`
- Confirmed unique daily grain:
  - `AtlasContractKey + TradingDate`
- Confirmed controlled session:
  - start: `2026-07-13 22:00:00 UTC`
  - end: `2026-07-14 20:59:00 UTC`
  - `TradingDate`: `2026-07-14`
- Confirmed daily Open equals the first chronological minute Open
- Confirmed daily Close equals the last chronological minute Close
- Confirmed daily High and Low reconcile with minute extrema
- Confirmed daily Volume reconciliation
- Confirmed daily Transaction reconciliation
- Confirmed daily Dollar Volume reconciliation
- Confirmed `MinuteBarCount = 1,380` for both contracts
- Confirmed no row was introduced or lost during persistence
- Confirmed `Decimal(18,5)` OHLC precision

### Semantic Model

- Confirmed all four new relationships are:
  - active;
  - one-to-many;
  - single-direction;
  - filtered from the dimension to the fact table.
- Confirmed `gold_dim_date` filters both Massive facts
- Confirmed `gold_dim_instrument` filters both Massive facts
- Confirmed no direct fact-to-fact relationships
- Confirmed existing CQG relationships remain unchanged
- Confirmed `MESU6` and `MNQU6` selection updates both daily and intraday measures consistently
- Confirmed guarded price measures return blank for zero or multiple governed contracts
- Confirmed additive activity measures remain available where appropriate

### Validated MESU6 Results

- Open: `7,558.25`
- High: `7,613.75`
- Low: `7,531.75`
- Close: `7,590.50`
- Return: approximately `0.43%`
- Range: `82.00`
- Session Volume: `958,226`

### Validated MNQU6 Results

- Open: `29,440.00`
- High: `29,922.00`
- Low: `29,303.25`
- Close: `29,794.75`
- Return: approximately `1.20%`
- Range: `618.75`
- Session Volume: `2,726,737`

### Regression

- Confirmed existing CQG fact tables remain unchanged
- Confirmed existing CQG Date relationships remain active
- Confirmed existing selected-period measures remain available
- Confirmed existing previous-trading-day measures remain available
- Confirmed the existing CQG five-trading-day moving average remains unchanged
- Confirmed the v1.1.0 Eventstream and Eventhouse path remains separate
- Confirmed no proprietary Massive market-data files were added to the public repository
- Confirmed no Key Vault secret values were committed or documented

## Known Limitations

- The Massive historical implementation currently covers one controlled trading session
- Only `MESU6` and `MNQU6` are included in the first governed Massive historical scope
- Multiple contract months and expired contract chains are not yet implemented
- Automatic Futures contract rollover is not implemented
- Continuous contracts are not implemented
- Massive provider correction precedence is not defined
- Broader exchange-wide data is inspected but not persisted
- `Decimal(18,5)` is validated only for the selected contracts and is not approved universally across all Futures products
- Currency and contract multiplier are not yet present in `gold_dim_instrument`
- Massive numeric exchange-code mapping is not yet governed
- CQG facts are not yet mapped into `gold_dim_instrument`
- CQG and Massive facts remain physically separate
- The historical and near-real-time Massive paths are not reconciled
- The Eventhouse pathway does not yet use `AtlasContractKey`
- Streaming Silver and Gold tables are not implemented
- Previous-trading-day Massive measures remain blank with one available session
- `Massive 5-Day MA Close` currently averages the available one-session history
- The semantic-model validation report remains a temporary development asset pending a release-retention decision
- Production orchestration, incremental historical loading and partitioning remain future work
- Hosted production-style AI inference remains environment-limited

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