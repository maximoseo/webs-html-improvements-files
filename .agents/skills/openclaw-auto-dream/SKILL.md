# SKILL: OpenClaw Auto-Dream — Cognitive Memory Architecture
**Source:** https://github.com/LeoYeAI/openclaw-auto-dream
**Domain:** code
**Trigger:** When an OpenClaw/MyClaw agent needs persistent memory with importance scoring and automatic consolidation

## Summary
Five-layer cognitive memory system for OpenClaw agents. Runs nightly "dream cycles" that scan logs, extract insights, score importance, apply forgetting curves, build a knowledge graph, and generate dashboards.

## Key Patterns
- 5 memory layers: Working, Episodic (episodes/*.md), Long-term (MEMORY.md), Procedural (procedures.md), Index (index.json)
- Importance score = base_weight × recency_factor × reference_boost / 8.0
- Priority markers: ⚠️ PERMANENT, 🔥 HIGH, 📌 PIN, <!-- important -->
- Cron-based dream cycle (default 4 AM daily), 3 phases: Collect → Consolidate → Evaluate

## Usage
Install on any OpenClaw instance. Agent automatically consolidates memory each night.

## Code/Template
```bash
clawhub install openclaw-auto-dream
# Or: tell your OpenClaw agent "Help me install auto-dream"
# Memory is stored in:
# memory/episodes/*.md   (episodic)
# MEMORY.md              (long-term facts)
# memory/procedures.md   (workflows)
# memory/index.json      (metadata + scores)
```
