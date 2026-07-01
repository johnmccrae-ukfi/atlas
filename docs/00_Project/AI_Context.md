# AI Context

## Project

Atlas is an enterprise AI Trading Intelligence Platform developed by UK Future Innovations.

The MVP ingests delayed intraday market data, processes it through a Microsoft Fabric medallion architecture, generates transparent trading signals, and presents insights through Power BI.

---

## Core Architecture

Atlas uses:

- Microsoft Fabric as the core data platform.
- Medallion Architecture: Bronze, Silver, Gold.
- GitHub-first engineering.
- AI-assisted development.
- Certified Semantic Models for KPI consistency.
- Market Data Abstraction Layer to avoid vendor lock-in.

---

## Medallion Principles

Bronze preserves reality.

Silver standardises reality.

Gold generates business intelligence.

Bronze contains raw provider data with minimal transformation.

Silver maps provider-specific data into Atlas canonical models.

Gold contains curated analytics, KPIs, trading signals and business-ready structures.

---

## Market Data Rules

All external market data providers must map into Atlas common domain models.

Provider-specific formats must not leak into downstream processing.

The first canonical market model is `MarketBar`.

`MarketBar` represents one OHLCV candle after provider normalisation.

Expected fields:

- instrument
- timestamp
- open
- high
- low
- close
- volume
- provider

---

## Python Engineering Standards

Use:

- Python type hints
- Dataclasses where appropriate
- Clear docstrings
- Small focused classes
- Provider abstraction
- Explicit validation
- Readable code over clever code

Avoid:

- Provider-specific logic in shared models
- Hard-coded secrets
- Unclear abbreviations
- Over-engineering
- Hidden business rules

---

## Validation Rules for MarketBar

A valid MarketBar must have:

- instrument populated
- provider populated
- timestamp populated and timezone-aware
- high greater than or equal to low
- open between low and high
- close between low and high
- prices greater than or equal to zero
- volume greater than or equal to zero when supplied

---

## AI Assistant Instructions

When generating code for Atlas:

- Follow the documented architecture.
- Respect ADR decisions.
- Keep provider-specific logic inside provider adapters.
- Keep common domain models provider-independent.
- Prefer clarity over cleverness.
- Include type hints and docstrings.
- Explain non-obvious decisions.
- Do not introduce new frameworks without justification.
- Do not bypass the Market Data Abstraction Layer.