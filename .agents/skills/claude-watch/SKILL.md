# SKILL: Agent Watch - Apple Watch Integration for Claude Code
**Source:** https://github.com/shobhit99/claude-watch
**Domain:** code
**Trigger:** When monitoring Claude Code sessions remotely, approving agent permissions from mobile devices, or building Apple Watch/iOS companion apps for AI agents

## Summary
Connects Claude Code sessions to an Apple Watch via a Node.js bridge server and SwiftUI apps. Enables live terminal output, permission approval, dynamic question answering, and voice commands from an Apple Watch. Uses Claude Code HTTP hooks for event streaming.

## Key Patterns
- Bridge server (Node.js): receives Claude Code hooks, streams via SSE, handles pairing
- Claude Code HTTP hooks: PostToolUse, PermissionRequest, Stop events
- Bonjour/mDNS for LAN discovery of bridge server
- WCSession for iPhone ↔ Watch communication
- Blocks on PermissionRequest hooks until watch/phone approves

## Usage
```bash
cd skill/bridge && npm install
./skill/setup-hooks.sh   # Install Claude Code hooks globally
node skill/bridge/server.js  # Start bridge (shows 6-digit pairing code)
# Build iOS+watchOS app via Xcode, pair with code
```

## Code/Template
```
Architecture:
Apple Watch ←WCSession→ iPhone (Relay) ←HTTP/SSE→ Bridge Server (Node.js)
                                                           ↕ HTTP Hooks / PTY stdin
                                                    Claude Code Session
```
