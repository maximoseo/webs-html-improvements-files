# SKILL: Finance Skills — Financial Analysis Agent Skills
**Source:** https://github.com/himself65/finance-skills
**Domain:** marketing
**Trigger:** Use when performing stock analysis, earnings research, ETF analysis, options payoff calculations, social media financial research, startup valuation, or financial data visualization within an AI agent.

## Summary
A collection of agent skills for financial analysis including market analysis (yfinance), social media readers (Twitter/Discord/LinkedIn/Telegram/YC), data providers, startup tools, and UI visualization. Organized as installable plugins for Claude Code.

## Key Patterns
- `finance-market-analysis`: earnings-preview, earnings-recap, stock-correlation, stock-liquidity, ETF premium, SEPA strategy, SaaS valuation, options payoff
- `finance-social-readers`: read-only Twitter, Discord, LinkedIn, Telegram, YC data
- `finance-data-providers`: structured market data feeds
- `finance-ui-tools`: charts and visualization components
- Install all: `npx plugins add himself65/finance-skills`
- Educational only — not financial advice

## Usage
When user needs financial research within an agent conversation: stock earnings, correlation analysis, valuation multiples, or reading financial social feeds.

## Code/Template
```bash
npx plugins add himself65/finance-skills
# or individual plugins:
npx plugins add himself65/finance-skills --plugin finance-market-analysis
npx plugins add himself65/finance-skills --plugin finance-social-readers

# Skills include: earnings-preview, earnings-recap, etf-premium, 
# options-payoff, saas-valuation-compression, sepa-strategy,
# stock-correlation, stock-liquidity, yfinance-data
```
