# SKILL: CLI-Anything — Make Any Software Agent-Native
**Source:** https://github.com/HKUDS/CLI-Anything
**Domain:** code
**Trigger:** When you want to make any desktop app or software controllable by an AI agent via a CLI harness

## Summary
Framework for generating CLI harnesses that make any software agent-native. Community hub of 100+ CLIs for apps like Blender, Godot, Obsidian, n8n, Exa, and more. Each CLI standardizes discovery, invocation, and structured output.

## Key Patterns
- Each CLI harness has a SKILL.md, unit tests, and E2E tests
- `cli-hub install <name>` to install any community CLI
- Output is JSON + human-readable for both agent and human consumption
- HARNESS.md defines the spec for building new harnesses

## Usage
Use to give AI agents access to any software. Install existing harnesses from CLI-Hub or generate new ones following HARNESS.md.

## Code/Template
```bash
pip install cli-anything-hub
cli-hub install obsidian    # install Obsidian CLI harness
cli-hub install blender     # install Blender CLI harness
cli-hub install godot       # install Godot CLI harness

# In Claude Code / any agent:
# "Use the blender CLI to render scene.blend at 1080p"

# npx skills add HKUDS/CLI-Anything --skill <skill-name> -g -y
```
