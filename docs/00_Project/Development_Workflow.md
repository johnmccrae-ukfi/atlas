# Atlas Development Workflow

## Purpose

This document defines the development workflow for the Atlas Market Data Platform.

Atlas is developed using modern software engineering practices including Git branching, Microsoft Fabric Git integration, CI/CD, and architectural governance.

---

# Repository

Repository:

https://github.com/johnmccrae-ukfi/atlas

Primary technologies:

- Python
- Microsoft Fabric
- OneLake
- PySpark
- Delta Lake
- GitHub
- VS Code

---

# Branch Strategy

## main

The **main** branch represents the stable production-quality codebase.

Changes are **never developed directly** on main.

Only completed features that have been tested and reviewed are merged into main.

---

## dev

The **dev** branch is the active development branch.

All development takes place here, including:

- Python development
- Microsoft Fabric notebooks
- Documentation
- Architecture changes

---

# Development Workflow

## Python Development

VS Code

↓

Checkout **dev**

↓

Develop feature

↓

Commit

↓

Push to GitHub

---

## Microsoft Fabric Development

Fabric Workspace

↓

Connected to **dev**

↓

Develop notebook

↓

Save

↓

Commit & Sync

↓

Push to GitHub

---

# Feature Completion

When a logical milestone is complete:

1. Update documentation
2. Update CHANGELOG.md
3. Commit changes
4. Push to dev
5. Create Pull Request
6. Merge dev into main

---

# Release Workflow

Development

↓

dev branch

↓

Pull Request

↓

main branch

↓

Git Tag

↓

GitHub Release

---

# Versioning

Atlas uses Semantic Versioning.

Examples:

v0.1.0 Foundation

v0.2.0 Bronze Complete

v0.3.0 Silver Complete

v0.4.0 Gold Complete

v1.0.0 MVP Release

---

# Microsoft Fabric

The Atlas Microsoft Fabric workspace is connected directly to the GitHub **dev** branch.

Artifacts committed from Fabric include:

- Lakehouse metadata
- Notebooks
- Pipelines
- Semantic models
- Data Factory assets

Python source code continues to be developed in VS Code.

---

# Architecture Governance

All significant architectural decisions are documented as ADRs.

Major platform changes should update:

- Architecture documentation
- CHANGELOG
- ADRs (where appropriate)

---

# Guiding Principles

Atlas is developed as a production-style enterprise data engineering platform.

Key principles:

- Git-first development
- Documentation-first architecture
- Reproducible data pipelines
- Source data provenance
- Validation at every layer
- Bronze → Silver → Gold medallion architecture
- Microsoft Fabric native implementation
- CI/CD by default