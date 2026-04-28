---
name: AI-Assisted Workflow (PRD→Code)
source: https://github.com/maiobarbero/my-ai-workflow
category: Coding
purpose: Structured AI development workflow — Free-form Plan → PRD → Issues → Tasks → Code → Review → Final Audit
when_to_use: When starting a non-trivial feature and want structured planning before coding begins
tags: [workflow, prd, planning, code-review, tdd, vertical-slices, ai-workflow]
---
# AI-Assisted Workflow

## Purpose
A Tech Lead's structured AI workflow where the real work happens before coding starts. Speed benefits of AI without losing clarity and maintainability.

## Core Principle
AI is great at implementation. It's bad at figuring out what you actually want. Every step: AI produces something → you review → it gets created.

## The Workflow
```
Free-form Plan → PRD → Issues → Tasks → Code → Review → Final Audit
```

### Step 1 — Free-form Plan
Write in plain language. Problem, thinking, constraints, uncertainties. No structure required.

### Step 2 — PRD (`write-a-prd`)
Structured interview. Explores codebase, interviews you about every branch of the design tree. Output: PRD with user stories, implementation decisions, module design, explicit out-of-scope items.

### Step 3 — Issues (`prd-to-issues`)
PRD → vertical slice issues (tracer bullets through every integration layer). Each issue: AFK (AI can merge alone) or HITL (human decision required). Each has Given/When/Then acceptance criteria.

### Step 4 — Tasks (`issues-to-tasks`)
Issues → concrete ordered tasks. One task = one focused AI session. If can't complete in one session: too large. Written as instructions to the AI that will execute them.

### Step 5 — Code
Fresh context per task (intentional — long sessions drift). Paste task description + parent issue.

### Step 6 — Code Review (`code-review`)
6-pass: Logic errors → Operation ordering → Bad practices → Security → Magic strings → Pattern improvements.
⚠️ Watch operation ordering — AI tends to notify before committing.

### Step 7 — Final Audit (`final-audit`)
Cross-cutting: inconsistencies between modules, patterns replicated incorrectly, security assumptions across full surface area.

## Integration Notes
- Credits: adapted from Mark Pocock's skills
- Not fast to set up — pays off for non-trivial features
- Pairs with `sdd-skill` for spec-driven variant
