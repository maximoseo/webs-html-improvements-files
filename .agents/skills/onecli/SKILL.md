# SKILL: OneCLI (Secret Vault for AI Agents)
**Source:** https://github.com/onecli/onecli
**Domain:** code
**Trigger:** When AI agents need to call external APIs without seeing the real credentials — centralizing secret management across multiple agents

## Summary
OneCLI is an open-source gateway that sits between AI agents and the APIs they call. Agents use placeholder keys; the Rust gateway intercepts requests, matches them by host/path patterns, and swaps in real AES-256-GCM encrypted credentials. Agents never see secrets.

## Key Patterns
- Agents authenticate with access tokens via `Proxy-Authorization` headers
- Secrets matched by host + path patterns; decrypted only at request time
- Rust gateway for fast, memory-safe HTTPS MITM interception
- Multi-agent: each agent gets scoped access token with limited permissions
- Two auth modes: single-user (no login) or Google OAuth (teams)
- Vault integration: connect Bitwarden or other password managers for on-demand injection

## Usage
```bash
curl -fsSL https://onecli.sh/install | sh
# Or:
docker compose -f docker/docker-compose.yml up -d --wait
# Dashboard: http://localhost:10254
# Gateway: http://localhost:10255
```

## Code/Template
```bash
# Agent config: point HTTP gateway to localhost:10255
# Agent uses: Authorization: Bearer FAKE_KEY
# OneCLI swaps FAKE_KEY → REAL_KEY before forwarding to API
```
