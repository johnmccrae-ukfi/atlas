# ADR-001: Why Microsoft Fabric?

## Status

Accepted

## Date

2026-06-30

## Context

Atlas requires an enterprise-grade data and AI platform capable of supporting ingestion, storage, transformation, analytics, reporting, governance and future intelligence features.

The platform must demonstrate skills relevant to modern Data Engineering, Analytics Engineering, AI Engineering and consultancy delivery.

The MVP requires a solution that can support:

- Market data ingestion
- Medallion architecture
- Lakehouse and warehouse patterns
- SQL-based analytics
- Notebook-based processing
- Power BI reporting
- Future real-time analytics
- Future AI and agentic capability
- GitHub-based engineering practices

## Decision

Atlas will use **Microsoft Fabric** as the core data and analytics platform.

Fabric will be the primary platform for:

- Lakehouse storage
- Data pipelines
- Data transformation
- Warehouse modelling
- Semantic modelling
- Power BI analytics
- Real-Time Intelligence where appropriate
- Integration with Microsoft Data & AI services

Azure AI, Azure OpenAI and AI Foundry may be added where they provide clear product value.

## Rationale

Microsoft Fabric is the preferred platform because it provides an integrated Microsoft Data & AI ecosystem covering data engineering, data warehousing, real-time analytics, business intelligence and AI-assisted analytics.

It allows Atlas to demonstrate an end-to-end enterprise architecture using technologies currently in demand for Microsoft data roles and consultancy engagements.

Fabric is particularly suitable because it supports:

- **Unified analytics:** Data engineering, data warehousing, data science, real-time analytics and Power BI in one platform.
- **Medallion architecture:** Bronze, Silver and Gold data layers can be implemented naturally using Lakehouse, Warehouse and notebooks.
- **Power BI integration:** Reporting and semantic modelling are first-class capabilities rather than separate bolt-ons.
- **SQL and Python workflows:** The platform supports John’s existing SQL strengths while extending into Python, PySpark and notebooks.
- **Enterprise relevance:** Fabric is increasingly relevant to data engineering, analytics engineering and AI consulting roles.
- **Scalability:** The architecture can start small for MVP development and scale later if the product becomes commercially viable.
- **Future AI integration:** Fabric can integrate with Azure AI, Azure OpenAI, AI Foundry and Copilot-style capabilities.
- **Portfolio value:** A well-engineered Fabric solution directly supports the professional objective of securing senior data and AI contract work.
- **Reusable platform thinking:** The same architectural pattern can later support healthcare, creative AI and other UKFI products.

## Alternatives Considered

### Azure Synapse Analytics

Azure Synapse provides strong analytics and data warehousing capability, but Fabric is now the more strategic Microsoft platform for integrated data engineering, analytics and Power BI-led solutions.

Synapse may still be relevant in enterprise environments, but Fabric better supports the product and portfolio goals of Atlas.

### Databricks

Databricks is a powerful data engineering and lakehouse platform, especially for Spark-based workloads.

However, Atlas is intentionally aligned with the Microsoft ecosystem, Power BI, Fabric, Azure AI and the contract market currently being targeted.

Databricks may be considered in future if a specific workload or client requirement justifies it.

### Standalone Azure SQL / SQL Server

Azure SQL and SQL Server are excellent relational platforms and may still be used where appropriate.

However, they do not provide the full integrated lakehouse, warehouse, notebook, pipeline, real-time analytics and Power BI ecosystem required for Atlas.

### Custom Python Application Only

A custom Python-based platform would provide flexibility, but it would require significantly more infrastructure, governance, deployment and reporting work.

It would also demonstrate fewer Microsoft Fabric-specific skills, reducing the portfolio and consultancy value of the project.

## Consequences

### Positive Consequences

- Atlas can demonstrate a complete Microsoft Data & AI solution.
- The architecture aligns strongly with current Microsoft Fabric contract opportunities.
- Power BI reporting can be integrated naturally.
- The project can start with a manageable MVP and scale over time.
- The same architecture can be reused for future UKFI products.
- Documentation and delivery can be aligned with enterprise consultancy practice.

### Negative Consequences

- Fabric capabilities are evolving rapidly, so features may change during development.
- Some Fabric functionality may require paid capacity or trial limitations.
- GitHub and CI/CD integration may require additional setup and discipline.
- Some advanced functionality may still require Azure services outside Fabric.
- The project becomes partly dependent on Microsoft platform direction.

## Mitigations

- Keep the architecture modular so components can be replaced if required.
- Avoid unnecessary lock-in where simple open formats or standard patterns are sufficient.
- Use small datasets during MVP development to control cost.
- Record major decisions in ADRs.
- Keep proprietary trading logic separate from public documentation where required.
- Use GitHub as the engineering source of truth rather than relying solely on portal configuration.

## Decision Summary

Microsoft Fabric is selected as the core platform for Atlas because it best supports the combined goals of enterprise-grade data engineering, analytics, AI integration, professional portfolio value and reusable UKFI product architecture.