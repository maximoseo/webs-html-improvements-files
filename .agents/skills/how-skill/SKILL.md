---
name: How (Codebase Explanation)
source: https://github.com/poteto/how
category: Coding
purpose: Ask how any subsystem, feature, or flow works — produces structured architectural explanation with optional multi-model critique
when_to_use: When onboarding to a new area of a codebase, or when you need a clear architectural explanation of a complex flow
tags: [codebase, explanation, architecture, critique, onboarding, cursor]
---
# How — Codebase Explanation Skill

## Purpose
Ask `/how` about any subsystem and get a structured architectural explanation at the level of a senior engineer onboarding onto a new area.

## Two Modes (auto-selected)
- **Explain** (default) — explore codebase → structured explanation: Overview, Key Concepts, How It Works, Where Things Live, Gotchas
- **Critique** — explain first → spawn multiple independent critics across different models to surface architectural problems

## Fan-Out Strategy
For complex multi-file questions: decomposes into 2-4 parallel exploration angles → parallel explorer subagents → synthesis agent reconciles findings. Simple questions run end-to-end in single agent.

## Example Prompts
- "How does message virtualization work?"
- "Walk me through what happens when a user sends a message"
- "How is the auth service structured? Also critique the design."
- "How does the auth middleware check permissions?"

## Structure
```
how/
├── .cursor-plugin/plugin.json
└── skills/how/
    ├── SKILL.md
    └── references/
        ├── explainer-prompt.md
        ├── explorer-prompt.md
        ├── critic-prompt.md
        └── critique-rubric.md
```

## Integration Notes
- Designed primarily for Cursor
- Critique mode spawns multiple critic subagents across different models
- Critique rubric in `references/critique-rubric.md`
- Pairs with `antivibe-skill` for deeper learning after understanding architecture
