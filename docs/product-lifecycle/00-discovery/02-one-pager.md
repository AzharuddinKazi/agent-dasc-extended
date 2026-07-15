# 1-Pager: DS-STAR Analytics Platform

**Stage**: Discovery — Stage 0
**Date**: 2026-06-24
**Author**: Product Team
**DRI**: TBD (pending project intake)
**Status**: Draft for leadership review

---

## The Problem

Analysts across the business sit on rich, multi-file datasets — sales reports, transaction logs, customer records, operational feeds — but extracting insights from this data today requires either writing Python/SQL code or waiting for a data team to build a report. Neither is fast enough for day-to-day decision-making.

The result: decisions are made on incomplete data, thematic reviews take weeks when they should take hours, and the analytical depth of a report is constrained by what a non-technical user can produce in a spreadsheet.

---

## The Hypothesis

If a non-technical analyst could type a question in plain English — "Which regions have the highest return rate relative to sales volume?" — and receive a clear, cited, data-backed answer in minutes, the quality and speed of analytical work would materially improve.

This is now technically feasible. Google's DS-STAR paper (arxiv:2509.21825, 2025) demonstrated that a structured multi-agent pipeline can autonomously plan, code, execute, verify, and iterate over complex multi-file datasets — with no human in the loop between question and answer. On hard analytical tasks, it outperforms a frontier LLM used alone by 32 percentage points.

---

## What We Are Building

An analytics platform — **DS-STAR** — built on the DS-STAR and DS-STAR+ architecture, generalized as a domain-agnostic data-analysis product for any team working with CSV, Excel, or JSON data.

**Two modes:**

- **DS-STAR (Insight mode)**: Answer specific analytical questions over uploaded data. The user types a question; the system plans, codes, executes, verifies, and returns a data-backed answer with a plain-English explanation.

- **DS-STAR+ (Research mode)**: Generate full research reports for open-ended topics. The system decomposes the topic into sub-questions, answers each independently, then synthesises a cited, structured report — ready for leadership briefings, thematic reviews, or business reports.

---

## Target Users

**Primary: Business analysts and operations teams** — benchmark performance, identify outliers, produce thematic review reports without writing code.

**Also serves:**
- Data & analytics teams looking to speed up ad-hoc requests
- Product and marketing teams analyzing usage and campaign data
- Finance and operations teams building recurring performance reports
- Research and strategy teams producing sector-wide trend reports

---

## Why Now

1. **The paper is proven**: DS-STAR is published, peer-reviewed, and benchmarked. We are not building research; we are adapting an engineered, validated system.

2. **Cloud LLM APIs are mature and cheap enough**: Models like Gemini 2.5 Flash and Pro now make autonomous, multi-round code generation and verification affordable at production scale.

3. **Data volume keeps growing while technical headcount doesn't**: Teams generate more spreadsheets, exports, and logs than their data teams can turn into reports.

---

## Why This Team

A small product team can build and iterate on an internal tool faster than waiting on a vendor, and a system built on a published, open architecture gives us full control over model selection and product direction.

---

## What Success Looks Like (Proposed KPIs)

| Metric | Baseline (Today) | Target (12 months post-launch) |
|--------|-----------------|-------------------------------|
| Time to produce a benchmarking table | 3–5 days (manual spreadsheet work) | < 15 minutes |
| Time to produce a thematic review report | 4–8 weeks | < 2 days |
| % of analytical requests answered same-day | ~20% | > 80% |
| Analyst satisfaction with data access | TBD (survey) | > 4.0 / 5.0 |
| # of thematic reviews completed per year | TBD (baseline) | 2× current |

---

## What This Is Not

- Not a replacement for human judgement — the system provides analysis; the analyst interprets and decides
- Not a general-purpose BI dashboard — this is a natural-language, agent-driven analysis tool, not a static reporting layer
- Not a real-time alerting system — this is an analytics tool for on-demand and scheduled analysis, not a streaming alert engine
- Not a data warehouse or ETL platform — it analyzes the files and datasets it's given; it does not replace existing data infrastructure

---

## Rough Effort Estimate (to be refined in TDD)

| Phase | Scope | Estimated Duration |
|-------|-------|-------------------|
| DS-STAR core implementation | 8-agent pipeline, Docker sandbox, state machine | 6–8 weeks |
| Domain-agnostic layer | Analyzer extension, general knowledge base, Explainer | 4–5 weeks |
| DS-STAR+ extension | Sub-question generator, Report Writer, Evaluator | 3–4 weeks |
| REST API + basic frontend | Query submission, result retrieval, PDF export | 4–5 weeks |
| Security hardening + audit log | RBAC, access controls, immutable log | 3–4 weeks |
| Integration testing + UAT | Realistic sample data, analyst user testing | 3–4 weeks |
| **Total** | | **~23–30 weeks** |

---

## Immediate Next Steps

1. Leadership review and Go / No-Go decision
2. Assign DRI and form cross-functional team (Eng, Product, Security)
3. Confirm cloud LLM provider and hosting approach
4. Write full PRD — `01-prd/01-prd-dsstar-platform.md`

---

*This 1-pager is the starting point for the project intake process. It does not commit to any implementation detail. Those are captured in the PRD and TDD.*
