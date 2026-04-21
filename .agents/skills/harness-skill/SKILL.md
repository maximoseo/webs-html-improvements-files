---
name: Harness (Team Architecture Factory)
source: https://github.com/revfactory/harness
category: Agent Skills
purpose: Meta-factory that generates Claude Code agent teams — 6 architectural patterns, auto-generates .claude/agents/ and .claude/skills/ from a domain description
when_to_use: When you need a structured multi-agent team for a complex domain (research, development, content creation, code review)
tags: [agent-teams, orchestration, meta-factory, architecture, claude-code, multi-agent]
---
# Harness — Team Architecture Factory

## Purpose
Say "build a harness for this project" and the plugin turns your domain description into an agent team + skills — picked from 6 architectural patterns.

## 6 Architecture Patterns
| Pattern | Use |
|---|---|
| Pipeline | Sequential dependent tasks |
| Fan-out/Fan-in | Parallel independent tasks |
| Expert Pool | Context-dependent selective invocation |
| Producer-Reviewer | Generation + quality review |
| Supervisor | Central agent with dynamic task distribution |
| Hierarchical Delegation | Top-down recursive delegation |

## Trigger
```
"Build a harness for this project"
"Design an agent team for this domain"
"Set up a harness"
```

## Generated Output
```
.claude/
├── agents/     # Agent definition files (analyst.md, builder.md, qa.md)
└── skills/     # Skill files for each agent
```

## Install
```bash
/plugin marketplace add revfactory/harness
/plugin install harness@harness
# or:
cp -r skills/harness ~/.claude/skills/harness
```

## Harness Evolution
`/harness:evolve` — captures delta between initial and shipped harness, feeds back into factory for next-gen improvement.

## Benchmark (A/B, n=15)
- +60% avg quality (49.5 → 79.3)
- 15/15 win rate
- −32% output variance

## Integration Notes
- Requires: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Coexists with Archon (runtime config factory), meta-harness (Codex port), ECC (cross-harness standards)
- 100 production-ready harnesses in `revfactory/harness-100` (10 domains, EN + KO)
