# Atlas Multi-Instrument Identity and Grain Design

## Document Status

**Status:** Implemented and validated for the controlled v1.3.0 scope  
**Target Release:** `v1.3.0 — Multi-Instrument Architecture`  
**Implementation Status:** Historical Massive Bronze, Silver, Gold, instrument dimension and semantic-model implementation complete for `MESU6` and `MNQU6`  
**Scope:** Historical CQG and Massive Futures analytical paths

---

# 1. Purpose

This document defines the initial proposed identity, grain, key and contract boundaries required for Atlas to support more than one historical Futures contract.

The design is intentionally limited to the first controlled multi-instrument increment:

```text
Existing CQG historical contract:
F.US.EU6M12

Existing Massive near-real-time and historical contract:
MESU6

First additional Massive historical contract:
MNQU6
```

The document does not approve:

- automatic futures-contract rollover;
- continuous-contract construction;
- broad exchange-wide ingestion;
- multi-asset reporting;
- historical and near-real-time reconciliation;
- consolidation of all providers into one physical fact table.

Its purpose is to establish a governed foundation before Fabric tables, semantic-model relationships or Power BI reports are changed.

---

# 2. Current Implementation

## 2.1 CQG Bronze and Silver

The current CQG historical path is:

```text
CQG legacy source file
        |
        v
bronze_cqg_legacy_ticks
        |
        v
silver_cqg_ticks
```

The current Silver table is:

```text
silver_cqg_ticks
```

Its implemented grain is:

> One row per CQG source market event.

The Silver layer preserves:

- source provider;
- provider-specific instrument value;
- source file identity;
- source row number;
- event sequence within the source file;
- event sequence within a trading minute;
- parsed price;
- event timestamp;
- validation status;
- Bronze and Silver load timestamps.

Event identity is currently based on:

```text
source_provider
+ source_file_name
+ event_sequence_in_file
```

The implemented notebook retains a single provider-specific `instrument` field.

The existing Silver contract documents both `instrument_code` and `contract_code`, but the current implementation does not persist a separate `contract_code`.

The current `instrument` value therefore performs several roles:

- provider-specific source identifier;
- contract identifier;
- grouping attribute;
- downstream reporting value.

This discrepancy between documentation and implementation must be corrected as part of the relevant v1.3.0 contract update.

## 2.2 CQG Gold

The current CQG Gold tables are:

```text
gold_cqg_minute_candles
gold_cqg_daily_candles
```

Their implemented grains are:

```text
gold_cqg_minute_candles:
Instrument + MinuteTimestamp
```

```text
gold_cqg_daily_candles:
Instrument + TradingDate
```

The Gold `Instrument` value is derived directly from the Silver `instrument` field.

It currently performs the roles of:

- provider identifier;
- contract identifier;
- grouping key;
- report display value;
- report slicer value.

The Gold notebook is structurally CQG-specific because it:

- reads `silver_cqg_ticks`;
- derives OHLC candles from individual market events;
- relies on deterministic CQG event sequencing;
- creates CQG-specific Gold table names;
- produces `FirstEventSequence` and `LastEventSequence`.

There is no literal hard-coded filter for `F.US.EU6M12`, but the processing model is inherently based on CQG event-level data.

## 2.3 Current Semantic Model

The historical semantic model is:

```text
sm_atlas_gold_reporting
```

It now includes six tables:

```text
Daily Candles
Minute Candles
gold_dim_date
gold_dim_instrument
gold_massive_futures_daily_candles
gold_massive_futures_minute_candles
```

The existing CQG tables remain unchanged:

```text
Daily Candles
Minute Candles
```

The Massive historical tables are:

```text
gold_massive_futures_daily_candles
gold_massive_futures_minute_candles
```

The governed dimensions are:

```text
gold_dim_date
gold_dim_instrument
```

The existing date relationships remain:

```text
gold_dim_date[Date]
    1 → *
Daily Candles[TradingDate]
```

```text
gold_dim_date[Date]
    1 → *
Minute Candles[TradingDate]
```

The implemented Massive date relationships are:

```text
gold_dim_date[Date]
    1 → *
gold_massive_futures_daily_candles[TradingDate]
```

```text
gold_dim_date[Date]
    1 → *
gold_massive_futures_minute_candles[TradingDate]
```

The implemented instrument relationships are:

```text
gold_dim_instrument[AtlasContractKey]
    1 → *
gold_massive_futures_daily_candles[AtlasContractKey]
```

```text
gold_dim_instrument[AtlasContractKey]
    1 → *
gold_massive_futures_minute_candles[AtlasContractKey]
```

All six relationships are:

- active;
- one-to-many;
- single-direction;
- filtered from the dimension to the fact table.

No direct relationships exist between:

- CQG and Massive fact tables;
- daily and minute fact tables;
- provider ticker fields;
- text `Instrument` fields.

The Massive historical facts therefore use:

```text
AtlasContractKey
```

as the governed instrument relationship key.

The CQG facts continue to use their existing provider-specific structure and remain outside the first instrument-dimension migration.

## 2.4 Current Measure Behaviour

The Massive semantic-model measures now implement explicit single-contract safeguards.

For price and point-in-time measures:

```text
exactly one Atlas contract selected
→ return the requested value

zero or multiple Atlas contracts selected
→ return blank
```

The guard is implemented using logic equivalent to:

```DAX
HASONEVALUE (
    gold_dim_instrument[AtlasContractKey]
)
```

Implemented Massive daily measure groups are:

```text
Massive\Daily Price
Massive\Daily Time Intelligence
Massive\Daily Activity
```

Implemented Massive intraday measure groups are:

```text
Massive\Intraday Price
Massive\Intraday Activity
Massive\Intraday Time
```

Examples of implemented daily measures include:

```text
Massive Selected Period Open
Massive Selected Period High
Massive Selected Period Low
Massive Selected Period Close
Massive Selected Period Return %
Massive Selected Period Range
Massive Selected Period Range %
Massive Selected Trading Date
Massive Previous Trading Date
Massive Selected Trading Day Close
Massive Previous Trading Day Close
Massive Trading Day Change
Massive Trading Day Change %
Massive 5-Day MA Close
Massive Total Volume
Massive Total Transactions
Massive Total Dollar Volume
Massive Trading Days
```

Examples of implemented intraday measures include:

```text
Massive Session Open
Massive Session High
Massive Session Low
Massive Session Close
Massive Last Price
Massive Session Change
Massive Session Change %
Massive Session Range
Massive Session Range %
Massive Session Volume
Massive Session Transactions
Massive Session Dollar Volume
Massive Minute Bar Count
Massive First Minute Timestamp
Massive Last Minute Timestamp
```

Activity measures may aggregate across selected Massive contracts where the measure name and report context make that behaviour clear.

The existing CQG measures remain unchanged.

---

# 3. Massive Historical Data Discovery

## 3.1 Flat Files Access

Massive Futures Flat Files are available through an S3-compatible endpoint.

The read-only catalogue probe confirmed that all 16 documented Futures dataset prefixes are listable:

```text
CBOT
CME
COMEX
NYMEX
```

with:

```text
session aggregates
minute aggregates
trades
quotes
```

The v1.3.0 implementation remains limited to minute aggregates available under the current Futures Starter subscription.

Trades and Quotes remain outside scope.

## 3.2 Validated Massive Minute-Aggregate Schema

The validated CME Futures minute-aggregate Flat File schema is:

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

One inspected daily CME file contained:

```text
89,951 rows
937 unique provider tickers
1,380 MESU6 rows
1,380 MNQU6 rows
```

The file is exchange-wide rather than instrument-specific.

A single daily source object therefore contains many products, contracts and contract types.

## 3.3 Massive Source Time Semantics

Massive provides both:

```text
window_start
session_end_date
```

These represent different concepts.

For example, a bar may have:

```text
window_start UTC:
2026-07-13 22:00:00

session_end_date:
2026-07-14
```

For Massive Futures data:

- `MinuteTimestamp` must be derived from `window_start`;
- `TradingDate` must be derived from the provider-supplied `session_end_date`;
- Atlas must not derive the trading date solely from the UTC calendar date.

## 3.4 Massive Price Precision

The Flat File represents OHLC values with nine decimal places in source text.

Examples include:

```text
7558.250000000
0.186000000
0.006187500
```

The source representation and meaningful business precision are different concepts.

For the selected contracts:

```text
MESU6 maximum meaningful scale: 2
MNQU6 maximum meaningful scale: 2
```

The current governed analytical precision remains suitable:

```text
Decimal(18,5)
```

However, this precision is not yet approved as universal across all CME Futures products.

Some currency and spread contracts require six or seven meaningful decimal places.

Broad cross-asset ingestion will therefore require a separate precision decision.

## 3.5 Massive Duplicate Behaviour

The expected Massive analytical grain appears to be:

```text
provider ticker
+ minute window
```

However, conflicting duplicate rows were observed at that apparent grain.

The duplicate records had the same:

```text
ticker
exchange
session_end_date
window_start
```

but different:

```text
Open
High
Low
Close
Volume
DollarVolume
Transactions
```

Therefore:

- `(ticker, window_start)` is not guaranteed to be physically unique;
- Bronze must preserve every physical source row;
- Silver must detect conflicting duplicates;
- Atlas must not use arbitrary `dropDuplicates()` logic;
- no general provider correction-precedence rule is currently approved.

The conflicts did not occur for `MESU6` or `MNQU6`.

Both selected contracts were unique at the expected minute grain in the inspected source file.

---

# 4. Source Model Differences

CQG and Massive begin at fundamentally different source grains.

## 4.1 CQG

```text
one row per source market event
        |
        v
Atlas generates minute OHLC candles
```

CQG requires:

- source event ordering;
- event sequence within a file;
- event sequence within a minute;
- first-event Open;
- last-event Close.

## 4.2 Massive

```text
one row per provider-generated minute aggregate
        |
        v
Atlas validates and governs the supplied minute bar
```

Massive already supplies:

- Open;
- High;
- Low;
- Close;
- volume;
- transaction count;
- dollar volume.

Massive does not provide or require CQG-style event ordering for historical minute aggregates.

Atlas must not fabricate:

```text
event_sequence_in_minute
FirstEventSequence
LastEventSequence
```

for Massive provider-generated bars.

Source row number is lineage metadata and is not market-event ordering.

---

# 5. Design Principles

The v1.3.0 design shall:

- preserve the existing CQG historical path;
- preserve deterministic CQG event ordering;
- preserve the existing CQG Gold tables;
- preserve Massive physical source rows before reconciliation;
- distinguish product identity from futures-contract identity;
- distinguish Atlas identity from provider symbols;
- retain provider and source lineage;
- avoid fabricated event sequencing;
- preserve `Decimal(18,5)` for the selected first contracts;
- avoid automatic rollover and continuous contracts;
- keep historical and near-real-time pathways separate;
- minimise changes to existing validated tables and reports;
- use compact surrogate keys for relationships;
- retain readable governed business keys;
- keep key allocation stable across reruns and environments;
- avoid keys generated from source order or load order.

---

# 6. Identity Concepts

Atlas shall distinguish the following concepts.

## 6.1 Provider

The external organisation supplying market data.

Examples:

```text
CQG
Massive
```

A provider is not an instrument, product, contract or exchange.

## 6.2 Provider Ticker

The symbol used by one provider to identify a contract.

Examples:

```text
Massive: MESU6
Massive: MNQU6
CQG:     F.US.EU6M12
```

Provider tickers remain source identifiers.

They shall not automatically become permanent Atlas canonical keys.

## 6.3 Product

The listed Futures product independent of a particular dated contract.

Examples:

```text
MES
Micro E-mini S&P 500

MNQ
Micro E-mini Nasdaq-100
```

The product grain is:

> One row per governed Atlas Futures product.

## 6.4 Futures Contract

A dated, tradable contract for a Futures product.

Examples:

```text
MES September 2026
MNQ September 2026
```

The contract grain is:

> One row per governed Atlas Futures product, contract month and contract year.

A contract is distinct from the provider ticker used to represent it.

## 6.5 Trading Venue

The Massive reference API returns:

```text
XCME
```

The Massive Flat File contains numeric exchange codes such as:

```text
4
11
12
```

These values must be preserved separately until an authoritative mapping is validated.

No provider exchange code shall automatically become the Atlas canonical venue key.

A venue code included in an Atlas business key must come from the governed Atlas venue mapping.

## 6.6 Asset Class

The initial governed asset class is:

```text
Futures
```

The first v1.3.0 implementation remains limited to equity-index Futures contracts.

Broader asset-class modelling remains outside the initial increment.

---

# 7. Key Strategy Decision

Atlas will use both:

- integer surrogate keys;
- governed deterministic text business keys.

This provides compact relationships while retaining transparent and reproducible business identity.

## 7.1 Prohibited Key Approaches

The following must not be used to allocate stable Atlas keys:

```text
row_number()
monotonically_increasing_id()
provider response order
CSV source row order
alphabetical sort position
current table row order
load timestamp
```

These methods are not stable across reruns, rebuilds or environments.

Provider symbols must also not be used as permanent canonical keys.

## 7.2 Initial Key Governance

For the first v1.3.0 increment, integer keys will be allocated through a small explicit governed seed mapping.

The initial mapping may be represented in:

- a controlled Fabric notebook configuration;
- a small governed reference dataset;
- or an equivalent source-controlled structure.

A general enterprise key-management service is not required for the initial two-product scope.

Future expansion may replace the seed mapping with durable reference tables and controlled merge processing.

---

# 8. Product Keys

## 8.1 AtlasProductKey

Proposed field:

```text
AtlasProductKey
```

Characteristics:

- integer surrogate key;
- one value per governed Futures product;
- used for joins and relationships;
- stable across reruns and environments;
- independent of provider symbols.

Initial allocation:

```text
1001 → Micro E-mini S&P 500
1002 → Micro E-mini Nasdaq-100
```

## 8.2 AtlasProductBusinessKey

Proposed field:

```text
AtlasProductBusinessKey
```

Characteristics:

- governed deterministic text;
- human-readable;
- provider-neutral;
- unique at product grain;
- useful for validation, documentation and debugging.

Proposed format:

```text
FUT-{VENUE}-{PRODUCT}
```

Initial values:

```text
FUT-XCME-MES
FUT-XCME-MNQ
```

Initial mapping:

```text
AtlasProductKey | AtlasProductBusinessKey
1001            | FUT-XCME-MES
1002            | FUT-XCME-MNQ
```

---

# 9. Contract Keys

## 9.1 AtlasContractKey

Proposed field:

```text
AtlasContractKey
```

Characteristics:

- integer surrogate key;
- primary semantic-model relationship key;
- one value per dated Futures contract;
- stable across reruns and environments;
- independent of provider symbols;
- reusable across historical and near-real-time facts.

Initial allocation:

```text
2001 → MES September 2026
2002 → MNQ September 2026
```

## 9.2 AtlasContractBusinessKey

Proposed field:

```text
AtlasContractBusinessKey
```

Characteristics:

- governed deterministic text;
- provider-neutral;
- unique at contract grain;
- useful for validation and external integration;
- readable across environments.

Proposed format:

```text
FUT-{VENUE}-{PRODUCT}-{YEAR}-{MONTH}
```

Initial values:

```text
FUT-XCME-MES-2026-09
FUT-XCME-MNQ-2026-09
```

Initial mapping:

```text
AtlasContractKey | AtlasContractBusinessKey
2001             | FUT-XCME-MES-2026-09
2002             | FUT-XCME-MNQ-2026-09
```

## 9.3 Contract-to-Product Relationship

Each contract belongs to exactly one governed product.

Initial relationships:

```text
AtlasContractKey 2001
→ AtlasProductKey 1001

AtlasContractKey 2002
→ AtlasProductKey 1002
```

---

# 10. Provider Contract Mapping

Provider symbols must be held separately from Atlas canonical identity.

A provider mapping shall associate:

```text
SourceProvider
ProviderTicker
AtlasContractKey
```

The mapping grain is:

> One row per provider and provider contract symbol.

Initial Massive mappings:

```text
SourceProvider | ProviderTicker | AtlasContractKey
Massive        | MESU6          | 2001
Massive        | MNQU6          | 2002
```

This allows another provider symbol to map to the same Atlas contract in future without changing the fact-table relationship key.

The provider mapping may eventually contain:

```text
SourceProvider
ProviderTicker
ProviderProductCode
ProviderGroupCode
ProviderContractType
ProviderTradingVenue
ProviderExchangeCode
AtlasProductKey
AtlasContractKey
MappingEffectiveFrom
MappingEffectiveTo
IsCurrent
```

Effective-dating is not required for the first v1.3.0 implementation unless a validated use case emerges.

---

# 11. Massive Contract Metadata

Massive returns the same 17-field reference schema for `MESU6` and `MNQU6`.

Common fields include:

```text
active
date
days_to_maturity
first_trade_date
group_code
last_trade_date
max_order_quantity
min_order_quantity
name
product_code
settlement_date
settlement_tick_size
spread_tick_size
ticker
trade_tick_size
trading_venue
type
```

Validated values include:

## MESU6

```text
ProviderTicker:          MESU6
ProductCode:             MES
GroupCode:               MS
TradingVenue:            XCME
FirstTradeDate:          2025-06-20
LastTradeDate:           2026-09-18
SettlementDate:          2026-09-18
TradeTickSize:           0.25
SettlementTickSize:      0.25
SpreadTickSize:          0.01
ProviderContractType:    single
IsActive:                true
```

## MNQU6

```text
ProviderTicker:          MNQU6
ProductCode:             MNQ
GroupCode:               NQ
TradingVenue:            XCME
FirstTradeDate:          2025-06-20
LastTradeDate:           2026-09-18
SettlementDate:          2026-09-18
TradeTickSize:           0.25
SettlementTickSize:      0.25
SpreadTickSize:          0.01
ProviderContractType:    single
IsActive:                true
```

The Massive reference endpoint does not currently provide all desired governed attributes.

Potential missing attributes include:

- descriptive underlying name;
- asset-class classification;
- currency;
- contract multiplier;
- contract month as a separate field;
- contract year as a separate field;
- provider-independent product name;
- mapping from numeric Flat File exchange code.

These values must not be invented silently.

Where Atlas supplies mapped or derived values, the source and rationale must be documented.

---

# 12. Proposed Instrument Dimension

The initial governed reporting dimension shall be:

```text
gold_dim_instrument
```

## 12.1 Grain

One row per:

```text
AtlasContractKey
```

For v1.3.0, each row represents one dated Futures contract.

The dimension does not represent:

- a continuous contract;
- an automatically rolled instrument;
- a product-level aggregate;
- an exchange-wide product chain;
- a provider-specific symbol as the canonical identity.

## 12.2 Minimum Implementation Schema

The first physical implementation shall contain only the fields required to support:

- governed product and contract identity;
- provider mapping;
- instrument filtering;
- readable contract display values;
- deterministic sorting;
- validated contract metadata;
- semantic-model relationships.

The approved minimum schema is:

```text
AtlasContractKey
AtlasContractBusinessKey
AtlasProductKey
AtlasProductBusinessKey
AssetClass
ProductCode
ProductName
ContractCode
ContractMonthCode
ContractMonthNumber
ContractMonthName
ContractYear
ContractDisplayName
TradingVenue
TradeTickSize
SettlementTickSize
SpreadTickSize
FirstTradeDate
LastTradeDate
SettlementDate
IsActive
SourceProvider
ProviderTicker
ProviderGroupCode
ProviderContractType
InstrumentSortOrder
GoldLoadedUTC
```

## 12.3 Physical Data Types

The initial physical schema shall use:

```text
AtlasContractKey          BIGINT
AtlasContractBusinessKey  STRING
AtlasProductKey           BIGINT
AtlasProductBusinessKey   STRING
AssetClass                STRING
ProductCode               STRING
ProductName               STRING
ContractCode              STRING
ContractMonthCode         STRING
ContractMonthNumber       INT
ContractMonthName         STRING
ContractYear              INT
ContractDisplayName       STRING
TradingVenue              STRING
TradeTickSize             DECIMAL(18,5)
SettlementTickSize        DECIMAL(18,5)
SpreadTickSize            DECIMAL(18,5)
FirstTradeDate            DATE
LastTradeDate             DATE
SettlementDate            DATE
IsActive                  BOOLEAN
SourceProvider            STRING
ProviderTicker            STRING
ProviderGroupCode         STRING
ProviderContractType      STRING
InstrumentSortOrder       INT
GoldLoadedUTC             TIMESTAMP
```

## 12.4 Field Ownership

### Atlas-governed integer keys

The following fields are allocated through the explicit Atlas seed mapping:

```text
AtlasProductKey
AtlasContractKey
```

These values must remain stable across reruns and environments.

They must not be generated from:

- row order;
- provider response order;
- source file order;
- alphabetical ordering;
- runtime-generated identifiers.

### Atlas-governed business keys

The following fields are constructed deterministically from approved Atlas identity rules:

```text
AtlasProductBusinessKey
AtlasContractBusinessKey
```

Initial formats:

```text
AtlasProductBusinessKey:
FUT-{VENUE}-{PRODUCT}
```

```text
AtlasContractBusinessKey:
FUT-{VENUE}-{PRODUCT}-{YEAR}-{MONTH}
```

### Atlas-governed descriptive mappings

The following values are maintained as explicit governed Atlas mappings:

```text
AssetClass
ProductName
ContractCode
ContractDisplayName
InstrumentSortOrder
```

These values may use validated provider metadata as supporting evidence, but they are Atlas reporting attributes rather than direct copies of provider fields.

### Deterministically derived contract attributes

The following fields are derived from the validated contract identity:

```text
ContractMonthCode
ContractMonthNumber
ContractMonthName
ContractYear
```

For the first implementation:

```text
U → 9 → September
6 → 2026
```

The derivation logic must be explicit and validated.

### Provider-supplied metadata

The following fields are sourced from Massive contract-reference metadata:

```text
ProductCode
TradingVenue
TradeTickSize
SettlementTickSize
SpreadTickSize
FirstTradeDate
LastTradeDate
SettlementDate
IsActive
ProviderTicker
ProviderGroupCode
ProviderContractType
```

The source provider is recorded as:

```text
SourceProvider = Massive
```

### Technical metadata

The following field records dimension-generation time:

```text
GoldLoadedUTC
```

## 12.5 Deferred Fields

The following fields shall not be included in the first physical implementation:

```text
Currency
ContractMultiplier
ProviderExchangeCode
```

Reasons:

- `Currency` was not returned by the validated contract-reference response.
- `ContractMultiplier` was not returned by the validated contract-reference response.
- the numeric Flat File exchange codes do not yet have an authoritative Atlas mapping.

These fields may be added later through governed schema evolution.

No placeholder or assumed values shall be inserted merely to complete the schema.

## 12.6 Initial Rows

The first implementation shall contain exactly two rows.

### MESU6

```text
AtlasContractKey:          2001
AtlasContractBusinessKey:  FUT-XCME-MES-2026-09
AtlasProductKey:           1001
AtlasProductBusinessKey:   FUT-XCME-MES
AssetClass:                Futures
ProductCode:               MES
ProductName:               Micro E-mini S&P 500
ContractCode:              MES-2026-09
ContractMonthCode:         U
ContractMonthNumber:       9
ContractMonthName:         September
ContractYear:              2026
ContractDisplayName:       Micro E-mini S&P 500 Sep 2026
TradingVenue:              XCME
TradeTickSize:             0.25000
SettlementTickSize:        0.25000
SpreadTickSize:            0.01000
FirstTradeDate:            2025-06-20
LastTradeDate:             2026-09-18
SettlementDate:            2026-09-18
IsActive:                  true
SourceProvider:            Massive
ProviderTicker:            MESU6
ProviderGroupCode:         MS
ProviderContractType:      single
InstrumentSortOrder:       1
```

### MNQU6

```text
AtlasContractKey:          2002
AtlasContractBusinessKey:  FUT-XCME-MNQ-2026-09
AtlasProductKey:           1002
AtlasProductBusinessKey:   FUT-XCME-MNQ
AssetClass:                Futures
ProductCode:               MNQ
ProductName:               Micro E-mini Nasdaq-100
ContractCode:              MNQ-2026-09
ContractMonthCode:         U
ContractMonthNumber:       9
ContractMonthName:         September
ContractYear:              2026
ContractDisplayName:       Micro E-mini Nasdaq-100 Sep 2026
TradingVenue:              XCME
TradeTickSize:             0.25000
SettlementTickSize:        0.25000
SpreadTickSize:            0.01000
FirstTradeDate:            2025-06-20
LastTradeDate:             2026-09-18
SettlementDate:            2026-09-18
IsActive:                  true
SourceProvider:            Massive
ProviderTicker:            MNQU6
ProviderGroupCode:         NQ
ProviderContractType:      single
InstrumentSortOrder:       2
```

`GoldLoadedUTC` is populated at dimension-generation time and is therefore not hard-coded in the seed values.

## 12.7 Validation Rules

Before persistence, the dimension-generation process must confirm:

```text
AtlasContractKey is not null
AtlasContractKey is unique
AtlasContractBusinessKey is not null
AtlasContractBusinessKey is unique
AtlasProductKey is not null
AtlasProductBusinessKey is not null
SourceProvider is not null
ProviderTicker is not null
SourceProvider + ProviderTicker is unique
InstrumentSortOrder is unique
TradeTickSize > 0
SettlementTickSize > 0
SpreadTickSize > 0
```

It must also confirm:

- each contract maps to exactly one product key;
- each product key maps to exactly one product business key;
- `ContractMonthCode = U`;
- `ContractMonthNumber = 9`;
- `ContractMonthName = September`;
- `ContractYear = 2026`;
- `LastTradeDate = SettlementDate`;
- `FirstTradeDate <= LastTradeDate`;
- `ProviderTicker MESU6` maps only to `AtlasContractKey 2001`;
- `ProviderTicker MNQU6` maps only to `AtlasContractKey 2002`;
- all tick-size fields preserve `Decimal(18,5)` precision;
- exactly two rows are produced for the initial scope.

Any failed validation must stop the dimension build.

## 12.8 Semantic-Model Role

The dimension is now the one side of the implemented Massive historical instrument relationships:

```text
gold_dim_instrument[AtlasContractKey]
    1 → *
gold_massive_futures_daily_candles[AtlasContractKey]
```

```text
gold_dim_instrument[AtlasContractKey]
    1 → *
gold_massive_futures_minute_candles[AtlasContractKey]
```

Both relationships are:

- active;
- one-to-many;
- single-direction;
- filtered from `gold_dim_instrument` to the fact table.

The preferred user-facing contract slicer is:

```text
gold_dim_instrument[ContractDisplayName]
```

`ContractDisplayName` is sorted by:

```text
InstrumentSortOrder
```

This produces the governed initial order:

```text
Micro E-mini S&P 500 Sep 2026
Micro E-mini Nasdaq-100 Sep 2026
```

Technical and provider-mapping fields are hidden from the normal report-authoring field list, including:

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

The hidden fields remain available internally for:

- relationships;
- DAX calculations;
- validation;
- debugging;
- future model evolution.

The fact-table `Instrument` fields remain available as compatibility attributes but are not the primary governed slicer.

The model may display a generated `(Blank)` dimension member where Power BI creates an unknown relationship member.

This value is excluded in report slicers through a visual-level non-blank filter.

## 12.9 Scope Boundary

For the first implementation, provider mapping attributes remain within `gold_dim_instrument`.

A separate provider-contract mapping table is not required for two contracts from one provider.

This may be reconsidered when Atlas supports:

- multiple providers for the same contract;
- historical provider-symbol changes;
- effective-dated mappings;
- contract rollover;
- broader contract-chain ingestion.

## 12.10 Dimension Role

The dimension provides:

- stable contract identity;
- stable product identity;
- provider-neutral fact relationships;
- readable contract labels;
- product-level descriptive attributes;
- deterministic slicer ordering;
- validated contract metadata;
- future historical and near-real-time convergence.

It does not yet provide:

- continuous-contract identity;
- automatic rollover;
- formal exchange-calendar enrichment;
- currency;
- contract multiplier;
- authoritative numeric exchange-code mapping;
- cross-provider reconciliation.

---

# 13. Proposed Massive Bronze Contract

## 13.1 Table

Proposed table:

```text
bronze_massive_futures_minute_aggregates
```

## 13.2 Grain

One row per physical source CSV row.

Bronze does not enforce provider business-grain uniqueness.

## 13.3 Physical Source Identity

The physical Bronze identity should include:

```text
source_provider
source_dataset
source_object_key
source_row_number
```

This combination must uniquely identify each ingested source row.

## 13.4 Proposed Fields

```text
source_provider
source_dataset
source_object_key
source_row_number
provider_ticker
provider_exchange_code
session_end_date
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

Source values should remain as close as practical to their Flat File representation.

## 13.5 Bronze Responsibilities

Bronze shall:

- preserve every accepted source row;
- preserve exact provider values;
- preserve source object identity;
- preserve source row position;
- preserve provider ticker;
- preserve numeric exchange code;
- preserve provider session date;
- preserve raw nanosecond timestamp;
- avoid provider-to-Atlas identity enrichment;
- avoid arbitrary deduplication;
- support replay and investigation.

## 13.6 Duplicate Handling

Bronze shall:

- preserve exact duplicates;
- preserve conflicting apparent-grain records;
- not select a preferred occurrence;
- retain sufficient lineage for investigation.

---

# 14. Proposed Massive Silver Contract

## 14.1 Table

Proposed table:

```text
silver_massive_futures_minute_aggregates
```

## 14.2 Expected Business Grain

Expected Silver business grain:

```text
source_provider
+ provider_ticker
+ minute_timestamp
```

For the first controlled increment, the transformation must fail if conflicting records exist for a selected contract at this grain.

## 14.3 Proposed Fields

```text
source_provider
provider_ticker
AtlasContractKey
AtlasContractBusinessKey
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
is_valid_timestamp
is_valid_ohlc
is_valid_activity
is_duplicate_business_key
has_conflicting_duplicate
silver_quality_status
bronze_loaded_at_utc
silver_loaded_at_utc
```

## 14.4 Silver Validation

Silver validation must confirm:

```text
High >= Open
High >= Close
High >= Low
Low <= Open
Low <= Close
Volume >= 0
Transactions >= 0
DollarVolume >= 0
```

It must also confirm:

- selected provider tickers map to exactly one `AtlasContractKey`;
- selected provider tickers map to exactly one `AtlasContractBusinessKey`;
- timestamps are valid UTC minute boundaries;
- `session_end_date` is preserved;
- no conflicting duplicate business keys enter trusted Silver;
- price values convert safely to the governed precision;
- selected contract grain is unique after validation;
- source lineage remains complete.

## 14.5 Event Ordering

Massive minute aggregates are already provider-generated bars.

Silver must not fabricate:

```text
event_sequence_in_file
event_sequence_in_minute
FirstEventSequence
LastEventSequence
```

Source row number is lineage metadata, not market-event ordering.

## 14.6 Duplicate Policy for Initial Scope

For `MESU6` and `MNQU6`:

- validate uniqueness at the expected business grain;
- fail processing if conflicting duplicates are found;
- do not choose a winner automatically;
- do not use arbitrary Spark deduplication;
- exclude broader correction-precedence logic from the first increment.

A general correction and revision policy remains future work.

---

# 15. Proposed Massive Gold Contracts

## 15.1 Gold Minute Table

Proposed table:

```text
gold_massive_futures_minute_candles
```

### Grain

One row per:

```text
AtlasContractKey
+ MinuteTimestamp
```

### Proposed Fields

```text
AtlasContractKey
AtlasContractBusinessKey
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

`Instrument` may remain as a user-facing compatibility or display attribute during the first increment.

`AtlasContractKey` is the governed relationship key.

`TradingDate` must be derived from the provider-supplied `session_end_date`.

### Precision

The OHLC fields shall use:

```text
Decimal(18,5)
```

for the selected `MESU6` and `MNQU6` contracts.

## 15.2 Gold Daily Table

Proposed table:

```text
gold_massive_futures_daily_candles
```

### Grain

One row per:

```text
AtlasContractKey
+ TradingDate
```

### Proposed Fields

```text
AtlasContractKey
AtlasContractBusinessKey
Instrument
TradingDate
Open
High
Low
Close
TotalVolume
TotalTransactions
TotalDollarVolume
GoldLoadedUTC
```

Daily values shall be derived from accepted Massive minute bars:

```text
Open
→ first chronological minute Open

High
→ maximum minute High

Low
→ minimum minute Low

Close
→ last chronological minute Close

TotalVolume
→ sum of minute Volume

TotalTransactions
→ sum of minute TransactionCount

TotalDollarVolume
→ sum of minute DollarVolume
```

No CQG event-sequence fields shall be added to Massive Gold tables.

---

# 16. Shared and Source-Specific Semantics

## 16.1 Potentially Shared Fields

The following concepts can be shared across CQG and Massive Gold tables:

```text
AtlasContractKey
AtlasContractBusinessKey
TradingDate
MinuteTimestamp
Open
High
Low
Close
```

## 16.2 CQG-Specific Fields

```text
TradeCount
FirstEventSequence
LastEventSequence
```

The CQG `TradeCount` currently represents the number of accepted CQG source events contributing to an Atlas-generated candle.

## 16.3 Massive-Specific Fields

```text
Volume
TransactionCount
DollarVolume
session_end_date lineage
provider exchange code
```

Massive `transactions` is a provider-supplied aggregate value.

It must not automatically be assumed to have identical meaning to CQG `TradeCount`.

## 16.4 Activity Measures

A shared semantic-model measure must not combine:

```text
CQG TradeCount
```

with:

```text
Massive TransactionCount
```

until their meanings are explicitly governed.

Massive Volume and DollarVolume may be additive across selected Massive contracts, but any multi-contract aggregation must be clearly labelled.

---

# 17. Implemented Semantic Model Relationships

## 17.1 Instrument Relationships

The implemented relationships are:

```text
gold_dim_instrument[AtlasContractKey]
    1 → *
gold_massive_futures_daily_candles[AtlasContractKey]
```

```text
gold_dim_instrument[AtlasContractKey]
    1 → *
gold_massive_futures_minute_candles[AtlasContractKey]
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

to the Massive fact tables.

## 17.2 Date Relationships

The implemented Massive date relationships are:

```text
gold_dim_date[Date]
    1 → *
gold_massive_futures_daily_candles[TradingDate]
```

```text
gold_dim_date[Date]
    1 → *
gold_massive_futures_minute_candles[TradingDate]
```

Both relationships are:

- active;
- one-to-many;
- single-direction;
- filtered from `gold_dim_date` to the fact table.

The existing CQG date relationships remain unchanged.

## 17.3 Fact-to-Fact Relationships

No direct relationship exists between:

```text
gold_massive_futures_daily_candles
```

and:

```text
gold_massive_futures_minute_candles
```

No direct relationship exists between Massive and CQG fact tables.

All filtering occurs through governed dimensions.

## 17.4 Relationship Validation

Relationship behaviour was validated through a temporary Power BI report.

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

Daily and intraday measures remained synchronised through the shared instrument dimension.

The existing CQG facts were not filtered by the Massive instrument dimension.

## 17.5 Initial CQG Position

The existing CQG fact tables remain unchanged during v1.3.0.

The first instrument dimension currently filters only the Massive historical facts.

Mapping the CQG contract into `gold_dim_instrument` remains a future controlled decision covering:

- exact CQG product identity;
- exact contract identity;
- addition of `AtlasContractKey` to CQG facts;
- regression testing of existing report behaviour;
- whether cross-provider shared historical facts are desirable.

---

# 18. Implemented Measure Behaviour

## 18.1 Price Measures

Massive price measures require exactly one selected governed contract.

Examples include:

```text
Massive Selected Period Open
Massive Selected Period High
Massive Selected Period Low
Massive Selected Period Close
Massive Selected Period Return %
Massive Selected Period Range
Massive Selected Period Range %
Massive Selected Trading Day Close
Massive Previous Trading Day Close
Massive Trading Day Change
Massive Trading Day Change %
Massive 5-Day MA Close
Massive Session Open
Massive Session High
Massive Session Low
Massive Session Close
Massive Last Price
Massive Session Change
Massive Session Change %
Massive Session Range
Massive Session Range %
```

Implemented behaviour is:

```text
one Atlas contract in filter context
→ return the measure

zero or multiple Atlas contracts in filter context
→ return blank
```

This prevents a price from being selected arbitrarily across unrelated contracts.

## 18.2 Previous-Trading-Day Measures

The following measures are implemented:

```text
Massive Previous Trading Date
Massive Previous Trading Day Close
Massive Trading Day Change
Massive Trading Day Change %
```

The current controlled dataset contains one trading session only.

These measures therefore correctly return blank until additional historical sessions are ingested.

## 18.3 Five-Trading-Day Moving Average

The following measure is implemented:

```text
Massive 5-Day MA Close
```

It selects up to the five most recent available trading dates for the selected contract.

With the current one-session dataset, it averages the one available close.

It becomes a true five-trading-session moving average after additional historical sessions are loaded.

## 18.4 Activity Measures

Implemented Massive daily activity measures include:

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

Implemented Massive intraday activity measures include:

```text
Massive Session Volume
Massive Session Transactions
Massive Session Dollar Volume
Massive Minute Bar Count
Massive Intraday Average Volume / Minute
Massive Intraday Average Transactions / Minute
Massive Intraday Average Dollar Volume / Minute
```

These measures retain Massive-specific semantics.

They do not combine with CQG `TradeCount`.

## 18.5 Measure Organisation

Measures are organised into the following display folders:

```text
Massive
├── Daily Activity
├── Daily Price
├── Daily Time Intelligence
├── Intraday Activity
├── Intraday Price
└── Intraday Time
```

This separates Massive measures from the existing CQG measures and improves semantic-model usability.

## 18.6 Validation Results

The implemented measures were validated for both initial contracts.

### MESU6

```text
Selected Period Open:    7,558.25
Selected Period High:    7,613.75
Selected Period Low:     7,531.75
Selected Period Close:   7,590.50
Selected Period Return:  0.43%
Selected Period Range:   82.00
Session Volume:          958,226
```

### MNQU6

```text
Selected Period Open:    29,440.00
Selected Period High:    29,922.00
Selected Period Low:     29,303.25
Selected Period Close:   29,794.75
Selected Period Return:  1.20%
Selected Period Range:   618.75
Session Volume:          2,726,737
```

For both contracts:

```text
Massive Selected Period Close
=
Massive Last Price
```

for the controlled complete trading session.

---

# 19. Initial Scope Decision

The first additional Massive historical contract is:

```text
MNQU6
```

The first Massive historical implementation scope is:

```text
MESU6
MNQU6
```

This choice validates:

- two distinct Futures products;
- one provider;
- one broad venue family;
- one contract month;
- one contract year;
- matching tick size;
- matching session coverage;
- safe current price precision;
- shared reference metadata structure;
- multi-instrument semantic filtering.

It does not introduce:

- automatic rollover;
- continuous contracts;
- a second asset class;
- a second venue family;
- cross-provider reconciliation;
- high-precision currency Futures;
- spread contracts;
- Trades or Quotes datasets.

---

# 20. Initial Key Allocation

## Products

```text
AtlasProductKey | AtlasProductBusinessKey | ProductCode
1001            | FUT-XCME-MES            | MES
1002            | FUT-XCME-MNQ            | MNQ
```

## Contracts

```text
AtlasContractKey | AtlasContractBusinessKey   | AtlasProductKey | ProviderTicker
2001             | FUT-XCME-MES-2026-09       | 1001            | MESU6
2002             | FUT-XCME-MNQ-2026-09       | 1002            | MNQU6
```

These allocations are proposed and must remain stable once implementation begins.

Keys must not be reassigned to different products or contracts.

Retired keys must not be reused.

---

# 21. Exclusions

The following remain outside the proposed first increment:

- automatic futures rollover;
- continuous contracts;
- contract-chain analytics;
- calendar spreads;
- other spread contracts;
- options;
- Trades Flat Files;
- Quotes Flat Files;
- broad exchange-wide ingestion;
- cross-asset reporting;
- formal exchange calendars;
- provider correction precedence rules;
- arbitrary duplicate resolution;
- merging CQG and Massive into one physical fact table;
- historical and Eventhouse reconciliation;
- production streaming Silver and Gold;
- Azure SQL persistence;
- production orchestration;
- multi-environment key-management services;
- generalised enterprise master-data management.

---

# 22. Validation Results

The controlled v1.3.0 implementation has confirmed:

1. `MESU6` and `MNQU6` map uniquely to separate `AtlasContractKey` values.
2. Each contract key maps to exactly one contract business key.
3. Each contract maps to exactly one product key.
4. Product and contract business keys are unique.
5. Every trusted Massive Silver row maps to one governed contract.
6. No conflicting duplicate apparent-grain records enter trusted Silver.
7. Massive minute grain is unique for both selected contracts.
8. Massive daily candles reconcile with accepted minute bars.
9. Provider `session_end_date` governs `TradingDate`.
10. `Decimal(18,5)` conversion is lossless for the selected contracts.
11. `gold_dim_date` contains the required controlled trading date.
12. `gold_dim_instrument` contains exactly two contract rows.
13. `gold_dim_instrument` filters both Massive fact tables correctly.
14. Instrument relationships are active, one-to-many and single-direction.
15. Date relationships are active, one-to-many and single-direction.
16. Existing CQG fact tables remain unchanged.
17. Existing CQG semantic-model relationships remain unchanged.
18. Massive price measures return correct values for `MESU6`.
19. Massive price measures return correct values for `MNQU6`.
20. Multiple-instrument price calculations are protected by single-contract guards.
21. Provider ticker values remain source attributes rather than canonical relationship keys.
22. Physical source lineage remains traceable to the Massive Flat File object and row.
23. Daily values reconcile with the persisted Massive minute table.
24. Daily Open uses the first chronological minute Open.
25. Daily Close uses the last chronological minute Close.
26. Daily High and Low reconcile with minute extrema.
27. Daily Volume, Transactions and Dollar Volume reconcile with minute totals.
28. Semantic-model measure folders were created successfully.
29. Technical instrument-dimension fields are hidden from report authors.
30. `ContractDisplayName` is sorted by `InstrumentSortOrder`.
31. No proprietary market-data files are committed to the public repository.
32. The validation report filters both daily and minute Massive measures correctly.

---

# 23. Remaining Decisions

The following decisions remain open after the controlled implementation:

- the durable long-term storage format for key seed mappings;
- authoritative source for currency;
- authoritative source for contract multiplier;
- authoritative mapping of Massive numeric exchange codes;
- future separation of provider mappings from `gold_dim_instrument`;
- how the CQG `F.US.EU6M12` contract maps into the governed identity structure;
- whether CQG facts should receive `AtlasContractKey`;
- whether Massive and CQG facts remain physically separate long term;
- whether a shared provider-neutral historical fact layer is desirable;
- how multiple historical sessions are loaded incrementally;
- whether Delta tables should be partitioned by `TradingDate`;
- how provider corrections and conflicting duplicate revisions are governed;
- how automatic futures rollover will eventually be modelled;
- whether continuous contracts are introduced;
- whether historical and Eventhouse data are reconciled;
- whether the temporary semantic-model validation report becomes a permanent regression asset;
- whether an ADR is required for the approved identity and key architecture.

The following are no longer open decisions:

```text
Initial instrument-dimension schema
Initial key allocation
Initial Massive contract mappings
Massive Bronze table grain
Massive Silver business grain
Massive Gold minute grain
Massive Gold daily grain
Initial semantic-model relationships
Single-contract price-measure behaviour
Measure folder structure
ContractDisplayName sorting
Initial technical-field visibility
```

---

# 24. Implemented Sequence

The controlled multi-instrument implementation was completed in the following order:

```text
1. Reviewed the existing CQG Silver, Gold and semantic-model implementation
2. Inspected Massive Futures contract metadata
3. Inspected Massive Futures Flat File catalogue structure
4. Validated one CME Futures minute-aggregate source object
5. Profiled selected contracts, precision and duplicate behaviour
6. Selected MNQU6 as the second governed historical contract
7. Approved product, contract and provider-mapping identity rules
8. Approved stable Atlas integer and text business keys
9. Defined gold_dim_instrument
10. Implemented nb_atlas_gold_dim_instrument
11. Validated and persisted gold_dim_instrument
12. Defined Massive Futures Bronze contract
13. Implemented nb_atlas_bronze_massive_futures_minute_aggregates
14. Added Azure Key Vault credential retrieval
15. Ingested one controlled Massive daily Flat File
16. Persisted 2,760 Bronze rows
17. Defined Massive Futures Silver contract
18. Implemented nb_atlas_silver_massive_futures_minute_aggregates
19. Validated identity mapping, typing and duplicate behaviour
20. Persisted 2,760 trusted Silver rows
21. Defined Massive Futures Gold contract
22. Implemented nb_atlas_gold_massive_futures_candles
23. Persisted 2,760 Massive minute Gold rows
24. Persisted two Massive daily Gold rows
25. Added the instrument dimension and Massive facts to sm_atlas_gold_reporting
26. Created four active dimension-to-fact relationships
27. Added guarded Massive daily measures
28. Added guarded Massive intraday measures
29. Organised measures into semantic display folders
30. Hid technical instrument-dimension attributes
31. Sorted ContractDisplayName by InstrumentSortOrder
32. Validated MESU6 and MNQU6 filtering and measure results
33. Created a temporary semantic-model validation report
```

Each material stage was validated before the next stage began.

---

# 25. Current Next Step

The controlled multi-instrument historical architecture is now implemented.

The immediate next step is documentation and release consolidation.

This includes:

```text
1. Update the Massive Futures Gold contract with semantic-model implementation results
2. Update the Atlas Master Context
3. Update the README architecture and feature summary
4. Update CHANGELOG.md
5. Update RELEASE_HISTORY.md
6. Review whether an ADR is required
7. Commit Fabric semantic-model and report changes
8. Commit local documentation and supporting scripts
9. Open the v1.3.0 pull request
10. Complete regression validation before release
```

The temporary validation report is:

```text
rpt_atlas_semantic_model_validation_dev
```

It may be retained during development as a regression and semantic-model validation asset.

A decision to retain, rename or delete it should be made before finalising the v1.3.0 release.

---

This document now records both the approved design and the completed controlled implementation for:

```text
MESU6
MNQU6
```

The architecture does not yet approve:

- automatic futures rollover;
- continuous contracts;
- broader exchange-wide ingestion;
- provider correction precedence;
- cross-provider fact consolidation;
- historical and near-real-time reconciliation.

---

This document records a proposed direction.

It does not become an approved architecture contract until the identity, key, dimension and semantic-model decisions have been reviewed and the relevant contract changes have been accepted.