---
name: Hue Brand Design System
source: https://github.com/dominikmartn/hue
category: UI/UX
purpose: Learn any brand from a URL, name, or screenshot and turn it into a complete design system — color tokens, typography, spacing, components, light + dark mode
when_to_use: When you need to capture an existing brand identity and make AI consistently generate visually coherent outputs
tags: [brand, design-system, color-tokens, typography, components, dark-mode]
---

# Hue Brand Design System

## Purpose
Analyzes a brand from URL/name/screenshot and produces a complete design language as a SKILL.md: color tokens, typography, spacing, components, light + dark mode, hero stage recipes, icon kit selection.

## When To Use
- "Make a design skill from cursor.com"
- "Create a design language inspired by Raycast"
- "Generate a hue skill from this screenshot"
- When two different AI sessions need to produce visually consistent output

## How To Apply
**Install (Claude Code):**
```bash
git clone https://github.com/dominikmartn/hue ~/.claude/skills/hue
```

**Trigger phrases:**
- "make a design skill from [url/name]"
- "create a design language inspired by [brand]"
- "generate a hue skill from this screenshot"

**Output:** design-model.yaml + landing-page.html per brand

**17 example brands included:** atlas, auris, drift, fizz, halcyon, kiln, ledger, meadow, orivion, oxide, prism, relay, ridge, solvent, stint, thrive, velvet

## Examples
- "Make a design skill from stripe.com" → generates stripe design-model.yaml with color tokens, typography, component patterns
- "Build a landing page in the style of Linear.app" → hue extracts design language → Claude generates matching page

## Integration Notes
- Compatible with Claude Code and Codex
- Output SKILL.md is usable by any agent session
- Alternative to figma tokens export + manual token setup
- Also available via hueapp.io for visual preview
