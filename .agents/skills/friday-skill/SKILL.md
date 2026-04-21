---
name: Friday (24/7 Autonomous AI Assistant)
source: https://github.com/missingus3r/friday-showcase
category: Automation
purpose: Always-on personal AI system on Claude Code $100/month — Telegram communication, 18 cron jobs, self-evolving skills, memory graph, Notion integration
when_to_use: When building or running a 24/7 autonomous AI assistant that self-improves over time
tags: [autonomous, ai-assistant, telegram, memory, cron, self-evolving, claude-code]
---
# Friday Autonomous Assistant

## Purpose
24/7 AI assistant powered by Claude Code CLI + Telegram + Flask/SQLite memory. Self-evolves through skill acquisition, daily reflection, preference learning, and world modeling.

## Architecture
```
User (Telegram) → Claude Code (MCP plugins)
    ├── Memory API (Flask + SQLite + Embeddings)
    ├── Self-Evolving (Skills, Reflections, Preferences, World Model, Proposals)
    ├── Knowledge Base (Notion MCP)
    ├── GitHub (repos, commits, PRs)
    ├── Voice (ElevenLabs TTS/STT)
    ├── Email (AgentMail MCP)
    ├── Web Search/Fetch
    ├── Cron System (18 scheduled jobs)
    └── Local tools (shell, scripts)
```

## 18 Cron Jobs Include
- Daily briefing (weather, forex, AI news, movies)
- AI Model Monitor (HuggingFace, blogs, AGI forecast)
- Self-reflection (12h: what went well/wrong)
- Preference learning (daily: infer rules from corrections)
- Skill promotion (draft→beta→stable)
- Auto-audit (3x/day: integrity scan)
- Memory decay (weekly: confidence half-life)

## Self-Evolving Systems
1. **Skill Acquisition** — extracts reusable patterns from solved tasks
2. **Daily Self-Reflection** — reviews logs, stores insights
3. **Preference Learning** — infers rules from repeated feedback
4. **World Model** — behavioral model with confidence scores
5. **Self-Improvement Proposals** — formal proposals, user approves

## Cost
$100/month Anthropic Max Plan — no additional infrastructure.

## Setup
```
Read the file ~/Downloads/SETUP.md and follow every step
```
Claude Code reads and walks through setup autonomously.

## Integration Notes
- v2 (April 2026): cognition harness — 13 new SQLite tables, 70+ new API endpoints, 8 new crons
- Disaster recovery: `/backup/export` → rsync nightly → `/backup/import` on new machine
- Memory: Flask + SQLite + embeddings (no vector DB, no Redis)
- Named after Tony Stark's last AI assistant
