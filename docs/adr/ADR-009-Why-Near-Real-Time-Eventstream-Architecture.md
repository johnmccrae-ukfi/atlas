# ADR-009 — Why Near-Real-Time Eventstream Architecture

**Status:** Accepted

**Date:** 2026-07-13

**Decision Makers:** UK Future Innovations (Atlas Engineering)

---

# Context

Atlas originally implemented a historical market-data architecture based on:

```text
CQG legacy futures ticks
→ Microsoft Fabric Lakehouse
→ Bronze, Silver and Gold layers
→ Direct Lake semantic model
→ Power BI
```

This architecture is appropriate for historical ingestion, repeatable transformations, curated analytics and AI-ready datasets.

Atlas v1.1.0 introduces a new requirement:

> ingest delayed futures minute aggregates as they arrive and make them available for near-real-time querying, validation and operational visualisation.

The initial source is the Massive delayed Futures WebSocket using:

```text
AM.MESU6
```

The Massive feed requires:

- an authenticated outbound WebSocket connection;
- a provider-specific subscription message;
- persistent connection handling;
- provider payload validation;
- conversion into an Atlas-controlled event contract;
- publication into Microsoft Fabric.

Microsoft Fabric Eventstream does not provide a native Massive Futures connector.

The solution therefore requires an architectural boundary between the external provider WebSocket and Fabric Real-Time Intelligence.

The v1.1.0 release is also being developed using a Microsoft Fabric trial capacity. The objective is to prove the complete vertical slice without prematurely introducing production cloud hosting or operational complexity.

---

# Decision

Atlas will implement the initial near-real-time pathway as:

```text
Massive delayed Futures WebSocket
        |
        v
Atlas Python streaming adapter
        |
        v
Microsoft Fabric Eventstream custom endpoint
        |
        v
Microsoft Fabric Eventhouse and KQL Database
        |
        v
Raw futures minute aggregates
        |
        v
KQL validation and Real-Time Dashboard
```

For v1.1.0:

- the Python streaming adapter will run locally;
- the adapter will connect to the Massive delayed Futures WebSocket;
- the adapter will subscribe only to `AM.MESU6`;
- the adapter will transform provider events into a governed Atlas envelope;
- the adapter will publish through the Event Hubs-compatible Eventstream custom endpoint;
- Eventstream will use direct ingestion;
- Eventhouse will persist events in an explicitly defined KQL table;
- an explicit JSON ingestion mapping will be used;
- the historical Lakehouse pathway and near-real-time Eventhouse pathway will remain separate.

The implementation is a controlled development vertical slice rather than a production-hosted streaming service.

---

# Architecture

```text
Historical Path

CQG Legacy Files
        |
        v
Fabric Lakehouse
        |
        v
Bronze
        |
        v
Silver
        |
        v
Gold
        |
        v
Direct Lake Semantic Model
        |
        v
Power BI


Near-Real-Time Path

Massive Delayed WebSocket
        |
        v
Atlas Python Streaming Adapter
        |
        v
Fabric Eventstream
        |
        v
Fabric Eventhouse
        |
        v
Raw KQL Table
        |
        v
KQL Queries and Real-Time Dashboard
```

The two paths serve different purposes:

| Path | Primary purpose |
|---|---|
| Historical Lakehouse | Repeatable transformation, curated analytics and long-term reporting |
| Near-real-time Eventhouse | Operational ingestion, low-latency querying and live monitoring |

---

# Why an External Python Adapter?

The Massive Futures feed requires provider-specific WebSocket behaviour.

The adapter is responsible for:

- loading the Massive API key;
- opening and maintaining the WebSocket connection;
- authenticating with Massive;
- subscribing to `AM.MESU6`;
- processing provider status messages;
- receiving completed minute aggregates;
- validating required fields;
- validating interval duration;
- validating OHLC consistency;
- validating non-negative measures;
- converting epoch milliseconds into UTC;
- adding Atlas lineage metadata;
- preserving the original provider payload;
- publishing the transformed event into Fabric.

Keeping this logic outside Fabric provides a clear provider boundary and avoids embedding provider-specific concerns into downstream storage and analytics components.

It also supports future provider abstraction and replacement.

---

# Why Local Hosting for v1.1.0?

The adapter will run locally during the initial release.

This was selected because the release objective is to validate:

- provider connectivity;
- event transformation;
- Eventstream publishing;
- Eventhouse ingestion;
- KQL validation;
- dashboard live refresh.

Introducing cloud hosting at this stage would add unrelated complexity, including:

- containerisation;
- deployment configuration;
- managed secrets;
- health probes;
- operational monitoring;
- restart policies;
- cloud cost;
- infrastructure lifecycle management.

Local hosting is therefore proportionate for the current trial-capacity and portfolio-development phase.

It must not be described as production hosting.

---

# Why Eventstream Custom Endpoint?

Fabric Eventstream does not provide a native Massive Futures WebSocket source.

The custom endpoint provides an Event Hubs-compatible ingestion boundary that allows the Atlas adapter to publish external events into Fabric.

This supports:

- decoupling between provider logic and Fabric storage;
- standard Azure Event Hubs client libraries;
- future replacement of the local adapter runtime;
- Eventstream routing and destination management;
- Fabric-native lifecycle and Git integration.

The Eventstream source is:

```text
src_atlas_massive_futures
```

The Eventstream item is:

```text
es_atlas_massive_futures_dev
```

---

# Why Direct Ingestion?

The initial Eventstream route uses direct ingestion into Eventhouse.

No Eventstream transformation operator is applied.

This was selected because the Atlas Python transformer already produces a governed event envelope containing:

- provider fields;
- canonical UTC timestamps;
- typed financial values;
- Atlas lineage metadata;
- schema version;
- deterministic event identifier;
- original raw payload.

Adding a second transformation layer in Eventstream would duplicate responsibility and make the raw ingestion path harder to reason about.

Future transformed routes may be added separately without changing the fidelity of the raw path.

---

# Why Eventhouse?

Eventhouse is designed for high-volume, time-oriented event data and low-latency KQL analysis.

It is a better fit for the initial streaming hot path than writing each incoming event directly into the historical Lakehouse Medallion pipeline.

Eventhouse provides:

- rapid event ingestion;
- time-series querying;
- built-in ingestion timestamps;
- KQL analytics;
- operational validation;
- Real-Time Dashboard integration;
- live refresh based on newly ingested data.

The Eventhouse and KQL database are:

```text
eh_atlas_realtime_dev
```

The raw table is:

```text
raw_massive_futures_minute_aggregates
```

---

# Why an Explicit KQL Schema?

Atlas defines the raw KQL table before ingestion.

The schema preserves:

- provider epoch values as `long`;
- canonical event timestamps as `datetime`;
- financial values as `decimal`;
- volume and event counts as `long`;
- provider payload as `dynamic`;
- Atlas lineage and schema metadata.

Automatic schema inference was rejected because it attempted to:

- introduce duplicate `_1` columns;
- convert epoch fields into datetimes;
- infer financial values as `real`;
- change the deliberately governed schema.

An explicit table contract improves:

- consistency;
- auditability;
- decimal precision;
- schema governance;
- downstream query stability.

---

# Why an Explicit JSON Ingestion Mapping?

Atlas uses:

```text
raw_massive_futures_minute_aggregates_json_mapping
```

The mapping binds Atlas event-envelope fields directly to the intended KQL columns.

This prevents automatic inference from changing types or adding unintended columns.

It also makes ingestion behaviour:

- repeatable;
- inspectable;
- versionable;
- easier to troubleshoot.

---

# Why Preserve the Raw Provider Payload?

The original Massive payload is retained in:

```text
raw_payload
```

This supports:

- provider fidelity;
- troubleshooting;
- auditability;
- future schema comparison;
- replay design;
- correction analysis;
- validation of transformed values.

The provider payload is preserved alongside normalised Atlas columns rather than used as the only persisted representation.

---

# Why Keep Historical and Near-Real-Time Paths Separate?

The historical and near-real-time paths currently have different operating characteristics.

The historical path provides:

- full batch replay;
- Medallion transformations;
- curated Gold datasets;
- semantic modelling;
- long-term Power BI reporting.

The near-real-time path provides:

- event-driven ingestion;
- fast operational querying;
- ingestion latency measurement;
- live dashboard refresh;
- raw event validation.

Combining both paths in v1.1.0 would require decisions about:

- hot and cold data convergence;
- reconciliation;
- duplicate handling;
- late-arriving data;
- contract rollover;
- common Silver models;
- historical backfill;
- retention policies.

These concerns are outside the controlled vertical-slice scope.

The paths will therefore remain separate until a later architectural decision defines their convergence.

---

# Benefits

The selected architecture provides:

- a clear provider integration boundary;
- low coupling between Massive and Fabric;
- explicit event-schema governance;
- preserved raw provider fidelity;
- low-latency Eventhouse ingestion;
- reusable KQL validation;
- live operational monitoring;
- a production-relevant architecture without premature hosting complexity;
- a clear migration path from local to cloud hosting;
- strong Microsoft Fabric Real-Time Intelligence portfolio evidence.

---

# Alternatives Considered

## Fabric-Native Massive Connector

Use a built-in Eventstream connector for Massive Futures.

**Rejected because:**

- no native Massive Futures connector is available;
- the provider requires authenticated WebSocket subscription behaviour;
- provider-specific transformation is still required.

---

## Poll the Massive REST API from Fabric

Use scheduled REST requests to retrieve the latest minute aggregates.

**Rejected because:**

- it changes the architecture from streaming to polling;
- it does not prove WebSocket ingestion;
- it introduces polling-state and duplicate retrieval concerns;
- it does not use the subscribed provider delivery mechanism.

REST remains useful for diagnostics, historical validation and possible recovery workflows.

---

## Azure Function as the Persistent Adapter

Host the permanent WebSocket connection inside an Azure Function.

**Rejected for the initial architecture because:**

- the workload is a continuously running worker;
- a persistent socket is not a natural bounded function execution;
- hosting-plan and timeout concerns add complexity;
- repeated short executions would create unnecessary reconnect churn.

Azure Functions may still be appropriate for bounded supporting tasks such as contract discovery, rollover checks or health monitoring.

---

## Azure Container Apps for v1.1.0

Containerise and host the adapter immediately.

**Deferred because:**

- production hosting is not required to validate the vertical slice;
- Fabric is currently running on trial capacity;
- the additional infrastructure would distract from the release objective.

Azure Container Apps remains a likely future hosting option.

---

## Write Streaming Events Directly to Lakehouse

Publish each incoming event directly into Lakehouse Delta tables.

**Rejected because:**

- the initial requirement is operational near-real-time analysis;
- Eventhouse is better suited to time-series event ingestion and KQL;
- direct Lakehouse ingestion would prematurely merge the hot and historical paths;
- a governed convergence strategy has not yet been defined.

---

## Eventstream Transformation Before Ingestion

Transform events inside Eventstream before writing to Eventhouse.

**Rejected for the raw route because:**

- the Python adapter already creates the Atlas envelope;
- duplicated transformation logic would reduce clarity;
- raw-path fidelity should remain simple and inspectable.

Future transformed routes may use Eventstream processing where justified.

---

## Automatic Schema Inference

Allow Fabric to infer and alter the destination schema.

**Rejected because:**

- inferred types did not match the intended contract;
- duplicate columns were proposed;
- financial values risked reduced precision;
- schema drift would be less controlled.

---

# Consequences

## Positive

- Provider-specific logic is isolated.
- Fabric receives a governed Atlas event contract.
- Eventhouse supports rapid operational analysis.
- Raw provider fidelity is retained.
- KQL validation is repeatable.
- Dashboard refresh is ingestion-aware.
- The solution can later move from local to cloud hosting without changing downstream Fabric architecture.
- The design is easy to explain during technical interviews and client discussions.

## Negative

- Ingestion stops when the local process is not running.
- Local workstation availability affects the stream.
- SAS credentials are currently stored in the ignored local `.env`.
- The implementation does not yet provide durable buffering.
- The destination does not enforce idempotency.
- Historical and near-real-time data are queried separately.
- Additional architecture will be required for production hosting and reconciliation.

---

# Risks

| Risk | Mitigation |
|---|---|
| Local adapter stops unexpectedly | Document development-hosted limitation and use clean operational logging. |
| Workstation sleeps or loses connectivity | Treat v1.1.0 as a controlled development implementation. |
| Duplicate publication | Use deterministic `atlas_event_id` and validate duplicates in KQL. |
| Schema drift | Use an explicit KQL schema and JSON ingestion mapping. |
| Financial precision loss | Transport values faithfully and persist them as KQL `decimal`. |
| Provider payload changes | Preserve `raw_payload` and use versioned Atlas envelopes. |
| Multiple adapter instances create duplicates | Run a single adapter instance during the initial release. |
| Historical and streaming data diverge | Defer convergence until reconciliation rules are explicitly designed. |
| Secret exposure | Keep `.env` ignored and commit placeholders only through `.env.example`. |

---

# Validation

The architecture was validated using genuine delayed `AM.MESU6` minute aggregates.

Confirmed:

- successful Massive WebSocket connection;
- successful authentication;
- successful `AM.MESU6` subscription;
- provider payload receipt;
- Atlas event transformation;
- Eventstream publication;
- Eventhouse ingestion;
- explicit schema and mapping behaviour;
- nested raw payload preservation;
- no duplicate live event identifiers;
- 60-second continuity while the adapter was active;
- no invalid OHLC or negative-measure rows;
- live dashboard refresh.

Initial sample measurements:

```text
Average provider delay:           approximately 603.9 seconds
Average Fabric ingestion latency: approximately 0.47 seconds
Average end-to-end latency:       approximately 604.4 seconds
```

The results demonstrate that observed latency is dominated by the delayed provider feed rather than Atlas or Fabric ingestion.

---

# Future Evolution

Future releases may introduce:

- configurable multi-instrument subscriptions;
- simultaneous current and next contract ingestion;
- automatic contract rollover;
- advanced reconnect and retry policies;
- durable local or cloud buffering;
- replay after disconnection;
- provider correction handling;
- destination-level deduplication;
- schema registry integration;
- Eventstream transformation routes;
- streaming Silver and Gold models;
- Eventhouse materialised views;
- alerting and Fabric Activator;
- Power BI DirectQuery over Eventhouse;
- near-real-time candlestick visualisation;
- Azure Container Apps hosting;
- Azure Key Vault integration;
- managed identity where supported;
- deployment automation;
- historical and near-real-time reconciliation.

Significant future changes should be recorded through additional ADRs.

---

# Relationship to Existing ADRs

ADR-001 selected Microsoft Fabric as the strategic platform.

ADR-002 established the Medallion Architecture for historical and analytical processing.

ADR-006 established the market-data abstraction layer.

ADR-009 extends Atlas with a complementary near-real-time ingestion path while preserving the existing historical Medallion architecture.

---

# Decision Summary

Atlas will use an external Python streaming adapter, Fabric Eventstream custom endpoint and Eventhouse direct ingestion for the initial near-real-time market-data pathway.

The adapter will run locally during v1.1.0 because the objective is to validate the streaming vertical slice without prematurely introducing production hosting infrastructure.

Atlas will preserve explicit schema governance, raw provider fidelity and a clear separation between provider integration, Fabric delivery and Eventhouse storage.

The historical Lakehouse and near-real-time Eventhouse pathways will remain separate until a later architectural decision defines reconciliation and convergence.