---
name: Paper Orchestra Writing
source: https://github.com/Ar9av/PaperOrchestra
category: Research
purpose: Multi-agent pipeline for turning unstructured research materials into submission-ready LaTeX papers with 5 specialized agents
when_to_use: When automating research paper writing from experimental logs, ideas, or scattered agent history
tags: [research, paper-writing, latex, multi-agent, literature-review, academic]
---

# Paper Orchestra Writing

## Purpose
Implements the PaperOrchestra 5-agent pipeline: Outline → Plotting → Literature Review → Section Writing → Content Refinement. Produces submission-ready LaTeX papers. Based on arXiv:2604.05018, with 50-68% win margins on literature review quality.

## When To Use
- Converting experimental logs + research ideas into LaTeX papers
- Automating literature review with Semantic Scholar verification
- Generating publication-quality figures (via PaperBanana integration)
- Building academic papers from scattered agent histories (via agent-research-aggregator)

## How To Apply
**Option A — structured inputs exist:**
1. Scaffold workspace: `python skills/paper-orchestra/scripts/init_workspace.py`
2. Add: idea.md, experimental_log.md, template.tex, conference_guidelines.md
3. Tell agent: "Run paper-orchestra pipeline on ./workspace"

**Option B — scattered research:**
1. Tell agent: "Write a paper from my work in ~/my-project"
2. Agent runs agent-research-aggregator first (4-phase: Discover → Extract → Synthesize → Format)
3. Then runs full 5-agent pipeline

**7 skills:**
- paper-orchestra (orchestrator)
- outline-agent, plotting-agent, literature-review-agent
- section-writing-agent, content-refinement-agent
- paper-writing-bench, paper-autoraters
- agent-research-aggregator (optional pre-pipeline)

## Examples
- "Turn my experiments in ~/research into a NeurIPS submission"
- "Aggregate my Claude Code history and write a conference paper"

## Integration Notes
- No API keys required for core pipeline (uses agent's web search)
- Optional: Semantic Scholar API key (higher rate limits), PaperBanana (figure generation, needs Gemini/OpenRouter key), Exa API (research search)
- All prompts are verbatim from Appendix F of the paper
- Steps 2 and 3 (Plotting + Literature Review) run in parallel
