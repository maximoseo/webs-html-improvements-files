# SKILL: Lil Agents - macOS Dock AI Companions
**Source:** https://github.com/ryanstephen/lil-agents
**Domain:** code
**Trigger:** When building macOS desktop AI integrations, creating dock-resident AI assistants, or building multi-CLI AI launcher apps for macOS

## Summary
macOS app providing animated dock companions (Bruce and Jazz) that open AI terminals for Claude Code, OpenAI Codex, GitHub Copilot, and Google Gemini CLIs. Click to chat with AI in themed popovers with four visual themes and slash commands.

## Key Patterns
- Animated HEVC transparent video for dock characters
- Multi-CLI support: Claude Code, Codex, Copilot, Gemini (switchable from menubar)
- Slash commands: /clear, /copy, /help in chat input
- Auto-updates via Sparkle, universal binary (Apple Silicon + Intel)
- No data transmission: runs entirely on device

## Usage
Download from https://lilagents.xyz or build via Xcode from `lil-agents.xcodeproj`. Requires macOS Sonoma 14.0+ and at least one supported CLI installed.

## Code/Template
Requirements:
- Claude Code: `curl -fsSL https://claude.ai/install.sh | sh`
- Codex: `npm install -g @openai/codex`
- Copilot: `brew install copilot-cli`
- Gemini: `npm install -g @google/gemini-cli`
