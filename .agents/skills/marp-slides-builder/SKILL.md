---
name: MARP Slides Builder
source: https://github.com/robonuggets/marp-slides
category: Tools
purpose: Create beautiful MARP presentations with SVG charts, dashboard components, dark/light themes, and 22 curated reference decks
when_to_use: When creating presentations, reports, dashboards, or slide decks in Markdown format
tags: [marp, presentations, slides, charts, svg, markdown, dashboard]
---

# MARP Slides Builder

## Purpose
Claude Code skill for MARP presentations. 22 curated reference decks teach composition quality. SVG charts, metric cards, gauges, sparklines, progress bars, interactive elements — all in raw HTML inside Markdown.

## When To Use
- "Create a MARP presentation reviewing my Q1 sales data. Dark theme, stat cards, bar chart."
- "Build a deck about coffee brewing methods. Editorial style, warm tones."
- "Make a fitness dashboard presentation from this CSV"

## How To Apply
**Install:**
```bash
git clone https://github.com/robonuggets/marp-slides
claude --add-dir ./marp-slides
```

**VS Code extension settings:**
```json
{
  "markdown.marp.enableHtml": true,
  "markdown.marp.allowLocalFiles": true
}
```

**Design system features:**
- Dark + light themes with tested font pairings (Outfit+Raleway, DM Serif+DM Sans, Space Grotesk+IBM Plex Mono)
- SVG charts: line/area, donut/pie, gauges, sparklines, bar, radar
- Dashboard: metric cards with gradient borders, status dots, verdict tags, hover rows
- Interactive: collapsible details sections, tooltips, progress bars
- Layout: before/after splits, terminal mockups, chat bubbles, timelines, flowcharts
- SVG icon library: 16+ inline icons

**22 example deck categories:** data/dashboard, lifestyle/editorial, guide/how-to, fun/creative, travel/location, showcase

**Export:**
```bash
npx @marp-team/marp-cli slides.md --pdf --allow-local-files    # PDF
npx @marp-team/marp-cli slides.md --pptx --allow-local-files   # PPTX
npx @marp-team/marp-cli slides.md --html --allow-local-files   # HTML
```

## Integration Notes
- The 22 examples teach composition, not just components — Claude matches their visual rhythm
- CSS variables drive theming — swap one variable to reskin entire deck
