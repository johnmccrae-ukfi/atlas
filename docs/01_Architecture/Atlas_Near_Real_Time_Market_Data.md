# Atlas Near-Real-Time Market Data Architecture

## 1. Purpose

This document describes the initial near-real-time market-data architecture introduced for:

> **Atlas v1.1.0 — Near-Real-Time Market Data Foundation**

The release implements a controlled vertical slice that proves Atlas can ingest continuously arriving futures market data into Microsoft Fabric while preserving the existing historical Lakehouse and medallion architecture.

The implemented pathway is:

```text
Massive delayed Futures WebSocket
        |
        v
Atlas Python streaming adapter
        |
        v
Microsoft Fabric Eventstream
        |
        v
Eventhouse and KQL Database
        |
        v
Raw near-real-time futures minute aggregates
        |
        v
KQL validation and Real-Time Dashboard
```

This is an architectural foundation rather than a production-complete streaming platform.

---

## 2. Scope

### 2.1 Implemented Scope

The initial implementation supports:

- the Massive delayed Futures WebSocket;
- one futures contract:
  - `MESU6`;
- one event type:
  - `AM` minute aggregates;
- one subscription:
  - `AM.MESU6`;
- a locally hosted Python streaming adapter;
- Atlas event-envelope transformation;
- publication to a Fabric Eventstream custom endpoint;
- direct ingestion into Eventhouse;
- a governed raw KQL table;
- explicit JSON ingestion mapping;
- KQL validation queries;
- a minimal Real-Time Dashboard;
- latency, continuity, duplicate, and OHLC validation.

### 2.2 Explicitly Excluded

The v1.1.0 implementation does not yet provide:

- production cloud hosting for the Python adapter;
- broad multi-instrument streaming;
- wildcard subscriptions;
- futures trades;
- quotes or top-of-book data;
- per-second aggregates;
- streaming Silver and Gold layers;
- real-time technical indicators;
- automatic futures contract rollover;
- durable delivery queues;
- duplicate suppression;
- provider corrections handling;
- advanced reconnect and replay logic;
- enterprise monitoring and alerting;
- deployment automation;
- historical and streaming reconciliation;
- managed identity;
- Azure Key Vault integration;
- production security hardening.

These capabilities remain future roadmap items.

---

## 3. Relationship to the Existing Atlas Architecture

The near-real-time pathway supplements rather than replaces the existing historical architecture.

The existing historical pathway remains:

```text
CQG legacy futures ticks
        |
        v
Bronze Parquet and OneLake
        |
        v
Silver canonical ticks
        |
        v
Gold minute and daily OHLC
        |
        v
Direct Lake semantic model
        |
        v
Power BI
        |
        v
Deterministic session summaries
        |
        v
AI market commentary framework
```

The new near-real-time pathway is currently independent:

```text
Massive delayed Futures WebSocket
        |
        v
Atlas Python streaming adapter
        |
        v
Fabric Eventstream
        |
        v
Eventhouse
        |
        v
Raw KQL table
        |
        v
KQL validation and Real-Time Dashboard
```

The two pathways are intentionally not yet merged into a common Silver or Gold model.

Future releases may introduce governed convergence between the historical Lakehouse pathway and the Eventhouse hot path.

---

## 4. Market-Data Provider

### 4.1 Provider

The initial near-real-time source is:

```text
Massive
```

### 4.2 Subscription

The project currently uses:

```text
Massive Futures Starter
```

The confirmed entitlement includes:

- CME, CBOT, NYMEX, and COMEX futures;
- all Futures tickers;
- 10-minute-delayed data;
- two years of historical data;
- minute aggregates;
- second aggregates;
- WebSockets;
- snapshots;
- reference data;
- flat files.

The subscription does not include:

- individual trades;
- quotes;
- top-of-book data.

### 4.3 WebSocket Endpoint

The delayed Futures WebSocket endpoint is:

```text
wss://delayed.massive.com/futures
```

### 4.4 Initial Contract

The initial contract is:

```text
MESU6
```

This is the September 2026 Micro E-mini S&P 500 futures contract.

The initial subscription is:

```text
AM.MESU6
```

Where:

```text
AM = minute aggregate
```

### 4.5 Contract Rollover

Automatic contract rollover is not implemented.

The provisional design direction is that Atlas will eventually:

1. ingest both the current and next active contracts;
2. maintain contract-specific analytics independently;
3. determine the designated front contract through explicit rollover logic;
4. retain historical contract identity;
5. avoid rewriting prior contract-specific indicators.

---

## 5. Source Payload

A live Massive minute-aggregate event has the following structure:

```json
{
  "c": "7595.25",
  "dv": "334184.25",
  "e": 1783932180000,
  "ev": "AM",
  "h": "7595.5",
  "l": "7594.75",
  "n": 27,
  "o": "7595.5",
  "s": 1783932120000,
  "sym": "MESU6",
  "v": 44
}
```

### 5.1 Field Interpretation

| Field | Meaning |
|---|---|
| `ev` | Provider event type |
| `sym` | Futures contract symbol |
| `s` | Aggregate interval start as Unix epoch milliseconds |
| `e` | Aggregate interval end as Unix epoch milliseconds |
| `o` | Open price |
| `h` | High price |
| `l` | Low price |
| `c` | Close price |
| `v` | Volume |
| `n` | Contributing transaction or event count |
| `dv` | Provider-calculated dollar volume |

### 5.2 Timestamp Behaviour

The provider timestamps are Unix epoch milliseconds.

For a valid minute aggregate:

```text
e - s = 60,000 milliseconds
```

The source timestamps are preserved unchanged and also converted into UTC datetime values.

UTC is the canonical Atlas time basis.

---

## 6. Atlas Streaming Adapter

### 6.1 Runtime

The adapter currently runs locally through:

```text
scripts/run_massive_futures_stream_adapter.py
```

This is the correct development implementation for v1.1.0.

The process must remain running for ingestion to continue.

### 6.2 Responsibilities

The adapter is responsible for:

- loading configuration from environment variables;
- opening the Massive delayed Futures WebSocket;
- authenticating with the Massive API key;
- subscribing to `AM.MESU6`;
- receiving provider status and market-data messages;
- validating the minute-aggregate payload;
- converting provider timestamps to UTC;
- validating the one-minute interval;
- validating OHLC consistency;
- validating non-negative volume and event counts;
- creating the Atlas event envelope;
- preserving the original provider payload;
- publishing the Atlas envelope to Fabric Eventstream;
- logging connection and delivery status;
- shutting down cleanly when interrupted.

### 6.3 Diagnostic Scripts

The following diagnostic scripts remain separate from the operational adapter:

```text
scripts/test_massive_futures_websocket.py
scripts/test_massive_futures_aggregates.py
scripts/test_massive_futures_minute_aggregate_transformer.py
scripts/send_test_atlas_event_to_fabric.py
```

Their separation is deliberate.

The smoke-test and one-event sender utilities should remain simple and usable for troubleshooting independently of the full adapter.

---

## 7. Atlas Event Transformation

The transformation logic is implemented in:

```text
src/common/transformers/
    massive_futures_minute_aggregate_transformer.py
```

The transformer converts a provider event into a governed Atlas envelope.

### 7.1 Atlas Envelope

A transformed event resembles:

```json
{
  "event_type": "AM",
  "symbol": "MESU6",
  "provider_start_epoch_ms": 1783932120000,
  "provider_end_epoch_ms": 1783932180000,
  "event_start_utc": "2026-07-13T08:42:00+00:00",
  "event_end_utc": "2026-07-13T08:43:00+00:00",
  "open_price": "7595.5",
  "high_price": "7595.5",
  "low_price": "7594.75",
  "close_price": "7595.25",
  "volume": 44,
  "event_count": 27,
  "dollar_volume": "334184.25",
  "atlas_received_utc": "2026-07-13T08:53:04.065700+00:00",
  "atlas_source": "massive",
  "atlas_feed": "futures_delayed",
  "atlas_subscription": "AM.MESU6",
  "atlas_schema_version": 1,
  "atlas_event_id": "massive|AM|MESU6|1783932120000",
  "raw_payload": {
    "c": "7595.25",
    "dv": "334184.25",
    "e": 1783932180000,
    "ev": "AM",
    "h": "7595.5",
    "l": "7594.75",
    "n": 27,
    "o": "7595.5",
    "s": 1783932120000,
    "sym": "MESU6",
    "v": 44
  }
}
```

### 7.2 Financial Values

Price and dollar-volume values are retained as strings in the JSON envelope.

This preserves the exact decimal source representation during transport.

They are mapped into KQL `decimal` columns during ingestion.

### 7.3 Event Identifier

The initial deterministic event identifier is:

```text
massive|<event_type>|<symbol>|<provider_start_epoch_ms>
```

Example:

```text
massive|AM|MESU6|1783932120000
```

This provides a stable validation key for the current one-contract, one-minute scope.

It should not yet be described as a complete production duplicate or correction-handling strategy.

### 7.4 Schema Version

The current Atlas streaming envelope version is:

```text
atlas_schema_version = 1
```

Future incompatible envelope changes must introduce an explicit schema-version decision and corresponding documentation.

---

## 8. Fabric Eventstream

### 8.1 Eventstream Item

The Eventstream is:

```text
es_atlas_massive_futures_dev
```

### 8.2 Custom Endpoint Source

The custom endpoint source is:

```text
src_atlas_massive_futures
```

It exposes an Event Hubs-compatible endpoint.

The Python adapter publishes through the Azure Event Hubs client library:

```text
azure-eventhub
```

### 8.3 Authentication

The current development implementation uses SAS-key authentication.

The following values are stored only in the local `.env` file:

```text
FABRIC_EVENTSTREAM_CONNECTION_STRING
FABRIC_EVENTSTREAM_EVENT_HUB_NAME
```

Safe placeholders are included in:

```text
.env.example
```

Credentials must never be committed.

### 8.4 Eventstream Processing Mode

The initial implementation uses:

```text
Direct ingestion
```

No Eventstream transformation operator is currently applied.

This is deliberate because the Python transformer already produces the governed Atlas envelope.

Future streaming transformations should use separate processing paths or destinations rather than weakening the fidelity of the raw route.

### 8.5 Schema Association

Eventstream schema association is not activated.

This is a deliberate v1.1.0 decision because:

- the feature remains a preview capability;
- Atlas already performs payload validation in Python;
- the KQL table and ingestion mapping define the current persisted contract;
- introducing Fabric schema-registry governance would add premature complexity.

Schema registry and formal event-schema governance remain future considerations.

---

## 9. Eventhouse and KQL Database

### 9.1 Eventhouse

The Eventhouse is:

```text
eh_atlas_realtime_dev
```

### 9.2 KQL Database

Fabric created the default KQL database with the same name:

```text
eh_atlas_realtime_dev
```

This default behaviour has been retained.

A second database was not created because the initial vertical slice requires only one KQL database.

### 9.3 Eventhouse Destination

The Eventstream destination is:

```text
dest_atlas_massive_futures_raw
```

It uses direct ingestion into the existing raw table.

---

## 10. Raw KQL Table

The raw table is:

```text
raw_massive_futures_minute_aggregates
```

### 10.1 Grain

The intended grain is:

```text
one row per provider
+ event type
+ futures contract
+ aggregate interval start
```

Within the current scope this is effectively:

```text
one row per MESU6 completed minute aggregate
```

### 10.2 Table Schema

```kusto
.create table raw_massive_futures_minute_aggregates
(
    event_type: string,
    symbol: string,
    provider_start_epoch_ms: long,
    provider_end_epoch_ms: long,
    event_start_utc: datetime,
    event_end_utc: datetime,
    open_price: decimal,
    high_price: decimal,
    low_price: decimal,
    close_price: decimal,
    volume: long,
    event_count: long,
    dollar_volume: decimal,
    atlas_received_utc: datetime,
    atlas_source: string,
    atlas_feed: string,
    atlas_subscription: string,
    atlas_schema_version: int,
    atlas_event_id: string,
    raw_payload: dynamic
)
```

### 10.3 Timestamp Responsibilities

The table preserves three timing stages:

```text
event_end_utc
    Provider aggregate interval completion

atlas_received_utc
    Arrival at the Atlas Python adapter

ingestion_time()
    Arrival in Eventhouse
```

The built-in KQL function:

```kusto
ingestion_time()
```

is preferred over a client-supplied ingestion timestamp.

---

## 11. JSON Ingestion Mapping

The explicit ingestion mapping is:

```text
raw_massive_futures_minute_aggregates_json_mapping
```

An explicit mapping was necessary because automatic inference attempted to:

- add duplicate `_1` columns;
- infer epoch values as datetimes;
- infer financial values as `real`;
- alter the deliberately created KQL schema.

The explicit mapping preserves:

- epoch fields as `long`;
- UTC fields as `datetime`;
- prices as `decimal`;
- volume and event counts as `long`;
- raw payload as `dynamic`.

The mapping is:

```kusto
.create-or-alter table raw_massive_futures_minute_aggregates ingestion json mapping
"raw_massive_futures_minute_aggregates_json_mapping"
'['
'{"column":"event_type","Properties":{"Path":"$.event_type"}},'
'{"column":"symbol","Properties":{"Path":"$.symbol"}},'
'{"column":"provider_start_epoch_ms","Properties":{"Path":"$.provider_start_epoch_ms"}},'
'{"column":"provider_end_epoch_ms","Properties":{"Path":"$.provider_end_epoch_ms"}},'
'{"column":"event_start_utc","Properties":{"Path":"$.event_start_utc"}},'
'{"column":"event_end_utc","Properties":{"Path":"$.event_end_utc"}},'
'{"column":"open_price","Properties":{"Path":"$.open_price"}},'
'{"column":"high_price","Properties":{"Path":"$.high_price"}},'
'{"column":"low_price","Properties":{"Path":"$.low_price"}},'
'{"column":"close_price","Properties":{"Path":"$.close_price"}},'
'{"column":"volume","Properties":{"Path":"$.volume"}},'
'{"column":"event_count","Properties":{"Path":"$.event_count"}},'
'{"column":"dollar_volume","Properties":{"Path":"$.dollar_volume"}},'
'{"column":"atlas_received_utc","Properties":{"Path":"$.atlas_received_utc"}},'
'{"column":"atlas_source","Properties":{"Path":"$.atlas_source"}},'
'{"column":"atlas_feed","Properties":{"Path":"$.atlas_feed"}},'
'{"column":"atlas_subscription","Properties":{"Path":"$.atlas_subscription"}},'
'{"column":"atlas_schema_version","Properties":{"Path":"$.atlas_schema_version"}},'
'{"column":"atlas_event_id","Properties":{"Path":"$.atlas_event_id"}},'
'{"column":"raw_payload","Properties":{"Path":"$.raw_payload"}}'
']'
```

---

## 12. Validation

The implementation was validated using several KQL checks.

### 12.1 Latest Events

```kusto
raw_massive_futures_minute_aggregates
| extend fabric_ingested_utc = ingestion_time()
| order by fabric_ingested_utc desc
| take 20
```

This confirms:

- recent rows are arriving;
- schema fields are populated;
- Eventhouse ingestion is active.

### 12.2 Duplicate Event IDs

```kusto
raw_massive_futures_minute_aggregates
| summarize row_count = count() by atlas_event_id
| where row_count > 1
| order by row_count desc
```

Observed result:

```text
No duplicate live event IDs
```

A deliberately replayed static diagnostic event is excluded from some validation queries.

### 12.3 Minute Continuity

```kusto
raw_massive_futures_minute_aggregates
| where atlas_event_id != "massive|AM|MESU6|1783932120000"
| order by event_start_utc asc
| serialize
| extend previous_event_start_utc = prev(event_start_utc)
| extend gap_seconds = datetime_diff(
    "second",
    event_start_utc,
    previous_event_start_utc
)
| project
    event_start_utc,
    previous_event_start_utc,
    gap_seconds,
    atlas_event_id
```

Observed result:

- `60` seconds between consecutive rows while the local adapter was running;
- larger gaps corresponded to periods when the adapter was not running.

No gap was attributed to Fabric when the adapter was continuously active.

### 12.4 OHLC and Non-Negative Measures

```kusto
raw_massive_futures_minute_aggregates
| where
    high_price < open_price
    or high_price < close_price
    or high_price < low_price
    or low_price > open_price
    or low_price > close_price
    or volume < 0
    or event_count < 0
    or dollar_volume < 0
| project
    event_start_utc,
    symbol,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    event_count,
    dollar_volume,
    atlas_event_id
```

Observed result:

```text
No invalid rows
```

### 12.5 Latency Profile

```kusto
raw_massive_futures_minute_aggregates
| extend fabric_ingested_utc = ingestion_time()
| extend
    feed_delay_seconds = datetime_diff(
        "millisecond",
        atlas_received_utc,
        event_end_utc
    ) / 1000.0,
    fabric_ingestion_seconds = datetime_diff(
        "millisecond",
        fabric_ingested_utc,
        atlas_received_utc
    ) / 1000.0,
    end_to_end_seconds = datetime_diff(
        "millisecond",
        fabric_ingested_utc,
        event_end_utc
    ) / 1000.0
| where atlas_event_id != "massive|AM|MESU6|1783932120000"
| summarize
    event_count = count(),
    average_feed_delay_seconds = avg(feed_delay_seconds),
    minimum_feed_delay_seconds = min(feed_delay_seconds),
    maximum_feed_delay_seconds = max(feed_delay_seconds),
    average_fabric_ingestion_seconds = avg(fabric_ingestion_seconds),
    minimum_fabric_ingestion_seconds = min(fabric_ingestion_seconds),
    maximum_fabric_ingestion_seconds = max(fabric_ingestion_seconds),
    average_end_to_end_seconds = avg(end_to_end_seconds)
    by symbol
```

Observed results from the initial live sample:

```text
Event count:                         7

Average provider delay:             603.910 seconds
Minimum provider delay:             603.901 seconds
Maximum provider delay:             603.922 seconds

Average Fabric ingestion latency:     0.473 seconds
Minimum Fabric ingestion latency:     0.106 seconds
Maximum Fabric ingestion latency:     1.637 seconds

Average end-to-end latency:         604.383 seconds
```

These results show that the total delay is dominated by the provider subscription delay.

Atlas and Fabric added less than half a second on average in the initial sample.

---

## 13. KQL Queryset

The default KQL queryset is:

```text
eh_atlas_realtime_dev_queryset
```

Named tabs currently include:

```text
Massive Futures Streaming Validation
Massive Futures Market Monitoring
Massive Futures Dashboard Source
```

### 13.1 Streaming Validation

Contains reusable checks for:

- latest events;
- duplicate event IDs;
- continuity;
- OHLC validity;
- latency.

### 13.2 Market Monitoring

Provides an operational view of recent market events and ingestion latency.

It is intended to answer:

- Is data arriving?
- What is the latest bar?
- Is the provider delay stable?
- Is Fabric ingestion latency acceptable?

### 13.3 Dashboard Source

Returns a simplified result set for dashboard visuals:

- event timestamp;
- symbol;
- OHLC;
- volume;
- event count.

Operational metadata is deliberately excluded unless required by a visual.

---

## 14. Real-Time Dashboard

The Real-Time Dashboard is:

```text
rtd_atlas_massive_futures_dev
```

The initial dashboard contains:

### Recent MESU6 Minute Aggregates

A table showing:

- event start;
- symbol;
- open;
- high;
- low;
- close;
- volume;
- event count.

### MESU6 Close Price — Delayed Minute Aggregates

A line chart using:

```text
X axis: event_start_utc
Y axis: close_price
Series: symbol
```

### MESU6 Volume — Delayed Minute Aggregates

A column chart using:

```text
X axis: event_start_utc
Y axis: volume
Series: symbol
```

The dashboard uses a wider temporary time filter during development so the small captured sample remains visible.

Future continuous sessions can use shorter operational windows.

---

## 15. Current Hosting Model

The Python adapter currently runs locally.

```text
Developer workstation
        |
        v
run_massive_futures_stream_adapter.py
        |
        v
Fabric Eventstream
```

This is appropriate for the current development and trial-capacity phase.

### 15.1 Current Limitation

Ingestion stops when:

- the terminal process stops;
- the workstation sleeps;
- the workstation shuts down;
- the local internet connection fails.

The current adapter should therefore not be described as a production-hosted service.

### 15.2 Future Hosting Direction

A future production-style implementation would retain the same logical architecture but host the adapter as an always-running cloud worker.

A likely future option is:

```text
Azure Container Apps
        |
        v
Atlas streaming adapter
        |
        v
Fabric Eventstream
```

A continuously running worker is a better fit than a standard event-triggered Azure Function because the adapter owns a persistent outbound WebSocket connection.

Production hosting is deferred until a much later release.

---

## 16. Security and Configuration

The local `.env` file contains:

```text
MASSIVE_API_KEY
MASSIVE_FUTURES_TICKER
FABRIC_EVENTSTREAM_CONNECTION_STRING
FABRIC_EVENTSTREAM_EVENT_HUB_NAME
```

The `.env` file is excluded from Git.

The `.env.example` file contains only safe placeholders.

No Massive credentials, SAS keys, connection strings, or provider secrets may be committed.

Future production-style hosting should consider:

- Azure Key Vault;
- managed identity where supported;
- secret rotation;
- least-privilege access;
- formal environment configuration.

---

## 17. Operational Characteristics

### 17.1 Delivery Semantics

The current implementation sends each received Atlas event directly to Eventstream.

It does not yet implement:

- persistent local buffering;
- guaranteed replay;
- dead-letter handling;
- automatic resend after process failure;
- idempotent destination enforcement;
- exactly-once processing.

The implementation should therefore be considered an initial at-least-attempted delivery pattern rather than a production-guaranteed delivery system.

### 17.2 Reconnection

The WebSocket client includes connection health settings and clean shutdown behaviour.

More advanced reconnect handling remains future work, including:

- exponential backoff;
- maximum retry policies;
- connection-state metrics;
- subscription restoration;
- replay after disconnect;
- escalation after repeated failures.

### 17.3 Multiple Instances

The current design assumes one running adapter instance.

Multiple simultaneous instances subscribing to the same symbol could generate duplicate events unless coordination or deduplication is introduced.

A future hosted implementation should initially use one active replica.

---

## 18. Design Decisions

The implementation follows these principles.

### 18.1 Preserve Provider Fidelity

The raw provider payload is retained in:

```text
raw_payload
```

### 18.2 Use UTC Canonically

All derived timestamps are stored as UTC.

### 18.3 Separate Provider Logic from Fabric Delivery

Provider WebSocket logic, transformation, and Eventstream writing remain separate responsibilities.

### 18.4 Avoid Automatic Schema Drift

The KQL table and explicit ingestion mapping are governed deliberately.

Fabric-generated duplicate columns were not accepted.

### 18.5 Keep Raw Ingestion Simple

The initial route uses direct ingestion without Eventstream transformations.

### 18.6 Distinguish Development from Production

Local hosting is documented honestly as a development implementation.

### 18.7 Build Incrementally

The release proves one event type and one instrument before expanding scope.

---

## 19. Future Evolution

Potential future enhancements include:

- configurable instrument subscriptions;
- simultaneous current and next contract ingestion;
- automated futures rollover;
- resilient WebSocket reconnection;
- durable buffering;
- duplicate and correction handling;
- schema registry;
- Eventstream processing operators;
- streaming Silver models;
- streaming OHLC and indicator calculations;
- real-time alerts;
- Fabric Activator;
- cloud hosting;
- managed secrets;
- deployment automation;
- historical and streaming reconciliation;
- unified instrument dimensions;
- operational monitoring dashboards;
- capacity and cost monitoring.

These should be introduced through later releases and, where significant, corresponding Architecture Decision Records.

---

## 20. Implemented Asset Summary

### Local Python

```text
scripts/test_massive_futures_websocket.py
scripts/test_massive_futures_aggregates.py
scripts/test_massive_futures_minute_aggregate_transformer.py
scripts/send_test_atlas_event_to_fabric.py
scripts/run_massive_futures_stream_adapter.py
```

### Transformer

```text
src/common/transformers/
    massive_futures_minute_aggregate_transformer.py
```

### Writer

```text
src/common/writers/
    FabricEventstreamWriter.py
```

### Fabric

```text
Eventstream:
es_atlas_massive_futures_dev

Custom endpoint source:
src_atlas_massive_futures

Eventhouse destination:
dest_atlas_massive_futures_raw

Eventhouse:
eh_atlas_realtime_dev

KQL database:
eh_atlas_realtime_dev

Raw table:
raw_massive_futures_minute_aggregates

JSON ingestion mapping:
raw_massive_futures_minute_aggregates_json_mapping

KQL queryset:
eh_atlas_realtime_dev_queryset

Real-Time Dashboard:
rtd_atlas_massive_futures_dev
```

---

## 21. Current Status

The initial near-real-time vertical slice is successfully implemented and validated.

Confirmed capabilities include:

- live Massive WebSocket connection;
- authentication;
- `AM.MESU6` subscription;
- minute-aggregate payload receipt;
- Atlas event transformation;
- Fabric Eventstream publication;
- Eventhouse ingestion;
- governed KQL schema;
- raw-payload preservation;
- duplicate validation;
- continuity validation;
- OHLC validation;
- latency analysis;
- basic Real-Time Dashboard visualisation.

The implemented architecture should be described as:

> A development-hosted, near-real-time futures market-data pathway that uses a local Atlas Python streaming adapter to ingest Massive delayed minute aggregates through Microsoft Fabric Eventstream into Eventhouse for KQL validation and Real-Time Dashboard visualisation.

It should not yet be described as a production-hosted or resilient streaming platform.