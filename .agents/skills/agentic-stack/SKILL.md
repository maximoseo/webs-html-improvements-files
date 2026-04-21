# SKILL: Agentic Stack
**Source:** https://github.com/codejunkie99/agentic-stack
**Domain:** code
**Trigger:** When setting up persistent memory and skills for AI coding agents across Claude Code, Cursor, Windsurf, OpenCode, or other harnesses

## Summary
A portable `.agent/` folder (memory + skills + protocols) that plugs into 8+ AI coding agent harnesses and persists knowledge across tool switches. Features layered memory, a review protocol for graduated lessons, and cross-harness recall.

## Key Patterns
- 4 memory layers: `working/`, `episodic/`, `semantic/`, `personal/`
- `auto_dream.py` nightly cycle stages candidate lessons for human review
- Review CLI: `graduate.py <id>`, `reject.py <id>`, `reopen.py <id>` — all require rationale
- `learn.py` — teach agent a rule in one command, idempotent
- `recall.py` — surface relevant graduated lessons before starting a task
- `show.py` — dashboard of brain state (episodes, candidates, lessons, activity)
- Progressive skill disclosure: lightweight manifest loads always, full SKILL.md only on trigger match
- Adapters for: claude-code, cursor, windsurf, opencode, openclaw, hermes, pi, standalone-python
- Onboarding wizard populates PREFERENCES.md (preferences, test strategy, commit style)

## Usage
Install: `brew tap codejunkie99/agentic-stack && brew install agentic-stack`. Run `agentic-stack claude-code` in project directory. Windows: `.\install.ps1 claude-code`. Reconfigure with `--reconfigure` flag.

## Code/Template
```bash
# Install and initialize
agentic-stack claude-code               # runs onboarding wizard
agentic-stack claude-code --yes         # accept all defaults (CI)
agentic-stack claude-code --reconfigure # re-run wizard

# Host-agent CLI tools
python3 .agent/tools/learn.py "Always UTC timestamps" --rationale "cross-region bugs"
python3 .agent/tools/recall.py "add created_at column"
python3 .agent/tools/show.py
```
