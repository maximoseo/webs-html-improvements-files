# SKILL: Symphony (OpenAI Agent Orchestration)
**Source:** https://github.com/openai/symphony
**Domain:** code
**Trigger:** When orchestrating coding agents autonomously from an issue tracker (Linear) — scheduling work, isolating per-issue workspaces, and managing concurrent agent runs without manual supervision

## Summary
Symphony is an OpenAI engineering preview that reads a Linear board, spawns isolated coding agents per issue, and manages retries, concurrency, and observability. Teams manage work (issues) instead of supervising individual agents. Agents land PRs and provide proof of work: CI status, walkthroughs, complexity analysis.

## Key Patterns
- Polls Linear on fixed cadence; dispatches to bounded concurrent agent pool
- Per-issue workspace isolation — agent commands run only inside workspace dirs
- `WORKFLOW.md` in repo defines agent prompt template + runtime settings (versioned with code)
- Components: Workflow Loader, Config Layer, Issue Tracker Client, Orchestrator, Workspace Manager, Agent Runner
- Handoff states: agent delivers to "Human Review" state, not necessarily "Done"
- Recovery: exponential backoff, restart recovery without persistent DB
- Language-agnostic spec: implement in any language via SPEC.md

## Usage
```
# Option 1: Tell your agent to build it
"Implement Symphony according to SPEC.md"

# Option 2: Use reference Elixir implementation
see elixir/README.md
```

## Code/Template
```markdown
# WORKFLOW.md front matter (YAML)
---
concurrency: 3
linear_team: "ENG"
eligible_states: ["Todo", "In Progress"]
handoff_state: "Human Review"
agent: codex
---
# Agent prompt template
You are working on {{issue.title}}.
Context: {{issue.description}}
```
