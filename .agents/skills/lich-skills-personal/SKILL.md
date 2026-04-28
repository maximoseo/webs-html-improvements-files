---
name: Lich Skills Personal Collection
source: https://github.com/LichAmnesia/lich-skills
category: Agent Skills
purpose: Personal engineering skill collection: spec-driven dev loop, debug-hypothesis loop, aggregate-N-sources, Tavily search, and Nano Banana image generation
when_to_use: When needing opinionated high-leverage engineering skills with scientific debugging methodology and multi-source research aggregation
tags: [spec-driven, debug, research-aggregation, web-search, image-generation, engineering]
---

# Lich Skills Personal Collection

## Purpose
5 engineering judgment skills built for Claude Code, Gemini CLI, and OpenAI Codex. Telegraph-style, opinionated, no filler.

## When To Use
- **spec-driven-dev**: Full SDLC workflow with anti-rationalization tables and exit criteria per phase
- **debug-hypothesis**: Scientific debugging (Observe → Hypothesize → Experiment → Conclude) — prevents bulldozing wrong theories
- **wiki-aggregate**: Aggregate N≥3 raw research artifacts into 1 structured pack with path:line provenance
- **tavily-search**: Web search + content extraction via Tavily API for fact-checking and source-cited research
- **nano-banana**: Text-to-image and image editing via Google's Nano Banana 2 (512/1K/2K/4K resolution)

## How To Apply
**Install (Claude Code):**
```
/plugin marketplace add LichAmnesia/lich-skills
/plugin install lich-skills@lich-skills
```

**Debug workflow:**
1. OBSERVE: Reproduce bug, collect symptoms, never touch code yet
2. HYPOTHESIZE: List 3-5 causes with evidence for each
3. EXPERIMENT: One test max 5 lines, falsify don't confirm
4. CONCLUDE: Root cause confirmed → fix + regression test

**Aggregate workflow:**
1. Point aggregator at N sources
2. Inspector reads files using tool budget of 25 iterations
3. Output: brief.md, findings.md, sources.tsv, _aggregation_log.md with path:line claims

## Examples
- "Debug this authentication failure" → triggers debug-hypothesis loop with mandatory DEBUG.md
- "Aggregate these 5 research papers on transformers" → triggers wiki-aggregate
- "Search for recent papers on diffusion models" → triggers tavily-search

## Integration Notes
- All credentials via env vars (TAVILY_API_KEY, GEMINI_API_KEY) — never hardcoded
- Repo scanned with gitleaks for secret leakage prevention
- Compatible: Claude Code, Gemini CLI, OpenAI Codex
