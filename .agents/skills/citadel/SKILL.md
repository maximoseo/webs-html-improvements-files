# SKILL: Citadel — Agent Orchestration Harness
**Source:** https://github.com/SethGammon/Citadel
**Domain:** agent-tools
**Trigger:** Use when setting up persistent agent memory, multi-agent orchestration, session resumption, or intent routing for Claude Code or OpenAI Codex projects.

## Summary
Citadel is an agent orchestration harness for Claude Code and Codex that coordinates parallel AI agents, persists memory across sessions, and routes intent to the cheapest execution path. Includes campaign persistence, telemetry, safety hooks, and worktree-based parallel execution.

## Key Patterns
- `/do` command routes intent: simple edits → direct, complex tasks → agent
- Persistent memory across sessions (no re-explaining codebase each time)
- Parallel agent spawning in isolated git worktrees
- Skills compound across sessions — build once, reuse forever
- Claude Code: `claude --plugin-dir /path/to/Citadel`
- Codex: run `codex-compat.js` + `install-hooks-codex.js`
- Quota-free local runners for routine/scheduled tasks

## Usage
When a user wants their AI agent to remember context across sessions, run tasks in parallel, or automatically route simple vs complex work. Run `/do setup` after installation.

## Code/Template
```bash
git clone https://github.com/SethGammon/Citadel.git

# Claude Code
claude --plugin-dir /path/to/Citadel

# Codex
node /path/to/Citadel/scripts/codex-compat.js
node /path/to/Citadel/scripts/install-hooks-codex.js

# Setup
/do setup
/do review src/main.ts
```
