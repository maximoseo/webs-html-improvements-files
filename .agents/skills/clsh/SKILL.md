# SKILL: clsh (Terminal Access from Phone)
**Source:** https://github.com/my-claude-utils/clsh
**Domain:** code
**Trigger:** When needing real terminal access to a Mac from a mobile device — to run Claude Code, manage sessions, or control the machine remotely via a secure tunnel

## Summary
clsh provides real PTY terminal access to your Mac from any browser/phone via a secure tunnel (ngrok/SSH/WiFi). Supports multiple concurrent sessions, tmux persistence, custom keyboard skins, PWA install, and Claude Code streaming.

## Key Patterns
- Real PTY via node-pty, not a simulation; sessions survive restarts via tmux
- 3-tier tunnel: ngrok (static URL) → localhost.run SSH (zero signup) → WiFi fallback
- Security: one-time bootstrap tokens, scrypt password hashing, WebAuthn Face ID, rate limiting
- Custom keyboard with sticky modifiers, key repeat, 6 skins
- Up to 8 concurrent terminal sessions with live grid preview
- PWA installable for fullscreen iOS experience

## Usage
```bash
npx clsh-dev          # zero-config, SSH tunnel, QR code
npx clsh-dev setup    # permanent ngrok URL (requires ngrok account)
TUNNEL=ssh npx clsh-dev   # force SSH tunnel
```

## Code/Template
```bash
# Permanent URL setup with ngrok
brew install ngrok
ngrok config add-authtoken YOUR_TOKEN
# Add to .env:
# NGROK_AUTHTOKEN=your_token
# NGROK_STATIC_DOMAIN=your-subdomain.ngrok-free.dev
npx clsh-dev
```
