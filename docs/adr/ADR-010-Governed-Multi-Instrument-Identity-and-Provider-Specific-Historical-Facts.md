# ADR-010 — Governed Multi-Instrument Identity and Provider-Specific Historical Facts

## Status

**Accepted**

## Date

2026-07-17

## Decision Owners

Atlas Platform Architecture

## Related Release

```text
v1.3.0 — Multi-Instrument Architecture
```

## Related Documents

```text
docs/01_Architecture/Atlas_Multi_Instrument_Identity_and_Grain_Design.md
docs/01_Architecture/Massive_Futures_Bronze_Contract.md
docs/01_Architecture/Massive_Futures_Silver_Contract.md
docs/01_Architecture/Massive_Futures_Gold_Contract.md
docs/00_Project/ATLAS_MASTER_CONTEXT.md
```

---

# 1. Context

Atlas originally implemented one historical market-data pathway based on a legacy CQG Futures tick file.

The CQG source contains individual market events and requires deterministic source ordering before Atlas can calculate minute and daily OHLC candles.

The initial CQG pathway is:

```text
CQG legacy event data
→ source-aligned Bronze data
→ silver_cqg_ticks
→ gold_cqg_minute_candles
→ gold_cqg_daily_candles
```

Atlas subsequently introduced a near-real-time Massive Futures pathway using delayed provider-generated minute aggregates:

```text
Massive delayed Futures WebSocket
→ Atlas Python streaming adapter
→ Microsoft Fabric Eventstream
→ Eventhouse and KQL Database
→ Real-Time Dashboard
```

For `v1.3.0`, Atlas introduced a third pathway: historical Massive Futures Flat Files containing provider-generated minute aggregates.

The selected controlled scope contains:

```text
MESU6
MNQU6
```

The Massive historical source differs materially from the CQG historical source.

CQG provides:

> Individual source market events requiring Atlas-generated interval aggregation.

Massive provides:

> Provider-generated minute OHLC aggregates that Atlas validates and projects into governed analytical structures.

The two sources therefore have different:

- physical grains;
- business grains;
- event-ordering capabilities;
- activity-measure semantics;
- lineage requirements;
- duplicate behaviour;
- transformation responsibilities.

Atlas also requires a durable identity model capable of distinguishing:

- provider identity;
- provider ticker;
- trading venue;
- asset class;
- Futures product;
- dated Futures contract;
- internal Atlas product identity;
- internal Atlas contract identity.

Provider symbols alone are not sufficient as long-term canonical keys because:

- symbols are provider-specific;
- equivalent contracts may have different provider representations;
- ticker formats may change;
- provider symbols may be reused over time;
- product identity and dated-contract identity are different concepts;
- future cross-provider reconciliation requires identity independent of one vendor.

The architecture therefore requires an explicit decision covering both:

1. governed multi-instrument identity;
2. whether provider-specific historical facts should remain separate or be consolidated immediately.

---

# 2. Decision Drivers

## 2.1 Stable Identity

Atlas requires stable internal identifiers that do not depend on:

- provider response order;
- file row order;
- alphabetical ordering;
- runtime-generated row numbers;
- load timestamps;
- semantic-model refresh behaviour.

## 2.2 Provider Independence

Atlas must avoid using a Massive or CQG symbol as the permanent canonical relationship key.

Provider symbols must remain source and mapping attributes.

## 2.3 Product and Contract Separation

The architecture must distinguish:

```text
Futures product
```

from:

```text
dated Futures contract
```

For example:

```text
Micro E-mini S&P 500
```

is a product, while:

```text
MESU6
```

represents a dated September 2026 contract through the Massive provider.

## 2.4 Source-Grain Fidelity

CQG event data and Massive minute aggregates must not be forced into one physical table where their underlying business meanings differ.

## 2.5 Financial Accuracy

The architecture must not combine activity fields whose semantics are not proven equivalent.

For example:

```text
CQG TradeCount
```

must not automatically be treated as identical to:

```text
Massive TransactionCount
```

## 2.6 Semantic-Model Governance

Power BI and Direct Lake reporting require governed dimensions and explicit relationships rather than unmanaged text joins.

## 2.7 Incremental Evolution

Atlas must support future providers and instruments without prematurely implementing:

- automatic Futures rollover;
- continuous contracts;
- cross-provider fact consolidation;
- universal precision rules;
- streaming and historical reconciliation.

## 2.8 Regression Protection

The existing CQG implementation and reports must remain stable while the new Massive pathway is introduced.

---

# 3. Decision

Atlas will adopt a governed internal product-and-contract identity model and retain provider-specific historical fact tables.

The decision has five principal parts.

---

## 3.1 Stable Atlas Product Identity

Atlas will assign a stable internal key and business key to each governed Futures product.

The initial product mappings are:

```text
AtlasProductKey:
1001

AtlasProductBusinessKey:
FUT-XCME-MES

Product:
Micro E-mini S&P 500
```

```text
AtlasProductKey:
1002

AtlasProductBusinessKey:
FUT-XCME-MNQ

Product:
Micro E-mini Nasdaq-100
```

The product key represents the underlying traded product rather than a dated contract.

Product keys must not be generated dynamically from source order or runtime execution.

---

## 3.2 Stable Atlas Contract Identity

Atlas will assign a stable internal key and business key to each governed dated Futures contract.

The initial contract mappings are:

```text
AtlasContractKey:
2001

AtlasContractBusinessKey:
FUT-XCME-MES-2026-09

ProviderTicker:
MESU6
```

```text
AtlasContractKey:
2002

AtlasContractBusinessKey:
FUT-XCME-MNQ-2026-09

ProviderTicker:
MNQU6
```

The contract key represents one dated Futures contract.

The key does not represent:

- an automatic front-month contract;
- a continuous contract;
- a rollover series;
- a generic provider symbol;
- the underlying product alone.

Contract keys must remain stable across repeat processing and semantic-model refreshes.

---

## 3.3 Governed Instrument Dimension

Atlas will use:

```text
gold_dim_instrument
```

as the governed instrument dimension for the initial Massive historical implementation.

Its grain is:

> One row per governed Atlas dated Futures contract.

The dimension contains:

- Atlas contract identity;
- Atlas product identity;
- provider mapping;
- contract code;
- contract display name;
- contract month and year;
- product name;
- trading venue;
- asset class;
- trade dates;
- settlement date;
- tick-size metadata;
- active status;
- deterministic sort order.

The dimension will provide the one side of the Massive historical relationships:

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

Both relationships will be:

- active;
- one-to-many;
- single-direction;
- filtered from dimension to fact.

The preferred user-facing contract slicer will be:

```text
gold_dim_instrument[ContractDisplayName]
```

Technical relationship keys and provider-mapping fields may be hidden from normal report authors while remaining available for relationships, calculations and debugging.

---

## 3.4 Provider-Specific Historical Facts

Atlas will retain separate physical historical fact tables for CQG and Massive.

The CQG Gold facts remain:

```text
gold_cqg_minute_candles
gold_cqg_daily_candles
```

The Massive Gold facts are:

```text
gold_massive_futures_minute_candles
gold_massive_futures_daily_candles
```

The fact tables will not be physically consolidated during `v1.3.0`.

This preserves the different source semantics.

### CQG

CQG minute candles are generated by Atlas from ordered source events.

CQG activity currently uses fields such as:

```text
TradeCount
TotalTrades
```

CQG Gold may retain event-ordering attributes derived from the source data.

### Massive

Massive minute candles originate from provider-generated minute aggregates.

Massive activity includes:

```text
Volume
TransactionCount
DollarVolume
```

Massive does not expose the underlying event sequence required to reproduce the CQG ordering model.

Atlas will not fabricate equivalent event-sequence fields for Massive.

---

## 3.5 Shared Dimensions Without Premature Fact Consolidation

Provider-specific facts may share governed dimensions where the relationship semantics are valid.

For the controlled Massive implementation, the shared Date relationships are:

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

The existing CQG Date relationships remain unchanged.

The initial `gold_dim_instrument` dimension will filter the Massive historical facts only.

CQG facts will not be assigned an `AtlasContractKey` until:

- the exact CQG product identity is approved;
- the exact CQG dated-contract identity is approved;
- the key mapping is governed;
- the facts are updated safely;
- existing report and measure behaviour is regression-tested.

Atlas will therefore converge provider paths first through governed identity and semantic modelling, not through premature physical table consolidation.

---

# 4. Provider Mapping Rules

Provider tickers are mapping attributes rather than canonical Atlas keys.

The initial mappings are:

```text
Massive + MESU6
→ AtlasContractKey 2001
```

```text
Massive + MNQU6
→ AtlasContractKey 2002
```

A provider mapping must identify at least:

```text
SourceProvider
ProviderTicker
AtlasContractKey
```

Future designs may move provider mappings into a separate bridge or mapping table when:

- multiple providers represent the same Atlas contract;
- multiple ticker aliases exist;
- mapping history becomes temporal;
- provider-specific attributes expand;
- instrument-dimension ownership becomes too broad.

The initial implementation may retain one provider mapping in `gold_dim_instrument` because the controlled scope contains one historical provider mapping per contract.

---

# 5. Key Allocation Rules

Atlas integer keys will be allocated explicitly through governed seed mappings.

Keys must not be derived from:

- `ROW_NUMBER`;
- alphabetical sorting;
- load order;
- provider response order;
- source row number;
- hash truncation without a governed collision strategy;
- current timestamp;
- semantic-model-generated identifiers.

Key allocation must be:

- deterministic;
- documented;
- repeatable;
- reviewable;
- independent of execution order.

Business keys must be readable and stable.

The initial naming convention is:

```text
Product:
FUT-<TRADING_VENUE>-<PRODUCT_CODE>
```

```text
Contract:
FUT-<TRADING_VENUE>-<PRODUCT_CODE>-<YYYY>-<MM>
```

This convention may be extended through a superseding decision if Atlas expands into asset classes where the structure is unsuitable.

---

# 6. Semantic-Model Measure Behaviour

Measures returning one price or point-in-time value must not silently combine unrelated contracts.

Massive price measures will require exactly one governed Atlas contract in filter context.

Expected behaviour:

```text
one Atlas contract selected
→ return the calculated value
```

```text
zero or multiple Atlas contracts selected
→ return blank
```

The model may implement this through logic equivalent to:

```DAX
HASONEVALUE (
    gold_dim_instrument[AtlasContractKey]
)
```

Additive activity measures may aggregate across selected Massive contracts where:

- the underlying field is additive;
- the measure name makes the behaviour clear;
- the report context is not misleading.

CQG and Massive activity measures will remain separate until their semantics are formally reconciled.

---

# 7. Futures Rollover and Continuous Contracts

This decision does not approve automatic Futures rollover.

Atlas will not currently interpret:

```text
MES
```

or:

```text
MNQ
```

as an automatically changing front-month contract.

Each governed row represents a specific dated contract.

The following remain separate future decisions:

- current-contract selection;
- next-contract preloading;
- expiry transition rules;
- liquidity-based rollover;
- calendar-based rollover;
- back-adjusted continuous series;
- unadjusted continuous series;
- contract-chain analytics;
- cross-contract indicator continuity.

Historical indicators for one dated contract must not be presented as though they automatically continue into another dated contract.

---

# 8. Historical and Near-Real-Time Identity

The `v1.3.0` identity model applies initially to the Massive historical Lakehouse pathway.

The existing Eventhouse stream currently uses provider-oriented fields such as:

```text
AM.MESU6
```

The streaming pathway does not yet use:

```text
AtlasContractKey
```

This ADR establishes the identity model that future streaming work should adopt, but it does not claim that historical and streaming identity are already reconciled.

Future Real-Time Intelligence work must define:

- how streaming provider symbols map to Atlas contract keys;
- whether mapping occurs in the adapter, Eventstream, KQL or a later transformation;
- correction and late-arrival behaviour;
- historical and streaming reconciliation;
- rollover handling;
- contract-expiry transitions.

---

# 9. Alternatives Considered

## 9.1 Use Provider Ticker as the Canonical Key

Examples:

```text
MESU6
MNQU6
```

### Advantages

- simple;
- directly available from the source;
- readable;
- minimal transformation.

### Rejected Because

- provider-specific;
- unsuitable for cross-provider mappings;
- may be reused or reformatted;
- does not distinguish canonical identity from source representation;
- weakens future reconciliation and governance.

---

## 9.2 Generate Integer Keys Dynamically During Each Load

Examples:

- Spark row numbering;
- alphabetical ordering;
- provider response order.

### Advantages

- easy to implement;
- no maintained seed mapping.

### Rejected Because

- keys may change between executions;
- relationships could become unstable;
- model refreshes could produce inconsistent identity;
- execution order would influence business identity;
- lineage and debugging would be weakened.

---

## 9.3 Consolidate CQG and Massive into Shared Historical Fact Tables Immediately

### Advantages

- fewer tables;
- potentially simpler report-authoring experience;
- shared measure definitions might appear easier.

### Rejected Because

- source grains differ;
- activity semantics differ;
- Massive bars lack CQG event-ordering metadata;
- nullable provider-specific fields would proliferate;
- false canonical equivalence could be introduced;
- regression risk to the proven CQG path would increase;
- one controlled Massive session is insufficient evidence for full physical consolidation.

---

## 9.4 Create Separate Semantic Models for CQG and Massive

### Advantages

- complete provider isolation;
- fewer shared relationship decisions;
- simpler provider-specific models.

### Rejected Because

- fragments governed reporting;
- duplicates shared Date logic;
- reduces the value of a common semantic layer;
- weakens the multi-instrument architecture demonstration;
- makes future comparison and shared reporting harder.

Provider-specific facts can coexist within one governed semantic model without being physically merged.

---

## 9.5 Implement Automatic Rollover During v1.3.0

### Advantages

- user-facing generic product selection;
- easier current-contract reporting;
- apparent continuity across expiry.

### Rejected Because

- rollover policy has not been governed;
- liquidity and calendar rules have not been evaluated;
- historical adjustment methodology is undefined;
- indicators could become misleading;
- the controlled release scope is intended to validate identity and grain first.

---

# 10. Consequences

## 10.1 Positive Consequences

- Atlas now has stable provider-neutral product and contract identity.
- The same contract can support future mappings from multiple providers.
- Provider symbols remain traceable without controlling the canonical model.
- Product identity is separated from dated-contract identity.
- The semantic model gains a governed Instrument dimension.
- Price measures can enforce safe single-contract behaviour.
- CQG and Massive retain source-appropriate grains.
- Existing CQG behaviour is protected.
- Future rollover and continuous-contract work has a stable identity foundation.
- Historical and streaming convergence can use governed contract keys later.
- The architecture demonstrates realistic enterprise modelling rather than simple ticker grouping.

## 10.2 Negative Consequences

- The model contains more fact tables.
- Some measures remain provider-specific.
- Report authors must understand that CQG and Massive are not yet one consolidated fact model.
- CQG does not initially participate in `gold_dim_instrument`.
- Provider mapping remains embedded in the first instrument-dimension version.
- Explicit key seed mappings require governance and maintenance.
- Cross-provider comparisons require further design.
- The model does not yet provide a generic front-month experience.

## 10.3 Risks

- Key mappings could diverge if edited independently across notebooks or documents.
- Future providers may require richer mapping structures.
- The dimension may become overloaded if provider mappings grow substantially.
- Report users may expect multi-selection price aggregation unless guarded measures are used.
- Contract metadata may require correction as authoritative sources improve.
- Premature rollover implementation could undermine the dated-contract model.

These risks will be managed through contracts, validation, documentation and future ADRs.

---

# 11. Implementation Summary

The initial accepted implementation includes:

```text
gold_dim_instrument
```

with:

```text
AtlasProductKey:
1001, 1002

AtlasContractKey:
2001, 2002
```

The implemented Massive historical facts are:

```text
gold_massive_futures_minute_candles
gold_massive_futures_daily_candles
```

The Direct Lake model includes relationships from:

```text
gold_dim_date
```

and:

```text
gold_dim_instrument
```

to both Massive facts.

The model retains:

```text
Daily Candles
Minute Candles
```

for the existing CQG path.

No direct fact-to-fact relationship is created.

The controlled implementation is validated for:

```text
MESU6
MNQU6
TradingDate 2026-07-14
```

---

# 12. Validation Requirements

The decision remains valid only while the implementation confirms:

- product keys are unique and non-null;
- contract keys are unique and non-null;
- business keys are unique and non-null;
- each contract maps to exactly one product;
- each provider ticker maps to exactly one governed contract in the accepted scope;
- Massive Silver rows map to one contract;
- Massive Gold grain is unique;
- Date and Instrument relationships are active and one-to-many;
- relationship filtering is single-direction;
- guarded price measures return blank for ambiguous contract context;
- existing CQG facts and measures remain unchanged;
- provider symbols remain traceable;
- no proprietary market data or credentials are committed.

A failure of these assumptions requires investigation and may require a superseding ADR.

---

# 13. Future Decisions

This ADR does not settle the following matters:

- authoritative currency metadata;
- contract multipliers;
- authoritative numeric exchange-code mappings;
- provider-mapping bridge design;
- CQG contract mapping into `gold_dim_instrument`;
- consolidation of provider-specific historical facts;
- historical incremental-load strategy;
- partitioning and clustering;
- provider correction precedence;
- multiple-provider mappings for one contract;
- contract-chain modelling;
- automatic rollover;
- continuous contracts;
- historical and streaming reconciliation;
- streaming propagation of `AtlasContractKey`;
- formal exchange calendars;
- product-level versus contract-level reporting defaults.

These require implementation evidence and may warrant separate ADRs.

---

# 14. Supersession

This ADR is not currently superseded.

If Atlas later adopts:

- shared provider-neutral physical fact tables;
- a separate provider-mapping bridge;
- automatically governed rollover;
- continuous-contract identities;
- a materially different key strategy;

a new ADR must supersede the relevant parts of this decision.

The original ADR must remain in the repository as a record of the architecture adopted for `v1.3.0`.

---

# 15. Final Decision Statement

Atlas will use stable internal product and dated-contract identities, represented through governed Atlas keys and business keys.

`gold_dim_instrument` will provide governed contract-level relationships for the initial Massive historical facts.

CQG and Massive historical facts will remain physically separate because their source grains, ordering capabilities and activity semantics differ.

Provider tickers will remain mapping attributes rather than canonical relationship keys.

Historical and streaming data will converge only through future governed identity, reconciliation and rollover decisions.

Automatic rollover and continuous contracts are explicitly outside the scope of this ADR and `v1.3.0`.
