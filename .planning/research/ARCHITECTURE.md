# Architecture Patterns

**Domain:** WordPress Article Generation System with N8N Workflow Automation
**Researched:** 2026-03-25
**Confidence:** HIGH (based on actual codebase analysis of existing oritmartin pipeline + v2 generic pipeline)

## System Overview

The HipsterStyle Article System is a **three-deliverable rebuild** of an existing N8N-powered WordPress article generation pipeline. The system takes a topic/content seed, crawls the client's main site for products and brand data, generates article content via LLM, renders it into WordPress-safe HTML using a strict template, and publishes it as a draft post.

### The Three Deliverables and Their Relationship

```
+---------------------+        +---------------------+        +-----------------------+
|  1. HTML TEMPLATE   |        |  2. N8N PROMPT      |        |  3. N8N WORKFLOW JSON |
|  (Reference Output) |<-------|  (LLM Instructions) |<-------|  (Orchestration)      |
+---------------------+        +---------------------+        +-----------------------+
| What the final      |        | Instructions that   |        | Automates the entire  |
| article looks like  |        | tell the LLM how to |        | pipeline: triggers,   |
| in WordPress.       |        | generate HTML that   |        | Firecrawl, product    |
| Pure inline CSS,    |        | matches the template.|        | extraction, LLM calls,|
| RTL, article tags.  |        | Contains injection   |        | HTML cleanup, WP post.|
|                     |        | block for N8N vars.  |        |                       |
| DEFINES the target. |        | GUIDES the LLM.     |        | EXECUTES the pipeline.|
+---------------------+        +---------------------+        +-----------------------+
```

**Critical dependency chain:** Template defines the target -> Prompt encodes the template's rules for the LLM -> Workflow orchestrates data flow and embeds the prompt. The template is the source of truth; prompt and workflow must align to it.

## Component Boundaries

| Component | Responsibility | Inputs | Outputs | Communicates With |
|-----------|---------------|--------|---------|-------------------|
| **Google Docs Trigger** | Detects new article content in a Drive folder | Google Drive folder watch | Document ID | Normalize Input |
| **Webhook Trigger** | Alternative manual/API trigger | HTTP POST with topic/content | Topic + optional content | Normalize Input |
| **Normalize Input** | Standardizes input from either trigger into uniform schema | Raw trigger data | Normalized JSON (siteUrl, topic, content, business facts) | Site Discovery |
| **Site Discovery (Firecrawl /map)** | Discovers all pages on the client's main site | Site URL | Array of page URLs | Parse Site Map |
| **Parse Site Map** | Identifies product/store pages, about page, gallery page | URL list | Categorized URLs + isStore flag | Store Check |
| **Store Check (IF node)** | Routes to product scraping or skip-products path | isStore boolean | Branch decision | Scrape Products OR Empty Products |
| **Scrape Product Pages (Firecrawl /scrape)** | Extracts product data from store pages | Product URLs | Raw product metadata (title, image, description, URL) | Extract Product Data |
| **Extract Product Data** | Normalizes and deduplicates scraped products | Raw scrape output | Clean product array | Rank Products |
| **Rank and Select Top Products** | Scores products by topic relevance, picks top 6 | Products + topic | Ranked product subset | Build Blog Brief |
| **Build Blog Brief** | Creates the LLM writing prompt for the article draft | Products, links, topic, source content | Hebrew blog brief prompt | Write Blog Draft (LLM) |
| **Write Blog Draft (LLM)** | Generates the article body text via Maximo API | Blog brief | Raw Hebrew article text | Writing Blog |
| **Writing Blog** | Validates LLM output is non-empty | LLM response | Validated article body | Preparing Images |
| **Preparing Images for HTML** | Maps product images to hero + section image slots | Products with images | Image URL map (hero, section_1-4) | Build Final HTML Prompt |
| **Build Final HTML Prompt** | Assembles the complete HTML rendering prompt with all data | Article body, products, images, site facts | Final prompt string (THE N8N PROMPT TXT) | Render Final HTML (LLM) |
| **Render Final HTML (LLM)** | Generates the complete HTML article via LLM | Final prompt | Raw HTML output | Clean HTML |
| **Clean HTML for WordPress** | Strips forbidden markup, validates article wrapper | Raw HTML | Sanitized HTML | Prepare WordPress Post |
| **Prepare WordPress Post** | Formats data for WP REST API (title, content, status, Yoast meta) | Clean HTML + metadata | WP post payload | Publish to WordPress |
| **Publish to WordPress** | Posts to WordPress via REST API as draft | WP post payload | Post URL / ID | Slack + Sheets notifications |
| **Supabase Storage** | Hosts stable images (author portrait, product images) | Image URLs to upload | Public CDN URLs | Referenced in HTML template and prompt |

## Data Flow

### Primary Pipeline Flow

```
TRIGGER (Google Docs or Webhook)
    |
    v
NORMALIZE INPUT
    |  (siteUrl, articleTopic, docContent, businessName, verifiedLinks)
    v
SITE DISCOVERY (Firecrawl /map)
    |  (array of all site URLs)
    v
PARSE SITE MAP
    |  (productUrls[], aboutUrl, galleryUrl, isStore)
    v
STORE CHECK ----[true]--> SCRAPE PRODUCTS (Firecrawl /scrape)
    |                           |
    |                           v
    |                      EXTRACT PRODUCT DATA
    |                           |
    |[false]                    |
    v                           |
EMPTY PRODUCTS                  |
    |                           |
    +----------+----------------+
               |
               v
RANK & SELECT TOP PRODUCTS (max 6, scored by topic relevance)
    |  (products[{title, url, imageUrl, description}])
    v
BUILD BLOG BRIEF (Hebrew LLM prompt for article text)
    |  (blogBrief string)
    v
WRITE BLOG DRAFT (LLM call via Maximo API)
    |  (raw article body text in Hebrew)
    v
WRITING BLOG (validate non-empty)
    |
    v
PREPARING IMAGES FOR HTML
    |  (images: {hero, section_1..4} each with .url)
    v
BUILD FINAL HTML PROMPT
    |  (htmlPrompt string containing:
    |    - All rendering rules from N8N Prompt TXT
    |    - Injection block: products JSON, article body, image URLs)
    v
RENDER FINAL HTML (LLM call via Maximo API)
    |  (raw HTML starting with <article>)
    v
CLEAN HTML FOR WORDPRESS
    |  (sanitized HTML, validated article wrapper)
    v
PREPARE WORDPRESS POST
    |  (title, content, status:draft, Yoast meta)
    v
PUBLISH TO WORDPRESS (REST API)
    |
    +---> NOTIFY SLACK (success/error)
    +---> SAVE TO GOOGLE SHEETS (article log)
```

### Product Data Flow

```
hipsterstyle.co.il (main site)
    |
    | Firecrawl /map
    v
URL Discovery -> Filter product/gallery/shop URLs
    |
    | Firecrawl /scrape (per product page)
    v
Raw Product Data {title, imageUrl, url, description}
    |
    | Score by topic relevance
    v
Top 6 Products -> JSON.stringify() -> Injected into N8N Prompt
    |
    | LLM renders product cards in HTML
    v
Product Cards in Final Article (img + link + title)
```

### Image Hosting Flow

```
Product Images (from Wix/source site)
    |
    | Option A: Direct reference (current oritmartin approach)
    | Use source URL directly (e.g., static.wixstatic.com)
    |
    | Option B: Supabase re-hosting (v2 pipeline approach)
    | Download -> Upload to Supabase Storage bucket -> Get public CDN URL
    v
Stable Public URLs referenced in HTML <img> tags
    |
    | For author portrait / logos: Always Supabase-hosted
    | Format: https://{project}.supabase.co/storage/v1/object/public/article-assets/{site-slug}/{path}
    v
WordPress article renders images from stable URLs
```

## Recommended Architecture for HipsterStyle Rebuild

### Key Differences from OritMartin Baseline

| Aspect | OritMartin (existing) | HipsterStyle (rebuild) |
|--------|----------------------|----------------------|
| Main site | oritmartin.com (Wix) | hipsterstyle.co.il |
| WP target | mahsan.websreport.net | mahsan.websreport.net |
| Content focus | Kabbalah art, spiritual paintings | Kids styling tips |
| Products | Art pieces from gallery | Fashion/styling products |
| Language | Hebrew RTL | Hebrew RTL |
| Verified links | Hardcoded in prompt | Must be discovered/verified for hipsterstyle |
| Style block | Scoped `#om-top` | Needs new scoped prefix (e.g., `#hs-top`) |
| Author portrait | Supabase-hosted | Needs Supabase upload for hipsterstyle |
| Social profiles | Facebook + Instagram verified | Need Firecrawl verification |

### Component Architecture for the Rebuild

```
+-------------------------------------------------------------------+
|                    N8N WORKFLOW (JSON)                              |
|                                                                    |
|  TRIGGERS          DISCOVERY            CONTENT GENERATION         |
|  +--------+       +----------------+   +---------------------+    |
|  |GDocs   |------>|                |   |                     |    |
|  +--------+       | Normalize      |-->| Build Blog Brief    |    |
|  +--------+       | Input          |   | (Hebrew prompt)     |    |
|  |Webhook |------>|                |   |                     |    |
|  +--------+       +-------+--------+   +----------+----------+    |
|                           |                       |               |
|                           v                       v               |
|                   +-------+--------+   +----------+----------+    |
|                   | Firecrawl      |   | LLM: Write Draft    |    |
|                   | Site Discovery |   | (Maximo API)        |    |
|                   +-------+--------+   +----------+----------+    |
|                           |                       |               |
|                           v                       v               |
|                   +-------+--------+   +----------+----------+    |
|                   | Product        |   | Prepare Images      |    |
|                   | Scraping +     |   | for HTML            |    |
|                   | Ranking        |   +----------+----------+    |
|                   +-------+--------+              |               |
|                           |                       v               |
|                           |            +----------+----------+    |
|                           +----------->| Build Final HTML    |    |
|                                        | Prompt (embeds      |    |
|                                        | N8N PROMPT TXT)     |    |
|                                        +----------+----------+    |
|                                                   |               |
|  RENDERING + PUBLISHING                           v               |
|                                        +----------+----------+    |
|                                        | LLM: Render HTML    |    |
|                                        | (Maximo API)        |    |
|                                        +----------+----------+    |
|                                                   |               |
|                                                   v               |
|  +----------+  +-----------+  +--------+  +-------+----------+   |
|  |Slack     |<-|Google     |<-|WP REST |<-| Clean HTML       |   |
|  |Notify    |  |Sheets Log |  |API Post|  | for WordPress    |   |
|  +----------+  +-----------+  +--------+  +------------------+   |
+-------------------------------------------------------------------+

EXTERNAL SERVICES:
  - Firecrawl API (v1/map, v1/scrape, v1/batch/scrape)
  - Maximo SEO API (LLM generation endpoint)
  - Supabase Storage (image CDN)
  - WordPress REST API (wp/v2/posts)
  - Google Sheets API (article log)
  - Slack Webhook (notifications)
  - Google Drive (trigger source)
```

### Three-Deliverable Structure

**1. HTML Template (`Improved_HTML_Template-claude-code-YYYY-MM-DD.html`)**
- A complete example article rendered in the target style
- Serves as the visual/structural reference, NOT consumed directly by the pipeline
- All inline CSS, RTL, scoped style block, article wrapper
- Used to validate that the LLM output matches expectations
- When rebuilding: create the template FIRST, then derive the prompt from it

**2. N8N Prompt (`Improved_N8N_Prompt-claude-code-YYYY-MM-DD.txt`)**
- Plain text instructions for the LLM that produces the final HTML
- Contains the LOCKED INJECTION BLOCK (non-negotiable N8N expressions):
  - `{{ JSON.stringify($json["products"], null, 2) }}` - product data
  - `{{ $("Writing Blog").first().json.output }}` - article body content
  - `{{ $("Preparing Images for HTML").first().json.images.*.url }}` - image URLs
- Contains ALL rendering rules derived from the template
- Contains site-specific facts (URLs, phone, email, social profiles)
- Contains WordPress hardening rules
- Contains mandatory CSS classes and hover/accordion behavior
- This file IS the prompt that gets embedded in the workflow's "Build Final HTML Prompt" node

**3. N8N Workflow (`Improved_N8N_Workflow-claude-code-YYYY-MM-DD.json`)**
- Complete workflow JSON importable into N8N
- Contains all nodes, connections, and code
- The "Build Final HTML Prompt" node embeds the Prompt TXT content
- Credential references use placeholder IDs (user configures in N8N)
- Error handling with Slack notifications

## Patterns to Follow

### Pattern 1: Scoped CSS for WordPress Safety
**What:** All hover/animation CSS goes in a single `<style>` block scoped to the article's ID, placed immediately after the opening `<article>` tag. Every element also gets full inline CSS as fallback.
**When:** Always -- WordPress admin posts preserve style blocks but non-admin posts may strip them.
**Why:** WordPress `wp_kses` filtering can strip style blocks for non-admin users. The scoped ID prevents style leakage into the rest of the page. Inline CSS ensures the article looks acceptable even if the style block is stripped.
```html
<article id="hs-top" lang="he" dir="rtl" style="max-width:880px;margin:0 auto;...">
<style>
#hs-top .hstl:hover{text-decoration:underline;color:#accent}
#hs-top details[open] .hsic{transform:rotate(45deg)}
/* ... scoped hover rules only ... */
</style>
<!-- article content with inline CSS on every element -->
</article>
```

### Pattern 2: Locked Injection Block
**What:** The N8N prompt contains exact N8N expression lines that inject dynamic data. These lines must never be modified, renamed, or reformatted.
**When:** Always in the prompt TXT file.
**Why:** N8N resolves `{{ }}` expressions at runtime. Changing the node names or expression format breaks the data pipeline.
```
### Available Products:
{{ JSON.stringify($json["products"], null, 2) }}

### Article Content:
{{ $("Writing Blog").first().json.output }}

### Available Images:
Section image 1 URL: {{ $("Preparing Images for HTML").first().json.images.section_1.url }}
...
```

### Pattern 3: Graceful Degradation with continueOnFail
**What:** Firecrawl nodes and Supabase upload nodes use `continueOnFail: true` or `onError: "continueRegularOutput"` so the pipeline continues even if a scrape fails.
**When:** Every external HTTP call in the workflow.
**Why:** Firecrawl may timeout, rate-limit, or fail for specific pages. The pipeline should produce an article with whatever data it can gather, not abort entirely.

### Pattern 4: Product Relevance Scoring
**What:** Products are scored by keyword overlap with the article topic and sorted by relevance before injection.
**When:** After product extraction, before prompt assembly.
**Why:** Firecrawl may return many products. Only the top 6 most relevant should appear in the article to avoid diluting the content.

### Pattern 5: Two-Phase LLM Generation
**What:** First LLM call writes the article body text. Second LLM call renders that text into final HTML using the template rules.
**When:** Every article generation.
**Why:** Separating content creation from HTML rendering produces better results. The first LLM focuses on editorial quality. The second focuses on structural compliance.

### Pattern 6: HTML Validation Gate
**What:** The "Clean HTML for WordPress" node validates the output starts with `<article` and ends with `</article>`, strips forbidden markup (scripts, comments, extra style blocks), and throws an error if validation fails.
**When:** After every LLM HTML generation.
**Why:** LLMs can produce malformed HTML. The validation gate catches this before it reaches WordPress.

## Anti-Patterns to Avoid

### Anti-Pattern 1: External CSS/JS Dependencies
**What:** Linking to external stylesheets or script files in the generated HTML.
**Why bad:** WordPress strips external resources from post content. CDN links become single points of failure. Violates the inline-only constraint.
**Instead:** All CSS inline on elements. Hover effects via scoped style block + inline onmouseover/onmouseout fallback.

### Anti-Pattern 2: Hardcoding Product Data in the Template
**What:** Putting specific product URLs, images, or titles directly in the HTML template file.
**Why bad:** The template is a reference, not a data source. Products change. The workflow dynamically injects products via the prompt injection block.
**Instead:** Template shows example products. Prompt contains the injection block. Workflow populates it at runtime.

### Anti-Pattern 3: Unscoped Style Blocks
**What:** Using generic CSS selectors like `.btn:hover` in the style block.
**Why bad:** These styles leak into the WordPress theme, causing visual conflicts across the site.
**Instead:** Every selector must be scoped: `#hs-top .hsbtn:hover`.

### Anti-Pattern 4: Relying on JavaScript for Core Layout
**What:** Using JavaScript to build the page structure, show/hide content, or control layout.
**Why bad:** WordPress may strip JS event handlers for non-admin posts. Even for admin posts, JS failures leave the article broken.
**Instead:** Use `<details>`/`<summary>` for accordions (native HTML). Use inline CSS for all layout. JS handlers (onmouseover, ontoggle) are progressive enhancement only.

### Anti-Pattern 5: Single Monolithic LLM Call
**What:** Sending all data + writing instructions + HTML rendering rules in one prompt.
**Why bad:** The LLM cannot simultaneously optimize for editorial quality AND structural compliance. Results are consistently worse than two-phase.
**Instead:** Two-phase: write first, render second.

## Build Order (Dependency Analysis)

The three deliverables have a strict dependency chain that dictates build order:

```
Phase 1: AUDIT + DISCOVERY
  |  - Audit existing baselines (oritmartin versions)
  |  - Firecrawl hipsterstyle.co.il for products, social links, brand data
  |  - Verify social profiles (Facebook, Instagram, YouTube)
  |  - Collect verified site facts
  |
  v
Phase 2: HTML TEMPLATE (build first)
  |  - Design the target article structure
  |  - All inline CSS, RTL, responsive
  |  - Scoped style block
  |  - Product cards, TOC, FAQ, CTA, floating buttons, author section
  |  - Use real hipsterstyle products from Phase 1
  |  - QA in WordPress rendering environment
  |
  v
Phase 3: N8N PROMPT (derives from template)
  |  - Encode ALL template rules as text instructions
  |  - Include hipsterstyle-specific site facts
  |  - Include locked injection block (unchanged)
  |  - WordPress hardening rules
  |  - QA checklist
  |
  v
Phase 4: N8N WORKFLOW JSON (embeds the prompt)
  |  - Update pipeline nodes for hipsterstyle
  |  - Embed prompt in "Build Final HTML Prompt" node
  |  - Update Firecrawl targets
  |  - Update verified links
  |  - Test end-to-end
  |
  v
Phase 5: INTEGRATION QA
     - Full pipeline test with real data
     - WordPress rendering validation
     - Mobile/tablet/desktop responsive QA
     - RTL verification
```

**Why this order:**
1. Template MUST come first because it defines what the LLM must produce. You cannot write instructions (prompt) without knowing the target.
2. Prompt MUST come second because every rule in it derives from template decisions (class names, structure, colors, sections).
3. Workflow MUST come last because it embeds the prompt and must reference the correct node names for the injection block to resolve.
4. Changing the template after the prompt is written means rewriting prompt rules. Changing the prompt after embedding in the workflow means updating the workflow node code.

## WordPress Rendering Considerations

| Concern | Admin Posts | Non-Admin Posts |
|---------|------------|-----------------|
| `<style>` blocks | Preserved | May be stripped by wp_kses |
| Inline CSS | Preserved | Preserved (most properties) |
| onmouseover/onmouseout | Preserved | Stripped by wp_kses |
| ontoggle | Preserved | Stripped by wp_kses |
| `<details>`/`<summary>` | Works natively | Works natively |
| `<article>` wrapper | Preserved | Preserved |
| `<svg>` inline | Preserved | May be stripped |
| `display` property | Preserved | May be stripped depending on context |
| `object-fit` | Preserved | Preserved |
| External images | Rendered | Rendered (if URL accessible) |

**Strategy:** Design for admin-level posts (which this pipeline produces) but ensure every element looks acceptable with pure inline CSS alone as fallback. The scoped style block handles hover/animation effects that degrade gracefully.

## External Service Architecture

### Firecrawl (Web Scraping)
- **/v1/map** - Site URL discovery (finds all pages). 1 credit. Used to discover product/gallery/shop pages.
- **/v1/scrape** - Single page data extraction. 1 credit + extras for JSON mode. Used to scrape individual product pages.
- **/v1/batch/scrape** - Multi-URL extraction in one job. Used for bulk product scraping (v2 pipeline).
- Rate limits apply. Timeout at 30s per request. `continueOnFail` required.

### Supabase Storage
- Bucket: `article-assets`
- Path convention: `{site-slug}/products/{product-slug}.jpg`, `{site-slug}/branding/logo.jpg`
- Public bucket = no auth needed to read, high CDN cache hit rate.
- Public URL format: `https://{project-ref}.supabase.co/storage/v1/object/public/article-assets/{path}`
- Upload via REST API with service key. Upsert supported.
- Smart CDN auto-invalidates on update (up to 60s propagation).

### WordPress REST API
- Endpoint: `{wp-url}/wp-json/wp/v2/posts`
- Auth: HTTP Basic Auth (application password)
- Payload: `{title, content, status: "draft"}`
- Yoast SEO meta passed as custom fields.

### Maximo SEO API
- Endpoint: `{maximo-url}/api/v1/generate` (for drafting) and `/api/v1/improve` (for HTML rendering)
- Auth: Bearer token via httpHeaderAuth
- Timeout: 120s (LLM generation is slow)
- Returns: `{output, html, content}` (varies by endpoint)

## Sources

- Codebase analysis: `wp-n8n-html-design-improver/Improved_N8N_Workflow-claude-code-2026-03-25.json` (HIGH confidence)
- Codebase analysis: `wp-n8n-html-design-improver/Improved_N8N_Prompt-claude-code-2026-03-25.txt` (HIGH confidence)
- Codebase analysis: `wp-n8n-html-design-improver/Improved_HTML_Template-claude-code-2026-03-25.html` (HIGH confidence)
- Codebase analysis: `wp-n8n-html-design-improver/n8n-improved-content-pipeline-google-docs-to-wordpress-with-firecrawl-supabase-products.json` (HIGH confidence, v2 generic pipeline)
- [WordPress wp_kses documentation](https://developer.wordpress.org/reference/functions/wp_kses/) (MEDIUM confidence)
- [Firecrawl API documentation](https://docs.firecrawl.dev/features/scrape) (MEDIUM confidence)
- [Supabase Storage CDN docs](https://supabase.com/docs/guides/storage/cdn/fundamentals) (MEDIUM confidence)
- [N8N WordPress automation guide](https://www.bigcloudy.com/blog/wordpress-automation-n8n/) (LOW confidence, general patterns)
