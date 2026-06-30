# Project Initiation Document

## Project Name

**Atlas**

## Product Description

Atlas is an Enterprise AI Intelligence Platform initially focused on trading and financial market decision support.

The MVP will demonstrate an end-to-end Microsoft Data & AI solution using Microsoft Fabric, Azure AI, Power BI, GitHub and modern software engineering practices.

---

## Project Sponsor

**John McCrae**

## Organisation / Brand

**UKFI / UK Future Innovations**

---

## Vision

To build an enterprise-grade AI-powered intelligence platform that demonstrates modern Microsoft Data & AI engineering while creating the foundation for commercially viable products and consultancy services.

Atlas will begin as an AI Trading Intelligence Platform and may later form part of a broader UKFI product suite covering finance, healthcare, creative AI and other intelligence-led domains.

---

## Project Charter

To build enterprise-grade AI products that demonstrate modern Microsoft Data & AI engineering while solving real business problems and creating reusable commercial assets.

---

## Business Objectives

Atlas has two primary objectives:

1. **Professional Portfolio Objective**

   Demonstrate high-value skills relevant to Microsoft Fabric, Azure AI, Power BI, Data Engineering, Analytics Engineering, DevOps and enterprise architecture.

2. **Commercial Product Objective**

   Create the first product in a potential UKFI suite of AI-driven intelligence platforms, with future commercial, licensing or consultancy opportunities.

---

## Problem Statement

Retail traders, analysts and decision-makers have access to large volumes of financial data, but insight is often fragmented across multiple tools, dashboards, news sources and analysis platforms.

Atlas aims to consolidate market data, analytics, trading signals and AI-generated explanations into a single decision-support platform.

The system will not initially execute trades automatically. It will provide transparent, explainable insight to support human decision-making.

---

## MVP Goal

The MVP will answer one core question:

> Can Atlas ingest market data, process it through a modern medallion architecture, generate basic trading signals, and present meaningful insights through a professional dashboard?

---

## MVP Scope

### In Scope

- GitHub repository and structured documentation
- Project Initiation Document
- Architecture Decision Records
- Microsoft Fabric architecture design
- Market data ingestion
- Bronze, Silver and Gold data layers
- Lakehouse and/or Warehouse implementation
- Data transformation using SQL, notebooks and/or PySpark
- Power BI dashboard
- Basic trading signal logic
- KPI reporting
- Initial release documentation

### Out of Scope for MVP

- Automated live trading
- Payment processing
- User subscriptions
- Mobile application
- Advanced AI agents
- Broker integration
- Regulatory compliance framework
- Production SaaS hosting
- Proprietary trading strategy exposure

---

## Success Criteria

The MVP will be considered successful when:

- Market data can be ingested reliably.
- Data is stored using a medallion architecture.
- Transformed data is available for reporting.
- Trading indicators or rules produce Buy / Hold / Sell style outputs.
- Power BI presents clear KPIs and trend analysis.
- The solution is documented clearly enough for a technical reviewer to understand.
- The GitHub repository demonstrates professional engineering practice.
- The project can be discussed confidently in contract interviews.
- The architecture can support future AI and product expansion.

---

## Key Technologies

- Microsoft Fabric
- Lakehouse
- Warehouse
- Eventhouse / Real-Time Intelligence where appropriate
- Pipelines
- Notebooks
- SQL
- PySpark
- KQL
- Power BI
- DAX
- Power Query
- Azure AI / Azure OpenAI / AI Foundry
- GitHub
- GitHub Actions
- VS Code
- Python
- Markdown documentation

---

## AI-Assisted Development Methodology

Atlas will use AI tools as part of a controlled engineering workflow.

### ChatGPT

Used for:

- Product planning
- Architecture
- Technical decision support
- Documentation
- Design review
- Learning support
- Project governance

### GitHub Copilot

Used for:

- Pair programming
- Boilerplate generation
- Code completion
- Refactoring support
- Test generation

### Claude

Used where appropriate for:

- Independent code review
- Alternative implementation suggestions
- Large-context review
- Quality assurance

Final responsibility for architecture, code quality, testing and delivery remains with the project owner.

---

## Development Principles

1. **Business value before technology**

   Technology is only included where it supports the product goal.

2. **Enterprise quality**

   The solution should be designed as if it were being delivered to a real client.

3. **Simple before clever**

   The MVP should be understandable, maintainable and demonstrable.

4. **Everything important is version controlled**

   Documentation, scripts, configuration and code should be managed in GitHub.

5. **Documentation is part of the product**

   If it is not documented, it is not complete.

6. **Reusable platform thinking**

   Components should be designed with future UKFI products in mind where practical.

---

## Stakeholders

| Stakeholder | Role |
|---|---|
| John McCrae | Product Owner, Solution Architect, Lead Engineer |
| UKFI | Product brand / future commercial owner |
| Recruiters and hiring managers | Portfolio audience |
| Potential clients | Consultancy audience |
| Future customers | Product audience |
| AI tools | Assisted development team |

---

## Initial Product Roadmap

### v0.1.0 — Foundation

- Repository created
- Folder structure created
- PID created
- ADR framework created
- Roadmap started
- Release plan started

### v0.2.0 — Architecture

- Logical architecture
- Physical architecture
- Data architecture
- Security design
- Technology decisions

### v0.3.0 — Data Ingestion

- Market data source selected
- Bronze ingestion pipeline implemented
- Raw data stored

### v0.4.0 — Data Processing

- Silver transformation layer
- Data validation
- Cleansed market dataset

### v0.5.0 — Analytics Model

- Gold layer
- Warehouse / semantic model
- Core KPIs

### v0.6.0 — Dashboard

- Power BI report
- Trading intelligence dashboard
- KPI visuals
- Trend analysis

### v0.7.0 — Trading Signals

- Initial rule-based trading logic
- Buy / Hold / Sell outputs
- Performance tracking

### v1.0.0 — MVP Release

- End-to-end demo
- Documentation complete
- GitHub repository polished
- Portfolio-ready release

---

## Assumptions

- Suitable market data sources will be available through free, delayed or low-cost APIs.
- Microsoft Fabric trial or development capacity will be sufficient for MVP development.
- The MVP will use delayed or historical data rather than live trading execution.
- The project will prioritise demonstrable engineering value over short-term trading profitability.
- Any commercially sensitive strategy logic can be separated into private repositories later.

---

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Market data API limitations | Medium | Start with free/delayed data; abstract ingestion layer |
| Fabric cost or capacity constraints | Medium | Use small datasets and development-scale workloads |
| Scope creep | High | Maintain MVP discipline and roadmap future ideas |
| Overuse of AI-generated code | Medium | Human review required before commit |
| Public exposure of proprietary logic | Medium | Keep sensitive algorithms private |
| Regulatory complexity | High | MVP is decision-support only, not automated trading |
| Too many technologies too early | Medium | Add tools only when required by architecture |

---

## Governance

The project will follow a lightweight consultancy-style governance model.

- Work will be committed to GitHub.
- Significant decisions will be recorded as Architecture Decision Records.
- Releases will use semantic versioning.
- Documentation will be maintained alongside code.
- Main branch should remain stable and presentable.
- Future development work should use feature branches once production code begins.

---

## Definition of Done

A feature or milestone is considered done when:

- It works as intended.
- It is committed to GitHub.
- It is documented.
- It can be explained clearly.
- It supports the project charter.
- It is suitable to demonstrate to a technical reviewer or client.

---

## Initial Status

**Stage:** Initiation and Vision  
**Current Release:** v0.1.0 Foundation  
**Status:** In progress  
**Next Step:** Complete PID, roadmap, release plan and initial ADRs.
