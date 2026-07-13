# Atlas Enterprise AI Intelligence Platform

## Master Project Context

**Document:** `ATLAS_MASTER_CONTEXT.md`
**Project:** Atlas Enterprise AI Intelligence Platform
**Repository:** `johnmccrae-ukfi/atlas`
**Current Release:** `v1.0.0`
**Current Phase:** Post-MVP evolution
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

Atlas is an enterprise-oriented Microsoft Fabric Data and AI platform built as a flagship portfolio project for senior Data Engineer, Fabric Engineer, Data Architect, and AI Engineer contract opportunities.

The platform demonstrates how historical and future real-time financial market data can be:

1. acquired from multiple providers;
2. preserved in a Bronze layer;
3. standardised into a canonical Silver model;
4. transformed into analytics-ready Gold datasets;
5. exposed through a Direct Lake semantic model;
6. visualised in Power BI;
7. enriched with deterministic analytics and AI-generated market commentary;
8. managed through professional GitHub, documentation, versioning, and release practices.

Atlas reached its first complete MVP with release:

> **Atlas Enterprise AI Intelligence Platform v1.0.0**

The MVP processes a large CQG legacy futures tick dataset through a Microsoft Fabric medallion architecture and produces minute and daily OHLC candlestick data, trading KPIs, interactive Power BI reports, session summaries, and an extensible AI commentary framework.

Atlas is no longer treated as a disposable demonstration or short-lived proof of concept. It is a long-term engineering platform that will evolve incrementally through documented post-MVP releases.

---

# 3. Project Vision

The long-term vision for Atlas is to become a credible enterprise reference architecture for market-data engineering and AI-assisted analytics on Microsoft Fabric.

Atlas should demonstrate not only that a technical result can be produced, but that the platform can be designed and operated using professional engineering disciplines.

The project therefore aims to show competence across:

* data platform architecture;
* Microsoft Fabric engineering;
* batch and future streaming ingestion;
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

Provide a publicly reviewable example of enterprise-grade Microsoft Fabric and Data and AI engineering that supports contract applications, technical discussions, and interviews.

## 4.2 Engineering Objective

Build a maintainable platform in which ingestion, transformation, analytics, reporting, and AI capabilities are separated into clear architectural responsibilities.

## 4.3 Architecture Objective

Demonstrate a practical medallion architecture using Bronze, Silver, and Gold layers, with explicit contracts and traceability between layers.

## 4.4 Microsoft Fabric Objective

Use Microsoft Fabric as an integrated platform rather than as a collection of disconnected features.

Relevant Fabric capabilities include:

* OneLake;
* Lakehouse;
* Delta tables;
* Fabric notebooks;
* Spark;
* Direct Lake semantic models;
* Power BI;
* Git integration;
* future Eventstream and Eventhouse capabilities;
* future Fabric Data Factory orchestration;
* future monitoring and operational controls.

## 4.5 AI Objective

Use AI as an explainable enrichment layer built on trusted analytical outputs rather than allowing an AI model to replace deterministic data engineering or calculation logic.

## 4.6 Professional Practice Objective

Demonstrate architecture governance, semantic versioning, controlled releases, documentation discipline, Git branching, validation, and incremental delivery.

---

# 5. Current Project Status

## 5.1 Current Version

**Current production-style repository release:** `v1.0.0`

**Release name:** Atlas Enterprise AI Intelligence Platform MVP

## 5.2 Current Lifecycle Stage

The MVP phase is complete.

The project has entered its post-MVP phase, beginning with the creation of this master context document and followed by development of `v1.1.0`.

## 5.3 MVP Completion Summary

The MVP includes:

* a provider abstraction for market data;
* legacy CQG tick-data ingestion;
* Bronze Parquet storage in OneLake;
* source and ordering metadata preservation;
* a canonical Silver tick model;
* minute OHLC Gold candles;
* daily OHLC Gold candles;
* trading KPIs;
* a Direct Lake semantic model;
* Power BI candlestick reporting;
* intraday and daily market analysis;
* deterministic session summaries;
* an AI market commentary framework;
* Fabric Git integration;
* GitHub release history;
* semantic versioning;
* ADRs;
* installation and workflow documentation;
* a professionally presented GitHub repository.

---

# 6. Current Architecture

## 6.1 Logical Architecture

The current logical flow is:

```text
Market Data Sources
        |
        v
Provider Abstraction
        |
        v
Bronze Layer
Raw and source-aligned market data
        |
        v
Silver Layer
Canonical, standardised market ticks
        |
        v
Gold Layer
Minute candles, daily candles and analytical summaries
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

## 6.2 Current Physical Flow

The implemented MVP primarily uses a legacy CQG futures tick file as its source.

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
Silver canonical tick Delta table
        |
        v
Gold minute and daily OHLC Delta tables
        |
        v
Direct Lake semantic model
        |
        v
Power BI reports
```

Gold analytical outputs also feed the session-summary and AI-commentary notebooks.

---

# 7. Medallion Architecture

## 7.1 Bronze Layer

The Bronze layer preserves data as close as reasonably possible to its source representation while adding technical metadata required for lineage, replay, validation, and deterministic ordering.

### Current Bronze Sources

* CQG legacy tick data;
* provider-generated Parquet files;
* Massive API provider framework for future API-based data acquisition.

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
gold_minute_candles
gold_daily_candles
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

The MVP includes reporting experiences for:

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

* Deneb candlestick visuals;
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

## 10.1 Microsoft Platform

* Microsoft Fabric
* OneLake
* Fabric Lakehouse
* Delta Lake
* Fabric notebooks
* Apache Spark
* PySpark
* Direct Lake
* Power BI
* Fabric Git integration
* Azure AI Foundry integration patterns
* Azure OpenAI integration patterns

## 10.2 Development

* Python
* PySpark
* SQL
* DAX
* Vega-Lite through Deneb
* Visual Studio Code
* Git
* GitHub
* Markdown
* virtual environments
* `requirements.txt`

## 10.3 Data Formats

* CQG legacy text-based tick files
* Parquet
* Delta tables
* structured JSON-compatible AI payloads where appropriate

## 10.4 Engineering Practices

* medallion architecture;
* provider abstraction;
* data contracts;
* ADRs;
* semantic versioning;
* feature-oriented releases;
* pull requests;
* Git branching;
* source control integration;
* validation scripts;
* professional repository documentation.

---

# 11. Fabric Assets

## 11.1 Workspace

The development workspace is the Git-integrated Fabric workspace used for Atlas development.

The workspace is connected to the GitHub `dev` branch.

## 11.2 Lakehouse

```text
lh_atlas_dev
```

## 11.3 Notebooks

Current principal notebooks include:

```text
nb_atlas_bronze_market_bars_load
nb_atlas_bronze_cqg_legacy_ticks_load
nb_atlas_silver_cqg_ticks
nb_gold_cqg_ohlc_candles
nb_gold_ai_session_summary
nb_gold_ai_market_commentary
```

## 11.4 Semantic Model

```text
sm_atlas_gold_reporting
```

## 11.5 Reports

The repository and Fabric workspace contain the report assets supporting:

* Market Overview;
* Intraday Analysis;
* daily candlestick analysis;
* minute candlestick analysis;
* market KPIs.

## 11.6 Future Fabric Assets

Potential future additions include:

* orchestration pipelines;
* parameterised deployments;
* environment-specific workspace configuration;
* deployment pipelines;
* Eventstream;
* Eventhouse;
* KQL databases;
* monitoring dashboards;
* data-quality reporting;
* alerting;
* operational metadata tables.

These are roadmap items and must not be described as implemented until they exist.

---

# 12. Repository Structure

The repository follows a separation between application source code, scripts, Fabric-managed assets, documentation, architecture records, and images.

A representative structure is:

```text
atlas/
|
|-- README.md
|-- ATLAS_MASTER_CONTEXT.md
|-- INSTALLATION.md
|-- CHANGELOG.md
|-- RELEASE_HISTORY.md
|-- Development_Workflow.md
|-- requirements.txt
|
|-- src/
|   |-- common/
|       |-- models/
|       |   |-- MarketBar.py
|       |
|       |-- providers/
|       |   |-- IMarketDataProvider.py
|       |   |-- MassiveProvider.py
|       |   |-- CQGLegacyProvider.py
|       |
|       |-- storage/
|           |-- parquet_writer.py
|           |-- BronzeWriter.py
|
|-- scripts/
|   |-- smoke_test_massive_provider.py
|   |-- run_cqg_provider.py
|   |-- validate_cqg_parquet.py
|   |-- analyse_cqg_streaming_profile.py
|
|-- docs/
|   |-- architecture/
|   |-- adr/
|   |-- contracts/
|   |-- images/
|
|-- fabric/
|   |-- notebooks/
|   |-- semantic-model/
|   |-- reports/
|
|-- data/
|   |-- sample/
|
|-- tests/
```

The exact physical structure may differ as Fabric generates and manages item folders. This document should be updated when significant repository restructuring occurs.

Large source datasets, secrets, generated environments, and unnecessary local artifacts must not be committed.

---

# 13. Core Source Components

## 13.1 Provider Interface

```text
IMarketDataProvider.py
```

Defines the abstraction expected from market-data providers.

The objective is to prevent Atlas from becoming tightly coupled to a single external API, vendor, or file format.

## 13.2 CQG Legacy Provider

```text
CQGLegacyProvider.py
```

Reads and interprets the legacy CQG tick-data format while preserving the information required for downstream ordering and transformation.

## 13.3 Massive Provider

```text
MassiveProvider.py
```

Provides the foundation for future API-based market-data acquisition.

It should remain isolated from downstream business logic so that authentication, request handling, pagination, retry behaviour, rate limits, and provider schemas can evolve independently.

## 13.4 Canonical Market Model

```text
MarketBar
```

Represents provider-neutral market-bar data where appropriate.

Tick data and bar data must not be treated as interchangeable without an explicit transformation.

## 13.5 Bronze Storage Components

```text
parquet_writer.py
BronzeWriter.py
```

Encapsulate Bronze persistence behaviour and reduce duplication between provider implementations.

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
gold_minute_candles
gold_daily_candles
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
gold_minute_candles:
one row per instrument per minute

gold_daily_candles:
one row per instrument per trading date
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

Atlas uses ADRs to record decisions with long-term architectural consequences.

The current ADR set covers the following areas.

## ADR-001 — Microsoft Fabric Platform

Records the decision to use Microsoft Fabric as the core integrated Data and AI platform.

## ADR-002 — Medallion Architecture

Records the use of Bronze, Silver, and Gold responsibilities to separate ingestion, standardisation, and analytical presentation.

## ADR-003 — AI-Assisted Development

Records the controlled use of AI assistants during design, implementation, review, and documentation while retaining human ownership of decisions and validation.

## ADR-004 — Direct Lake

Records the use of Direct Lake for reporting over Fabric Gold datasets.

## ADR-005 — Certified Semantic Models

Records the intended direction toward governed, reusable, and potentially certified semantic models as Atlas matures.

## ADR-006 — Bronze Provider Strategy

Records the separation of provider-specific acquisition from common Bronze persistence and downstream transformation.

## ADR-007 — Multi-AI Workflow

Records the principle that different AI tools or providers may be used where appropriate, without allowing the project to become dependent on one assistant or inference provider.

## ADR-008 — Bronze Ingestion

Records the selected Bronze ingestion design, including large-file handling, metadata preservation, Parquet generation, and Fabric loading.

## 18.1 ADR Rules

Create a new ADR when a decision:

* materially changes architecture;
* introduces a major platform dependency;
* changes data contracts;
* changes deployment strategy;
* changes security or governance posture;
* establishes a long-term engineering convention;
* reverses a previous ADR.

Do not create ADRs for minor implementation details that can be adequately explained in code or ordinary documentation.

Accepted ADRs should not be rewritten to conceal historical decisions. If a decision changes, create a superseding ADR.

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

Established the repository, solution structure, provider abstraction, initial development standards, and project foundation.

## v0.2.0 — Bronze Layer

Implemented Bronze ingestion and persistence foundations for market data.

## v0.3.0 — Silver Layer

Introduced the canonical Silver tick model and standardised transformation.

## v0.4.0 — Gold OHLC

Created minute and daily OHLC candle datasets.

## v0.5.0 — Reporting Foundation

Established the semantic-model and Power BI reporting foundation.

## v0.6.0 — Interactive Trading Dashboard

Added interactive report behaviour and candlestick analysis.

## v0.7.0 — Trading Analytics and Report UX

Improved analytical measures, report usability, and trading-focused experience.

## v0.8.0 — AI Trading Intelligence Foundation

Introduced deterministic session analytics and the initial AI architecture.

## v0.9.0 — AI Market Commentary Framework

Added the structured market-commentary generation framework.

## v0.9.1 — Fabric AI Provider Integration

Added and documented Fabric AI provider integration, including the capacity limitation encountered during live inference.

## v1.0.0 — MVP Finalisation

Completed the professional MVP release, including repository presentation, installation guidance, architecture diagrams, release documentation, requirements, and final consistency improvements.

---

# 23. Current Roadmap

The roadmap is incremental and may be refined as implementation discoveries, platform constraints, portfolio priorities, and contract-market opportunities emerge.

The post-MVP sequence deliberately introduces a small near-real-time vertical slice before the wider reporting, multi-instrument, AI, and production streaming phases. This allows Atlas to demonstrate both historical analytics and live market-data ingestion without prematurely implementing the complete real-time architecture.

## v1.1.0 — Near-Real_time Market Data Foundation

Planned focus:

* introduce the first end-to-end streaming market-data pathway;
* connect to a Massive delayed market-data WebSocket feed;
* begin with one event type and one or a small number of liquid instruments;
* create an Atlas Python streaming adapter;
* forward JSON market events into Microsoft Fabric Eventstream;
* route Eventstream output into Eventhouse;
* create a KQL database and raw market-event table;
* preserve provider timestamps and Atlas ingestion metadata;
* validate event arrival, schema, latency, ordering, and record counts;
* create basic KQL queries for current and recent market activity;
* create a minimal real-time dashboard or visual validation experience;
* document the distinction between real-time ingestion and delayed market data;
* add an ADR covering the initial streaming architecture;
* document subscription, licensing, capacity, and environment limitations.

The intended scope is a controlled architectural foundation rather than a production-complete streaming platform.

The initial flow is expected to resemble:

Massive delayed WebSocket
        |
        v
Atlas Python streaming adapter
        |
        v
Microsoft Fabric Eventstream
        |
        v
Eventhouse and KQL Database
        |
        v
Raw near-real-time market events
        |
        v
KQL validation and basic visualisation

This release should prove that Atlas can ingest and analyse continuously arriving market data while preserving the existing historical Lakehouse and medallion architecture.

It should not yet attempt to deliver:

* enterprise-grade continuous hosting;
* broad multi-instrument subscriptions;
* full streaming Silver and Gold models;
* live algorithm execution;
* advanced duplicate or correction handling;
* comprehensive monitoring and alerting;
* production deployment automation;
* historical and streaming reconciliation.

Those capabilities remain part of the later Real-Time Intelligence expansion.

## v1.2.0 — Reporting Navigation and Time Intelligence

Planned focus:

* report drill-through;
* dedicated date dimension;
* improved time intelligence;
* reporting UX refinements;
* clearer navigation between daily and intraday views;
* reusable semantic-model measures;
* documentation updates;
* validation of semantic-model relationships and filtering behaviour.

This release will improve the usability and analytical consistency of the existing historical reporting solution.

## v1.3.0 — Multi-Instrument Architecture

Planned focus:

* support multiple instruments;
* validate provider-neutral canonical modelling;
* introduce or strengthen instrument dimensions;
* distinguish asset class, provider, exchange, and instrument identity;
* review Silver and Gold keys, partitioning, and grain;
* validate aggregation behaviour across instruments;
* improve semantic-model governance;
* progress the certified semantic-model approach;
* assess how historical and streamed instruments should converge on shared domain models.

This release will establish the structural foundations required for Atlas to grow beyond its initial CQG futures dataset and the limited instruments used by the first streaming implementation.

## v1.4.0 — Production-Style AI Inference

Planned focus:

* Azure AI Foundry or Azure OpenAI integration;
* configurable AI providers;
* secure configuration and secret handling;
* prompt templates and prompt versioning;
* structured model inputs and outputs;
* inference logging;
* model and provider traceability;
* validation and fallback behaviour;
* responsible handling of unsupported claims;
* cost and capacity awareness;
* controlled integration with trusted Gold analytical outputs;
* potential commentary across multiple instruments.

The AI layer will continue to consume deterministic analytical results rather than calculate authoritative market facts through generative inference.

## v1.5.0 — Real-Time Intelligence Expansion

Planned focus:

* expand the v1.1.0 streaming foundation into a more complete Real-Time Intelligence architecture;
* support additional instruments and event types;
* improve WebSocket resilience, reconnection, retry, and operational recovery;
* introduce production-style stream hosting;
* implement schema management and evolution controls;
* address duplicate events, corrections, late arrival, and incomplete intervals;
* create streaming transformations;
* develop real-time or near-real-time OHLC aggregations;
* introduce governed KQL functions and reusable query patterns;
* improve Eventhouse and KQL performance design;
* add real-time dashboards;
* introduce configurable alerts and Fabric Activator capabilities where appropriate;
* add operational monitoring, observability, and failure handling;
* reconcile streamed data with historical Lakehouse data;
* define promotion from the streaming hot path into canonical Silver and Gold models;
* establish security, deployment, capacity, and environment-management patterns;
perform performance and cost testing.

The v1.1.0 implementation should therefore be treated as the first vertical slice of this future architecture, not as its completed state.

## v1.6.0 and Beyond

Potential later capabilities:

* technical indicators;
* volatility analytics;
* comparative instrument analysis;
* anomaly detection;
* configurable trading and data-quality alerts;
* AI-assisted market investigation;
* historical market replay;
* strategy-research and backtesting foundations;
* model evaluation;
* data-quality dashboards;
* Fabric pipeline orchestration;
* deployment automation;
* environment promotion;
* CI/CD expansion;
* observability;
* cost monitoring;
* performance optimisation;
* advanced governance;
* security hardening;
* semantic-model certification;
* operational support documentation.

The exact ordering of later capabilities will depend on architectural dependencies, available Fabric capacity, data-provider licensing, portfolio value, and relevance to current contract opportunities.

---

# 24. Immediate Post-MVP Priorities

Before substantial `v1.1.0` feature development:

1. add this master context document;
2. review the repository for references that became outdated at `v1.0.0`;
3. confirm the existing Fabric and GitHub branches are synchronised;
4. define the exact `v1.1.0` scope;
5. review the current semantic model before adding `DimDate`;
6. identify drill-through source and target pages;
7. document any new architectural decisions;
8. implement incrementally;
9. validate report behaviour;
10. complete the release through the established Git workflow.

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

## 26.1 Single Primary Historical Instrument

The current MVP is validated principally against one CQG futures instrument dataset.

Multi-instrument behaviour is a roadmap item.

## 26.2 Historical Batch Focus

The current implementation is batch-oriented.

Real-time ingestion and Eventhouse architecture are planned for later releases.

## 26.3 Limited Hosted AI Execution

Hosted AI inference was constrained by the available Fabric trial capacity and permissions.

The framework exists, but production-style inference requires a suitable deployed model and approved environment.

## 26.4 Development Environment

The current Fabric assets are development-oriented.

A complete multi-environment promotion strategy has not yet been implemented.

## 26.5 Orchestration

Notebook execution is not yet represented as a fully productionised, monitored orchestration pipeline.

## 26.6 Automated Testing

The repository contains validation utilities and engineering checks, but test automation and CI coverage can be expanded.

## 26.7 Governance

Formal certification, endorsement, lineage governance, access control, and operational ownership are roadmap areas rather than fully implemented enterprise controls.

## 26.8 Data Licensing and Distribution

Large proprietary or restricted source datasets must not be distributed through the repository.

The public project should use documentation, schemas, samples, or reproducible instructions where full source data cannot be shared.

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

Atlas validation should operate at several levels.

## 28.1 Source and Provider Validation

* source file exists;
* source file is readable;
* schema is recognised;
* malformed rows are handled deliberately;
* row sequencing is preserved;
* expected source fields are mapped.

## 28.2 Bronze Validation

* expected Parquet files are created;
* source metadata is populated;
* row counts reconcile;
* ordering metadata is unique where required;
* output can be loaded by Fabric.

## 28.3 Silver Validation

* required columns exist;
* types match the Silver contract;
* mandatory values are populated;
* duplicate behaviour is understood;
* source-event order is retained;
* row counts reconcile with accepted transformations.

## 28.4 Gold Validation

For every candle:

```text
high >= open
high >= close
high >= low
low <= open
low <= close
trade_count >= 0
```

Additional checks should include:

* expected candle grain;
* no unintended duplicate keys;
* correct first and last prices;
* correct grouping boundaries;
* date and time consistency;
* reconciliation with Silver events;
* appropriate decimal precision.

## 28.5 Semantic Model Validation

* relationships behave as intended;
* filters propagate correctly;
* measures return expected results;
* date filtering is consistent;
* totals remain meaningful;
* report visuals use governed measures.

## 28.6 AI Validation

* analytical inputs are complete;
* generated commentary reflects supplied facts;
* unsupported claims are avoided;
* missing data is handled explicitly;
* prompt and provider versions are identifiable;
* model failures have a controlled fallback.

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
* Deneb specifications;
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

At the completion of `v1.0.0`, Atlas is:

* a working Microsoft Fabric medallion architecture;
* a large-volume historical market-data engineering solution;
* a Bronze-to-Silver-to-Gold pipeline;
* a Direct Lake reporting platform;
* an interactive Power BI trading analytics solution;
* an extensible AI market-commentary framework;
* a professionally governed GitHub portfolio repository;
* a foundation for multi-instrument, real-time, and advanced AI development.

The next planned release is:

> **Atlas v1.1.0 — Reporting Navigation and Time Intelligence**

The immediate next engineering phase will focus on drill-through, a dedicated date dimension, improved report navigation, semantic-model refinement, and associated documentation.

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
