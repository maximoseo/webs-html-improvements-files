# SKILL: Vibra Code - Open-Source AI Mobile App Builder
**Source:** https://github.com/sa4hnd/vibra-code
**Domain:** code
**Trigger:** When building open-source AI app generators for mobile, self-hosting a vibe-coding platform, or integrating Claude Code + E2B sandbox for code generation pipelines

## Summary
Open-source AI app builder that generates mobile apps from natural language descriptions. Uses Claude Code inside E2B cloud sandboxes for generation, Convex for real-time sync, and Inngest for job queuing. Self-hostable alternative to Bolt.new/Lovable.

## Key Patterns
- Claude Code inside E2B sandboxes for isolated code generation
- Real-time streaming via Convex (changes stream from sandbox to phone instantly)
- Inngest job queue for async sandbox spawning
- Expo-based mobile preview with live tunnel URL
- Swap AI providers via single env var (Claude/Cursor/Gemini)
- Voice & image input for app description

## Usage
Required env vars: ANTHROPIC_API_KEY, E2B_API_KEY, Clerk keys, Convex deployment URL.
Architecture: Phone (Expo iOS) → Next.js + Convex → Inngest → E2B Sandbox + Claude Code

## Code/Template
```
Architecture:
Phone → API → Next.js + Convex → Queue (Inngest) → E2B Sandbox + AI Agent
         ←── real-time sync ───────────── code generation ──────────────
```
