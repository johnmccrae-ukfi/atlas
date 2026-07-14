# Atlas Gold Layer Contract

## Current Contract State

Updated for:

- `v0.8.0 — AI Trading Intelligence Foundation`
- `v1.2.0 — Reporting Navigation and Time Intelligence`

## Purpose

The Gold layer provides business-ready analytical structures derived from validated Silver market events.

Gold currently contains three logical analytical responsibilities:

- Gold market analytics;
- Gold reporting dimensions;
- Gold AI intelligence.

Gold market analytics produces deterministic market structures suitable for semantic modelling and reporting.

Gold reporting dimensions provide governed filtering, sorting and time-intelligence support across analytical tables.

Gold AI intelligence derives reproducible market intelligence and AI-ready prompt templates from trusted Gold analytical data.

The Gold layer does not generate trading signals, forecasts, trading advice or authoritative calculations through Large Language Model inference.

## Source Layer

Gold analytical tables are derived from the trusted Silver Lakehouse layer.

Silver provides:

- validated market events;
- instrument identity;
- event timestamps;
- trading dates;
- deterministic event ordering;
- provenance;
- data-quality classifications.

The Gold date dimension is derived from the governed date coverage of the current Gold candle tables.

## Critical Engineering Rule

Open and Close prices must never be calculated using `MIN()` or `MAX()` against unordered market events.

Open and Close must always be derived from preserved event ordering.

- Open = first valid event in the candle window
- Close = last valid event in the candle window
- High = maximum valid price in the candle window
- Low = minimum valid price in the candle window

This rule applies to all candle granularities.

## Gold Tables

### gold_cqg_minute_candles

Minute-level OHLC candles generated from validated Silver CQG market events.

**Grain:**

One row per:

- `Instrument`
- `MinuteTimestamp`

**Fields:**

- `Instrument`
- `TradingDate`
- `MinuteTimestamp`
- `TradingTime`
- `TradingHour`
- `MinuteOfDay`
- `Open`
- `High`
- `Low`
- `Close`
- `Volume`
- `TradeCount`
- `FirstEventSequence`
- `LastEventSequence`
- `GoldLoadedUTC`

`TradingDate` provides the date-only relationship key used by the reporting semantic model.

`Volume` is currently retained as a placeholder where the source data does not provide a validated volume measure.

Open and Close must be derived from the first and last valid Silver events in preserved event order.

### gold_cqg_daily_candles

Daily OHLC candles generated from persisted Gold minute candles.

**Grain:**

One row per:

- `Instrument`
- `TradingDate`

**Fields:**

- `Instrument`
- `TradingDate`
- `Open`
- `High`
- `Low`
- `Close`
- `TotalTrades`
- `GoldLoadedUTC`

Daily Open and Close must be derived from the first and last minute candles in chronological order.

Daily values must preserve the agreed financial precision:

```text
Decimal(18,5)
```

### gold_dim_date

Governed calendar date dimension used by the historical reporting semantic model.

**Grain:**

One row per calendar date.

**Fields:**

- `Date`
- `Year`
- `QuarterNumber`
- `Quarter`
- `MonthNumber`
- `Month`
- `MonthShort`
- `YearMonth`
- `YearMonthSort`
- `DayOfMonth`
- `DayOfWeekNumber`
- `DayOfWeek`
- `IsWeekend`

The date range is generated dynamically from the minimum and maximum `TradingDate` values found across the current Gold daily and minute candle tables.

The table includes every calendar date in the governed range, including weekends.

`IsTradingDay` is deliberately not inferred from the presence or absence of candle rows. Formal exchange calendars, exchange holidays and instrument-specific trading calendars remain future work.

The table supports:

- Direct Lake semantic-model relationships;
- shared filtering across daily and minute candle tables;
- reusable period calculations;
- previous-trading-date calculations;
- consistent report date formatting;
- chronological month, quarter and weekday sorting;
- future multi-instrument reporting.

### gold_ai_session_summary

Deterministic AI-ready trading-session summaries generated from trusted Gold analytical tables.

**Grain:**

One row per:

- `Instrument`
- `TradingDate`

**Fields:**

- `Instrument`
- `TradingDate`
- `Open`
- `High`
- `Low`
- `Close`
- `TotalTrades`
- `SessionHigh`
- `SessionLow`
- `SessionTradeCount`
- `MostActiveMinute`
- `MostActiveMinuteTradeCount`
- `DailyRange`
- `DailyMovement`
- `DailyRangePct`
- `DailyReturnPct`
- `PriceDirection`
- `SessionDirection`
- `VolatilityBand`
- `ActivityBand`
- `SessionCharacter`
- `PromptVersion`
- `PromptTemplate`

This table is deterministic and reproducible.

`PromptTemplate` is an AI-ready prompt constructed from validated analytical outputs.

No Large Language Model inference is performed within the Gold layer.

## Semantic Model Relationships

The historical reporting semantic model is:

```text
sm_atlas_gold_reporting
```

The semantic model uses Direct Lake against the governed Gold tables.

The date relationships are:

```text
gold_dim_date[Date]
    1 → *
gold_cqg_daily_candles[TradingDate]
```

```text
gold_dim_date[Date]
    1 → *
gold_cqg_minute_candles[TradingDate]
```

Both relationships must be:

- active;
- one-to-many;
- single-direction;
- filtered from `gold_dim_date` to the candle table.

The daily and minute candle tables must not be related directly to one another because they are analytical tables at different grains.

## Semantic Model Measures

Reusable reporting logic should be implemented as explicit semantic-model measures rather than duplicated within individual report visuals.

Current reusable measure areas include:

- selected-period Open;
- selected-period High;
- selected-period Low;
- selected-period Close;
- selected-period Return percentage;
- selected-period Range;
- selected-period Range percentage;
- distinct Trading Days;
- Selected Trading Date;
- Previous Trading Date;
- Selected Trading Day Close;
- Previous Trading Day Close;
- Trading Day Change;
- Trading Day Change percentage;
- five-trading-day moving average;
- total and average trading activity measures.

Trading-day calculations must use dates that exist in the daily candle table rather than assuming that every calendar date is a valid trading date.

The five-day moving-average measure currently retains its proven Daily Candles implementation because the selected candlestick custom visual evaluates the trend measure in a visual-specific context.

## Reporting Behaviour

The reporting semantic model supports:

- shared Date filtering across daily and minute analytical tables;
- continuous calendar date ranges including weekends;
- daily market-overview analysis;
- single-date intraday analysis;
- previous-trading-day comparisons;
- selected-period calculations;
- chronological time attributes;
- reusable report measures.

Selecting a weekend or another date with no market data may legitimately produce blank report visuals. This is expected because `gold_dim_date` represents the full calendar rather than only dates with candle records.

Artificial blank members exposed by Power BI slicers may be excluded using a visual-level `is not blank` filter.

## Drill-Through Evaluation

Daily-to-intraday drill-through was evaluated during `v1.2.0`.

The semantic-model relationships and target-page drill-through configuration were validated successfully using standard Power BI visuals.

The current free candlestick custom visual does not expose a selected candle as compatible Power BI drill-through context.

Drill-through is therefore deferred rather than represented as implemented.

The report retains:

- adjustable date-range analysis on Market Overview;
- single-date selection on Intraday Analysis;
- explicit page-navigation controls between the two report pages.

## Design Principles

The Gold layer must remain:

- analytical;
- deterministic;
- reproducible;
- traceable to trusted source data;
- suitable for Direct Lake semantic modelling;
- suitable for Power BI reporting;
- suitable for controlled AI consumption;
- explicit about analytical grain;
- free from unvalidated trading-strategy logic.

Reporting dimensions must:

- contain stable keys;
- have documented grain;
- support reusable relationships;
- avoid unsupported business assumptions;
- remain reusable across analytical tables.

## Exclusions

The following remain outside the current Gold contract:

- buy or sell signals;
- trading recommendations;
- automated trading execution;
- profit-and-loss calculations;
- strategy backtesting;
- predictive modelling;
- generative AI calculation of authoritative market facts;
- formal exchange-calendar and holiday modelling;
- production streaming Silver and Gold tables;
- historical and streaming reconciliation;
- automatic futures-contract rollover;
- cross-instrument analytical models;
- production deployment and orchestration.

Near-real-time ingestion now exists as a separate Eventstream and Eventhouse pathway introduced in `v1.1.0`.

That near-real-time architecture does not yet populate the historical Lakehouse Gold analytical tables governed by this contract.

## Validation Requirements

### Minute Candles

For every minute candle:

```text
High >= Open
High >= Close
High >= Low
Low <= Open
Low <= Close
TradeCount >= 0
FirstEventSequence <= LastEventSequence
```

Additional validation must confirm:

- one row per Instrument and MinuteTimestamp;
- no unintended duplicate grain keys;
- correct first-event Open;
- correct last-event Close;
- expected decimal precision;
- reconciliation with accepted Silver events.

### Daily Candles

For every daily candle:

```text
High >= Open
High >= Close
High >= Low
Low <= Open
Low <= Close
TotalTrades >= 0
```

Additional validation must confirm:

- one row per Instrument and TradingDate;
- correct first-minute Open;
- correct last-minute Close;
- reconciliation with minute candles;
- expected date coverage;
- expected decimal precision.

### Date Dimension

Validation must confirm:

- one row per Date;
- no null Date values;
- no duplicate Date values;
- continuous calendar coverage;
- minimum Date equals the governed minimum Gold TradingDate;
- maximum Date equals the governed maximum Gold TradingDate;
- weekend classification is correct;
- sort attributes are deterministic.

### Semantic Model

Validation must confirm:

- `gold_dim_date` is on the one side of both relationships;
- both relationships are active;
- both relationships use single-direction filtering;
- no candle `TradingDate` values are null;
- no candle `TradingDate` values fall outside `gold_dim_date`;
- shared Date slicers filter both candle tables correctly;
- measures respond correctly to changing date ranges;
- weekend selections behave predictably;
- report refresh displays the latest semantic-model calculations.

## Success Criteria

This Gold contract is satisfied when:

1. Gold analytical tables have explicit and documented grain.
2. OHLC values preserve deterministic event ordering.
3. Price values retain the agreed financial precision.
4. `gold_dim_date` provides continuous governed calendar coverage.
5. Date relationships filter daily and minute candle tables correctly.
6. Semantic-model measures centralise reusable analytical logic.
7. Selected-period calculations return validated results.
8. Previous-trading-day calculations skip non-trading calendar dates.
9. Report visuals use governed model fields and measures.
10. Gold AI session summaries remain deterministic and reproducible.
11. Generative AI inference remains separated from authoritative Gold calculations.
12. Implemented capabilities and known limitations are represented accurately.