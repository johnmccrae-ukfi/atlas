# Fabric Bronze Ingestion

**Version:** 1.0  
**Status:** Draft  
**Last Updated:** July 2026

---

# 1. Purpose

This document defines how Atlas Bronze data should be ingested into Microsoft Fabric.

The goal is to move from local Bronze Parquet files to a Fabric Lakehouse while preserving the same provider / writer architecture.

---

# 2. Current Local Bronze Pattern

Atlas currently uses the following pattern:

```text
Source Data
    ↓
Provider
    ↓
BronzeWriter
    ↓
Local Parquet Files
```

Example:

```text
F.US.EU6M12_201203.ts
    ↓
CQGLegacyProvider
    ↓
BronzeWriter
    ↓
data/bronze/cqg/
```

The local Bronze output has already been validated against the source row count.

---

# 3. Fabric Target Pattern

The Fabric target pattern should become:

```text
Source Data
    ↓
Provider
    ↓
FabricBronzeWriter
    ↓
OneLake / Lakehouse Bronze Area
```

The provider must not change when switching from local storage to Fabric storage.

Only the writer should change.

---

# 4. Design Principle

Providers are responsible for reading and normalising source data.

Writers are responsible for persistence.

Therefore:

- `CQGLegacyProvider` does not know about Fabric.
- `MassiveProvider` does not know about Fabric.
- `FabricBronzeWriter` does not know about CQG internals.

This separation keeps Atlas modular, reusable and testable.

---

# 5. Recommended Lakehouse Layout

Initial Bronze layout:

```text
Files/
└── bronze/
    └── cqg/
        └── legacy/
            └── futures/
                └── F_US_EU6M12/
                    └── 201203/
                        ├── cqg_F_US_EU6M12_201203_chunk_0001.parquet
                        ├── cqg_F_US_EU6M12_201203_chunk_0002.parquet
                        └── ...
```

This layout preserves:

- Provider
- Data family
- Asset class
- Instrument
- Contract month
- Chunk identity

---

# 6. Bronze File Naming Convention

Recommended filename format:

```text
{provider}_{instrument}_{contract_month}_chunk_{chunk_number}.parquet
```

Example:

```text
cqg_F_US_EU6M12_201203_chunk_0001.parquet
```

Each file can be identified without opening it.

---

# 7. Bronze Schema

CQG Legacy Bronze currently includes:

```text
source_file
source_row_number
instrument
trade_date_raw
unknown_raw
time_raw
price_raw
event_type
flag1
flag2
size
trade_date
time_hhmm
price_decimal
loaded_at_utc
```

Original vendor fields are always preserved.

Derived fields are additive only.

---

# 8. Delta vs Parquet

For the initial Fabric implementation Atlas will load Bronze as **Parquet files** into the Lakehouse **Files** area.

Reasons:

- Matches the local development architecture
- Preserves raw Bronze files
- Avoids unnecessary Spark complexity during initial development
- Allows later promotion into Delta tables

Future flow:

```text
Bronze Parquet Files
        │
        ▼
Fabric Notebook / Pipeline
        │
        ▼
Bronze Delta Table
        │
        ▼
Silver Tables
```

---

# 9. Partitioning Strategy

Initial folder hierarchy:

```text
provider
    data_family
        asset_class
            instrument
                contract_month
```

Example:

```text
cqg
 └── legacy
      └── futures
            └── F_US_EU6M12
                    └── 201203
```

Future Delta partition candidates include:

- Provider
- Instrument
- Contract month
- Trade date

Partitioning should remain simple until query patterns are understood.

---

# 10. Metadata Requirements

Every Bronze record should include:

```text
source_file
source_row_number
loaded_at_utc
```

Future metadata may include:

```text
provider_name
ingestion_run_id
source_file_hash
bronze_file_name
source_system
```

These support lineage, auditing and reprocessing.

---

# 11. Validation Requirements

Every ingestion should validate:

- Source row count
- Bronze row count
- Number of chunks written
- File naming convention
- Schema consistency

Current validation script:

```text
scripts/validate_cqg_bronze.py
```

Future validation should generate an ingestion manifest.

Example:

```json
{
  "provider": "cqg",
  "source_file": "F.US.EU6M12_201203.ts",
  "source_rows": 17317408,
  "bronze_rows": 17317408,
  "chunks_written": 18,
  "status": "passed"
}
```

---

# 12. FabricBronzeWriter Responsibilities

`FabricBronzeWriter` should:

- Accept a DataFrame chunk
- Accept provider metadata
- Build the OneLake destination path
- Write Parquet files into the Lakehouse Files area
- Return the written destination

It should **not**:

- Parse CQG files
- Perform Silver transformations
- Apply business rules
- Know anything about market structure

---

# 13. Open Decisions

The following architectural decisions remain open:

- Should Bronze remain Files-only or also become managed Delta tables?
- Should ingestion run locally or inside Fabric notebooks?
- Should OneLake writes use mounted paths, REST APIs or notebook copy operations?
- Should ingestion manifests be stored as JSON or Delta tables?
- Should original vendor files also be archived into OneLake?

These decisions should be resolved before production deployment.

---

# 14. Initial Implementation Plan

## Phase 1

Continue generating validated Bronze Parquet locally.

## Phase 2

Copy Bronze Parquet into the Fabric Lakehouse Files area.

## Phase 3

Create a Fabric Notebook to inspect and validate the Bronze files.

## Phase 4

Create Bronze Delta tables from the Parquet files.

## Phase 5

Begin implementation of the Silver normalisation layer.

---

# 15. Summary

The Fabric Bronze ingestion layer extends the Atlas architecture rather than replacing it.

The key architectural principle is:

```text
Change the writer, not the provider.
```

This allows Atlas to support local development, Microsoft Fabric, Azure Data Lake Storage and future cloud platforms using exactly the same provider framework.

The ingestion architecture has already been proven against a complete CQG legacy futures dataset containing over **17 million market events**, providing confidence that the design can scale to significantly larger historical datasets and additional market data providers.