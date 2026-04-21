---
name: SkillClaw (Collective Skill Evolution)
source: https://github.com/AMAP-ML/SkillClaw
category: Agent Skills
purpose: Collective skill evolution system — skills that improve autonomously from real interactions across sessions, teams, and users
when_to_use: When building a long-running skill system that should get better over time through use, without manual updates
tags: [skill-evolution, collective-intelligence, meta-skill, autonomous, improvement]
---
# SkillClaw — Collective Skill Evolution

## Purpose
A system for skills that evolve: each interaction can improve the skill for future uses. Collective intelligence for agent skill networks.

## Core Concept
Traditional skills are static. SkillClaw skills can:
1. Track which patterns worked/failed across sessions
2. Synthesize improvements from repeated edge cases
3. Promote draft patterns to stable skills automatically
4. Share improvements across users/teams

## Evolution Lifecycle
```
Discovery → Draft (per-session) → Beta (repeated across sessions) → Stable (vetted)
                                     ↓
                              Merge conflicts → Human review → Merge or discard
```

## How To Apply
1. Install SkillClaw monitoring alongside existing skills
2. Enable pattern collection: `SKILLCLAW_COLLECT=true`
3. After N sessions, run evolution pass: `skillclaw evolve`
4. Review proposed skill improvements
5. Accept/reject → apply to canonical SKILL.md

## Key Features
- **Anti-regression guard** — evolution never removes working patterns
- **Conflict resolution** — flags contradictory patterns for human review
- **Confidence scoring** — patterns need N confirmations before promotion
- **Rollback** — every evolution is versioned, one-command rollback

## Integration Notes
- Complementary to any existing skill system
- Pairs with `friday-skill` (preference learning uses similar mechanism)
- Best deployed in team contexts where multiple sessions share skill state
- AMAP-ML (Ant Group) internal tooling — community edition available
