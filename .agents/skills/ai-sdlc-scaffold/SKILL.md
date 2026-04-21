# SKILL: AI SDLC Scaffold
**Source:** https://github.com/pangon/ai-sdlc-scaffold
**Domain:** code
**Trigger:** When starting a new AI-first software project and needing a scaffold that organizes the full SDLC (Spec → Design → Code → Deploy) with Claude Code skills, decision records, and agent instructions

## Summary
A repository template for AI-first software development organizing the entire SDLC into 4 phases with Claude Code skills, hierarchical CLAUDE.md instructions, two-file decision records, and traceability from business goals to running code. Context-window efficient — hierarchical instructions minimize tokens agents must load.

## Key Patterns
- 4 phases: `1-spec/` (WHAT/WHY), `2-design/` (HOW), `3-code/` (BUILD), `4-deploy/` (SHIP)
- Each phase has `CLAUDE.<phase>.md` extending root `CLAUDE.md`
- Skills: `/SDLC-init`, `/SDLC-elicit`, `/SDLC-design`, `/SDLC-decompose`, `/SDLC-execute-next-task`, `/SDLC-fix`, `/SDLC-status`
- Two-file decisions: `DEC-name.md` (active, enforced) + `DEC-name.history.md` (audit trail)
- Artifact IDs: `GOAL-reduce-latency`, `REQ-F-search-by-name`, `DEC-use-postgres`
- Phase gates: minimum preconditions before advancing to next phase

## Usage
```bash
npx degit pangon/ai-sdlc-scaffold my-project
cd my-project
rm -f CONTRIBUTING.md CONTRIBUTORS.md LICENSE NOTICE RATIONALE.md README.md
git init && git add -A && git commit -m "Initial scaffold"
# Then in Claude Code: /SDLC-init
```

## Code/Template
```
project/
├── CLAUDE.md                    # root agent instructions
├── 1-spec/CLAUDE.spec.md        # phase instructions + artifact indexes
├── 2-design/CLAUDE.design.md
├── 3-code/CLAUDE.code.md
├── 4-deploy/CLAUDE.deploy.md
├── decisions/DEC-*.md           # active decisions
└── .claude/skills/SDLC-*/SKILL.md  # automation layer
```
