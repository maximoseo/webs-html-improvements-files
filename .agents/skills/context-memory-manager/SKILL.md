---
name: Context & Memory Manager
description: Advanced memory retrieval, context-packing, and persistent memo workflows.
color: "#8B5CF6"
emoji: 🧠
vibe: Retain everything, recall instantly.
---

# Context & Memory Manager Skill

Inspired by `thedotmack/claude-mem` and `feuersteiner/contextrie`.

## 🧠 Core Capabilities
- **Context Packing:** Optimizes how history and files are loaded into the prompt context window to avoid bloat.
- **Memory Persistence:** Manages global `MEMO.md` and `EXAMPLES.md` files across multi-agent sessions.
- **State Retrieval:** Ensures agents can recall past architectural decisions without hallucinating.

## 🎯 When to Use
- When orchestrating complex, multi-turn coding tasks that require historical context.
- When an agent seems to "forget" previous instructions or rules.

## 🚨 Anti-Patterns
- Do not dump thousands of lines of raw logs into memory; synthesize them into concise bullet points.
