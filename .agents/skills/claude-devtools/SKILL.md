# SKILL: claude-devtools
**Source:** https://github.com/matt1398/claude-devtools
**Domain:** code
**Trigger:** When debugging Claude Code sessions — inspecting tool calls, token usage per turn, subagent trees, extended thinking, or file diffs that are hidden in the Claude Code terminal

## Summary
claude-devtools reads Claude Code session logs from `~/.claude/` and reconstructs everything hidden by Claude Code's opaque summaries: exact file paths, diffs, tool call I/O, thinking steps, per-turn token attribution (7 categories), and subagent execution trees. Zero config, no API key.

## Key Patterns
- Reads `~/.claude/` session logs directly — no wrapper, no interference
- Per-turn token attribution: CLAUDE.md, skills, @-mentioned files, tool I/O, thinking, team overhead, user text
- Subagent execution trees with tool traces, token metrics, duration, cost
- Tool call inspector: syntax-highlighted reads, inline diffs, bash output
- Compaction visualization showing when context fills/compresses/refills
- Notification triggers: .env access, tool errors, high token usage, custom regex
- SSH remote sessions, multi-pane layout, Cmd+K cross-session search
- Docker deployment for server/headless use

## Usage
```bash
brew install --cask claude-devtools     # macOS
# Or download from GitHub Releases for Linux/Windows
# Docker:
docker compose up && open http://localhost:3456
```

## Code/Template
```bash
# Docker deployment (server mode)
docker run -p 3456:3456 -v ~/.claude:/data/.claude:ro claude-devtools
```
