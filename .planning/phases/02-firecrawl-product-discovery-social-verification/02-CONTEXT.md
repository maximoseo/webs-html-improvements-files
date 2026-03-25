# Phase 2: Firecrawl Product Discovery & Social Verification - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Use Firecrawl to crawl hipsterstyle.co.il inner pages, discover real product pages relevant to kids styling tips, extract product data (titles, images, URLs), and verify social media profiles (Instagram, Facebook, YouTube, etc.). All data must be real — no invented URLs, no placeholder content.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — infrastructure/data discovery phase:
- Firecrawl crawl strategy (sitemap vs deep crawl vs targeted inner page discovery)
- Product relevance filtering criteria (kids clothing, styling accessories, etc.)
- Social profile verification approach (Firecrawl scrape of footer/contact pages)
- Image stability assessment (which product images need Supabase hosting)
- Data format for extracted products (JSON structure for downstream template use)

</decisions>

<code_context>
## Existing Code Insights

### Firecrawl Integration
- Firecrawl MCP tools available: firecrawl_scrape, firecrawl_crawl, firecrawl_map, firecrawl_search, firecrawl_extract
- Main site: https://hipsterstyle.co.il/
- Article topic: kids styling tips — products must be relevant to this subject

### Site Reference Migration Map (from Phase 1)
- 58 replacement points mapped across 3 files (oritmartin.com → hipsterstyle.co.il)
- Social links currently point to oritmartin.com profiles
- Need to discover hipsterstyle.co.il's actual social profiles

### Known Constraints
- Products must link to real pages on hipsterstyle.co.il
- No prices (link to live pages instead)
- Skip products without usable images
- Only kids-styling-relevant products in final set

</code_context>

<specifics>
## Specific Ideas

No specific requirements — follow Firecrawl best practices for e-commerce product discovery.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>
