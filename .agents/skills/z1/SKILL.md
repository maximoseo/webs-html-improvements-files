# SKILL: Z1 - MCP Proxy for Claude Code to Control React Apps
**Source:** https://github.com/thomscoder/z1
**Domain:** code
**Trigger:** When testing React app error states, loading states, or UI behavior via Claude Code; when intercepting/mocking HTTP requests for AI-driven testing; or building MCP tools for browser control

## Summary
Local dev proxy that lets Claude Code observe and control a React app with zero code changes. Intercepts HTTP requests, exposes the live React fiber tree, and provides MCP tools for Claude to delay/drop/mock requests and control the browser DOM.

## Key Patterns
- Proxy sits between browser and dev server, injects client bundle automatically
- MCP tools: z1_observe, z1_inject, z1_clear, z1_rules, z1_components, z1_query, z1_fill, z1_click, z1_navigate, z1_reload
- Rules engine: delay, respond, drop, throttle (longest match wins)
- React fiber tree access without reading source code
- Auto-writes .mcp.json to project for Claude Code auto-detection
- Session token auth on WebSocket control plane

## Usage
```bash
# Two terminal setup
bun run /path/to/z1/cli.ts proxy localhost:<PORT> --spawn "bun dev"
claude  # Auto-detects .mcp.json
# Open http://localhost:4000
```

## Code/Template
```
# Claude Code interaction example:
"delay GET /api/users by 3 seconds, check if loading state renders correctly"
→ z1_inject({ match: "GET /api/users", action: "delay", params: { ms: 3000 } })
→ z1_observe({ path: "/api/users" })  # sees durationMs: 3042
→ z1_eval({ code: "document.querySelector('.skeleton') !== null" })  # true
→ z1_clear()  # remove rule
```
