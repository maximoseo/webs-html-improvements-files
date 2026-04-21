---
name: Spec-Driven Development (LIDR)
source: https://github.com/LIDR-academy/manual-SDD
category: Coding
purpose: Complete Spec-Driven Development workflow with reusable skills: PRD → Issues → Tasks → Code → Review → Final Audit
when_to_use: When running AI-assisted development that requires structured, reviewable, maintainable software delivery
tags: [sdd, spec-driven, prd, workflow, ai-coding, multi-copilot, issues]
---

# Spec-Driven Development (LIDR)

## Purpose
Turns SDD from a high-level idea into a repeatable system with shared standards, canonical prompts, and portable conventions. Works across Codex, Cursor, and Claude.

## When To Use
- Starting a new feature or significant codebase change
- When you need planning, review, and verification checkpoints
- When multiple AI tools (Codex, Cursor, Claude) work on the same codebase
- When accountability and traceability matter

## How To Apply
**7-step workflow:**
1. write-a-prd: Free-form plan → structured PRD with user stories and implementation decisions
2. prd-to-issues: PRD → vertical-slice issues (AFK vs HITL classification)
3. issues-to-tasks: Issues → concrete tasks (one task = one focused AI session)
4. Handoff to code: Each task description is a self-contained prompt for a fresh AI session
5. code-review: 6-pass review (logic, operation ordering, bad practices, security, magic strings, patterns)
6. final-audit: Cross-cutting audit after full feature implementation
7. write-pr-report: Summarize what was built

**Key skills in this repo:**
- `enrich-user-story/SKILL.md`
- `write-pr-report/SKILL.md`

## Examples
- "Write a PRD for adding real-time notifications to our app" → runs write-a-prd skill
- "Convert this PRD into issues and tasks" → runs prd-to-issues + issues-to-tasks

## Integration Notes
- Multi-copilot: single canonical source in ai-specs/, symlinked to .codex/, .cursor/, .claude/
- Fresh context per task is intentional — prevents long-session drift
- Technical context goes in docs/, not scattered across files
