# SKILL: Agentlytics
**Source:** https://github.com/f/agentlytics
**Domain:** code
**Trigger:** When analyzing AI coding session metrics across multiple editors, tracking token costs, or comparing editor effectiveness

## Summary
A unified analytics dashboard for AI coding sessions across 16 editors (Cursor, Windsurf, Claude Code, VS Code Copilot, Codex, Gemini CLI, Zed, etc.). One command, fully local, no data leaves machine. Shows KPIs, token costs, activity heatmaps, and coding streaks.

## Key Patterns
- Supports 16 editors: auto-detects installed editors and sessions
- `npx agentlytics` — opens dashboard at http://localhost:4637
- `npx agentlytics --collect` — build cache without starting server
- Deno sandboxed mode: `deno run --allow-read --allow-env mod.ts` — zero network/write access
- `--json` flag for machine-readable output
- Dashboard: KPIs, heatmap, editor breakdown, token economy, peak hours, top models/tools
- Session search across all conversations
- 100% local — reads editor-specific locations (`~/.claude/`, `~/.cursor/`, `~/.codex/`, etc.)
- macOS-only for full dashboard; Deno scan works cross-platform

## Usage
Run `npx agentlytics` or `bunx agentlytics`. For CI/scripts use Deno sandboxed mode. Access dashboard at http://localhost:4637.

## Code/Template
```bash
# Full dashboard
npx agentlytics
# or: bunx agentlytics | pnpm dlx agentlytics

# Lightweight scan (Deno, no install)
deno run --allow-read --allow-env https://raw.githubusercontent.com/f/agentlytics/master/mod.ts

# JSON output for scripting
deno run --allow-read --allow-env mod.ts --json

# Build cache only (no server)
npx agentlytics --collect
```
