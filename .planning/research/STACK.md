# Technology Stack

**Project:** HipsterStyle Article System Rebuild
**Researched:** 2026-03-25
**Domain:** WordPress-safe article HTML templates with N8N automation, Firecrawl product discovery, Supabase asset hosting

## Recommended Stack

### Core: WordPress-Safe HTML Template Layer

This is not a framework choice -- it is a set of **constraints** dictated by WordPress's `wp_kses_post()` sanitization. Every technology decision flows from what WordPress allows to survive in post content.

| Technology | Version/Spec | Purpose | Why |
|------------|-------------|---------|-----|
| Inline CSS (style attributes) | CSS3 subset | All visual styling | WordPress strips `<style>` blocks via wp_kses. Inline `style=""` attributes are the ONLY CSS delivery mechanism that survives. |
| `<article>` wrapper | HTML5 | Root container for all content | Allowed in `$allowedposttags`. Keeps article self-contained. WordPress themes provide the outer page chrome. |
| `<details>` + `<summary>` | HTML5 | TOC and FAQ accordions | Native HTML accordion without JS. WordPress allows these elements. No plugin dependency. |
| `<img>` tags (never background-image) | HTML5 | All images | `background-image` in inline CSS is allowed since WP 5.0 but unreliable across themes. `<img>` tags are universally safe and get proper alt text for SEO. |
| `onmouseover`/`onmouseout` | Inline JS events | Hover states | WordPress allows inline event handlers for admin/editor-level posts. The only WordPress-safe hover mechanism without `<style>` blocks. |
| SVG inline | SVG 1.1 | WhatsApp icon, back-to-top arrow | WordPress allows inline SVG within post content. No external icon dependency. |
| Arimo font family | Google Fonts | Hebrew RTL typography | Metrically compatible with Arial. Excellent Hebrew glyph coverage. Falls back to `Arial, sans-serif` if unavailable. |
| `dir="rtl"` + `lang="he"` | HTML attributes | Hebrew right-to-left layout | Set on `<article>` root. All child elements inherit direction. Border-right becomes the reading-start accent border. |
| `clamp()` function | CSS3 | Fluid responsive typography | Supported in wp_kses since WordPress 6.1 (added to `safecss_filter_attr`). Enables responsive font sizes without media queries. |
| `calc()` function | CSS3 | Dynamic sizing | Supported in wp_kses since WordPress 5.8. Safe for inline style calculations. |
| `var()` with fallbacks | CSS Custom Properties | NOT recommended | `var()` is technically parsed since WP 5.8/6.1, but CSS custom properties require a `:root` declaration in a `<style>` block, which gets stripped. Useless without the declaration context. Use literal values instead. |
| Percentage/viewport units | CSS3 | Responsive padding/widths | `vw`, `%`, `rem` all survive wp_kses. Use `padding: 0 5%` as mobile-safe baseline. |

### WordPress CSS Properties: What Survives wp_kses

**Confidence: HIGH** -- verified against WordPress core `safecss_filter_attr()` source and official changelogs.

| CSS Property Category | Allowed Since | Safe to Use | Notes |
|----------------------|---------------|-------------|-------|
| `color`, `background`, `background-color` | WP 3.0+ | YES | Core properties, always allowed |
| `font-family`, `font-size`, `font-weight`, `font-style` | WP 3.0+ | YES | All font properties safe |
| `margin`, `padding` (all sides) | WP 3.0+ | YES | Shorthand and longhand both safe |
| `border`, `border-radius`, `border-color` | WP 3.0+ | YES | All border properties safe |
| `width`, `height`, `max-width`, `max-height` | WP 4.4+ | YES | min/max variants added 4.4 |
| `display` | Needs `safe_style_css` filter | CAUTION | Not in default allowed list. Stripped unless theme/plugin adds it. Use sparingly; many themes add it. |
| `flex`, `grid`, `grid-template-columns` | WP 5.3+ | YES | Grid layout properties added 5.3 |
| `position: fixed` | Needs filter | CAUTION | `position` property needs `safe_style_css` extension. However, admin-level posts bypass kses entirely. |
| `z-index` | Needs filter | CAUTION | Same as position -- admin bypass. |
| `box-shadow` | WP 5.3+ | YES | Added in 5.3 |
| `text-decoration`, `text-align` | WP 3.0+ | YES | Core text properties |
| `object-fit` | WP 5.3+ | YES | Critical for product images |
| `overflow`, `overflow: hidden` | WP 5.3+ | YES | Needed for card containers |
| `list-style`, `list-style-type` | WP 4.6+ | YES | For TOC/FAQ lists |
| `cursor: pointer` | WP 5.3+ | YES | For interactive elements |
| `opacity`, `transform` | WP 5.3+ | YES | For subtle visual effects |
| `transition` | WP 5.3+ | YES | Animation properties |
| `clamp()`, `min()`, `max()` in values | WP 6.1+ | YES | CSS functions for responsive design |
| `calc()` in values | WP 5.8+ | YES | Dynamic CSS calculations |

**Critical insight:** WordPress admin-level users (who publish via N8N/API) typically bypass `wp_kses` entirely because `unfiltered_html` capability is granted to admins. However, designing for kses compatibility is the correct defensive approach because:
1. Some security plugins re-enable kses for admins
2. Theme/plugin hooks may re-filter content
3. Content migration between sites may trigger kses
4. It is the difference between "works" and "always works"

### N8N Workflow Automation

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| N8N | Self-hosted (latest) | Workflow orchestration | Already deployed. Central automation platform. All article generation flows through N8N. |
| N8N Code Node | v2 | Template variable injection, HTML post-processing | JavaScript execution within N8N. Handles placeholder replacement, WordPress safety sanitization, and HTML assembly. |
| N8N HTTP Request Node | v4.1 | API calls to Firecrawl, Supabase, WordPress | Standard REST API integration node. Used for all external service calls. |
| N8N OpenAI/Anthropic Node | Latest | LLM article generation | Receives the TXT prompt with injected variables. Generates the full HTML article body. |
| N8N WordPress Node / HTTP | v4.1 | Publishing to WordPress | Uses WP REST API v2 (`/wp-json/wp/v2/posts`). HTTP Request with Basic Auth, not the dedicated WP node, for more control over the request body. |
| N8N IF Node | v2 | Conditional branching | Routes workflow based on store detection, product availability, Firecrawl success/failure. |
| N8N Set Node | v3 | Variable assembly | Consolidates variables from multiple upstream nodes into a single payload for the LLM prompt. |

#### N8N Workflow Architecture (Recommended Node Chain)

```
Google Docs Trigger
  -> Parse Document (Code Node)
  -> Firecrawl: Discover Site Data (HTTP Request, continueOnFail: true)
  -> Merge Site Data (Code Node)
  -> Detect Store Logic (Code Node)
  -> IF: Is Store?
     -> YES: Firecrawl: Scrape Products (HTTP Request)
              -> Extract Product JSON (Code Node)
              -> IF: Images Need Hosting?
                 -> YES: Upload to Supabase (HTTP Request per image)
                         -> Replace URLs (Code Node)
                 -> NO: Continue
     -> NO: Continue (empty products array)
  -> Assemble LLM Variables (Code Node)
  -> LLM: Generate Article HTML (OpenAI/Anthropic Node)
  -> Post-Process HTML (Code Node) -- strips any <style> blocks, validates structure
  -> WordPress: Create Draft Post (HTTP Request)
```

#### N8N Prompt Variable Strategy

**Confidence: HIGH** -- verified against existing codebase patterns.

The N8N prompt uses `[SQUARE_BRACKET]` placeholders (not `{{double_curly}}` which N8N interprets as expressions). The Code Node replaces these before sending to the LLM:

```javascript
// In Code Node: replace [VARIABLE] placeholders with actual values
let prompt = $node['Get Prompt'].json.prompt;
prompt = prompt.replace(/\[ARTICLE_TOPIC\]/g, articleTopic);
prompt = prompt.replace(/\[PRODUCTS_JSON\]/g, JSON.stringify(products));
// ... etc
```

**N8N expression gotcha:** Double curly braces `{{ }}` in prompt text cause N8N to evaluate them as expressions, producing errors or empty strings. The `OPEN_BRACE` / `CLOSE_BRACE` marker pattern in the existing prompt is the correct workaround for JavaScript snippets within the LLM prompt (e.g., `scrollTo` calls).

### Firecrawl: Product Discovery

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Firecrawl Scrape API | v1 | Single-page data extraction | Extracts site metadata (colors, business name, social links, logo) from homepage. Structured extraction with JSON schema. |
| Firecrawl Extract mode | v1 | Product data extraction | AI-powered extraction of product objects (title, url, imageUrl, description) from store/gallery pages. Returns clean JSON matching the prompt's `[PRODUCTS_JSON]` schema. |
| Firecrawl Crawl API | v1 | Multi-page product discovery | Crawls store sitemap or product category pages to find all products. Used when products span multiple pages. |

#### Firecrawl Usage Patterns

**Site Data Discovery (homepage):**
```json
{
  "url": "https://hipsterstyle.co.il/",
  "formats": ["extract"],
  "extract": {
    "schema": {
      "type": "object",
      "properties": {
        "businessName": { "type": "string" },
        "primaryColor": { "type": "string" },
        "contactUrl": { "type": "string" },
        "socialProfiles": { "type": "array", "items": { "type": "object" } }
      }
    }
  }
}
```

**Product Discovery (inner pages):**
```json
{
  "url": "https://hipsterstyle.co.il/shop",
  "formats": ["extract"],
  "extract": {
    "schema": {
      "type": "object",
      "properties": {
        "products": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "title": { "type": "string" },
              "url": { "type": "string" },
              "imageUrl": { "type": "string" },
              "description": { "type": "string" },
              "price": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```

**Confidence: MEDIUM** -- Firecrawl extract schema is well-documented; actual product page structure of hipsterstyle.co.il not yet verified.

### Supabase: Asset Hosting

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Supabase Storage | Public bucket | Stable image hosting for article images | External product image URLs (e.g., Wix CDN, Shopify CDN) may change or expire. Supabase public bucket provides permanent, CDN-backed URLs that survive indefinitely. |
| Supabase Storage CDN | Global (285+ cities) | Fast image delivery | Public bucket objects get automatic CDN caching with high HIT ratio. No auth required for public assets. |
| Supabase Image Transformations | On-the-fly | Image optimization | Resize/compress images to appropriate article dimensions (800px wide max) without manual processing. Reduces page weight. |

#### Supabase Storage Patterns

**Bucket structure:**
```
article-assets/
  hipsterstyle-co-il/
    products/
      product-slug-1.jpg
      product-slug-2.jpg
    authors/
      author-photo.jpg
    logos/
      site-logo.png
```

**URL format:**
```
https://<project-id>.supabase.co/storage/v1/object/public/article-assets/hipsterstyle-co-il/products/product-1.jpg
```

**When to use Supabase hosting (decision matrix):**

| Image Source | Stable? | Action |
|-------------|---------|--------|
| wixstatic.com CDN | Mostly stable, but URLs can break on Wix editor republish | Upload to Supabase as backup |
| Shopify CDN | Stable | Use directly, optional Supabase mirror |
| Self-hosted WordPress media | Stable | Use directly |
| Social media profile images | Often changes | Upload to Supabase |
| Unknown third-party CDN | Unpredictable | Always upload to Supabase |

**N8N Supabase upload pattern (HTTP Request node):**
```
POST https://<project-id>.supabase.co/storage/v1/object/article-assets/{path}
Headers:
  Authorization: Bearer <SUPABASE_SERVICE_KEY>
  Content-Type: image/jpeg
Body: Binary image data
```

**Confidence: HIGH** -- Supabase Storage API is well-documented and the project already has Supabase integration in the codebase.

### Supporting Techniques

| Technique | Purpose | When to Use |
|-----------|---------|-------------|
| `loading="lazy"` on images | Defer offscreen image loading | ALL product/gallery images. Saves bandwidth on long articles. |
| `object-fit: contain` | Prevent image cropping | ALL product images. Products (art, clothing) must never be cropped. |
| `rel="noopener noreferrer"` on external links | Security | ALL `target="_blank"` links. Prevents reverse tabnabbing. |
| `aria-label` on icon-only buttons | Accessibility | Floating WhatsApp/Back-to-top buttons with no visible text. |
| JSON-LD `<script>` blocks | Structured data / SEO | FAQ schema, Article schema. Scripts survive wp_kses in admin posts. |
| No `<h1>` tag | WordPress convention | WordPress supplies H1 from the post title. Duplicate H1 hurts SEO. |

## What NOT to Use (and Why)

| Anti-Pattern | Why It Fails in WordPress |
|-------------|--------------------------|
| `<style>` blocks | Stripped by `wp_kses_post()`. This is the #1 constraint. No exceptions. |
| `<link rel="stylesheet">` | External stylesheets stripped. No CDN CSS imports. |
| CSS custom properties (`--var-name`) | `var()` is parsed but `:root` declarations require `<style>` blocks which are stripped. The variables have no source. |
| `@media` queries | Only exist inside `<style>` blocks. Cannot be inlined. Use `clamp()` and percentage widths instead. |
| `@keyframes` / CSS animations | Require `<style>` block declarations. Use `transition` on inline styles with `onmouseover`/`onmouseout` instead. |
| `class="..."` attributes | Not stripped by WordPress, BUT useless without `<style>` rules to target them. The existing workflow strips them in post-processing anyway. Adds dead weight. |
| `<script>` for interactivity | Stripped by `wp_kses` for non-admin users. Admin users can include them, but relying on inline JS beyond event handlers is fragile. JSON-LD scripts are the exception. |
| External JavaScript (CDN) | Stripped. No Bootstrap JS, no jQuery CDN, no external dependencies. |
| `<iframe>` for embeds | Allowed by wp_kses but problematic: responsive sizing, security headers, and many themes restrict iframe dimensions. Avoid unless embedding YouTube (which WordPress auto-embeds via oEmbed anyway). |
| CSS `background-image: url()` | Technically allowed since WP 5.0, but: (1) no alt text for SEO, (2) no lazy loading, (3) unreliable responsive behavior, (4) harder to debug. Use `<img>` tags. |
| Tailwind / Utility CSS | Requires `<style>` or external CSS. The utility-first approach is fundamentally incompatible with inline-only WordPress constraints. |
| Email-style table layouts | Unnecessary. WordPress is a browser context, not an email client. Flexbox and Grid work fine in inline styles. |
| `!important` in inline styles | Technically works but signals a specificity war with the theme's CSS. Design the template to not need it. |

## Responsive Strategy Without Media Queries

Since `@media` queries require `<style>` blocks (stripped by WordPress), responsiveness must be achieved entirely through inline CSS techniques:

| Technique | What It Replaces | Example |
|-----------|-----------------|---------|
| `clamp(min, preferred, max)` | `@media` font-size breakpoints | `font-size: clamp(1.3rem, 3vw, 1.7rem)` |
| `padding: 0 5%` | Fixed px padding with breakpoints | Percentage-based, scales with viewport |
| `grid-template-columns: repeat(auto-fill, minmax(220px, 1fr))` | Grid breakpoint changes | Auto-responsive grid, cards reflow naturally |
| `max-width: 800px; margin: 0 auto` | Container width breakpoints | Content stays readable, centered on desktop |
| `width: 100%` on images | Responsive image sizing | Images scale to container width |
| `max-height: 320px; object-fit: contain` | Image dimension control | Prevents oversized images, no cropping |
| Viewport units (`vw`) in clamp | Fluid scaling | Typography and spacing scale smoothly |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| CSS delivery | Inline `style=""` | `<style>` block with scoped CSS | WordPress strips `<style>` blocks. Non-negotiable. |
| Accordion UI | `<details>`/`<summary>` | JavaScript accordion library | External JS deps stripped. `<details>` is native HTML, zero dependencies. |
| Hover effects | `onmouseover`/`onmouseout` | CSS `:hover` pseudo-class | `:hover` requires `<style>` block. Inline event handlers are the only option. |
| Font loading | System font stack with Arimo | Google Fonts `<link>` import | External stylesheet stripped. Arimo works if the theme loads it; otherwise falls back to Arial gracefully. |
| Image hosting | Supabase public bucket | WordPress Media Library | WP Media Library is fine for images uploaded directly, but N8N workflow needs API-accessible storage. Supabase has a simpler upload API than WP Media REST API. |
| Product scraping | Firecrawl | Cheerio/Puppeteer in Code Node | N8N Code Nodes have limited runtime. Firecrawl handles JS rendering, anti-bot, and structured extraction as a service. |
| Workflow engine | N8N | Zapier, Make.com | N8N is already deployed and self-hosted. Full control, no per-execution costs, custom Code nodes. |
| LLM for generation | OpenAI GPT-4o / Claude | Local LLM | Quality of Hebrew content generation requires frontier models. Local LLMs cannot match Hebrew fluency. |

## Installation / Setup

No package installation required for the HTML template itself -- it is pure HTML/CSS output.

**N8N workflow dependencies (environment variables):**
```bash
# Firecrawl
FIRECRAWL_API_KEY=fc-xxxxxxxx

# Supabase
SUPABASE_URL=https://<project-id>.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIs...
SUPABASE_BUCKET=article-assets

# WordPress
WORDPRESS_URL=https://mahsan.websreport.net
WORDPRESS_USER=admin
WORDPRESS_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# LLM
OPENAI_API_KEY=sk-xxxxxxxx
# or
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx

# Defaults
DEFAULT_SITE_URL=https://hipsterstyle.co.il/
```

## Version Compatibility Matrix

| WordPress Version | Minimum Required | Why |
|------------------|-----------------|-----|
| 6.1+ | Required | `clamp()`, `min()`, `max()` in inline CSS values |
| 5.8+ | Minimum fallback | `calc()` and basic `var()` support |
| 5.3+ | Absolute minimum | Grid, flex, box-shadow, object-fit in inline styles |

**Recommendation:** Target WordPress 6.1+ as minimum. The template uses `clamp()` extensively for responsive typography. Older WordPress versions would strip these values, breaking the responsive design.

## Sources

- [WordPress wp_kses() function reference](https://developer.wordpress.org/reference/functions/wp_kses/)
- [WordPress safe_style_css hook reference](https://developer.wordpress.org/reference/hooks/safe_style_css/)
- [WordPress safecss_filter_attr() function reference](https://developer.wordpress.org/reference/functions/safecss_filter_attr/)
- [WordPress Trac #43215 - Allow wp_kses to pass allowed CSS properties](https://core.trac.wordpress.org/ticket/43215)
- [WordPress Trac #46498 - Block style attribute issue with CSS variables](https://core.trac.wordpress.org/ticket/46498)
- [WordPress Trac #55966 - safecss_filter_attr() and min()](https://core.trac.wordpress.org/ticket/55966)
- [Firecrawl + n8n integration docs](https://docs.firecrawl.dev/developer-guides/workflow-automation/n8n)
- [Firecrawl n8n web scraping workflow templates](https://www.firecrawl.dev/blog/n8n-web-scraping-workflow-templates)
- [n8n Firecrawl integration page](https://n8n.io/integrations/firecrawl/)
- [Supabase Storage CDN fundamentals](https://supabase.com/docs/guides/storage/cdn/fundamentals)
- [Supabase Storage buckets documentation](https://supabase.com/docs/guides/storage/buckets/fundamentals)
- [Supabase Storage overview](https://supabase.com/docs/guides/storage)
- [n8n Code Node documentation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
- [WordPress kses.php source on GitHub](https://github.com/WordPress/WordPress/blob/master/wp-includes/kses.php)
- [WordPress accordions in 6.9](https://developer.wordpress.org/news/2025/10/styling-accordions-in-wordpress-6-9/)
- [WP-Mix: Allowed HTML tags for wp_kses()](https://wp-mix.com/allowed-html-tags-wp_kses/)
- [Arimo font - Google Fonts](https://fonts.google.com/specimen/Arimo)
