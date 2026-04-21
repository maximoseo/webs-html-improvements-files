---
name: Skill-Based Architecture (Meta-Skill Generator)
source: https://github.com/WoJiSama/skill-based-architecture
category: Agent Skills
purpose: Meta-skill that analyzes any codebase and distills its rules, workflows, and lessons into a dedicated project skill
when_to_use: When onboarding to a new codebase, or when you need to create a reusable skill from an existing project's conventions
tags: [meta-skill, codebase-analysis, architecture, skill-generation, conventions]
---
# Skill-Based Architecture

## Purpose
A meta-skill that produces skills. Point it at any codebase and it distills the project's rules, workflows, and hard-won lessons into a dedicated `skills/<name>/` directory.

## When To Use
- Starting on a new codebase and want AI to follow its conventions
- After discovering important patterns that should be reusable
- Creating a "project memory" that every AI agent consults before every task

## How To Apply
1. Point at a codebase: "Analyze this project and create a project skill"
2. The skill reads existing files, discovers patterns, extracts conventions
3. Outputs a `skills/<project-name>/` with SKILL.md and references/

Output includes:
- Architectural decisions and rationale
- Naming conventions and code patterns
- Test approaches and quality gates
- Anti-patterns to avoid
- Workflow scripts and automation patterns

## Examples
```
"Create a project skill from this React/Next.js codebase"
"Distill the galoz.co.il article template conventions into a skill"
"Build a skill from our n8n workflow patterns"
```

## Integration Notes
- Output is a SKILL.md that becomes single source of truth for every AI agent
- Works with Cursor, Claude Code, Codex, Windsurf, Gemini
- Pairs with `autoskills` for installation automation
