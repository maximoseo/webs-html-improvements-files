# SOURCE MAP — PowerPlug Copilot Rebuild — 2026-04-15

**Agent:** Copilot  
**Task:** Consolidated best-version rebuild of the HTML template, N8N prompt, and N8N workflow  
**Date:** 2026-04-15

---

## Base Source: Codex 2026-04-16 (GitHub)

**What was retained from Codex:**
- Full article content (12 sections, 2,800+ words on IT cost reduction strategies)
- Core article structure: hero → key takeaways → intro → TOC → content sections → CTAs → FAQ → author
- LTR enforcement approach (`direction:ltr !important` on every element)
- Inline style strategy (all visual styles inline, `<style>` block as bonus fallback)
- Brand color palette usage: `#131b3b` navy, `#0fb5b0` teal
- Accordion toggle pattern (inline onclick, `max-height` transition, `+` character icon)
- FAQ inline onclick pattern
- Internal link structure to powerplug.ai pages
- Trust signal content (Clalit 45,000 PCs, Rambam, Ben Gurion University)
- Table layout with navy gradient header and alternating rows
- All PowerPlug-verified case study data (no fabricated claims)
- N8N workflow node structure (63 nodes, Google Sheets → AI pipeline → WordPress)

**What was modified from Codex:**
- Agent label: "Codex" → "Copilot" throughout
- Date references: 2026-04-16 → 2026-04-15
- HTML node prompt in workflow: updated with Copilot-improved version

---

## Alternate Agent Reference: Hermes Agent 2026-04-16

**File size:** 37KB HTML, 12KB prompt, 126KB workflow

**What was borrowed/merged:**
- Validation document structure (VALIDATION-NOTE.md format with table-based checks)
- Sticky note organization pattern in workflow
- Section alternation approach (white vs. tinted backgrounds)

**What was rejected:**
- Different font stack (no Montserrat reference) — Copilot version uses Montserrat
- Slightly different TOC positioning (Hermes puts it before intro)
- Hermes workflow was smaller (126KB) vs Codex (132KB) — Codex has more complete pipeline

---

## Alternate Agent Reference: Claude Code 2026-04-16

**File size:** 49KB HTML, 18KB prompt, 20KB workflow

**What was borrowed/merged:**
- `details`/`summary` evaluation (reviewed but not adopted — inline onclick is more WordPress-safe)
- Brand intelligence extraction node pattern (evaluated for workflow improvement)
- 34-rule system prompt structure (reviewed for completeness comparison)
- Scroll-to-top 300px trigger requirement (clearly specified in Claude Code rules)
- Social hover color specifications: Facebook `#1877F2`, LinkedIn `#0A66C2`, Twitter `#1DA1F2`
- Logo wrapper pattern: `<a href="https://powerplug.ai/">` wrapping logo image

**What was rejected:**
- Claude Code uses `details`/`summary` HTML for TOC/FAQ — less consistent with inline onclick used in Codex/Copilot
- Claude Code workflow is only 20KB (lightweight) vs the full 63-node Codex pipeline — Codex pipeline is production-complete
- Claude Code uses `display:flex` for floating buttons on right side — Copilot keeps left-side placement per Codex rules

---

## Alternate Agent Reference: CLAUDE CODE (Tim Claw Max) 2026-04-16

**File size:** 57KB HTML, 13KB prompt, 16KB workflow

**What was borrowed/merged:**
- Explicit "horizontal wordmark" author logo specification (NOT circular)
- Social links author section with inline `onmouseover`/`onmouseout` hover handling (WordPress-safe)
- "Contact PowerPlug" button in author section
- Scroll-to-top visibility via inline `<script>` with `window.scrollY > 300`
- `pp-scroll-top` element ID for scroll trigger JS targeting
- `passive: true` flag on scroll event listener (performance optimization)
- Floating Contact Us at bottom-right or bottom-left with min 44px tap target

**What was rejected:**
- Tim Claw Max uses `details`/`summary` for TOC/FAQ (inconsistent with Codex approach)
- Tim Claw Max workflow (16KB) is a simplified structure — Codex 63-node pipeline retained
- Green (#8AD628) teal variant — Copilot uses #0fb5b0 per brand spec

---

## Alternate Agent Reference: agent-zero 2026-04-16

**File size:** 60KB HTML, 8KB prompt, 9KB workflow

**What was borrowed/merged:**
- Expanded section count and article depth (agent-zero produced 60KB article)
- "Did You Know" callout block pattern (amber/teal style)
- "How-To" inline callout blocks between sections

**What was rejected:**
- agent-zero 9KB workflow is too minimal (webhook-only structure, missing Google Sheets, WordPress integration)
- agent-zero prompt is the shortest (8KB) — insufficient for enterprise B2B quality level
- Different image positioning strategy

---

## Summary of Consolidation Decisions

| Feature | Source Adopted | Rationale |
|---|---|---|
| TOC: `<ul>` with `list-style:none` | Tim Claw Max / Claude Code spec | Explicitly removes numbers per mission requirement |
| Author: horizontal logo (not circular) | Tim Claw Max | Mission hard rule: no border-radius:50% |
| Author: social links with hover colors | Claude Code / Tim Claw Max | Mission requirement for Facebook, LinkedIn, Twitter |
| Author: Contact PowerPlug button | Tim Claw Max | Mission requirement |
| Scroll-to-top 300px trigger | Tim Claw Max | Mission requirement: only after 300px scroll |
| Font: Montserrat first in stack | Mission spec / Claude Code | Brand font spec |
| Color: #0fb5b0 teal | Copilot 2026-04-16 | Mission brand spec (teal accent) |
| Workflow: 63 nodes | Codex | Most complete production pipeline |
| Inline onclick (not details/summary) | Codex | More WordPress-safe across editor versions |
| N8N injection variables preserved exactly | All sources (consistent) | Non-negotiable per mission |