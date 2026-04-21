---
name: How Codebase Explainer
source: https://github.com/poteto/how
category: Tools
purpose: Cursor skill that explains how any subsystem, feature, or flow works — automatic mode selection (Explain vs Critique), parallel multi-angle exploration, synthesized architectural explanations
when_to_use: When onboarding to a codebase, understanding a complex flow, or getting architectural critique of a subsystem
tags: [codebase, explanation, architecture, cursor, multi-agent, critique, onboarding]
---

# How Codebase Explainer

## Purpose
Adds the `/how` command to Cursor. Ask how a subsystem works → get a senior-engineer-quality architectural explanation. Two auto-selected modes: Explain and Critique.

## When To Use
- "How does message virtualization work?"
- "Walk me through what happens when a user sends a message"
- "How is the auth service structured? Also critique the design."
- "How does the auth middleware check permissions?"
- When onboarding to an unfamiliar area of a codebase

## How To Apply
**Install:** Drop the `how/` folder (with .cursor-plugin/ and skills/) into your Cursor plugins directory.

**Two modes (auto-selected from question):**
- **Explain** (default): Overview → Key Concepts → How It Works → Where Things Live → Gotchas
- **Critique**: Explain first → spawn multiple independent critics across different models → surface architectural problems

**Simple vs Complex routing:**
- Simple questions → single agent, end-to-end
- Complex (multiple files/services) → decompose into 2-4 parallel exploration angles → synthesis agent reconciles

## Examples
- "How does the billing service calculate proration?" → simple path, single agent explains
- "How does auth work across all services? Critique the design." → fan-out: token validation angle, session management angle, cross-service propagation angle → synthesis + critique pass

## Integration Notes
- Structure: SKILL.md (routing logic) + references/ (explainer, explorer, critic prompts + critique rubric)
- Cursor-specific: uses .cursor-plugin/plugin.json manifest
- MIT license
