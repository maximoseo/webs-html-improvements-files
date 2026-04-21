# SKILL: Capit
**Source:** https://github.com/day50-dev/capit
**Domain:** code
**Trigger:** When managing per-agent API spending budgets or preventing runaway LLM costs from agent loops

## Summary
A CLI tool that creates capped API keys for AI agents using OpenRouter/AiHubMix guardrails. Each agent gets its own spending-limited key — if it goes rogue, it can only cost the capped amount. Fully local, no capit servers.

## Key Patterns
- `capit openrouter <amount> --agent <name>` — create capped key and install into agent config
- Per-agent isolation: each agent gets its own key with independent cap
- Supported agents: claude, cursor, windsurf, openclaw, and more
- Key cap enforced by OpenRouter (not just locally)
- `capit --keys list` — view all keys with spending info
- `capit --keys delete <name>` — delete specific key
- Platform extensible via skills: `skills/platform-creator.md`
- Backup created automatically before overwriting agent config

## Usage
Install: `uv tool install capit`. Add OpenRouter master key: `capit --platforms add`. Then: `capit openrouter 5.00 --agent claude`. Agent now has a $5 hard cap.

## Code/Template
```bash
# Give Claude Code a $5 budget
capit openrouter 5.00 --agent claude

# Give Cursor a $10 budget
capit openrouter 10.00 --agent cursor

# List all keys with spending
capit --keys list

# List supported agents
capit --agents
```
