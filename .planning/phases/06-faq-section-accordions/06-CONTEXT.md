# Phase 6: FAQ Section & Accordions - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Replace FAQ stub in template with individual closed accordion items using details/summary. No numbering, plus/minus animation, hover emphasis on headers. Positioned before author section.

</domain>

<decisions>
## Implementation Decisions

### FAQ Structure (all locked by spec)
- Position: before author section
- No numbering on questions
- Each question: separate details/summary accordion item
- All items start closed by default (no "open" attribute)
- WordPress-safe details/summary structure
- Plus/minus indicator with subtle open/close animation (same pattern as TOC)
- Hover emphasis on FAQ headers without hurting readability

### FAQ Content
- Questions/answers are N8N-templated (use placeholder Hebrew text for now)
- 5-7 FAQ items typical for this article type
- FAQ schema markup will be added in Phase 8 (SEO)

### Claude's Discretion
- Exact FAQ question/answer placeholder text
- Spacing between FAQ items
- Header font size within the accordion

</decisions>

<code_context>
## Existing Code Insights

### Current Template
- claude-code/Files/Improved_HTML_Template-claude-code-2026-03-25.html
- Has FAQ stub section ready for replacement
- TOC already has working plus/minus pattern (Phase 4) — reuse same approach

</code_context>

<specifics>
## Specific Ideas

Reuse the same ontoggle plus/minus pattern from the TOC accordion.

</specifics>

<deferred>
## Deferred Ideas

FAQ JSON-LD schema — Phase 8

</deferred>
