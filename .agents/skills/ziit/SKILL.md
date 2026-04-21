# SKILL: Ziit — Code Time Tracking
**Source:** https://github.com/0PandaDEV/Ziit
**Domain:** developer-tools
**Trigger:** Use when setting up self-hosted code time tracking, WakaTime alternative, coding statistics dashboard, or embedding coding-time badges in READMEs.

## Summary
Ziit is an open-source, self-hostable alternative to WakaTime that tracks coding activity (projects, languages, editors, files, branches, OS, time) and displays clean stats. Supports VS Code, JetBrains, GitHub/Email login, WakaTime import, and public leaderboard.

## Key Patterns
- Self-host with Bun + TimescaleDB (Docker or manual)
- Install IDE extension (VS Code, JetBrains) → points to your instance
- Embed coding-time badge: `https://<instance>/api/public/badge/<id>/<project>`
- Import existing data from WakaTime or WakAPI
- Public stats page + community leaderboard at `/leaderboard`

## Usage
When a user wants to track coding time privately, embed progress badges in repos, or replace WakaTime with a self-hosted solution. Guide them to deploy an instance then install the IDE extension.

## Code/Template
```bash
# Setup
bun i
bunx prisma migrate dev
cp .env.example .env
bun dev   # http://localhost:3000

# Badge embed in README
![coding time](https://ziit.app/api/public/badge/<project-id>/<project-name>)
```
