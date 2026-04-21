---
name: Autoskills Stack Detector
description: Automatic skill discovery, project tech-stack detection, and zero-config context.
color: "#3B82F6"
emoji: 🔍
vibe: Read the environment, load the skills.
---

# Autoskills Stack Detector Skill

Synthesized from `midudev/autoskills`.

## 🧠 Core Capabilities
- **Automatic Tech Detection:** Scans `package.json`, `requirements.txt`, or Gradle files to identify the project's frameworks and infrastructure.
- **Skill Suggestion:** Recommends relevant markdown-based skills based on the detected stack.
- **Context Synthesis:** Generates a unified `CLAUDE.md` or `AGENTS.md` summary linking all active skills for the agent.

## 🎯 When to Use
- When initializing a new repository or entering a workspace for the first time.
- When organizing a chaotic project that lacks clear agent instructions.

## 🚨 Anti-Patterns
- Do not forcibly overwrite existing `CLAUDE.md` files if they contain custom human instructions. Always append or merge.
