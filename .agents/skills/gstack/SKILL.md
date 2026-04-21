# SKILL: GStack
**Source:** https://github.com/garrytan/gstack
**Domain:** code
**Trigger:** When turning Claude Code into a virtual engineering team with specialized roles (CEO, PM, designer, reviewer, QA, security, release engineer)

## Summary
Garry Tan's (YC CEO) open-source software factory with 23 specialist slash commands and 8 power tools for Claude Code. Ships a full virtual engineering team: plan-ceo-review, plan-eng-review, design-review, review, qa, ship, security audit, and more. MIT license.

## Key Patterns
- 23+ slash commands: `/office-hours`, `/plan-ceo-review`, `/plan-eng-review`, `/design-review`, `/review`, `/qa`, `/ship`, `/land-and-deploy`, `/canary`, `/benchmark`, `/browse`, `/cso`, `/retro`, `/investigate`, `/document-release`, `/codex`
- Team mode: auto-updates for shared repos via `./setup --team`
- `/browse` skill for all web browsing (never use MCP chrome tools directly)
- `/review` — code review with production bug detection
- `/qa` — opens real browser for QA testing
- `/cso` — OWASP + STRIDE security audit
- `/ship` — PR creation workflow
- gstack-team-init for shared repos: `required` or `optional` mode
- OpenClaw compatible: skills work via ACP when Claude Code has gstack

## Usage
Install: paste one-liner into Claude Code (git clone to `~/.claude/skills/gstack && ./setup`). Start with `/office-hours`, then `/plan-ceo-review`, then `/review` on changed code, then `/qa` on staging URL.

## Code/Template
```bash
# Install (paste into Claude Code)
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git \
  ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup

# Team mode (shared repo)
(cd ~/.claude/skills/gstack && ./setup --team) && \
  ~/.claude/skills/gstack/bin/gstack-team-init required && \
  git add .claude/ CLAUDE.md && git commit -m "require gstack"

# Key workflows:
# /office-hours        — describe what you're building
# /plan-ceo-review     — product + feature review
# /review              — code review on current branch
# /qa                  — browser QA on staging URL
# /ship                — create PR
```
