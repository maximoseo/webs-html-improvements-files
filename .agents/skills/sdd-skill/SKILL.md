---
name: Spec-Driven Development (SDD Starter Kit)
source: https://github.com/LIDR-academy/manual-SDD
category: Coding
purpose: Multi-copilot spec-driven development — single canonical ai-specs/ shared across Codex, Cursor, Claude via symlinks; enrich-user-story and write-pr-report skills
when_to_use: When running a structured SDD workflow across multiple AI tools (Cursor, Claude Code, Codex) with a shared skill source
tags: [spec-driven, sdd, workflow, planning, multi-copilot, symlinks, canonical]
---
# Spec-Driven Development (SDD) Starter Kit

## Purpose
Practical manual and starter kit for Spec-Driven Development with AI — single canonical source in `ai-specs/` exposed to all AI tools via symlinks.

## Repository Structure
```
ai-specs/          # Canonical source (agents, commands, skills)
├── .agents/       # Agent role definitions
├── .commands/     # Shared utility commands
└── skills/        # Canonical skill definitions (main entrypoint)

.codex/ → symlinks to ai-specs/
.cursor/ → symlinks to ai-specs/
.claude/ → symlinks to ai-specs/
```

## Why Symlinks
- Single source of truth: one definition for agents/commands/skills
- No duplicated maintenance: update once, all tools stay aligned
- Safe evolution: workflows change without reorganizing every folder

## Skills Included
- `enrich-user-story/SKILL.md` — enriches user stories with acceptance criteria, edge cases, and implementation hints
- `write-pr-report/SKILL.md` — generates PR reports with context, changes, risks, and test evidence

## Quick Start
1. Copy structure into your project
2. Keep `ai-specs/` as canonical
3. Create symlinks from `.codex/`, `.cursor/`, `.claude/` to `ai-specs/`
4. Store project context in `docs/`
5. Build new workflows as skills under `ai-specs/skills/`

## Integration Notes
- Creator: Javier Vargas, Head of AI @ Mapal
- Pairs with `ai-workflow-skill` for full PRD→Code workflow
- Uses OpenSpec-ready structure for broader ecosystem compatibility
- Docs: `doc_architecture.md`, `doc_ai_planning_mode.md`, `doc_verification_guide.md`
