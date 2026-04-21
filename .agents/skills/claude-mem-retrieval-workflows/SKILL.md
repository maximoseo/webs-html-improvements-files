---
name: Claude Mem Retrieval Workflows
description: Advanced 3-layer search patterns and progressive disclosure memory retrieval.
color: "#EC4899"
emoji: 🕰️
vibe: Retrieve exactly what is needed.
---

# Claude Mem Retrieval Workflows Skill

Extended from `thedotmack/claude-mem` (deduplicated from prior Memory Manager skill).

## 🧠 Core Capabilities
- **Progressive Disclosure:** Queries memory in stages (Index → Timeline → Full Observation) to minimize token consumption.
- **Session Compression:** Forces automated summarization at the end of every active tool-use cycle.

## 🎯 When to Use
- When querying massive historical project databases.
