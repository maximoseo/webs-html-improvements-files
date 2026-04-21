---
name: Skill-Based Architecture (Meta-Skill)
source: https://github.com/WoJiSama/skill-based-architecture
category: Agent Skills
purpose: Meta-skill that produces skills — analyzes any codebase and distills its rules, workflows, and patterns into a dedicated project skill directory
when_to_use: When onboarding to a new codebase, when creating project-specific skills, or when standardizing AI agent behavior across a team
tags: [meta-skill, codebase-analysis, skill-generation, project-skills, ai-standards]
---

# Skill-Based Architecture (Meta-Skill)

## Purpose
Point it at any codebase and it distills the project rules, workflows, and hard-won lessons into a dedicated `skills/<name>/` directory — a project skill that becomes the single source of truth every AI agent consults before every task.

## When To Use
- New team member / agent onboarding to a codebase
- Standardizing how Cursor, Claude Code, Codex, Windsurf, Gemini behave on a project
- Creating reusable workflow patterns from implicit codebase conventions
- When the same mistakes keep happening because context isn't captured

## How To Apply
1. Point the skill at a codebase directory
2. It analyzes: architecture patterns, naming conventions, error handling, test patterns, deployment workflows, common pitfalls
3. Output: `skills/<project-name>/SKILL.md` + optional reference files
4. Install the generated skill in all team members' agent configs
5. Evolve the skill as the project grows

## Examples
- "Build a skill from this Next.js codebase" → generates skills/nextjs-app/SKILL.md with project conventions
- "Create a harness skill from the payment service" → distills payment-specific patterns

## Integration Notes
- Output format is agentskills.io spec-compatible
- Compatible with Cursor, Claude Code, Codex, Windsurf, Gemini
- Pair with harness-team-factory for full project + team architecture
- The generated skill is a living document — update as patterns evolve
