# SKILL: MetaClaw — Agent That Meta-Learns and Evolves in the Wild
**Source:** https://github.com/aiming-lab/MetaClaw
**Domain:** code
**Trigger:** When you want your AI agent to automatically improve from every conversation without manual training

## Summary
Meta-learning proxy for OpenClaw and compatible agents. Intercepts live conversations, injects relevant skills, creates/updates skills from experience, runs RL training during idle windows. No GPU cluster required — uses cloud LoRA via Tinker/MinT API.

## Key Patterns
- Skills mode: auto-creates and improves skills from conversations (default, no RL)
- RL mode: meta-learns from accumulated experience during idle/sleep windows
- Contexture layer: cross-session memory with adaptive policy + background consolidation
- Supports: OpenClaw, CoPaw, IronClaw, PicoClaw, ZeroClaw, NanoClaw, NemoClaw

## Usage
Run metaclaw as a proxy in front of any OpenClaw-compatible agent. Fully async, non-blocking.

## Code/Template
```bash
pip install metaclaw
metaclaw setup              # one-time config wizard
metaclaw start              # auto mode: skills + scheduled RL
metaclaw start --mode rl    # RL only (trains immediately on full batch)
metaclaw start --mode skills_only  # skills only, no RL

# OpenClaw one-click plugin:
# Drop metaclaw folder into OpenClaw extensions dir
# Then run setup command
```
