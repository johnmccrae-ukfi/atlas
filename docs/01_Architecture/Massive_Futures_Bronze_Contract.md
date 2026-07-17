# Massive Futures Bronze Contract

## Document Status

**Version:** 1.0.0  
**Status:** Proposed for `v1.3.0` implementation  
**Target Release:** `v1.3.0 — Multi-Instrument Architecture`  
**Layer:** Bronze  
**Source Provider:** Massive  
**Dataset:** Futures minute aggregates  
**Initial Scope:** `MESU6` and `MNQU6`

---

# 1. Purpose

This contract defines the Bronze-layer requirements for ingesting Massive Futures historical minute aggregates into the Atlas Lakehouse.

The Bronze layer preserves source-aligned provider data and complete ingestion lineage.

It does not:

- create Atlas canonical contract identity;
- apply business aggregation;
- resolve conflicting provider records;
- generate Silver or Gold analytical values;
- perform automatic futures-contract rollover;
- create continuous contracts;
- reconcile historical data with the near-real-time Eventhouse pathway.

The Bronze layer must provide a replayable and traceable source foundation for downstream Silver validation.

---

# 2. Scope

## 2.1 Source

The source is the Massive Futures Flat Files S3-compatible object store.

The initial source dataset is:

```text
us_futures_cme/minute_aggs_v1
```

The source consists of compressed daily CSV objects containing provider-generated minute aggregates for multiple CME Futures products and contracts.

## 2.2 Initial Selected Contracts

The initial v1.3.0 ingestion scope is:

```text
MESU6
MNQU6
```

These represent:

```text
MESU6
Micro E-mini S&P 500
September 2026 contract
```

```text
MNQU6
Micro E-mini Nasdaq-100
September 2026 contract
```

The source object may contain many additional provider tickers.

The initial Atlas ingestion shall retain only the explicitly approved contract scope unless the notebook is deliberately run in an approved source-profiling mode.

## 2.3 Target Table

The Bronze Delta table is:

```text
bronze_massive_futures_minute_aggregates
```

## 2.4 Initial Controlled Source Object

The first implementation shall ingest one explicitly selected daily source object.

The initial validated development object is:

```text
us_futures_cme/minute_aggs_v1/2026/07/2026-07-14.csv.gz
```

The source object must be supplied explicitly through notebook configuration.

The notebook must not silently select the latest available object.

---

# 3. Source Schema

The validated Massive Futures minute-aggregate source schema is:

```text
ticker
exchange
session_end_date
window_start
open
high
low
close
volume
dollar_volume
transactions
```

## 3.1 Source Field Meanings

### ticker

The provider-specific Futures contract symbol.

Examples:

```text
MESU6
MNQU6
```

The ticker is a source identifier.

It is not the permanent Atlas canonical contract key.

### exchange

A provider-supplied numeric exchange code contained in the Flat File.

Observed examples include:

```text
4
11
12
```

The Bronze layer shall preserve this value without translating it into an Atlas venue.

### session_end_date

The provider-supplied Futures session date.

This value is distinct from the UTC calendar date of `window_start`.

Bronze shall preserve it exactly as supplied.

### window_start

The provider-supplied minute-window start represented as Unix epoch nanoseconds.

Bronze shall preserve the original nanosecond value.

Timestamp conversion belongs to Silver.

### open

Provider-supplied minute Open price.

### high

Provider-supplied minute High price.

### low

Provider-supplied minute Low price.

### close

Provider-supplied minute Close price.

### volume

Provider-supplied minute volume.

### dollar_volume

Provider-supplied minute dollar volume.

### transactions

Provider-supplied minute transaction count.

---

# 4. Grain

The physical Bronze grain is:

> One row per accepted physical CSV source row.

Bronze does not assume that:

```text
ticker + window_start
```

is physically unique.

The source may contain:

- unique minute rows;
- exact duplicate rows;
- conflicting rows with the same apparent business key;
- rows for products and contracts outside the approved Atlas scope.

Bronze preserves accepted physical source rows before downstream reconciliation.

---

# 5. Physical Source Identity

Each Bronze row shall be identified through source lineage rather than through the expected provider business grain.

The physical source identity is:

```text
source_provider
+ source_dataset
+ source_object_key
+ source_row_number
```

## 5.1 source_provider

For this contract:

```text
Massive
```

## 5.2 source_dataset

For this contract:

```text
us_futures_cme/minute_aggs_v1
```

## 5.3 source_object_key

The complete object-store key of the source Flat File.

Example:

```text
us_futures_cme/minute_aggs_v1/2026/07/2026-07-14.csv.gz
```

## 5.4 source_row_number

The one-based physical data-row position within the decompressed CSV source object.

The CSV header is not counted as a data row.

The first data record shall have:

```text
source_row_number = 1
```

`source_row_number` is immutable lineage metadata.

It is not:

- an exchange sequence;
- a trade sequence;
- a market-event sequence;
- a correction-precedence indicator;
- a substitute for timestamp ordering.

---

# 6. Proposed Bronze Schema

The initial Bronze table shall contain:

```text
source_provider
source_dataset
source_object_key
source_row_number
provider_ticker
provider_exchange_code
session_end_date_raw
window_start_ns
open_raw
high_raw
low_raw
close_raw
volume_raw
dollar_volume_raw
transactions_raw
bronze_loaded_at_utc
```

---

# 7. Physical Data Types

The proposed initial physical schema is:

```text
source_provider         STRING
source_dataset          STRING
source_object_key       STRING
source_row_number       BIGINT
provider_ticker         STRING
provider_exchange_code  STRING
session_end_date_raw    STRING
window_start_ns         BIGINT
open_raw                STRING
high_raw                STRING
low_raw                 STRING
close_raw               STRING
volume_raw              STRING
dollar_volume_raw       STRING
transactions_raw        STRING
bronze_loaded_at_utc    TIMESTAMP
```

## 7.1 Raw Field Preservation

The following fields shall initially remain strings:

```text
session_end_date_raw
open_raw
high_raw
low_raw
close_raw
volume_raw
dollar_volume_raw
transactions_raw
```

This preserves the provider representation before Silver typing and validation.

For example, source prices may be represented as:

```text
7558.250000000
0.186000000
0.006187500
```

Bronze shall not prematurely reduce this source scale to `Decimal(18,5)`.

The governed analytical conversion to `Decimal(18,5)` applies later to the approved initial instruments after Silver validates that conversion is lossless.

## 7.2 Nanosecond Timestamp Preservation

The source `window_start` value shall be stored as:

```text
window_start_ns BIGINT
```

Bronze shall not:

- truncate the value;
- convert it to milliseconds;
- derive a local timestamp;
- derive `TradingDate`;
- infer an exchange timezone.

Timestamp construction and minute-boundary validation belong to Silver.

## 7.3 Exchange Code Preservation

The provider `exchange` value shall be stored as:

```text
provider_exchange_code STRING
```

It shall remain source-aligned until an authoritative Atlas exchange-code mapping has been approved.

---

# 8. Bronze Responsibilities

The Bronze process shall:

- connect to the configured Massive Flat Files object store;
- retrieve one explicitly configured source object;
- decompress the source object;
- read the CSV header;
- validate the expected source column names;
- preserve accepted physical source rows;
- assign deterministic one-based source row numbers;
- retain source object lineage;
- retain provider ticker values;
- retain provider exchange codes;
- retain raw session dates;
- retain raw nanosecond timestamps;
- retain raw OHLC values;
- retain raw activity values;
- populate one consistent Bronze load timestamp;
- filter to the approved initial contract scope;
- write the result as a Delta table;
- validate the persisted result.

---

# 9. Bronze Exclusions

The Bronze process shall not:

- construct `AtlasProductKey`;
- construct `AtlasContractKey`;
- construct Atlas business keys;
- join to `gold_dim_instrument`;
- translate provider tickers;
- translate provider exchange codes;
- derive `MinuteTimestamp`;
- derive `TradingDate`;
- cast prices to governed analytical precision;
- validate OHLC relationships;
- calculate daily candles;
- calculate indicators;
- calculate moving averages;
- generate event sequences;
- select a preferred conflicting duplicate;
- silently discard duplicate rows;
- combine Massive data with CQG data;
- populate the Eventhouse near-real-time pathway;
- implement contract rollover.

---

# 10. Contract Selection

The initial selected provider tickers are:

```text
MESU6
MNQU6
```

The selected ticker list shall be explicit and source-controlled.

The notebook shall not infer the selected contracts from:

- current date;
- active-contract status;
- highest volume;
- provider result ordering;
- expiry proximity;
- previous notebook output;
- near-real-time subscription state.

Adding another contract requires an intentional design and configuration change.

This rule prevents accidental implementation of automatic rollover.

---

# 11. Source Header Validation

Before processing data rows, the notebook must validate that the source object contains exactly the required columns:

```text
ticker
exchange
session_end_date
window_start
open
high
low
close
volume
dollar_volume
transactions
```

Processing must stop if:

- a required column is absent;
- a source column is unexpectedly renamed;
- duplicate column names are present;
- the source cannot be parsed as the expected CSV structure.

Additional source columns must not be silently incorporated into the governed Bronze schema.

A deliberate schema review is required before contract evolution.

---

# 12. Source Row Numbering

`source_row_number` shall represent the physical data-row order in the decompressed source object.

Requirements:

- numbering starts at 1;
- the header is excluded;
- rows filtered out because their ticker is outside the initial scope retain no Bronze record;
- selected rows retain their original source position;
- row numbers must not be regenerated after ticker filtering;
- rerunning the same unchanged object must produce the same source row numbers.

The implementation must therefore assign physical row numbers before applying the approved ticker filter.

---

# 13. Duplicate Preservation

Source profiling identified conflicting records at the apparent business grain:

```text
provider_ticker
+ window_start_ns
```

The conflicting rows contained different OHLC and activity values.

Therefore, Bronze shall preserve:

- exact duplicate rows;
- conflicting duplicate rows;
- all selected physical source occurrences.

Bronze shall not use:

```text
dropDuplicates()
distinct()
groupBy()
first()
last()
max(volume)
max(transactions)
```

to select or collapse source rows.

Duplicate classification and trusted-row decisions belong to Silver.

---

# 14. Idempotency

Reprocessing the same configured source object and selected ticker scope shall produce the same business data and lineage rows.

For the first controlled implementation, the target table may be written using:

```text
mode("overwrite")
```

provided that:

- the notebook scope is one explicitly configured source object;
- the operation is documented as a controlled development load;
- persisted validation runs immediately after writing;
- no assumption is made that overwrite is the final production ingestion strategy.

A future multi-object implementation will require an approved incremental or merge strategy.

---

# 15. Load Timestamp

All rows created during one notebook execution shall use one consistent:

```text
bronze_loaded_at_utc
```

The timestamp shall be generated once per run and applied to every accepted Bronze row.

It must not be generated independently for each row.

`bronze_loaded_at_utc` records Atlas ingestion time.

It is not a source-market timestamp.

---

# 16. Credentials and Security

Massive object-store credentials must be obtained from secure runtime configuration.

Expected local environment variables include:

```text
MASSIVE_S3_ACCESS_KEY
MASSIVE_S3_SECRET_KEY
```

Credentials must not be:

- hard-coded in the Fabric notebook;
- written to notebook output;
- stored in the Delta table;
- added to Markdown documentation;
- committed to GitHub;
- embedded in screenshots;
- included in exception text.

The final production credential mechanism remains future work.

---

# 17. Public Repository Rules

Massive market-data files are proprietary subscription data.

The following must not be committed to the public Atlas repository:

- downloaded CSV files;
- compressed Flat Files;
- extracts containing market rows;
- parquet copies;
- Delta table data;
- access keys;
- secret keys;
- signed URLs;
- provider responses containing credentials.

The repository may contain:

- ingestion code;
- schemas;
- contracts;
- validation logic;
- redacted output examples;
- aggregate row counts;
- non-sensitive metadata;
- source object-key patterns where permitted.

---

# 18. Initial Validation Requirements

## 18.1 Source Validation

The notebook must confirm:

- the configured source object exists;
- the source object can be retrieved;
- the object can be decompressed;
- the CSV header matches the expected schema;
- the source contains data rows;
- `MESU6` exists in the source;
- `MNQU6` exists in the source.

## 18.2 Physical Lineage Validation

The notebook must confirm:

- `source_provider` is always `Massive`;
- `source_dataset` is always the configured dataset;
- `source_object_key` is always the configured object;
- `source_row_number` is non-null;
- `source_row_number` is positive;
- physical source identity is unique;
- one consistent `bronze_loaded_at_utc` value exists for the run.

## 18.3 Selected Scope Validation

The notebook must confirm:

```text
provider_ticker IN ("MESU6", "MNQU6")
```

No unapproved ticker may enter the initial target table.

For the validated development object, the expected initial counts are:

```text
MESU6:  1,380 rows
MNQU6:  1,380 rows
Total:  2,760 rows
```

These are initial controlled-file expectations rather than universal daily invariants.

The notebook must not assume every future trading session always contains exactly 1,380 bars.

## 18.4 Raw Field Validation

Bronze must confirm required source fields were captured, but it shall not classify business validity.

The following fields must be present in the parsed source structure:

```text
provider_ticker
provider_exchange_code
session_end_date_raw
window_start_ns
open_raw
high_raw
low_raw
close_raw
volume_raw
dollar_volume_raw
transactions_raw
```

Business validation of their values belongs to Silver.

## 18.5 Persistence Validation

After writing the Delta table, the notebook must confirm:

- persisted row count matches the prepared Bronze DataFrame;
- persisted schema matches the governed Bronze schema;
- physical source identity remains unique;
- only approved tickers are present;
- source row numbers are retained;
- the expected source object key is retained;
- no row was introduced or lost during persistence.

Any failed validation must stop the notebook.

---

# 19. Expected Initial Output

For the initial controlled source object, the target table is expected to contain:

```text
2,760 rows
```

comprising:

```text
1,380 MESU6 rows
1,380 MNQU6 rows
```

The exact source row numbers are determined by the original position of those records within the exchange-wide CSV object.

The output shall contain no other provider ticker.

---

# 20. Relationship to Silver

The downstream Silver table is proposed as:

```text
silver_massive_futures_minute_aggregates
```

Silver will be responsible for:

- parsing `session_end_date_raw` as a date;
- converting `window_start_ns` to a UTC minute timestamp;
- strongly typing OHLC and activity values;
- validating timestamp boundaries;
- validating OHLC relationships;
- validating non-negative activity values;
- mapping provider tickers to `AtlasContractKey`;
- detecting duplicate business keys;
- distinguishing exact from conflicting duplicates;
- stopping trusted processing when conflicting duplicates affect selected contracts;
- creating Silver quality fields.

Bronze must retain sufficient lineage for every Silver row to be traced back to its physical source record.

---

# 21. Relationship to Gold

Bronze does not directly populate Gold.

The downstream Gold tables are proposed as:

```text
gold_massive_futures_minute_candles
gold_massive_futures_daily_candles
```

Gold will consume only trusted Silver rows.

The governed instrument dimension is:

```text
gold_dim_instrument
```

Bronze shall not join to or depend on this Gold dimension.

---

# 22. Relationship to the Near-Real-Time Pathway

Atlas already contains a separate Massive near-real-time pathway:

```text
Massive WebSocket
        |
        v
local streaming adapter
        |
        v
Fabric Eventstream
        |
        v
Eventhouse / KQL database
```

The historical Flat File Bronze pathway is separate:

```text
Massive Futures Flat File
        |
        v
bronze_massive_futures_minute_aggregates
        |
        v
future historical Silver and Gold tables
```

The Bronze contract does not approve:

- historical and streaming reconciliation;
- Eventhouse-to-Lakehouse replication;
- common physical ingestion tables;
- late-event correction handling;
- streaming contract rollover.

These remain future architectural decisions.

---

# 23. Operational Boundaries

The initial notebook is a controlled development implementation.

It is not yet:

- production-orchestrated;
- scheduled;
- incremental across many source objects;
- retry-managed;
- parameterised through a deployment pipeline;
- integrated with formal secrets management;
- monitored through production alerts;
- designed for broad provider backfill.

Those capabilities require later design and operational contracts.

---

# 24. Success Criteria

This Bronze contract is satisfied when:

1. One explicitly configured Massive daily minute-aggregate object is retrieved successfully.
2. The expected source header is validated.
3. Physical source row order is preserved through one-based row numbering.
4. Only `MESU6` and `MNQU6` are retained for the initial implementation.
5. Every accepted row retains complete object and row lineage.
6. Raw source values are preserved without premature analytical conversion.
7. Raw nanosecond timestamps are retained.
8. Provider exchange codes remain source-aligned.
9. No Atlas contract keys are added in Bronze.
10. No duplicate source rows are collapsed.
11. The Delta table is written successfully.
12. Persisted row counts reconcile with the prepared Bronze DataFrame.
13. The initial controlled file produces the validated expected counts.
14. Credentials and proprietary data remain outside the public repository.
15. Failed validation stops the notebook rather than producing an untrusted table.

---

# 25. Exclusions

The following are outside this Bronze contract:

- automatic contract discovery;
- automatic contract rollover;
- continuous contracts;
- contract-chain ingestion;
- broad exchange-wide persistence;
- multiple daily-file ingestion;
- Trades Flat Files;
- Quotes Flat Files;
- session aggregates;
- COMEX ingestion;
- CBOT ingestion;
- NYMEX ingestion;
- Silver typing;
- OHLC business validation;
- provider correction precedence;
- duplicate resolution;
- instrument-dimension enrichment;
- semantic-model relationships;
- Power BI changes;
- production orchestration;
- historical and streaming reconciliation.

---

# 26. Future Evolution

Future Bronze versions may include:

- parameterised date ranges;
- multi-object ingestion;
- incremental Delta processing;
- object manifest tables;
- ingestion status and audit tables;
- controlled replay;
- provider file checksums;
- schema-version tracking;
- additional approved contracts;
- additional Futures venues;
- production secret management;
- orchestration and monitoring.

These enhancements must preserve the core Bronze principles:

- source fidelity;
- physical lineage;
- replayability;
- no arbitrary deduplication;
- no silent business assumptions.

---

# 27. Ownership

**Platform:** Atlas Market Data Platform  
**Layer:** Bronze  
**Provider:** Massive  
**Dataset:** Futures minute aggregates  
**Target Table:** `bronze_massive_futures_minute_aggregates`  
**Status:** Proposed for controlled v1.3.0 implementation