# Phase 4: Navigation & Table of Contents - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the TOC section replacing the stub in the template. Details/summary accordion, closed by default, single column, no numbering, Hebrew title, hover states with inline JS, plus/minus indicator animation.

</domain>

<decisions>
## Implementation Decisions

### TOC Structure (all locked by spec)
- Position: near top of article, after intro/summary card
- Structure: details/summary HTML elements
- Default state: closed
- Layout: single column
- Numbering: none
- Title: exactly "תוכן עניינים"
- Anchors: point to correct H2 heading IDs (section-1 through section-6 + faq, author)

### Hover & Animation (locked by spec)
- TOC link hover: underline + subtle color shift (accent #c8a97e)
- Accordion indicator: plus/minus with smooth transition
- All hover states via inline onmouseover/onmouseout JS handlers (WordPress-safe)
- Animation via CSS transition on inline style (if WP allows) or JS-driven

### Claude's Discretion
- Exact plus/minus Unicode character (+ → − or ▸ → ▾)
- TOC link spacing and padding values
- Smooth scroll behavior approach

</decisions>

<code_context>
## Existing Code Insights

### Current Template
- claude-code/Files/Improved_HTML_Template-claude-code-2026-03-25.html (97 lines)
- Has TOC stub section ready for replacement
- 9 H2 headings with anchor IDs available for TOC links

</code_context>

<specifics>
## Specific Ideas

No specific requirements beyond spec — all decisions locked.

</specifics>

<deferred>
## Deferred Ideas

None

</deferred>
