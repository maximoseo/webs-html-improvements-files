# SKILL: Mails
**Source:** https://github.com/chekusu/mails
**Domain:** code
**Trigger:** When AI agents need to send/receive emails, wait for verification codes, or search an inbox programmatically

## Summary
Email infrastructure for AI agents: send via Resend, receive via Cloudflare Email Routing, search inbox with full-text search, and auto-extract verification codes. Supports hosted (@mails.dev) and self-hosted Cloudflare Worker deployments.

## Key Patterns
- `mails claim <name>` — claim free @mails.dev mailbox
- `mails send --to email --subject "..." --body "..."` — send with optional attachments
- `mails inbox --query "keyword"` — full-text search with relevance ranking
- `mails code --to agent@mails.dev` — wait and extract verification codes (stdout for piping)
- Advanced filters: `--has-attachments`, `--from domain.com`, `--since date`
- `mails sync` — pull remote emails to local SQLite for offline/backup
- SDK: `send()`, `getInbox()`, `searchInbox()`, `waitForCode()` — zero runtime deps (raw fetch)
- Self-hosted via Cloudflare Worker + D1 database

## Usage
Install globally: `npm install -g mails`. Claim a mailbox: `mails claim myagent`. Use `mails code` to extract OTPs/verification codes. Pipe code to scripts: `CODE=$(mails code --to agent@mails.dev)`.

## Code/Template
```typescript
import { send, waitForCode, searchInbox } from 'mails'
await send({ to: 'user@example.com', subject: 'Hello', text: 'World' })
const code = await waitForCode('agent@mails.dev', { timeout: 30 })
if (code) console.log(code.code) // "123456"
const results = await searchInbox('agent@mails.dev', { query: 'invoice' })
```
