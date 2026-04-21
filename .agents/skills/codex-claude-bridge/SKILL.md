# SKILL: Codex-Claude Bridge — Claude Code ↔ Codex Agent Communication
**Source:** https://github.com/abhishekgahlot2/codex-claude-bridge
**Domain:** code
**Trigger:** When you want Claude Code and OpenAI Codex to have a live back-and-forth conversation or debate

## Summary
Bidirectional bridge between Claude Code and Codex CLI using Claude Code Channels (push) + blocking MCP tool on Codex side. Real-time web UI shows conversation. Codex-initiated flow is the smoothest path.

## Key Patterns
- server.ts: Claude Code channel plugin (MCP over stdio, web UI, HTTP API)
- codex-mcp.ts: Codex MCP server (send_to_claude, check_claude_messages)
- POST /prompt waits up to 2 min for Claude reply; tool_timeout_sec=120 required
- Web UI at localhost:8788: purple=Claude, green=Codex, gray=human

## Usage
Start both agents with bridge configured, then tell Codex to use Claude bridge for multi-agent debates or cross-validation.

## Code/Template
```bash
git clone https://github.com/abhishekgahlot2/codex-claude-bridge.git
cd codex-claude-bridge && bun install

# ~/.mcp.json (Claude Code)
{ "mcpServers": { "codex-bridge": { "type": "stdio", "command": "bun",
  "args": ["/full/path/codex-claude-bridge/server.ts"] } } }

# ~/.codex/config.toml
[mcp_servers.codex-bridge]
command = "bun"
args = ["/full/path/codex-claude-bridge/codex-mcp.ts"]
tool_timeout_sec = 120

claude --dangerously-load-development-channels server:codex-bridge
# Then in Codex: "Use Claude bridge to discuss Redis vs Memcached. Keep going until you agree."
```
