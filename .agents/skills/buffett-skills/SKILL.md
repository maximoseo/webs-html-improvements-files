---
name: Buffett Investment Skills
source: https://github.com/agi-now/buffett-skills
category: Research
purpose: Warren Buffett's complete investment thinking system — moat analysis, management assessment, valuation, risk, industry playbooks
when_to_use: When analyzing stocks, evaluating business quality, making buy/hold/sell decisions, or studying value investing
tags: [investing, finance, buffett, value-investing, moat, valuation, research]
---
# Buffett Investment Skills

## Purpose
Activates Warren Buffett's complete investment thinking system with structured output and industry-specific playbooks.

## When To Use
- Analyze any stock or company
- Evaluate investment opportunities
- Read financial reports or annual letters
- Judge competitive moat or management quality
- Buy/hold/sell decisions

## Dispatch Logic
| Path | When | Files Read |
|---|---|---|
| A · Quick screen | "Is this worth analyzing?" | 8-question checklist |
| B · Deep analysis | Full evaluation | moat → management → financials → valuation → industry |
| C · Topic question | Specific concept | Relevant reference file directly |

## Output Format (Mandatory)
- Conclusion (Buy/Pass/Watch/Hold/Sell + one-sentence rationale)
- Circle of Competence
- Key Assumptions (3-5)
- Business Quality (moat type + management)
- Financial Snapshot (ROIC, cash conversion, owner earnings)
- Valuation (intrinsic value range, margin of safety, entry price)
- Sell Criteria Check
- Key Risks (top 3)
- Monitoring Indicators
- Final Verdict in Buffett's voice

## Benchmark
- With skill: 100% pass rate (15/15), avg 43k tokens
- Without skill: 66.7% pass rate (10/15), avg 12k tokens
- +33% pass rate improvement

## Integration Notes
- Install: `cp -r skills/buffett .claude/skills/buffett`
- 8 reference files loaded progressively based on analysis type
- No need to say "Buffett" — any investment analysis triggers it
