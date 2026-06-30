# ADR-004: Why GitHub-First Engineering?

## Status

Accepted

## Date

2026-06-30

---

## Context

Modern software development requires a reliable system for managing source code, documentation, architecture, collaboration and release history.

Atlas is intended to demonstrate consultancy-quality engineering while simultaneously forming the foundation of a future commercial software product.

To achieve this, all project artefacts must be managed using a consistent engineering workflow.

---

## Decision

Atlas will adopt a **GitHub-First Engineering** methodology.

GitHub will become the single source of truth for:

- Source code
- Documentation
- Architecture
- ADRs
- Release history
- Version control
- Engineering standards

Portal-based development should be avoided where practical unless the platform requires it.

---

## Why GitHub First?

Software should never exist only inside cloud portals.

Every important engineering asset should be version controlled.

GitHub provides:

- Complete history
- Traceability
- Collaboration
- Review
- Repeatability
- Disaster recovery
- Professional engineering practice

The repository becomes the product's engineering record.

---

## Engineering Workflow

```text
Business Requirement

        │

        ▼

Documentation

        │

        ▼

Architecture

        │

        ▼

Implementation

        │

        ▼

Testing

        │

        ▼

Commit

        │

        ▼

Release
```

Every stage should leave evidence inside GitHub.

---

## Repository Principles

The repository should contain:

- Documentation
- Architecture
- Source code
- Infrastructure
- Tests
- Sample data
- Release history

The repository should **not** contain:

- Secrets
- Passwords
- API keys
- Temporary files
- Experimental code
- Large binary datasets
- Personal information

---

## Documentation First

Atlas follows a Documentation First philosophy.

Before implementation begins the project should contain:

- Vision
- PID
- ADRs
- Architecture
- Roadmap
- Release Plan

Implementation then follows an agreed design rather than creating documentation retrospectively.

---

## Branching Strategy

### Initiation Stage

Direct commits to `main` are acceptable while creating the initial project foundation.

No production code exists at this stage.

---

### Development Stage

Once implementation begins:

```text
main

▲

│ Merge

develop

▲

│ Merge

feature/*
```

Feature branches should be used for all new functionality.

---

## Commit Standards

Atlas adopts Conventional Commits.

Examples:

```
feat:
docs:
fix:
refactor:
test:
build:
ci:
chore:
```

Commit messages should describe **why** a change exists rather than simply **what** changed.

---

## Release Philosophy

Releases represent project milestones.

Examples include:

- Foundation
- Architecture Complete
- MVP
- Beta
- Production

Documentation milestones are considered equally important to software milestones.

---

## Benefits

### Traceability

Every engineering decision is recorded.

### Professionalism

The repository demonstrates enterprise engineering practice.

### Learning

The complete engineering journey is preserved.

### Collaboration

Future contributors can understand project history.

### Commercial Value

The repository supports consultancy, portfolio and future product development.

---

## Risks

| Risk | Mitigation |
|-------|------------|
| Poor commit discipline | Adopt Conventional Commits. |
| Documentation drift | Update documentation alongside implementation. |
| Large binary files | Store externally where appropriate. |
| Portal-only changes | Recreate changes in Git where practical. |

---

## Alternatives Considered

### Portal-First Development

Rejected because:

- Limited version control.
- Reduced traceability.
- Difficult collaboration.
- Architecture decisions become disconnected from implementation.

---

### Documentation After Development

Rejected because:

- Lower quality.
- Increased technical debt.
- Harder knowledge transfer.
- Reduced architectural consistency.

---

## Relationship to Previous ADRs

ADR-001 defines the platform.

ADR-002 defines the data architecture.

ADR-003 defines the engineering methodology.

ADR-004 defines where engineering knowledge is managed and preserved.

---

## Future Evolution

Future enhancements may include:

- GitHub Actions
- Automated testing
- CI/CD pipelines
- Release automation
- Security scanning
- Dependency management
- Documentation generation
- AI-assisted pull request review

These capabilities should extend, rather than replace, the GitHub-First philosophy.

---

## Decision Summary

GitHub is adopted as the engineering source of truth because it provides professional software lifecycle management, supports consultancy-quality delivery and preserves the complete engineering history of Atlas.

Every significant engineering artefact should exist within version control.