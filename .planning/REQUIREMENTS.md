# Requirements: HipsterStyle Article System Rebuild

**Defined:** 2026-03-25
**Core Value:** Final HTML must be 100% WordPress-safe, premium, and production-grade

## v1 Requirements

### Template Structure

- [ ] **TMPL-01**: Article wrapped in `<article>` tags with no content outside wrapper
- [ ] **TMPL-02**: Full RTL Hebrew layout with dir="rtl" and lang="he"
- [ ] **TMPL-03**: All CSS delivered via inline style attributes — zero `<style>` blocks
- [ ] **TMPL-04**: Responsive layout without media queries using clamp()/percentages/auto-fill
- [ ] **TMPL-05**: Semantic H2/H3 heading hierarchy throughout article
- [ ] **TMPL-06**: Premium editorial whitespace, typography, and visual hierarchy
- [ ] **TMPL-07**: No external CSS/JS dependencies, no CDN links
- [ ] **TMPL-08**: No HTML comments, no markdown, no code fences in output

### Navigation & TOC

- [ ] **NAV-01**: Table of Contents positioned near top of article (after intro/summary)
- [ ] **NAV-02**: TOC starts closed by default using details/summary
- [ ] **NAV-03**: Single column TOC layout, no numbering on items
- [ ] **NAV-04**: All TOC anchors point to correct heading IDs
- [ ] **NAV-05**: TOC title is exactly "תוכן עניינים" for Hebrew
- [ ] **NAV-06**: Hover state with underline and subtle color shift on TOC items
- [ ] **NAV-07**: Polished accordion open/close indicator animation

### Product Integration

- [ ] **PROD-01**: Firecrawl discovers real product pages from hipsterstyle.co.il inner pages
- [ ] **PROD-02**: Only products relevant to article topic are selected
- [ ] **PROD-03**: Product cards display image above, text/title below in separate area
- [ ] **PROD-04**: All product cards are uniform size and aligned
- [ ] **PROD-05**: No text overlay on product images, clear spacing between image and text
- [ ] **PROD-06**: Images never cut, broken, or distorted — use img tags with object-fit
- [ ] **PROD-07**: No empty cards, no cards without images, no duplicate images
- [ ] **PROD-08**: Links go to real product pages — no invented URLs
- [ ] **PROD-09**: No prices displayed (link to live pages for current pricing)
- [ ] **PROD-10**: Unstable images hosted via Supabase with stable public URLs

### FAQ Section

- [ ] **FAQ-01**: FAQ section positioned before author section
- [ ] **FAQ-02**: No numbering on FAQ questions
- [ ] **FAQ-03**: Each question is separate accordion item using details/summary
- [ ] **FAQ-04**: All FAQ items start closed by default
- [ ] **FAQ-05**: Clean WordPress-safe accordion structure
- [ ] **FAQ-06**: Polished plus/minus indicator with subtle open/close animation
- [ ] **FAQ-07**: Hover emphasis on FAQ headers without hurting readability

### Author & Social

- [ ] **AUTH-01**: About the Author section is the final section — nothing appears after it
- [ ] **AUTH-02**: Author section includes logo image, visually centered and balanced
- [ ] **AUTH-03**: Social links with correct verified URLs
- [ ] **AUTH-04**: Firecrawl verifies real active social profiles and YouTube channel
- [ ] **AUTH-05**: Only verified real profiles added — no invented links
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

- [ ] **HOVER-01**: TOC items: underline + subtle color shift on hover
- [ ] **HOVER-02**: FAQ headers: subtle emphasis without hurting readability
- [ ] **HOVER-03**: CTA button: premium professional hover effect
- [ ] **HOVER-04**: Social links: network brand-color hover
- [ ] **HOVER-05**: All hover states remain readable and WordPress-safe (inline JS handlers)

### WordPress Safety

- [ ] **WP-01**: Inline CSS only — survives wp_kses_post() sanitization
- [ ] **WP-02**: No style blocks, no external CSS, no external JS
- [ ] **WP-03**: Accordion stable inside WordPress post content
- [ ] **WP-04**: Anchor IDs reliable after WordPress processing
- [ ] **WP-05**: Floating buttons do not conflict with theme UI
- [ ] **WP-06**: Images use durable URLs (Supabase-backed if needed)
- [ ] **WP-07**: No hidden text risk on hover states
- [ ] **WP-08**: RTL alignment verified for WordPress rendering

### File Delivery

- [ ] **DEL-01**: HTML template file dated 2026-03-25 with -claude-code- suffix
- [ ] **DEL-02**: N8N prompt TXT file dated 2026-03-25 with -claude-code- suffix
- [ ] **DEL-03**: N8N workflow JSON file dated 2026-03-25 with -claude-code- suffix
- [ ] **DEL-04**: Files saved to ./claude-code/Files/ locally
- [ ] **DEL-05**: Files uploaded to Dropbox target directory
- [ ] **DEL-06**: Old files deleted from Dropbox before upload
- [ ] **DEL-07**: Before/after audit summary produced
- [ ] **DEL-08**: WordPress rendering risk review completed

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
| TMPL-01 through TMPL-08 | Phase TBD | Pending |
| NAV-01 through NAV-07 | Phase TBD | Pending |
| PROD-01 through PROD-10 | Phase TBD | Pending |
| FAQ-01 through FAQ-07 | Phase TBD | Pending |
| AUTH-01 through AUTH-07 | Phase TBD | Pending |
| FLOAT-01 through FLOAT-05 | Phase TBD | Pending |
| N8N-01 through N8N-08 | Phase TBD | Pending |
| SEO-01 through SEO-03 | Phase TBD | Pending |
| HOVER-01 through HOVER-05 | Phase TBD | Pending |
| WP-01 through WP-08 | Phase TBD | Pending |
| DEL-01 through DEL-08 | Phase TBD | Pending |

**Coverage:**
- v1 requirements: 62 total
- Mapped to phases: 0 (pending roadmap)
- Unmapped: 62

---
*Requirements defined: 2026-03-25*
*Last updated: 2026-03-25 after initial definition*
