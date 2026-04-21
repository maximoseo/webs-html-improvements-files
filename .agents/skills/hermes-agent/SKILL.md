# SKILL: Hermes Agent — Self-Improving AI Agent by Nous Research
**Source:** https://github.com/NousResearch/hermes-agent
**Domain:** code
**Trigger:** When building a persistent, self-improving AI agent with memory, skills, multi-platform messaging, and scheduled automations

## Summary
Self-improving agent with a closed learning loop: autonomous skill creation, skill self-improvement during use, FTS5 session search, Honcho dialectic user modeling. Runs on VPS, Docker, SSH, Modal (serverless). Works with any OpenAI-compatible model.

## Key Patterns
- Skills created and improved automatically from complex tasks
- Memory: agent-curated with periodic nudges, cross-session recall
- Multi-platform: Telegram, Discord, Slack, WhatsApp, Signal, CLI
- Terminal backends: local, Docker, SSH, Daytona, Singularity, Modal
- Cron scheduler: daily reports, nightly backups in natural language

## Usage
Install on a VPS or cloud VM for a persistent 24/7 agent. Connect via Telegram/CLI.

## Code/Template
```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc
hermes          # start chatting
hermes model    # choose LLM provider/model
hermes gateway  # start messaging gateway (Telegram, Discord, etc.)
hermes setup    # full setup wizard
hermes claw migrate  # migrate from OpenClaw
```
