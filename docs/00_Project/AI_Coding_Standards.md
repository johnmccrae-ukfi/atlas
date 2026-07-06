# AI Coding Standards

## Purpose

This document provides coding guidance for AI assistants contributing to Atlas.

It should be used alongside `AI_Context.md`.

---

## Core Principles

- Keep code simple, readable and maintainable.
- Follow the architecture documented in ADRs.
- Do not introduce new frameworks without explicit approval.
- Do not over-engineer for future requirements.
- Prefer small, focused classes.
- Use type hints.
- Use clear docstrings.
- Keep provider-specific logic inside provider adapters.
- Keep common models provider-independent.
- Write tests for domain logic.

---

## Python Standards

- Follow PEP 8 naming conventions.
- Use dataclasses for simple immutable domain models.
- Prefer `datetime` for timestamps after Silver normalisation.
- Prefer explicit validation for domain rules.
- Avoid hidden side effects.
- Avoid hard-coded secrets.
- Keep functions short and focused.

---

## Fabric Notebook Standards

Fabric notebooks should follow a consistent structure:

1. Markdown overview
2. Imports
3. Configuration
4. Read source data
5. Inspect source schema and sample rows
6. Apply transformation logic
7. Validate transformation results
8. Persist output tables
9. Validate persisted output tables

Notebook code should be organised so that each cell has a clear purpose.

Each notebook should clearly document:

- source tables
- target tables
- expected row counts where known
- key business or engineering rules
- validation checks
- release scope

Gold layer notebooks must prove that Open and Close values are derived from event ordering, not from `MIN()` or `MAX()`.

Persisted Delta tables should always be validated after writing by:

- reading the table back from Spark
- checking row counts
- printing the schema
- displaying ordered sample rows

Notebook transformations should prefer deterministic ordering and explicit validation over implicit assumptions.

---

## Testing Standards

- Use Python `unittest` unless another test framework is explicitly added.
- Test domain validation rules.
- Test expected success cases.
- Test expected failure cases.
- Keep tests small and readable.
- Tests should explain business behaviour, not just code behaviour.

---

## Naming Conventions

Interfaces use an `I` prefix (e.g. `IMarketDataProvider`) to distinguish contracts from implementations.

Concrete implementations omit the prefix (e.g. `MassiveProvider`).

---

## Atlas Domain Standards

Bronze preserves raw provider data.

Silver standardises provider data into Atlas canonical models.

Gold creates business-ready analytics and trading intelligence.

`MarketBar` should remain a minimal, canonical Silver-layer OHLCV model.

It should not contain trading signal logic, provider API logic, Power BI logic or Fabric-specific logic.

---

## AI Assistant Rules

When suggesting code:

- Explain the reason for meaningful changes.
- Avoid unnecessary abstractions.
- Do not add future functionality unless requested.
- Do not move business logic into domain models unless explicitly approved.
- Do not make provider-specific assumptions in common models.
- Prefer understandable code over clever code.
- Keep implementation aligned with the current sprint goal.

---

## Repository Operations

- AI agents may implement code.
- The engineer owns repository operations.
- File moves, renames and large refactors should be reviewed carefully.
- On Windows, filename case-only changes may require a two-step rename to remain compatible with Git and Linux CI.