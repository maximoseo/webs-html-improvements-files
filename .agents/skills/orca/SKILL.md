# SKILL: Orca - Multi-Agent AI Orchestrator Desktop App
**Source:** https://github.com/stablyai/orca
**Domain:** code
**Trigger:** When running multiple AI coding agents side-by-side, managing multi-repo agent workflows, or needing a desktop GUI for Claude Code/Codex/Gemini orchestration

## Summary
Desktop AI orchestrator for macOS/Windows/Linux that runs Claude Code, Codex, OpenCode and 20+ other CLI agents side-by-side in worktree-isolated tabs. Built-in source control, GitHub PR/issue integration, and per-worktree feature branches.

## Key Patterns
- Worktree-native: every feature gets its own worktree (no stashing/branch juggling)
- Multi-agent terminals: tabs and panes with active-agent indicators
- Built-in diff review and quick edit before committing
- GitHub integration: PRs, issues, Actions checks linked per worktree
- No login required: BYOK (bring your own Claude Code/Codex subscription)
- Supports any CLI agent, not just the listed ones

## Usage
Download at https://onOrca.dev. No login needed - brings your existing CLI agent subscriptions. Create worktrees per feature, run agents in tabs, review diffs in-app, commit without leaving Orca.

## Code/Template
```
Workflow: Create worktree → Launch agent in tab → Review diff in-app → Commit → PR
Supported: Claude Code, Codex, Gemini, Pi, Hermes, OpenCode, Goose, Amp, Cline, Cursor, etc.
```
