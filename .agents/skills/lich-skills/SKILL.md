---
name: Lich Skills (Spec-Driven Dev + Debug)
source: https://github.com/LichAmnesia/lich-skills
category: Coding
purpose: Telegraph-style engineering skills — spec-driven dev loop, debug-hypothesis loop, wiki-aggregate, tavily search, nano-banana image gen
when_to_use: For structured software delivery (Spec→Plan→Build→Test→Review→Ship), scientific debugging, or multi-source research aggregation
tags: [spec-driven, debugging, research, image-generation, coding, workflow]
---
# Lich Skills

## Purpose
5 opinionated engineering skills with explicit exit criteria and anti-rationalization guards.

## Skills Included

### spec-driven-dev
Full SDLC: Spec → Plan → Build → Test → Review → Ship with anti-rationalization tables and verification gates.

### debug-hypothesis
Scientific-method debugging: Observe → Hypothesize → Experiment → Conclude. Max 5-line experiments. Mandatory `DEBUG.md` evidence trail. Prevents AI bulldozing through wrong theories.

### wiki-aggregate
Agentic aggregation for long-horizon research: N raw notes → 1 structured pack. Every claim gets `path:line` provenance. Cross-source contradictions surfaced.

### tavily-search
Web search + content extraction via Tavily API. Use for fact-checking, docs lookup, source-cited research.

### nano-banana
Text-to-image + editing via Google Nano Banana 2 (gemini-3.1-flash-image-preview). Supports 512/1K/2K/4K.

## Install
```
/plugin marketplace add LichAmnesia/lich-skills
/plugin install lich-skills@lich-skills
```

## Integration Notes
- All skills use environment variables only (TAVILY_API_KEY, GEMINI_API_KEY)
- Works with Claude Code, Gemini CLI, OpenAI Codex
- Debug loop diagram forces hypothesis-before-experiment discipline
