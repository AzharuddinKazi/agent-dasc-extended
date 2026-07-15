# Requirements Discovery Log

**Stage**: Discovery — Stage 0
**Date**: 2026-06-24
**Session**: Initial requirements Q&A
**Participants**: Product & Analytics Team

---

## Summary

This document records the confirmed requirements captured through a structured Q&A session during the discovery phase. These decisions feed directly into the PRD and TDD.

---

## Confirmed Requirements

### 1. Data Sources

**Decision**: All common structured and unstructured file types

The system must handle data from the following categories:

| Data Type | Description | Primary Consumer |
|-----------|-------------|-----------------|
| **Transactional / operational logs** | Order records, activity logs, event exports (structured tabular data) | Operations, Analytics |
| **Customer / account records** | Customer profiles, segmentation data, lifecycle stage, onboarding data | Product, Customer Success |
| **Survey / complaint data** | Free-text feedback, support tickets, satisfaction scores | Customer Success, Product |
| **Market / benchmarking data** | Industry or peer comparison datasets, trend data | Strategy, Research |

Additionally, teams may work with recurring performance datasets as a primary data source:

| Data Type | Description |
|-----------|-------------|
| **Performance reports** | Metric, channel, amount, method, entity_id, reporting_period — submitted periodically by business units |
| **Quality/control assessments** | Qualitative and quantitative assessment data from internal reviews |
| **Industry benchmarking datasets** | Peer comparison data; sector/regional benchmarks |

---

### 2. Deployment Model

**Decision**: Cloud-hosted SaaS

The system is deployed as a standard cloud-hosted service. This keeps the architecture simple, avoids operating dedicated infrastructure, and lets the team iterate quickly without managing hardware.

**Implication**: The LLM inference layer uses a cloud LLM API. The architecture uses a **provider-agnostic adapter** so the LLM backend can be configured without changing any agent code:

```
config.yaml:
  llm_provider: "gemini"           # default
  llm_model_flash: "gemini-2.5-flash"
  llm_model_pro: "gemini-2.5-pro"
```

The system is designed to accept any OpenAI-compatible or Gemini-compatible API endpoint, so switching providers later is a configuration change, not a rewrite.

---

### 3. Target Users

**Decision**: Any team that works with recurring data analysis needs

The primary persona is a **business analyst or operations lead** who understands their domain deeply but cannot write Python or SQL to extract insights from data. The system is designed to serve multiple teams across the organization.

| Team | Role | Representative Queries |
|------|------|----------------------|
| **Operations** ⭐ | Benchmarks performance, monitors trends | "Which regions have the highest return rate vs. peer median?", "Show performance trends by channel over the past 12 months", "Which units are statistical outliers on key metrics?" |
| **Customer Success** | Tracks satisfaction, retention | "Which segments have declining retention rates?", "Show complaint volume by product category", "Which accounts have gaps in onboarding completion?" |
| **Product / Marketing** | Monitors usage, campaign performance, feedback | "Show complaint volumes by product and category", "Which cohorts have materially more churn than peers?", "Identify potential drop-off patterns from usage data" |
| **Finance** | Reviews spend, variance, forecasting | "Pull all revenue data for Region X across the last 3 years", "Generate a summary for quarterly review #XXXX", "Show the historical pattern of Region Y's cost trends" |
| **Strategy & Research** | Develops plans, conducts sector research | "What is the company-wide sales trend by channel (retail, digital, wholesale)?", "Compare regional performance against industry benchmarks", "Generate a thematic report on churn growth across the business" |

**User persona**: Non-technical. The target user can articulate what they want to know but cannot write Python or SQL to extract it. They understand their domain deeply but rely on technical colleagues or manual spreadsheet work for data analysis today.

---

### 4. Output Requirements

**Decision**: Both standalone reports AND a REST API

| Output Type | Description | Use Case |
|-------------|-------------|----------|
| **Standalone reports** | PDF and Excel export, formatted to company reporting standards | Business reviews, leadership briefings, thematic reviews |
| **REST API** | Programmatic query submission and result retrieval | Integration with future dashboards, automated reporting pipelines, dashboard feeds |
| **WebSocket streaming** | Real-time step-by-step progress as the agent runs | Frontend UI, keeping analysts informed during longer analyses |

---

### 5. LLM Inference

**Decision**: Provider-agnostic adapter — Gemini by default

The system is built with a clean abstraction layer between agents and LLM providers. Switching providers requires only a config file change — zero changes to agent code.

| Provider | Use Case |
|----------|----------|
| Gemini API | Default provider for production, development, and benchmarking |
| Other OpenAI-compatible APIs | Supported via the adapter if a team prefers a different provider |

The agent-to-model tier mapping (Flash for most agents, Pro for Report Writer) is preserved in the adapter and mapped to whatever models are configured.

---

## Organisational Context

- **Initiating team**: Operations / Analytics
- **Data custodian**: Data & Analytics team (data submitted by business units)
- **IT infrastructure**: Cloud-hosted
- **Current state**: Analysis done manually in spreadsheets; technical reports require data-team involvement; thematic reviews take weeks

---

## Open Questions (to be resolved in PRD phase)

| # | Question | Needed For |
|---|----------|-----------|
| 1 | How do analysts authenticate today? (SSO provider?) | Security Review, RBAC design |
| 2 | What is the largest dataset an analyst would query in a single session? (rows / GB) | Infrastructure sizing, Executor memory limits |
| 3 | Are there existing report templates used for business reviews? (Word/PDF formats) | Finalizer template design |
| 4 | Does output need to integrate with an existing BI or case management system? | API contract design |
| 5 | What is the data freshness requirement? (Can the system query data that is 24 hours old, or does it need real-time?) | Data ingestion pipeline design |
| 6 | Who has authority to approve what an analyst can query? (Sensitivity tiers for data access) | RBAC policy design |

---

## Next Step

Write the PRD → `01-prd/01-prd-dsstar-platform.md`

*Resume on branch `docs/product-lifecycle` in any future session.*
