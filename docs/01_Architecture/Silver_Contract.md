# Atlas Market Data Platform

# Silver Contract

Version: 1.0.0

Status: Approved

---

# Purpose

The Silver layer represents the first curated dataset within the Atlas Market Data Platform.

Its purpose is to transform raw Bronze events into a clean, strongly typed, validated event model while preserving the exact ordering and provenance of every source event.

The Silver layer remains event-level.

No aggregation or business summarisation occurs in Silver.

---

# Objectives

The Silver layer shall:

- Preserve every valid market event.
- Preserve original event ordering.
- Preserve complete source provenance.
- Apply data typing.
- Apply data quality validation.
- Standardise field names.
- Produce a trusted analytical dataset for downstream consumers.

---

# Scope

Input

Bronze Delta table

Output

silver_cqg_ticks

---

# Grain

One row represents one market event from one source file.

No events are combined.

No events are aggregated.

---

# Ordering Principle

CQG legacy market files contain timestamps with minute precision (HHMM).

Since no seconds or milliseconds exist within the source data, Atlas deliberately preserves ordering using sequence numbers rather than inventing timestamps.

The following ordering columns shall be maintained.

## event_sequence_in_file

Represents the absolute ordering of every event within the original source file.

This ordering is immutable.

## event_sequence_in_minute

Represents the ordering of events occurring within the same trading minute.

Sequence numbering restarts at the beginning of every minute.

The first event within a minute shall have a value of 1.

---

# Provenance

The following source metadata shall be preserved.

- source_provider
- source_file_name
- source_file_path
- source_file_row_number
- bronze_loaded_at_utc

Silver adds

- silver_loaded_at_utc

---

# Data Transformations

The Silver layer performs the following transformations.

## Data Typing

Convert raw values into strongly typed business columns.

Examples

- trade_date → DATE
- price_decimal → DECIMAL
- event_minute_ts → TIMESTAMP

## Timestamp Construction

Create

event_minute_ts

using

trade_date + HHMM

No artificial seconds or milliseconds shall be generated.

## Sequence Generation

Generate

event_sequence_in_minute

using the ordering preserved in Bronze.

## Standardisation

Apply consistent naming conventions.

Standardise data types.

Remove implementation-specific formatting.

---

# Data Quality Rules

Every record shall be evaluated against the following rules.

Required

- trade_date exists
- time_hhmm exists
- price_decimal exists
- event_sequence_in_file exists
- source_file_name exists

Validation

- HHMM represents a valid time
- price_decimal > 0

Rows failing validation shall be flagged rather than silently discarded.

---

# Quality Columns

The following quality fields shall be maintained.

- is_valid_time
- is_valid_price
- is_duplicate_source_event
- silver_quality_status

---

# Schema

| Column | Description |
|---------|-------------|
| source_provider | Market data provider |
| instrument_code | Instrument identifier |
| contract_code | Contract identifier |
| trade_date | Trading date |
| time_hhmm | Original HHMM value |
| event_minute_ts | Minute-level timestamp |
| price_decimal | Parsed market price |
| event_sequence_in_file | Original ordering within source file |
| event_sequence_in_minute | Ordering within trading minute |
| source_file_row_number | Original file row |
| source_file_name | Source filename |
| source_file_path | Original source path |
| is_valid_time | Time validation flag |
| is_valid_price | Price validation flag |
| is_duplicate_source_event | Duplicate detection flag |
| silver_quality_status | Overall quality status |
| bronze_loaded_at_utc | Bronze ingestion timestamp |
| silver_loaded_at_utc | Silver processing timestamp |

---

# Design Principles

The Silver layer shall:

- Preserve every valid event.
- Never invent market data.
- Never fabricate timestamps.
- Preserve deterministic ordering.
- Preserve complete lineage.
- Remain provider-specific.
- Avoid aggregation.
- Produce a trusted analytical dataset.

---

# Event Identity

Each Silver event is uniquely identified by the combination of:

- source_provider
- source_file_name
- event_sequence_in_file

No surrogate key shall be generated within the Silver layer.

Surrogate keys, if required, belong to downstream analytical models.

---

# Future Evolution

Future versions of Silver may include

- duplicate detection across files
- trading session classification
- exchange calendar enrichment
- contract metadata enrichment
- trading day dimension joins
- canonical market event model

These enhancements shall remain non-aggregated.

Aggregation belongs exclusively within the Gold layer.

---

# Ownership

Atlas Market Data Platform

Layer

Silver

Status

Production Design