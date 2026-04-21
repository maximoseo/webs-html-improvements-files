---
name: Harness Team Architecture Factory
source: https://github.com/revfactory/harness
category: Agent Skills
purpose: Meta-factory that generates complete agent team architectures from a domain description — 6 patterns, auto-generates agent definitions and skills, with evolution feedback loop
when_to_use: When designing multi-agent systems for any domain, generating team architectures, or building agent pipelines for complex workflows
tags: [multi-agent, team-architecture, agent-factory, orchestration, harness, meta-skill]
---

# Harness Team Architecture Factory

## Purpose
Domain sentence → complete agent team + skills, picked from 6 pre-defined team-architecture patterns. Generates .claude/agents/ and .claude/skills/ tailored to your domain. Evolution mechanism feeds delta back into factory for next-gen improvement.

## When To Use
- "Build a harness for this project" / "Design an agent team for this domain"
- Starting multi-agent workflows for: deep research, website dev, code review, content production, data pipelines, marketing campaigns
- When you need Pipeline / Fan-out / Expert Pool / Producer-Reviewer / Supervisor / Hierarchical patterns

## How To Apply
**Install:**
```bash
cp -r skills/harness ~/.claude/skills/harness
```

**6 architecture patterns:**
| Pattern | Use Case |
|---------|----------|
| Pipeline | Sequential dependent tasks |
| Fan-out/Fan-in | Parallel independent tasks |
| Expert Pool | Context-dependent selective invocation |
| Producer-Reviewer | Generation + quality review |
| Supervisor | Central agent + dynamic distribution |
| Hierarchical Delegation | Top-down recursive delegation |

**6-phase workflow:** Domain Analysis → Team Design → Agent Definitions → Skill Generation → Integration → Validation

**Evolution mechanism:**
1. Initial harness deployed
2. Real project usage
3. `/harness:evolve` captures shipped-vs-initial delta
4. Factory improves next-gen for similar domains

**A/B study (n=15):** +60% avg quality (49.5→79.3), 100% win rate, -32% variance

## Examples
- "Build a harness for deep research with web + academic + community angles" → Fan-out pattern
- "Design an agent team for full-stack website dev" → Pipeline (design→frontend→backend→QA)

## Integration Notes
- Requires: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
- 100 production harnesses: revfactory/harness-100 (10 domains, EN+KO)
- Neighbor: Archon (runtime configs), ECC (cross-harness standardization), wshobson/agents (parts catalog)
