# HTML Template Risk Inventory

**File:** `wp-n8n-html-design-improver/Improved_HTML_Template-claude-code-2026-03-25.html`
**Lines:** 321
**Audit date:** 2026-03-25
**Auditor:** Automated grep-based analysis cross-referenced with WordPress wp_kses_post() safe_style_css whitelist

---

## 1. Executive Summary

| Severity | Count | Description |
|----------|-------|-------------|
| CRITICAL | 7 | Layout-breaking display property usage; style block stripped |
| HIGH | 4 | Dead class attributes; wrong domain URLs; fragile external images; inline-block stripped |
| MEDIUM | 5 | Event handlers require unfiltered_html; floating button placement; JSON-LD site data; gradient verification |
| LOW | 3 | box-sizing uncertainty; redundant dir attributes; missing explicit text-align on text containers |

**Overall risk: CRITICAL.** The template relies on `display:flex`, `display:grid`, and `display:inline-flex` throughout. The `display` CSS property is NOT on WordPress's default `safe_style_css` whitelist. All flex/grid layouts will collapse upon publishing via wp_kses_post(). Additionally, the `<style>` block (lines 2-14) will be completely stripped, removing all hover effects and marker hiding.

**Total display: occurrences:** 64 (27 flex, 1 grid, 25 inline-flex, 1 inline-block, 8 block, 2 none in style block)

---

## 2. CRITICAL Issues

Issues that cause layout collapse, content disappearance, or total functionality loss.

| ID | Line(s) | Pattern | What Happens in WP | Fix Strategy |
|----|---------|---------|---------------------|--------------|
| C1 | 2-14 | `<style>` block containing hover effects (.omcta:hover, .ompb:hover, etc.), accordion rotation animation (#om-top details[open] .omic), and summary marker hiding (summary::-webkit-details-marker) | WordPress strips the entire `<style>` block. All class-based hover effects vanish. The + indicator rotation animation stops. The native summary disclosure marker reappears. | Remove the `<style>` block entirely. Hover effects are already duplicated via inline `onmouseover`/`onmouseout` handlers. Marker hiding must move to inline style `list-style:none` (already present on summaries). Accept that rotation animation requires `unfiltered_html` for the ontoggle handler. |
| C2 | 51 | `display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))` | `display` is stripped by wp_kses_post(). The grid collapses to a single-column block layout. `grid-template-columns` survives on safe_style_css but has no effect without `display:grid`. | Replace with percentage-based widths using `calc()` (on safe_style_css since WP 5.8) and natural block flow. Example: child divs with `width:calc(33.33% - 18px)` and `vertical-align:top`. Or ensure target WP has `display` added to `safe_style_css` via filter. |
| C3 | 32, 226, 235, 244, 253, 262, 271 | `display:flex` on `<summary>` elements (7 occurrences: 1 TOC + 6 FAQ) with `align-items:center;justify-content:space-between` | Summary elements revert to default block display. The flex layout that places text left and + indicator right collapses. Both elements stack vertically. | Use `overflow:hidden` on summary, `float:left` for the + indicator span (RTL: floats reverse visually), and padding-based positioning. Summary defaults to block display which is acceptable with overflow containment. |
| C4 | 52, 61, 70, 79, 88, 97 | `display:flex;flex-direction:column` on product card outer containers (6 occurrences) | Cards lose flex column layout. `flex-direction:column` survives on safe_style_css but is useless without `display:flex`. The `min-width:0` constraint also becomes irrelevant. | Natural block flow already stacks children vertically. Remove `display:flex;flex-direction:column` and rely on default block behavior. The `flex:1` on content divs (lines 56, 65, 74, 83, 92, 101) becomes ineffective but content still renders. |
| C5 | 53, 62, 71, 80, 89, 98 | `display:flex;align-items:center;justify-content:center` on product image `<a>` links (6 occurrences) | Image centering within card container lost. Images fall to default inline/block positioning. | Replace with `text-align:center` on the `<a>` element and `margin:0 auto` on the `<img>`. Both properties are on safe_style_css. |
| C6 | 297, 302 | `display:flex;justify-content:center;gap:10px;flex-wrap:wrap` on author section button container divs (2 occurrences) | Author buttons lose horizontal centered layout. Div is block-level, so children (`<a>` tags with display:inline-flex) stack or flow unexpectedly. | Parent div: use `text-align:center`. Child `<a>` tags: remove `display:inline-flex`, rely on natural inline behavior with explicit padding. `gap` becomes irrelevant; use `margin` on children instead. |
| C7 | 34, 195, 217, 218, 219, 228, 237, 246, 255, 264, 273, 286, 290, 298, 299, 300, 303, 304, 308 | `display:inline-flex` on buttons, CTA links, social links, floating buttons, accordion + indicators (25 occurrences) | All elements revert from inline-flex to default inline. `align-items`, `justify-content`, `gap` properties survive but have no effect without flex context. Visual alignment of icon+text combos breaks. | Replace with explicit padding, `vertical-align:middle` on SVG icons, and `text-align:center`. For button-like elements, `display:inline-block` is equally stripped but natural inline rendering with padding is acceptable. |

---

## 3. HIGH Issues

Significant visual degradation or wrong-site references.

| ID | Line(s) | Pattern | What Happens in WP | Fix Strategy |
|----|---------|---------|---------------------|--------------|
| H1 | 32, 34, 38-43, 58, 67, 76, 85, 94, 103, 195, 218, 219, 226, 228, 235, 237, 244, 246, 253, 255, 262, 264, 271, 273, 284, 286, 290, 298, 299, 300, 303, 304, 308 | 38 `class="..."` attributes (omfs, omic, omtl, ompb, omcta, omab, omsl, omfb) | Dead weight. Classes only have meaning via the `<style>` block which WordPress strips. All handlers use `this.style` directly, not class selectors. Adds ~400 bytes of unnecessary markup. | Remove all `class` attributes. They serve no purpose after the style block is stripped. Hover handlers already use inline `this.style` assignments. |
| H2 | 16, 53, 58, 62, 67, 71, 76, 80, 85, 89, 94, 98, 103, 122, 175, 185, 195, 218, 284, 286, 293, 300, 313, 316 | 24 lines containing `oritmartin.com` references (URLs, brand mentions, JSON-LD data) | Template displays wrong brand/domain. All product links, about links, gallery links, contact links point to oritmartin.com instead of hipsterstyle.co.il. JSON-LD structured data references wrong business. | Full search-and-replace from oritmartin.com to hipsterstyle.co.il. See 04-site-reference-migration-map.md for complete mapping. Product URLs, about page, gallery, contact, social profiles, phone, email all need updating. |
| H3 | 54, 63, 72, 81, 90, 99 | 6 `wixstatic.com` image URLs for product images | External CDN hotlinking. Wix may change URLs on republish, add hotlink protection, or restructure CDN paths. Images break silently. | Upload all 6 images to Supabase storage (per existing pattern -- author portrait already on Supabase at line 293). Replace wixstatic URLs with Supabase public URLs. |
| H4 | 54, 63, 72, 81, 90, 99, 293 | `display:block` on `<img>` elements (7 occurrences: 6 product + 1 author portrait) and `display:block` on line 284 CTA | `display:block` will be stripped. For `<img>`, default is inline which changes spacing and alignment slightly. For the CTA `<a>` on line 284, it loses block-level centering behavior. | For images: `display:block` is mainly to remove inline gap. Use `vertical-align:top` or `vertical-align:middle` instead (on safe_style_css). For the CTA: wrap in a `<div>` with `text-align:center` instead of relying on `display:block` + `margin:0 auto`. |

---

## 4. MEDIUM Issues

Minor visual issues or functionality dependent on unfiltered_html capability.

| ID | Line(s) | Pattern | What Happens in WP | Fix Strategy |
|----|---------|---------|---------------------|--------------|
| M1 | 31, 225, 234, 243, 252, 261, 270 | `ontoggle` handlers on 7 `<details>` elements (1 TOC + 6 FAQ) | Handlers stripped unless user has `unfiltered_html` capability. The + indicator rotation animation stops. Accordion open/close still works natively via `<details>` element behavior. | Keep handlers for admin publishing (N8N publishes via admin API with unfiltered_html). Ensure the + indicator looks acceptable in its static state. Current static state shows "+" which is fine. |
| M2 | 32, 38-43, 58, 67, 76, 85, 94, 103, 195, 226, 235, 244, 253, 262, 271, 284, 286, 290, 298, 299, 300, 303, 304, 308 | 28 `onmouseover` + 28 `onmouseout` handlers | All hover effects disappear without unfiltered_html. Elements display their base inline styles only. | Verify each element's base inline style is visually complete without hover. Current template: all base states have visible backgrounds, colors, and borders. No content is hidden by default. PASS -- base states are acceptable. |
| M3 | 286, 290, 308 | Three floating buttons with `position:fixed`: Contact (left:16px, bottom:72px), Back-to-top (left:16px, bottom:18px), WhatsApp (right:16px, bottom:72px) | `position:fixed`, `z-index`, `bottom`, `left`, `right` are all on safe_style_css. Buttons render correctly. However: WhatsApp on right (line 308) may conflict with WordPress theme's fixed elements (chat widgets, cookie banners). Contact and Back-to-top on left is correct for RTL. Inconsistent side placement. | Review target theme for right-side fixed elements. Consider moving WhatsApp to left side for consistency. Test z-index:999 against theme z-index values. |
| M4 | 312-319 | Three `<script type="application/ld+json">` blocks: Article schema (line 313), LocalBusiness schema (line 316), FAQPage schema (line 319) | Script tags are allowed for users with `unfiltered_html` capability. Content is valid JSON-LD but contains oritmartin.com data throughout. Article schema references wrong author, publisher. LocalBusiness references wrong gallery URL and phone. | Keep JSON-LD structure. Update all oritmartin references to hipsterstyle equivalents. Verify FAQPage schema matches final FAQ content. |
| M5 | 214, 292 | `background:linear-gradient(...)` in inline styles (CTA banner and author section) | `background` shorthand is on safe_style_css. `linear-gradient` is supported via `background-image` since it evaluates to a valid CSS gradient function. Should survive wp_kses_post(). | LOW risk. Verify on target WordPress. If stripped, fall back to solid background color. |

---

## 5. LOW Issues

Cosmetic or minor structural concerns.

| ID | Line(s) | Pattern | What Happens in WP | Fix Strategy |
|----|---------|---------|---------------------|--------------|
| L1 | 1, 53, 62, 71, 80, 89, 98, 284 | `box-sizing:border-box` (8 occurrences) | `box-sizing` is NOT explicitly listed on the default safe_style_css whitelist. If stripped, padding calculations change -- elements may overflow their intended width. | Verify on target WordPress. If stripped, adjust padding/width values to account for content-box model. Low visual impact on most elements since `max-width` constraints contain overflow. |
| L2 | 21, 37 | `dir="rtl"` on inner `<ul>` elements | Redundant -- inherits from `<article dir="rtl">` on line 1. Not harmful, adds ~18 bytes. | Clean up for clarity. Remove redundant `dir` attributes since the article root sets RTL. |
| L3 | Multiple | Missing explicit `text-align:right` on text paragraph containers | In RTL context, browsers default to right alignment. However, WordPress themes may reset text-align on inner elements. Paragraphs could revert to left alignment if theme CSS interferes. | Add explicit `text-align:right` to `<p>` and `<section>` elements that contain Hebrew text. Currently only table (line 124), CTA banners (lines 192, 214, 284), and author section (line 292) have explicit text-align. Body text sections (lines 109-211) rely on inherited RTL. |

---

## 6. CSS Property Audit Summary

Every unique inline CSS property found in the template, with safe_style_css status and occurrence count.

| CSS Property | On safe_style_css? | Occurrences | Risk Level |
|-------------|-------------------|-------------|------------|
| `display` | **NO** | 64 (flex:27, inline-flex:25, grid:1, block:8, inline-block:1, none:2 in style block) | CRITICAL |
| `flex-direction` | YES (WP 5.3+) | 8 | Safe but useless without display:flex |
| `align-items` | YES | ~30 | Safe but useless without display:flex |
| `justify-content` | YES | ~22 | Safe but useless without display:flex |
| `gap` | YES | ~12 | Safe but useless without display:flex/grid |
| `flex-wrap` | YES | 4 | Safe but useless without display:flex |
| `flex-shrink` | YES | 8 | Safe but useless without display:flex |
| `flex` (shorthand) | YES | 8 | Safe but useless without display:flex |
| `margin` / `margin-*` | YES | ~80+ | Safe |
| `padding` / `padding-*` | YES | ~60+ | Safe |
| `font-size` | YES | ~40 | Safe |
| `font-weight` | YES | ~35 | Safe |
| `font-family` | YES | 1 | Safe |
| `color` | YES | ~45 | Safe |
| `background` / `background-color` | YES | ~40 | Safe |
| `border` / `border-*` | YES | ~35 | Safe |
| `border-radius` | YES | ~30 | Safe |
| `box-shadow` | YES | ~12 | Safe |
| `text-decoration` | YES | ~20 | Safe |
| `text-align` | YES | 5 | Safe |
| `line-height` | YES | ~30 | Safe |
| `max-width` | YES | 2 | Safe |
| `min-width` | YES | 2 | Safe |
| `width` | YES | ~12 | Safe |
| `height` | YES | ~10 | Safe |
| `min-height` | YES | ~18 | Safe |
| `max-height` | YES | 6 | Safe |
| `overflow` / `overflow-x` | YES | 8 | Safe |
| `position` | YES | 3 | Safe |
| `z-index` | YES | 3 | Safe |
| `bottom` | YES | 3 | Safe |
| `left` | YES | 2 | Safe |
| `right` | YES | 1 | Safe |
| `object-fit` | YES | 7 | Safe |
| `cursor` | YES | 8 | Safe |
| `list-style` | YES | 7 | Safe |
| `transition` | YES | 8 | Safe |
| `transform` | YES | 0 inline (in handlers only) | Safe when present |
| `filter` | YES | 0 inline (in handlers only) | Safe when present |
| `vertical-align` | YES | 2 | Safe |
| `white-space` | YES | 2 | Safe |
| `scroll-margin-top` | Uncertain | 5 | LOW risk -- decorative |
| `box-sizing` | Uncertain | 8 | LOW risk -- affects padding calc |
| `clamp()` | YES (WP 6.1+) | 6 | Safe |
| `calc()` | YES (WP 5.8+) | 0 (not used yet) | Safe -- available for fix strategies |
| `linear-gradient` | YES (via background) | 2 | Safe |

**Key finding:** 64 of the template's inline style declarations use `display` which is NOT on safe_style_css. This is the single root cause of most CRITICAL issues.

---

## 7. Anchor ID Audit

Every `id="..."` attribute in the template, verified for WordPress safety.

| Line | ID Value | ASCII Safe? | Conflict Risk | Used As Anchor? |
|------|----------|-------------|---------------|-----------------|
| 1 | `om-top` | YES - lowercase, hyphenated | LOW - prefixed with "om" | YES - Back-to-top link target |
| 20 | `article-summary` | YES - lowercase, hyphenated | LOW - descriptive prefix | NO - aria-labelledby reference |
| 49 | `gallery-highlights` | YES - lowercase, hyphenated | LOW - descriptive prefix | NO - aria-labelledby reference |
| 109 | `meaning` | YES - lowercase, simple | MEDIUM - generic name, could conflict with theme/plugin IDs | YES - TOC anchor |
| 119 | `sefirot` | YES - lowercase, simple | LOW - unique term | YES - TOC anchor |
| 172 | `symbols` | YES - lowercase, simple | MEDIUM - somewhat generic | YES - TOC anchor |
| 182 | `choosing` | YES - lowercase, simple | LOW - specific gerund | YES - TOC anchor |
| 198 | `colors` | YES - lowercase, simple | MEDIUM - generic name | YES - TOC anchor |
| 207 | `meditation` | YES - lowercase, simple | LOW - specific term | YES - TOC anchor |
| 224 | `faq-title` | YES - lowercase, hyphenated | LOW - descriptive prefix | NO - aria-labelledby reference |
| 294 | `author-title` | YES - lowercase, hyphenated | LOW - descriptive prefix | NO - aria-labelledby reference |

**Assessment:** All IDs use simple lowercase ASCII with optional hyphens. No Hebrew characters, no spaces, no special characters. WordPress-safe. Minor risk of conflict with generic names (meaning, symbols, colors) if theme or plugins generate similar IDs. Consider prefixing with `om-` for safety (e.g., `om-meaning`, `om-symbols`, `om-colors`).

---

## 8. Floating Button Audit

Three floating buttons with `position:fixed`. All positioning properties verified against safe_style_css.

| Line | Element | Position | z-index | Bottom | Left/Right | Safe? | Theme Conflict Risk |
|------|---------|----------|---------|--------|------------|-------|---------------------|
| 286 | Contact Us button | `position:fixed` | `z-index:999` | `bottom:72px` | `left:16px` | YES -- all properties on safe_style_css | LOW -- left side avoids common theme elements in RTL |
| 290 | Back to Top button | `position:fixed` | `z-index:999` | `bottom:18px` | `left:16px` | YES -- all properties on safe_style_css | LOW -- left side, bottom corner |
| 308 | WhatsApp button | `position:fixed` | `z-index:999` | `bottom:72px` | `right:16px` | YES -- all properties on safe_style_css | MEDIUM -- right side may conflict with theme chat widgets, WP admin bar, cookie consent banners |

**Assessment:**
- Positioning CSS properties (`position`, `z-index`, `bottom`, `left`, `right`) are all on safe_style_css. SAFE.
- `display:inline-flex` on all three buttons will be stripped (CRITICAL -- see C7). Buttons lose flex alignment of icon+text.
- WhatsApp button on RIGHT side while Contact/Back-to-top on LEFT creates inconsistent UX. In RTL layouts, the right side is the "primary" side -- theme elements are more likely there.
- `z-index:999` should be sufficient for most themes but may lose to modals (typically z-index:1000+).

---

## 9. Hidden Text Risk Audit

For each onmouseover/onmouseout handler, document the base inline style state. Verify all text is visible WITHOUT JavaScript execution.

| Line(s) | Element | Base State (visible?) | Hover Change | Risk Without JS |
|---------|---------|----------------------|--------------|-----------------|
| 32 | TOC summary | `background:#fcfbf9` - visible | `background:#f7f2eb` | NONE -- text fully visible |
| 38-43 | TOC links (6) | `color:#7a5b38;text-decoration:none` - visible | `text-decoration:underline;color:#a47b4c` | NONE -- links visible, just no hover underline |
| 58, 67, 76, 85, 94, 103 | Product "view" buttons (6) | `background:#363636;color:#ffffff` - visible | `background:#C4A265` | NONE -- buttons fully visible |
| 195 | CTA call button | `background:#C4A265;color:#ffffff` - visible | No handler on this specific element (class-based only) | NONE |
| 226, 235, 244, 253, 262, 271 | FAQ summaries (6) | `background:#ffffff;color:#2f2f2f` - visible | `background:#f7f2eb` | NONE -- text fully visible |
| 284 | Gallery CTA button | `background:#C4A265;color:#ffffff` - visible | `background:#b99258;transform:translateY(-1px)` | NONE -- button visible |
| 286 | Contact floating button | `background:#C4A265;color:#ffffff` - visible | `background:#b99258;transform:translateY(-1px)` | NONE -- button visible |
| 290 | Back-to-top button | `background:#363636;color:#ffffff` - visible | `background:#4a4038;transform:translateY(-1px)` | NONE -- button visible |
| 298 | Phone button | `background:#C4A265;color:#ffffff` - visible | `background:#b99258` | NONE |
| 299 | Email button | `background:#363636;color:#ffffff` - visible | `background:#4a4038` | NONE |
| 300 | About link | `background:#ffffff;color:#2f2f2f;border:1px solid #e3d8c7` - visible | `borderColor:#C4A265;color:#8c6840` | NONE |
| 303 | Facebook link | `background:#ffffff;color:#2f2f2f;border:1px solid #e3d8c7` - visible | `borderColor:#1877F2;color:#1877F2` | NONE |
| 304 | Instagram link | `background:#ffffff;color:#2f2f2f;border:1px solid #e3d8c7` - visible | `borderColor:#E4405F;color:#E4405F` | NONE |
| 308 | WhatsApp floating button | `background:#25D366` - visible (icon only) | `transform:translateY(-2px)` | NONE |

**Assessment: PASS.** No text is hidden in the base state. All hover effects are purely decorative (color shifts, transforms, underlines). Without JavaScript, all content remains fully visible and readable. No hidden-text SEO risk.

---

## 10. RTL Alignment Audit

| Check | Status | Details |
|-------|--------|---------|
| `dir="rtl"` on article root | PRESENT (line 1) | `<article id="om-top" lang="he" dir="rtl">` |
| `dir="rtl"` on inner elements | REDUNDANT (lines 21, 37) | Two `<ul>` elements have explicit `dir="rtl"` -- unnecessary since inherited from article |
| `text-align:right` on text containers | PARTIAL | Only on table (line 124), CTA banners (lines 192, 214, 284), and author section (line 292) use text-align. Body text sections rely on inherited RTL. |
| Physical CSS: `border-right` | USED CORRECTLY (lines 19, 49, 110, 114, 120, 167, 173, 177, 183, 187, 198, 202, 207, 224) | `border-right:4px solid #C4A265` used as accent line. In RTL, this correctly appears on the right side (the "start" side in Hebrew). |
| Physical CSS: `padding-right` | USED CORRECTLY (lines 49, 110, 120, 173, 183, 198, 208, 224) | `padding-right:14px` on headings -- correct for RTL accent alignment. |
| Physical CSS: `left`/`right` for floating buttons | INTENTIONAL | Contact/Back-to-top: `left:16px` (in RTL, left is the "end" side -- less prominent). WhatsApp: `right:16px` (primary side). |
| `margin-left:auto;margin-right:auto` | PRESENT (line 296) | For centering author bio text. Correct -- works in both LTR and RTL. |
| Physical padding on lists | lines 21, 37 | `padding:0 1.15rem 0 0` -- padding-right only, which is correct for RTL bullet indentation. |

**RTL gaps identified:**
1. **No explicit `text-align:right`** on body `<p>` elements (lines 15-17, 111-113, 121-122, 174-176, 184-186, 200-201, 209-211, 281-282). These rely on inherited `dir="rtl"` which triggers browser default right-alignment. If WordPress theme CSS sets `text-align:left` on `<p>` elements, text will misalign.
2. **Physical property usage** (border-right, padding-right) is correct for Hebrew RTL but would break if the template were ever adapted for LTR. Acceptable since this is a Hebrew-only article system.
3. **`scroll-margin-top`** (lines 109, 119, 172, 182, 198, 207) is direction-independent. SAFE.

**Recommendation:** Add `text-align:right` to all `<p>` and text-containing `<section>` elements to guard against theme CSS interference.
