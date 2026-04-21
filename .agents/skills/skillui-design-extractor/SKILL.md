---
name: SkillUI Design System Extractor
source: https://github.com/amaancoderx/npxskillui
category: UI/UX
purpose: Reverse-engineer any design system from a URL, git repo, or local codebase into a Claude-ready SKILL.md file with full design tokens
when_to_use: When you need to match a website's visual design, extract design tokens, or build UI that matches an existing brand
tags: [design-system, design-tokens, ui-extraction, claude-ready, figma-alternative, css-variables]
---

# SkillUI Design System Extractor

## Purpose
CLI that crawls any website, git repo, or local codebase and extracts its complete design system — colors, typography, spacing, animations, components, screenshots — packaged into a folder Claude Code reads automatically.

## When To Use
- Need to replicate a website's visual language exactly
- Building a UI that must match an existing brand
- Onboarding to a design system you don't know
- Creating pixel-perfect clones or redesigns
- Extracting design tokens for a component library

## How To Apply
```bash
# Default mode — pure static analysis
skillui --url https://notion.so

# Ultra mode — full cinematic extraction with Playwright
skillui --url https://linear.app --mode ultra

# Scan local project
skillui --dir ./my-app

# Clone and scan repo
skillui --repo https://github.com/org/repo
```

**Output structure:**
- SKILL.md (auto-loaded by Claude)
- CLAUDE.md (project context)
- DESIGN.md (full token system)
- tokens/colors.json, spacing.json, typography.json
- screens/ (scroll screenshots in ultra mode)
- fonts/ (bundled Google Fonts woff2)

**Ultra mode extras:** scroll screenshots, hover/focus interaction diffs, CSS keyframes, flex/grid layout extraction, DOM component fingerprinting

## Examples
- `skillui --url https://stripe.com` → extracts Stripe's design system, open in Claude and say "build a pricing page matching this"
- `skillui --url https://linear.app --mode ultra --screens 10` → full cinematic extraction

## Integration Notes
- Node.js 18+ required; Playwright for ultra mode
- No AI, no API keys — pure static analysis
- Output includes .skill ZIP for portability
- Claude automatically reads SKILL.md and CLAUDE.md on session start
