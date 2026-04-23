---
name: impeccable
description: "Create distinctive, production-grade frontend interfaces with high design quality. Generates creative, polished code that avoids generic AI aesthetics. Use when the user asks to build web components, pages, artifacts, posters, or applications, or when any design skill requires project context. Call with 'craft' for shape-then-build, 'teach' for design context setup, or 'extract' to pull reusable components and tokens into the design system."
argument-hint: "[craft|teach|extract|audit|critique|polish|distill|animate|colorize|bolder|quieter|delight|adapt|typeset|layout|overdrive]"
user-invocable: true
license: Apache 2.0. Based on Anthropic's frontend-design skill.
---

# SKILL: Impeccable
**Source:** https://github.com/pbakaus/impeccable
**Domain:** design
**Trigger:** Building web UI, design review, typography polish, animation, any frontend design work

## Summary
A comprehensive frontend design skill with 7 reference modules (typography, color, spatial design, motion, interaction, responsive, UX writing) and 18 steering commands for audit, critique, polish, animation, and more. Fights LLM design monoculture (Inter, purple gradients, nested cards) with curated anti-patterns.

## Key Patterns
- **18 commands**: craft, teach, extract, audit, critique, polish, distill, clarify, optimize, harden, animate, colorize, bolder, quieter, delight, adapt, typeset, layout, overdrive
- **7 reference domains**: typography, color-and-contrast, spatial-design, motion-design, interaction-design, responsive-design, ux-writing
- **Font selection procedure**: List 3 reflex fonts → reject them all → browse catalog with brand words → cross-check against reflex patterns
- **Banned fonts** (reflex defaults): Inter, Roboto, DM Sans, IBM Plex, Space Grotesk, Outfit, Plus Jakarta Sans, Instrument Sans, Fraunces, Playfair Display, Cormorant, Newsreader, Syne, Lora...
- **Anti-patterns**: Gray text on colored backgrounds, pure black/gray, cards-in-cards, bounce/elastic easing, purple-on-white gradients
- **OKLCH color**: Use for tinted neutrals, dark mode, accessibility-safe palettes
- **Context required**: Must run `/impeccable teach` or check `.impeccable.md` before design work

## Usage
Via Claude Code: `/impeccable [command]`  
Via Cursor/Codex: `$impeccable [command]`

Workflow: `/impeccable teach` → gather context → `/impeccable craft` → shape-then-build → `/polish` before shipping

Download bundles: https://impeccable.style

## Code/Template
```
/audit blog              # Technical quality check (a11y, performance, responsive)
/critique landing page   # UX design review: hierarchy, clarity, emotional resonance
/polish feature modal    # Final pass before release
/animate hero            # Add purposeful motion with correct easing curves
/typeset heading         # Fix font choices, hierarchy, fluid sizing with clamp()
/layout dashboard        # Fix spacing, visual rhythm, 8px grid alignment
/bolder design           # Amplify boring, safe designs
/quieter design          # Tone down overly bold designs
/delight onboarding      # Add moments of joy and micro-interactions
/overdrive hero          # Add technically extraordinary effects (Three.js, shaders)
```

Typography principles:
- Fluid sizing with `clamp()` for marketing pages; fixed `rem` for app UIs
- Line-height scales inversely with line length
- Cap body at 65-75ch
- Fewer sizes with more contrast (1.25+ ratio between scale steps)
