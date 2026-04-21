# SKILL: Claude Replay
**Source:** https://github.com/es617/claude-replay
**Domain:** code
**Trigger:** When sharing AI coding sessions as interactive HTML replays, documenting AI-assisted development, or monitoring live agent sessions

## Summary
Converts Claude Code, Cursor, Codex CLI, Gemini CLI, and OpenCode session logs into self-contained interactive HTML replays with playback controls, bookmarks, secret redaction, and live watch mode.

## Key Patterns
- Auto-detects session format from multiple editors
- Output is a single self-contained HTML file (no external deps) — email or host anywhere
- Session locations: `~/.claude/projects/`, `~/.cursor/projects/`, `~/.codex/sessions/`, `~/.gemini/tmp/`
- `--serve --watch` for real-time monitoring of running agent sessions
- Secret redaction before export
- Collapse/expand tool calls and Claude thinking blocks
- File activity sidebar — which files were touched, navigate to tool calls
- Embeddable via iframe
- Pass session ID or full path; auto-searches all known locations
- Docker image available for server/container use

## Usage
Install: `npm install -g claude-replay`. Run with no args for web editor UI. Generate: `claude-replay <session-id> -o replay.html`. Chain sessions: `claude-replay id1 id2 -o combined.html`.

## Code/Template
```bash
# Install
npm install -g claude-replay

# Auto-discover and generate replay
claude-replay abc123def456 -o replay.html

# Live monitoring
claude-replay ~/.claude/projects/myproject/ --serve --watch

# Docker (web editor)
docker run --rm -p 7331:7331 \
  -v ~/.claude/projects:/root/.claude/projects:ro \
  ghcr.io/es617/claude-replay

# Chain multiple sessions
claude-replay session1 session2 -o combined.html
```
