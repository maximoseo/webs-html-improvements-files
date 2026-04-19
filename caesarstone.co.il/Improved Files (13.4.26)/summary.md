# Summary — Caesarstone 13.4.26 Rebuild

**Date**: 2026-04-15
**Agent**: Latest Files
**Scope**: Replace 3 primary files in `Improved Files (13.4.26)` + add 3 supporting artifacts

---

## What Changed vs. 12.4.26 and 13.4.26 Baselines

### File size delta

| File | 12.4.26 | 13.4.26 (before) | 2026-04-15 (after) | Delta vs 13.4.26 |
|---|---|---|---|---|
| `Improved_HTML_Template.html` | 66,049 B | 65,002 B | 86,773 B | **+21,771 B (+33%)** |
| `Improved_N8N_Prompt.txt` | 18,063 B | 23,108 B | 37,133 B | **+14,025 B (+61%)** |
| `Improved_N8N_Workflow.json` | 152,039 B | 154,781 B | 174,286 B | **+19,505 B (+13%)** |
| `validation_note.md` | — | — | NEW | added |
| `source_map.md` | — | — | NEW | added |
| `summary.md` | — | — | NEW | added |

---

## HTML Template — Changes

### Fixed

- **H1 compliance**: Title was `<h2 data-resp="heading">` in 13.4.26 baseline — changed to `<h1 data-resp="heading">`. Exactly one H1 in the document now. The old N8N prompt explicitly said "H1 is FORBIDDEN" — that rule was wrong and has been inverted.
- **TOC position**: TOC was rendered AFTER the stat-grid and insight-card in 13.4.26 (too late). Moved to directly after the hero image + first intro paragraph. Never first; never below 2nd content section.
- **Author-block logo link**: Logo in author block was a bare `<img>` with no anchor. Now wrapped in `<a href="https://www.caesarstone.co.il/" aria-label="Caesarstone homepage">` — same treatment applied to sticky header logo and footer logo.
- **Author social icons**: Were text letters ("f", "ig", "P", "yt", "in"). Replaced with real inline SVG brand glyphs for Facebook, Instagram, YouTube, LinkedIn, Pinterest. Hover animates to official network colors.
- **Scroll-to-top visibility**: Button was always visible. Added inline IIFE `<script>` that toggles `.visible` class on scroll > 300px; opacity transitions 0→1 via CSS.

### Added

- **Trust-signal strip** (after TOC, before stat grid): 4 chips with real Caesarstone facts — since 1987, lifetime warranty, global + Israeli production, 50+ colors. Real SVG icons in brand color.
- **Did You Know callout** (inside Modern section): distinct warm-taupe background, `data-resp="callout-didyouknow"`. First mention of Bauhaus design heritage.
- **Tip callout** (inside Classic section): Brand-primary border-right accent, `data-resp="callout-tip"`, with lightbulb icon. Professional balance-advice tip.
- **How-To callout** (inside Choose section): Numbered-steps format with `data-resp="callout-howto"`, checklist icon. 5-step kitchen-selection guide.
- **Mid-article CTA #1** (~30% mark, after minimalist section): Brand gradient card with white primary button to contact-us + outlined phone button.
- **Mid-article CTA #2** (~55% mark, after choose section): Soft gradient card with primary contact button + green WhatsApp button.
- **External link #2**: Added ArchDaily kitchen category link in Eclectic section, complementing existing Globes.co.il link.
- **Intro paragraph**: New dedicated lede paragraph between hero image and TOC, explaining article scope (no dates).
- **RTL-correct icon placement**: All CTA buttons now use inline-flex with `gap:8px`, icons positioned AFTER text on same baseline — matches Hebrew reading order.
- **Ordering**: Catalog CTA → Closing CTA → FAQ → Author. Closing CTA is now genuinely "above the FAQ/author section" (was between FAQ and Author in 13.4.26).

### Preserved (intentionally)

- Single `<style>` block + inline CSS (WordPress-safe approach validated in baseline).
- `<details>/<summary>` accordion for TOC + FAQ (native, zero-JS, identical in WP and raw HTML).
- Media query breakpoints (1024 / 768 / 480).
- Sticky header pattern with logo + context text + contact button.
- Footer 4-column grid with brand info + nav + contact.
- 3× JSON-LD schemas (Article, Organization, FAQPage).
- Brand palette (no invented colors).
- Real content copy from 13.4.26 (refined, not replaced).

### Delta vs 12.4.26

- 12.4.26 had the same fundamental gaps as 13.4.26 (no H1, no author logo link, no scroll-threshold button, no callout variety, placeholder social icons). The 13.4.26 iteration marginally improved a few things (added sticky header, top-btn, float-btn) but did not fix the core issues. The 2026-04-15 rebuild fixes them systematically.

---

## N8N Prompt — Changes

### Fixed

- **H1 rule inverted**: Old prompt line 212 said "H1 is FORBIDDEN - start with authority-establishing hook". New prompt has a dedicated "H1 RULE — ABSOLUTELY MANDATORY" section requiring exactly one `<h1>` with the primary article title.
- **TOC position rule**: Was implicit. Now explicit: "AFTER the first paragraph of the article (or after the hero image if the hero image directly follows the header). TOC is NEVER the first element. TOC is NEVER placed below the second content section."
- **TOC numeric-prefix ban**: New explicit instruction: 'NO leading numeric prefix ("1.", "2.", "3.")'.
- **Collapsed-by-default requirement**: New explicit rule for TOC and FAQ: "start COLLAPSED by default (use `<details>` WITHOUT the open attribute)".
- **Author logo link**: New rule: "MUST be wrapped in `<a href="https://www.caesarstone.co.il/" aria-label="Caesarstone homepage">` — NO placeholder `#` href".
- **Real social URLs**: New explicit rule listing all 5 URLs with "NEVER use `#` as href".
- **Date/time ban in hero area**: New rule: "NO DATES, NO YEARS, NO TIME-STAMPED PHRASES in the first paragraph, intro, hero header, or trust strip BEFORE the TOC. Dates ARE allowed later in body content when contextually needed".

### Added

- **WordPress safety rules section** (explicit): single style block, no Tailwind JIT, no external build, no admin-only JS, graceful JS degradation.
- **Trust Signal Strip section**: codifies 4 real facts with distinct SVG icons.
- **Callout component structures** (3 types): Tip, How-To (numbered steps), Did You Know — with inline data-resp attributes and distinct visuals.
- **Mid-article CTA structure** (CTA #1 + CTA #2) with explicit position markers (~30% / ~60%) and gradient/border prescriptions.
- **Closing CTA block section**: placed BEFORE FAQ with explicit headline + 3 buttons (contact + phone + WhatsApp).
- **Back-to-Top visibility behavior**: the `.visible` class toggle via inline IIFE script, 300px threshold.
- **Responsive validation checklist** (17 self-checks the model must perform before emitting).
- **RTL / Hebrew layout rules** (explicit section): icons after text on same baseline, floating button icon+text single line, hover-color contrast preservation.
- **Section order** (numbered 1–31): makes the final article structure unambiguous.
- **Internal + external link requirements**: "AT LEAST 1 internal … AT LEAST 1 external authoritative … at least 4 CTAs to contact page".

### Preserved

- All style variables and responsive framework.
- Existing content tokens (`{{ $('Writing Blog').first().json.output }}`, image URL expressions).
- Table wrapper rules.
- Sticky header / footer / JSON-LD schema specs.

---

## N8N Workflow — Changes

### Fixed

- Overwrote `nodes[name="HTML"].parameters.text` with new 36,406-character prompt (up from 20,386 — preserves token anchors, grew rule specificity).

### Preserved

- All 63 nodes untouched except the HTML agent.
- All 47 connections preserved byte-for-byte.
- Workflow name, settings, meta, credentials binding — unchanged.
- Other agent nodes (slug, Post Title, Meta Description, Meta Title) — unchanged.

---

## Supporting Artifacts (NEW)

- **validation_note.md**: Pass/fail matrix against all 27 specific requirements + 34 additional mandatory rules + 30 acceptance criteria.
- **source_map.md**: Every brand asset (logo, color, URL, social, phone, trust signal, author identity) mapped back to its live-site source.
- **summary.md** (this file): What changed vs the 12.4.26 and 13.4.26 baselines.

---

## Unresolved Questions

- None. All 27 requirements + 34 rules + 30 acceptance criteria are addressed in the delivered files. Post-publish Obsidian sync and Render dashboard redeploy execute after GitHub push (tracked in Task #9).
