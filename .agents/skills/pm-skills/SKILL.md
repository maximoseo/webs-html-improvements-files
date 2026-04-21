# SKILL: PM Skills Marketplace — AI Operating System for Product Decisions
**Source:** https://github.com/phuryn/pm-skills
**Domain:** marketing
**Trigger:** Use when making product decisions, writing PRDs, running discovery, building go-to-market plans, defining metrics, or conducting market research — as a PM or product-adjacent role.

## Summary
65 PM skills and 36 chained workflows across 8 plugins encoding Teresa Torres, Marty Cagan, and Alberto Savoia frameworks. Available for Claude Code, Cowork, and other agents. Skills chain automatically: `/discover` → `/strategy` → `/write-prd` → `/plan-launch`.

## Key Patterns
- Plugins: pm-toolkit, pm-product-strategy, pm-product-discovery, pm-market-research, pm-data-analytics, pm-marketing-growth, pm-go-to-market, pm-execution
- Commands: `/discover`, `/strategy`, `/write-prd`, `/plan-launch`, `/north-star`, `/mvp`
- Skills auto-load when relevant; force with `/plugin:skill-name`
- Commands chain: each suggests relevant next command
- Frameworks: opportunity-solution-tree, prioritization-frameworks, OKRs, JTBD

## Usage
Start a new idea with `/discover`. Get strategic clarity with `/strategy`. Write structured PRD with `/write-prd`. Define KPIs with `/north-star`. Plan launch with `/plan-launch`.

## Code/Template
```bash
# Claude Code
claude plugin marketplace add phuryn/pm-skills
claude plugin install pm-toolkit@pm-skills
claude plugin install pm-product-discovery@pm-skills
claude plugin install pm-go-to-market@pm-skills

# Usage in chat
/discover  → brainstorm → assumptions → prioritize → experiments
/write-prd → structured PRD with frameworks
/north-star → metric definition with OKRs
```
