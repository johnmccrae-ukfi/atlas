# Massive Futures Silver Contract

## Document Status

**Version:** 1.0.0  
**Status:** Proposed for `v1.3.0` implementation  
**Target Release:** `v1.3.0 — Multi-Instrument Architecture`  
**Layer:** Silver  
**Source Provider:** Massive  
**Dataset:** Futures minute aggregates  
**Initial Scope:** `MESU6` and `MNQU6`

---

# 1. Purpose

This contract defines the Silver-layer requirements for transforming Massive Futures historical Bronze minute aggregates into a clean, strongly typed, validated and contract-enriched Silver dataset.

The Silver layer converts source-aligned Bronze values into trusted analytical minute bars while preserving complete physical source lineage.

Silver is responsible for:

- strong typing;
- timestamp construction;
- session-date parsing;
- instrument identity enrichment;
- OHLC validation;
- activity validation;
- duplicate detection;
- quality classification;
- trusted-grain enforcement.

Silver remains at minute-bar grain.

It does not:

- create additional market aggregation;
- calculate daily candles;
- calculate indicators;
- resolve general provider correction precedence;
- fabricate CQG-style event sequencing;
- implement automatic contract rollover;
- create continuous contracts;
- reconcile historical data with the near-real-time Eventhouse pathway.

---

# 2. Scope

## 2.1 Input Table

```text
bronze_massive_futures_minute_aggregates
```

## 2.2 Instrument Reference

```text
gold_dim_instrument
```

The dimension currently supplies the governed provider-to-contract mapping for the initial implementation.

## 2.3 Output Table

```text
silver_massive_futures_minute_aggregates
```

## 2.4 Initial Contracts

```text
MESU6
MNQU6
```

No additional provider ticker may enter the initial trusted Silver output without an intentional contract and configuration change.

---

# 3. Source Bronze Contract

The input Bronze table preserves one row per accepted physical CSV source row.

Its physical identity is:

```text
source_provider
+ source_dataset
+ source_object_key
+ source_row_number
```

Bronze preserves raw provider values, including:

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

Silver must preserve all Bronze lineage fields required to trace every Silver row to its source object and physical row.

---

# 4. Grain

## 4.1 Physical Input Grain

The physical Bronze grain is:

> One row per accepted physical source CSV row.

## 4.2 Expected Silver Business Grain

The expected Silver business grain is:

```text
source_provider
+ provider_ticker
+ minute_timestamp
```

For the first controlled `MESU6` and `MNQU6` scope, trusted Silver output must contain no duplicate rows at this business grain.

## 4.3 Physical Lineage and Business Grain

The physical source identity and Silver business grain serve different purposes.

Physical identity:

```text
source_provider
+ source_dataset
+ source_object_key
+ source_row_number
```

Business grain:

```text
source_provider
+ provider_ticker
+ minute_timestamp
```

Multiple physical rows may share one apparent business key.

Silver must detect and classify this condition rather than silently collapse it.

---

# 5. Proposed Silver Schema

The initial Silver table shall contain:

```text
source_provider
provider_ticker
AtlasContractKey
AtlasContractBusinessKey
AtlasProductKey
AtlasProductBusinessKey
provider_exchange_code
trading_venue
session_end_date
minute_timestamp
open_price
high_price
low_price
close_price
volume
dollar_volume
transactions
source_dataset
source_object_key
source_row_number
is_valid_ticker
is_valid_session_date
is_valid_timestamp
is_valid_minute_boundary
is_valid_price
is_valid_ohlc
is_valid_activity
is_duplicate_business_key
is_exact_duplicate
has_conflicting_duplicate
silver_quality_status
bronze_loaded_at_utc
silver_loaded_at_utc
```

---

# 6. Physical Data Types

The initial physical schema shall use:

```text
source_provider                  STRING
provider_ticker                  STRING
AtlasContractKey                 BIGINT
AtlasContractBusinessKey         STRING
AtlasProductKey                  BIGINT
AtlasProductBusinessKey          STRING
provider_exchange_code           STRING
trading_venue                    STRING
session_end_date                 DATE
minute_timestamp                 TIMESTAMP
open_price                       DECIMAL(18,5)
high_price                       DECIMAL(18,5)
low_price                        DECIMAL(18,5)
close_price                      DECIMAL(18,5)
volume                           BIGINT
dollar_volume                    DECIMAL(28,5)
transactions                     BIGINT
source_dataset                   STRING
source_object_key                STRING
source_row_number                BIGINT
is_valid_ticker                  BOOLEAN
is_valid_session_date            BOOLEAN
is_valid_timestamp               BOOLEAN
is_valid_minute_boundary          BOOLEAN
is_valid_price                   BOOLEAN
is_valid_ohlc                    BOOLEAN
is_valid_activity                BOOLEAN
is_duplicate_business_key        BOOLEAN
is_exact_duplicate               BOOLEAN
has_conflicting_duplicate        BOOLEAN
silver_quality_status            STRING
bronze_loaded_at_utc             TIMESTAMP
silver_loaded_at_utc             TIMESTAMP
```

## 6.1 Price Precision

The governed analytical price precision for the initial selected contracts is:

```text
Decimal(18,5)
```

This precision has been validated as lossless for:

```text
MESU6
MNQU6
```

It is not approved as universal across all Futures products.

## 6.2 Dollar Volume Precision

The proposed initial type for `dollar_volume` is:

```text
Decimal(28,5)
```

This provides greater whole-number capacity than the OHLC price fields while retaining five decimal places.

Silver must validate that every selected raw value converts successfully.

## 6.3 Activity Types

The initial selected source values support:

```text
volume       BIGINT
transactions BIGINT
```

Silver must not coerce invalid or fractional values silently.

---

# 7. Instrument Identity Enrichment

## 7.1 Mapping Source

Silver shall map Bronze provider identity through:

```text
gold_dim_instrument
```

using:

```text
source_provider
+ provider_ticker
```

The initial mappings are:

```text
Massive + MESU6
→ AtlasContractKey 2001
→ AtlasContractBusinessKey FUT-XCME-MES-2026-09
→ AtlasProductKey 1001
→ AtlasProductBusinessKey FUT-XCME-MES
```

```text
Massive + MNQU6
→ AtlasContractKey 2002
→ AtlasContractBusinessKey FUT-XCME-MNQ-2026-09
→ AtlasProductKey 1002
→ AtlasProductBusinessKey FUT-XCME-MNQ
```

## 7.2 Mapping Requirements

Silver must confirm:

- each selected provider ticker maps to exactly one contract row;
- no selected provider ticker is unmapped;
- no selected provider ticker maps to multiple contract keys;
- the mapped provider is `Massive`;
- the mapped contract key is non-null;
- the mapped contract business key is non-null;
- the mapped product key is non-null;
- the mapped product business key is non-null.

An unmapped or multiply mapped selected ticker must stop trusted Silver processing.

## 7.3 Trading Venue

The Silver `trading_venue` value shall come from the governed instrument mapping:

```text
gold_dim_instrument[TradingVenue]
```

The provider Flat File numeric exchange code remains preserved separately as:

```text
provider_exchange_code
```

Silver shall not assume that numeric exchange code `4` is itself the canonical Atlas venue.

---

# 8. Session Date Parsing

Bronze provides:

```text
session_end_date_raw
```

Silver shall parse it into:

```text
session_end_date DATE
```

The expected source format is:

```text
yyyy-MM-dd
```

Silver must classify the value as invalid if:

- parsing returns null;
- the source value is blank;
- the source value does not match the expected date representation.

For Massive Futures historical bars, this date is the governed session date used later as Gold `TradingDate`.

Silver must not replace it with the UTC calendar date of `minute_timestamp`.

---

# 9. Timestamp Construction

Bronze provides:

```text
window_start_ns
```

as Unix epoch nanoseconds.

Silver shall derive:

```text
minute_timestamp
```

as a UTC timestamp.

## 9.1 Conversion Rule

The conversion must preserve the source instant represented by:

```text
window_start_ns
```

Conceptually:

```text
epoch seconds = window_start_ns / 1,000,000,000
```

The implementation must avoid accidental conversion as:

- milliseconds;
- microseconds;
- local time;
- session-local exchange time.

## 9.2 UTC Semantics

`minute_timestamp` represents the start of the Massive provider minute window in UTC.

No timezone conversion to Chicago, London or another local timezone occurs in Silver.

## 9.3 Minute-Boundary Validation

A valid minute aggregate must begin exactly on a UTC minute boundary.

Silver must confirm that:

```text
window_start_ns % 60,000,000,000 = 0
```

Equivalent timestamp validation must show:

```text
seconds = 0
fractional seconds = 0
```

Rows not aligned to a minute boundary shall be classified as invalid.

---

# 10. Strong Typing

Silver shall transform the raw Bronze fields as follows:

```text
session_end_date_raw
→ session_end_date DATE
```

```text
window_start_ns
→ minute_timestamp TIMESTAMP
```

```text
open_raw
→ open_price DECIMAL(18,5)
```

```text
high_raw
→ high_price DECIMAL(18,5)
```

```text
low_raw
→ low_price DECIMAL(18,5)
```

```text
close_raw
→ close_price DECIMAL(18,5)
```

```text
volume_raw
→ volume BIGINT
```

```text
dollar_volume_raw
→ dollar_volume DECIMAL(28,5)
```

```text
transactions_raw
→ transactions BIGINT
```

Failed conversions must result in null typed values and failed quality flags.

They must not be silently replaced with zero.

---

# 11. Price Validation

## 11.1 Valid Price Rule

A row has valid prices when all four typed OHLC values:

- are non-null;
- are greater than zero;
- preserve the approved `Decimal(18,5)` conversion.

The quality field is:

```text
is_valid_price
```

## 11.2 OHLC Relationship Validation

A row has valid OHLC relationships when:

```text
high_price >= open_price
high_price >= close_price
high_price >= low_price

low_price <= open_price
low_price <= close_price
```

The quality field is:

```text
is_valid_ohlc
```

This validation applies only after all price values have converted successfully.

## 11.3 No Recalculation

Silver must not recalculate provider OHLC values from other rows.

The provider-generated minute aggregate remains the authoritative source bar subject to validation.

---

# 12. Activity Validation

A row has valid activity values when:

```text
volume >= 0
transactions >= 0
dollar_volume >= 0
```

and all three typed values are non-null.

The quality field is:

```text
is_valid_activity
```

Silver shall not assume that:

```text
transactions
```

has identical semantics to the current CQG Gold `TradeCount`.

That semantic distinction remains governed downstream.

---

# 13. Ticker Validation

The quality field:

```text
is_valid_ticker
```

shall be true only when:

- `source_provider = Massive`;
- `provider_ticker` is non-null;
- the ticker is in the approved initial scope;
- the ticker maps to exactly one governed instrument row.

The approved initial ticker scope is:

```text
MESU6
MNQU6
```

No automatic contract discovery or rollover is permitted.

---

# 14. Duplicate Detection

## 14.1 Apparent Business Key

Duplicate detection shall use:

```text
source_provider
+ provider_ticker
+ minute_timestamp
```

## 14.2 Duplicate Business-Key Flag

The field:

```text
is_duplicate_business_key
```

shall be true when more than one physical Silver candidate row shares the same apparent business key.

## 14.3 Exact Duplicate

The field:

```text
is_exact_duplicate
```

shall be true when multiple physical rows share the same apparent business key and the same typed business values:

```text
session_end_date
open_price
high_price
low_price
close_price
volume
dollar_volume
transactions
provider_exchange_code
```

Physical lineage fields are excluded from exact-business-value comparison.

## 14.4 Conflicting Duplicate

The field:

```text
has_conflicting_duplicate
```

shall be true when multiple physical rows share the same apparent business key but differ in one or more compared business values.

## 14.5 Preservation Rule

Silver shall preserve duplicate physical rows for traceability during classification.

It shall not use:

```text
dropDuplicates()
distinct()
first()
last()
max(volume)
max(transactions)
source_row_number precedence
```

to select a preferred record.

## 14.6 Initial Trusted-Scope Rule

For the first controlled `MESU6` and `MNQU6` implementation:

- duplicate business keys are not expected;
- exact duplicates are not expected;
- conflicting duplicates are not expected;
- any conflicting duplicate must stop trusted Silver persistence;
- no provider correction-precedence rule is approved.

If exact duplicates are encountered, the notebook must stop for explicit review rather than silently collapse them.

---

# 15. Quality Fields

Silver shall maintain:

```text
is_valid_ticker
is_valid_session_date
is_valid_timestamp
is_valid_minute_boundary
is_valid_price
is_valid_ohlc
is_valid_activity
is_duplicate_business_key
is_exact_duplicate
has_conflicting_duplicate
silver_quality_status
```

---

# 16. Silver Quality Status

The initial controlled status values are:

```text
Valid
InvalidTicker
InvalidSessionDate
InvalidTimestamp
InvalidMinuteBoundary
InvalidPrice
InvalidOHLC
InvalidActivity
ExactDuplicate
ConflictingDuplicate
```

## 16.1 Status Precedence

Where a row fails multiple checks, `silver_quality_status` shall use this precedence:

```text
1. InvalidTicker
2. InvalidSessionDate
3. InvalidTimestamp
4. InvalidMinuteBoundary
5. InvalidPrice
6. InvalidOHLC
7. InvalidActivity
8. ConflictingDuplicate
9. ExactDuplicate
10. Valid
```

This gives deterministic classification.

Detailed boolean flags remain available even when only one overall status is assigned.

## 16.2 Trusted Row Definition

A trusted Silver row must satisfy:

```text
silver_quality_status = Valid
```

and therefore:

```text
is_valid_ticker = true
is_valid_session_date = true
is_valid_timestamp = true
is_valid_minute_boundary = true
is_valid_price = true
is_valid_ohlc = true
is_valid_activity = true
is_duplicate_business_key = false
is_exact_duplicate = false
has_conflicting_duplicate = false
```

---

# 17. Provenance

Silver shall preserve:

```text
source_provider
source_dataset
source_object_key
source_row_number
bronze_loaded_at_utc
```

Silver shall add:

```text
silver_loaded_at_utc
```

All rows created during one Silver notebook execution shall share one consistent `silver_loaded_at_utc` timestamp.

`silver_loaded_at_utc` records Atlas processing time.

It is not a source-market timestamp.

---

# 18. Event Ordering

Massive minute aggregates are already provider-generated bars.

Silver shall not create or retain CQG-style event sequencing such as:

```text
event_sequence_in_file
event_sequence_in_minute
FirstEventSequence
LastEventSequence
```

`source_row_number` remains physical lineage only.

It must not be interpreted as:

- trade order;
- event order within the minute;
- correction order;
- precedence for duplicate resolution.

---

# 19. Persistence Strategy

For the first controlled implementation, the Silver table may be written using:

```text
mode("overwrite")
```

provided that:

- the Bronze input is the one controlled daily object;
- only the approved selected contracts are processed;
- all pre-persistence validation succeeds;
- all persisted validation succeeds immediately after writing.

This is a development-stage strategy.

Future multi-object ingestion requires an approved incremental or merge design.

---

# 20. Initial Expected Output

The controlled Bronze input contains:

```text
MESU6: 1,380 rows
MNQU6: 1,380 rows
Total: 2,760 rows
```

For the validated source object, the expected trusted Silver output is:

```text
MESU6: 1,380 Valid rows
MNQU6: 1,380 Valid rows
Total: 2,760 Valid rows
```

Expected duplicate classifications:

```text
Duplicate business keys: 0
Exact duplicates:        0
Conflicting duplicates:  0
```

These counts are controlled-file expectations.

They are not universal daily invariants for all future sessions.

---

# 21. Pre-Persistence Validation Requirements

Before writing Silver, the notebook must confirm:

1. Bronze contains exactly the approved provider tickers.
2. Every Bronze row maps to exactly one instrument row.
3. No mapped contract or product key is null.
4. All session dates parse successfully.
5. All nanosecond timestamps convert successfully.
6. Every timestamp is aligned to a UTC minute boundary.
7. All OHLC values convert to `Decimal(18,5)`.
8. All OHLC prices are positive.
9. All OHLC relationships are valid.
10. All volume values convert to `BIGINT`.
11. All transaction values convert to `BIGINT`.
12. All dollar-volume values convert to `Decimal(28,5)`.
13. All activity values are non-negative.
14. Physical source identity remains unique.
15. Source lineage is complete.
16. Exactly one Silver load timestamp exists.
17. No conflicting duplicate exists.
18. No exact duplicate exists without explicit review.
19. The expected business grain is unique for trusted rows.
20. The expected controlled row counts reconcile with Bronze.

Any failed validation must stop persistence.

---

# 22. Persisted Validation Requirements

After writing the Delta table, the notebook must confirm:

- persisted row count matches the prepared Silver DataFrame;
- persisted schema matches the governed Silver schema;
- provider ticker counts reconcile;
- quality-status counts reconcile;
- physical source identity remains unique;
- trusted business grain is unique;
- mapped Atlas keys are retained;
- source lineage remains complete;
- date values remain correct;
- timestamps remain UTC minute boundaries;
- financial precision remains correct;
- no row was introduced or lost during persistence.

Any failed persisted validation must fail the notebook.

---

# 23. Relationship to Gold

The downstream proposed Gold tables are:

```text
gold_massive_futures_minute_candles
gold_massive_futures_daily_candles
```

Gold shall consume only:

```text
silver_quality_status = Valid
```

For the Massive minute path, Gold minute candles will largely project governed trusted provider bars into reporting-friendly fields rather than reconstructing bars from lower-level events.

The Gold daily table will aggregate trusted minute bars using chronological minute ordering.

Silver does not create daily candles.

---

# 24. Relationship to gold_dim_instrument

The current Silver implementation uses:

```text
gold_dim_instrument
```

as the governed source of initial provider-to-contract mapping.

This is a deliberate first-release simplification.

A separate provider-contract mapping table may be introduced later when Atlas supports:

- multiple providers for one contract;
- effective-dated provider mappings;
- provider-symbol changes;
- broader contract chains;
- automatic rollover.

The current mapping dependency does not permit Silver to infer keys directly from ticker text.

---

# 25. Relationship to CQG Silver

The existing CQG Silver table is:

```text
silver_cqg_ticks
```

The Massive Silver table remains separate because the two sources have different grains:

```text
CQG:
one row per source market event
```

```text
Massive:
one row per provider-generated minute aggregate
```

Massive Silver shall not be forced into the CQG tick schema.

The two Silver paths may share identity and reporting concepts without sharing one physical table.

---

# 26. Relationship to Near-Real-Time Data

The existing Massive near-real-time pathway remains separate:

```text
Massive WebSocket
→ local streaming adapter
→ Fabric Eventstream
→ Eventhouse
```

This Silver contract governs only the historical Lakehouse pathway:

```text
Massive Flat File Bronze
→ Massive historical Silver
→ future Massive historical Gold
```

It does not approve:

- reconciliation with Eventhouse;
- streaming Silver tables;
- streaming Gold tables;
- correction handling across pathways;
- common historical and real-time physical storage.

---

# 27. Public Repository Rules

The public repository may contain:

- Silver notebook code;
- schemas;
- validation logic;
- contracts;
- aggregate counts;
- redacted output;
- non-sensitive metadata.

It must not contain:

- Massive market-data files;
- extracted market rows;
- credentials;
- Key Vault secret values;
- signed URLs;
- proprietary provider datasets;
- Delta table data.

---

# 28. Success Criteria

This Silver contract is satisfied when:

1. Every Bronze row is strongly typed or explicitly classified as invalid.
2. Session dates are parsed without replacing provider session semantics.
3. Nanosecond timestamps are converted correctly to UTC.
4. Minute-boundary alignment is validated.
5. OHLC values retain governed `Decimal(18,5)` precision.
6. Activity values are strongly typed and validated.
7. Every selected ticker maps to one governed Atlas contract.
8. Contract and product identity fields are populated.
9. Provider exchange codes remain source-aligned.
10. Trading venue comes from the governed instrument mapping.
11. Physical source lineage is preserved.
12. Duplicate business keys are detected.
13. Exact and conflicting duplicates are distinguished.
14. No duplicate is resolved arbitrarily.
15. Conflicting duplicates stop trusted processing.
16. No CQG-style event sequence is fabricated.
17. Trusted output is unique at the expected business grain.
18. Controlled row counts reconcile with Bronze.
19. The Delta table persists successfully.
20. Persisted validation confirms no loss or introduction of rows.
21. Proprietary data and credentials remain outside the public repository.

---

# 29. Exclusions

The following remain outside this Silver contract:

- automatic contract discovery;
- automatic futures rollover;
- continuous contracts;
- provider correction precedence;
- arbitrary duplicate resolution;
- broad contract-chain ingestion;
- multiple daily-object processing;
- session-level aggregation;
- daily Gold candle creation;
- technical indicators;
- AI commentary;
- CQG and Massive physical-table consolidation;
- historical and streaming reconciliation;
- formal exchange calendars;
- production orchestration;
- production monitoring;
- effective-dated provider mappings.

---

# 30. Future Evolution

Future Silver versions may include:

- multi-object processing;
- incremental ingestion;
- durable provider-contract mapping tables;
- effective-dated mappings;
- approved provider correction logic;
- exchange-code enrichment;
- formal trading-session classification;
- exchange calendar enrichment;
- broader contract support;
- provider reconciliation;
- precision rules by product;
- production data-quality telemetry.

These changes must preserve:

- source lineage;
- explicit grain;
- deterministic validation;
- no fabricated market data;
- no arbitrary duplicate resolution.

---

# 31. Ownership

**Platform:** Atlas Market Data Platform  
**Layer:** Silver  
**Provider:** Massive  
**Dataset:** Futures minute aggregates  
**Input Table:** `bronze_massive_futures_minute_aggregates`  
**Output Table:** `silver_massive_futures_minute_aggregates`  
**Status:** Proposed for controlled v1.3.0 implementation