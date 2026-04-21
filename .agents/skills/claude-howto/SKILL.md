# SKILL: Claude How To Guide
**Source:** https://github.com/luongnv89/claude-howto
**Domain:** code
**Trigger:** When learning or teaching Claude Code features — slash commands, memory, skills, hooks, MCP, subagents, plugins — with visual tutorials and copy-paste templates

## Summary
Structured, visual, example-driven guide to mastering Claude Code with Mermaid diagrams, production-ready copy-paste templates, and a 10-module learning path from beginner to advanced. 21,800+ stars.

## Key Patterns
- 10 modules: Slash Commands → Memory → Checkpoints → CLI → Skills → Hooks → MCP → Subagents → Advanced → Plugins
- `01-slash-commands/`, `02-memory/`, `03-skills/` — copy-paste template directories
- Self-assessment quiz via `/self-assessment` slash command in Claude Code
- Combines features: slash commands + memory + subagents + hooks = automated pipelines
- CLAUDE.md template, hook scripts, MCP configs, subagent definitions included

## Usage
```bash
git clone https://github.com/luongnv89/claude-howto.git
cd claude-howto
# Copy slash commands
cp 01-slash-commands/*.md .claude/commands/
# Copy memory template
cp 02-memory/project-CLAUDE.md ./CLAUDE.md
# Install a skill
cp -r 03-skills/code-review ~/.claude/skills/
```

## Code/Template
```bash
# Learning path order (11-13 hours total)
# 1. Slash Commands (30min) → 2. Memory (45min) → 3. Checkpoints
# → 4. CLI → 5. Skills (1hr) → 6. Hooks (1hr) → 7. MCP
# → 8. Subagents (1.5hr) → 9. Advanced → 10. Plugins
```
