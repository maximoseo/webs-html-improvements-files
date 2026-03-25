# Roadmap: HipsterStyle Article System Rebuild

## Overview

Rebuild the HipsterStyle WordPress article system from audit through delivery. Starting with a full audit of existing baselines and Firecrawl product discovery, then rebuilding the HTML template section-by-section (foundation, TOC, products, FAQ, author/social, floating UI), aligning the N8N prompt and workflow JSON, running WordPress-safe QA validation, and finally packaging and delivering all three dated files. Every phase produces observable, verifiable output.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Baseline Audit & WordPress Risk Assessment** - Audit existing HTML template, N8N prompt, and workflow JSON; document every WordPress-unsafe pattern
- [ ] **Phase 2: Firecrawl Product Discovery & Social Verification** - Crawl hipsterstyle.co.il for real product data and verify social profile URLs
- [ ] **Phase 3: Template Foundation & Article Structure** - Build the core article wrapper with RTL, inline CSS, semantic hierarchy, and responsive layout
- [ ] **Phase 4: Navigation & Table of Contents** - Build the TOC section with closed-by-default accordion, correct anchors, and hover states
- [ ] **Phase 5: Product Card Integration** - Build uniform product cards with Firecrawl data, Supabase image hosting, and WordPress-safe layout
- [ ] **Phase 6: FAQ Section & Accordions** - Build FAQ accordion section with individual details/summary items and polished animations
- [ ] **Phase 7: Author Section, Social Links & Floating UI** - Build author bio with verified social links and floating Back to Top / Contact buttons
- [ ] **Phase 8: SEO Schema & Hover States Polish** - Add JSON-LD article/FAQ schema and finalize all hover state interactions
- [ ] **Phase 9: N8N Prompt & Workflow Alignment** - Rebuild N8N prompt TXT with exact injection block and update workflow JSON to match new template
- [ ] **Phase 10: QA Validation & File Delivery** - WordPress rendering QA, responsive testing, file packaging with dated names, and Dropbox upload

## Phase Details

### Phase 1: Baseline Audit & WordPress Risk Assessment
**Goal**: Complete understanding of what exists, what breaks in WordPress, and what must change
**Depends on**: Nothing (first phase)
**Requirements**: WP-01, WP-02, WP-03, WP-04, WP-05, WP-06, WP-07, WP-08, DEL-07, DEL-08
**Success Criteria** (what must be TRUE):
  1. Every WordPress-unsafe pattern in the existing HTML template is documented with line numbers and fix strategy
  2. Existing N8N prompt and workflow JSON have been reviewed and gaps documented
  3. A before-state audit summary exists capturing current template structure, CSS approach, and known issues
  4. WordPress rendering risk review is complete with wp_kses_post() impact analysis
  5. A prioritized list of required changes drives all subsequent phases
**Plans**: 3 plans

Plans:
- [x] 01-01-PLAN.md -- HTML template risk inventory and site reference migration map (Wave 1)
- [x] 01-02-PLAN.md -- N8N prompt contradiction report and workflow logic bug report (Wave 1)
- [x] 01-03-PLAN.md -- Consolidated WordPress rendering risk summary and prioritized change list (Wave 2)

### Phase 2: Firecrawl Product Discovery & Social Verification
**Goal**: Real product data and verified social links are available for template integration
**Depends on**: Phase 1
**Requirements**: PROD-01, PROD-02, PROD-08, AUTH-03, AUTH-04, AUTH-05
**Success Criteria** (what must be TRUE):
  1. Firecrawl has crawled hipsterstyle.co.il inner pages and extracted real product data (titles, images, URLs)
  2. Only products relevant to the article topic (kids styling tips) are in the final product set
  3. All product URLs resolve to real pages on hipsterstyle.co.il
  4. Social profile URLs (Instagram, Facebook, YouTube, etc.) have been verified as active and real
  5. No invented or placeholder URLs exist in the extracted data
**Plans**: 2 plans

Plans:
- [x] 02-01-PLAN.md -- Fetch product data from Shopify JSON API, verify URLs, download images (Wave 1)
- [x] 02-02-PLAN.md -- Upload images to Supabase, verify social/contact URLs, assemble consolidated discovery JSON (Wave 2)

### Phase 3: Template Foundation & Article Structure
**Goal**: A WordPress-safe article skeleton with RTL, inline CSS, semantic headings, and responsive layout is ready for section content
**Depends on**: Phase 1
**Requirements**: TMPL-01, TMPL-02, TMPL-03, TMPL-04, TMPL-05, TMPL-06, TMPL-07, TMPL-08
**Success Criteria** (what must be TRUE):
  1. Article is wrapped in `<article dir="rtl" lang="he">` with no content outside the wrapper
  2. All CSS is delivered via inline style attributes -- zero `<style>` blocks, zero class-based selectors
  3. Responsive layout works using clamp()/percentages/auto-fill with no media queries
  4. Semantic H2/H3 heading hierarchy is in place with premium editorial whitespace and typography
  5. No external CSS/JS dependencies, no CDN links, no HTML comments, no markdown, no code fences
**Plans**: 2 plans

Plans:
- [x] 03-01-PLAN.md -- Article wrapper, RTL setup, inline CSS architecture, and "In This Article" summary card (Wave 1)
- [x] 03-02-PLAN.md -- Semantic heading hierarchy, responsive clamp() typography, editorial spacing, and stub sections for Phases 4-8 (Wave 2)

### Phase 4: Navigation & Table of Contents
**Goal**: Users can navigate the article via a polished, WordPress-safe TOC that starts closed and links to correct headings
**Depends on**: Phase 3
**Requirements**: NAV-01, NAV-02, NAV-03, NAV-04, NAV-05, NAV-06, NAV-07, HOVER-01
**Success Criteria** (what must be TRUE):
  1. TOC appears near the top of the article (after intro/summary) using details/summary element
  2. TOC starts closed by default, opens with polished animation, displays single-column with no numbering
  3. TOC title reads "תוכן עניינים" in Hebrew
  4. Every TOC link points to a correct heading ID anchor that survives WordPress processing
  5. TOC items show underline + subtle color shift on hover via inline JS handlers
**Plans**: 1 plan

Plans:
- [x] 04-01-PLAN.md -- Full TOC: anchor links to all H2 sections, hover states, plus/minus indicator (Wave 1)

### Phase 5: Product Card Integration
**Goal**: Real products from hipsterstyle.co.il display in uniform, WordPress-safe cards with stable images
**Depends on**: Phase 2, Phase 3
**Requirements**: PROD-03, PROD-04, PROD-05, PROD-06, PROD-07, PROD-09, PROD-10
**Success Criteria** (what must be TRUE):
  1. Product cards display image above and text/title below in separate areas -- no text overlay on images
  2. All product cards are uniform size and visually aligned
  3. Images are never cut, broken, or distorted -- using img tags with object-fit: contain
  4. No empty cards, no cards without images, no duplicate images, no prices displayed
  5. Unstable product images are hosted on Supabase with stable public URLs
**Plans**: 1 plan

Plans:
- [x] 05-01-PLAN.md -- 6 product cards with inline-block layout, Supabase images, real URLs, no prices (Wave 1)

### Phase 6: FAQ Section & Accordions
**Goal**: FAQ section renders as individual closed accordions with polished animations, positioned before author section
**Depends on**: Phase 3
**Requirements**: FAQ-01, FAQ-02, FAQ-03, FAQ-04, FAQ-05, FAQ-06, FAQ-07, HOVER-02
**Success Criteria** (what must be TRUE):
  1. FAQ section appears before the author section in document flow
  2. Each question is a separate details/summary accordion item -- no numbering
  3. All FAQ items start closed by default
  4. Plus/minus indicator animates smoothly on open/close
  5. FAQ headers show subtle emphasis on hover without hurting readability
**Plans**: 1 plan

Plans:
- [x] 06-01-PLAN.md -- Replace FAQ stub with 6 details/summary accordion items, plus/minus toggle, hover emphasis (Wave 1)

### Phase 7: Author Section, Social Links & Floating UI
**Goal**: Author bio with verified social links is the final article section, and floating buttons provide persistent navigation
**Depends on**: Phase 2, Phase 3
**Requirements**: AUTH-01, AUTH-02, AUTH-06, AUTH-07, FLOAT-01, FLOAT-02, FLOAT-03, FLOAT-04, FLOAT-05, HOVER-03, HOVER-04
**Success Criteria** (what must be TRUE):
  1. About the Author is the final section -- nothing appears after it in the article
  2. Author section includes logo image, visually centered, with only verified real social link URLs
  3. Social links show network brand-color on hover; social area is elegant and non-spammy
  4. Floating Back to Top and Contact Us buttons are visible, professional, and do not overlap content
  5. On tablet/mobile, floating buttons resize/reposition to avoid obstructing content
**Plans**: 1 plan

Plans:
- [x] 07-01-PLAN.md -- Author section with logo/bio/social links + floating Back to Top and Contact Us buttons (Wave 1)

### Phase 8: SEO Schema & Hover States Polish
**Goal**: Article and FAQ schema markup is embedded, and all hover state interactions are finalized and WordPress-safe
**Depends on**: Phase 4, Phase 6, Phase 7
**Requirements**: SEO-01, SEO-02, SEO-03, HOVER-05
**Success Criteria** (what must be TRUE):
  1. JSON-LD Article schema is embedded in the template
  2. JSON-LD FAQ schema covers all FAQ questions and answers
  3. Proper heading hierarchy is verified for SEO crawlers
  4. All hover states across TOC, FAQ, CTA, and social links remain readable and WordPress-safe via inline JS handlers
**Plans**: TBD

Plans:
- [ ] 08-01: Article and FAQ JSON-LD schema markup
- [ ] 08-02: SEO heading hierarchy verification
- [ ] 08-03: Cross-section hover state audit and WordPress safety check

### Phase 9: N8N Prompt & Workflow Alignment
**Goal**: N8N prompt TXT contains the exact injection block and workflow JSON produces output matching the new template
**Depends on**: Phase 8
**Requirements**: N8N-01, N8N-02, N8N-03, N8N-04, N8N-05, N8N-06, N8N-07, N8N-08
**Success Criteria** (what must be TRUE):
  1. N8N prompt contains the exact products injection: `{{ JSON.stringify($json["products"], null, 2) }}`
  2. N8N prompt contains the exact content injection: `{{ $("Writing Blog").first().json.output }}`
  3. Hebrew instruction line and image URL lines for sections 1-4 + hero are present exactly as specified
  4. No extra JSON/N8N injection lines exist beyond the specified block
  5. Workflow JSON implements two-phase LLM generation (content then HTML rendering) aligned to new template
**Plans**: TBD

Plans:
- [ ] 09-01: N8N prompt TXT rebuild with exact injection block
- [ ] 09-02: N8N workflow JSON update and alignment to new template
- [ ] 09-03: Two-phase LLM generation pattern validation

### Phase 10: QA Validation & File Delivery
**Goal**: All three deliverables are validated in WordPress, packaged with correct dated filenames, and delivered to local path and Dropbox
**Depends on**: Phase 9
**Requirements**: DEL-01, DEL-02, DEL-03, DEL-04, DEL-05, DEL-06
**Success Criteria** (what must be TRUE):
  1. HTML template renders correctly in WordPress on mahsan.websreport.net without broken styles or missing content
  2. Mobile, tablet, and desktop responsive behavior verified
  3. All three files (HTML, TXT, JSON) are dated 2026-03-25 with -claude-code- suffix
  4. Files exist in ./claude-code/Files/ locally
  5. Files uploaded to Dropbox at /Webs/HTML IMPROVMENT FILES/hipsterstyle.co.il/claude-code/Files after removing old files
**Plans**: TBD

Plans:
- [ ] 10-01: WordPress rendering validation on mahsan.websreport.net
- [ ] 10-02: Responsive QA across mobile, tablet, and desktop viewports
- [ ] 10-03: File packaging with dated naming convention
- [ ] 10-04: Local save to ./claude-code/Files/ and Dropbox upload

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Baseline Audit & WordPress Risk Assessment | 3/3 | Complete | 2026-03-25 |
| 2. Firecrawl Product Discovery & Social Verification | 2/2 | Complete | 2026-03-25 |
| 3. Template Foundation & Article Structure | 2/2 | Complete | 2026-03-25 |
| 4. Navigation & Table of Contents | 1/1 | Complete | 2026-03-25 |
| 5. Product Card Integration | 0/1 | Planned | - |
| 6. FAQ Section & Accordions | 0/1 | Planned | - |
| 7. Author Section, Social Links & Floating UI | 0/1 | Not started | - |
| 8. SEO Schema & Hover States Polish | 0/3 | Not started | - |
| 9. N8N Prompt & Workflow Alignment | 0/3 | Not started | - |
| 10. QA Validation & File Delivery | 0/4 | Not started | - |
