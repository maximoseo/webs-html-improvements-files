# HipsterStyle Article System Rebuild

## What This Is

A full audit, professional redesign, and production-grade rebuild of the HipsterStyle WordPress article system. Produces 3 deliverables: an improved HTML template, an improved N8N prompt, and an improved N8N workflow JSON — all WordPress-hardened and ready for live deployment on mahsan.websreport.net.

## Core Value

The final HTML output must be 100% WordPress-safe, premium, and production-grade — anything fragile will break in WordPress.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Full audit of existing baseline files (HTML template, N8N prompt, N8N workflow)
- [ ] Firecrawl product discovery from hipsterstyle.co.il inner pages
- [ ] Firecrawl social profile / YouTube channel verification
- [ ] TOC near top, closed by default, single column, no numbering, correct anchors
- [ ] Product cards: image above, text below, uniform size, no overlay text
- [ ] Images never cut/broken/distorted — use img tags, object-fit contain
- [ ] Pixel-perfect TOC and FAQ accordion with polished open/close animation
- [ ] Polished hover states for TOC, FAQ, CTA, social links
- [ ] FAQ before author section, no numbering, separate closed accordions
- [ ] Floating Contact Us and Back to Top buttons
- [ ] About the Author section with logo and verified social links as final section
- [ ] WordPress-safe inline CSS only — no style blocks, no external deps
- [ ] Article wrapped in `<article>` tags, no content outside
- [ ] RTL support for Hebrew content
- [ ] Mobile/tablet/desktop responsive QA validation
- [ ] N8N prompt must contain exact injection block (non-negotiable)
- [ ] N8N workflow JSON updated and aligned to new prompt + template
- [ ] Supabase image hosting if asset stability requires it
- [ ] WordPress rendering risk review and mitigation
- [ ] Files saved to ./claude-code/Files/ locally
- [ ] Upload to Dropbox: /Webs/HTML IMPROVMENT FILES/hipsterstyle.co.il/claude-code/Files

### Out of Scope

- Mobile app — web/WordPress only
- Multi-language i18n system — Hebrew content only per article
- Custom WordPress plugin development — pure HTML/CSS template
- CMS admin interface — output is static article HTML
- Payment/e-commerce integration — display products only
- Video hosting — link to external only

## Context

- **WordPress URL:** https://mahsan.websreport.net/kids-styling-tips-guide-21/
- **Main Site:** https://hipsterstyle.co.il/
- **Existing baselines:** wp-n8n-html-design-improver/ directory contains previous versions
- **Three dated files from earlier today exist** — these are the starting baselines to audit and improve
- **Environment:** N8N workflow automation, Supabase for asset hosting, Firecrawl for crawling
- **Content direction:** Hebrew RTL, kids styling tips article
- **The output goes into real WordPress** — must account for WordPress rendering quirks

## Constraints

- **Inline CSS only**: WordPress strips style blocks — all CSS must be inline
- **No external dependencies**: No external CSS/JS, no CDN links for styles
- **WordPress-safe HTML**: article tag wrapper, no markdown, no code fences, no comments
- **Exact N8N injection block**: The TXT prompt must contain the exact injection expressions (non-negotiable)
- **File naming**: Files must be dated exactly 2026-03-25 with -claude-code- suffix
- **Local path**: Final files in ./claude-code/Files/ — not generic shared folders
- **Dropbox target**: /Webs/HTML IMPROVMENT FILES/hipsterstyle.co.il/claude-code/Files

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Inline CSS only | WordPress strips style blocks | -- Pending |
| Firecrawl for product discovery | Need real product data from hipsterstyle.co.il | -- Pending |
| Supabase for unstable images | WordPress may break external image URLs | -- Pending |
| Hebrew RTL layout | Target audience is Hebrew-speaking | -- Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check -- still the right priority?
3. Audit Out of Scope -- reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-25 after initialization*
