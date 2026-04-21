# SKILL: Harness - Team Architecture Factory for Claude Code
**Source:** https://github.com/revfactory/harness
**Domain:** code
**Trigger:** When designing multi-agent team architectures, generating agent definitions and skills for a project domain, or orchestrating specialized agent teams

## Summary
A Claude Code plugin that converts a domain description into a full multi-agent team architecture. Say "build a harness for this project" and it generates .claude/agents/ and .claude/skills/ tailored to your domain using one of 6 pre-defined team patterns.

## Key Patterns
- 6 architectural patterns: Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical Delegation
- Auto-generates agent definitions (.claude/agents/) and skills (.claude/skills/)
- Progressive Disclosure skill generation for efficient context management
- Harness Evolution Mechanism: feeds deltas back to improve next generation
- Trigger: "build a harness for this project" / "하네스 구성해줘" / "ハーネスを構成して"

## Usage
Install via `/plugin install harness@harness` or copy `skills/harness` to `~/.claude/skills/harness`. Then say "build a harness for this project" with a domain description.

## Code/Template
```
Workflow:
Phase 1: Domain Analysis
Phase 2: Team Architecture Design
Phase 3: Agent Definition Generation (.claude/agents/)
Phase 4: Skill Generation (.claude/skills/)
Phase 5: Integration & Orchestration
Phase 6: Validation & Testing
```
