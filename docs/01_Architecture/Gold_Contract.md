# Atlas Gold Layer Contract

## Release

v0.8.0 — AI Trading Intelligence Foundation

## Purpose

The Gold layer provides business-ready analytical structures derived from validated Silver market events.

The Gold layer provides business-ready analytical structures derived from validated Silver market events.

Gold now consists of two logical analytical tiers:

- Gold Analytics
- Gold AI Intelligence

Gold Analytics produces deterministic market structures suitable for reporting.

Gold AI Intelligence derives reproducible market intelligence and AI-ready prompt templates from trusted Gold analytical data.

The Gold layer does not generate trading signals, forecasts or Large Language Model (LLM) responses.

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

### gold_ai_session_summary

AI-ready trading session summaries generated from Gold analytical tables.

Fields:

* Instrument
* TradingDate
* Open
* High
* Low
* Close
* TotalTrades
* SessionHigh
* SessionLow
* SessionTradeCount
* MostActiveMinute
* MostActiveMinuteTradeCount
* DailyRange
* DailyMovement
* DailyRangePct
* DailyReturnPct
* PriceDirection
* SessionDirection
* VolatilityBand
* ActivityBand
* SessionCharacter
* PromptVersion
* PromptTemplate

This table is deterministic and reproducible.

PromptTemplate is an AI-ready prompt constructed from validated market analytics.

No Large Language Model inference is performed within the Gold layer.

## Design Principles

The Gold layer must be:

* analytical
* reproducible
* deterministic
* AI-ready
* deterministic prompt generation
* derived only from trusted Silver data
* suitable for Power BI reporting
* free from strategy or signal logic

## Exclusions

The following are explicitly out of scope for v0.8.0:

* trading indicators
* buy/sell signals
* backtesting
* predictive modelling
* AI-generated trading advice
* LLM inference within the Gold layer
* real-time streaming
* profit and loss calculations

## Success Criteria

v0.8.0 is complete when:

1. Gold analytical tables are documented.
2. AI session summaries are generated from Gold analytical data.
3. Session classifications are deterministic and reproducible.
4. AI prompt templates are generated without LLM inference.
5. Gold AI session summaries are written to Delta.
6. The Semantic Model can consume AI-ready Gold tables.
