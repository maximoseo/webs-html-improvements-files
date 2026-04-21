# SKILL: ez - Agent-First Version Control with Stacked PRs
**Source:** https://github.com/rohoswagger/ez-stack
**Domain:** code
**Trigger:** When managing git workflows for AI coding agents, implementing stacked PRs, or enabling multiple agents to work on the same repo without conflicts

## Summary
Agent-first version control CLI that makes git invisible for AI coding agents. Four commands cover the full lifecycle: worktree isolation per agent, stacked PRs, auto-restacking, and structured JSON output for agent verification.

## Key Patterns
- Worktree isolation: each `ez create` gives agent its own worktree (no merge conflicts)
- Stacked PR workflow: automatic base management and restacking after merges
- Scope Guard: restrict agent file access to defined glob patterns
- JSON output and mutation receipts for agent verification
- Worktree hooks: markdown instructions in .ez/hooks/post-create/ for agent setup

## Usage
```bash
pip install ez-stack && ez setup --yes && ez init
ez create feat/auth          # Start: worktree + branch + cd
ez push -am "feat: add auth" # Ship: stage + commit + push + PR
ez sync --autostash          # Sync: pull trunk, clean merged, restack
ez delete feat/auth --yes    # Done: remove worktree + branch
ez list                      # Dashboard: PRs, CI, age, ports, state
```

## Code/Template
```bash
# Multi-agent workflow (no conflicts)
ez create feat/auth --from main  # Agent 1
ez create feat/api --from main   # Agent 2
# Each agent works in .worktrees/<branch>/

# Scope guard for focused agents
ez create feat/auth --scope 'src/auth/**' --scope 'tests/auth/**'
ez scope set --mode strict 'src/auth/**'
```
