# Atlas Architecture

**Version:** 1.0  
**Status:** Draft  
**Last Updated:** July 2026

## Related Documents

This document provides the architectural overview.

For detailed information, see:

- Logical_Architecture.md
- Physical_Architecture.md
- Solution_Architecture.md
- Technology_Decisions.md
- Security.md

For architectural decisions, see:

- ADR-001 onwards in the `/docs/adr` folder.

---

# 1. Vision

Atlas is a modular market data engineering platform designed to ingest, normalise, store and analyse financial market data from multiple heterogeneous sources.

The platform is being developed as a production-quality Microsoft Fabric solution while remaining cloud-agnostic through the use of abstraction layers.

Atlas demonstrates modern Data Engineering principles including:

- Provider-based data ingestion
- Bronze / Silver / Gold architecture
- Modular storage abstraction
- Streaming data processing
- Reusable components
- Infrastructure as Code
- AI-assisted software engineering

The project serves both as a professional portfolio and as the foundation for future quantitative market research.

---

# 2. Design Principles

Atlas is built around several core principles.

## 2.1 Separation of Concerns

Each component has a single responsibility.

Examples include:

- Providers retrieve data
- Writers persist data
- Profilers analyse data
- Analytics consume data

Each layer is independent and interchangeable.

---

## 2.2 Reusable Components

Components should be reusable across multiple data providers.

The same Bronze writer should be capable of writing data from:

- CQG Legacy
- Massive API
- Interactive Brokers
- Future providers

without modification.

---

## 2.3 Streaming First

Large datasets should never require loading entirely into memory.

Providers process data using chunked streaming wherever possible.

This allows Atlas to process datasets containing tens or hundreds of millions of market events.

---

## 2.4 Preserve Vendor Data

The Bronze layer preserves vendor supplied data with minimal transformation.

Derived values are added without removing original values.

Example:

```
price_raw
price_decimal
```

Both values are retained.

---

# 3. High Level Architecture

```
                 +----------------+
                 |  Data Sources  |
                 +----------------+
                    |       |
          +---------+       +----------+
          |                            |
     Massive API                CQG Legacy
          |                            |
          +-------------+--------------+
                        |
                 Provider Layer
                        |
                 Bronze Writer
                        |
                 Bronze Storage
                        |
                 Silver Processing
                        |
                 Gold Analytics
                        |
              Reports / ML / AI
```

---

# 4. Current Components

## Providers

Current providers:

- MassiveProvider
- CQGLegacyProvider

Planned providers:

- Interactive Brokers
- Polygon.io
- AlphaVantage
- Custom CSV providers

---

## Writers

Current writers:

- BronzeWriter

Planned writers:

- FabricBronzeWriter
- DeltaWriter
- ADLSWriter

---

## Profilers

Current:

- CQG investigation scripts

Planned:

- BaseProfiler
- CQGProfiler
- MassiveProfiler

---

# 5. Bronze Layer

The Bronze layer represents the immutable source of truth.

Responsibilities include:

- Preserve original vendor fields
- Add metadata
- Record ingestion timestamps
- Maintain source ordering
- Persist as Parquet

Typical metadata:

- source_file
- source_row_number
- loaded_at_utc

No business rules are applied in Bronze.

---

# 6. Silver Layer

The Silver layer performs data normalisation.

Examples include:

- Common timestamp formats
- Normalised instruments
- Market calendars
- Data quality validation
- Derived market features

The Silver layer converts multiple vendor formats into a common market data model.

---

# 7. Gold Layer

The Gold layer provides analytical datasets.

Examples include:

- Market microstructure
- Bid / Ask analytics
- Trade analytics
- Liquidity measures
- Volatility metrics
- Feature engineering
- Machine Learning datasets

---

# 8. Repository Structure

```
src/
    common/
        providers/
        writers/
        profiling/

scripts/
    run_cqg_provider.py
    run_massive_provider.py

data/
    bronze/
    sample/
    reference/

docs/
    01_Architecture/
    02_Product/
    03_Intelligence/

adr/
```

---

# 9. Current Status

Completed

- Massive API provider
- CQG Legacy provider
- Bronze Writer
- Chunked streaming
- Local Bronze Parquet generation
- Dataset profiling framework

In Progress

- Architecture documentation
- Provider abstraction
- Bronze ingestion framework

Planned

- Fabric Bronze Writer
- Silver transformations
- Gold analytical models
- Semantic Models
- Power BI reporting
- AI-assisted analytics

---

# 10. Technology Stack

Current technologies include:

- Python
- Pandas
- PyArrow
- Microsoft Fabric
- OneLake
- GitHub
- VS Code

Planned technologies include:

- Delta Lake
- DuckDB
- Power BI
- Semantic Models
- Azure Functions
- Microsoft Fabric Pipelines

---

# 11. Future Roadmap

Short Term

- Complete Bronze ingestion
- Fabric integration
- Silver layer
- Common provider framework

Medium Term

- Gold analytical models
- Market microstructure analytics
- Feature engineering

Long Term

- Machine Learning
- Strategy research
- AI-assisted quantitative analysis
- Multi-provider market data platform

---

# 12. Architectural Philosophy

Atlas is intentionally designed around abstraction rather than implementation.

Providers should not know where data is stored.

Writers should not know how data was retrieved.

Analytics should not know which vendor supplied the data.

This separation enables Atlas to scale from a local development environment to a production Microsoft Fabric platform with minimal architectural change.

---

*"Good architecture allows new functionality to be added by extending the platform rather than rewriting it."*