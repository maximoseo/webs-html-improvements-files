---
name: design-dna
description: >-
  Extract, define, and apply design DNA across three dimensions: design system
  (tokens), design style (qualitative feel), and visual effects (Canvas, WebGL,
  3D, particles, shaders, scroll effects, etc.). Use this skill when: (1) a user
  wants to see the full 3-dimension design structure/schema, (2) a user provides
  images, screenshots, or URLs of reference designs and wants them analyzed into
  a structured JSON profile covering all three dimensions, (3) a user has a
  Design DNA JSON and content and wants a design generated from it, or (4) any
  combination of these phases. Triggers on "design DNA", "extract design style",
  "analyze design", "design tokens from reference", "generate design from JSON",
  "design system from screenshot", "design profile", "style guide JSON",
  "visual effects analysis", "design with effects", "3d design analysis".
---

# SKILL: Design DNA
**Source:** https://github.com/zanwei/design-dna
**Domain:** design
**Trigger:** When user wants to extract, analyze, or apply visual design identity from reference designs

## Summary
An agent skill for extracting, structuring, and applying visual design identity as machine-readable "Design DNA" across three dimensions: design tokens, qualitative style, and visual effects. Drives a three-phase workflow: Structure → Analyze → Generate.

## Key Patterns
- **3 Dimensions**: Design System (measurable tokens), Design Style (qualitative perception), Visual Effects (Canvas/WebGL/3D/particles/shaders/scroll)
- **Phase 1 – Structure**: Output full JSON schema with field descriptions
- **Phase 2 – Analyze**: From screenshots/URLs, produce complete DNA JSON (every field filled, no empty strings)
- **Phase 3 – Generate**: Given DNA JSON + content, implement faithful HTML/CSS/JS output
- DNA JSON is portable: commit to git, share across teams, version control design identity
- Polish iteration: re-attach reference images to close gap between draft and reference-faithful result

## Usage
Install: `npx skills add zanwei/design-dna`

1. **Structure phase**: Ask agent to "show me the design DNA schema"
2. **Analyze phase**: Provide screenshots/URLs → agent outputs complete DNA JSON
3. **Generate phase**: Provide DNA JSON + content → agent implements the design

For visual effects, agent scans for canvas, WebGL, Three.js, particles, shaders, scroll triggers.

## Code/Template
```json
{
  "design_system": {
    "color": { "primary": "#...", "secondary": "#...", "accent": "#..." },
    "typography": { "display_font": "...", "body_font": "...", "scale_ratio": 1.25 },
    "spacing": { "base": "8px", "density": "comfortable" },
    "layout": { "max_width": "1280px", "columns": 12 },
    "shape": { "border_radius": "8px" },
    "elevation": { "shadow": "0 4px 12px rgba(0,0,0,0.1)" },
    "motion": { "easing": "ease-out", "duration": "200ms" }
  },
  "design_style": {
    "mood": "...", "visual_language": "...", "composition": "...",
    "brand_voice": "..."
  },
  "visual_effects": {
    "enabled": true,
    "effect_intensity": "moderate",
    "performance_tier": "standard",
    "composite_notes": "..."
  }
}
```
