---
name: AutoSkills (Stack-Detecting Installer)
source: https://github.com/midudev/autoskills
category: Tools
purpose: Auto-detect project tech stack and install matching Claude Code skills in one command
when_to_use: When starting a new project or onboarding to an existing codebase — auto-installs relevant skills
tags: [tools, installer, stack-detection, claude-code, productivity]
---
# AutoSkills

## Purpose
Automatically detects the tech stack of a project and installs the most relevant Claude Code skills without manual selection.

## When To Use
- Starting work on a new or unfamiliar codebase
- Onboarding a team to a standard skill set
- After adding new tech to an existing project (e.g., adding Next.js to a React app)

## How To Apply
```bash
npx autoskills
```
1. Scans `package.json`, `requirements.txt`, `Gemfile`, `go.mod`, etc.
2. Detects stack (React, Next.js, Django, Rails, Go, etc.)
3. Downloads + installs matching skills into `.claude/skills/`
4. Generates `CLAUDE.md` summary of installed skills and triggers

## Examples
```bash
# In a Next.js project
npx autoskills
# → detects React + Next.js + TypeScript
# → installs: frontend-dev, typescript-patterns, nextjs-routing, etc.

# Force specific skills
npx autoskills --skills react,typescript,testing
```

## Integration Notes
- Creates `CLAUDE.md` at project root summarizing all skills
- Works with Claude Code, Cursor, Codex CLI
- Respects existing `.claude/skills/` — only adds, never overwrites
