# SKILL: Agent Kernel
**Source:** https://github.com/oguzbilgic/agent-kernel
**Domain:** code
**Trigger:** When creating a stateful AI agent that remembers between sessions using only markdown files and git — no database or framework required

## Summary
Agent Kernel is a minimal memory OS for AI agents using three markdown files and a git repo. The agent reads AGENTS.md (kernel), maintains IDENTITY.md and KNOWLEDGE.md, and appends daily session logs to `notes/`. Works with any coding agent (Claude Code, OpenCode, Codex, Cursor).

## Key Patterns
- `AGENTS.md` — kernel instructions (generic, ship with repo, don't edit)
- `IDENTITY.md` — who this agent is (agent maintains on first session)
- `KNOWLEDGE.md` — index of knowledge files (agent maintains)
- `knowledge/` — mutable facts about current state (agent updates)
- `notes/` — append-only daily session logs (never modified after day ends)
- Each agent = its own git repo; multiple agents = multiple repos

## Usage
```bash
git clone https://github.com/oguzbilgic/agent-kernel.git my-agent
cd my-agent
opencode     # or claude, codex, cursor, etc.
# Agent reads kernel, asks who you want it to be, remembers
```

## Code/Template
```
my-agent/
├── AGENTS.md          ← kernel (don't edit)
├── IDENTITY.md        ← who this agent is
├── KNOWLEDGE.md       ← index of knowledge files
├── knowledge/         ← current state facts (mutable)
└── notes/             ← session logs (append-only)
```
