---
name: SkillUI (Design System Extractor)
source: https://github.com/amaancoderx/npxskillui
category: Design Systems
purpose: Reverse-engineer any website's design system into a Claude-ready SKILL.md — colors, typography, spacing, animations, components
when_to_use: When you need to clone a site's visual style, or when building UI that must match an existing brand/design system
tags: [design-system, ui, css, extraction, skillui, brand]
---
# SkillUI (Design System Extractor)

## Purpose
Crawls any website, git repo, or local codebase and extracts its complete design system — packaged into a folder Claude reads automatically.

## When To Use
- Cloning or matching an existing site's visual language
- Generating a design system skill from any URL
- Building UI components that must match a specific brand
- Extracting design tokens (colors, spacing, typography) for use in new projects

## How To Apply
```bash
# Install
npm install -g skillui

# Extract from URL
skillui --url https://notion.so

# Ultra mode (Playwright, captures screenshots + animations)
skillui --url https://linear.app --mode ultra

# Scan local project
skillui --dir ./my-app

# Clone and scan repo
skillui --repo https://github.com/org/repo
```

Output folder contains:
- `SKILL.md` — auto-loaded by Claude
- `DESIGN.md` — full design system tokens
- `tokens/` — colors.json, spacing.json, typography.json
- `references/` — ANIMATIONS.md, LAYOUT.md, COMPONENTS.md
- `screens/` — scroll screenshots (ultra mode)
- `fonts/` — bundled Google Fonts (woff2)

## Examples
```bash
# Extract galoz.co.il design system
skillui --url https://galoz.co.il --mode ultra --out ./galoz-design
cd galoz-design && claude
# → "Build a hero section matching this design system"
```

## Integration Notes
- Pure static analysis — no AI, no API keys required for default mode
- Ultra mode requires: `npm install playwright && npx playwright install chromium`
- Version 1.3.2 (npm package: `skillui`)
- Pairs with `hue-design-skill` for brand-first design generation
