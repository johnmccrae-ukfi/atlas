# ADR-002: Why Medallion Architecture?

## Status

Accepted

## Date

2026-06-30

---

## Context

Atlas requires a scalable, maintainable and auditable data architecture capable of supporting both the MVP and future commercial releases.

The platform must support:

- Multiple external market data sources
- Incremental data ingestion
- Data quality validation
- Historical replay
- Analytics-ready datasets
- AI-driven intelligence
- Future real-time processing

The architecture should also demonstrate industry best practice for Microsoft Fabric and modern Data Engineering.

---

## Decision

Atlas will implement a **Medallion Architecture** consisting of Bronze, Silver and Gold layers.

The Medallion Architecture will become the standard data pattern across Atlas and future UKFI intelligence platforms.

---

## Why Medallion?

The Medallion Architecture separates data according to its level of refinement.

Rather than continually modifying the same dataset, each stage has a clearly defined responsibility.

This improves:

- Data quality
- Traceability
- Maintainability
- Testing
- Reusability
- Explainability

It also aligns closely with Microsoft Fabric best practice.

---

## Bronze Layer

### Purpose

Store raw source data exactly as received.

### Characteristics

- Minimal transformation
- Immutable where practical
- Historical record retained
- Supports replay and auditing

Typical contents include:

- Market prices
- Trading volumes
- Instrument reference data
- Exchange metadata
- Future news feeds

Bronze answers the question:

> "What did the source system actually send us?"

---

## Silver Layer

### Purpose

Create trusted operational datasets.

Typical processing includes:

- Data cleansing
- Standardisation
- Missing value handling
- Duplicate removal
- Data quality validation
- Type conversion
- Business rule validation

Silver answers:

> "What data can we trust?"

---

## Gold Layer

### Purpose

Provide business-ready analytics.

Gold datasets are optimised for:

- Power BI
- KPI reporting
- Trading indicators
- Signal generation
- AI analysis
- Future APIs

Typical entities include:

- Instrument Dimension
- Date Dimension
- Price Fact
- Indicator Fact
- Signal Fact
- Portfolio Fact

Gold answers:

> "What insight can we generate?"

---

## Data Flow

```text
External Data

        │

        ▼

 Bronze (Raw)

        │

        ▼

 Silver (Trusted)

        │

        ▼

 Gold (Business Ready)

        │

        ▼

Analytics

AI

Dashboards

Future APIs
```

---

## Benefits

### Data Quality

Errors are isolated before reaching reporting.

### Traceability

Every Gold record can be traced back to its original source.

### Maintainability

Each transformation has a single responsibility.

### Reprocessing

Historical data can be rebuilt without re-ingesting external feeds.

### AI Readiness

AI models receive consistent, validated datasets.

### Scalability

New sources can be added without redesigning downstream analytics.

### Portfolio Reuse

Future UKFI products can adopt the same architecture.

---

## Alternatives Considered

### Single Database

Store everything in one relational model.

**Rejected because:**

- Difficult to separate raw and curated data.
- Harder to audit.
- Less scalable.
- Poor alignment with Fabric best practice.

---

### Direct Reporting from Raw Data

Connect Power BI directly to source data.

**Rejected because:**

- Poor performance.
- Data quality issues.
- Difficult to maintain.
- Limited governance.

---

### ELT into Warehouse Only

Load directly into a warehouse.

**Rejected because:**

- Raw history lost.
- Reduced flexibility.
- Harder to replay ingestion.
- Less suitable for AI and future workloads.

---

## Consequences

### Positive

- Clear separation of responsibilities.
- Supports enterprise governance.
- Enables future AI capability.
- Aligns with Microsoft guidance.
- Easy to explain during client engagements.
- Demonstrates modern Data Engineering practice.

### Negative

- Additional storage required.
- More transformation steps.
- Slightly higher implementation effort.
- Requires discipline to maintain boundaries between layers.

---

## Risks

| Risk | Mitigation |
|-------|------------|
| Duplicate logic across layers | Keep each layer focused on a single responsibility. |
| Scope creep | Maintain strict Bronze → Silver → Gold progression. |
| Over-engineering | Build only the layers required for the MVP. |
| Performance issues | Optimise transformations incrementally as the platform grows. |

---

## Future Evolution

Future releases may extend the architecture with:

- Eventhouse
- Streaming ingestion
- Delta tables
- Feature engineering
- Machine Learning datasets
- AI vector indexes
- Real-time intelligence
- Databricks integration where appropriate

The Bronze, Silver and Gold principles will remain unchanged.

---

## Relationship to ADR-001

ADR-001 selected Microsoft Fabric as the strategic platform.

ADR-002 defines the preferred data architecture implemented within that platform.

Together these ADRs establish the core architectural foundation for Atlas.

---

## Decision Summary

Atlas will use the Medallion Architecture because it provides a scalable, maintainable and enterprise-aligned approach to organising data.

It supports Microsoft Fabric best practice, improves data quality and governance, enables future AI capabilities and creates a reusable architectural pattern for future UKFI products.