# SKILL: GitAgentProtocol (Open GAP)
**Source:** https://github.com/open-gitagent/gitagent
**Domain:** code
**Trigger:** When defining AI agents as portable, git-native, framework-agnostic artifacts — versioned, forkable, compliance-ready, and exportable to any framework

## Summary
GitAgentProtocol (GAP) is a standard where a git repo IS the agent definition. Drop agent.yaml + SOUL.md into any repo and it becomes a portable agent that exports to Claude Code, LangChain, CrewAI, AutoGen, etc. Includes compliance (FINRA, SEC), SOD, live memory, versioning, and CI/CD patterns.

## Key Patterns
- Required files: `agent.yaml` (manifest) + `SOUL.md` (identity)
- Optional: `RULES.md`, `DUTIES.md`, `skills/`, `tools/` (MCP YAML), `workflows/`, `knowledge/`, `memory/runtime/`, `hooks/`, `compliance/`, `agents/` (sub-agents)
- `gapman validate` — validate agent structure in CI
- Human-in-the-loop: new skills → branch+PR for human review before merge
- SOD: define roles (maker/checker/executor/auditor), conflicts, handoffs in agent.yaml
- `memory/runtime/dailylog.md`, `context.md` — persistent cross-session state

## Usage
```bash
npm install -g gapman
gapman init my-agent        # scaffold agent structure
gapman validate             # check agent.yaml + structure
gapman export --format langchain  # export to framework
```

## Code/Template
```yaml
# agent.yaml minimal
name: my-agent
version: "1.0.0"
model: claude-opus-4-5
skills:
  - code-review
compliance:
  segregation_of_duties:
    roles:
      - id: maker
        permissions: [create, submit]
      - id: checker
        permissions: [review, approve]
    conflicts: [[maker, checker]]
```
