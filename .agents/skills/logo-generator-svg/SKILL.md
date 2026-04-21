---
name: SVG Logo Generator
source: https://github.com/op7418/logo-generator-skill
category: Design Systems
purpose: Professional SVG logo generator with 6+ variants per request and 12 professional showcase background styles using Gemini image generation
when_to_use: When generating professional logos for startups, side projects, or brand identity iteration
tags: [logo, svg, design, brand, gemini, image-generation, showcase]
---

# SVG Logo Generator

## Purpose
Creates 6+ geometric SVG logo variants per request, then generates high-end showcase images with 12 professional backgrounds using Gemini 3.1 Flash Image Preview (Nano Banana).

## When To Use
- "Generate a logo for my AI product DataFlow"
- "Create 6 logo variants for CloudSync"
- "Show me the logo in different background styles"
- Startups needing professional logos quickly
- Designers exploring initial brand concepts

## How To Apply
**Install:**
```bash
npx skills add https://github.com/op7418/logo-generator-skill.git
```

**5-phase workflow:**
1. Information Gathering: product name, industry, core concept, design preferences (cold/warm, minimal/complex)
2. Pattern Matching + SVG Generation: 6+ distinct variants with design rationale
3. Iteration: select favorites, adjust parameters (size, spacing, rotation)
4. High-End Showcase: export SVG→PNG → generate showcase with Gemini in 4 styles
5. Delivery: HTML showcase page + SVG files + PNG exports + showcase images

**12 background styles:**
- Dark: The Void, Frosted Horizon, Fluid Abyss, Studio Spotlight, Analog Liquid, LED Matrix
- Light: Editorial Paper, Iridescent Frost, Morning Aura, Clinical Studio, UI Container, Swiss Flat

**6 design principles:** Extreme Simplicity, Generous Negative Space (40-50%), Precise Proportions (2.5-4px), Visual Tension, Restraint Over Decoration, Single Focal Point

## Examples
- "Design a logo for a blockchain security platform" → 6 SVG variants (dot matrix, line systems, mixed composition)
- "Generate showcase images for logo #3 in void and editorial styles"

## Integration Notes
- Gemini API key required (GEMINI_API_KEY) for showcase generation
- Python deps: google-genai, python-dotenv, cairosvg, Pillow
- `npx skills add` for automatic installation
- Optional third-party Gemini-compatible endpoints supported
