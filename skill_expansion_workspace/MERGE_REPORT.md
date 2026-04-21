# MERGE REPORT

**Date:** 2026-04-20
**Scope:** Deduplication and synthesis of 35 GitHub repositories into the Agent Skill Registry.

## Deduplication & Consolidation

### 1. Presentation & UI
- **Sources:** `lewislulu/html-ppt-skill`, `robonuggets/marp-slides`, `hamen/material-3-skill`, `dominikmartn/hue`
- **Merge Action:** Consolidated into a unified `brand-to-design-system` and `html-redesign-mega`. Instead of separating HTML PPTs and standard UI, color tokenization and spacing rules were unified into a single responsive layout engine.

### 2. Communication Protocols
- **Sources:** `hexiecs/talk-normal`, `amanattar/caveman-claude-skill`, `getlago/inside-lago-voice-skill`
- **Merge Action:** Merged into `talk-normal-caveman`. The agent understands that concise, terse communication is the baseline, while the Lago skill provides the framework if a specific *brand voice* is requested.

### 3. Core Development Loop
- **Sources:** `LIDR-academy/manual-SDD`, `maiobarbero/my-ai-workflow`, `LichAmnesia/lich-skills`, `poteto/how`
- **Merge Action:** Combined into `spec-driven-development`. The "How" repository's onboarding explanation mechanics were integrated into the SDD planning phase, ensuring the agent explains the *architecture* before modifying it.

### 4. Agentic Evolution
- **Sources:** `AMAP-ML/SkillClaw`, `WoJiSama/skill-based-architecture`, `midudev/autoskills`, `spencerpauly/awesome-cursor-skills`
- **Merge Action:** Consolidated into `agentic-eval-loop` and the general instruction set. The agent now inherently understands that skills should be extracted, saved into `.cursor/skills` or `.agents/skills`, and continuously verified.

## Unique Retained Capabilities
- `aoyunyang/spider-king-skill` (Pure protocol reversal, left distinct from standard web fetching).
- `40RTY-ai/shopify-admin-skills` (Highly specific domain, kept as a distinct specialized skill).
- `lugasia/3gpp-skill` (Highly specific domain).
