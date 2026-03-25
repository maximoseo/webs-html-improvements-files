# Consolidated WordPress Rendering Risk Summary

**Date:** 2026-03-25
**Fulfills:** DEL-07 (Before-State Audit Summary) and DEL-08 (WordPress Rendering Risk Review)
**Source documents:**
- `01-html-template-risk-inventory.md` (19 issues, 10 audit sections)
- `02-prompt-contradiction-report.md` (2 CRITICAL, 3 HIGH, 3 MEDIUM)
- `03-workflow-logic-bug-report.md` (2 CRITICAL, 2 HIGH, 3 MEDIUM)
- `04-site-reference-migration-map.md` (58 replacement points across 3 files)

**Purpose:** Single authoritative document for all subsequent phases. A Phase 3+ executor can read ONLY this document and know exactly what needs to change, in what order, and why.

---

## 1. Before-State Audit Summary (DEL-07)

Documents the current state of all three deliverable files before any modifications.

### 1a. HTML Template Current State

**File:** `wp-n8n-html-design-improver/Improved_HTML_Template-claude-code-2026-03-25.html`
**Lines:** 321

**Overall structure:**
- `<article id="om-top" lang="he" dir="rtl">` wrapper (line 1)
- `<style>` block (lines 2-14) -- 12 CSS rules for hover/accordion effects
- Summary card section with 6 bullet points (lines 15-29)
- TOC accordion using `<details>/<summary>` (lines 30-46) -- closed by default, 6 anchor links
- Product cards section (lines 47-107) -- `display:grid` container with 6 cards
- Body content sections with H2 headings (lines 108-221): meaning, sefirot, symbols, choosing, colors, meditation
- 2 inline CTA banners (lines 192-196, 214-221)
- FAQ section with 6 `<details>/<summary>` accordions (lines 222-279)
- Gallery CTA (lines 280-285)
- Floating buttons: Contact (line 286), Back-to-top (line 290)
- Author section with portrait, bio, contact buttons, social links (lines 291-306)
- WhatsApp floating button (line 308) -- not mentioned in prompt, template drift
- 3 JSON-LD script blocks: Article, LocalBusiness, FAQPage (lines 312-319)
- `</article>` closing tag (line 321)

**CSS approach:** Mix of inline styles + `<style>` block + 38 `class="..."` attributes. Hover effects duplicated across style block and inline `onmouseover`/`onmouseout` handlers. Classes serve no purpose after style block removal since all handlers use `this.style` directly.

**Layout approach:** Flex/grid based throughout. 64 occurrences of `display:` property (27 flex, 25 inline-flex, 1 grid, 8 block, 1 inline-block, 2 none in style block). All will collapse in WordPress since `display` is NOT on the `safe_style_css` whitelist.

**Interactive elements:**
- 7 `<details>/<summary>` accordions (1 TOC + 6 FAQ) with `ontoggle` handlers
- 28 `onmouseover` + 28 `onmouseout` handlers for hover effects
- All event handlers require `unfiltered_html` capability

**Image sources:**
- 6 `wixstatic.com` product image URLs (fragile external CDN hotlinks)
- 1 Supabase URL for author portrait (stable)

**Site references:** 24 lines containing `oritmartin.com` (wrong domain -- should be `hipsterstyle.co.il`)

**JSON-LD:** 3 schema blocks (Article, LocalBusiness, FAQPage) placed after author section -- contradicts prompt Line 26 which says "No JSON-LD block"

### 1b. N8N Prompt Current State

**File:** `wp-n8n-html-design-improver/Improved_N8N_Prompt-claude-code-2026-03-25.txt`
**Lines:** 331

**Overall structure:**
- Title and role definition (lines 1-10)
- Mandatory site facts section with oritmartin.com data (lines 57-68)
- N8N injection block with 7 expressions (lines 70-100) -- LOCKED, non-negotiable
- HTML rendering instructions (lines 105-280)
- Forbidden patterns list (lines 282-295)
- QA checklist (lines 307-323)

**Key contradictions:** 2 CRITICAL
- CRIT-1: Style block mandated (lines 18, 29-44) AND forbidden (lines 282, 292, 320) simultaneously
- CRIT-2: JSON-LD prohibited (line 26) but present in template (lines 312-319)

**oritmartin-specific hardcoded data:** 18+ direct occurrences across 20 lines (site URLs, phone, email, Facebook, Instagram, portrait URL, author name, brand references)

**N8N expression syntax:** All 7 `{{ }}` expressions are syntactically valid. Node references are string-name-based (fragile if nodes renamed). Locked block instruction (lines 70-80) correctly protects against modification.

### 1c. N8N Workflow Current State

**File:** `wp-n8n-html-design-improver/Improved_N8N_Workflow-claude-code-2026-03-25.json`
**Lines:** 683
**Total nodes:** 22 (20 functional + 1 disconnected error handler + workflow root)

**Workflow flow:** Trigger(s) -> Normalize Input -> Site Discovery (Firecrawl) -> Parse Site Map -> Store/Non-Store Router -> [Scrape Products | Empty Set] -> Rank Products -> Build Blog Brief -> Write Blog Draft (LLM) -> Writing Blog -> Preparing Images for HTML -> Build Final HTML Prompt -> Render Final HTML (LLM) -> Clean HTML for WordPress -> Prepare WordPress Post -> Publish to WordPress -> [Notify Slack, Save to Sheets]

**Key bugs:** 7 total (2 CRITICAL, 2 HIGH, 3 MEDIUM)
- BUG-1: Clean HTML node self-contradiction -- preserves style block then rejects it
- BUG-2: Build Final HTML Prompt contains style block AND inline-only instructions
- BUG-3: LLM API uses Maximo credentials -- verify for hipsterstyle deployment
- BUG-4: WordPress Publish content escaping -- double quotes in HTML break JSON

**Node connection issues:** Error Handler (Slack) node exists but is not connected to any node. `settings.errorWorkflow` is empty string.

**Credential references:** `maximo-api-key` and `maximoApiUrl` used by both LLM nodes. 17+ oritmartin references across 6 nodes and metadata.

---

## 2. WordPress Rendering Risk Review (DEL-08)

Comprehensive `wp_kses_post()` impact analysis consolidating all findings from reports 01-04.

### 2a. Consolidated Risk Matrix

Every issue from all four audit reports, deduplicated and assigned a target fix phase.

| ID | Severity | File(s) | Issue Summary | wp_kses Impact | Fix Phase |
|----|----------|---------|---------------|----------------|-----------|
| C1 | CRITICAL | Template (lines 2-14) | `<style>` block with 12 CSS rules for hover/accordion effects | Entire block stripped by wp_kses_post(). All class-based hover effects, rotation animation, marker hiding vanish. | Phase 3 |
| C2 | CRITICAL | Template (line 51) | `display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))` on product container | `display` stripped. Grid collapses to single-column block. `grid-template-columns` survives but useless without `display:grid`. | Phase 5 |
| C3 | CRITICAL | Template (lines 32, 226, 235, 244, 253, 262, 271) | `display:flex` on 7 `<summary>` elements (1 TOC + 6 FAQ) | Summary elements revert to block. Flex layout for text-left/indicator-right breaks. Both elements stack vertically. | Phase 4 (TOC), Phase 6 (FAQ) |
| C4 | CRITICAL | Template (lines 52, 61, 70, 79, 88, 97) | `display:flex;flex-direction:column` on 6 product card outer containers | Cards lose flex column layout. `flex-direction:column` useless without `display:flex`. | Phase 5 |
| C5 | CRITICAL | Template (lines 53, 62, 71, 80, 89, 98) | `display:flex;align-items:center;justify-content:center` on 6 product image links | Image centering lost. Images fall to default inline positioning. | Phase 5 |
| C6 | CRITICAL | Template (lines 297, 302) | `display:flex;justify-content:center;gap:10px;flex-wrap:wrap` on 2 author button containers | Author buttons lose horizontal centered layout. `gap` useless without flex context. | Phase 7 |
| C7 | CRITICAL | Template (25 occurrences across lines 34, 195, 217-219, 228, 237, 246, 255, 264, 273, 286, 290, 298-300, 303-304, 308) | `display:inline-flex` on buttons, CTAs, social links, floating buttons | All revert from inline-flex to inline. Icon+text alignment breaks. `align-items`, `justify-content`, `gap` useless. | Phase 4-8 (per section) |
| CRIT-1 | CRITICAL | Prompt (lines 18, 29-44 vs 282, 292, 320) | Style block simultaneously mandated AND forbidden in prompt | LLM cannot satisfy both. Current template follows mandate side, but QA checklist fails itself. Workflow Clean HTML node also contradicts. | Phase 9 |
| CRIT-2 | CRITICAL | Prompt (line 26) vs Template (lines 312-319) | JSON-LD prohibited in prompt but 3 blocks present in template after author section | Template violates prompt rule "no JSON-LD" and "nothing after author section". | Phase 8 (schema), Phase 9 (prompt) |
| BUG-1 | CRITICAL | Workflow (line 302) | Clean HTML node preserves #om-top style block (regex negative lookahead) then throws error if any style block exists | Workflow ALWAYS fails when LLM correctly follows prompt's style block instruction. Self-defeating logic. | Phase 9 |
| BUG-2 | CRITICAL | Workflow (line 261) | Build Final HTML Prompt node contains "MUST include style block" AND "Inline CSS only" in consecutive instructions | Same contradiction as CRIT-1 but embedded inside workflow node's JavaScript string. | Phase 9 |
| H1 | HIGH | Template (38 occurrences) | 38 `class="..."` attributes (omfs, omic, omtl, ompb, omcta, omab, omsl, omfb) | Dead weight. Classes only work via `<style>` block which is stripped. Handlers use `this.style`. ~400 bytes wasted. | Phase 3 |
| H2 | HIGH | Template (24 lines), Prompt (18+ lines), Workflow (17+ lines) | All oritmartin.com references (58 total replacement points across 3 files) | Wrong brand/domain displayed. All URLs, brand mentions, JSON-LD data point to oritmartin.com. | Phase 2 (discovery), Phase 7 (author/brand), Phase 9 (prompt/workflow) |
| H3 | HIGH | Template (lines 54, 63, 72, 81, 90, 99) | 6 `wixstatic.com` image URLs for product images | External CDN hotlinking. Wix may change URLs, add protection, or restructure CDN. Images break silently. | Phase 5 |
| H4 | HIGH | Template (7 occurrences: lines 54, 63, 72, 81, 90, 99, 284, 293) | `display:block` on `<img>` elements and CTA `<a>` | `display:block` stripped. Images revert to inline (spacing changes). CTA loses block centering. | Phase 3 (architecture), Phase 5 (products) |
| HIGH-1 | HIGH | Prompt (lines 167, 226, 262, 276) | Prompt instructs LLM to generate `display:flex` and `display:grid` patterns | Every flex/grid instruction produces HTML that collapses in WordPress. Accordion indicator, product grid, author buttons all break. | Phase 9 |
| HIGH-2 | HIGH | Prompt (18+ occurrences across 20 lines) | All oritmartin.com hardcoded data in prompt | Not parameterized. Every site-specific reference must change for hipsterstyle deployment. | Phase 9 |
| HIGH-3 | HIGH | Prompt vs Template | Prompt-to-template drift: WhatsApp button in template but not in prompt; style block partial match | Undocumented elements and partial implementation mismatches. | Phase 9 |
| BUG-3 | HIGH | Workflow (lines 205, 272) | LLM API uses `maximo-api-key` credentials | May be wrong credentials for hipsterstyle deployment. If invalid, both LLM calls fail silently. | Phase 9 |
| BUG-4 | HIGH | Workflow (line 334) | WordPress Publish content escaping -- `$json.content` with double quotes breaks JSON | Unescaped double quotes in HTML attributes break the JSON body. Intermittent publish failures. | Phase 9 |
| M1 | MEDIUM | Template (7 occurrences) | `ontoggle` handlers on `<details>` elements | Stripped without `unfiltered_html`. Accordion rotation animation stops. Open/close still works natively. | Phase 4 (TOC), Phase 6 (FAQ) |
| M2 | MEDIUM | Template (28+28 handlers) | `onmouseover`/`onmouseout` handlers on interactive elements | All hover effects disappear without `unfiltered_html`. Base states verified visible -- PASS. | Phase 3 (verify base states) |
| M3 | MEDIUM | Template (lines 286, 290, 308) | Floating buttons with `position:fixed` -- WhatsApp on right may conflict with theme | Position CSS properties are safe. But WhatsApp on right side while others on left is inconsistent for RTL. | Phase 7 |
| M4 | MEDIUM | Template (lines 312-319) | 3 JSON-LD `<script>` blocks with oritmartin.com data | Allowed for `unfiltered_html` users. Contains wrong brand data throughout. | Phase 8 |
| M5 | MEDIUM | Template (lines 214, 292) | `background:linear-gradient(...)` in inline styles | Should survive via `background-image` on safe_style_css. LOW actual risk. | Phase 3 (verify) |
| MED-1 | MEDIUM | Prompt (lines 313, 319, 320) | QA checklist items contradict body instructions | "No style block exists" contradicts lines 18, 29-44. "Nothing after author section" contradicts JSON-LD placement. | Phase 9 |
| MED-2 | MEDIUM | Prompt (lines 18 vs 120, lines 115 vs 121) | Ambiguous CSS instructions (inline + style vs inline only, handlers + complete without JS) | Confusing but not strictly contradictory for the handler case. | Phase 9 |
| MED-3 | MEDIUM | Prompt (lines 83, 86, 92-96) | N8N expression syntax -- node references are string-name-based | Valid syntax but fragile. If node names change, expressions silently return undefined. | Phase 9 |
| BUG-5 | MEDIUM | Workflow (line 407) | Error Handler (Slack) node not connected -- `errorWorkflow` empty | Errors in mid-pipeline never trigger Slack notification. Only visible in N8N execution log. | Phase 9 |
| BUG-6 | MEDIUM | Workflow (lines 358, 413) | Slack notifications hardcode "Orit Martin" | Notification messages reference wrong brand. Confusing for operators. | Phase 9 |
| BUG-7 | MEDIUM | Workflow (line 194) | Build Blog Brief prompt injection risk -- user content concatenated without sanitization | If `docContent` contains prompt injection, it passes directly into LLM. | Phase 9 |
| L1 | LOW | Template (8 occurrences) | `box-sizing:border-box` -- uncertain safe_style_css status | If stripped, padding calculations change. Low visual impact due to max-width constraints. | Phase 3 |
| L2 | LOW | Template (lines 21, 37) | Redundant `dir="rtl"` on inner `<ul>` elements | Inherits from article root. Dead weight (~18 bytes). | Phase 3 |
| L3 | LOW | Template (multiple body text sections) | Missing explicit `text-align:right` on text paragraph containers | Relies on inherited RTL. WP theme CSS may override with `text-align:left`. | Phase 3 |

**Total issues: 34** (11 CRITICAL, 9 HIGH, 11 MEDIUM, 3 LOW)

### 2b. The display Property Problem

The single most impactful issue across the entire template. This section explains why and provides fix strategy options.

**Scale of impact:**
- 64 total occurrences of `display:` in the template
- Breakdown: `flex` (27), `inline-flex` (25), `grid` (1), `block` (8), `inline-block` (1), `none` (2 in style block)
- Affects: product card grid, all accordion summaries, all button containers, all CTA links, all social links, all floating buttons, author section layout

**Root cause:** The `display` CSS property is NOT on WordPress's default `safe_style_css` whitelist. The `safecss_filter_attr()` function in `wp-includes/kses.php` strips any CSS property not in the allowed list. `display` has never been added to the default list as of WordPress 6.7+.

**Paradox:** All flex/grid child properties ARE on the whitelist:
- `flex-direction`, `align-items`, `justify-content`, `gap`, `flex-wrap`, `flex-shrink`, `flex` (shorthand) -- all allowed since WP 5.3+
- `grid-template-columns` -- allowed
- But these properties have ZERO effect without their parent `display:flex` or `display:grid`

**Fix strategy options:**

**Option A: Add `display` to `safe_style_css` filter on target WordPress**
```php
add_filter('safe_style_css', function($styles) {
    $styles[] = 'display';
    return $styles;
});
```
- Pros: No template redesign needed. All flex/grid layouts work as-is.
- Cons: Requires server access to mahsan.websreport.net. Theme/plugin update could remove the filter. Not portable to other WordPress sites.

**Option B: Redesign all layouts without `display` property (RECOMMENDED)**
- Replace `display:flex` + `justify-content:center` with `text-align:center` on parent
- Replace `display:flex` + `align-items:center` on summary with `overflow:hidden` + float-based positioning
- Replace `display:grid` with percentage-based widths using `calc()` (safe since WP 5.8) and natural block flow
- Replace `display:inline-flex` on buttons with natural inline rendering + explicit padding + `vertical-align:middle`
- `display:block` on images replaced with `vertical-align:top` or `vertical-align:middle`

**Recommendation:** Design for Option B (no display property) as defensive default. Test Option A on target WordPress in Phase 10 as enhancement. This ensures the template works on ANY WordPress installation without server-side modifications.

### 2c. unfiltered_html Dependency Map

Every feature that depends on the `unfiltered_html` WordPress capability.

| Feature | Handler Type | Count | Graceful Degradation? | Impact Without |
|---------|-------------|-------|----------------------|----------------|
| Hover effects (color shifts, transforms) | `onmouseover` / `onmouseout` | 28 pairs (56 total handlers) | YES -- all base inline styles show fully visible text, buttons, and links. Hover is purely decorative. | No visual feedback on hover. All content still visible and functional. |
| Accordion +/- rotation animation | `ontoggle` | 7 handlers (1 TOC + 6 FAQ) | YES -- `<details>/<summary>` open/close works natively. The + indicator just stays static. | Plus sign doesn't rotate to minus. Accordion still opens/closes. |
| JSON-LD structured data | `<script type="application/ld+json">` | 3 blocks (Article, LocalBusiness, FAQPage) | YES for users -- schema is invisible. NO for SEO -- structured data lost. | No rich snippets in search results. No local business data for Google. |

**Key insight:** The N8N pipeline publishes via WordPress admin API credentials, which typically have `unfiltered_html` capability. All event handlers and script blocks SHOULD survive in the published post. However, defensive design requires all base states to be visually complete without JavaScript.

**Verification result:** PASS. All 56 hover handlers affect only decorative properties (background color, border color, text-decoration, transform). No text is hidden, no content depends on hover state for visibility.

---

## 3. Prioritized Change List

Master driving document for all subsequent phases. Ordered by execution dependency.

### Priority 1 -- Architectural Foundation (Phase 3)

The template's CSS architecture must be rebuilt before any section-specific work.

| # | Change | Affected Lines | Rationale |
|---|--------|---------------|-----------|
| 1.1 | Remove `<style>` block entirely (lines 2-14) | 12 lines deleted | WordPress strips it. Hover effects already duplicated via inline handlers. Marker hiding replaced with `list-style:none` (already present on summaries). |
| 1.2 | Remove all 38 `class="..."` attributes | 38 attributes across template | Dead weight without style block. Handlers use `this.style` directly. Saves ~400 bytes. |
| 1.3 | Replace all `display:flex/grid/inline-flex/inline-block/block` with WordPress-safe alternatives | 64 occurrences | `display` NOT on safe_style_css. Use `text-align:center`, `overflow:hidden` + floats, `calc()` widths, `vertical-align`, natural block flow. |
| 1.4 | Establish inline-only CSS architecture | Entire template | All styling via inline `style=""` attributes. No class selectors, no style blocks, no external CSS. |
| 1.5 | Add explicit `text-align:right` to all text containers | Body text sections (lines 108-221) | Guard against WordPress theme CSS overriding inherited RTL alignment. |
| 1.6 | Remove redundant `dir="rtl"` from inner elements | Lines 21, 37 | Inherits from `<article dir="rtl">`. Cleanup only. |
| 1.7 | Verify `box-sizing:border-box` survival | 8 occurrences | Uncertain safe_style_css status. If stripped, adjust padding/width calculations. |
| 1.8 | Verify `linear-gradient` survival in `background` | Lines 214, 292 | Should survive via `background-image`. Low risk but verify on target WP. |

### Priority 2 -- Content Discovery (Phase 2)

All TBD replacement values must be resolved before template rebuild can complete.

| # | Discovery Task | Method | Blocking Count |
|---|---------------|--------|----------------|
| 2.1 | Resolve hipsterstyle.co.il site structure (about, gallery, contact paths) | Firecrawl `/v1/map` | 19 URLs across 3 files |
| 2.2 | Discover real product page URLs (6 products needed) | Firecrawl inner page crawl | 14 URL occurrences in template |
| 2.3 | Verify social profile URLs (Facebook, Instagram) | Firecrawl social discovery or manual | 4 occurrences per profile |
| 2.4 | Get hipsterstyle contact info (phone, email) | Firecrawl contact page scrape or manual | 6 phone + 4 email occurrences |
| 2.5 | Get hipsterstyle brand/author name (Hebrew + English) | Manual verification | 18+ text references |
| 2.6 | Extract product images for Supabase upload | Firecrawl image extraction from product pages | 6 wixstatic URLs to replace |

**Total Phase 2 dependencies:** 14 unique TBD values blocking 58 replacement points.

### Priority 3 -- Section Rebuilds (Phases 4-7)

Each section has specific issues from the audit that must be addressed during its rebuild.

**Phase 4 -- TOC Section:**
- C3 (partial): `display:flex` on TOC `<summary>` (line 32) -- replace with float-based indicator positioning
- C7 (partial): `display:inline-flex` on TOC links (line 34) -- replace with inline + padding
- M1 (partial): `ontoggle` handler on TOC `<details>` (line 31) -- keep for animation, ensure static + is acceptable
- TOC hover handlers (lines 38-43) -- verify base states acceptable

**Phase 5 -- Product Cards:**
- C2: `display:grid` on product container (line 51) -- replace with `calc()` percentage widths
- C4: `display:flex;flex-direction:column` on 6 card containers -- rely on natural block stacking
- C5: `display:flex;align-items:center;justify-content:center` on 6 image links -- use `text-align:center` + `margin:0 auto`
- H3: 6 `wixstatic.com` URLs -- upload to Supabase, replace with stable URLs
- H4 (partial): `display:block` on product images -- use `vertical-align:top`

**Phase 6 -- FAQ Section:**
- C3 (partial): `display:flex` on 6 FAQ `<summary>` elements (lines 226-271) -- same float-based fix as TOC
- C7 (partial): `display:inline-flex` on FAQ accordion indicators -- inline + padding
- M1 (partial): `ontoggle` on 6 FAQ `<details>` -- keep, ensure static state acceptable

**Phase 7 -- Author Section, Social Links, Floating UI:**
- C6: `display:flex` on 2 author button containers (lines 297, 302) -- `text-align:center` on parent
- C7 (partial): `display:inline-flex` on social links, floating buttons (lines 286, 290, 298-300, 303-304, 308) -- inline + padding
- H2 (partial): oritmartin.com references in author section -- replace with hipsterstyle data from Phase 2
- M3: WhatsApp button on right side conflicts with RTL conventions -- evaluate side placement
- H4 (partial): `display:block` on CTA (line 284) -- wrap in centered `<div>` instead

### Priority 4 -- Cross-Cutting Concerns (Phase 8)

| # | Change | Source Issue(s) | Details |
|---|--------|----------------|---------|
| 4.1 | JSON-LD schema fixes | M4, CRIT-2 | Remove all oritmartin.com data from Article, LocalBusiness, FAQPage schemas. Replace with hipsterstyle equivalents. |
| 4.2 | JSON-LD placement decision | CRIT-2 | Resolve prompt Line 26 prohibition. Recommendation: keep JSON-LD (valuable for SEO) but move inside article before closing tag or make explicit prompt exception. |
| 4.3 | Hover state audit | M2 | Verify ALL base inline styles are visually complete without JavaScript. Current template PASSES but must re-verify after Phase 3-7 rebuilds. |
| 4.4 | SEO heading hierarchy verification | -- | Verify H2 structure matches TOC anchors and FAQ schema after all section rebuilds. |

### Priority 5 -- N8N Alignment (Phase 9)

| # | Change | Source Issue(s) | Details |
|---|--------|----------------|---------|
| 5.1 | Remove MANDATORY CSS BLOCK from prompt (lines 28-44) | CRIT-1 | Keep FORBIDDEN PATTERNS (line 292) as authoritative. Remove "one `<style>` block" from line 18. |
| 5.2 | Resolve JSON-LD policy in prompt | CRIT-2 | Update line 26 to allow JSON-LD explicitly. Add placement instructions. |
| 5.3 | Replace all `display:flex/grid` instructions in prompt | HIGH-1 | Lines 167, 226, 262, 276 must use WordPress-safe alternatives. Document `display` gap in prompt's WP Hardening section. |
| 5.4 | Parameterize all oritmartin.com references | HIGH-2, H2, BUG-6 | Extract 18+ prompt references + 17+ workflow references into variables. Use Normalize Input node for injection. |
| 5.5 | Fix Clean HTML node self-contradiction | BUG-1 | Remove preserve-then-reject logic. Strip ALL style blocks unconditionally: `html.replace(/<style[\s\S]*?<\/style>/gi, '')`. |
| 5.6 | Fix Build Final HTML Prompt embedded contradiction | BUG-2 | Remove "MUST include style block" from embedded prompt string. Keep "Inline CSS only" as authoritative. |
| 5.7 | Fix WordPress Publish content escaping | BUG-4 | Replace raw expression interpolation with Code node using `JSON.stringify()` for proper HTML escaping. |
| 5.8 | Connect Error Handler node | BUG-5 | Wire Error Handler (Slack) into connections map or set `errorWorkflow` to this workflow's ID. |
| 5.9 | Add prompt injection mitigation | BUG-7 | Wrap source content in `<source_content>` delimiters with instruction to treat as raw text only. |
| 5.10 | Decide prompt source of truth | HIGH-3 | Choose: (A) load TXT file dynamically into Build Final HTML Prompt node, or (B) maintain embedded version and deprecate TXT file. Two copies will drift. |
| 5.11 | Verify Maximo LLM credentials | BUG-3 | Confirm `maximoApiUrl` and `maximo-api-key` valid for hipsterstyle. Consider renaming to generic names. |
| 5.12 | Align QA checklist with body instructions | MED-1 | Remove/update lines 313, 319, 320 to not contradict body instructions after prompt rebuild. |
| 5.13 | Add WhatsApp button to prompt or remove from template | HIGH-3 | Currently undocumented drift. |

### Priority 6 -- Validation (Phase 10)

| # | Validation Task | What It Verifies |
|---|----------------|-----------------|
| 6.1 | Test actual HTML on mahsan.websreport.net | Confirm `display` property behavior on target WordPress. If custom `safe_style_css` filter exists, reassess Option A vs B. |
| 6.2 | Verify wp_kses_post() doesn't strip additional properties | Check `box-sizing`, `scroll-margin-top`, `linear-gradient` on target WP. |
| 6.3 | Responsive QA across viewports | Mobile (320-480px), tablet (768px), desktop (1024-1920px). Verify `clamp()` and `calc()` render correctly. |
| 6.4 | Floating button conflict test | Check z-index:999 against theme elements. Verify no overlap with WP admin bar, cookie banners, chat widgets. |
| 6.5 | JSON-LD validation | Run schema through Google Rich Results Test. Verify Article, LocalBusiness, FAQPage pass. |
| 6.6 | RTL alignment verification | Confirm `text-align:right` renders correctly. Check border accents appear on correct side. |

---

## 4. Open Questions for Phase 2+

### Q1: Target WordPress Version on mahsan.websreport.net
- **What we know:** Must be WP 6.1+ for `clamp()` support. Site is live and accessible.
- **What's unclear:** Exact version, installed security plugins, custom `safe_style_css` filters, theme-level CSS resets.
- **Which phase resolves:** Phase 10 (WordPress rendering QA). Consider checking earlier if server access available.
- **Impact if unresolved:** May design for Option B (no display) when Option A (filter) would suffice. Low risk -- Option B is more portable anyway.

### Q2: Whether Target WP Has Custom safe_style_css Filter Adding display
- **What we know:** Default WordPress does NOT allow `display`. Some themes/plugins add it.
- **What's unclear:** The specific configuration of mahsan.websreport.net.
- **Which phase resolves:** Phase 10 via actual rendering test.
- **Recommended test:** Publish a test post containing `<div style="display:flex">test</div>` and inspect rendered HTML.

### Q3: HipsterStyle Contact Info (Phone, Email)
- **What we know:** Main site is hipsterstyle.co.il. WordPress target is mahsan.websreport.net.
- **What's unclear:** Phone number, email address, physical address for LocalBusiness schema.
- **Which phase resolves:** Phase 2 (Firecrawl contact page scrape or manual discovery).
- **Impact if unresolved:** 10+ template references stay as placeholders. JSON-LD LocalBusiness incomplete.

### Q4: HipsterStyle Social Profiles
- **What we know:** Current template has Facebook and Instagram links (both to oritmartin accounts).
- **What's unclear:** Whether hipsterstyle has Facebook, Instagram, YouTube, or other social profiles.
- **Which phase resolves:** Phase 2 (Firecrawl social discovery).
- **Impact if unresolved:** Social links section may have fewer or different networks.

### Q5: Maximo LLM API Credentials for HipsterStyle Deployment
- **What we know:** Workflow uses `maximo-api-key` and `maximoApiUrl` for both LLM calls.
- **What's unclear:** Whether these credentials are valid for hipsterstyle content generation, billing implications, rate limits.
- **Which phase resolves:** Phase 9 (N8N workflow alignment).
- **Impact if unresolved:** Both LLM calls fail. Entire pipeline non-functional.

### Q6: HipsterStyle Brand/Author Identity
- **What we know:** Current template features "Orit Martin" (artist, Jerusalem/Har Nof, spiritual/Kabbalistic art).
- **What's unclear:** Who is the HipsterStyle brand owner? Same person? Different name/identity? Kids styling focus vs spiritual art.
- **Which phase resolves:** Phase 2 (manual verification or Firecrawl about page).
- **Impact if unresolved:** 18+ text references and entire author section need correct identity.

---

## 5. Audit Statistics

| Metric | Value |
|--------|-------|
| **Total issues found** | **34** |
| By severity: CRITICAL | 11 |
| By severity: HIGH | 9 |
| By severity: MEDIUM | 11 |
| By severity: LOW | 3 |
| **Total files affected** | **3** (HTML template, N8N prompt TXT, N8N workflow JSON) |
| **Total line references** | 180+ unique lines cited across all reports |
| **Cross-file contradictions** | 4 (style block mandate/forbid, JSON-LD prohibit/include, prompt-template drift, workflow-prompt contradiction) |
| **Issues requiring Phase 2 discovery** | 14 unique TBD values blocking 58 replacement points |
| **Issues fixable in Phase 3** (architectural) | 8 (biggest single-phase batch: style block, classes, display, inline CSS, text-align, dir cleanup, box-sizing, gradient verify) |
| **Issues fixable in Phase 9** (N8N alignment) | 13 (prompt contradictions, workflow bugs, credential verification, parameterization) |
| **display: occurrences in template** | 64 (the single root cause of 7 CRITICAL issues) |
| **oritmartin references across all files** | 58 replacement points (23 unique values) |
| **wixstatic.com image URLs** | 6 (all need Supabase migration) |
| **Event handlers requiring unfiltered_html** | 63 (28 onmouseover + 28 onmouseout + 7 ontoggle) |
| **Hidden text risk** | NONE -- all base states pass visibility check |

---

*Generated from consolidated analysis of all four Phase 1 audit reports. All issue IDs, line numbers, and severity levels verified against source documents.*
