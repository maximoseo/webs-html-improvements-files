# Examples — Post-Ingestion Usage

## Example 1 — Onboard a new domain

```
User: "Set up HTML redesign pipeline for newbrand.co.il"
Assistant:
  1. Run skillui-cli in ultra mode against https://newbrand.co.il/ → extracts tokens
  2. Run hue-brand-extractor on the homepage → fills secondary colors
  3. Merge into domain-brand-map.json → new entry
  4. Invoke /redesign-html-template newbrand.co.il
  5. Run agentic-seo-audit on output → block if < B grade
  6. Deploy to Obsidian + GitHub via existing pipeline
```

## Example 2 — Add a chart to an article

```
User: "This galoz article needs a Modbus vs Profinet latency chart"
Assistant (uses figure-router pattern):
  - Data is numeric (real latency numbers) → ROUTE TO PLOT MODE
  - Emit inline Chart.js + <canvas> block (WP-safe — no external deps)
  - Alt: use marp-slides sparkline primitive for inline stat strip
```

## Example 3 — Swap the article theme at runtime

```
Content team: "Make this article use the 'minimal' theme instead of 'technical'"
Pipeline (html-ppt-skill token-swap pattern):
  - Single line change: <link rel="stylesheet" href="/themes/minimal.css">
  - All CSS custom properties re-resolve → no content rewrite
  - Preview via ?preview=minimal query param
```

## Example 4 — Add a decorative hero illustration

```
Editor: "Galoz article feels flat — add something in the hero"
Pipeline (svg-hand-drawn-skill):
  - Fetch SVG concept (static)
  - Run hand-drawn animation converter → preview.html + player.js embed snippet
  - Drop <div id="gz-hero-anim"> + 1-line script into article
  - Player auto-plays, pause on scroll-out
```

## Example 5 — Post-publish drift monitor

```
Cron (adapted from friday-showcase):
  Nightly 02:00 IST:
    for each published article in priority domains:
      fetch live WP post
      run agentic-seo-audit → grade
      if grade dropped ≥ 1 letter from published:
        open PR with diff + recommended fixes
        notify Telegram
```

## Example 6 — Quality scorecard on a draft

```
User: "Score this draft before I ship"
Assistant (compose-style-rubric):
  Performance 35 / 35 ✓ (all images lazy, minified, <style> scoped)
  Structure 22 / 25  (4 H2 sections — recommend 6+)
  A11y 18 / 20       (1 image missing alt)
  Tokens 20 / 20 ✓  (all colors from map, no hex leaks)
  Total: 95 / 100 — A-
  → Action: add 2 H2 sections; add alt to product-3 image.
```
