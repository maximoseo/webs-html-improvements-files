# SKILL: OpenRoom / VibeApps — Browser Desktop with AI Agent
**Source:** https://github.com/MiniMax-AI/OpenRoom
**Domain:** code
**Trigger:** When building AI-operated browser-based desktop apps or vibe-coding new apps via Claude Code

## Summary
Browser-based desktop (macOS-inspired) with a built-in AI agent that operates apps via natural language. Vibe Workflow generates full apps from descriptions using Claude Code CLI in 6 stages.

## Key Patterns
- AI Agent operates built-in apps (Music, Chess, Email, Diary, etc.) via Action system
- /vibe command generates new React+TypeScript apps: Requirement → Architecture → Tasks → Code → Assets → Integration
- Everything runs locally in browser (IndexedDB), no backend needed
- Evolve existing apps: `/vibe AppName Add feature X`

## Usage
Use the /vibe workflow in Claude Code to generate fully-integrated browser apps from natural language descriptions.

## Code/Template
```bash
git clone https://github.com/MiniMax-AI/OpenRoom.git && cd OpenRoom
pnpm install && pnpm dev    # http://localhost:3000

# In Claude Code CLI (NOT browser chat):
/vibe WeatherApp Create a weather dashboard with 5-day forecasts
/vibe MusicApp Add a lyrics panel that shows synced lyrics
/vibe MyApp --from=04-codegen    # resume from stage
```
