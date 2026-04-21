# SKILL: Context Gateway — Background LLM Context Compaction
**Source:** https://github.com/Compresr-ai/Context-Gateway
**Domain:** code
**Trigger:** When AI agent conversations hit context limits and you want background compaction without waiting

## Summary
Sits between your AI agent (Claude Code, Cursor, OpenClaw) and LLM API. Pre-computes context compression in the background so compaction is instant when triggered, eliminating wait time.

## Key Patterns
- Transparent proxy between agent and LLM API
- Trigger threshold configurable (default 75% context fill)
- Supports claude_code, cursor, openclaw, custom agents
- Logs to logs/history_compaction.jsonl

## Usage
Install and configure once; runs transparently in background for any agent session.

## Code/Template
```bash
curl -fsSL https://compresr.ai/api/install | sh
context-gateway    # interactive TUI wizard to configure agent + threshold
# Choose: claude_code | cursor | openclaw | custom
# Set summarizer model, API key, trigger threshold
```
