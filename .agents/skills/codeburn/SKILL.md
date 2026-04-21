# SKILL: CodeBurn — AI Coding Token Usage Tracker
**Source:** https://github.com/AgentSeal/codeburn
**Domain:** code
**Trigger:** When you need to track, analyze, or optimize AI coding tool token usage and costs

## Summary
TUI dashboard that tracks token usage and costs across Claude Code, Codex, Cursor, OpenCode, Pi, and GitHub Copilot by reading session data from disk — no proxy or API keys needed.

## Key Patterns
- Auto-detects all AI coding providers on disk
- Tracks cost by task type, tool, model, MCP server, and project
- One-shot success rate per activity type
- JSON/CSV export, auto-refresh every 30s

## Usage
Run `codeburn` for interactive dashboard. Use `codeburn report --format json | jq` for automation/scripting.

## Code/Template
```bash
npm install -g codeburn
codeburn                          # interactive dashboard (7 days)
codeburn today                    # today only
codeburn report --format json     # full data as JSON
codeburn optimize                 # find waste, get fixes
codeburn report --provider claude # Claude Code only
codeburn export -f json           # export to JSON
```
