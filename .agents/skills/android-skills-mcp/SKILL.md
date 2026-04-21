---
name: Android Skills MCP
source: https://github.com/skydoves/android-skills-mcp
category: Coding
purpose: Wraps Google android/skills library as MCP server + packager CLI — AI agents can discover and apply Android development skills without copy-paste, offline via npx
when_to_use: When developing Android apps with Jetpack Compose, needing Android-specific best practices, or setting up android/skills in any AI coding assistant
tags: [android, mcp-server, jetpack-compose, kotlin, edge-to-edge, android-skills]
---

# Android Skills MCP

## Purpose
2 tools that share a common parser and bundled snapshot of android/skills. MCP server for real-time discovery, packager CLI for committed rules files. Works offline through npx.

## When To Use
- Developing Android apps with Jetpack Compose
- Need edge-to-edge, r8-analyzer, or other android/skills in your AI assistant
- Want to commit android skill rules to your project repository
- Any MCP-capable client (Claude Code, Cursor, Codex CLI, Windsurf)

## How To Apply
**Install MCP server (Claude Code):**
```bash
claude mcp add android-skills -- npx -y android-skills-mcp
```

**Install as rules files:**
```bash
npx android-skills-pack install --target claude-code
npx android-skills-pack install --target cursor
npx android-skills-pack install --target all

# Filter to specific skill
npx android-skills-pack install --target cursor --skill edge-to-edge
```

**3 MCP tools:**
- `list_skills`: Show all available android skills
- `search_skills`: BM25 full-text search
- `get_skill`: Fetch specific skill content

**7 output targets:**
| Target | Output |
|--------|--------|
| claude-code | .claude/skills/<name>/SKILL.md |
| cursor | .cursor/rules/<name>.mdc |
| copilot | .github/instructions/<name>.instructions.md |
| gemini | .gemini/styleguide.md (concatenated) |
| junie | .junie/skills/<name>/SKILL.md |
| continue | .continue/rules/<name>.md |
| aider | CONVENTIONS.md (repo root) |

## Integration Notes
- Bundled snapshot loads <200ms — minimal session startup cost
- Tech: gray-matter (YAML frontmatter), zod (agentskills.io spec validation), minisearch (BM25)
- Not affiliated with Google — redistributes android/skills under Apache 2.0
- 64 tests across 3 packages (core, mcp, pack)
