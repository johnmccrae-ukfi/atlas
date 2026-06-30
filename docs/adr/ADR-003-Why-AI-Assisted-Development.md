# ADR-003: Why AI-Assisted Development?

## Status

Accepted

## Date

2026-06-30

---

## Context

Atlas is an ambitious product that combines Data Engineering, Analytics Engineering, Artificial Intelligence and enterprise software engineering.

Traditional software development alone would significantly increase development time and reduce the opportunity to explore innovative product ideas.

Modern AI development tools have matured sufficiently to become valuable engineering assistants when used within an appropriate governance framework.

Atlas therefore requires a defined approach to incorporating AI into the software engineering lifecycle.

---

## Decision

Atlas will adopt an **AI-Assisted Development** methodology.

Artificial Intelligence will augment—not replace—human engineering decisions.

Final responsibility for architecture, design, implementation, testing and deployment remains with the project owner.

---

## Objectives

The AI-assisted methodology aims to:

- Increase engineering productivity.
- Improve documentation quality.
- Accelerate learning.
- Reduce repetitive coding tasks.
- Improve architectural consistency.
- Encourage independent review.
- Maintain full human ownership of technical decisions.

---

## AI Team Structure

Atlas treats AI tools as specialist members of a virtual engineering team.

### ChatGPT

Primary responsibilities:

- Product planning
- Solution architecture
- Technical leadership
- Documentation
- Architecture Decision Records
- Project governance
- Design reviews
- Technical mentoring

---

### GitHub Copilot

Primary responsibilities:

- Code completion
- Boilerplate generation
- Unit test generation
- Refactoring suggestions
- IDE productivity

---

### Claude

Primary responsibilities:

- Independent code review
- Alternative implementations
- Large-context analysis
- Technical critique
- Quality assurance

---

### Human Engineer

Responsibilities remain with the project owner:

- Product vision
- Business requirements
- Architecture approval
- Technology selection
- Code review
- Testing
- Security
- Deployment
- Commercial decisions

---

## Development Workflow

Atlas follows a structured AI-assisted workflow.

```text
Business Requirement

        │

        ▼

Architecture & Design

(ChatGPT)

        │

        ▼

Implementation

(Human + Copilot)

        │

        ▼

Independent Review

(Claude where appropriate)

        │

        ▼

Human Approval

        │

        ▼

Git Commit

        │

        ▼

Release
```

AI contributes throughout the lifecycle but never bypasses human approval.

---

## Guiding Principles

### AI assists.

Humans decide.

---

### Architecture before implementation.

Design decisions should be understood before code is generated.

---

### Prompt engineering is engineering.

Well-designed prompts improve quality, repeatability and productivity.

---

### AI output is reviewed.

Generated code should never be accepted without human review.

---

### Documentation is generated alongside software.

Documentation is considered part of the product.

---

### Learning takes priority over automation.

AI should increase understanding rather than encourage blind acceptance of generated code.

---

## Benefits

### Productivity

Reduce repetitive engineering effort.

---

### Documentation

Maintain consultancy-quality documentation throughout development.

---

### Knowledge Transfer

Provide continuous explanation of unfamiliar technologies.

---

### Quality

Independent AI reviews reduce implementation bias.

---

### Learning

Accelerate adoption of Python, PySpark, AI engineering and emerging technologies.

---

### Innovation

Allow more engineering time to be spent solving business problems rather than repetitive coding tasks.

---

## Risks

| Risk | Mitigation |
|-------|------------|
| Incorrect AI output | Human review before commit. |
| Over-reliance on AI | Understand code before accepting it. |
| Reduced engineering knowledge | Treat AI as a mentor rather than an answer engine. |
| Inconsistent AI responses | Maintain documented architecture and engineering standards. |
| Security risks | Never expose secrets or sensitive data in prompts. |

---

## Alternatives Considered

### Traditional Development Only

Rejected because:

- Lower productivity.
- Slower documentation.
- Reduced opportunity for rapid experimentation.
- Less effective use of modern engineering tools.

---

### AI-Generated Development Only

Rejected because:

- Loss of architectural control.
- Increased technical risk.
- Reduced understanding.
- Lower code quality.
- Unsuitable for consultancy-grade delivery.

---

## Consequences

### Positive

- Faster development.
- Better documentation.
- Better architectural consistency.
- Stronger learning outcomes.
- Reusable engineering methodology.
- Supports rapid MVP development.

### Negative

- Requires prompt engineering skills.
- AI output quality varies.
- Human review remains essential.
- Development process becomes dependent on AI availability.

---

## Relationship to Previous ADRs

ADR-001 selected Microsoft Fabric as the strategic platform.

ADR-002 selected the Medallion Architecture.

ADR-003 defines **how Atlas itself will be engineered.**

Together these decisions establish both the technical architecture and the engineering methodology.

---

## Future Evolution

As AI tooling evolves, Atlas may incorporate:

- Automated documentation generation.
- AI-assisted testing.
- AI-assisted code review.
- AI-generated release notes.
- Multi-agent engineering workflows.
- Domain-specific engineering agents.

These capabilities should enhance, rather than replace, human engineering judgement.

---

## Decision Summary

Atlas will adopt an AI-Assisted Development methodology because it provides the best balance between engineering productivity, software quality, learning and architectural control.

AI is considered a trusted engineering assistant, not an autonomous software engineer.

Human ownership of the product remains fundamental to the UKFI engineering philosophy.