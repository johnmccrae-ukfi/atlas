# Atlas Enterprise AI Intelligence Platform

## Master Project Context

**Document:** `ATLAS_MASTER_CONTEXT.md`
**Project:** Atlas Enterprise AI Intelligence Platform
**Repository:** `johnmccrae-ukfi/atlas`
**Current Release:** `v1.2.0`
**Current Phase:** Post-MVP platform evolution
**Primary Platform:** Microsoft Fabric
**Document Status:** Living authoritative reference

---

## 1. Purpose of This Document

This document is the authoritative high-level reference for the Atlas Enterprise AI Intelligence Platform.

It is intended to provide sufficient context for:

* future development sessions;
* AI coding assistants;
* prospective collaborators;
* technical reviewers;
* recruiters and hiring managers;
* future maintainers;
* architectural reviews;
* release planning;
* the project owner’s own future reference.

The document consolidates the most important information from the repository’s architecture documents, contracts, ADRs, release notes, workflow documentation, notebooks, code, and reporting assets.

It does not replace detailed implementation documents. Instead, it provides the context required to understand how those documents and components fit together.

Where this document conflicts with an approved Architecture Decision Record, the ADR takes precedence for the decision it governs. Where it conflicts with the current implementation, the discrepancy should be investigated and the documentation corrected as part of the same development change.

---

# 2. Executive Summary

Atlas is an enterprise-oriented Microsoft Fabric Data and AI platform built as a flagship portfolio project for senior Data Engineer, Fabric Engineer, Data Architect and AI Engineer contract opportunities.

The platform demonstrates how historical and near-real-time financial market data can be:

1. acquired from multiple providers;
2. preserved in source-aligned Bronze structures;
3. standardised into canonical Silver models;
4. transformed into analytics-ready Gold datasets;
5. exposed through governed Direct Lake semantic models;
6. analysed through Power BI and Fabric Real-Time Intelligence;
7. enriched with deterministic analytics and AI-generated market commentary;
8. managed through professional GitHub, documentation, versioning and release practices.

Atlas reached its first complete MVP with:

> **Atlas Enterprise AI Intelligence Platform v1.0.0**

The MVP processes a large CQG legacy futures tick dataset through a Microsoft Fabric medallion architecture and produces minute and daily OHLC candlestick data, trading KPIs, interactive Power BI reports, deterministic session summaries and an extensible AI commentary framework.

Atlas then expanded through:

> **v1.1.0 — Near-Real-Time Market Data Foundation**

This introduced a development-hosted Massive delayed Futures WebSocket adapter, Microsoft Fabric Eventstream ingestion, Eventhouse and KQL Database storage, validation and monitoring queries, and a live-refresh Real-Time Dashboard.

The reporting architecture was subsequently strengthened through:

> **v1.2.0 — Reporting Navigation and Time Intelligence**

This introduced a governed Gold date dimension, validated semantic-model relationships, reusable selected-period and trading-day measures, shared Date filtering across daily and minute analytical tables, and clearer report-page navigation.

Atlas is no longer treated as a disposable demonstration or short-lived proof of concept. It is a long-term engineering platform that evolves incrementally through documented releases, explicit contracts, governed architecture and validated implementation.

---

# 3. Project Vision

The long-term vision for Atlas is to become a credible enterprise reference architecture for market-data engineering and AI-assisted analytics on Microsoft Fabric.

Atlas should demonstrate not only that a technical result can be produced, but that the platform can be designed and operated using professional engineering disciplines.

The project therefore aims to show competence across:

* data platform architecture;
* Microsoft Fabric engineering;
* batch and near-real-time streaming ingestion;
* large-volume market data processing;
* schema standardisation;
* dimensional and analytical modelling;
* semantic model design;
* Power BI report development;
* AI-assisted analytics;
* responsible AI integration;
* source control;
* software design;
* testing and validation;
* technical documentation;
* architectural governance;
* release management;
* maintainable development workflows.

The value of Atlas comes from the complete platform and engineering lifecycle, not from any single notebook, report, chart, or AI response.

---

# 4. Strategic Objectives

Atlas has the following strategic objectives.

## 4.1 Portfolio Objective

Provide a publicly reviewable example of enterprise-grade Microsoft Fabric and Data and AI engineering that supports contract applications, technical discussions and interviews.

## 4.2 Engineering Objective

Build a maintainable platform in which ingestion, transformation, analytics, reporting, streaming and AI capabilities are separated into clear architectural responsibilities.

## 4.3 Architecture Objective

Demonstrate a practical medallion architecture using Bronze, Silver and Gold layers, with explicit contracts and traceability between layers.

Maintain a deliberate separation between:

- the historical Lakehouse analytical path;
- the near-real-time Eventstream and Eventhouse path;
- deterministic analytics;
- generative AI enrichment.

These paths may converge in future releases only through governed domain models and explicit architectural decisions.

## 4.4 Microsoft Fabric Objective

Use Microsoft Fabric as an integrated platform rather than as a collection of disconnected features.

Current Fabric capabilities used by Atlas include:

- OneLake;
- Fabric Lakehouse;
- Delta tables;
- Fabric notebooks;
- Apache Spark;
- Direct Lake semantic models;
- Power BI;
- Fabric Git integration;
- Eventstream;
- Eventhouse;
- KQL Database;
- KQL querysets;
- Real-Time Dashboards.

Future Fabric capabilities may include:

- Data Factory orchestration;
- deployment pipelines;
- environment promotion;
- Fabric Activator;
- operational monitoring;
- alerting;
- capacity and cost governance.

## 4.5 Reporting Objective

Provide governed and reusable historical reporting through:

- explicit analytical grain;
- shared dimensions;
- validated semantic-model relationships;
- reusable DAX measures;
- consistent filtering behaviour;
- clear daily and intraday report navigation;
- accurate financial formatting and calculation logic.

## 4.6 Near-Real-Time Objective

Demonstrate a controlled near-real-time market-data pathway using continuously arriving provider events, explicit schema governance, deterministic event identifiers, low-latency Fabric ingestion, KQL validation and live dashboard monitoring.

The current objective is architectural validation rather than production-complete streaming operations.

## 4.7 AI Objective

Use AI as an explainable enrichment layer built on trusted analytical outputs rather than allowing a model to replace deterministic data engineering or calculation logic.

## 4.8 Professional Practice Objective

Demonstrate architecture governance, semantic versioning, controlled releases, documentation discipline, Git branching, validation, incremental delivery and honest representation of limitations.

---

# 5. Current Project Status

## 5.1 Current Version

**Current production-style repository release:** `v1.2.0`

**Release name:** Reporting Navigation and Time Intelligence

## 5.2 Current Lifecycle Stage

The MVP phase is complete.

Atlas has now completed three major platform stages:

1. the `v1.0.0` historical Data and AI MVP;
2. the `v1.1.0` Near-Real-Time Market Data Foundation;
3. the `v1.2.0` Reporting Navigation and Time Intelligence release.

The project is now preparing for `v1.3.0 — Multi-Instrument Architecture`.

## 5.3 Current Capability Summary

Atlas currently includes:

- provider abstraction for historical and streaming market data;
- legacy CQG tick-data ingestion;
- Bronze Parquet storage in OneLake;
- source and deterministic ordering metadata;
- a canonical Silver tick model;
- minute and daily Gold OHLC candles;
- a governed Gold date dimension;
- a Direct Lake semantic model;
- reusable selected-period and trading-day measures;
- Power BI daily and intraday candlestick reporting;
- shared Date filtering across daily and minute analytical tables;
- explicit report-page navigation;
- deterministic session summaries;
- an AI market-commentary framework;
- a development-hosted near-real-time streaming adapter;
- Microsoft Fabric Eventstream ingestion;
- Eventhouse and KQL Database storage;
- KQL validation and market-monitoring queries;
- a live-refresh Real-Time Dashboard;
- Fabric Git integration;
- semantic versioning;
- Architecture Decision Records;
- installation, workflow and release documentation;
- a professionally presented public GitHub repository.

## 5.4 Current Development Direction

The next planned release is:

> **Atlas v1.3.0 — Multi-Instrument Architecture**

The next phase will focus on expanding Atlas beyond its initial historical CQG dataset and the single delayed Massive Futures contract used by the near-real-time pathway.

---

# 6. Current Architecture

Atlas currently contains two complementary market-data pathways:

1. a historical Lakehouse and Direct Lake analytical path;
2. a near-real-time Eventstream and Eventhouse path.

These pathways are intentionally separate at the current stage.

## 6.1 Historical Analytical Architecture

The historical logical flow is:

```text
Historical Market Data Sources
        |
        v
Provider Abstraction
        |
        v
Bronze Layer
Source-aligned market data and lineage metadata
        |
        v
Silver Layer
Canonical and validated market events
        |
        v
Gold Layer
Minute candles, daily candles, date dimension and analytical summaries
        |
        +----------------------+
        |                      |
        v                      v
Direct Lake              AI Analytics
Semantic Model           and Commentary
        |                      |
        +----------+-----------+
                   |
                   v
              Power BI
```

The current implemented historical physical flow is:

```text
CQG legacy .ts file
        |
        v
CQGLegacyProvider
        |
        v
Bronze Parquet files in OneLake
        |
        v
Bronze Fabric ingestion notebook
        |
        v
silver_cqg_ticks
        |
        v
gold_cqg_minute_candles
        |
        v
gold_cqg_daily_candles
        |
        +----------------------+
        |                      |
        v                      v
gold_dim_date          Gold AI summaries
        |                      |
        v                      v
sm_atlas_gold_reporting
        |
        v
Power BI Market Overview
and Intraday Analysis
```

The governed date dimension provides shared filtering across daily and minute candle tables.

The daily and minute candle tables remain separate analytical tables at different grains and are not related directly to each other.

## 6.2 Near-Real-Time Architecture

The implemented near-real-time flow is:

```text
Massive delayed Futures WebSocket
        |
        v
Atlas local Python streaming adapter
        |
        v
Microsoft Fabric Eventstream
        |
        v
Eventhouse and KQL Database
        |
        v
raw_massive_futures_minute_aggregates
        |
        v
KQL validation and market monitoring
        |
        v
Live-refresh Real-Time Dashboard
```

The current feed uses:

```text
Endpoint:
wss://delayed.massive.com/futures

Subscription:
AM.MESU6
```

The streaming adapter:

- connects to the Massive delayed Futures WebSocket;
- authenticates and subscribes to minute aggregates;
- transforms provider events into an Atlas event envelope;
- validates required fields, timestamps, interval values, OHLC values and non-negative measures;
- generates deterministic Atlas event identifiers;
- preserves the raw provider payload;
- publishes JSON events through the Fabric Eventstream custom endpoint.

## 6.3 Current Architectural Separation

The historical Lakehouse path and near-real-time Eventhouse path are intentionally separate.

The current architecture does not yet provide:

- streaming Silver tables;
- streaming Gold candle tables;
- automatic reconciliation between historical and streamed data;
- promotion from Eventhouse into the canonical Lakehouse model;
- automatic futures-contract rollover;
- production cloud hosting for the streaming adapter.

These remain future architectural increments rather than hidden implementation gaps.

## 6.4 Reporting Architecture Integration

The historical reporting path uses:

```text
gold_dim_date
        |
        +------------------------------+
        |                              |
        v                              v
gold_cqg_daily_candles       gold_cqg_minute_candles
        |                              |
        +---------------+--------------+
                        |
                        v
             sm_atlas_gold_reporting
                        |
                        v
                    Power BI
```

The semantic model provides:

- active one-to-many Date relationships;
- single-direction filtering from `gold_dim_date`;
- reusable selected-period measures;
- reusable previous-trading-day measures;
- shared Date filtering across report pages;
- daily and intraday analytical experiences.

## 6.5 Architectural Direction

Future development should preserve the separation of responsibilities already established.

Historical and near-real-time data should converge only when Atlas has:

- provider-neutral instrument identity;
- multi-instrument canonical modelling;
- explicit streaming Silver and Gold contracts;
- duplicate and correction handling;
- historical and streaming reconciliation rules;
- production-style hosting and operational controls.

---

# 7. Medallion Architecture

## 7.1 Bronze Layer

The Bronze layer preserves data as close as reasonably possible to its source representation while adding technical metadata required for lineage, replay, validation, and deterministic ordering.

### Current Bronze Sources

* CQG legacy tick data;
* provider-generated Parquet files;
* Massive REST and delayed Futures WebSocket provider framework.

### Bronze Responsibilities

* ingest source data;
* preserve source values;
* preserve source-file identity;
* retain source row ordering;
* record technical ingestion metadata;
* avoid premature business transformation;
* support replay and investigation;
* provide a stable input for Silver transformations.

### Important Bronze Metadata

The Bronze implementation includes metadata such as:

* `source_file_name`;
* `source_file_path`;
* `source_row_number`;
* `event_sequence_in_file`.

Exact column names should remain aligned with the current implementation and Bronze contract.

### Current Validated CQG Dataset

The MVP reference dataset is:

```text
File: F.US.EU6M12_201203.ts
Instrument: F.US.EU6M12
Approximate size: 722.7 MB
Validated rows: 17,317,408
Trading days represented: 26
Bronze Parquet chunks: 18
Detected event-ordering issues: 0
```

The preservation of event order is a deliberate architectural requirement because multiple market events may share the same displayed timestamp.

---

## 7.2 Silver Layer

The Silver layer converts source-specific Bronze data into a canonical market-data representation.

### Current Silver Table

```text
silver_cqg_ticks
```

### Silver Responsibilities

* standardise field names;
* convert source values into agreed types;
* create a consistent market tick schema;
* preserve event ordering;
* separate source-specific ingestion concerns from downstream analytics;
* validate required fields;
* expose a stable contract to Gold transformations.

### Silver Design Principle

Downstream analytical logic should not need to understand the original CQG file layout.

Future providers should map their source data into the same canonical model wherever the underlying business meaning is equivalent.

Provider-specific differences must be handled deliberately rather than hidden through unsafe assumptions.

---

## 7.3 Gold Layer

The Gold layer contains analytics-ready datasets designed for semantic models, reporting, business calculations, and AI enrichment.

### Current Gold Tables

```text
gold_cqg_minute_candles
gold_cqg_daily_candles
gold_dim_date
```

### Minute Candle Grain

One row per:

```text
instrument
+ minute_timestamp
```

### Daily Candle Grain

One row per:

```text
instrument
+ trading_date
```

### Current Gold Measures and Attributes

Gold datasets include values such as:

* open price;
* high price;
* low price;
* close price;
* trade count;
* total trades;
* daily range;
* session-level metrics;
* chronological candle timestamps.

### Numeric Precision

Price values use an agreed high-precision decimal representation, currently:

```text
Decimal(18,5)
```

Changes to financial precision must be treated as architectural and contract changes rather than cosmetic implementation details.

---

# 8. Reporting Architecture

## 8.1 Semantic Model

The current semantic model is:

```text
sm_atlas_gold_reporting
```

It uses Direct Lake against Fabric Gold-layer data.

## 8.2 Current Reports

The current historical reporting solution includes:

### Market Overview

* daily candlestick visualisation;
* instrument filtering;
* date filtering;
* daily KPIs;
* trading-day analysis;
* price range analysis;
* trend information;
* daily return analysis.

### Intraday Analysis

* minute-level candlestick visualisation;
* intraday market behaviour;
* session trade counts;
* minute-level high, low, open, and close values;
* instrument and date filtering.

## 8.3 Current Visual Components

The reporting solution includes:

* custom Power BI candlestick visuals;
* date slicers;
* instrument slicers;
* KPI cards;
* moving-average or trend analysis;
* daily return percentage;
* trading-day count;
* daily range;
* daily range percentage;
* session trade count.

## 8.4 Reporting Direction

Future reporting development should prefer reusable semantic-model measures over visual-specific calculations.

Business logic should be centralised wherever practical so that report pages present consistent results.

---

# 9. AI Architecture

## 9.1 Current AI Components

The MVP contains two principal AI-related notebooks:

```text
nb_gold_ai_session_summary
nb_gold_ai_market_commentary
```

## 9.2 Session Summary

The session-summary process produces deterministic analytical context from Gold data.

This may include:

* session open;
* session close;
* session high;
* session low;
* price change;
* percentage change;
* session range;
* trade count;
* directional classification;
* notable analytical observations.

The deterministic summary is the trusted analytical input to any generative-AI commentary.

## 9.3 Market Commentary

The market-commentary notebook converts structured session analytics into human-readable commentary.

The design separates:

```text
trusted calculation
from
natural-language generation
```

The language model must not be treated as the authoritative calculator of OHLC values, percentages, counts, or other core market measures.

## 9.4 Provider Abstraction

The AI implementation is designed to support multiple inference options over time, including:

* Fabric-native AI capabilities;
* Azure AI Foundry;
* Azure OpenAI;
* approved external model providers;
* offline or mock providers for development and validation.

## 9.5 Current Limitation

A live Fabric AI inference call was blocked under the available trial capacity with an error associated with unsupported capacity or permissions.

The architecture and integration pattern were retained and documented even though production-style hosted inference could not be completed under that environment.

This limitation must not be disguised. It is an environment constraint rather than a reason to weaken the architecture.

---

# 10. Technology Stack

## 10.1 Microsoft Fabric Platform

Atlas currently uses:

- Microsoft Fabric
- OneLake
- Fabric Lakehouse
- Delta Lake
- Fabric notebooks
- Apache Spark
- PySpark
- Direct Lake
- Power BI
- Fabric Git integration
- Eventstream
- Eventhouse
- KQL Database
- KQL querysets
- Real-Time Dashboards

Future Fabric capabilities may include:

- Data Factory pipelines
- deployment pipelines
- environment promotion
- Fabric Activator
- operational monitoring
- alerting
- capacity and cost governance

## 10.2 Data Engineering and Analytics

- Python
- PySpark
- SQL
- KQL
- DAX
- Power BI semantic modelling
- custom Power BI candlestick visuals
- deterministic market-data aggregation
- reusable semantic-model measures

## 10.3 Development and Source Control

- Visual Studio Code
- Git
- GitHub
- Markdown
- Python virtual environments
- `requirements.txt`
- `.env` configuration
- Fabric Git integration
- pull-request-based development
- semantic versioning

## 10.4 Data Formats and Storage

- CQG legacy text-based tick files
- Parquet
- Delta tables
- JSON streaming event envelopes
- provider-native raw JSON payloads
- KQL table storage
- structured AI prompt and metadata records

## 10.5 External Data and Integration Technologies

- Massive REST APIs
- Massive delayed Futures WebSocket
- Event Hubs-compatible Fabric Eventstream custom endpoint
- Azure Event Hubs Python client libraries
- Azure AI Foundry integration patterns
- Azure OpenAI integration patterns

## 10.6 Engineering Practices

Atlas uses:

- medallion architecture;
- provider abstraction;
- explicit data contracts;
- documented analytical grain;
- deterministic event ordering;
- governed schema evolution;
- reusable semantic-model measures;
- Architecture Decision Records;
- semantic versioning;
- feature-oriented releases;
- Git branching;
- pull requests;
- source-control integration;
- validation scripts and notebook checks;
- professional repository documentation;
- explicit distinction between implemented and planned capabilities.

---

# 11. Fabric Assets

## 11.1 Development Workspace

Atlas is developed in a Git-integrated Microsoft Fabric workspace connected to the GitHub `dev` branch.

The workspace contains the historical Lakehouse reporting path and the near-real-time Eventstream and Eventhouse path.

## 11.2 Lakehouse

```text
lh_atlas_dev
```

The Lakehouse contains the historical Bronze, Silver and Gold analytical assets used by notebooks, Direct Lake semantic modelling and Power BI reporting.

## 11.3 Historical Data Tables

Current principal historical analytical tables include:

```text
silver_cqg_ticks
gold_cqg_minute_candles
gold_cqg_daily_candles
gold_dim_date
gold_ai_session_summary
```

The exact complete table inventory remains governed by the relevant Bronze, Silver and Gold contracts.

## 11.4 Fabric Notebooks

Current principal notebooks include:

```text
nb_atlas_bronze_market_bars_load
nb_atlas_bronze_cqg_legacy_ticks_load
nb_atlas_silver_cqg_ticks
nb_gold_cqg_ohlc_candles
nb_gold_dim_date
nb_gold_ai_session_summary
nb_gold_ai_market_commentary
```

`nb_gold_dim_date` generates and validates the governed Gold date dimension from the minimum and maximum `TradingDate` values present across the Gold daily and minute candle tables.

## 11.5 Semantic Model

```text
sm_atlas_gold_reporting
```

The semantic model uses Direct Lake against governed Gold tables.

It currently includes:

- daily candle data;
- minute candle data;
- `gold_dim_date`;
- active one-to-many Date relationships;
- reusable selected-period measures;
- reusable previous-trading-day measures;
- trading KPIs;
- the validated five-trading-day moving average.

## 11.6 Historical Power BI Report

The current historical report asset is:

```text
rpt_atlas_market_overview
```

It contains:

### Market Overview

- daily candlestick analysis;
- adjustable date-range filtering;
- instrument filtering;
- selected-period Open, High, Low and Close measures;
- selected-period Range and Range percentage;
- selected-period Return percentage;
- distinct Trading Days;
- Trading Day Change percentage;
- Total Trades;
- five-trading-day moving average;
- navigation to Intraday Analysis.

### Intraday Analysis

- minute-level candlestick analysis;
- single-date selection;
- instrument filtering;
- Last Price;
- Session High;
- Session Low;
- Session Trade Count;
- page navigation back to Market Overview.

Daily-to-intraday drill-through was evaluated but is not currently implemented because the selected free candlestick custom visual does not expose compatible Power BI drill-through context.

## 11.7 Eventstream

```text
es_atlas_massive_futures_dev
```

Current Eventstream components include:

```text
src_atlas_massive_futures
dest_atlas_massive_futures_raw
```

The custom endpoint source receives Atlas JSON event envelopes from the local Python streaming adapter.

The Eventhouse destination routes accepted events into the governed raw KQL table.

## 11.8 Eventhouse and KQL Database

```text
eh_atlas_realtime_dev
```

The current Eventhouse and KQL Database store the v1.1.0 delayed Futures minute-aggregate stream.

Current raw KQL table:

```text
raw_massive_futures_minute_aggregates
```

Current JSON ingestion mapping:

```text
raw_massive_futures_minute_aggregates_json_mapping
```

## 11.9 KQL Queryset

```text
eh_atlas_realtime_dev_queryset
```

Current query tabs include:

```text
Massive Futures Streaming Validation
Massive Futures Market Monitoring
Massive Futures Dashboard Source
```

The queryset supports:

- event-arrival validation;
- schema validation;
- duplicate-event checks;
- OHLC and non-negative measure checks;
- continuity analysis;
- provider-delay analysis;
- Fabric ingestion-latency analysis;
- dashboard-source queries.

## 11.10 Real-Time Dashboard

```text
rtd_atlas_massive_futures_dev
```

The current dashboard includes:

- recent `MESU6` minute aggregates;
- delayed close-price line visualisation;
- delayed volume column visualisation;
- live refresh after Eventhouse ingestion.

The Real-Time Dashboard demonstrates the near-real-time pathway but does not yet represent a production operational-monitoring solution.

## 11.11 Current External Runtime Dependency

The v1.1.0 Python streaming adapter is intentionally development-hosted and must currently run locally.

It connects to:

```text
wss://delayed.massive.com/futures
```

and subscribes to:

```text
AM.MESU6
```

The local adapter is not a Fabric item and is represented in the source repository through Python scripts, transformers and writers.

## 11.12 Future Fabric Assets

Potential future additions include:

- orchestration pipelines;
- parameterised deployments;
- environment-specific workspace configuration;
- deployment pipelines;
- Fabric Activator;
- data-quality dashboards;
- production operational monitoring;
- alerting;
- managed streaming transformations;
- streaming Silver and Gold models;
- historical and streaming reconciliation assets;
- operational metadata tables;
- environment-promotion controls.

These are roadmap items and must not be described as implemented until they exist.

---

# 12. Repository Structure

The Atlas repository separates application source code, local utilities, Fabric-managed assets, documentation, architecture records, images and configuration.

A representative structure is:

```text
atlas/
|
|-- README.md
|-- INSTALLATION.md
|-- CHANGELOG.md
|-- RELEASE_HISTORY.md
|-- Development_Workflow.md
|-- requirements.txt
|-- .env.example
|
|-- src/
|   |-- common/
|       |
|       |-- models/
|       |   |-- MarketBar.py
|       |
|       |-- providers/
|       |   |-- IMarketDataProvider.py
|       |   |-- MassiveProvider.py
|       |   |-- CQGLegacyProvider.py
|       |
|       |-- storage/
|       |   |-- parquet_writer.py
|       |   |-- BronzeWriter.py
|       |
|       |-- transformers/
|       |   |-- massive_futures_minute_aggregate_transformer.py
|       |
|       |-- writers/
|           |-- FabricEventstreamWriter.py
|
|-- scripts/
|   |-- smoke_test_massive_provider.py
|   |-- run_cqg_provider.py
|   |-- validate_cqg_parquet.py
|   |-- analyse_cqg_streaming_profile.py
|   |-- discover_massive_futures_contracts.py
|   |-- test_massive_futures_aggregates.py
|   |-- test_massive_futures_websocket.py
|   |-- test_massive_futures_minute_aggregate_transformer.py
|   |-- send_test_atlas_event_to_fabric.py
|   |-- run_massive_futures_stream_adapter.py
|
|-- docs/
|   |
|   |-- 00_Project/
|   |   |-- ATLAS_MASTER_CONTEXT.md
|   |
|   |-- 01_Architecture/
|   |   |-- Atlas_Architecture.md
|   |   |-- Atlas_Near_Real_Time_Market_Data.md
|   |   |-- Fabric_Bronze_Ingestion.md
|   |   |-- Silver_Contract.md
|   |   |-- Gold_Contract.md
|   |
|   |-- adr/
|       |-- ADR-001-...
|       |-- ADR-002-...
|       |-- ADR-003-...
|       |-- ADR-004-...
|       |-- ADR-005-...
|       |-- ADR-006-...
|       |-- ADR-007-...
|       |-- ADR-008-...
|       |-- ADR-009-Why-Near-Real-Time-Eventstream-Architecture.md
|
|-- fabric/
|   |
|   |-- nb_atlas_bronze_market_bars_load.Notebook/
|   |-- nb_atlas_bronze_cqg_legacy_ticks_load.Notebook/
|   |-- nb_atlas_silver_cqg_ticks.Notebook/
|   |-- nb_gold_cqg_ohlc_candles.Notebook/
|   |-- nb_gold_dim_date.Notebook/
|   |-- nb_gold_ai_session_summary.Notebook/
|   |-- nb_gold_ai_market_commentary.Notebook/
|   |
|   |-- sm_atlas_gold_reporting.SemanticModel/
|   |-- rpt_atlas_market_overview.Report/
|
|-- images/
|   |-- architecture_overview.png
|   |-- medallion_gold_assets.png
|   |-- ai_commentary.png
|   |-- github_workflow.png
|   |-- near_realtime_dashboard.png
|
|-- data/
|   |-- sample/
|
|-- tests/
```

The exact physical structure may vary because Microsoft Fabric generates and manages item folders and definition files.

Fabric-managed items should normally be changed in Fabric first and then committed through Fabric Git integration to the `dev` branch.

Local Python source, scripts and documentation should be updated through Visual Studio Code after pulling the latest Fabric commit.

Large market-data files, generated environments, credentials, local caches and unnecessary runtime artefacts must not be committed.

The repository must continue to distinguish clearly between:

- reusable source code;
- development and validation scripts;
- Fabric-generated item definitions;
- architecture and contract documentation;
- public images and screenshots;
- local or environment-specific configuration.

---

# 13. Core Source Components

## 13.1 Provider Interface

```text
IMarketDataProvider.py
```

Defines the abstraction expected from market-data providers.

The objective is to prevent Atlas from becoming tightly coupled to a single vendor, API, transport mechanism or file format.

Provider implementations should isolate:

- authentication;
- request and subscription handling;
- pagination;
- rate limits;
- retries;
- provider-specific schemas;
- provider-specific error handling;
- source metadata.

Downstream analytical logic should consume provider-neutral structures wherever the underlying business meaning is equivalent.

## 13.2 CQG Legacy Provider

```text
CQGLegacyProvider.py
```

Reads and interprets the legacy CQG tick-data format.

Its responsibilities include:

- parsing source rows;
- preserving source identity;
- retaining row order;
- exposing market-event values required by Bronze ingestion;
- supporting chunked or streaming processing for large files;
- surfacing malformed or unsupported rows clearly.

The provider must preserve enough information for deterministic downstream event ordering.

## 13.3 Massive Provider

```text
MassiveProvider.py
```

Provides the Atlas abstraction for Massive market-data access.

Current and future responsibilities may include:

- REST authentication;
- contract discovery;
- historical aggregate requests;
- provider-specific request construction;
- response validation;
- rate-limit handling;
- retry behaviour;
- provider metadata;
- conversion into provider-neutral Atlas models where appropriate.

The provider remains isolated from Fabric Eventstream publishing and downstream analytical logic.

## 13.4 Canonical Market Model

```text
MarketBar
```

Represents provider-neutral market-bar data where appropriate.

Tick data, aggregate data and bar data must not be treated as interchangeable without an explicit transformation.

Canonical models should preserve:

- instrument identity;
- event or interval timestamps;
- Open, High, Low and Close values where applicable;
- activity measures such as volume or trade count;
- provider and source metadata where required;
- sufficient precision for financial analysis.

## 13.5 Bronze Storage Components

```text
parquet_writer.py
BronzeWriter.py
```

These components encapsulate Bronze persistence behaviour and reduce duplication between provider implementations.

Their responsibilities include:

- stable output naming;
- Parquet persistence;
- chunked writing where required;
- schema consistency;
- technical metadata;
- source provenance;
- error reporting;
- separation of provider acquisition from Bronze storage.

## 13.6 Massive Futures Minute-Aggregate Transformer

```text
massive_futures_minute_aggregate_transformer.py
```

Transforms Massive Futures WebSocket minute-aggregate payloads into the governed Atlas streaming event envelope.

Its responsibilities include:

- validating required provider fields;
- validating the expected minute interval;
- converting provider epoch-millisecond timestamps into UTC timestamps;
- validating OHLC relationships;
- validating non-negative volume and transaction values;
- generating deterministic Atlas event identifiers;
- preserving the raw provider payload;
- adding Atlas ingestion metadata;
- producing JSON-compatible output for Fabric Eventstream publishing.

The transformer does not publish events directly and does not contain Fabric transport logic.

## 13.7 Fabric Eventstream Writer

```text
FabricEventstreamWriter.py
```

Encapsulates publication of Atlas streaming event envelopes to the Event Hubs-compatible Fabric Eventstream custom endpoint.

Its responsibilities include:

- connection configuration;
- JSON serialisation;
- event batching where appropriate;
- Eventstream publication;
- send confirmation;
- transport-level error reporting;
- separation of Fabric delivery from provider and transformation logic.

The writer does not perform provider authentication or market-data transformation.

## 13.8 Near-Real-Time Streaming Adapter

```text
run_massive_futures_stream_adapter.py
```

Coordinates the current development-hosted near-real-time pathway.

The adapter:

1. connects to the Massive delayed Futures WebSocket;
2. authenticates with the provider;
3. subscribes to `AM.MESU6`;
4. receives minute-aggregate events;
5. invokes the Massive Futures transformer;
6. publishes validated Atlas event envelopes through `FabricEventstreamWriter`;
7. logs connection, authentication, subscription, transformation and delivery status.

The adapter is intentionally local and development-hosted.

It is not yet a production service and does not currently provide:

- cloud hosting;
- durable buffering;
- replay;
- destination-level deduplication;
- advanced reconnect recovery;
- automatic contract rollover;
- managed identity;
- production secret management.

## 13.9 Streaming Discovery and Validation Scripts

Current v1.1.0 scripts include:

```text
discover_massive_futures_contracts.py
test_massive_futures_aggregates.py
test_massive_futures_websocket.py
test_massive_futures_minute_aggregate_transformer.py
send_test_atlas_event_to_fabric.py
run_massive_futures_stream_adapter.py
```

These scripts support:

- contract discovery;
- REST diagnostics;
- WebSocket connectivity;
- authentication testing;
- subscription testing;
- transformer validation;
- one-event Fabric diagnostics;
- end-to-end stream-adapter execution.

They are development and validation utilities rather than production orchestration components.

## 13.10 Gold Date-Dimension Notebook

```text
nb_gold_dim_date
```

Generates the governed Gold date dimension used by the historical reporting semantic model.

Its responsibilities include:

- reading minimum and maximum `TradingDate` values from Gold daily and minute candle tables;
- generating one continuous row per calendar date;
- deriving deterministic calendar attributes;
- validating row count and continuity;
- validating Date uniqueness and null handling;
- persisting `gold_dim_date` as a Delta table;
- reloading and validating the persisted table;
- confirming that all Gold candle trading dates match the date dimension.

The notebook does not infer formal trading calendars or exchange holidays.

## 13.11 Semantic Model Components

```text
sm_atlas_gold_reporting
```

Contains the historical Direct Lake semantic model.

Its current responsibilities include:

- exposing governed Gold tables;
- relating `gold_dim_date` to daily and minute candle tables;
- providing reusable selected-period measures;
- providing previous-trading-day measures;
- providing trading KPIs;
- preserving the validated five-trading-day moving average;
- controlling user-facing formatting, sort behaviour and hidden technical columns;
- supporting Market Overview and Intraday Analysis.

The semantic model should remain the preferred location for reusable reporting logic that does not require a physical Gold table.

## 13.12 Power BI Report Components

```text
rpt_atlas_market_overview
```

Contains the historical reporting experience.

Current pages include:

- Market Overview;
- Intraday Analysis.

The report uses:

- custom candlestick visuals;
- shared Date filtering;
- instrument filtering;
- KPI cards;
- selected-period measures;
- previous-trading-day comparisons;
- explicit page-navigation controls.

The report should consume governed semantic-model measures rather than duplicate business logic inside visuals wherever practical.

---

# 14. Naming Conventions

## 14.1 General Principles

Names should be:

* descriptive;
* stable;
* implementation-relevant;
* consistent across code and documentation;
* explicit about architectural layer where useful;
* free from unexplained abbreviations.

## 14.2 Fabric Items

Recommended patterns:

```text
lh_<project>_<environment>
nb_<layer>_<subject>_<purpose>
sm_<project>_<purpose>
pl_<project>_<purpose>
```

Examples:

```text
lh_atlas_dev
nb_atlas_silver_cqg_ticks
nb_gold_ai_market_commentary
sm_atlas_gold_reporting
```

## 14.3 Tables

Recommended patterns:

```text
bronze_<source>_<entity>
silver_<source-or-domain>_<entity>
gold_<business-grain-or-purpose>
```

Examples:

```text
silver_cqg_ticks
gold_cqg_minute_candles
gold_cqg_daily_candles
gold_dim_date
```

## 14.4 Python

* Classes: `PascalCase`
* Functions and methods: `snake_case`
* Variables: `snake_case`
* Constants: `UPPER_SNAKE_CASE`
* Private implementation details: leading underscore where appropriate
* Python file names should follow the established repository convention and remain consistent with existing imports.

## 14.5 Markdown Documents

Major repository documents use clear, descriptive names, normally in uppercase or title-style form where already established.

Examples:

```text
README.md
INSTALLATION.md
CHANGELOG.md
RELEASE_HISTORY.md
ATLAS_MASTER_CONTEXT.md
Development_Workflow.md
```

## 14.6 ADRs

ADRs use a numeric prefix and descriptive title.

Example:

```text
ADR-001-<decision-title>.md
```

Once assigned, ADR numbers must not be reused.

---

# 15. Coding Standards

## 15.1 General Standard

Code should be written for maintainability, clarity, traceability, and reviewability.

Cleverness is not a substitute for understandable engineering.

## 15.2 Python Standards

Python components should:

* use type hints where practical;
* separate responsibilities;
* avoid unnecessary global state;
* include meaningful docstrings for public classes and functions;
* raise informative exceptions;
* validate external inputs;
* isolate provider-specific behaviour;
* avoid embedding secrets;
* avoid hard-coded machine-specific paths;
* make file and environment configuration explicit;
* use streaming or chunked processing for large source files where appropriate.

## 15.3 Notebook Standards

Fabric notebooks should:

* begin with a clear purpose and scope;
* document inputs and outputs;
* group logic into understandable stages;
* avoid unexplained hidden state;
* minimise duplicated transformation logic;
* use stable table names;
* include validation checks;
* display concise operational summaries;
* avoid relying solely on manual cell execution order;
* be suitable for later orchestration.

## 15.4 SQL and Spark Standards

Transformations should:

* make grain explicit;
* preserve required precision;
* use deterministic ordering;
* avoid accidental duplicate generation;
* handle nulls deliberately;
* document assumptions;
* distinguish technical timestamps from market timestamps;
* keep layer responsibilities separate.

## 15.5 DAX Standards

Measures should:

* use descriptive names;
* centralise reusable business logic;
* return consistent results across report pages;
* avoid embedding business logic unnecessarily in individual visuals;
* include formatting appropriate to the measure;
* distinguish measures from source columns clearly.

## 15.6 Error Handling

Errors should include enough context to diagnose:

* the operation;
* the source or asset involved;
* the affected file or table where appropriate;
* the underlying reason;
* whether retry or manual intervention is appropriate.

## 15.7 Secrets and Credentials

Secrets must never be committed.

Use approved approaches such as:

* environment variables;
* local `.env` files excluded by `.gitignore`;
* Fabric connections;
* Azure Key Vault in future production-style deployments;
* managed identity where supported.

---

# 16. Data Engineering Standards

## 16.1 Grain

Every analytical table must have a documented grain.

For example:

```text
gold_cqg_minute_candles:
one row per instrument per minute timestamp

gold_cqg_daily_candles:
one row per instrument per trading date

gold_dim_date:
one row per calendar date
```

## 16.2 Ordering

Market-event ordering must not rely solely on timestamps when multiple events can share the same timestamp.

Source row numbers or explicit event sequence fields must be retained where required.

## 16.3 Precision

Financial prices must not be silently converted to imprecise types.

Changes to scale or precision require:

* impact analysis;
* data-contract review;
* regression validation;
* documentation updates.

## 16.4 Idempotency

Where practical, pipeline operations should be designed so they can be rerun safely.

Append, overwrite, merge, and partition behaviour must be chosen deliberately.

## 16.5 Validation

Each layer should validate both technical and business expectations.

Examples include:

* row counts;
* required columns;
* null checks;
* duplicate checks;
* ordering checks;
* OHLC consistency;
* date coverage;
* instrument coverage;
* invalid price detection;
* reconciliation between layers.

## 16.6 Lineage

The design should retain sufficient metadata to trace Gold results through Silver and Bronze to their original provider data.

---

# 17. Documentation Standards

Documentation is part of the implementation, not an optional final activity.

## 17.1 Documentation Synchronisation

A change is not complete until affected documentation has been reviewed.

Potentially affected documents include:

* `README.md`;
* `ATLAS_MASTER_CONTEXT.md`;
* architecture documents;
* data contracts;
* ADRs;
* `INSTALLATION.md`;
* `CHANGELOG.md`;
* `RELEASE_HISTORY.md`;
* `Development_Workflow.md`;
* notebook markdown;
* code comments and docstrings.

## 17.2 Documentation Style

Documentation should:

* use clear headings;
* define acronyms;
* distinguish current implementation from future plans;
* avoid unsupported claims;
* include diagrams where they add meaning;
* describe architectural rationale, not only steps;
* use exact names for Fabric items and repository components;
* remain understandable to a technically competent reader who did not build the project.

## 17.3 Current Architecture Documents

Key detailed documents include:

```text
Atlas_Architecture.md
Fabric_Bronze_Ingestion.md
Silver_Contract.md
Gold_Contract.md
Development_Workflow.md
INSTALLATION.md
```

## 17.4 Images and Diagrams

Current repository imagery includes:

```text
architecture_overview.png
medallion_gold_assets.png
ai_commentary.png
github_workflow.png
```

Diagrams should be updated when architectural changes make the current representation materially inaccurate.

---

# 18. Architecture Decision Records

Atlas uses Architecture Decision Records to document decisions with long-term architectural consequences.

The current ADR set covers the following areas.

## ADR-001 — Microsoft Fabric Platform

Records the decision to use Microsoft Fabric as the core integrated Data and AI platform.

## ADR-002 — Medallion Architecture

Records the use of Bronze, Silver and Gold responsibilities to separate ingestion, standardisation and analytical presentation.

## ADR-003 — AI-Assisted Development

Records the controlled use of AI assistants during design, implementation, review and documentation while retaining human ownership of decisions and validation.

## ADR-004 — Direct Lake

Records the use of Direct Lake for reporting over Fabric Gold datasets.

## ADR-005 — Certified Semantic Models

Records the intended direction toward governed, reusable and potentially certified semantic models as Atlas matures.

## ADR-006 — Bronze Provider Strategy

Records the separation of provider-specific acquisition from common Bronze persistence and downstream transformation.

## ADR-007 — Multi-AI Workflow

Records the principle that different AI tools or providers may be used where appropriate, without allowing the project to become dependent on one assistant or inference provider.

## ADR-008 — Bronze Ingestion

Records the selected Bronze ingestion design, including large-file handling, metadata preservation, Parquet generation and Fabric loading.

## ADR-009 — Near-Real-Time Eventstream Architecture

```text
ADR-009-Why-Near-Real-Time-Eventstream-Architecture.md
```

Records the decision to introduce the first near-real-time Atlas pathway using:

```text
Massive delayed Futures WebSocket
→ local Atlas Python streaming adapter
→ Microsoft Fabric Eventstream
→ Eventhouse and KQL Database
→ raw minute aggregates
→ KQL validation and monitoring
→ Real-Time Dashboard
```

The ADR establishes that:

- the initial streaming scope is a controlled vertical slice;
- the adapter is intentionally development-hosted;
- historical Lakehouse and near-real-time Eventhouse pathways remain separate;
- Eventstream and Eventhouse are used for continuously arriving market events;
- raw provider payloads and timestamps are preserved;
- explicit KQL schema governance is preferred over uncontrolled inference;
- production hosting, resilient buffering, automatic rollover and streaming Silver and Gold models remain future work.

## 18.1 ADR Rules

Create a new ADR when a decision:

- materially changes architecture;
- introduces a major platform dependency;
- changes data contracts;
- changes deployment strategy;
- changes security or governance posture;
- establishes a long-term engineering convention;
- reverses a previous ADR.

Do not create ADRs for minor implementation details that can be adequately explained in code, ordinary documentation or release notes.

Accepted ADRs should not be rewritten to conceal historical decisions.

When a decision changes:

1. retain the original ADR;
2. create a new superseding ADR;
3. explain the reason for the change;
4. update affected architecture documentation and contracts.

## 18.2 Current ADR Position for v1.2.0

No new ADR was required for `v1.2.0 — Reporting Navigation and Time Intelligence`.

The release extended the existing governed Gold, Direct Lake and semantic-model architecture without introducing a new platform dependency or reversing an existing architectural decision.

The new `gold_dim_date` table and reusable measures are governed through:

- the Gold contract;
- the Direct Lake ADR;
- the certified semantic-model direction;
- semantic-model validation;
- release documentation.

Daily-to-intraday drill-through was evaluated but deferred because of a current custom-visual capability limitation. This did not constitute an architectural decision requiring a new ADR.

---

# 19. Development Workflow

Atlas uses an agreed workflow combining Fabric Git integration, local VS Code development, and GitHub pull requests.

This workflow is fixed unless explicitly changed through an architectural or process decision.

## 19.1 Branches

```text
main
dev
```

### `main`

Represents the stable, reviewed repository state.

### `dev`

Represents active integrated development and is connected to the Fabric development workspace.

## 19.2 Standard Workflow

```text
Fabric Git Integration
        |
        v
Commit Fabric changes to dev
        |
        v
VS Code
git checkout dev
git pull origin dev
        |
        v
Develop or update local code and documentation
        |
        v
git add .
git commit
git push origin dev
        |
        v
GitHub Pull Request
dev -> main
        |
        v
Review and merge
        |
        v
Create semantic version tag and GitHub release where applicable
        |
        v
Synchronise dev from main
```

## 19.3 Standard Commands

```bash
git checkout dev
git pull origin dev

git status
git add .
git commit -m "<type>: <description>"
git push origin dev
```

After the pull request is merged:

```bash
git checkout main
git pull origin main

git checkout dev
git pull origin main
git push origin dev
```

The precise synchronisation commands may vary depending on repository state, but the result must be:

```text
dev is aligned with main after the release merge
```

## 19.4 Fabric-First Changes

For Fabric-managed items:

1. make and validate the change in Fabric;
2. commit the Fabric changes to `dev`;
3. pull `dev` into the local repository;
4. add or update local documentation and source code;
5. push the complete change set to `dev`;
6. create the pull request.

## 19.5 Pull Requests

Pull requests should explain:

* what changed;
* why it changed;
* architectural impact;
* validation performed;
* documentation updated;
* known limitations;
* release impact.

## 19.6 Direct Commits to Main

Direct development commits to `main` should be avoided.

`main` should normally be changed through a pull request from `dev`.

---

# 20. Commit Conventions

Atlas uses concise, professional commit messages.

Recommended format:

```text
<type>: <description>
```

Common types include:

```text
feat:
fix:
docs:
refactor:
test:
chore:
build:
ci:
```

Examples:

```text
feat: add daily OHLC candle generation
docs: add AI trading intelligence architecture
fix: preserve source event ordering
refactor: extract common Bronze writer
```

Commit messages should describe the completed change, not the activity used to produce it.

Avoid vague messages such as:

```text
updates
changes
more work
fix stuff
```

---

# 21. Versioning and Release Management

Atlas follows semantic versioning:

```text
MAJOR.MINOR.PATCH
```

## 21.1 Version Meaning

### Major

Used for incompatible architectural or product-level changes.

### Minor

Used for backward-compatible feature releases or significant platform increments.

### Patch

Used for backward-compatible corrections, documentation improvements, integration adjustments, or limited enhancements.

## 21.2 Release Requirements

A release should normally include:

* completed implementation;
* validation;
* updated documentation;
* updated changelog;
* updated release history where appropriate;
* pull request merge;
* Git tag;
* GitHub release entry;
* synchronised `dev` and `main` branches.

Not every documentation commit requires a release tag. Release tags should correspond to meaningful repository states.

---

# 22. Release History Summary

## v0.1.0 — Foundation

Established the repository, solution structure, provider abstraction, initial development standards and project foundation.

## v0.2.0 — Bronze Layer

Implemented Bronze ingestion and persistence foundations for market data.

## v0.3.0 — Silver Layer

Introduced the canonical Silver tick model and standardised transformation.

## v0.4.0 — Gold OHLC

Created minute and daily OHLC candle datasets.

## v0.5.0 — Reporting Foundation

Established the semantic model and Power BI reporting foundation.

## v0.6.0 — Interactive Trading Dashboard

Added interactive report behaviour, candlestick analysis, KPI cards and date filtering.

## v0.7.0 — Trading Analytics and Report UX

Improved analytical measures, report usability and the trading-focused user experience.

## v0.8.0 — AI Trading Intelligence Foundation

Introduced deterministic session analytics, analytical classifications and the initial AI architecture.

## v0.9.0 — AI Market Commentary Framework

Added the structured market-commentary generation framework.

## v0.9.1 — Fabric AI Provider Integration

Added and documented Fabric AI provider integration, including the capacity limitation encountered during live inference.

## v1.0.0 — MVP Finalisation

Completed the professional MVP release, including repository presentation, installation guidance, architecture diagrams, release documentation, requirements and final consistency improvements.

## v1.1.0 — Near-Real-Time Market Data Foundation

Introduced Atlas’s first governed near-real-time market-data pathway.

The release added:

- Massive delayed Futures WebSocket ingestion;
- a local Atlas Python streaming adapter;
- Microsoft Fabric Eventstream;
- Eventhouse and KQL Database storage;
- an explicit raw KQL table and JSON ingestion mapping;
- KQL validation and monitoring queries;
- a live-refresh Real-Time Dashboard;
- preserved provider timestamps and raw payloads;
- deterministic Atlas streaming event identifiers;
- documented development-hosting and production-readiness limitations.

The release established the first working Real-Time Intelligence vertical slice while preserving the separate historical Lakehouse architecture.

## v1.2.0 — Reporting Navigation and Time Intelligence

Strengthened the historical Direct Lake reporting architecture.

The release added:

- `nb_gold_dim_date`;
- the governed `gold_dim_date` Delta table;
- continuous calendar coverage based on the current Gold data range;
- active one-to-many Date relationships to daily and minute candle tables;
- shared Date filtering across Market Overview and Intraday Analysis;
- reusable selected-period measures;
- reusable previous-trading-day measures;
- a multi-instrument-safe distinct Trading Days measure;
- improved date formatting and chronological sort metadata;
- explicit page-navigation controls;
- consistent KPI-card styling and report-page layout;
- updated Gold contract and validation rules.

Daily-to-intraday drill-through was evaluated and validated with standard Power BI visuals but deferred because the current free candlestick custom visual does not expose compatible drill-through context.

The release preserved the existing date-range analysis and implemented explicit page navigation instead.

---

# 23. Current Roadmap

The Atlas roadmap is incremental and may be refined as implementation discoveries, platform constraints, portfolio priorities and contract-market opportunities emerge.

The sequence deliberately separates:

- historical Lakehouse engineering;
- governed Direct Lake reporting;
- near-real-time Eventstream and Eventhouse ingestion;
- multi-instrument modelling;
- production-style AI inference;
- production-style Real-Time Intelligence.

Completed releases remain documented here because they establish the architectural dependencies for later work.

## v1.1.0 — Near-Real-Time Market Data Foundation

**Status:** Completed

Implemented focus:

- introduced the first end-to-end near-real-time market-data pathway;
- connected to the Massive delayed Futures WebSocket;
- began with delayed minute aggregates for `AM.MESU6`;
- created the Atlas Python streaming adapter;
- transformed provider payloads into a governed Atlas event envelope;
- forwarded JSON events into Microsoft Fabric Eventstream;
- routed Eventstream output into Eventhouse;
- created the KQL Database and raw market-event table;
- preserved provider timestamps and Atlas ingestion metadata;
- preserved the raw provider payload;
- validated event arrival, schema, latency, ordering and record counts;
- created KQL validation, monitoring and dashboard-source queries;
- created a live-refresh Real-Time Dashboard;
- documented delayed-market-data behaviour and environment limitations;
- added ADR-009 for the initial near-real-time architecture.

Implemented flow:

```text
Massive delayed Futures WebSocket
        |
        v
Atlas local Python streaming adapter
        |
        v
Microsoft Fabric Eventstream
        |
        v
Eventhouse and KQL Database
        |
        v
raw_massive_futures_minute_aggregates
        |
        v
KQL validation and monitoring
        |
        v
Live-refresh Real-Time Dashboard
```

The release proved that Atlas can ingest and analyse continuously arriving market data while preserving the existing historical Lakehouse and medallion architecture.

The following remain outside the completed v1.1.0 scope:

- enterprise-grade continuous hosting;
- broad multi-instrument subscriptions;
- full streaming Silver and Gold models;
- durable buffering and replay;
- destination-level deduplication;
- provider correction handling;
- comprehensive monitoring and alerting;
- automatic futures-contract rollover;
- production deployment automation;
- historical and streaming reconciliation.

These capabilities remain part of the later Real-Time Intelligence expansion.

## v1.2.0 — Reporting Navigation and Time Intelligence

**Status:** Completed

Implemented focus:

- created the governed `gold_dim_date` table;
- added `nb_gold_dim_date`;
- generated continuous calendar coverage from the minimum to maximum Gold `TradingDate`;
- included weekends without inferring formal trading-day status;
- added deterministic calendar attributes and chronological sort columns;
- added active one-to-many relationships from `gold_dim_date` to daily and minute candle tables;
- validated relationship cardinality, direction and filtering behaviour;
- replaced fact-table date slicers with the shared Date dimension;
- added reusable selected-period measures;
- added reusable previous-trading-day measures;
- changed Trading Days to a distinct-date measure suitable for future multi-instrument reporting;
- preserved the validated five-trading-day moving average;
- added explicit page navigation between Market Overview and Intraday Analysis;
- improved KPI-card consistency, spacing and report UX;
- updated the Gold contract, changelog, release history and master context.

Daily-to-intraday drill-through was evaluated.

The semantic model and target-page configuration were validated successfully with standard Power BI visuals.

The current free candlestick custom visual does not expose a selected candle as compatible drill-through context.

Drill-through was therefore deferred rather than represented as implemented.

The release retained:

- adjustable date-range analysis on Market Overview;
- single-date intraday analysis;
- explicit page-navigation controls.

## v1.3.0 — Multi-Instrument Architecture

**Status:** Next planned release

Planned focus:

- support multiple historical and near-real-time instruments;
- ingest selected Massive historical datasets;
- validate provider-neutral canonical modelling;
- introduce or strengthen governed instrument dimensions;
- distinguish provider identity, exchange identity, asset class and instrument identity;
- define stable instrument keys;
- review Silver and Gold keys, grain and partitioning;
- validate date and instrument filtering together;
- validate aggregation behaviour across instruments;
- review semantic-model relationships for multiple fact tables and dimensions;
- improve measure behaviour under multi-instrument selections;
- progress the certified semantic-model approach;
- review contract-month and futures-rollover representation;
- assess current and next futures-contract coverage;
- assess how historical and streamed instruments should converge on shared domain models;
- document data-provider licensing and retention constraints.

This release should establish the structural foundation required for Atlas to move beyond:

- the initial CQG historical futures dataset;
- the single `AM.MESU6` near-real-time subscription;
- report assumptions based on one instrument.

The release should not introduce automatic futures-contract rollover until instrument identity, contract identity and provider-neutral keys have been designed and validated.

## v1.4.0 — Production-Style AI Inference

**Status:** Planned

Planned focus:

- Azure AI Foundry or Azure OpenAI integration;
- configurable AI providers;
- secure configuration and secret handling;
- prompt templates and prompt versioning;
- structured model inputs and outputs;
- inference logging;
- model and provider traceability;
- validation and fallback behaviour;
- responsible handling of unsupported claims;
- cost and capacity awareness;
- controlled integration with trusted Gold analytical outputs;
- potential commentary across multiple instruments.

The AI layer will continue to consume deterministic analytical results rather than calculate authoritative market facts through generative inference.

## v1.5.0 — Real-Time Intelligence Expansion

**Status:** Planned

Planned focus:

- expand the v1.1.0 streaming foundation into a more complete Real-Time Intelligence architecture;
- support additional instruments and event types;
- improve WebSocket resilience, reconnection, retry and operational recovery;
- introduce production-style stream hosting;
- implement schema-management and evolution controls;
- address duplicate events, corrections, late arrival and incomplete intervals;
- introduce durable buffering and replay;
- create streaming transformations;
- develop near-real-time OHLC aggregations;
- introduce governed KQL functions and reusable query patterns;
- improve Eventhouse and KQL performance design;
- expand real-time dashboards;
- introduce configurable alerts and Fabric Activator where appropriate;
- add operational monitoring, observability and failure handling;
- reconcile streamed data with historical Lakehouse data;
- define promotion from the streaming hot path into canonical Silver and Gold models;
- establish security, deployment, capacity and environment-management patterns;
- perform performance and cost testing.

The v1.1.0 implementation must continue to be treated as the first vertical slice of this architecture rather than its completed production state.

## v1.6.0 and Beyond

Potential later capabilities include:

- technical indicators;
- volatility analytics;
- comparative instrument analysis;
- anomaly detection;
- configurable trading and data-quality alerts;
- AI-assisted market investigation;
- historical market replay;
- strategy-research and backtesting foundations;
- model evaluation;
- data-quality dashboards;
- Fabric pipeline orchestration;
- deployment automation;
- environment promotion;
- CI/CD expansion;
- observability;
- cost monitoring;
- performance optimisation;
- advanced governance;
- security hardening;
- semantic-model certification;
- operational support documentation.

The exact ordering of later capabilities will depend on:

- architectural dependencies;
- available Fabric capacity;
- data-provider licensing;
- available historical and streaming datasets;
- portfolio value;
- relevance to current contract opportunities.

---

# 24. Immediate v1.3.0 Priorities

The next engineering phase is:

> **Atlas v1.3.0 — Multi-Instrument Architecture**

Before substantial implementation begins, Atlas should complete the following controlled planning and discovery work.

## 24.1 Confirm the Initial Instrument Scope

Define the first multi-instrument dataset and provider scope.

This should include:

- which Massive historical datasets are available;
- which futures contracts or instruments will be ingested first;
- expected date coverage;
- expected event or bar grain;
- provider licensing and retention constraints;
- whether current and expired contracts are both required;
- whether the initial scope includes only futures or introduces another asset class.

The first v1.3.0 increment should remain small enough to validate the architecture without introducing unnecessary breadth.

## 24.2 Inspect Current Instrument Representation

Review the current instrument fields and assumptions across:

- Bronze data;
- `silver_cqg_ticks`;
- `gold_cqg_minute_candles`;
- `gold_cqg_daily_candles`;
- `gold_ai_session_summary`;
- `sm_atlas_gold_reporting`;
- Power BI slicers and measures;
- the Massive near-real-time event envelope;
- the raw Eventhouse table.

Identify any places where a single-instrument assumption is embedded in:

- keys;
- grouping logic;
- partitioning;
- measure definitions;
- report titles;
- visual filters;
- notebook parameters;
- provider-specific symbols.

## 24.3 Define Instrument Identity

Design a provider-neutral instrument identity model before loading multiple datasets.

The design should distinguish where required:

- internal Atlas instrument key;
- provider;
- provider symbol;
- asset class;
- exchange;
- underlying product;
- contract month;
- contract year;
- full contract symbol;
- currency;
- tick size;
- price precision;
- active or expired status.

Provider symbols must not automatically become the long-term canonical Atlas key.

## 24.4 Define the Instrument Dimension

Determine whether v1.3.0 should introduce a governed Gold instrument dimension such as:

```text
gold_dim_instrument
```

The dimension should have:

- explicit grain;
- a stable key;
- documented source and ownership;
- validated uniqueness;
- reusable semantic-model relationships;
- clear handling of contract-level and product-level identity.

The design must avoid premature assumptions about automatic futures rollover or continuous-contract construction.

## 24.5 Review Data Contracts

Review and update the relevant contracts before changing table grain or keys.

The review should cover:

- Bronze provider contracts;
- Silver canonical market-data contract;
- Gold candle contract;
- Gold date-dimension interaction;
- future instrument-dimension contract;
- streaming event-envelope contract;
- semantic-model relationship expectations.

Any change to grain, keys, financial precision or business meaning must be treated as a contract change.

## 24.6 Review Partitioning and Performance

Assess whether the existing historical tables should be partitioned or organised differently for multiple instruments and longer date ranges.

Consider:

- instrument;
- trading date;
- contract;
- provider;
- expected row volume;
- overwrite and incremental-load behaviour;
- Direct Lake performance;
- Spark transformation cost;
- future historical and streaming reconciliation.

Partitioning decisions should be based on expected access patterns and data volume rather than convention alone.

## 24.7 Review Semantic Model Design

Validate how multiple instruments will interact with:

- `gold_dim_date`;
- daily candles;
- minute candles;
- future `gold_dim_instrument`;
- selected-period measures;
- previous-trading-day measures;
- five-trading-day moving averages;
- totals and averages;
- instrument slicers;
- report titles;
- single-select and multi-select behaviour.

Measures must not silently aggregate unrelated instruments into misleading values.

## 24.8 Define the First Implementation Increment

The smallest coherent v1.3.0 implementation increment should likely include:

1. one additional historical instrument or contract;
2. a documented provider-neutral identity mapping;
3. validated Silver and Gold grain;
4. a governed instrument dimension or equivalent stable model;
5. semantic-model relationships;
6. instrument filtering in the existing reports;
7. reconciliation and regression validation;
8. documentation updates.

Automatic rollover, continuous contracts and broad multi-asset support should remain outside the first increment unless required by the validated design.

## 24.9 Preserve Existing Capabilities

All v1.3.0 work must preserve:

- validated CQG historical ingestion;
- deterministic event ordering;
- OHLC precision;
- `gold_dim_date`;
- existing selected-period measures;
- existing previous-trading-day measures;
- the five-trading-day moving average;
- current daily and intraday report behaviour;
- the separate v1.1.0 near-real-time pathway;
- the fixed Fabric and GitHub workflow.

## 24.10 Complete Through the Established Workflow

Each v1.3.0 increment should follow:

```text
inspect current implementation
→ define contract and grain
→ implement in Fabric or local source as appropriate
→ validate data and relationships
→ commit Fabric changes to dev
→ pull dev locally
→ update code and documentation
→ push dev
→ create pull request
→ review and merge
→ tag the completed release
→ synchronise dev from main
```

---

# 25. Design Principles

## 25.1 Maintainability Over Shortcuts

Atlas should favour clear, reusable, testable solutions over fast but fragile demonstrations.

## 25.2 Architecture Before Tool Novelty

New Fabric or AI features should be introduced because they support the architecture, not simply because they are available.

## 25.3 Data Contracts Matter

Changes to schema, grain, precision, keys, or business meaning must be treated as contract changes.

## 25.4 Deterministic Analytics Before Generative AI

Core facts and measures must be calculated through deterministic logic.

AI may explain or enrich trusted outputs but should not invent the underlying facts.

## 25.5 Source Fidelity in Bronze

Bronze should preserve enough source information to support replay, reconciliation, and investigation.

## 25.6 Canonical Meaning in Silver

Silver should establish shared domain meaning and remove unnecessary provider coupling.

## 25.7 Business Usability in Gold

Gold should be optimised for analysis, semantic modelling, reporting, and controlled AI consumption.

## 25.8 Documentation as an Engineering Deliverable

Documentation should evolve with the code and platform assets.

## 25.9 Incremental Releases

Atlas should grow through coherent, reviewable releases rather than large undocumented changes.

## 25.10 Honest Representation

The repository must distinguish clearly between:

* implemented functionality;
* partially implemented functionality;
* validated architecture;
* planned roadmap;
* environmental limitations.

---

# 26. Known Limitations

## 26.1 Single Primary Historical Dataset

The historical Lakehouse architecture is still validated principally against one large CQG futures dataset:

```text
F.US.EU6M12
```

Atlas now has a governed date dimension and reusable reporting measures, but the historical model has not yet been fully validated across multiple instruments, providers, exchanges or asset classes.

Multi-instrument behaviour is the primary focus of `v1.3.0`.

## 26.2 Development-Hosted Near-Real-Time Streaming

Atlas includes a working near-real-time market-data pathway, but the Python streaming adapter must currently run locally.

The current implementation does not yet provide:

- production cloud hosting;
- managed service supervision;
- durable buffering;
- replay;
- advanced reconnect recovery;
- automatic process restart;
- managed identity;
- production secret management;
- operational service-level monitoring.

The near-real-time architecture should therefore be treated as a validated development foundation rather than a production deployment.

## 26.3 Limited Near-Real-Time Instrument Scope

The current streaming implementation supports:

```text
AM.MESU6
```

from:

```text
wss://delayed.massive.com/futures
```

The current scope does not yet include:

- multiple simultaneous instruments;
- multiple event types;
- automatic futures-contract rollover;
- current-and-next contract management;
- continuous-contract construction;
- broader provider coverage.

## 26.4 Delayed Market Data

The Massive Futures feed used by Atlas is delayed.

Observed provider delay during v1.1.0 validation was approximately ten minutes.

The Real-Time Dashboard therefore demonstrates continuously arriving delayed market data rather than exchange-live market data.

Atlas documentation and screenshots must continue to describe this accurately.

## 26.5 Historical and Near-Real-Time Separation

The historical Lakehouse path and near-real-time Eventhouse path remain intentionally separate.

Atlas does not yet provide:

- streaming Silver tables;
- streaming Gold candle tables;
- promotion from Eventhouse into canonical Lakehouse tables;
- reconciliation between historical and streamed events;
- late-arrival handling across both paths;
- unified historical and near-real-time semantic models.

This separation is deliberate until shared instrument identity, streaming contracts and reconciliation rules are defined.

## 26.6 Duplicate and Correction Handling

Deterministic Atlas event identifiers support duplicate detection, and duplicate checks were validated during v1.1.0.

However:

- destination-level duplicate suppression is not enforced;
- provider correction messages are not yet handled;
- replay behaviour is not implemented;
- late or revised intervals are not reconciled automatically.

These capabilities remain part of the future Real-Time Intelligence expansion.

## 26.7 Formal Trading Calendars

`gold_dim_date` contains one row per calendar date and includes deterministic weekend classification.

Atlas does not yet implement:

- exchange-specific holidays;
- early-close sessions;
- daylight-saving session rules;
- asset-specific trading calendars;
- formal `IsTradingDay` logic;
- contract-specific session calendars.

`IsTradingDay` is deliberately not inferred from the presence or absence of historical candle rows.

Selecting a weekend or another date with no market data may therefore produce blank report visuals, which is expected.

## 26.8 Date-Dimension Range

The current `gold_dim_date` range is generated dynamically from the minimum and maximum `TradingDate` values present in the governed Gold daily and minute candle tables.

This is appropriate for v1.2.0, but the range will expand as v1.3.0 introduces additional historical datasets and instruments.

The implementation is dynamic and does not require a fixed hard-coded future horizon.

## 26.9 Drill-Through Limitation

Daily-to-intraday drill-through was evaluated during v1.2.0.

The semantic-model relationships and target-page configuration were validated successfully with standard Power BI visuals.

The current free candlestick custom visual does not expose a selected candle as compatible Power BI drill-through context.

Atlas therefore uses explicit page-navigation controls instead of candle-level drill-through.

This is a current visual capability limitation rather than a semantic-model or relationship defect.

## 26.10 Custom Visual Dependency

The historical report depends on a free custom Power BI candlestick visual.

The visual currently supports the required daily and minute candlestick presentation, but some Power BI interactions may behave differently from native visuals.

Atlas should avoid paying for or replacing the visual solely to satisfy a minor feature unless the replacement provides sufficient architectural or portfolio value.

## 26.11 Limited Hosted AI Execution

Hosted AI inference was constrained by available Fabric capacity and permissions.

The AI framework, provider abstraction and deterministic analytical preparation exist, but production-style hosted inference requires:

- an approved model deployment;
- suitable capacity;
- secure secret handling;
- provider configuration;
- cost controls;
- inference monitoring.

This limitation must continue to be represented as an environment constraint rather than hidden.

## 26.12 Development Environment

The current Fabric assets are development-oriented.

Atlas does not yet have a complete multi-environment strategy covering:

- development;
- test;
- staging;
- production;
- deployment pipelines;
- parameterised environment configuration;
- promotion approvals;
- rollback procedures.

## 26.13 Orchestration

Notebook execution is not yet represented as a fully productionised, monitored orchestration pipeline.

Current processes depend on controlled manual execution and validation.

Future orchestration should include:

- dependency management;
- scheduling;
- retries;
- failure notifications;
- run metadata;
- idempotency controls;
- environment configuration.

## 26.14 Automated Testing

The repository contains validation scripts, notebook checks and explicit reconciliation logic.

However, automated test coverage and continuous integration can be expanded.

Current gaps include:

- broader unit-test coverage;
- automated notebook validation;
- semantic-model regression tests;
- automated report validation;
- streaming integration tests;
- CI enforcement before merge.

## 26.15 Governance and Certification

Formal semantic-model certification, endorsement, lineage governance, access-control design and operational ownership remain roadmap areas.

The semantic model is governed through contracts, naming conventions, relationships and reusable measures, but it has not yet completed a formal enterprise certification process.

## 26.16 Data Licensing and Distribution

Large proprietary or restricted market-data files must not be distributed through the public repository.

The public project should use:

- schemas;
- representative samples;
- screenshots;
- documented row counts;
- reproducible instructions;
- configuration examples;
- architecture documentation.

Provider terms, licensing restrictions and redistribution rights must be reviewed before adding new historical or streaming datasets.

---

# 27. Security and Governance Principles

Even though Atlas is a portfolio platform, it should model responsible enterprise behaviour.

The project should:

* never commit credentials;
* minimise sensitive configuration;
* document external dependencies;
* use least-privilege access where practical;
* separate code from environment configuration;
* avoid exposing proprietary datasets;
* validate AI inputs and outputs;
* record model-provider assumptions;
* preserve lineage;
* make limitations explicit;
* prepare for future managed identity and Key Vault use;
* avoid embedding personal data in sample datasets or logs.

---

# 28. Testing and Validation Strategy

Atlas validation operates across source acquisition, historical medallion processing, semantic modelling, reporting, AI preparation and near-real-time ingestion.

Validation should be explicit, repeatable and appropriate to the grain and responsibility of each layer.

## 28.1 Source and Provider Validation

Source and provider validation should confirm:

- source files or endpoints exist and are reachable;
- authentication succeeds where required;
- the provider schema is recognised;
- malformed or unsupported rows are handled deliberately;
- source identifiers are preserved;
- timestamps are interpreted correctly;
- required provider fields are present;
- provider symbols are mapped deliberately;
- source ordering is retained where required;
- external limitations such as rate limits and delayed data are recorded.

For WebSocket sources, validation should also confirm:

- successful connection;
- successful authentication;
- successful subscription;
- expected event type;
- expected instrument;
- continuity while the adapter is active;
- controlled handling of connection failures.

## 28.2 Bronze Validation

Bronze validation should confirm:

- expected Parquet or Delta outputs are created;
- source metadata is populated;
- row counts reconcile with accepted source rows;
- ordering metadata is unique where required;
- source-file identity is retained;
- output schemas remain stable;
- data can be loaded by Fabric;
- replay and investigation remain possible;
- rejected or malformed records are accounted for.

Bronze must preserve source fidelity and must not introduce unsupported business interpretation.

## 28.3 Silver Validation

Silver validation should confirm:

- required columns exist;
- data types match the Silver contract;
- mandatory values are populated;
- provider-specific fields are mapped correctly;
- canonical field meaning is preserved;
- source-event order remains deterministic;
- quality-status fields are populated;
- invalid prices and timestamps are handled deliberately;
- duplicate behaviour is understood;
- row counts reconcile with accepted transformations;
- future multi-instrument keys remain unique at the documented grain.

## 28.4 Gold Candle Validation

For every minute and daily candle:

```text
High >= Open
High >= Close
High >= Low
Low <= Open
Low <= Close
```

Additional minute-candle validation should confirm:

- one row per Instrument and MinuteTimestamp;
- no unintended duplicate grain keys;
- TradeCount is non-negative;
- FirstEventSequence is less than or equal to LastEventSequence;
- Open matches the first valid ordered event;
- Close matches the last valid ordered event;
- High and Low match the valid source prices in the interval;
- Decimal(18,5) precision is preserved;
- persisted row counts match generated row counts.

Additional daily-candle validation should confirm:

- one row per Instrument and TradingDate;
- no unintended duplicate grain keys;
- TotalTrades is non-negative;
- Open matches the first minute candle of the day;
- Close matches the last minute candle of the day;
- High and Low reconcile with minute candles;
- Decimal(18,5) precision is preserved;
- daily row counts and date coverage are expected.

## 28.5 Gold Date-Dimension Validation

Validation of `gold_dim_date` must confirm:

- one row per Date;
- no null Date values;
- no duplicate Date values;
- continuous calendar coverage;
- minimum Date matches the minimum governed Gold TradingDate;
- maximum Date matches the maximum governed Gold TradingDate;
- expected row count equals the inclusive date range;
- Year, Quarter, Month and weekday values are correct;
- Monday-to-Sunday numbering is deterministic;
- weekend classification is correct;
- chronological sort columns are valid;
- no candle TradingDate values fall outside the dimension;
- no candle TradingDate values are null.

Formal exchange-calendar behaviour is not part of the current validation scope.

## 28.6 Semantic Model Validation

The historical semantic model should be validated for:

- correct table inclusion;
- active one-to-many relationships;
- `gold_dim_date` on the one side;
- daily and minute candle tables on the many side;
- single-direction filtering from the Date dimension;
- no direct daily-to-minute fact relationship;
- correct date-only formatting;
- correct sort-by-column settings;
- hidden technical sort columns;
- stable display folders;
- reusable explicit measures;
- multi-instrument-safe distinct-date calculations;
- correct filter propagation;
- meaningful totals and subtotals;
- stable behaviour after semantic-model refresh.

Current reusable measure validation should include:

- Selected Period Open;
- Selected Period High;
- Selected Period Low;
- Selected Period Close;
- Selected Period Return percentage;
- Daily Range;
- Daily Range percentage;
- Trading Days;
- Selected Trading Date;
- Previous Trading Date;
- Selected Trading Day Close;
- Previous Trading Day Close;
- Trading Day Change;
- Trading Day Change percentage;
- five-trading-day moving average.

Expected validated reference results for the current full historical range include:

```text
Selected Period Open: 1.33550
Selected Period Close: 1.33460
Selected Period Return: approximately -0.07%
Daily Range: 0.03830
Daily Range percentage: approximately 2.87%
Trading Days: 26
Previous Trading Day Close: 1.33610
Selected Trading Day Close: 1.33460
Trading Day Change: -0.00150
Trading Day Change percentage: approximately -0.11%
```

These values are reference checks for the current dataset rather than universal constants.

## 28.7 Power BI Report Validation

Report validation should confirm:

- Market Overview uses the governed Date dimension;
- Intraday Analysis uses the governed Date dimension;
- adjustable date-range filtering works on Market Overview;
- single-date selection works on Intraday Analysis;
- weekend selections produce expected blank visuals where no market data exists;
- artificial blank slicer members are excluded without removing genuine calendar dates;
- all KPI cards respond to filter changes;
- custom candlestick visuals render correctly;
- the five-day moving-average line remains correct after refresh;
- navigation between pages works in edit and reading modes;
- card formatting and decimal precision are consistent;
- titles and labels remain clear;
- no temporary diagnostic visuals remain;
- report visuals are bound to intended measures.

Daily-to-intraday drill-through should not be reported as implemented unless the selected candlestick visual exposes compatible Power BI drill-through context.

## 28.8 Near-Real-Time Transformation Validation

The Massive Futures transformer should validate:

- required fields are present;
- the event is a supported minute aggregate;
- interval values are correct;
- provider timestamps are valid;
- UTC timestamps are derived correctly;
- Open, High, Low and Close relationships are valid;
- volume and transaction values are non-negative;
- deterministic Atlas event identifiers are generated;
- the raw provider payload is preserved;
- output is JSON-compatible;
- transformation failures include useful diagnostics.

## 28.9 Eventstream and Eventhouse Validation

The near-real-time pathway should confirm:

- successful publication to the Fabric Eventstream custom endpoint;
- successful routing to Eventhouse;
- successful JSON ingestion mapping;
- expected KQL schema;
- expected decimal handling;
- provider and Atlas timestamps are populated;
- event identifiers are present;
- raw payloads remain queryable;
- no invalid OHLC rows;
- no negative-measure rows;
- duplicate-event checks return expected results;
- event continuity is visible while the adapter is running;
- provider delay is measurable;
- Fabric ingestion latency is measurable;
- end-to-end latency is measurable;
- dashboard-source queries return recent events.

Current validated observations include:

```text
Average provider delay: approximately 603.9 seconds
Average Fabric ingestion latency: approximately 0.47 seconds
Average end-to-end latency: approximately 604.4 seconds
```

These are observed development-environment results rather than production service-level commitments.

## 28.10 Real-Time Dashboard Validation

The Real-Time Dashboard should be checked for:

- recent event visibility;
- correct instrument filtering;
- correct ordering by event time;
- close-price line rendering;
- volume column rendering;
- live refresh after new Eventhouse ingestion;
- no stale or misleading titles;
- explicit indication that the provider feed is delayed.

The dashboard currently validates the streaming path rather than providing full production observability.

## 28.11 AI Validation

AI-related validation should confirm:

- deterministic analytical inputs are complete;
- prompts contain trusted calculated values;
- prompt versions are identifiable;
- provider configuration is explicit;
- inference metadata is recorded;
- generated commentary reflects supplied facts;
- unsupported claims are avoided;
- missing data is handled explicitly;
- provider failures have a controlled fallback;
- environment or capacity limitations are surfaced honestly.

Generative models must not be treated as authoritative calculators of OHLC values, counts, returns or other core market facts.

## 28.12 Regression Validation

Every material change should include regression checks against existing capabilities.

Regression validation should confirm that:

- Bronze row counts remain stable where expected;
- Silver grain remains stable;
- Gold OHLC values remain correct;
- financial precision is preserved;
- `gold_dim_date` remains continuous;
- relationships still filter correctly;
- existing measures still return expected results;
- Power BI visuals still render;
- page navigation still works;
- the near-real-time adapter still transforms and publishes correctly;
- KQL validation queries still run;
- documentation remains aligned with implementation.

## 28.13 Future Multi-Instrument Validation

For v1.3.0 and later, validation must expand to include:

- stable provider-neutral instrument keys;
- uniqueness across instruments and contracts;
- correct instrument-dimension relationships;
- date and instrument filter interaction;
- multi-instrument measure behaviour;
- prevention of misleading cross-instrument totals;
- contract-month handling;
- source-to-canonical symbol mapping;
- provider and exchange attribution;
- historical and streaming instrument alignment;
- partitioning and performance under larger date ranges.

---

# 29. AI Collaboration Guidelines

AI assistants are active development collaborators, but they do not own the architecture or determine truth independently.

## 29.1 Required Context

At the beginning of a new AI-assisted development session, provide or reference:

* this master context document;
* the current release;
* the target release;
* the relevant ADRs;
* the relevant contracts;
* the current repository state;
* the exact task being undertaken.

## 29.2 AI Responsibilities

An AI assistant may help with:

* architecture discussion;
* implementation design;
* Python;
* PySpark;
* SQL;
* DAX;
* Power BI design;
* custom Power BI visual configuration;
* tests;
* validation;
* documentation;
* release notes;
* commit messages;
* pull request descriptions;
* troubleshooting;
* code review.

## 29.3 Human Responsibilities

The project owner remains responsible for:

* approving architecture;
* executing changes;
* reviewing generated code;
* validating Fabric behaviour;
* verifying schemas and results;
* protecting secrets;
* deciding releases;
* merging pull requests;
* representing project capabilities accurately.

## 29.4 Rules for AI-Generated Changes

AI-generated output must:

* fit the existing architecture;
* use actual repository names;
* avoid inventing implemented assets;
* preserve agreed contracts;
* explain significant design choices;
* include validation steps;
* update relevant documentation;
* avoid replacing working code without cause;
* avoid unnecessary dependencies;
* remain reviewable by a human engineer.

## 29.5 Context Preservation

AI assistants should treat Atlas as a long-running project.

They should not restart architecture design from first principles unless:

* the project owner requests a redesign;
* a serious flaw is discovered;
* an ADR is being intentionally reconsidered.

## 29.6 Evidence and Honesty

An assistant must distinguish between:

* repository facts supplied by the project owner;
* conclusions derived from code or output;
* assumptions;
* recommendations;
* future proposals.

Unverified assumptions should not be presented as implemented facts.

## 29.7 Preferred Interaction Style

For implementation work, AI collaboration should normally proceed in small, controlled steps:

1. confirm the current state;
2. define the immediate change;
3. explain the design;
4. implement one coherent increment;
5. validate the result;
6. update documentation;
7. provide the appropriate commit or PR wording;
8. proceed to the next increment.

Large unreviewed code dumps should be avoided where a smaller iterative approach is possible.

---

# 30. Change Management for This Document

`ATLAS_MASTER_CONTEXT.md` is a living document.

It should be reviewed when any of the following occurs:

* a release is completed;
* architecture changes;
* a new Fabric asset is introduced;
* repository structure changes;
* an ADR is accepted or superseded;
* a data contract changes;
* the Git workflow changes;
* a major limitation is resolved;
* roadmap priorities change;
* an AI provider or deployment approach changes;
* naming conventions change.

Updates should be made in the same pull request as the implementation they describe whenever practical.

This document must not become a historical dump of every implementation detail. It should remain a concise but comprehensive description of the current platform, its governing decisions, and its direction.

Detailed technical instructions should continue to live in their dedicated documents.

---

# 31. Definition of Done

A development increment is considered complete when the applicable items below have been satisfied:

* implementation completed;
* code reviewed;
* Fabric assets saved and committed;
* expected results validated;
* data contracts preserved or intentionally updated;
* tests or validation checks completed;
* documentation updated;
* ADR added or superseded where required;
* changelog updated;
* pull request created;
* pull request reviewed and merged;
* version tagged when the increment constitutes a release;
* `dev` synchronised with `main`;
* roadmap and master context updated where necessary.

---

# 32. Current Authoritative Summary

At the completion of `v1.2.0`, Atlas is:

- a working Microsoft Fabric medallion architecture;
- a large-volume historical market-data engineering solution;
- a Bronze-to-Silver-to-Gold analytical pipeline;
- a governed Gold reporting layer;
- a Direct Lake semantic-model platform;
- an interactive Power BI daily and intraday reporting solution;
- a reusable time-intelligence and selected-period analytics model;
- a development-hosted near-real-time streaming architecture;
- an Eventstream and Eventhouse ingestion solution;
- a KQL validation and market-monitoring environment;
- a live-refresh Real-Time Dashboard;
- a deterministic AI analytical-preparation framework;
- an extensible AI market-commentary architecture;
- a professionally governed GitHub portfolio repository;
- a foundation for multi-instrument, production-style AI and expanded Real-Time Intelligence development.

## 32.1 Historical Analytical Capability

The historical pathway currently supports:

```text
CQG legacy futures ticks
→ Bronze Parquet and OneLake
→ silver_cqg_ticks
→ gold_cqg_minute_candles
→ gold_cqg_daily_candles
→ gold_dim_date
→ sm_atlas_gold_reporting
→ Power BI Market Overview and Intraday Analysis
```

The historical model includes:

- deterministic event ordering;
- minute and daily OHLC candles;
- Decimal(18,5) financial precision;
- a continuous governed date dimension;
- active one-to-many Date relationships;
- shared daily and intraday Date filtering;
- reusable selected-period measures;
- reusable previous-trading-day measures;
- a distinct Trading Days calculation;
- a validated five-trading-day moving average;
- explicit navigation between reporting pages.

## 32.2 Near-Real-Time Capability

The near-real-time pathway currently supports:

```text
Massive delayed Futures WebSocket
→ Atlas local Python streaming adapter
→ Microsoft Fabric Eventstream
→ Eventhouse and KQL Database
→ raw_massive_futures_minute_aggregates
→ KQL validation and monitoring
→ Real-Time Dashboard
```

The current streaming implementation:

- subscribes to `AM.MESU6`;
- receives delayed minute aggregates;
- validates timestamps, interval values, OHLC and non-negative measures;
- generates deterministic Atlas event identifiers;
- preserves the raw provider payload;
- publishes JSON events through the Fabric Eventstream custom endpoint;
- stores events in a governed KQL table;
- supports delay, latency, continuity and duplicate analysis;
- refreshes the Real-Time Dashboard after ingestion.

The adapter remains development-hosted and must currently run locally.

## 32.3 AI Capability

Atlas currently separates deterministic analytical preparation from generative inference.

The AI architecture includes:

- deterministic session summaries;
- validated market metrics;
- AI-ready prompt templates;
- configurable provider patterns;
- inference metadata;
- failure handling;
- an extensible market-commentary framework.

Production-style hosted inference remains dependent on suitable model deployment, capacity, secure configuration and cost controls.

## 32.4 Current Reporting Position

The historical report currently includes:

- Market Overview;
- Intraday Analysis;
- shared governed Date filtering;
- instrument filtering;
- daily and minute candlestick analysis;
- selected-period KPIs;
- previous-trading-day comparison;
- consistent KPI-card styling;
- explicit page-navigation controls.

Daily-to-intraday drill-through was evaluated but deferred because the current free candlestick custom visual does not expose compatible Power BI drill-through context.

This limitation is documented accurately and does not affect the semantic-model relationships or explicit page navigation.

## 32.5 Current Architectural Boundaries

Atlas does not yet provide:

- a fully validated multi-instrument historical model;
- a governed instrument dimension;
- automatic futures-contract rollover;
- production cloud hosting for the streaming adapter;
- durable streaming buffering and replay;
- provider correction handling;
- destination-level deduplication;
- streaming Silver and Gold models;
- historical and near-real-time reconciliation;
- production-style hosted AI inference;
- formal exchange-calendar logic;
- complete multi-environment deployment and orchestration.

These are planned architectural increments rather than implied implemented capabilities.

## 32.6 Next Planned Release

The next planned release is:

> **Atlas v1.3.0 — Multi-Instrument Architecture**

The immediate next engineering phase will focus on:

- selected Massive historical datasets;
- additional futures instruments or contracts;
- provider-neutral instrument identity;
- stable instrument keys;
- a governed instrument dimension;
- Silver and Gold grain validation;
- date and instrument filter interaction;
- multi-instrument semantic-model behaviour;
- report and measure validation across multiple instruments;
- preparation for future historical and streaming convergence.

Atlas must continue to evolve through explicit contracts, small implementation increments, human validation, professional documentation and the established Fabric-to-GitHub workflow.

---

# 33. Project Continuity Statement

Atlas must continue to be developed as an enterprise-quality, long-term platform.

Future contributors and AI assistants should preserve the established strengths of the project:

* deliberate architecture;
* clear layer responsibilities;
* source traceability;
* deterministic analytical logic;
* professional documentation;
* controlled Git workflow;
* semantic versioning;
* honest treatment of limitations;
* incremental delivery;
* maintainable engineering.

Changes should improve the coherence of the platform rather than merely increase its feature count.

---

**End of document**
