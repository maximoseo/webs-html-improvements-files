# Feature Landscape

**Domain:** WordPress article template system for e-commerce blog (Hebrew RTL, kids fashion/styling, product integration)
**Project:** HipsterStyle Article System Rebuild
**Researched:** 2026-03-25

## Table Stakes

Features users expect. Missing = article feels amateur or broken.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **RTL Hebrew layout** | Target audience is Hebrew-speaking; broken RTL = unusable | Med | `dir="rtl"` on article root, `text-align: right`, logical CSS properties. Must mirror all UI elements correctly. |
| **Responsive design (mobile/tablet/desktop)** | ~80% e-commerce traffic is mobile; broken mobile = lost readers | Med | Breakpoints: 480px, 768px, 1024px. Use `clamp()` for fluid typography. Grid auto-fit for product cards. |
| **Table of contents (collapsible)** | Long-form articles need navigation; users expect scannable structure | Low | `<details>/<summary>` with correct anchor links. Closed by default. Single column, no numbering. |
| **Product cards (image above, text below)** | Core e-commerce integration; links readers to products | Med | Uniform card size via CSS grid. Image container with `object-fit: contain`. CTA button per card. 250-350px card width desktop, full-width or 2-col mobile. |
| **FAQ accordion section** | SEO value (FAQ schema), user expectation for Q&A content | Low | Individual `<details>` elements, each independently closeable. No numbering. Placed before author section. |
| **About the Author section** | Builds credibility and trust; expected at article end | Low | Photo, name, bio (3-5 sentences, third person), social links with icons, contact buttons. |
| **Inline CSS only** | WordPress strips `<style>` blocks in many setups; broken styling = broken article | High | Every element needs inline styles. Hover states require `onmouseover`/`onmouseout` inline handlers or a scoped `<style>` block within `<article>`. This is the hardest constraint. |
| **WordPress-safe HTML** | Output goes into real WordPress; non-safe HTML = rendering failures | Med | `<article>` wrapper, no markdown, no code fences, no HTML comments, no external dependencies. |
| **Proper image handling** | Distorted/cut images = unprofessional | Low | `<img>` tags with `object-fit: contain`, `loading="lazy"`, `decoding="async"`. Fixed-height containers. No background-image CSS. |
| **Semantic headings hierarchy** | SEO, accessibility, screen readers | Low | h2 for sections, proper nesting. `aria-labelledby` on sections. |
| **External link safety** | Security baseline | Low | `target="_blank" rel="noopener"` on all external links. |
| **Article schema markup (JSON-LD)** | SEO; enables rich results in Google (headline, author, date) | Low | `<script type="application/ld+json">` with Article schema. Include headline, description, author, publisher, inLanguage. |
| **FAQ schema markup (JSON-LD)** | SEO; FAQ rich results drive CTR from search | Low | FAQPage schema matching visible FAQ content exactly. |

## Differentiators

Features that elevate from "functional template" to "premium editorial experience."

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Floating Contact/WhatsApp button** | Persistent conversion touchpoint; WhatsApp is primary contact in Israel | Low | Fixed position, z-index 999. Green WhatsApp circle (right side for RTL). Phone/contact on left. Must not overlap content on mobile. |
| **Back to Top button** | UX for long-form articles; reduces scroll fatigue | Low | Fixed position bottom-left (in RTL context). Smooth scroll via `href="#top"`. Pill or circle shape. |
| **Polished hover states** | Feel of interactivity and premium quality | Low | `onmouseover`/`onmouseout` inline JS for color/transform changes. Subtle `translateY(-1px)` lifts, color shifts. Keep transitions in scoped `<style>` block if available. |
| **Article summary box** | Quick scannable overview before deep reading | Low | Highlighted box near top with bullet points summarizing what article covers. Border accent (brand color). |
| **Accent border on headings** | Visual hierarchy and brand identity | Low | `border-right: 4px solid [brand-color]` with `padding-right` (RTL). Consistent across all h2s. |
| **Callout/highlight boxes** | Break up long text, emphasize key points | Low | Bordered box with background tint, bold intro text ("Key point:"). Used sparingly. |
| **Data tables** | Structured info presentation for comparison content | Med | Responsive overflow with `overflow-x: auto`. Min-width for usability. Styled headers. Alternating row colors. |
| **CTA button (primary)** | Drives traffic to product gallery/store | Low | Centered, pill-shaped, brand-color background. Max-width 320px. Shadow for depth. Hover lift effect. |
| **Social links with brand-colored hover** | Cross-platform engagement; builds author ecosystem | Low | Icon + text buttons. Each social platform gets its brand color on hover (Facebook blue, Instagram pink). |
| **Premium typography** | Readability and editorial quality feel | Low | `clamp()` responsive font sizes. Line-height 1.85-1.9. Arial/sans-serif for Hebrew clarity. Color #2f2f2f (not pure black). |
| **Smooth open/close animation on accordions** | Polish that separates amateur from professional templates | Low | CSS `transition: transform 0.3s ease` on icon rotation. `ontoggle` handler for `+` to `x` rotation. |
| **LocalBusiness schema** | Additional SEO for business with physical location | Low | JSON-LD with name, address, telephone, URL. Enhances Knowledge Panel potential. |

## Anti-Features

Features to explicitly NOT build. Each is tempting but harmful in this context.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Heavy JavaScript / complex animations** | WordPress may strip scripts; JS bloats load time; breaks in some WP themes | Use CSS transitions only (`transition` property). Use `<details>` for native accordion behavior. Inline `onmouseover`/`onmouseout` for hover states. |
| **External CSS/JS dependencies (CDN)** | External deps can fail, slow loading, get blocked by ad blockers | Everything inline or in a scoped `<style>` block. Zero external resources. |
| **`<style>` blocks (if WordPress strips them)** | Some WordPress setups strip style blocks from post content | Test whether target WordPress allows scoped style blocks. If not, fall back to 100% inline styles. The existing template uses a scoped `<style>` inside `<article>` which works in the current WP setup. |
| **Background images via CSS** | WordPress content filters may strip CSS backgrounds; harder to lazy-load | Use `<img>` tags with `object-fit` for all images. |
| **Complex multi-column layouts** | Break on mobile, hard to maintain with inline CSS, RTL complexity | Use single-column for text content. Grid only for product card sections with `auto-fit`. |
| **Video embeds** | Heavy, slow, requires external hosting/scripts | Link to external video (YouTube) with text link or thumbnail. No iframes in template. |
| **Custom fonts / Google Fonts** | External dependency, FOUT, blocks rendering, adds requests | Use system fonts: Arial, Helvetica, sans-serif. Hebrew renders well in Arial. |
| **Sticky headers / fixed navigation** | Eats viewport on mobile, conflicts with WordPress theme headers | TOC is collapsible within content flow. No fixed-position navigation bars. |
| **Infinite scroll / pagination** | Single article template, not a feed; adds unnecessary complexity | Single long-form article with TOC for navigation. |
| **Comment system** | Out of scope; WordPress handles comments at theme level | Rely on WordPress native comment system. Template does not include comment markup. |
| **Price display on product cards** | Prices change; stale prices in article HTML create user distrust | Show product name + image + "View Product" CTA that links to live product page with current price. |
| **i18n / multi-language** | Out of scope per PROJECT.md; Hebrew only | Hardcode `lang="he" dir="rtl"`. No language switching UI. |
| **WordPress plugin dependencies** | Template must be self-contained; plugins create maintenance burden | All features implemented in raw HTML/CSS. No shortcodes, no plugin-specific markup. |

## Feature Dependencies

```
RTL Hebrew Layout ─────────────────────┐
                                        ├──> All visual features depend on RTL being correct
Responsive Design ─────────────────────┘

Inline CSS Only ───────────────────────> Constrains ALL styling approaches
                                         (hover states, animations, grid layouts)

Semantic Headings ─────> TOC (needs anchors on h2s)
                    └──> Article Schema (uses heading as headline)

FAQ Accordion ─────────> FAQ Schema (must match visible content exactly)

Product Cards ─────────> Proper Image Handling (object-fit, lazy loading)
              └────────> CTA Button Pattern (reused on each card)

About the Author ──────> Social Links (nested inside author section)
                 └─────> Contact Buttons (phone, email, website)

Floating Buttons ──────> WhatsApp Button (fixed position right)
                └──────> Contact Button (fixed position left)
                └──────> Back to Top Button (fixed position left, below contact)
```

## MVP Recommendation

### Must Ship (Phase 1 - Core Template)

1. **RTL Hebrew layout** with correct `dir="rtl"` and mirrored UI
2. **Responsive design** with mobile-first breakpoints
3. **WordPress-safe HTML** with `<article>` wrapper and inline CSS
4. **Proper image handling** with `object-fit: contain`
5. **Semantic headings** with anchor IDs for TOC links
6. **Table of contents** (collapsible, closed by default)
7. **Product cards** (grid layout, image above text, CTA per card)
8. **FAQ accordion** (individual details/summary elements)
9. **Article + FAQ schema markup** (JSON-LD)

### Should Ship (Phase 2 - Polish)

10. **About the Author section** with social links
11. **Floating buttons** (WhatsApp, Contact, Back to Top)
12. **Hover states** on all interactive elements
13. **CTA button** (primary, centered, brand-colored)
14. **Article summary box** near top
15. **Accent borders** on headings
16. **Callout/highlight boxes** for key points
17. **LocalBusiness schema**

### Defer

- **Data tables**: Only if article content requires comparison data. Not every article needs them.
- **Social links with brand-colored hover**: Nice polish but not conversion-critical. Can ship with simple styled links first.

## Complexity Budget

| Complexity | Count | Features |
|-----------|-------|----------|
| **Low** | 15 | TOC, FAQ, author bio, image handling, headings, schema (x3), back-to-top, summary box, accent borders, callouts, CTA button, hover states, floating buttons |
| **Medium** | 4 | RTL layout, responsive design, product cards, data tables |
| **High** | 1 | Inline CSS constraint (affects everything; requires inline JS for hover states, careful style management) |

The inline CSS constraint is the single highest-complexity factor because it touches every other feature. Every hover state, every responsive behavior, every visual polish decision must work within this constraint.

## Sources

- [WordPress RTL Support - Jetpack](https://jetpack.com/resources/wordpress-rtl/)
- [WordPress i18n & RTL Best Practices - rtcamp](https://rtcamp.com/handbook/developing-for-block-editor-and-site-editor/i18n-rtl-support/)
- [CSS FAQ Accordion for Schema Markup](https://www.365i.co.uk/blog/2025/05/21/7-steps-to-the-best-css-faq-accordion-for-schema-markup/)
- [Styling Accordions in WordPress 6.9](https://developer.wordpress.org/news/2025/10/styling-accordions-in-wordpress-6-9/)
- [Fashion E-commerce CTA Best Practices - RevLifter](https://www.revlifter.com/blog/how-to-craft-high-converting-ctas-for-fashion-ecommerce)
- [Ecommerce CTA Strategies 2025 - FirstPier](https://www.firstpier.com/resources/ecommerce-call-to-action)
- [Product Card Design Examples - WPDean](https://wpdean.com/product-card-design/)
- [Typography Best Practices 2026](https://www.adoc-studio.app/blog/typography-guide)
- [Web Typography Readability - Smashing Magazine](https://www.smashingmagazine.com/2009/03/10-principles-for-readable-web-typography/)
- [Article Schema Best Practices 2025](https://www.seo-day.de/wiki/on-page-seo/html-optimierung/strukturierte-daten/article-schema.php?lang=en)
- [Schema Markup 2025 Guide](https://allgreatthings.io/blog/seo-content-marketing/schema-markup-in-2025-what-to-use-and-what-to-skip)
- [WordPress Floating Buttons Guide](https://wisernotify.com/blog/wordpress-floating-buttons/)
- [Author Bio Patterns - WordPress.org](https://wordpress.org/patterns/pattern/author-bio-with-image-header-description-social-links-and-button/)
- Existing baseline template: `wp-n8n-html-design-improver/Improved_HTML_Template-claude-code-2026-03-25.html`
