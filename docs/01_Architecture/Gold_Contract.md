# Atlas Gold Layer Contract

## Release

v0.4.0 — Gold Foundation

## Purpose

The Gold layer provides business-ready analytical structures derived from validated Silver market events.

For this release, Gold is focused on OHLC candle generation for reporting and visualization.

This release does not introduce trading signals, strategy logic, forecasting, or AI interpretation.

## Source Layer

Gold tables are derived from the Silver Lakehouse.

Silver is the trusted source for:

* validated market events
* instrument identity
* event timestamps
* trading dates
* event ordering
* provenance
* data quality flags

## Critical Engineering Rule

Open and Close prices must never be calculated using `MIN()` or `MAX()`.

Open and Close must always be derived from preserved event ordering.

* Open = first valid event in the candle window
* Close = last valid event in the candle window
* High = maximum price in the candle window
* Low = minimum price in the candle window

This rule applies to all candle granularities.

## Gold Tables

### gold_cqg_minute_candles

Minute-level OHLC candles generated from Silver market events.

Fields:

* Instrument
* TradingDate
* MinuteTimestamp
* Open
* High
* Low
* Close
* Volume
* TradeCount
* FirstEventSequence
* LastEventSequence
* GoldLoadedUTC

Volume is included as a placeholder where source data does not yet provide reliable volume.

### gold_cqg_daily_candles

Daily OHLC candles generated from minute candles where appropriate.

Fields:

* Instrument
* TradingDate
* Open
* High
* Low
* Close
* TotalTrades
* GoldLoadedUTC

Daily Open and Close must be derived from the first and last minute candles in event order.

## Design Principles

The Gold layer must be:

* analytical
* reproducible
* deterministic
* derived only from trusted Silver data
* suitable for Power BI reporting
* free from strategy or signal logic

## Exclusions

The following are explicitly out of scope for v0.4.0:

* trading indicators
* buy/sell signals
* backtesting
* predictive modelling
* AI commentary
* real-time streaming
* profit and loss calculations

## Success Criteria

v0.4.0 is complete when:

1. The Gold contract is documented.
2. Minute OHLC candles are generated and written to Delta.
3. Daily OHLC candles are generated from minute candles.
4. Open and Close are proven to use event ordering.
5. Power BI can consume Gold tables.
6. A first candlestick visual can be built from the Gold layer.
