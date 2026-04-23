# SKILL: Paseo — Multi-Agent Management Interface
**Source:** https://github.com/getpaseo/paseo
**Domain:** agent-tools
**Trigger:** Use when managing multiple Claude Code, Codex, or OpenCode agents from one interface, running agents in parallel across projects, or controlling agents from mobile devices.

## Summary
Paseo provides a unified interface (iOS, Android, desktop, web, CLI) for running Claude Code, Codex, and OpenCode agents in parallel on your own machines. Self-hosted daemon, voice control, cross-device handoff, and experimental orchestration skills.

## Key Patterns
- Local daemon manages agents; clients connect via QR code or host:port
- `paseo run --provider claude/opus-4.6 "implement user auth"` — CLI usage
- `paseo ls` / `paseo attach <id>` / `paseo send <id> "follow-up"` — session management
- Orchestration skills: `/paseo-handoff` — plan with Claude, implement with Codex
- `--worktree feature-x` — run in isolated git worktree
- Privacy-first: no telemetry, no forced login

## Usage
When user wants to run multiple AI agents in parallel, control them from phone, or hand off tasks between different models (plan with Claude, build with Codex).

## Code/Template
```bash
npm install -g @getpaseo/cli
paseo  # starts daemon, shows QR

# CLI examples
paseo run --provider claude/opus-4.6 "implement feature X"
paseo run --provider codex/gpt-5.4 --worktree feature-x "build Y"
paseo ls
paseo attach abc123
paseo send abc123 "also add unit tests"
```
