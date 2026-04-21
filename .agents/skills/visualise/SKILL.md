---
name: visualise
description: "Render inline interactive visuals — SVG diagrams, HTML widgets, charts, and explainers — directly in the conversation. Use this skill whenever the user asks to visualize, diagram, chart, illustrate, or explain something visually, or when an explanation would genuinely benefit from a spatial/interactive diagram rather than text. Also triggers for: flowcharts, architecture diagrams, data visualizations, interactive explainers, comparison layouts, UI mockups, and any request containing 'show me', 'draw', 'map out', 'visualize', or 'diagram'. Even when the user doesn't explicitly ask for a visual, use this skill proactively when the topic has spatial, sequential, or systemic relationships that a diagram would clarify better than prose."
---

# SKILL: Visualise
**Source:** https://github.com/bentossell/visualise
**Domain:** design
**Trigger:** User asks to visualize, diagram, chart, illustrate, or "show me" anything

## Summary
An agent skill that renders rich interactive visuals — SVG diagrams, HTML widgets, charts, and explainers — directly inline in conversations as sandboxed iframes. Uses progressive disclosure: core rules always loaded, reference modules pulled in as needed.

## Key Patterns
- **Two output modes**: SVG mode (starts with `<svg>`, auto-wrapped in card) and HTML mode (raw fragment for interactive content)
- **Streaming constraints**: `<style>` first, visible content second, `<script>` last; no gradients/shadows/blur during streaming; inline styles preferred
- **Sandbox rules**: No localStorage, no position:fixed, no external fetches; CDN allowlist: cdnjs, esm.sh, jsdelivr, unpkg
- **4 reference modules**: design-system.md (always read first), diagrams.md, components.md, charts.md
- **`sendPrompt(text)`** bridge: makes visuals conversational by sending follow-up to chat
- **Routing by verb**: "how does X work" → illustrative; "steps" → flowchart; "compare" → side-by-side; "show data" → chart

## Usage
Install: `git clone https://github.com/bentossell/visualise.git ~/.agents/skills/visualise`

Triggers on: visualize, diagram, chart, illustrate, "show me", draw, map out, flowchart, architecture diagram.

Route visual type based on what user is asking:
| User says | Visual type |
|-----------|-------------|
| "how does X work" | Illustrative diagram (spatial metaphor) |
| "walk me through steps" | Flowchart |
| "compare X vs Y" | Comparison layout |
| "show data" | Chart.js viz |
| "explain X" (spatial) | Interactive explainer with sliders |

## Code/Template
```html
<!-- SVG mode (static diagrams) -->
<svg width="600" height="400" viewBox="0 0 600 400">
  <rect x="10" y="10" width="200" height="80" rx="8" fill="var(--surface-2)"/>
  <text x="110" y="55" text-anchor="middle" fill="var(--text-1)">Component</text>
</svg>

<!-- HTML mode (interactive) - structure: style → content → script -->
<style>:root { --accent: #3b82f6; }</style>
<div class="widget">...</div>
<script>
  function sendPrompt(text) { window.parent.postMessage({ type: 'prompt', text }, '*'); }
</script>
```
