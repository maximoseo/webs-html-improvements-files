---
name: SVG Hand-Drawn Animator
source: https://github.com/shaom/svg-hand-drawn-skill
category: Tools
purpose: Transform any SVG into a hand-drawn animation deliverable — draws paths first, reveals fills afterward, preserves source colors
when_to_use: When you need to present an SVG with a charming hand-drawn animation effect for demos, prototypes, or interactive previews
tags: [svg, animation, hand-drawn, html, canvas, preview, interactive]
---

# SVG Hand-Drawn Animator

## Purpose
Agent-native skill that turns any SVG into a hand-drawn animation deliverable. Default output: preview.html + player.js. Draws SVG paths first, reveals fills afterward, preserves source colors.

## When To Use
- "Turn this SVG into a hand-drawn preview page"
- "Generate a preview.html from this SVG with animation"
- Making architecture diagrams more engaging for presentations
- Creating interactive SVG demos that feel hand-crafted

## How To Apply
**Typical request examples:**
1. "Turn this SVG into a hand-drawn preview page."
2. "Generate a preview.html and player.js from this SVG."
3. "Apply a hand-drawn path and fill animation to this SVG."

**Provide:** local SVG file path or SVG URL
**Get:** preview.html + player.js

**Embed in any webpage:**
```html
<div id="svg-player"></div>
<script src="./player.js"></script>
<script>
  createSvgHanddrawPlayer("#svg-player", {
    svgMarkup: "<svg>...</svg>",
    speed: 1
  });
</script>
```

**Player API:** play(), pause(), seek(ratio), setSpeed(value), destroy()

## Examples
- System architecture SVG → preview.html with hand-drawn reveal animation for keynote
- Logo SVG → animated hand-drawn presentation for brand reveal

## Integration Notes
- No build step needed — pure vanilla JS
- Agent-driven: no Python/Node required by end user
- Reusable assets: player.js, preview-template.html in skills/svg-hand-drawn-preview/assets/
- The example in examples/svg-player-demo/ shows intended output shape
