---
name: Friday Autonomous AI Assistant
source: https://github.com/missingus3r/friday-showcase
category: Agent Skills
purpose: 24/7 autonomous AI assistant system running on Claude Code + Telegram with self-evolving skills, persistent memory, 18 cron jobs, and a complete cognition harness
when_to_use: When building a persistent always-on AI assistant with Telegram interface, scheduled briefings, self-improvement, and autonomous task execution
tags: [autonomous-agent, telegram, persistent-memory, self-evolving, cron, 24-7-assistant]
---

# Friday Autonomous AI Assistant

## Purpose
Claude Code powers a full 24/7 assistant — no custom AI backend, no agent framework. Telegram MCP + Flask+SQLite memory server + 18 autonomous cron jobs + self-evolving cognition harness. $100/month Anthropic Max Plan.

## When To Use
- Building a personal 24/7 AI assistant with Telegram interface
- Need scheduled briefings (weather, forex, AI news, movie updates)
- Want self-evolving skills that improve from real interactions
- Implementing proactive messaging (assistant reaches out first)
- Building a system that learns your preferences over time

## How To Apply
**Setup:** Download SETUP.md, paste to fresh Claude Code: "Read ~/Downloads/SETUP.md and follow every step to set up a 24/7 AI assistant"

**Start:** `claude --channels plugin:telegram@claude-plugins-official --dangerously-skip-permissions`

**18 cron jobs include:** email check (1h), cron watchdog (6h), daily briefing (9AM), heartbeat (1h), reflection (12h), preference learning (nightly), AI model monitor (daily 10:17), memory API health (3h), weekly summarization, goal priorizer, memory decay, experiments runner, world model grower, auto-audit (3x/day)

**5 self-evolving subsystems:**
1. Skill Acquisition (extract reusable patterns from solved tasks)
2. Daily Self-Reflection (nightly log review for patterns + insights)
3. Preference Learning (infer rules from repeated feedback corrections)
4. World Modeling (user behavior model with confidence + expiration)
5. Self-Improvement Proposals (changes proposed, never auto-applied)

**v2 Cognition Harness (April 2026):** Goal engine, hierarchical planner, 3-layer memory (episodic/semantic/procedural), causal world model, self-knowledge/autonomy ladder, verifier+sandbox, experiments+skill compiler, 11 KPIs

## Integration Notes
- Stack: Claude Code (Opus 4.7, 1M context), Telegram MCP, Flask+SQLite, ElevenLabs TTS/STT, Notion MCP, GitHub API
- Memory: single Python file, no vector DB — Flask+SQLite+BLOBs
- Backup: `/backup/export` + `/backup/import` HTTP endpoints for disaster recovery
- Golden rule: no unrecorded autonomy — every goal, plan, action leaves a DB row
