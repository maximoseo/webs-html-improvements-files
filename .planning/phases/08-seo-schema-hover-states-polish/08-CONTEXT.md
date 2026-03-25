# Phase 8: SEO Schema & Hover States Polish - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Add JSON-LD Article and FAQ schema markup to the template. Audit and finalize all hover state interactions across TOC, FAQ, CTA, and social links for WordPress safety.

</domain>

<decisions>
## Implementation Decisions

### SEO Schema (locked by spec)
- Article schema (JSON-LD) with proper headline, author, datePublished
- FAQ schema (JSON-LD) covering all FAQ questions and answers
- Proper heading hierarchy verified for crawlers
- Schema embedded as script type="application/ld+json" inside article

### Hover States Polish (locked by spec)
- All hover states must remain readable and WordPress-safe
- Implemented via inline onmouseover/onmouseout JS handlers
- Cross-section audit: TOC (Phase 4), FAQ (Phase 6), CTA+Social (Phase 7)
- Verify no hover state hides text or breaks layout

### Claude's Discretion
- JSON-LD schema property values (publisher, image, etc.)
- Whether to combine Article+FAQ schema or keep separate script tags
- Any hover state adjustments needed after cross-section audit

</decisions>

<code_context>
## Existing Code Insights

### Current Template
- TOC hover: underline + #c8a97e color shift (Phase 4)
- FAQ hover: bold + #c8a97e color shift (Phase 6)
- Social hover: FB #1877F2, IG #E4405F (Phase 7)
- CTA hover: #b8956e darker accent (Phase 7)
- All using onmouseover/onmouseout inline JS

</code_context>

<specifics>
## Specific Ideas

Schema should use hipsterstyle.co.il as publisher URL.

</specifics>

<deferred>
## Deferred Ideas

None

</deferred>
