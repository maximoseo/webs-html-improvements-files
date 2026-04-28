# WORKFLOW MAP — HTML REDESIGN SYSTEM 2026-04-20

## MAIN WORKFLOW: Article Redesign

```
INPUT (raw HTML / brief / existing article)
    │
    ▼
[B1] Brand Design System Extraction
    │  → Extract brand colors, fonts, spacing from site URL
    │  → Generate :root CSS tokens
    │
    ▼
[Module 11] Content Structure Planning
    │  → Identify sections: hero, TOC, content, FAQ, author, CTA
    │  → Plan H1/H2/H3 hierarchy
    │  → Draft anchor IDs for TOC
    │
    ▼
[Module 8] WordPress-Safe HTML Generation
    │  → Apply card patterns (div + overlay-a)
    │  → Set up <style> block at top
    │  → No inline JS, no block-in-anchor
    │
    ▼
[Module 9 if Hebrew] RTL Layout Engine
    │  → dir="rtl" lang="he" on wrapper
    │  → Flip margins/padding/borders
    │  → Hebrew font stack
    │
    ▼
[Module 10] TOC + FAQ
    │  → <details>/<summary> TOC
    │  → FAQ accordion items
    │  → Anchor links validated
    │
    ▼
[Module 13] Floating Buttons
    │  → Contact button → /contact/
    │  → Scroll-to-top button
    │  → Mobile: icon-only
    │
    ▼
[Module 14] CTA Engine
    │  → End-of-article CTA block
    │  → Brand-aligned colors
    │
    ▼
[Module 17] Accessibility Pass
    │  → Contrast ratios checked
    │  → Focus states added
    │  → ARIA labels on icon-only buttons
    │
    ▼
[Module 15] Pre-Delivery Validation
    │  → Full checklist run
    │  → wpautop simulation
    │  → Responsive breakpoint check
    │
    ▼
[Module 16] N8N Sync (if needed)
    │  → Insert {{TEMPLATE_VARS}}
    │  → Validate N8N function node
    │
    ▼
OUTPUT: Production-ready HTML
    │
    ├── Obsidian sync (PUT /vault/{path})
    └── GitHub push (push_to_github.sh)
```

## PARALLEL WORKFLOW: Large Redesign (Multi-Section)

```
[Harness Fan-out Pattern]
    │
    ├── Subagent A: Hero + TOC + Intro
    ├── Subagent B: Main content sections + callouts
    ├── Subagent C: Product grid + comparison tables
    └── Subagent D: FAQ + Author + CTA + Floating
    │
    ▼
[Synthesis Agent]: Merge all sections
    │
    ▼
[Module 15]: Final QA
    │
    ▼
DELIVERY
```

## WORKFLOW: Debug-Hypothesis (for broken HTML)

```
OBSERVE: What exactly is broken?
    │  → Screenshot at 3 viewports
    │  → Identify specific element/breakpoint
    │
    ▼
HYPOTHESIZE: List 3-5 possible causes
    │  → wpautop corruption?
    │  → Missing breakpoint?
    │  → Inline JS stripped?
    │  → Class conflict with theme?
    │  → sizes=auto conflict?
    │
    ▼
EXPERIMENT: One targeted fix, test immediately
    │
    ▼
CONCLUDE: Root cause confirmed → apply fix + document in SKILL
```

## WORKFLOW: AEO Article Optimization

```
CHECK SCORE:
    │  npx agentic-seo [URL]
    │  Target: ≥80/100
    │
    ├── Discovery issues → add llms.txt, AGENTS.md
    ├── Content structure → fix headings, add semantics
    ├── Token budget → trim to <8000 tokens/page
    ├── Capability signaling → add SKILL.md / schema
    └── UX Bridge → ensure markdown source available
    │
    ▼
OUTPUT: AEO-ready article
```
