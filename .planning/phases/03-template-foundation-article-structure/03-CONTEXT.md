# Phase 3: Template Foundation & Article Structure - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the core article wrapper HTML with RTL Hebrew layout, all-inline CSS architecture, responsive design via clamp()/percentages (no media queries), semantic H2/H3 heading hierarchy, and premium editorial typography. This is the foundation all subsequent phases build upon.

</domain>

<decisions>
## Implementation Decisions

### Layout Architecture
- Use `inline-block` with percentage widths for layout (NOT flex/grid — `display` not on WP safe_style_css whitelist)
- Max article width: 780px (premium editorial, readable line length)
- Base font size: clamp(16px, 2.5vw, 19px) for responsive without media queries
- Section spacing: 48px between major sections, 24px within sections

### Typography & RTL
- Font family: `'Arial', 'Helvetica Neue', sans-serif` — safe in all WP themes, no CDN
- Heading scale: H2 clamp(22px,3vw,28px), H3 clamp(18px,2.5vw,22px)
- Colors: Body #2d2d2d, Headings #1a1a1a, Accent #c8a97e (warm gold)
- RTL: `text-align: right` on all text elements (explicit, WP-safe)

### Content Structure
- 2-3 paragraph intro with hero image, then "In This Article" summary card
- Section dividers: subtle 1px border-top in #e8e0d4 (warm neutral)
- "In This Article" card: light background #f9f6f1, 1px border #e8e0d4, 16px padding
- Stub H2 sections for TOC, Products, FAQ, Author with markers for subsequent phases

### Claude's Discretion
- Exact paragraph content for intro (will be N8N-templated)
- Hero image placement and sizing approach
- Specific heading text (Hebrew content from N8N)
- Internal spacing of the "In This Article" card items

</decisions>

<code_context>
## Existing Code Insights

### Baseline Template
- wp-n8n-html-design-improver/Improved_HTML_Template-claude-code-2026-03-25.html (307 lines)
- Has style block on lines 2-18 that MUST be eliminated
- 54 uses of display property that must be replaced with inline-block/float
- 38 dead class attributes to remove

### Phase 1 Audit Findings
- 34 issues documented: 11 CRITICAL, 9 HIGH, 11 MEDIUM, 3 LOW
- display property is the #1 issue (64 occurrences)
- All hover transitions in style block will be lost — need inline JS handlers

### Discovery Data (Phase 2)
- hipsterstyle-discovery.json has all product/social/brand data
- Brand accent color should align with hipsterstyle.co.il branding

</code_context>

<specifics>
## Specific Ideas

- The template must start with `<article dir="rtl" lang="he">` and end with `</article>`
- Zero style blocks, zero class selectors, zero external dependencies
- Must be a complete working HTML fragment (not a full page)
- Placeholder sections for Phases 4-8 content

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>
