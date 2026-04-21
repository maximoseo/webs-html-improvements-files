# SKILL: Awesome DESIGN.md
**Source:** https://github.com/VoltAgent/awesome-design-md
**Domain:** design
**Trigger:** When you need a DESIGN.md for a project to give AI agents visual style guidance, or when mimicking a specific product's design language

## Summary
A curated collection of 69 DESIGN.md files inspired by developer-focused websites. DESIGN.md is a plain-text design system document that AI agents read to generate consistent, brand-accurate UI — inspired by Google Stitch's concept. Drop one into your project root and any AI coding agent knows exactly how your UI should look.

## Key Patterns
- **DESIGN.md format**: Plain markdown, no JSON/Figma/tooling required — drop in project root
- **69 real-world designs** including AI platforms, dev tools, databases, e-commerce, fintech, productivity
- **Key categories**: AI/LLM Platforms, Developer Tools/IDEs, Backend/Database, SaaS, E-Commerce, Fintech, Productivity
- **Notable designs**: Claude (warm terracotta, editorial), Vercel (black/white precision, Geist), Cursor (sleek dark + gradient), Stripe (financial precision, clean), Raycast (dark chrome, vibrant gradient), Warp (dark IDE-like, block-based)
- **Request system**: Request any website at getdesign.md/request
- **Agent integration**: Works with any AI coding agent that reads project files (Claude Code, Cursor, Copilot)

## Usage
1. Browse collection at https://github.com/VoltAgent/awesome-design-md
2. Copy a DESIGN.md into your project root
3. Tell your AI agent: "build a page that looks like this"

The agent reads DESIGN.md and generates pixel-perfect UI matching the chosen design language.

**Common patterns from the collection:**
- Dark SaaS: Void-black canvas, monochrome, single accent color (emerald/purple)
- AI-native: Cinematic dark, media-rich, animated
- Editorial: Clean white canvas, strong typography, code-forward
- Minimalist: Near-monochrome, generous whitespace, tight letter-spacing

## Code/Template
```markdown
# DESIGN.md

## Visual Identity
**Primary color:** #635BFF (Stripe violet)
**Background:** #FFFFFF
**Text primary:** #0A2540

## Typography
**Display font:** Sohne (or system-ui fallback)
**Body font:** 16px/1.6 base
**Heading scale:** 48px → 32px → 24px → 20px → 16px

## Spacing
Base unit: 8px. Section padding: 80px vertical. Card padding: 24px.

## Components
Cards: 1px border #E5E7EB, 8px radius, subtle shadow
Buttons: 6px radius, Sohne medium, 44px min height
```
