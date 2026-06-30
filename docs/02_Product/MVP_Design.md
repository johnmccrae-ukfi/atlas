# MVP Design

## MVP Objective

Build the smallest end-to-end version of Atlas capable of ingesting delayed intraday market data, transforming it through a Microsoft Fabric medallion architecture, generating a transparent breakout trading signal and presenting actionable insights in Power BI.

The MVP should demonstrate enterprise-grade engineering while remaining simple, explainable and extensible.

---

# MVP Scope

The first release will deliver:

- Scheduled ingestion of delayed market data.
- Microsoft Fabric medallion architecture.
- Power BI trading dashboard.
- Transparent rule-based trading signals.
- GitHub-based engineering workflow.
- Foundation for future AI intelligence.

The MVP intentionally excludes:

- Live broker integration.
- Automated trading.
- Real-time streaming.
- AI-generated recommendations.
- Multi-user authentication.
- Subscription management.

---

# Target Market

The initial MVP will focus on:

**E-mini S&P 500 Futures (ES)**

Reasons:

- Highly liquid.
- Fast-moving.
- Excellent demonstration dataset.
- Widely recognised by traders.
- Suitable for future expansion.

Future versions may support:

- Nasdaq Futures
- Gold Futures
- Crude Oil
- Foreign Exchange
- Individual Equities
- ETFs
- Cryptocurrency

---

# Data Provider Strategy

The preferred MVP data provider is:

**Massive**

Reasons:

- Futures market support.
- Historical and delayed market data.
- REST API suitable for scheduled ingestion.
- WebSocket support provides a future migration path to streaming.
- Consistent API across multiple asset classes.

To minimise vendor lock-in, Atlas will abstract market data behind a provider layer.

```text
Market Data Provider
        │
        ▼
Market Data Adapter
        │
        ▼
Fabric Pipeline
```

Future providers may include:

- Finnhub
- Alpha Vantage
- Twelve Data
- Other compatible market data services

---

# MVP Data Pipeline

```text
Massive REST API
        │
        ▼
Fabric Pipeline (Scheduled)
        │
        ▼
Bronze Lakehouse
        │
        ▼
Silver Lakehouse
        │
        ▼
Gold Warehouse
        │
        ▼
Power BI Dashboard
```

---

# Refresh Strategy

The MVP will use scheduled ingestion.

Initial proposal:

- Pipeline frequency: Every minute.
- Market data: Delayed feed.
- Dashboard refresh aligned with ingestion schedule.

Real-time streaming will be evaluated after MVP completion.

---

# MVP Dashboard

The first Power BI dashboard will include:

- Candlestick chart
- Latest market price
- Session high
- Session low
- Previous swing high
- Previous swing low
- Current trading signal
- Signal history
- Market summary

Future dashboards may include:

- Portfolio analysis
- AI commentary
- Performance statistics
- Watchlists
- Multi-market comparison

---

# MVP Trading Signal

The first algorithm will be known as:

## ABS-1

**Atlas Breakout Signal v1**

Rule:

BUY WATCH

Current Close > Highest High of Previous 20 Candles

SELL WATCH

Current Close < Lowest Low of Previous 20 Candles

Otherwise

HOLD

The objective is not to maximise profitability but to create a simple, transparent and explainable signal suitable for future enhancement.

---

# Future Signal Roadmap

Future releases may introduce:

- Moving averages
- Trend analysis
- Volume confirmation
- RSI
- MACD
- Divergence
- Support and resistance
- AI confidence scoring
- News sentiment
- Economic event analysis

These enhancements should build upon rather than replace the original ABS-1 signal.

---

# MVP Success Criteria

The MVP will be considered successful when it can:

- Retrieve delayed futures market data.
- Load data through the complete medallion architecture.
- Generate the ABS-1 trading signal.
- Display results in Power BI.
- Demonstrate a complete end-to-end engineering workflow.
- Be suitable for portfolio demonstrations and technical interviews.

---

# Out of Scope

The following items are deferred until later releases:

- Eventstream
- Eventhouse
- Streaming analytics
- Live trading
- AI-generated trading recommendations
- Broker connectivity
- Mobile application
- SaaS platform
- Commercial licensing

---

# Summary

The Atlas MVP prioritises simplicity, transparency and architectural quality.

The objective is to demonstrate a complete Microsoft Fabric data platform capable of ingesting market data, producing explainable trading signals and presenting actionable insights.

Future releases will extend this foundation through streaming, AI intelligence and additional financial markets while preserving the architectural principles established during the MVP.