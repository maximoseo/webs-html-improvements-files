# Requirements: HipsterStyle Article System Rebuild

**Defined:** 2026-03-25
**Core Value:** Final HTML must be 100% WordPress-safe, premium, and production-grade

## v1 Requirements

### Template Structure

- [x] **TMPL-01**: Article wrapped in `<article>` tags with no content outside wrapper
- [x] **TMPL-02**: Full RTL Hebrew layout with dir="rtl" and lang="he"
- [x] **TMPL-03**: All CSS delivered via inline style attributes — zero `<style>` blocks
- [x] **TMPL-04**: Responsive layout without media queries using clamp()/percentages/auto-fill
- [x] **TMPL-05**: Semantic H2/H3 heading hierarchy throughout article
- [x] **TMPL-06**: Premium editorial whitespace, typography, and visual hierarchy
- [x] **TMPL-07**: No external CSS/JS dependencies, no CDN links
- [x] **TMPL-08**: No HTML comments, no markdown, no code fences in output

### Navigation & TOC

- [x] **NAV-01**: Table of Contents positioned near top of article (after intro/summary)
- [x] **NAV-02**: TOC starts closed by default using details/summary
- [x] **NAV-03**: Single column TOC layout, no numbering on items
- [x] **NAV-04**: All TOC anchors point to correct heading IDs
- [x] **NAV-05**: TOC title is exactly "תוכן עניינים" for Hebrew
- [x] **NAV-06**: Hover state with underline and subtle color shift on TOC items
- [x] **NAV-07**: Polished accordion open/close indicator animation

### Product Integration

- [x] **PROD-01**: Firecrawl discovers real product pages from hipsterstyle.co.il inner pages
- [x] **PROD-02**: Only products relevant to article topic are selected
- [x] **PROD-03**: Product cards display image above, text/title below in separate area
- [x] **PROD-04**: All product cards are uniform size and aligned
- [x] **PROD-05**: No text overlay on product images, clear spacing between image and text
- [x] **PROD-06**: Images never cut, broken, or distorted — use img tags with object-fit
- [x] **PROD-07**: No empty cards, no cards without images, no duplicate images
- [x] **PROD-08**: Links go to real product pages — no invented URLs
- [x] **PROD-09**: No prices displayed (link to live pages for current pricing)
- [x] **PROD-10**: Unstable images hosted via Supabase with stable public URLs

### FAQ Section

- [x] **FAQ-01**: FAQ section positioned before author section
- [x] **FAQ-02**: No numbering on FAQ questions
- [x] **FAQ-03**: Each question is separate accordion item using details/summary
- [x] **FAQ-04**: All FAQ items start closed by default
- [x] **FAQ-05**: Clean WordPress-safe accordion structure
- [x] **FAQ-06**: Polished plus/minus indicator with subtle open/close animation
- [x] **FAQ-07**: Hover emphasis on FAQ headers without hurting readability

### Author & Social

- [ ] **AUTH-01**: About the Author section is the final section — nothing appears after it
- [ ] **AUTH-02**: Author section includes logo image, visually centered and balanced
- [x] **AUTH-03**: Social links with correct verified URLs
- [x] **AUTH-04**: Firecrawl verifies real active social profiles and YouTube channel
- [x] **AUTH-05**: Only verified real profiles added — no invented links
- [ ] **AUTH-06**: Brand-color hover on each social network icon
- [ ] **AUTH-07**: Social area is elegant and non-spammy

### Floating UI

- [ ] **FLOAT-01**: Floating Back to Top button that scrolls to top
- [ ] **FLOAT-02**: Floating Contact Us button linking to real contact page
- [ ] **FLOAT-03**: Buttons are professional, minimal, and do not overlap content
- [ ] **FLOAT-04**: No duplication of existing floating UI actions
- [ ] **FLOAT-05**: On tablet/mobile, buttons resize/reposition to avoid obstructing content

### N8N Integration

- [ ] **N8N-01**: Improved N8N Prompt TXT contains exact injection block (non-negotiable)
- [ ] **N8N-02**: Products injection: `{{ JSON.stringify($json["products"], null, 2) }}`
- [ ] **N8N-03**: Content injection: `{{ $("Writing Blog").first().json.output }}`
- [ ] **N8N-04**: Hebrew instruction line present exactly as specified
- [ ] **N8N-05**: Image URL lines for sections 1-4 and hero exactly as specified
- [ ] **N8N-06**: No extra JSON/N8N injection lines beyond the specified block
- [ ] **N8N-07**: Workflow JSON updated and aligned to new prompt + template
- [ ] **N8N-08**: Two-phase LLM generation pattern (content then HTML rendering)

### SEO & Schema

- [ ] **SEO-01**: Article schema (JSON-LD) markup embedded
- [ ] **SEO-02**: FAQ schema markup for FAQ section
- [ ] **SEO-03**: Proper heading hierarchy for SEO crawlers

### Hover States

- [x] **HOVER-01**: TOC items: underline + subtle color shift on hover
- [x] **HOVER-02**: FAQ headers: subtle emphasis without hurting readability
- [ ] **HOVER-03**: CTA button: premium professional hover effect
- [ ] **HOVER-04**: Social links: network brand-color hover
- [ ] **HOVER-05**: All hover states remain readable and WordPress-safe (inline JS handlers)

### WordPress Safety

- [x] **WP-01**: Inline CSS only — survives wp_kses_post() sanitization
- [x] **WP-02**: No style blocks, no external CSS, no external JS
- [x] **WP-03**: Accordion stable inside WordPress post content
- [x] **WP-04**: Anchor IDs reliable after WordPress processing
- [x] **WP-05**: Floating buttons do not conflict with theme UI
- [x] **WP-06**: Images use durable URLs (Supabase-backed if needed)
- [x] **WP-07**: No hidden text risk on hover states
- [x] **WP-08**: RTL alignment verified for WordPress rendering

### File Delivery

- [ ] **DEL-01**: HTML template file dated 2026-03-25 with -claude-code- suffix
- [ ] **DEL-02**: N8N prompt TXT file dated 2026-03-25 with -claude-code- suffix
- [ ] **DEL-03**: N8N workflow JSON file dated 2026-03-25 with -claude-code- suffix
- [ ] **DEL-04**: Files saved to ./claude-code/Files/ locally
- [ ] **DEL-05**: Files uploaded to Dropbox target directory
- [ ] **DEL-06**: Old files deleted from Dropbox before upload
- [x] **DEL-07**: Before/after audit summary produced
- [x] **DEL-08**: WordPress rendering risk review completed

## v2 Requirements

### Advanced Features

- **ADV-01**: Multi-language support beyond Hebrew
- **ADV-02**: A/B testing of article templates
- **ADV-03**: Analytics integration for article performance
- **ADV-04**: Automated image optimization pipeline
- **ADV-05**: Dynamic product price updates via API

## Out of Scope

| Feature | Reason |
|---------|--------|
| Custom WordPress plugin | Pure HTML template — no PHP |
| CMS admin interface | Output is static article HTML |
| Payment/e-commerce integration | Display products only, link to store |
| Video hosting | Link to external only |
| Custom fonts via CDN | WordPress strips link tags |
| CSS Grid/Flexbox | Not on wp_kses safe_style_css whitelist |
| Media queries | Stripped with style blocks |
| JavaScript frameworks | WordPress strips script tags |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| TMPL-01 | Phase 3 | Complete |
| TMPL-02 | Phase 3 | Complete |
| TMPL-03 | Phase 3 | Complete |
| TMPL-04 | Phase 3 | Complete |
| TMPL-05 | Phase 3 | Complete |
| TMPL-06 | Phase 3 | Complete |
| TMPL-07 | Phase 3 | Complete |
| TMPL-08 | Phase 3 | Complete |
| NAV-01 | Phase 4 | Complete |
| NAV-02 | Phase 4 | Complete |
| NAV-03 | Phase 4 | Complete |
| NAV-04 | Phase 4 | Complete |
| NAV-05 | Phase 4 | Complete |
| NAV-06 | Phase 4 | Complete |
| NAV-07 | Phase 4 | Complete |
| PROD-01 | Phase 2 | Complete |
| PROD-02 | Phase 2 | Complete |
| PROD-03 | Phase 5 | Complete |
| PROD-04 | Phase 5 | Complete |
| PROD-05 | Phase 5 | Complete |
| PROD-06 | Phase 5 | Complete |
| PROD-07 | Phase 5 | Complete |
| PROD-08 | Phase 2 | Complete |
| PROD-09 | Phase 5 | Complete |
| PROD-10 | Phase 5 | Complete |
| FAQ-01 | Phase 6 | Complete |
| FAQ-02 | Phase 6 | Complete |
| FAQ-03 | Phase 6 | Complete |
| FAQ-04 | Phase 6 | Complete |
| FAQ-05 | Phase 6 | Complete |
| FAQ-06 | Phase 6 | Complete |
| FAQ-07 | Phase 6 | Complete |
| AUTH-01 | Phase 7 | Pending |
| AUTH-02 | Phase 7 | Pending |
| AUTH-03 | Phase 2 | Complete |
| AUTH-04 | Phase 2 | Complete |
| AUTH-05 | Phase 2 | Complete |
| AUTH-06 | Phase 7 | Pending |
| AUTH-07 | Phase 7 | Pending |
| FLOAT-01 | Phase 7 | Pending |
| FLOAT-02 | Phase 7 | Pending |
| FLOAT-03 | Phase 7 | Pending |
| FLOAT-04 | Phase 7 | Pending |
| FLOAT-05 | Phase 7 | Pending |
| N8N-01 | Phase 9 | Pending |
| N8N-02 | Phase 9 | Pending |
| N8N-03 | Phase 9 | Pending |
| N8N-04 | Phase 9 | Pending |
| N8N-05 | Phase 9 | Pending |
| N8N-06 | Phase 9 | Pending |
| N8N-07 | Phase 9 | Pending |
| N8N-08 | Phase 9 | Pending |
| SEO-01 | Phase 8 | Pending |
| SEO-02 | Phase 8 | Pending |
| SEO-03 | Phase 8 | Pending |
| HOVER-01 | Phase 4 | Complete |
| HOVER-02 | Phase 6 | Complete |
| HOVER-03 | Phase 7 | Pending |
| HOVER-04 | Phase 7 | Pending |
| HOVER-05 | Phase 8 | Pending |
| WP-01 | Phase 1 | Complete |
| WP-02 | Phase 1 | Complete |
| WP-03 | Phase 1 | Complete |
| WP-04 | Phase 1 | Complete |
| WP-05 | Phase 1 | Complete |
| WP-06 | Phase 1 | Complete |
| WP-07 | Phase 1 | Complete |
| WP-08 | Phase 1 | Complete |
| DEL-01 | Phase 10 | Pending |
| DEL-02 | Phase 10 | Pending |
| DEL-03 | Phase 10 | Pending |
| DEL-04 | Phase 10 | Pending |
| DEL-05 | Phase 10 | Pending |
| DEL-06 | Phase 10 | Pending |
| DEL-07 | Phase 1 | Complete |
| DEL-08 | Phase 1 | Complete |

**Coverage:**
- v1 requirements: 76 total
- Mapped to phases: 76
- Unmapped: 0

---
*Requirements defined: 2026-03-25*
*Last updated: 2026-03-25 after roadmap creation*
