---
name: AI Workflow PRD System (maiobarbero)
source: https://github.com/maiobarbero/my-ai-workflow
category: Coding
purpose: Structured AI-assisted development workflow: Free-form Plan → PRD → Issues → Tasks → Code → Review → Final Audit
when_to_use: When building software features that require planning, traceability, and maintainable outcomes — especially with AI coding tools
tags: [workflow, prd, issues, tasks, code-review, ai-development, planning]
---

# AI Workflow PRD System

## Purpose
Turns the SDD workflow into a repeatable system. The core principle: AI is great at implementation, bad at figuring out what you actually want. Every step: AI produces something → you review → it gets created.

## When To Use
- Starting any non-trivial feature
- When you need planning + review checkpoints
- When multiple AI tools work on the same codebase
- When accountability and traceability matter
- NOT for: hot-fix patches, quick experiments, 1-file scripts

## How To Apply
**7 steps:**
1. **write-a-prd**: Free-form plan → structured PRD (problem, user stories, implementation decisions, out-of-scope)
2. **prd-to-issues**: PRD → vertical-slice issues (AFK = AI can merge; HITL = human decision required)
3. **issues-to-tasks**: Issues → concrete ordered tasks (one task = one fresh AI session)
4. **Handoff**: Each task description = self-contained prompt to new session (fresh context is intentional)
5. **code-review**: 6-pass review (logic errors, operation ordering, bad practices, security, magic strings, patterns)
6. **final-audit**: Cross-cutting audit after full feature implementation
7. **write-pr-report**: Summarize what was built

**Watch: operation ordering.** AI does right things in wrong sequence (notification before transaction commit).

## Examples
- "Write a PRD for adding WebSocket notifications" → write-a-prd skill
- "Convert this PRD into issues and tasks" → prd-to-issues + issues-to-tasks

## Integration Notes
- Adapted from Mark Pocock skills
- The quality of downstream steps depends entirely on the quality of Step 1 (free-form plan)
- PRD user stories are the backbone of everything downstream
- Acceptance criteria: Given/When/Then format including error cases
