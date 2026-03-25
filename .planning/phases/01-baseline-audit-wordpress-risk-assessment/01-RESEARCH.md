# Phase 1: Baseline Audit & WordPress Risk Assessment - Research

**Researched:** 2026-03-25
**Domain:** WordPress wp_kses_post sanitization audit of existing HTML template, N8N prompt, and workflow JSON
**Confidence:** HIGH

## Summary

The existing baseline files (HTML template, N8N prompt TXT, N8N workflow JSON) contain multiple WordPress-unsafe patterns and internal contradictions that will cause silent failures in production. The most critical issue is pervasive use of `display:flex` and `display:grid` in inline styles -- the `display` property is NOT on WordPress's default `safe_style_css` whitelist and will be stripped by `wp_kses_post()`, collapsing all grid/flex layouts. This affects product cards, TOC/FAQ accordion summaries, button containers, and the author section.

Additionally, all three files reference `oritmartin.com` throughout and must be updated to `hipsterstyle.co.il`. The HTML template contains a `<style>` block (lines 2-14) that WordPress strips. The prompt file contradicts itself by instructing the LLM to include a `<style>` block (lines 18, 29-44) while also asserting "No style block exists" in the QA checklist (line 320). The workflow JSON Clean HTML node has logic that tries to preserve the `#om-top` style block then immediately fails its own validation that rejects ALL style blocks.

**Primary recommendation:** The audit must produce a line-by-line risk inventory categorized by severity (CRITICAL/HIGH/MEDIUM/LOW), with specific fix strategies for each issue. The planner should structure tasks around: (1) CSS property audit, (2) `<style>` block and class attribute audit, (3) prompt internal contradictions, (4) workflow JSON logic bugs, (5) site reference migration map.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
None -- all implementation choices at Claude's discretion for this audit phase.

### Claude's Discretion
All implementation choices are at Claude's discretion -- pure infrastructure/audit phase. Key focus areas:
- Identify every `<style>` block, class-based selector, and external dependency
- Check wp_kses_post() impact on existing HTML patterns
- Review N8N expression syntax and node references for correctness
- Document RTL alignment risks
- Prioritize changes by WordPress rendering impact severity

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| WP-01 | Inline CSS only -- survives wp_kses_post() sanitization | CSS property audit findings: `display` NOT on safe_style_css; flex/grid layout properties ARE allowed; `<style>` block must be removed |
| WP-02 | No style blocks, no external CSS, no external JS | Template line 2-14 contains `<style>` block; prompt instructs LLM to add it; 38 class attributes are dead weight without it |
| WP-03 | Accordion stable inside WordPress post content | `<details>` and `<summary>` ARE in `$allowedposttags` (verified in WP source); `ontoggle` handlers require `unfiltered_html` capability |
| WP-04 | Anchor IDs reliable after WordPress processing | `id` attribute allowed on headings in post context; current IDs use simple lowercase ASCII -- SAFE |
| WP-05 | Floating buttons do not conflict with theme UI | `position:fixed`, `z-index`, `bottom`, `left`, `right` ARE on safe_style_css -- layout safe; but `display:inline-flex` will be stripped |
| WP-06 | Images use durable URLs (Supabase-backed if needed) | 6 wixstatic.com URLs in template are external/fragile; 1 Supabase URL exists (author portrait) |
| WP-07 | No hidden text risk on hover states | Hover effects use `onmouseover`/`onmouseout` (35 handlers); these require `unfiltered_html`; base state must be fully visible without JS |
| WP-08 | RTL alignment verified for WordPress rendering | `dir="rtl"` on article root; physical CSS properties (border-right accents) used correctly for Hebrew; `text-align` not explicitly set on all containers |
| DEL-07 | Before/after audit summary produced | This audit IS the before-state; audit document will catalog all issues with line numbers |
| DEL-08 | WordPress rendering risk review completed | Full risk inventory with severity levels below |
</phase_requirements>

## Standard Stack

No libraries needed for this audit phase. The audit produces markdown documentation only.

### Tools Used
| Tool | Purpose | Why |
|------|---------|-----|
| grep/search | Line-by-line pattern matching in HTML/TXT/JSON files | Identify all instances of unsafe patterns |
| WordPress source (kses.php) | Verify allowed tags and CSS properties | Ground truth for what survives sanitization |
| Manual code review | Cross-reference prompt vs template vs workflow | Detect contradictions and drift |

## Architecture Patterns

### Audit Document Structure
The audit output should follow this structure:
```
audit/
  01-html-template-risk-inventory.md     # Line-by-line HTML issues
  02-prompt-contradiction-report.md       # Prompt internal contradictions
  03-workflow-logic-bug-report.md         # Workflow JSON issues
  04-site-reference-migration-map.md      # oritmartin -> hipsterstyle mapping
  05-wordpress-rendering-risk-summary.md  # Consolidated risk matrix
```

### Risk Severity Classification
| Severity | Definition | Example |
|----------|-----------|---------|
| CRITICAL | Layout breaks, content disappears, or functionality lost | `display:flex` stripped -> product card grid collapses |
| HIGH | Visual degradation significant enough to look broken | `<style>` block stripped -> all hover/accordion CSS effects lost |
| MEDIUM | Minor visual issues, still functional | `linear-gradient` in background potentially stripped |
| LOW | Cosmetic, won't affect user experience materially | Unused class attributes adding dead weight |

## WordPress CSS Survival Matrix (Verified)

**Confidence: HIGH** -- verified against WordPress core `safecss_filter_attr()` source and `safe_style_css` hook official documentation (March 2026).

### CRITICAL CORRECTION to STACK.md
The prior STACK.md research contained errors about what is and isn't on the safe_style_css whitelist. The corrections below are verified against the WordPress developer reference.

| CSS Property | On safe_style_css? | In Template? | Impact |
|-------------|-------------------|--------------|--------|
| `display` | **NO** | 54 occurrences (flex, grid, inline-flex, inline-block, block) | **CRITICAL** -- all layout collapses |
| `flex-direction` | **YES** (since WP 5.3) | ~18 occurrences | Safe IF display:flex survives (it won't) |
| `align-items` | **YES** | ~30 occurrences | Same -- useless without display:flex |
| `justify-content` | **YES** | ~20 occurrences | Same |
| `gap` | **YES** | ~10 occurrences | Same |
| `flex-wrap` | **YES** | ~4 occurrences | Same |
| `flex-shrink` | **YES** | ~7 occurrences | Same |
| `flex` (shorthand) | **YES** | ~6 occurrences | Same |
| `grid-template-columns` | **YES** | 1 occurrence (line 51) | Safe IF display:grid survives (it won't) |
| `position` | **YES** | 3 occurrences (fixed) | Allowed |
| `z-index` | **YES** | 3 occurrences | Allowed |
| `box-shadow` | **YES** | Multiple | Allowed |
| `object-fit` | **YES** | Multiple | Allowed |
| `border-radius` | **YES** | Multiple | Allowed |
| `clamp()` | **YES** (since WP 6.1) | Multiple | Allowed |
| `linear-gradient` | **YES** (background-image) | 2 occurrences (lines 214, 292) | Allowed via background-image |
| `transition` | **YES** | Multiple | Allowed |
| `transform` | **YES** | Used in hover handlers | Allowed |
| `filter` | **YES** | 1 occurrence (brightness) | Allowed |
| `cursor` | **YES** | Multiple | Allowed |
| `overflow` | **YES** | Multiple | Allowed |

### The Display Property Problem
The `display` property is the single most impactful gap. Without it:
- `display:flex` -> elements revert to browser default (block/inline based on element type)
- `display:grid` -> same, reverts to block
- `display:inline-flex` -> reverts to inline
- `display:inline-block` -> reverts to inline
- `display:block` -> most elements are block by default, so minimal impact

**However**, all flexbox properties (`flex-direction`, `align-items`, `justify-content`, `gap`, `flex-wrap`) ARE on the whitelist. They just have no effect without `display:flex`. The fix strategy is to ensure `display` is added via the `safe_style_css` filter on the target WordPress, OR redesign layouts to not depend on display switching.

### Elements That Use `<details>` and `<summary>`
| Element | Count | WP Allowed? |
|---------|-------|-------------|
| `<details>` | 7 (1 TOC + 6 FAQ) | **YES** -- in `$allowedposttags` with `align` and `open` attributes |
| `<summary>` | 7 | **YES** -- in `$allowedposttags` with `align` attribute |

### Inline Event Handlers
| Handler | Count | WP Behavior |
|---------|-------|-------------|
| `onmouseover` | ~14 | Stripped unless `unfiltered_html` capability |
| `onmouseout` | ~14 | Same |
| `ontoggle` | 7 | Same |

These handlers are allowed for admin-level users with `unfiltered_html` capability. The N8N pipeline publishes via admin API credentials, so they SHOULD survive. However, defensive design requires the template to look acceptable without them.

## HTML Template Risk Inventory

### CRITICAL Issues

| # | Lines | Pattern | Risk | Fix Strategy |
|---|-------|---------|------|--------------|
| C1 | 2-14 | `<style>` block with hover/accordion CSS | WordPress strips entire block. All class-based hover effects, accordion rotation animation, and summary marker hiding vanish. | Remove block entirely. Convert all effects to inline `onmouseover`/`onmouseout` handlers (already partially done) or accept static appearance. |
| C2 | 51 | `display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))` | Product card grid collapses to single column. `display` is stripped; `grid-template-columns` survives but has no effect. | Replace with percentage-based widths + `display:inline-block` approach OR ensure target WP has `display` added to `safe_style_css` filter. |
| C3 | 32, 226, 235, 244, 253, 262, 271 | `display:flex` on `<summary>` elements | Accordion summary layout breaks. The flex layout (text left, + indicator right) collapses. | Summary elements default to block display. Need alternative layout (float-right for + indicator, or padding-based positioning). |
| C4 | 52, 56, 61, 65, 70, 74, 79, 83, 88, 92, 97, 101 | `display:flex;flex-direction:column` on product card containers and inner divs | Product cards lose vertical stacking layout. Content areas lose flex:1 equal-height behavior. | Use natural block flow (elements already stack vertically by default). Remove flex-specific properties. |
| C5 | 53, 62, 71, 80, 89, 98 | `display:flex;align-items:center;justify-content:center` on product image links | Image centering within card container lost. | Use `text-align:center` on parent + `margin:0 auto` on image instead. |
| C6 | 297, 302 | `display:flex;justify-content:center;gap:10px;flex-wrap:wrap` on author button containers | Author section buttons lose horizontal layout. | Use `text-align:center` on parent + `display:inline-block` replacement (but `display` is still stripped). |
| C7 | 217 | `display:inline-flex` on CTA banner button container | Buttons lose inline-flex layout. | Same strategy as C6. |

### HIGH Issues

| # | Lines | Pattern | Risk | Fix Strategy |
|---|-------|---------|------|--------------|
| H1 | 2-14 | 38 `class="..."` attributes throughout template | Dead weight. Classes only have value via the `<style>` block which is stripped. Add bytes without function. | Remove all class attributes OR keep only if hover handlers reference them (they don't -- handlers use `this.style` directly). |
| H2 | All oritmartin.com references (24 in template) | Site references point to wrong domain | Template is for hipsterstyle.co.il, not oritmartin.com. Every URL, every brand mention, author info, social links -- all wrong. | Full search-and-replace audit needed. Map every oritmartin reference to hipsterstyle equivalent. |
| H3 | 54, 63, 72, 81, 90, 99 | 6 `wixstatic.com` image URLs | External CDN images may break on Wix republish. Hotlinking uncertain. | Upload to Supabase and replace URLs (per PROD-10 requirement). |
| H4 | 58, 67, 76, 85, 94, 103, 195, 218, 219, 284, 286, 290, 298-300, 303-304, 308 | `display:inline-flex` on buttons/links (~20 occurrences) | All buttons lose inline-flex centering. Revert to inline elements with no flex alignment. | Replace with `display:inline-block` (also stripped) or accept browser-default inline rendering. Add `text-align:center` and explicit padding for visual fix. |

### MEDIUM Issues

| # | Lines | Pattern | Risk | Fix Strategy |
|---|-------|---------|------|--------------|
| M1 | 31, 225, 234, 243, 252, 261, 270 | `ontoggle` handlers on `<details>` elements | Accordion + rotation animation fails without `unfiltered_html`. Accordion still opens/closes natively. | Keep handlers but ensure base CSS state is acceptable without animation. The + sign just won't rotate. |
| M2 | 32, 38-43, 226, 235, 244, 253, 262, 271 | `onmouseover`/`onmouseout` handlers | Hover effects disappear without `unfiltered_html`. Elements must look complete without them. | Verify each element's base inline style is already acceptable. Current template does this correctly for most elements. |
| M3 | 308 | WhatsApp floating button (`right:16px`) | Positioned on right side -- may conflict with RTL theme right-side elements. Contact/Back-to-top on left (correct for RTL). Inconsistent placement. | Review whether right-side WhatsApp button conflicts with theme. Consider moving all floating buttons to same side. |
| M4 | 312-319 | `<script type="application/ld+json">` blocks (JSON-LD) | Allowed for admin posts (`unfiltered_html`). Contains oritmartin.com data that needs updating. | Keep JSON-LD but update all references. Note: prompt line 26 says "No JSON-LD block" but template includes 3. |
| M5 | 214, 292 | `background:linear-gradient(...)` | Linear gradients in inline style `background` property. `background-image` is on safe_style_css. The shorthand `background` is also allowed. Should survive. | Verify on target WordPress. LOW risk. |

### LOW Issues

| # | Lines | Pattern | Risk | Fix Strategy |
|---|-------|---------|------|--------------|
| L1 | 1 | `box-sizing:border-box` on article wrapper | On safe_style_css? Not explicitly listed. May be stripped. | Verify; if stripped, adjust padding calculations. |
| L2 | 140, 152 | `background:#fbfbfb` on alternating table rows | Inline background on `<tr>` elements. Should survive. | Low risk -- decorative only. |
| L3 | 21, 37 | `dir="rtl"` on inner `<ul>` elements | Redundant -- inherits from `<article dir="rtl">`. Not harmful. | Clean up for clarity but not critical. |

## N8N Prompt Contradiction Report

### CRITICAL: Style Block Contradiction
| Line | Says | Contradicts |
|------|------|-------------|
| 18 | "Inline CSS on each element PLUS one `<style>` block inside the article" | Line 292 "Style blocks" listed in FORBIDDEN PATTERNS |
| 29-44 | Entire "MANDATORY CSS BLOCK" section with exact `<style>` content | Line 320 "No style block exists" in QA CHECKLIST |
| 282 | "No html, head, body, or **style** wrapper" | Lines 29-44 mandate style block |

**Impact:** The LLM receives contradictory instructions. In practice, the current template DOES include the style block (lines 2-14), which means the "MANDATORY CSS BLOCK" instruction won. But the QA checklist fails.

### HIGH: Prompt Says "No JSON-LD" But Template Has It
| Line | Says |
|------|------|
| 26 | "No JSON-LD block at the end. The author section must remain the final section." |
| Template 312-319 | Three JSON-LD script blocks after the author section |

The prompt says no JSON-LD but the template includes it AND places it after the author section, violating another rule.

### MEDIUM: Brand/Site Reference Issues
The prompt hardcodes Orit Martin data throughout:
- Lines 59-68: All verified site facts are oritmartin.com
- Lines 107-108: "Orit Martin's real gallery"
- Lines 208-213, 240-241, 250-251, 257-261: Orit Martin specific instructions
- Lines 269-277: Design colors specific to Orit Martin brand

These all need updating to HipsterStyle brand.

## N8N Workflow Logic Bug Report

### BUG 1: Clean HTML Node Self-Contradiction (CRITICAL)
**Node:** "Clean HTML for WordPress" (line 302 of JSON)
**Code logic:**
1. First: `html.replace(/<style>(?!\s*#om-top)[\s\S]*?<\/style>/gi, '')` -- tries to PRESERVE the #om-top style block while stripping others
2. Then: `if (/<style\b/i.test(html)) throw new Error('Forbidden markup remained after cleanup.')` -- throws error if ANY style block exists

**Result:** If the LLM follows the prompt's "MANDATORY CSS BLOCK" instruction and includes the `<style>` block, step 1 preserves it, then step 2 throws an error. The workflow ALWAYS fails when the LLM obeys the style block instruction.

**Fix:** Either remove the style block instruction from the prompt and strip all style blocks, OR remove the validation check that blocks style blocks.

### BUG 2: Build Final HTML Prompt Also Contradicts (HIGH)
**Node:** "Build Final HTML Prompt" (line 261 of JSON)
The embedded prompt string says both:
- "MUST include one `<style>` block right after the opening `<article id=om-top>` tag"
- "Inline CSS only" (two lines later)

### BUG 3: LLM API Uses Maximo Credentials (MEDIUM)
**Nodes:** "Write Blog Draft (LLM)" and "Render Final HTML (LLM)"
Both use `={{$credentials.maximoApiUrl}}/api/v1/generate` with `maximo-api-key` credentials. This is a custom/internal LLM proxy. Need to verify this is correct for hipsterstyle deployment or if different LLM credentials should be used.

### BUG 4: Error Workflow Not Connected (MEDIUM)
**Node:** "Error Handler (Slack)" exists but `settings.errorWorkflow` is empty string. The error handler node is not connected to any node in the connections map. Errors in mid-workflow nodes will not trigger the Slack notification.

### BUG 5: WordPress Publish Content Escaping (MEDIUM)
**Node:** "Publish to WordPress" (line 334)
Content is injected via N8N expression into JSON: `"content": "{{ $json.content }}"`. If the cleaned HTML contains double quotes (which it does -- every attribute uses them), the JSON becomes malformed. This should use a Code node to properly JSON-encode the content, not raw expression interpolation.

## Site Reference Migration Map

### Files Affected
| File | oritmartin refs | hipsterstyle refs | Action |
|------|----------------|-------------------|--------|
| HTML Template | 24 occurrences | 0 | Full replacement needed |
| N8N Prompt TXT | 9+ occurrences | 0 | Full replacement needed |
| N8N Workflow JSON | 3 occurrences | 0 | Full replacement needed |

### Reference Categories
| Category | Current Value | New Value | Count |
|----------|--------------|-----------|-------|
| Main website URL | oritmartin.com | hipsterstyle.co.il | ~15 |
| About page | oritmartin.com/about | hipsterstyle.co.il/about (verify exists) | ~4 |
| Gallery page | oritmartin.com/gallery | hipsterstyle.co.il equivalent (verify) | ~5 |
| Contact page | oritmartin.com/contact | hipsterstyle.co.il equivalent (verify) | ~4 |
| Phone number | +972587676321 | hipsterstyle phone (TBD) | ~4 |
| Email | orit-26@netvision.net.il | hipsterstyle email (TBD) | ~2 |
| Facebook profile | facebook.com/orit-martin-... | hipsterstyle Facebook (TBD) | ~2 |
| Instagram profile | instagram.com/orit_martin_spiritual_art | hipsterstyle Instagram (TBD) | ~2 |
| Author portrait | supabase.co/.../oritmartin/author-portrait.jpeg | hipsterstyle author image (TBD) | ~2 |
| Product URLs | oritmartin.com/product-page/... | hipsterstyle product pages (TBD) | ~12 |
| Business name | "Orit Martin" / "אורית מרטין" | HipsterStyle brand name (TBD) | ~10 |
| Workflow name/tags | "orit-martin", "oritmartin" | "hipsterstyle" | 3 |

## Common Pitfalls

### Pitfall 1: Auditing Without Testing on Target WordPress
**What goes wrong:** Audit lists theoretical risks based on WP core behavior, but target WordPress (mahsan.websreport.net) may have custom `safe_style_css` filters, security plugins, or theme-level overrides that change what survives.
**Prevention:** Phase 1 audit documents theoretical risks. A future phase MUST test actual HTML snippets on the target WordPress to confirm what actually survives.

### Pitfall 2: Missing the display Property as Root Cause
**What goes wrong:** Auditor flags individual flex properties as problematic when the real issue is that `display:flex` itself is stripped. Without `display:flex`, all flex child properties are meaningless even though they ARE on the whitelist.
**Prevention:** Clearly document that `display` is the root cause. Fix strategies should focus on `display` replacement, not individual flex properties.

### Pitfall 3: Prompt/Template/Workflow Drift After Edits
**What goes wrong:** Fixing the template without updating the prompt and workflow creates new contradictions.
**Prevention:** The audit must map every contradiction across all three files so subsequent phases fix them atomically.

## Code Examples

### Current display:flex Pattern (WILL BREAK)
```html
<!-- Line 32 - TOC summary with flex layout -->
<summary style="cursor:pointer;list-style:none;display:flex;align-items:center;
  justify-content:space-between;gap:12px;padding:15px 18px;...">
```

### Proposed Fix: Float-based Alternative
```html
<!-- Float-based layout that survives wp_kses_post without display property -->
<summary style="cursor:pointer;list-style:none;padding:15px 18px;overflow:hidden;">
  <span style="float:right;">תוכן עניינים</span>
  <span style="float:left;color:#C4A265;font-size:1.1rem;font-weight:700;
    width:20px;height:20px;line-height:20px;text-align:center;">+</span>
</summary>
```

### Current Product Grid (WILL BREAK)
```html
<!-- Line 51 - Grid layout stripped -->
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
  gap:18px;align-items:stretch;">
```

### Proposed Fix: Inline-block Based Grid
```html
<!-- Inline-block approach -- no display property needed -->
<div style="text-align:center;margin:0 -9px;">
  <div style="width:calc(33.33% - 18px);margin:0 9px 18px;
    vertical-align:top;text-align:right;">
    <!-- card content -->
  </div>
</div>
```
Note: `calc()` is on safe_style_css since WP 5.8. `vertical-align` is allowed.

### Workflow Clean HTML Fix
```javascript
// CURRENT (contradictory):
html = html.replace(/<style>(?!\s*#om-top)[\s\S]*?<\/style>/gi, '');
// ...later...
if (/<style\b/i.test(html)) { throw new Error('Forbidden markup'); }

// FIX: Strip ALL style blocks unconditionally
html = html.replace(/<style[\s\S]*?<\/style>/gi, '');
```

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Manual HTML inspection + grep-based pattern matching |
| Config file | none -- audit phase produces documentation only |
| Quick run command | `grep -n "display:" template.html \| wc -l` |
| Full suite command | N/A -- no automated tests for audit deliverables |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| WP-01 | All inline CSS survives wp_kses_post | manual | grep for `display:` and cross-reference safe_style_css | N/A |
| WP-02 | No style blocks | manual | `grep -c "<style" template.html` (should be 0 after fix) | N/A |
| WP-03 | Accordion stable | manual | `grep -c "<details" template.html` + verify in WP | N/A |
| WP-04 | Anchor IDs reliable | manual | `grep 'id="' template.html` + verify simple ASCII | N/A |
| WP-05 | Floating buttons safe | manual | verify `position:fixed` + `z-index` on safe_style_css | N/A |
| WP-06 | Durable image URLs | manual | `grep 'wixstatic' template.html` (should be 0 after fix) | N/A |
| WP-07 | No hidden text on hover | manual | verify base inline style shows all text without JS | N/A |
| WP-08 | RTL alignment | manual | verify `dir="rtl"` + `text-align:right` on text containers | N/A |
| DEL-07 | Before/after audit | manual | audit document produced and committed | N/A |
| DEL-08 | WP rendering risk review | manual | risk matrix with severity levels produced | N/A |

### Sampling Rate
- **Per task commit:** Review audit document sections for completeness
- **Per wave merge:** Cross-reference all three files for consistency
- **Phase gate:** All risk items catalogued with fix strategies before proceeding to Phase 2

### Wave 0 Gaps
None -- audit phase produces markdown documentation, no test infrastructure needed.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `display` not on safe_style_css | Still not on default list (WP 6.7+) | N/A -- never added | Must use alternative layout approaches OR add via filter |
| Flex/grid properties not allowed | Flex/grid child properties added WP 5.3+ | WP 5.3 (Oct 2019) | Usable IF display:flex/grid can be established |
| `<details>`/`<summary>` not in allowedposttags | Added to allowedposttags | Verified in current WP master | Safe to use for accordions |
| `position`, `z-index` not allowed | Added to safe_style_css | WP 5.3+ | Fixed positioning for floating buttons is safe |
| `clamp()` not allowed | Added to safecss_filter_attr | WP 6.1 (Nov 2022) | Responsive typography via clamp() is safe |

## Open Questions

1. **Target WordPress exact version on mahsan.websreport.net**
   - What we know: Must be 6.1+ for clamp() support
   - What's unclear: Exact version, installed security plugins, custom safe_style_css filters
   - Recommendation: Check WP version before Phase 2 implementation begins

2. **HipsterStyle brand assets and URLs**
   - What we know: Main site is hipsterstyle.co.il, WordPress target is mahsan.websreport.net
   - What's unclear: Contact page URL, social profiles, author info, product page structure
   - Recommendation: Phase 2 (Firecrawl discovery) will resolve this; audit should map all replacement points

3. **Whether target WordPress has custom `safe_style_css` filter adding `display`**
   - What we know: Default WP does NOT allow `display`
   - What's unclear: Theme or plugin may have added it
   - Recommendation: Test a simple `<div style="display:flex">test</div>` on target WP before committing to display-less layout strategies

4. **Maximo LLM API credentials for hipsterstyle**
   - What we know: Workflow uses maximo-api-key credentials
   - What's unclear: Whether same credentials work for hipsterstyle deployment
   - Recommendation: Verify during N8N workflow phase

## Sources

### Primary (HIGH confidence)
- [WordPress kses.php source on GitHub](https://github.com/WordPress/WordPress/blob/master/wp-includes/kses.php) -- verified `details`/`summary` in `$allowedposttags`
- [safe_style_css hook - Developer.WordPress.org](https://developer.wordpress.org/reference/hooks/safe_style_css/) -- verified full default CSS property list
- [safecss_filter_attr() - Developer.WordPress.org](https://developer.wordpress.org/reference/functions/safecss_filter_attr/) -- verified `display` NOT on list, flex properties ARE on list
- [WordPress Trac #56122](https://core.trac.wordpress.org/ticket/56122) -- discussion of allowing layout CSS properties
- Direct code analysis of all three baseline files

### Secondary (MEDIUM confidence)
- [wp-mix.com allowed HTML tags](https://wp-mix.com/allowed-html-tags-wp_kses/) -- summary tag in allowedposttags since WP 3.3.1
- [WordPress accordions in 6.9](https://developer.wordpress.org/news/2025/10/styling-accordions-in-wordpress-6-9/) -- native accordion block support

## Metadata

**Confidence breakdown:**
- CSS property survival matrix: HIGH -- verified against WordPress official developer reference and source code
- `<details>`/`<summary>` support: HIGH -- verified in WordPress kses.php source
- Template risk inventory: HIGH -- based on direct grep analysis of all 307 lines
- Prompt contradiction report: HIGH -- direct text comparison within the file
- Workflow logic bug report: HIGH -- direct code analysis of node JavaScript
- Site reference migration: HIGH -- direct grep counts

**Research date:** 2026-03-25
**Valid until:** 2026-04-25 (stable -- WordPress kses behavior changes rarely)
