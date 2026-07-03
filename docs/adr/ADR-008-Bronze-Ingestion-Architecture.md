# ADR-008 – Bronze Ingestion Architecture

- **Status:** Accepted
- **Date:** 2026-07-03
- **Decision Makers:** John McCrae

---

# Context

Atlas is an Enterprise AI Intelligence Platform that ingests financial market data from external providers into Microsoft Fabric.

The first provider integrated into Atlas is the Massive REST API.

Several possible ingestion approaches were considered:

1. Read the API directly from Microsoft Fabric notebooks.
2. Use Python to retrieve data and write directly into Spark DataFrames.
3. Introduce a canonical data model before writing to Microsoft Fabric.

The project aims to support multiple market data providers over time while maintaining a consistent downstream data model.

---

# Decision

Atlas will use the following ingestion architecture:

```
External API
      │
      ▼
Provider Adapter
      │
      ▼
Canonical MarketBar Model
      │
      ▼
Pandas DataFrame
      │
      ▼
Parquet
      │
      ▼
Microsoft Fabric Lakehouse (Bronze)
      │
      ▼
Spark DataFrame
      │
      ▼
Delta Table
```

Each stage performs a single responsibility:

| Component | Responsibility |
|-----------|----------------|
| Provider Adapter | Retrieve provider-specific data |
| MarketBar | Canonical business model |
| DataFrame Transformer | Convert domain objects into tabular data |
| Parquet Writer | Persist data in an open analytical format |
| Fabric Notebook | Load Bronze data into Delta tables |

---

# Rationale

Introducing a canonical MarketBar model decouples Atlas from any individual market data provider.

Future providers can implement the same interface without requiring downstream changes.

Using Pandas before Spark provides several advantages:

- Fast development and debugging
- Simple validation
- Easy local testing
- Straightforward unit testing
- Ability to generate portable Parquet files

Parquet was selected because it is:

- Open standard
- Columnar
- Compressed
- Optimised for analytics
- Natively supported by Microsoft Fabric

Microsoft Fabric then becomes responsible for large-scale distributed processing rather than API integration.

---

# Benefits

- Clean separation of responsibilities
- Provider-independent architecture
- Easier testing
- Easier debugging
- Portable intermediate format
- Compatible with future cloud platforms
- Supports Bronze → Silver → Gold architecture

---

# Consequences

Positive:

- Modular architecture
- Reusable provider implementations
- Reduced coupling
- Easier maintenance
- Easier onboarding of additional providers

Trade-offs:

- One additional transformation step
- Temporary local storage during early development
- Slightly more code than direct notebook ingestion

These trade-offs are considered acceptable in exchange for improved maintainability and extensibility.

---

# Future Evolution

The current implementation writes Parquet files locally before loading them into Microsoft Fabric.

Future versions of Atlas are expected to remove the manual upload step by writing directly to OneLake or Microsoft Fabric storage.

The canonical architecture will remain unchanged; only the storage implementation will evolve.

---

# Status

Accepted as the standard Bronze ingestion architecture for Atlas v0.1.