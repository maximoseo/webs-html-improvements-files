# SKILL: Paperclip (AI Company Orchestration)
**Source:** https://github.com/paperclipai/paperclip
**Domain:** code
**Trigger:** When orchestrating teams of AI agents as a company — with org charts, goal alignment, budgets, heartbeats, and governance across multiple agent runtimes

## Summary
Paperclip is an open-source Node.js server + React UI that orchestrates teams of AI agents (OpenClaw, Claude Code, Codex, Cursor) toward business goals. Provides org charts, per-agent budgets, heartbeat scheduling, full audit trails, and a ticket system. "If OpenClaw is an employee, Paperclip is the company."

## Key Patterns
- Define business goal → hire agent team (CEO, CTO, engineers) → approve strategy → run
- Heartbeats: agents wake on schedule, check work, delegate up/down the org chart
- Per-agent monthly budgets — agents stop when limit hit
- Brings-your-own-agent: any runtime that accepts a heartbeat webhook
- Full tool-call tracing + immutable audit log + cost monitoring
- Multi-company isolation in one deployment

## Usage
```bash
git clone https://github.com/paperclipai/paperclip
# See documentation at https://paperclip.ing/docs
```

## Code/Template
```
Workflow:
01. Define goal: "Build #1 AI note-taking app to $1M MRR"
02. Hire team: CEO, CTO, engineers, designers, marketers
03. Set budgets per agent (monthly token cost limits)
04. Approve strategy → agents run autonomously 24/7
05. Monitor from dashboard / phone
```
