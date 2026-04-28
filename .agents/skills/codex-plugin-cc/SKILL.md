# SKILL: Codex Plugin for Claude Code
**Source:** https://github.com/openai/codex-plugin-cc
**Domain:** code
**Trigger:** When using Codex from inside Claude Code — for code reviews, adversarial reviews, or delegating background tasks to Codex

## Summary
Official OpenAI plugin that integrates Codex into Claude Code workflows. Enables code review, adversarial design review, background task delegation, and job management — all via Claude Code slash commands.

## Key Patterns
- `/codex:review` — Codex code review on current changes (read-only)
- `/codex:adversarial-review` — steerable review challenging design decisions, tradeoffs, assumptions
- `/codex:rescue` — delegate a task to Codex as a subagent
- `/codex:status`, `/codex:result`, `/codex:cancel` — background job management
- `--background` flag for long-running reviews; `--base <ref>` for branch diff review
- Review gate: Stop hook that blocks Claude until Codex review passes
- Config via `.codex/config.toml`: `model`, `model_reasoning_effort`

## Usage
```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```

## Code/Template
```bash
# Typical flows
/codex:review --base main          # review branch diff
/codex:adversarial-review --background challenge caching design
/codex:rescue investigate why CI is failing
/codex:status && /codex:result     # check background job
```
