# SKILL: cc-skills-golang — Production-Ready Go Agent Skills
**Source:** https://github.com/samber/cc-skills-golang
**Domain:** developer-tools
**Trigger:** Use when working on Go projects and needing AI agent guidance on idiomatic Go patterns, error handling, testing, observability, performance, security, or concurrency — not generic Go questions.

## Summary
A collection of Go-specific agent skills covering language idioms, error handling, testing, security, observability, and performance. Designed as atomic, cross-referencing units — install all for consistent guidelines. Human-reviewed, no AI slop.

## Key Patterns
- Skills are atomic and cross-referencing: install all for consistency
- golang-performance, golang-error-handling, golang-observability, golang-testing, golang-security
- `npx skills add https://github.com/samber/cc-skills-golang --all` — install all
- Single skill: `npx skills add ... --skill golang-performance`
- Works with Claude Code, Openclaw, Cursor, Copilot, OpenCode, Codex, Antigravity

## Usage
Install all Go skills together for consistent agent behavior. Skills cross-reference each other — e.g., error handling rules affect logging guidelines.

## Code/Template
```bash
# Install all (recommended)
npx skills add https://github.com/samber/cc-skills-golang --all

# Claude Code
/plugin marketplace add samber/cc
/plugin install cc-skills-golang@samber

# Gemini CLI
gemini extensions install https://github.com/samber/cc-skills-golang

# OpenCode
git clone https://github.com/samber/cc-skills-golang.git ~/.agents/skills/cc-skills-golang
```
