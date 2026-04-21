# SKILL: Waza - Engineering Habits as Claude Code Skills
**Source:** https://github.com/tw93/claude-health
**Domain:** code
**Trigger:** When installing engineering habit skills for Claude Code, auditing Claude Code setup health, or applying systematic development workflows via slash commands

## Summary
Eight Claude Code skills packaging core engineering habits: requirement thinking, UI design, diff review, systematic debugging, prose writing, domain learning, URL reading, and Claude Code health audit. Minimal, goal-focused, model-improvement-aware design.

## Key Patterns
- /think: challenges problem and validates architecture before coding
- /design: produces distinctive UI with committed aesthetic direction
- /check: reviews diff, auto-fixes safe issues, verifies with evidence
- /hunt: systematic debugging with root cause confirmed before fixing
- /write: rewrites prose naturally in Chinese and English
- /learn: 6-phase research workflow (collect, digest, outline, fill, refine, publish)
- /read: fetches URLs/PDFs as clean Markdown with platform routing
- /health: audits CLAUDE.md, rules, skills, hooks, MCP (Claude Code only)

## Usage
```bash
npx skills add tw93/Waza -a claude-code -g -y   # Claude Code
npx skills add tw93/Waza -a codex -g -y          # Codex
# Statusline for context/quota display:
curl -sL https://raw.githubusercontent.com/tw93/Waza/main/scripts/setup-statusline.sh | bash
```

## Code/Template
Each skill lives in skills/<name>/SKILL.md with reference docs, helper scripts, and gotchas.
Repo: https://github.com/tw93/Waza (actual repo behind claude-health URL)
