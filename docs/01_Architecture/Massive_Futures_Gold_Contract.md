# Massive Futures Gold Contract

## Document Status

**Version:** 1.1.0  
**Status:** Implemented and validated for the controlled `v1.3.0` scope  
**Target Release:** `v1.3.0 — Multi-Instrument Architecture`  
**Layer:** Gold  
**Source Provider:** Massive  
**Dataset:** Futures minute aggregates  
**Implemented Scope:** `MESU6` and `MNQU6`

The controlled Massive Futures Gold implementation is complete for one trading session ending:

```text
2026-07-14
```

Implemented assets include:

```text
gold_massive_futures_minute_candles
gold_massive_futures_daily_candles
gold_dim_instrument
sm_atlas_gold_reporting
rpt_atlas_semantic_model_validation_dev
```

The implementation remains a controlled development increment rather than a production historical backfill.

---

# 1. Purpose

This contract defines the Gold-layer requirements for transforming trusted Massive Futures historical Silver minute aggregates into business-ready analytical candle tables.

The Massive source already supplies provider-generated minute OHLC bars.

The Gold layer therefore performs two distinct responsibilities:

1. project trusted Silver minute bars into a governed reporting-friendly minute table;
2. aggregate trusted minute bars into deterministic daily candles.

The Gold layer shall preserve:

- governed Atlas contract identity;
- governed Atlas product identity;
- provider session-date semantics;
- UTC minute timestamps;
- validated OHLC precision;
- provider volume;
- provider transaction count;
- provider dollar volume;
- traceability to trusted Silver data.

The Gold layer shall not:

- reconstruct minute OHLC values from lower-level market events;
- fabricate CQG-style event sequencing;
- perform automatic futures-contract rollover;
- create continuous contracts;
- generate trading signals;
- generate forecasts;
- create trading recommendations;
- reconcile historical data with the Eventhouse near-real-time pathway.

---

# 2. Scope

## 2.1 Input Table

```text
silver_massive_futures_minute_aggregates
```

## 2.2 Instrument Dimension

```text
gold_dim_instrument
```

## 2.3 Output Tables

```text
gold_massive_futures_minute_candles
gold_massive_futures_daily_candles
```

## 2.4 Initial Contracts

```text
MESU6
MNQU6
```

## 2.5 Initial Data Coverage

The first controlled implementation covers one Massive Futures trading session:

```text
Session end date:
2026-07-14
```

Expected trusted Silver rows:

```text
MESU6: 1,380 minute bars
MNQU6: 1,380 minute bars
Total: 2,760 minute bars
```

Expected initial Gold output:

```text
Minute table:
2,760 rows

Daily table:
2 rows
```

These counts are controlled-session expectations rather than universal daily invariants.

---

# 3. Source Silver Contract

The input Silver table contains strongly typed, validated and contract-enriched provider-generated minute aggregates.

Gold shall consume only rows where:

```text
silver_quality_status = Valid
```

Trusted Silver rows must already satisfy:

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

Gold shall not repair or reinterpret invalid Silver rows.

If the expected selected scope contains invalid or duplicate Silver rows, Gold processing must stop.

---

# 4. Source Model Difference from CQG Gold

The CQG Gold path starts from individual market events:

```text
CQG Silver events
→ Atlas-generated minute candles
→ Atlas-generated daily candles
```

The Massive Gold path starts from provider-generated minute bars:

```text
Massive Silver minute aggregates
→ governed minute candle projection
→ Atlas-generated daily candles
```

Therefore, the Massive minute Gold table shall not contain:

```text
FirstEventSequence
LastEventSequence
event_sequence_in_minute
```

The source does not expose the lower-level event ordering required to support those fields.

`source_row_number` remains Silver lineage and is not propagated as a Gold market-ordering attribute.

---

# 5. Design Principles

The Massive Gold layer shall:

- consume only trusted Silver rows;
- use stable Atlas contract keys;
- use provider session date as `TradingDate`;
- use UTC source minute timestamp as `MinuteTimestamp`;
- preserve validated minute OHLC values;
- preserve validated provider activity values;
- maintain `Decimal(18,5)` OHLC precision;
- maintain explicit minute and daily grain;
- derive daily Open and Close chronologically;
- preserve source-specific activity semantics;
- avoid arbitrary aggregation across unrelated contracts;
- remain suitable for Direct Lake semantic modelling;
- remain reproducible and deterministic.

---

# 6. Gold Minute Candle Table

## 6.1 Table

```text
gold_massive_futures_minute_candles
```

## 6.2 Grain

One row per:

```text
AtlasContractKey
+ MinuteTimestamp
```

Equivalent descriptive grain:

```text
one governed dated Futures contract
+ one UTC provider minute window
```

## 6.3 Source

Each Gold minute row is derived from exactly one trusted Massive Silver minute row.

No lower-level aggregation occurs in the minute Gold transformation.

## 6.4 Proposed Schema

```text
AtlasContractKey
AtlasContractBusinessKey
AtlasProductKey
AtlasProductBusinessKey
Instrument
TradingDate
MinuteTimestamp
TradingTime
TradingHour
MinuteOfDay
Open
High
Low
Close
Volume
TransactionCount
DollarVolume
GoldLoadedUTC
```

## 6.5 Physical Data Types

```text
AtlasContractKey          BIGINT
AtlasContractBusinessKey  STRING
AtlasProductKey           BIGINT
AtlasProductBusinessKey   STRING
Instrument                STRING
TradingDate               DATE
MinuteTimestamp           TIMESTAMP
TradingTime               STRING
TradingHour               INT
MinuteOfDay               INT
Open                      DECIMAL(18,5)
High                      DECIMAL(18,5)
Low                       DECIMAL(18,5)
Close                     DECIMAL(18,5)
Volume                    BIGINT
TransactionCount          BIGINT
DollarVolume              DECIMAL(28,5)
GoldLoadedUTC             TIMESTAMP
```

---

# 7. Gold Minute Field Rules

## 7.1 Atlas Identity

The following values shall be retained from trusted Silver:

```text
AtlasContractKey
AtlasContractBusinessKey
AtlasProductKey
AtlasProductBusinessKey
```

`AtlasContractKey` is the governed semantic-model relationship key.

Provider ticker text shall not replace the Atlas key.

## 7.2 Instrument

For the first implementation:

```text
Instrument
```

shall contain the provider ticker:

```text
MESU6
MNQU6
```

This field is retained as a readable compatibility attribute.

It is not the governed relationship key and should not become the primary report slicer once `gold_dim_instrument` is in use.

## 7.3 TradingDate

```text
TradingDate
```

shall be copied from:

```text
session_end_date
```

It must not be derived from the UTC date portion of `MinuteTimestamp`.

For example:

```text
MinuteTimestamp:
2026-07-13 22:00:00 UTC

TradingDate:
2026-07-14
```

This preserves the provider-defined Futures session date.

## 7.4 MinuteTimestamp

```text
MinuteTimestamp
```

shall be copied from the trusted Silver UTC:

```text
minute_timestamp
```

No additional timezone conversion occurs in Gold.

## 7.5 TradingTime

```text
TradingTime
```

shall be formatted from `MinuteTimestamp` as:

```text
HH:mm
```

This is a reporting attribute.

It does not replace the timestamp key.

## 7.6 TradingHour

```text
TradingHour
```

shall contain the UTC hour component of `MinuteTimestamp`.

Expected range:

```text
0 to 23
```

## 7.7 MinuteOfDay

```text
MinuteOfDay
```

shall be calculated as:

```text
TradingHour * 60 + minute component
```

Expected range:

```text
0 to 1439
```

This field supports deterministic chronological sorting within a UTC calendar day.

Cross-midnight Futures session ordering shall continue to use `MinuteTimestamp`, not `MinuteOfDay` alone.

## 7.8 OHLC

The following values shall be projected directly from trusted Silver:

```text
open_price  → Open
high_price  → High
low_price   → Low
close_price → Close
```

Gold shall not recalculate these values from adjacent rows.

The provider-generated minute bar remains authoritative after Silver validation.

## 7.9 Activity

The following values shall be projected directly from trusted Silver:

```text
volume        → Volume
transactions  → TransactionCount
dollar_volume → DollarVolume
```

`TransactionCount` represents the Massive provider-supplied `transactions` field.

It must not be assumed to have identical semantics to CQG `TradeCount`.

## 7.10 GoldLoadedUTC

All rows created during one Gold notebook execution shall share one consistent:

```text
GoldLoadedUTC
```

This is Atlas processing metadata.

It is not a source-market timestamp.

---

# 8. Gold Minute Validation Rules

For every minute candle:

```text
High >= Open
High >= Close
High >= Low

Low <= Open
Low <= Close

Open > 0
High > 0
Low > 0
Close > 0

Volume >= 0
TransactionCount >= 0
DollarVolume >= 0
```

Additional validation must confirm:

- one row per `AtlasContractKey` and `MinuteTimestamp`;
- no null contract keys;
- no null business keys;
- no null `TradingDate`;
- no null `MinuteTimestamp`;
- all timestamps are UTC minute boundaries;
- `TradingDate` equals the trusted Silver `session_end_date`;
- OHLC values preserve `Decimal(18,5)`;
- activity values reconcile exactly with trusted Silver;
- exactly one Gold row is produced for each trusted Silver row;
- no invalid Silver row enters Gold.

---

# 9. Gold Daily Candle Table

## 9.1 Table

```text
gold_massive_futures_daily_candles
```

## 9.2 Grain

One row per:

```text
AtlasContractKey
+ TradingDate
```

Equivalent descriptive grain:

```text
one governed dated Futures contract
+ one provider-defined trading session
```

## 9.3 Source

Daily candles shall be derived from the persisted Massive Gold minute table:

```text
gold_massive_futures_minute_candles
```

This ensures that daily calculations reconcile with the exact governed minute dataset exposed to reporting.

## 9.4 Proposed Schema

```text
AtlasContractKey
AtlasContractBusinessKey
AtlasProductKey
AtlasProductBusinessKey
Instrument
TradingDate
Open
High
Low
Close
TotalVolume
TotalTransactions
TotalDollarVolume
MinuteBarCount
SessionStartTimestamp
SessionEndTimestamp
GoldLoadedUTC
```

## 9.5 Physical Data Types

```text
AtlasContractKey          BIGINT
AtlasContractBusinessKey  STRING
AtlasProductKey           BIGINT
AtlasProductBusinessKey   STRING
Instrument                STRING
TradingDate               DATE
Open                      DECIMAL(18,5)
High                      DECIMAL(18,5)
Low                       DECIMAL(18,5)
Close                     DECIMAL(18,5)
TotalVolume               BIGINT
TotalTransactions         BIGINT
TotalDollarVolume         DECIMAL(38,5)
MinuteBarCount            BIGINT
SessionStartTimestamp     TIMESTAMP
SessionEndTimestamp       TIMESTAMP
GoldLoadedUTC             TIMESTAMP
```

---

# 10. Daily OHLC Rules

Daily Open and Close must be derived from chronological minute ordering.

They must never be calculated using unordered `MIN()` or `MAX()` logic.

## 10.1 Open

```text
Open
```

is the `Open` value from the first chronological minute candle for the contract and `TradingDate`.

## 10.2 High

```text
High
```

is the maximum minute `High` value for the contract and `TradingDate`.

## 10.3 Low

```text
Low
```

is the minimum minute `Low` value for the contract and `TradingDate`.

## 10.4 Close

```text
Close
```

is the `Close` value from the last chronological minute candle for the contract and `TradingDate`.

## 10.5 Ordering Field

Chronological ordering shall use:

```text
MinuteTimestamp
```

The following must not be used alone for session Open or Close:

```text
TradingTime
TradingHour
MinuteOfDay
source_row_number
```

The Futures session crosses UTC midnight, so time-of-day fields alone are insufficient for complete session ordering.

---

# 11. Daily Activity Rules

## 11.1 TotalVolume

```text
TotalVolume
```

shall equal:

```text
SUM(Volume)
```

across accepted minute candles for the contract and `TradingDate`.

## 11.2 TotalTransactions

```text
TotalTransactions
```

shall equal:

```text
SUM(TransactionCount)
```

across accepted minute candles for the contract and `TradingDate`.

## 11.3 TotalDollarVolume

```text
TotalDollarVolume
```

shall equal:

```text
SUM(DollarVolume)
```

across accepted minute candles for the contract and `TradingDate`.

The daily type is widened to:

```text
Decimal(38,5)
```

to reduce overflow risk during aggregation.

## 11.4 MinuteBarCount

```text
MinuteBarCount
```

shall equal the number of accepted Gold minute rows contributing to the daily candle.

For the initial controlled session, the expected count is:

```text
1,380
```

for each contract.

This is not a universal invariant for every future session.

## 11.5 SessionStartTimestamp

```text
SessionStartTimestamp
```

shall equal:

```text
MIN(MinuteTimestamp)
```

for the contract and `TradingDate`.

## 11.6 SessionEndTimestamp

```text
SessionEndTimestamp
```

shall equal:

```text
MAX(MinuteTimestamp)
```

for the contract and `TradingDate`.

For the initial controlled session, expected coverage is approximately:

```text
2026-07-13 22:00:00 UTC
through
2026-07-14 20:59:00 UTC
```

---

# 12. Gold Daily Validation Rules

For every daily candle:

```text
High >= Open
High >= Close
High >= Low

Low <= Open
Low <= Close

Open > 0
High > 0
Low > 0
Close > 0

TotalVolume >= 0
TotalTransactions >= 0
TotalDollarVolume >= 0
MinuteBarCount > 0

SessionStartTimestamp <= SessionEndTimestamp
```

Additional validation must confirm:

- one row per `AtlasContractKey` and `TradingDate`;
- daily Open equals the first chronological minute Open;
- daily Close equals the last chronological minute Close;
- daily High equals the maximum minute High;
- daily Low equals the minimum minute Low;
- activity totals reconcile with minute rows;
- `MinuteBarCount` reconciles with minute rows;
- session start and end timestamps reconcile with minute coverage;
- every daily row maps to one governed instrument;
- no minute row contributes to more than one daily row.

---

# 13. Initial Expected Minute Output

For the controlled source session:

```text
MESU6:
1,380 minute Gold rows

MNQU6:
1,380 minute Gold rows

Total:
2,760 minute Gold rows
```

Expected minute grain uniqueness:

```text
AtlasContractKey
+ MinuteTimestamp
```

Expected duplicates:

```text
0
```

Expected invalid rows:

```text
0
```

---

# 14. Initial Expected Daily Output

For the controlled source session:

```text
MESU6:
1 daily Gold row

MNQU6:
1 daily Gold row

Total:
2 daily Gold rows
```

Expected `TradingDate`:

```text
2026-07-14
```

Expected `MinuteBarCount`:

```text
MESU6: 1,380
MNQU6: 1,380
```

Expected session start:

```text
2026-07-13 22:00:00 UTC
```

Expected session end:

```text
2026-07-14 20:59:00 UTC
```

These values are controlled-file expectations, not permanent assumptions for every future session.

---

# 15. Instrument Dimension Relationship

The governed instrument dimension is:

```text
gold_dim_instrument
```

The implemented relationships are:

```text
gold_dim_instrument[AtlasContractKey]
    1 → *
gold_massive_futures_minute_candles[AtlasContractKey]
```

```text
gold_dim_instrument[AtlasContractKey]
    1 → *
gold_massive_futures_daily_candles[AtlasContractKey]
```

Both relationships are:

```text
Cardinality:
One-to-many

Cross-filter direction:
Single

Active:
Yes
```

The filter direction runs from:

```text
gold_dim_instrument
```

to each Massive fact table.

The governed user-facing instrument slicer is:

```text
gold_dim_instrument[ContractDisplayName]
```

`ContractDisplayName` is sorted by:

```text
InstrumentSortOrder
```

The implemented order is:

```text
Micro E-mini S&P 500 Sep 2026
Micro E-mini Nasdaq-100 Sep 2026
```

Technical identity and provider-mapping fields are hidden from the normal report field list, including:

```text
AtlasContractKey
AtlasContractBusinessKey
AtlasProductKey
AtlasProductBusinessKey
SourceProvider
ProviderTicker
ProviderGroupCode
ProviderContractType
InstrumentSortOrder
GoldLoadedUTC
```

These fields remain present for:

- relationships;
- DAX calculations;
- validation;
- debugging;
- future model evolution.

The fact-table `Instrument` columns remain compatibility attributes.

They are not the primary governed slicer.

---

# 16. Date Dimension Relationship

The governed date dimension is:

```text
gold_dim_date
```

The implemented relationships are:

```text
gold_dim_date[Date]
    1 → *
gold_massive_futures_minute_candles[TradingDate]
```

```text
gold_dim_date[Date]
    1 → *
gold_massive_futures_daily_candles[TradingDate]
```

Both relationships are:

```text
Cardinality:
One-to-many

Cross-filter direction:
Single

Active:
Yes
```

The filter direction runs from:

```text
gold_dim_date
```

to each Massive fact table.

The existing CQG date relationships remain unchanged:

```text
gold_dim_date[Date]
    1 → *
Minute Candles[TradingDate]
```

```text
gold_dim_date[Date]
    1 → *
Daily Candles[TradingDate]
```

No direct relationship exists between:

- the Massive minute and daily facts;
- the CQG minute and daily facts;
- CQG and Massive fact tables.

All facts are filtered through governed dimensions appropriate to their current implementation.

The current controlled Massive trading date:

```text
2026-07-14
```

is covered by `gold_dim_date`.

The date-dimension generation process must be reviewed again when the Massive historical range expands.

---

# 17. Fact Table Relationships

No direct relationship shall exist between:

```text
gold_massive_futures_minute_candles
```

and:

```text
gold_massive_futures_daily_candles
```

The two tables have different analytical grains.

They shall be filtered through governed dimensions.

No direct relationship shall initially exist between CQG and Massive fact tables.

---

# 18. Implemented Semantic Measure Behaviour

## 18.1 Single-Contract Price Guard

Massive measures returning a single price or point-in-time value require exactly one governed contract in filter context.

Implemented behaviour:

```text
one Atlas contract selected
→ return the measure

zero or multiple Atlas contracts selected
→ return blank
```

The guard uses logic equivalent to:

```DAX
HASONEVALUE (
    gold_dim_instrument[AtlasContractKey]
)
```

This prevents Atlas from returning an arbitrary price across unrelated contracts.

## 18.2 Daily Price Measures

Implemented daily price measures include:

```text
Massive Selected Period Open
Massive Selected Period High
Massive Selected Period Low
Massive Selected Period Close
Massive Selected Period Return %
Massive Selected Period Range
Massive Selected Period Range %
```

These measures are stored in:

```text
Massive\Daily Price
```

## 18.3 Daily Time-Intelligence Measures

Implemented daily time-intelligence measures include:

```text
Massive Trading Days
Massive Selected Trading Date
Massive Previous Trading Date
Massive Selected Trading Day Close
Massive Previous Trading Day Close
Massive Trading Day Change
Massive Trading Day Change %
Massive 5-Day MA Close
```

These measures are stored in:

```text
Massive\Daily Time Intelligence
```

The controlled implementation currently contains one trading session.

Therefore:

```text
Massive Previous Trading Date
Massive Previous Trading Day Close
Massive Trading Day Change
Massive Trading Day Change %
```

correctly return blank until additional sessions are loaded.

`Massive 5-Day MA Close` currently averages the one available session.

It becomes a full five-trading-session measure after historical coverage expands.

## 18.4 Daily Activity Measures

Implemented daily activity measures include:

```text
Massive Total Volume
Massive Total Transactions
Massive Total Dollar Volume
Massive Total Minute Bars
Massive Average Volume / Day
Massive Average Transactions / Day
Massive Average Dollar Volume / Day
Massive Average Volume / Minute
Massive Average Transactions / Minute
Massive Average Dollar Volume / Minute
```

These measures are stored in:

```text
Massive\Daily Activity
```

## 18.5 Intraday Price Measures

Implemented intraday price measures include:

```text
Massive Last Price
Massive Session Open
Massive Session High
Massive Session Low
Massive Session Close
Massive Session Change
Massive Session Change %
Massive Session Range
Massive Session Range %
```

These measures are stored in:

```text
Massive\Intraday Price
```

## 18.6 Intraday Activity Measures

Implemented intraday activity measures include:

```text
Massive Session Volume
Massive Session Transactions
Massive Session Dollar Volume
Massive Minute Bar Count
Massive Intraday Average Volume / Minute
Massive Intraday Average Transactions / Minute
Massive Intraday Average Dollar Volume / Minute
```

These measures are stored in:

```text
Massive\Intraday Activity
```

## 18.7 Intraday Time Measures

Implemented intraday time measures include:

```text
Massive First Minute Timestamp
Massive Last Minute Timestamp
```

These measures are stored in:

```text
Massive\Intraday Time
```

## 18.8 Activity Semantics

Massive activity measures retain provider-specific meanings:

```text
Volume
TransactionCount
DollarVolume
```

They must not automatically combine with CQG:

```text
TradeCount
```

because the underlying business semantics differ.

## 18.9 Existing CQG Measures

The existing CQG measures and report behaviour remain unchanged.

No CQG measure was migrated, renamed or rewritten during this implementation.

Future shared-measure work requires explicit regression testing.

---

# 19. Pre-Persistence Validation Requirements

## 19.1 Minute Table

Before writing the minute table, the notebook must confirm:

1. Only `silver_quality_status = Valid` rows are selected.
2. Input trusted Silver row count is 2,760.
3. `MESU6` trusted row count is 1,380.
4. `MNQU6` trusted row count is 1,380.
5. Every row has a non-null `AtlasContractKey`.
6. Every row has a non-null contract business key.
7. Every row has a non-null product key.
8. Every row has a non-null product business key.
9. Every row has a non-null `TradingDate`.
10. Every row has a non-null `MinuteTimestamp`.
11. Minute grain is unique.
12. All OHLC values are positive.
13. All OHLC relationships are valid.
14. All activity values are non-negative.
15. `TradingDate` reconciles with Silver session date.
16. Minute values reconcile exactly with trusted Silver.
17. Exactly one Gold load timestamp exists.
18. No row is introduced or lost.

## 19.2 Daily Table

Before writing the daily table, the notebook must confirm:

1. Exactly two daily rows are produced.
2. One row exists for `MESU6`.
3. One row exists for `MNQU6`.
4. Daily grain is unique.
5. `TradingDate = 2026-07-14`.
6. Each row has `MinuteBarCount = 1,380`.
7. Daily Open reconciles with first minute Open.
8. Daily Close reconciles with last minute Close.
9. Daily High reconciles with maximum minute High.
10. Daily Low reconciles with minimum minute Low.
11. Total Volume reconciles with minute Volume.
12. Total Transactions reconcile with minute TransactionCount.
13. Total Dollar Volume reconciles with minute DollarVolume.
14. Session start and end timestamps reconcile with minute coverage.
15. All daily OHLC relationships are valid.
16. Exactly one Gold load timestamp exists.

Any failed validation must stop persistence.

---

# 20. Persisted Validation Requirements

After writing each Delta table, the notebook must confirm:

- persisted row count matches the prepared DataFrame;
- persisted schema matches the governed schema;
- persisted grain remains unique;
- instrument keys remain populated;
- contract counts reconcile;
- date coverage reconciles;
- OHLC precision is retained;
- activity values reconcile;
- Gold load timestamps remain consistent;
- no row was introduced or lost during persistence.

Persisted daily validation must also reconcile the saved daily table back to the saved minute table.

Any failed validation must fail the notebook.

---

# 21. Persistence Strategy

For the first controlled implementation, both Gold tables may be written using:

```text
mode("overwrite")
```

provided that:

- the Silver input represents one explicitly controlled source session;
- the selected contract scope is fixed;
- pre-persistence validation succeeds;
- persisted validation succeeds immediately after writing.

This is a development-stage strategy.

Future multi-session ingestion requires an approved incremental, partitioned or merge design.

---

# 22. Partitioning

No physical Delta partitioning is required for the initial one-session implementation.

Future larger historical loads should evaluate partitioning by:

```text
TradingDate
```

Potential secondary clustering or optimisation may consider:

```text
AtlasContractKey
MinuteTimestamp
```

Partitioning must not be introduced prematurely without sufficient data volume and query evidence.

---

# 23. Precision

## 23.1 OHLC

The approved initial OHLC precision is:

```text
Decimal(18,5)
```

This is validated for:

```text
MESU6
MNQU6
```

It is not approved as universal for all Futures contracts.

## 23.2 Minute Dollar Volume

```text
DollarVolume
```

uses:

```text
Decimal(28,5)
```

## 23.3 Daily Dollar Volume

```text
TotalDollarVolume
```

uses:

```text
Decimal(38,5)
```

to support safe aggregation.

Future product expansion must re-evaluate precision and scale requirements.

---

# 24. Relationship to Existing Gold Contract

The existing general Gold contract currently governs the CQG historical tables:

```text
gold_cqg_minute_candles
gold_cqg_daily_candles
```

This Massive Gold contract is provider-path-specific.

It preserves the same core analytical principles:

- explicit grain;
- deterministic Open and Close;
- governed date semantics;
- validated financial precision;
- no unsupported trading logic;
- suitability for semantic modelling.

The Massive and CQG tables remain physically separate during the initial v1.3.0 implementation.

---

# 25. Relationship to Near-Real-Time Data

The existing Massive near-real-time pathway remains:

```text
Massive WebSocket
→ local adapter
→ Fabric Eventstream
→ Eventhouse
```

This Gold contract governs only the historical Lakehouse pathway:

```text
Massive Flat File
→ Bronze
→ Silver
→ historical Gold
```

It does not approve:

- Eventhouse-to-Lakehouse reconciliation;
- common historical and streaming Gold tables;
- late-event correction handling;
- shared rollover logic;
- near-real-time semantic-model integration.

---

# 26. Public Repository Rules

The public repository may contain:

- Gold notebook code;
- table schemas;
- contracts;
- validation logic;
- aggregate row counts;
- redacted screenshots;
- non-sensitive metadata.

It must not contain:

- Massive Flat Files;
- extracted proprietary market rows;
- Delta table data;
- credentials;
- Key Vault secret values;
- signed source URLs.

---

# 27. Success Criteria and Results

This Gold contract has been satisfied for the controlled `MESU6` and `MNQU6` implementation.

1. Only trusted Massive Silver rows entered Gold.
2. Minute Gold contains one row per contract and minute timestamp.
3. Minute OHLC values reconcile exactly with trusted Silver.
4. Minute activity values reconcile exactly with trusted Silver.
5. Provider session date became Gold `TradingDate`.
6. UTC timestamp semantics were preserved.
7. No CQG-style event sequence was fabricated.
8. Minute grain is unique.
9. Daily Open was derived from the first chronological minute.
10. Daily Close was derived from the last chronological minute.
11. Daily High and Low reconcile with minute extrema.
12. Daily activity totals reconcile with minute values.
13. Daily session timestamps reconcile with minute coverage.
14. Contract and product keys remain populated.
15. `Decimal(18,5)` OHLC precision was retained.
16. Both Delta tables persisted successfully.
17. Persisted validation confirmed no row loss or introduction.
18. The existing CQG path remained unchanged.
19. Historical and near-real-time paths remain separate.
20. Proprietary data and credentials remain outside the public repository.
21. `gold_dim_instrument` filters both Massive fact tables correctly.
22. `gold_dim_date` filters both Massive fact tables correctly.
23. All new relationships are active, one-to-many and single-direction.
24. Single-contract price guards prevent misleading multi-contract prices.
25. Measures are organised into governed display folders.
26. Technical dimension fields are hidden from report authors.
27. `ContractDisplayName` is sorted deterministically.
28. Both initial contracts were validated through a Power BI report.

Controlled output counts:

```text
Gold minute rows:
2,760

MESU6 minute rows:
1,380

MNQU6 minute rows:
1,380

Gold daily rows:
2
```

Controlled session coverage:

```text
TradingDate:
2026-07-14

Session start:
2026-07-13 22:00:00 UTC

Session end:
2026-07-14 20:59:00 UTC
```

---

# 28. Exclusions

The following remain outside this Gold contract:

- automatic futures-contract rollover;
- continuous contracts;
- contract-chain analytics;
- provider correction precedence;
- multiple-session incremental loading;
- cross-provider reconciliation;
- CQG and Massive fact-table consolidation;
- common activity semantics across providers;
- formal exchange calendars;
- trading signals;
- strategy backtesting;
- forecasts;
- predictive modelling;
- automated execution;
- generative AI calculation of authoritative market facts;
- Eventhouse reconciliation;
- production orchestration;
- production monitoring.

---

# 29. Future Evolution

Future Gold versions may include:

- multiple trading sessions;
- historical backfill;
- incremental Gold processing;
- partitioned or optimised Delta tables;
- wider contract coverage;
- product-level reporting;
- contract-chain reporting;
- governed rollover;
- continuous-contract analytics;
- historical and streaming reconciliation;
- provider-neutral canonical Gold facts;
- additional semantic-model measures;
- certified multi-instrument semantic models.

These changes must preserve:

- explicit grain;
- deterministic chronological ordering;
- financial precision;
- governed identity;
- provider-specific semantics where required;
- reproducibility;
- traceability.

---

# 30. Ownership

**Platform:** Atlas Market Data Platform  
**Layer:** Gold  
**Provider:** Massive  
**Dataset:** Futures minute aggregates  
**Input Table:** `silver_massive_futures_minute_aggregates`  
**Minute Output:** `gold_massive_futures_minute_candles`  
**Daily Output:** `gold_massive_futures_daily_candles`  
**Instrument Dimension:** `gold_dim_instrument`  
**Semantic Model:** `sm_atlas_gold_reporting`  
**Validation Report:** `rpt_atlas_semantic_model_validation_dev`  
**Status:** Implemented and validated for the controlled v1.3.0 scope

---

# 31. Semantic-Model Validation Results

## 31.1 Validation Report

The semantic-model implementation was validated using:

```text
rpt_atlas_semantic_model_validation_dev
```

The report is retained temporarily as a development and regression-validation asset.

It may be:

- extended as more historical sessions are loaded;
- reused for semantic-model regression checks;
- renamed as a permanent validation asset;
- deleted before release if no longer required.

A final retention decision will be made during v1.3.0 release consolidation.

## 31.2 Instrument Filtering

Selecting:

```text
Micro E-mini S&P 500 Sep 2026
```

filtered both Massive fact tables to:

```text
MESU6
```

Selecting:

```text
Micro E-mini Nasdaq-100 Sep 2026
```

filtered both Massive fact tables to:

```text
MNQU6
```

Daily and intraday measures remained synchronised through:

```text
gold_dim_instrument
```

## 31.3 MESU6 Results

```text
Selected Period Open:    7,558.25
Selected Period High:    7,613.75
Selected Period Low:     7,531.75
Selected Period Close:   7,590.50
Selected Period Return:  0.43%
Selected Period Range:   82.00
Session Volume:          958,226
```

## 31.4 MNQU6 Results

```text
Selected Period Open:    29,440.00
Selected Period High:    29,922.00
Selected Period Low:     29,303.25
Selected Period Close:   29,794.75
Selected Period Return:  1.20%
Selected Period Range:   618.75
Session Volume:          2,726,737
```

For both controlled contracts:

```text
Massive Selected Period Close
=
Massive Last Price
```

because the selected period contains one complete trading session.

## 31.5 Multi-Selection Behaviour

When more than one governed contract is selected:

```text
guarded price measures
→ blank
```

Activity measures may aggregate across selected Massive contracts where their names and report context clearly indicate additive behaviour.

## 31.6 Presentation Note

Power BI cards may abbreviate values using display units such as:

```text
29.44K
3M
```

Production price cards should use:

```text
Display units:
None
```

where exact financial values are required.

Volume and activity cards may retain abbreviated display units where appropriate.

## 31.7 Current Boundary

This semantic-model validation covers:

```text
two contracts
one provider
one trading session
historical Lakehouse facts
```

It does not yet validate:

- multiple historical trading sessions;
- previous-trading-day values;
- a full five-session moving average;
- automatic rollover;
- continuous contracts;
- CQG instrument-dimension mapping;
- historical and Eventhouse reconciliation.