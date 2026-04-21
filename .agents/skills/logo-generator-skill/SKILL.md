---
name: Logo Generator (SVG via Gemini)
source: https://github.com/op7418/logo-generator-skill
category: Design Systems
purpose: Generate SVG brand logos from text descriptions using Gemini — 6+ variants per brand concept, brand color palette extraction
when_to_use: When you need a brand logo, icon, or mark generated without paying for a designer
tags: [logo, svg, brand, gemini, design, ai-generated]
---
# Logo Generator Skill

## Purpose
Generates SVG logos from text descriptions via Gemini's image reasoning — outputs 6+ variants covering different visual approaches for any brand concept.

## When To Use
- Quick brand concept exploration
- Logo variations for A/B testing
- Icon sets for apps or interfaces
- Placeholder brand marks for prototypes

## How To Apply
```bash
# Dependencies
pip install pillow requests google-generativeai

# Run
python generate.py --brand "EcoMart" --colors "#2D7D32,#A5D6A7" --variants 6

# Or trigger in Claude
"Generate logo variants for: [brand name], [brand essence], [industry]"
```

## What's Generated
- 6 distinct SVG approaches: wordmark, lettermark, symbol, combination, emblem, abstract
- Each variant in brand color palette
- Each exported as clean SVG (scalable, editable)
- Summary comparison HTML

## Logo Styles Covered
- Minimalist geometric
- Tech/modern
- Organic/natural
- Bold wordmark
- Abstract symbol
- Lettermark

## Integration Notes
- Requires `GEMINI_API_KEY` environment variable
- Output SVGs are hand-verifiable (no raster)
- Pairs with `hue-design-skill` for full design system generation after logo is chosen
- Install: copy `SKILL.md` to `.claude/skills/logo-generator/`
