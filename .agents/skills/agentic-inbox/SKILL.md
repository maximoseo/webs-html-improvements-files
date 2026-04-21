# SKILL: Agentic Inbox
**Source:** https://github.com/cloudflare/agentic-inbox
**Domain:** code
**Trigger:** When building a self-hosted AI email client on Cloudflare, or integrating email capabilities into AI agents via MCP

## Summary
A self-hosted email client with AI agent built entirely on Cloudflare Workers. Each mailbox runs in its own Durable Object with SQLite storage, attachments in R2, and a built-in AI agent with 9 email tools for reading/searching/drafting/sending.

## Key Patterns
- Per-mailbox isolation via Durable Objects with SQLite
- AI agent auto-drafts replies on inbound emails (requires explicit confirmation to send)
- MCP server at `/mcp` for external AI tools (Claude Code, Cursor) to operate on mailboxes
- Cloudflare Access JWT validation as security boundary
- Stack: React 19, Hono, Cloudflare Workers, AIChatAgent (Agents SDK), Workers AI (kimi-k2.5)
- Email receive via Cloudflare Email Routing catch-all → Worker
- Email send via Email Service binding (`send_email`)

## Usage
Deploy via "Deploy to Cloudflare" button. Configure Cloudflare Access for authentication. Set up Email Routing catch-all rule. Enable Email Service binding for sending. Connect external AI tools via MCP endpoint at `/mcp` with `mailboxId` param.

## Code/Template
```bash
npm install && npm run dev   # local dev
npm run deploy               # production deploy

# Architecture:
# Browser → Hono Worker → MailboxDO (SQLite+R2)
#                       → EmailAgent DO (AIChatAgent, 9 tools, Workers AI)
# Auth: Cloudflare Access JWT (required in production)
```
