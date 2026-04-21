# SKILL: KeyID Agent Kit — Free Email Infrastructure for AI Agents
**Source:** https://github.com/KeyID-AI/agent-kit
**Domain:** code
**Trigger:** When an AI agent needs a real email address to send, receive, and manage email autonomously

## Summary
27 email tools via MCP: provision free email addresses, send/receive/reply, manage contacts, set auto-reply, webhooks. No signup or API keys required — powered by KeyID.ai.

## Key Patterns
- Auto-generates Ed25519 keypair as identity (or bring your own)
- MCP protocol over stdio, compatible with Claude Desktop, Cursor, any MCP client
- Tools: keyid_provision, keyid_send, keyid_reply, keyid_get_inbox, keyid_create_webhook, etc.

## Usage
Add to MCP config in Claude Desktop or any MCP client for agents that need email capabilities.

## Code/Template
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "keyid": {
      "command": "npx",
      "args": ["@keyid/agent-kit"],
      "env": {
        "KEYID_PUBLIC_KEY": "...hex...",
        "KEYID_PRIVATE_KEY": "...hex..."
      }
    }
  }
}
```
```bash
npm install @keyid/agent-kit
npx @keyid/agent-kit   # auto-generates keypair if not set
```
