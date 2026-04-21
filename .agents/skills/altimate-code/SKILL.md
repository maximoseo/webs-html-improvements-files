# SKILL: Altimate Code — Data Engineering AI Harness
**Source:** https://github.com/AltimateAI/altimate-code
**Domain:** code
**Trigger:** When working with SQL, dbt, data warehouses, or data engineering tasks with an AI agent

## Summary
100+ deterministic tools for SQL analysis, column-level lineage, dbt, FinOps, and warehouse connectivity. Works standalone or as intelligence layer under Claude Code/Codex.

## Key Patterns
- SQL anti-pattern detection: 19 rules, 100% F1, 0 false positives
- Column-level lineage extraction (100% edge-match on 500 queries)
- Cross-dialect SQL translation: Snowflake ↔ BigQuery ↔ Databricks ↔ Redshift
- PII detection: 15 categories, 30+ regex patterns
- dbt native: manifest parsing, test gen, model scaffolding

## Usage
Use for any data engineering/SQL task. Integrate with Claude Code via `/configure-claude`.

## Code/Template
```bash
npm install -g altimate-code
altimate /connect       # setup LLM provider
altimate /discover      # auto-detect data stack (dbt, warehouse, tools)
# Then use natural language:
# "Analyze this query for issues: SELECT * FROM ..."
# "/sql-translate this Snowflake query to BigQuery: ..."
# "/generate-tests for models/staging/stg_orders.sql"
# "/cost-report"
```
