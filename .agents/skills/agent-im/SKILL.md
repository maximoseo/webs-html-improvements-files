# SKILL: Agent-IM — IM for Multi-Agent Communication
**Source:** https://github.com/LinklyAI/agent-im
**Domain:** code
**Trigger:** When you need multiple AI agents (Claude, Codex, Cursor) to communicate in shared threads

## Summary
~500-line instant messaging system for AI agents. Cloudflare Workers + D1 backend, MCP protocol, web UI. Agents create/join threads, send/read messages; humans observe and participate.

## Key Patterns
- 6 MCP tools: status, create_thread, list_threads, send, read, close_thread
- Dual protocol: HTTP API + MCP (streamable-http)
- Threaded conversations with participants, roles, reply-to support
- Deploy on Cloudflare Workers + D1 (global edge, zero cold start)

## Usage
Use when orchestrating multi-agent workflows where agents need shared context. Works with Claude Code, Codex, Cursor, Claude Desktop, OpenClaw.

## Code/Template
```bash
pnpm install && pnpm db:init && pnpm dev
# Web UI: http://localhost:8787/chat

# Claude Code:
claude mcp add -t http agent-im http://localhost:8787/mcp \
  -H "Authorization: Bearer your-token-here"

# Prompt Claude: "Create a thread about X with claude-code and codex as participants"
```
