# SKILL: Clicky
**Source:** https://github.com/farzaa/clicky
**Domain:** code
**Trigger:** When building an AI screen-aware assistant on macOS that can see your screen, talk, and point at UI elements

## Summary
An open-source macOS menu bar app where an AI (Claude) acts as a teacher/buddy that can see your screen, hear your voice (push-to-talk), and point at specific UI elements using cursor overlays. Built with Swift + Cloudflare Worker proxy.

## Key Patterns
- Push-to-talk: Control+Option hotkey streams audio via WebSocket to AssemblyAI
- Screenshot sent with transcript to Claude via streaming SSE
- Claude embeds `[POINT:x,y:label:screenN]` to fly cursor to UI elements (multi-monitor)
- All API keys proxied through Cloudflare Worker (never in app binary)
- Menu bar app (no dock icon) with two NSPanel windows
- Requires: Screen Recording, Accessibility, Microphone permissions
- Cloudflare Worker has 3 routes: `/chat` (Claude SSE), `/tts` (ElevenLabs), `/transcribe-token` (AssemblyAI)
- Architecture in `CLAUDE.md` for agent-assisted development

## Usage
Clone, deploy Cloudflare Worker with API keys (Anthropic, AssemblyAI, ElevenLabs), update proxy URLs in Swift code, open in Xcode, build and run. Claude Code can handle full setup via CLAUDE.md.

## Code/Template
```bash
# Set up Cloudflare Worker
cd worker && npm install
npx wrangler secret put ANTHROPIC_API_KEY
npx wrangler secret put ASSEMBLYAI_API_KEY
npx wrangler secret put ELEVENLABS_API_KEY
npx wrangler deploy

# Find and replace proxy URLs in Swift
grep -r "clicky-proxy" leanring-buddy/
# Replace with your worker URL

# Build in Xcode
open leanring-buddy.xcodeproj  # Cmd+R to build
```
