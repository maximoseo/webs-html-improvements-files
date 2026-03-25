# Phase 5: Product Card Integration - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the product card grid replacing the products stub in the template. Uses 6 products from hipsterstyle-discovery.json with Supabase-hosted images. Cards: image above, text below, uniform size, no overlay, no prices.

</domain>

<decisions>
## Implementation Decisions

### Card Layout (locked by spec + Phase 1 audit)
- Image above, text/title below in separate clean text area
- Clear spacing between image and text
- All cards same overall size and aligned
- No text overlay on images
- No display:flex/grid — use inline-block with percentage widths
- Responsive: 3 cards per row desktop, 2 tablet, 1 mobile (via percentage widths + inline-block)

### Image Handling (locked by spec)
- Use img tags, NOT CSS background-image
- object-fit: contain (if WP allows) for proportional display
- Height: auto for natural proportions
- Source: Supabase public URLs from hipsterstyle-discovery.json
- No broken, cut, or distorted images

### Product Data (locked by spec + Phase 2)
- 6 products from hipsterstyle-discovery.json
- No prices displayed — link to live product pages
- Real product URLs only — no invented links
- No empty cards, no cards without images

### Claude's Discretion
- Card border/shadow styling details
- Image height constraint value
- CTA button text (Hebrew)
- Card hover effect (subtle, premium)

</decisions>

<code_context>
## Existing Code Insights

### Discovery Data
- .planning/phases/02-firecrawl-product-discovery-social-verification/data/hipsterstyle-discovery.json
- 6 products with Supabase image URLs, titles, product page URLs

### Current Template
- claude-code/Files/Improved_HTML_Template-claude-code-2026-03-25.html
- Has products stub section ready for replacement
- Using inline-block layout system established in Phase 3

</code_context>

<specifics>
## Specific Ideas

Cards should feel premium and editorial — not a typical e-commerce grid. Clean, minimal, balanced.

</specifics>

<deferred>
## Deferred Ideas

None

</deferred>
