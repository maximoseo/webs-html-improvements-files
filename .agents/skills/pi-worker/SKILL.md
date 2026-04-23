# SKILL: Pi Coding Agent on Cloudflare Workers
**Source:** https://github.com/qaml-ai/pi-worker
**Domain:** code
**Trigger:** When running AI coding agents on Cloudflare Workers, building edge-deployed agent infrastructure, or creating browser-terminal AI interfaces

## Summary
Monorepo for running pi-style coding agents on Cloudflare Workers with persistent SQLite-backed Durable Object sessions, dynamic worker sandboxes, and browser terminal UI. Enables serverless edge-deployed AI agent infrastructure.

## Key Patterns
- Durable Object session store (SQLite-backed persistent files)
- Dynamic Worker sandboxes for isolated code execution
- Browser terminal UI backed by edge workers
- Durable Object alarm-powered cron jobs for agent scheduling
- Publish session-scoped Workers from within agent sessions

## Usage
Clone repo, `npm install` from root, then `cd examples/terminal-agent && npm run dev`. Key packages: `pi-worker` (core primitives), `pi-coding-agent-worker` (Claude agent), `pi-tui-worker` (terminal UI).

## Code/Template
```typescript
// packages/pi-worker - core worker helpers
// examples/terminal-agent - full browser terminal agent
// Architecture: Browser → Durable Object session → Dynamic Worker sandboxes
```
