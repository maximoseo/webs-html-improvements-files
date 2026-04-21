# SKILL: Wormhole — Open-Source ngrok Alternative
**Source:** https://github.com/MuhammadHananAsghar/wormhole
**Domain:** developer-tools
**Trigger:** Use when exposing a local server to the internet instantly, sharing localhost URLs with clients/teammates, testing webhooks locally, or replacing ngrok without signup.

## Summary
Wormhole is a zero-config, open-source ngrok alternative that gives local servers a public HTTPS URL. One command, HTTPS by default via Cloudflare, built-in traffic inspector at localhost:4040, request replay, HAR export, WebSocket support, auto-reconnect.

## Key Patterns
- `wormhole http 3000` → public HTTPS URL instantly
- Custom subdomains: `wormhole http 3000 --subdomain myapp` (free with GitHub login)
- Traffic inspector at `http://localhost:4040` with live request stream
- Request replay: re-send any captured request with one click
- HAR export for traffic analysis
- Auto-reconnect with exponential backoff
- No signup required for basic tunnels

## Usage
When user needs to share localhost URL, test webhooks, demo to clients, or debug incoming requests. Zero config alternative to ngrok/localtunnel.

## Code/Template
```bash
# Install
curl -fsSL https://wormhole.bar/install.sh | sh
# or: brew install MuhammadHananAsghar/tap/wormhole

# Expose port 3000
wormhole http 3000

# Custom subdomain
wormhole http 3000 --subdomain myapp
# → https://myapp.wormhole.bar

# View traffic inspector
open http://localhost:4040
```
