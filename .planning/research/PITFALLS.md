# Domain Pitfalls

**Domain:** WordPress Article Template System + N8N Automation (Hebrew RTL)
**Project:** HipsterStyle Article System Rebuild
**Researched:** 2026-03-25

---

## Critical Pitfalls

Mistakes that cause rewrites, broken production output, or complete template failure.

---

### Pitfall 1: WordPress `wp_kses_post` Strips CSS Properties You Need

**What goes wrong:** You build a template using `display:flex`, `display:grid`, `gap`, `flex-direction`, `align-items`, `justify-content` in inline styles. WordPress silently strips them. Product card grids collapse to vertical stacks. TOC layouts break. The template looks completely wrong in production despite working in local preview.

**Why it happens:** WordPress's `safecss_filter_attr()` function checks every inline `style` attribute against a whitelist of CSS properties. The default `safe_style_css` list allows background, border, color, font, margin, padding, text, and some column properties. As of WP 5.3+, `grid-template-columns`, `grid-column`, `grid-row` were added. BUT common layout properties like `display`, `flex-direction`, `align-items`, `justify-content`, `gap`, `flex-wrap`, `order`, `flex-grow`, `flex-shrink`, `flex-basis` are **NOT on the default whitelist**. They are stripped silently -- no error, no warning.

**Consequences:**
- Product card grid collapses to single-column stack
- TOC horizontal layout breaks
- FAQ accordion alignment fails
- Floating buttons lose positioning rules
- Template looks completely different in WordPress vs local HTML preview

**Prevention:**
1. **Know the whitelist.** Only use CSS properties that WordPress allows by default: `background-*`, `border-*`, `color`, `font-*`, `margin-*`, `padding-*`, `text-*`, `width`, `height`, `max-width`, `max-height`, `min-width`, `min-height`, `float`, `clear`, `overflow`, `vertical-align`, `list-style-*`, `column-*`, `grid-template-columns`, `grid-column`, `grid-row`.
2. **Avoid `display:flex` and `display:grid` in inline styles.** Use floats, percentage widths, and `display:inline-block` instead -- these survive sanitization.
3. **Test by passing HTML through `wp_kses_post()` on the target WordPress instance** before calling the template complete.
4. **If you must use flex/grid:** Ensure the site admin has added a `safe_style_css` filter to allow them. Do NOT assume this is done.
5. **Alternative approach for product card grids:** Use `display:inline-block` with fixed widths and `vertical-align:top`. This survives `wp_kses_post` and achieves similar visual results.

**Detection:** Compare template rendering in a raw HTML file vs WordPress post output. If layouts differ, CSS property stripping is the cause.

**Phase:** Must be addressed in Phase 1 (Template Design). Every CSS property in the template must be vetted against the WP whitelist before any layout work begins.

**Confidence:** HIGH -- based on WordPress official docs for `safe_style_css` hook and `safecss_filter_attr()`.

---

### Pitfall 2: `<style>` Blocks Stripped -- Inline-Only Enforcement Is Non-Negotiable

**What goes wrong:** Developer adds a `<style>` block for hover states, animations, media queries, or shared styles. WordPress strips the entire block. All dependent styles vanish. Hover effects disappear, responsive breakpoints stop working, animations freeze.

**Why it happens:** WordPress's content sanitizer (`wp_kses_post`) does NOT allow `<style>` tags in post content for the `post` context. The tag is not in `$allowedposttags`. This is a security measure against CSS-based attacks and content injection.

**Consequences:**
- ALL non-inline styles disappear
- No hover states (`:hover` requires a style block or JS)
- No media queries (responsive design via CSS is impossible)
- No CSS animations (`@keyframes` require style blocks)
- Template appears completely unstyled for anything beyond basic inline properties

**Prevention:**
1. **Every single CSS declaration must be inline** on the element it applies to. No exceptions.
2. **Hover states:** Cannot be done with CSS alone in WordPress post content. Options:
   - Use inline `onmouseover`/`onmouseout` JavaScript attributes (but note: WP may strip these too depending on `unfiltered_html` capability)
   - Accept that hover states won't work in standard WP post content unless `unfiltered_html` is enabled for the publishing user
   - Use `:focus-within` pseudo-class (not available inline)
3. **Responsive design:** Cannot use media queries. Design must use percentage widths, `max-width`, and fluid layouts that work at all sizes without breakpoints.
4. **Animations:** Use CSS `transition` property inline (it IS allowed) for simple state changes, but `@keyframes` animations are impossible.

**Detection:** Search template for `<style`, `@media`, `@keyframes`, `:hover`, `:focus`. If found, they will not survive WordPress.

**Phase:** Phase 1 (Template Design). This is a hard architectural constraint.

**Confidence:** HIGH -- WordPress core behavior, well-documented.

---

### Pitfall 3: The `unfiltered_html` Capability Gate

**What goes wrong:** Template works when posted by an admin user but breaks when posted via N8N API using a different user role. OR template works on one WordPress installation but not another (e.g., multisite vs single site).

**Why it happens:** WordPress applies `wp_kses_post` sanitization ONLY to users who lack the `unfiltered_html` capability. Administrators and Editors on single-site WordPress have this capability by default. But:
- On **WordPress Multisite**, only Super Admins have `unfiltered_html` by default
- If N8N uses an API user with **Author** or **Contributor** role, full kses sanitization is applied
- Some security plugins (Wordfence, Sucuri, iThemes Security) **remove** `unfiltered_html` from all roles
- WordPress.com hosted sites **never** allow `unfiltered_html`

**Consequences:**
- Template works in admin testing but breaks in automated N8N publishing
- Template works on dev/staging but breaks on production (different security config)
- Inline JavaScript event handlers (`onclick`, `onmouseover`) stripped for non-admin users
- Some HTML5 tags may be stripped depending on kses configuration

**Prevention:**
1. **Verify the WordPress user credentials N8N uses** -- must have Administrator role with `unfiltered_html` capability
2. **Test with the exact same API credentials N8N will use** in production
3. **Never depend on `unfiltered_html`** for core template functionality. Design the template to survive full `wp_kses_post` sanitization even without `unfiltered_html`.
4. **Document the required user role** in the N8N workflow setup instructions
5. **Check if security plugins are installed** on the target WordPress site that might strip capabilities

**Detection:** Post the exact same HTML manually as admin, then via N8N API. Compare outputs. Differences indicate capability-related filtering.

**Phase:** Phase 1 (Template Design) for defensive design. Phase 4 (N8N Workflow) for credential verification.

**Confidence:** HIGH -- WordPress core documentation on capabilities system.

---

### Pitfall 4: TOC Anchor Links Break When `id` Attributes Are Stripped

**What goes wrong:** Table of Contents links point to `#section-name` anchors, but the `id` attributes on heading tags (`<h2 id="section-name">`) are stripped by WordPress. Clicking TOC links does nothing or jumps to page top.

**Why it happens:** The `id` attribute IS generally allowed on heading tags in `$allowedposttags` for users with `unfiltered_html`. But for users WITHOUT this capability, attributes may be filtered. Additionally, some themes and page builders add their own heading ID generation, causing conflicts or duplicates.

**Consequences:**
- TOC is completely non-functional (links don't navigate)
- User experience severely degraded for long articles
- SEO impact -- broken internal anchors

**Prevention:**
1. **Use `id` attributes on heading tags** (h2, h3) -- these are in the default allowed attributes for the `post` context
2. **Use simple, lowercase, hyphenated IDs** without special characters: `id="section-name"` not `id="Section: Name!"`
3. **Avoid duplicate IDs** -- WordPress won't flag them but browsers will only scroll to the first one
4. **Do NOT use `name` attribute on anchors** as a fallback -- it's deprecated in HTML5
5. **Test anchor navigation** on the actual WordPress instance after publishing
6. **For Hebrew content:** Use transliterated English IDs, not Hebrew characters. `id="kids-styling"` not `id="עיצוב-ילדים"`. Hebrew characters in IDs may cause encoding issues in URLs.

**Detection:** After publishing, click each TOC link. If page doesn't scroll to heading, IDs were stripped.

**Phase:** Phase 2 (TOC Implementation). Verify on target WordPress immediately after first template test.

**Confidence:** MEDIUM -- `id` is generally allowed for post context, but edge cases exist with security plugins and multisite.

---

### Pitfall 5: RTL Layout Breaks With Physical CSS Properties

**What goes wrong:** Developer uses `margin-left`, `padding-right`, `float:left`, `text-align:left` for layout. In Hebrew RTL context, everything is mirrored incorrectly. Product cards flow wrong direction. TOC alignment is off. Text alignment conflicts with reading direction.

**Why it happens:** Physical CSS properties (`left`, `right`) don't respect `direction:rtl`. They are absolute -- `margin-left:20px` means left side in both LTR and RTL contexts. This is the fundamental problem of RTL CSS.

**Consequences:**
- Content hugs wrong side of container
- Spacing appears on wrong side (e.g., image gap on left instead of right)
- Float-based layouts flow in wrong direction
- Mixed Hebrew/English text renders in wrong order
- Product card grids may appear mirrored or have inconsistent spacing

**Prevention:**
1. **Use `direction:rtl` on the article wrapper** -- this flips flexbox/grid flow direction automatically (but remember, `display:flex` might be stripped by WP)
2. **For floats in RTL:** `float:right` makes content flow left-to-right in RTL context (which is the reading direction). Counter-intuitive but correct.
3. **Use CSS logical properties where WP allows them:** `margin-inline-start`, `margin-inline-end`, `padding-inline-start`, `padding-inline-end`. BUT check if these survive `safe_style_css` (they may NOT be on the whitelist).
4. **Fallback strategy:** Use `margin-right` instead of `margin-left` for RTL spacing. Manually mirror all physical properties.
5. **Set `text-align:right`** explicitly on text containers for Hebrew content
6. **Mixed content (Hebrew + English brand names):** Wrap English text in `<span dir="ltr">` to prevent bidirectional text reordering issues
7. **Test with actual Hebrew content** -- Lorem ipsum won't reveal RTL bugs

**Detection:** Visual inspection with real Hebrew text. Check that text is right-aligned, lists flow RTL, product cards order right-to-left.

**Phase:** Phase 1 (Template Design). RTL must be baked in from the start, not bolted on after.

**Confidence:** HIGH -- well-documented RTL CSS patterns and WordPress RTL support documentation.

---

### Pitfall 6: N8N Expression Injection Produces Malformed HTML

**What goes wrong:** N8N workflow template uses expression syntax `{{ $json.field }}` inside HTML attributes or content. The injected value contains quotes, angle brackets, Hebrew characters with special encoding, or unexpected null/undefined values. Output HTML is malformed. WordPress renders broken content or strips it entirely.

**Why it happens:** N8N expressions perform direct string interpolation without HTML encoding by default. If a product name contains a `"` character, and it's injected into an HTML attribute like `alt="{{ $json.productName }}"`, the output becomes `alt="Product "Name""` -- broken HTML. Similarly, if an AI-generated content block contains unescaped HTML entities, the template structure breaks.

**Consequences:**
- Malformed HTML that WordPress sanitizer then mangles further
- Missing product data (null/undefined renders as empty or literal "undefined")
- Broken image tags when URLs contain special characters
- Article content shifts or disappears when injected data is unexpected shape
- Hard to debug because the error is in the N8N output, not the template itself

**Prevention:**
1. **Validate all N8N expression outputs** -- add a Code node after AI generation to sanitize HTML
2. **Escape HTML entities** in injected values: replace `"` with `&quot;`, `<` with `&lt;`, `>` with `&gt;`
3. **Add null/fallback handling** for every expression: `{{ $json.field || "default value" }}`
4. **Test with edge-case data** -- product names with quotes, Hebrew text with punctuation, empty arrays, missing fields
5. **Use the N8N Code node** to validate the final HTML structure before sending to WordPress (check matching tags, valid attributes)
6. **The N8N prompt injection block must be exact** -- any deviation in expression syntax breaks the entire pipeline. Document the exact expressions and don't let AI "improve" them.
7. **Version control the N8N workflow JSON** -- workflow drift is invisible without it

**Detection:** Check N8N execution logs for HTML output. Validate against an HTML parser. Compare expected vs actual WordPress rendering.

**Phase:** Phase 3 (N8N Prompt) and Phase 4 (N8N Workflow). Build validation nodes into the workflow.

**Confidence:** HIGH -- direct experience from project requirements stating "exact injection block (non-negotiable)."

---

## Moderate Pitfalls

---

### Pitfall 7: Product Card Images Break With External URLs

**What goes wrong:** Product card images reference external URLs from hipsterstyle.co.il or affiliate networks. Images load initially but later become 404s (product removed, URL changed, hotlinking blocked). Cards show broken image icons in production articles.

**Why it happens:** External image URLs are outside your control. E-commerce sites regularly change product URLs, CDN paths change, hotlinking protections block requests from other domains. WordPress caches the post HTML but not the images.

**Prevention:**
1. **Host critical images on Supabase** (as noted in project requirements) -- download and re-upload product images
2. **Use `<img>` tags with explicit `width` and `height` attributes** to prevent layout shift when images fail
3. **Add `onerror` fallback** on img tags: `onerror="this.src='fallback.jpg'"` (but note: `onerror` may be stripped by `wp_kses_post` without `unfiltered_html`)
4. **Use `object-fit:contain`** (it IS on the safe_style_css whitelist as of recent WP versions -- verify on target site) to prevent image distortion
5. **Set `background-color` on image containers** so broken images show a styled placeholder instead of nothing
6. **Periodically validate external URLs** if not self-hosting images

**Detection:** Broken image icons visible on the article. Check browser dev tools network tab for 404 image responses.

**Phase:** Phase 2 (Product Cards). Image hosting strategy must be decided before building cards.

**Confidence:** MEDIUM -- `object-fit` whitelist status needs verification on target WordPress version. Image hosting on Supabase is a project decision already identified.

---

### Pitfall 8: Accordion `<details>/<summary>` Tags May Not Survive WordPress

**What goes wrong:** You implement FAQ and TOC accordions using HTML5 `<details>` and `<summary>` elements (the most accessible, JS-free approach). WordPress strips them because they're not in the default `$allowedposttags`.

**Why it happens:** While WordPress 6.9 (Dec 2025) added a native Accordion block, the `<details>` and `<summary>` HTML tags may or may not be in the `$allowedposttags` whitelist for the `post` context depending on WordPress version and configuration. If they're not allowed, `wp_kses_post` strips them and your accordion content collapses into flat text.

**Consequences:**
- FAQ accordion becomes a flat list of questions and answers (no collapsing)
- TOC becomes an always-visible block (cannot be toggled closed)
- User experience degrades on long articles
- Layout is larger than intended (everything expanded)

**Prevention:**
1. **Test `<details>` and `<summary>` on the target WordPress instance first** before committing to this approach
2. **If stripped:** Fall back to visible-by-default content with styled headings. Accept that true accordion behavior requires either:
   - `unfiltered_html` capability to allow JS event handlers
   - A WordPress plugin that adds the tags to allowed list
   - Admin adding a `wp_kses_allowed_html` filter
3. **Design the FAQ section to look acceptable even when fully expanded** -- this is your safety net
4. **For TOC:** Design it as a simple styled list that defaults to visible. "Closed by default" requires JavaScript or `<details>` -- both may be stripped.

**Detection:** Publish test content with `<details>` tags, view the post. If content is expanded with no toggle, tags were stripped.

**Phase:** Phase 2 (TOC and FAQ). Must verify target WordPress behavior before choosing accordion implementation.

**Confidence:** MEDIUM -- `<details>/<summary>` support in `wp_kses_post` varies by WordPress version. WordPress 6.9+ added Accordion block but that doesn't guarantee raw `<details>` tags pass sanitization in post content.

---

### Pitfall 9: Floating Buttons Z-Index Wars With Theme Elements

**What goes wrong:** "Contact Us" and "Back to Top" floating buttons appear behind the theme's header, cookie consent bar, WooCommerce cart widget, or other fixed-position elements. Or conversely, your buttons cover the theme's navigation.

**Why it happens:** WordPress themes use widely varying z-index values (1 to 99999). There is no standard z-index scale. Your fixed-position buttons compete with:
- Theme sticky header (often z-index: 999-9999)
- Cookie consent popups (often z-index: 99999)
- WooCommerce mini-cart (often z-index: 999)
- Admin bar when logged in (z-index: 99999)
- Other floating button plugins (Buttonizer etc.)

**Consequences:**
- Buttons hidden behind other elements
- Buttons covering critical navigation elements
- Different behavior logged-in vs logged-out (admin bar changes stacking)
- Mobile keyboard can push buttons into weird positions

**Prevention:**
1. **Use `z-index:9999`** for floating buttons -- high enough for most themes, not so high it covers admin bar
2. **Add `position:fixed`** (allowed by `safe_style_css`)
3. **Use `bottom:20px`** (not 0) to avoid mobile browser UI conflicts
4. **Place buttons in bottom-right** (or bottom-left for RTL) to minimize header conflicts
5. **For RTL:** Float buttons on bottom-LEFT, as that's the non-reading side
6. **Test with the admin bar visible** -- it adds 32px at the top
7. **Keep buttons small** (48px touch target minimum, but not larger than 56px) to minimize overlap risk
8. **Note:** `position:fixed` IS on the safe_style_css whitelist. Verify `bottom`, `right`, `left` properties are also allowed.

**Detection:** Scroll the page and check button visibility at different scroll positions. Check mobile. Check with admin bar. Check with cookie consent popup.

**Phase:** Phase 2 (Floating Buttons). Test on target WordPress theme specifically.

**Confidence:** MEDIUM -- z-index behavior depends entirely on the target theme. Fixed positioning is generally allowed but needs target-site verification.

---

### Pitfall 10: N8N Workflow JSON Drift From Prompt Template

**What goes wrong:** The N8N prompt template (TXT file) describes a structure, but the N8N workflow JSON connects nodes differently or uses different field mappings. After editing one, the other becomes out of sync. AI generates content following the prompt, but the workflow processes it expecting a different structure.

**Why it happens:** Three files must stay perfectly synchronized:
1. HTML template (defines structure and CSS)
2. N8N prompt (tells AI what to generate)
3. N8N workflow JSON (defines processing pipeline and WordPress publishing)

When any one is updated independently, the others become stale. The prompt might reference sections the template doesn't have, or the workflow might expect fields the AI doesn't produce.

**Consequences:**
- AI-generated content doesn't match template placeholders
- Workflow fails silently (publishes malformed content)
- Missing sections in published articles
- Published articles have placeholder text like `{{ $json.tocSection }}`
- Debugging requires tracing through all three files to find the mismatch

**Prevention:**
1. **Treat all three files as a single atomic unit** -- never update one without checking the other two
2. **The N8N prompt injection block expressions are NON-NEGOTIABLE** -- document the exact expressions and enforce them
3. **Version all three files together** with the same date suffix (e.g., `2026-03-25`)
4. **Add a validation step in the N8N workflow** (Code node) that checks the AI output contains expected sections before publishing
5. **Create a mapping document** listing every expression in the prompt and where it's used in the template and workflow

**Detection:** Trace each `{{ expression }}` in the prompt through the workflow JSON to the template. If any expression doesn't have a source (workflow) or destination (template), there's drift.

**Phase:** Phase 3 (N8N Prompt) and Phase 4 (N8N Workflow). Synchronization check must be the final step.

**Confidence:** HIGH -- this is explicitly called out in project requirements as "non-negotiable."

---

### Pitfall 11: Responsive Design Without Media Queries

**What goes wrong:** Developer builds a template that looks great on desktop but breaks on mobile. The instinct is to add media queries (`@media (max-width: 768px) { ... }`). But media queries require a `<style>` block, which WordPress strips.

**Why it happens:** Responsive design has been built on media queries for 15+ years. Every CSS tutorial teaches them. But in WordPress post content, you cannot use `<style>` blocks. Inline styles cannot contain media queries.

**Consequences:**
- Desktop layout forced on mobile (tiny text, horizontal scrolling, cut-off cards)
- Product cards too wide for mobile screens
- TOC/FAQ sections overflow on small screens
- Images don't resize
- Floating buttons may overlap content

**Prevention:**
1. **Use fluid/intrinsic design** -- percentage widths, `max-width`, `min-width` in inline styles
2. **Product cards:** Use `width:100%; max-width:300px; display:inline-block` -- they'll wrap naturally on smaller screens
3. **Images:** Always use `max-width:100%; height:auto` -- this is the single most important responsive pattern
4. **Font sizes:** Use relative units where allowed, or set reasonable fixed sizes that work at all viewports
5. **Container width:** `max-width:800px; margin:0 auto; width:100%` creates a readable column that adapts
6. **DO NOT attempt to hide/show elements** for different screen sizes -- you cannot without media queries
7. **Test on actual mobile devices** not just browser resize

**Detection:** View the published article on a 375px-wide mobile device. If horizontal scrolling exists or content is cut off, responsive design is broken.

**Phase:** Phase 1 (Template Design). Fluid design must be the default approach from day one.

**Confidence:** HIGH -- this is a fundamental constraint of WordPress inline CSS-only approach.

---

## Minor Pitfalls

---

### Pitfall 12: Hebrew Text Direction in Mixed Content

**What goes wrong:** Article contains Hebrew text with embedded English brand names, product model numbers, URLs, or technical terms. The Unicode Bidirectional Algorithm renders these in unexpected order. "Nike Air Max 90 בצבע שחור" might render the English words in reversed order or in the wrong position.

**Prevention:**
1. Wrap English text spans in `<span dir="ltr">` to isolate direction
2. Use `&#x200F;` (Right-to-Left Mark) before Hebrew text that follows English
3. Test with real product names that mix languages
4. Keep English segments short and within their own inline elements

**Phase:** Phase 2 (Content sections). Test with actual Hebrew article content.

**Confidence:** HIGH -- well-documented Unicode BiDi behavior.

---

### Pitfall 13: WordPress Auto-Formatting (wpautop) Mangles HTML

**What goes wrong:** WordPress's `wpautop()` function automatically wraps content in `<p>` tags and converts double line breaks to paragraph breaks. This can insert unexpected `<p>` and `<br>` tags inside your carefully structured template HTML, breaking layouts.

**Prevention:**
1. Keep HTML tightly formatted -- no blank lines between elements
2. Avoid line breaks inside block-level elements where WordPress might insert `<p>`
3. The REST API may or may not apply `wpautop` depending on the endpoint and WordPress version
4. Test by examining the rendered HTML source in WordPress (View Source, not the editor)
5. If using Classic Editor or REST API, the raw HTML is generally preserved better than Block Editor content

**Detection:** View page source of published article. Search for unexpected `<p>` or `<br>` tags inside your template structure.

**Phase:** Phase 4 (N8N Workflow). The publishing method affects whether `wpautop` is applied.

**Confidence:** MEDIUM -- behavior varies by WordPress version and publishing method.

---

### Pitfall 14: Image `object-fit` Requires Fixed Container Dimensions

**What goes wrong:** Developer sets `object-fit:contain` on images but doesn't set explicit `width` and `height` on the image or its container. `object-fit` has no effect without defined dimensions. Images still distort or overflow.

**Prevention:**
1. Always pair `object-fit:contain` with explicit `width` and `height` on the `<img>` tag
2. Use `width:100%; height:200px; object-fit:contain` pattern for uniform card images
3. Set `background-color` on image container to fill the space when `object-fit:contain` creates letterboxing
4. Verify `object-fit` is on the target WordPress `safe_style_css` whitelist

**Phase:** Phase 2 (Product Cards).

**Confidence:** HIGH -- standard CSS behavior.

---

### Pitfall 15: N8N Workflow Error Handling Silently Publishes Broken Content

**What goes wrong:** AI node in N8N workflow fails partially (rate limit, timeout, truncated response), but the workflow continues and publishes incomplete or mangled content to WordPress. Article goes live with missing sections, placeholder text, or cut-off content.

**Prevention:**
1. Add an IF node after AI generation to check content length meets minimum threshold
2. Add a Code node to validate expected HTML structure (presence of key sections)
3. Set N8N workflow to **stop on error** rather than continue
4. Add a "draft" status in the WordPress publish step -- publish as Draft first, not Published
5. Add notification (email/Slack) on workflow error so manual review can occur
6. Never auto-publish to "Published" status without human review gate

**Phase:** Phase 4 (N8N Workflow). Error handling nodes must be part of workflow design.

**Confidence:** HIGH -- common N8N workflow pattern issue documented in community forums.

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Template Design (Phase 1) | CSS properties stripped by `safe_style_css` (Pitfall 1) | Vet every CSS property against WP whitelist before use |
| Template Design (Phase 1) | Style blocks stripped (Pitfall 2) | Inline-only from day one, no exceptions |
| Template Design (Phase 1) | RTL physical property mistakes (Pitfall 5) | Set `direction:rtl` on wrapper, manually mirror all LTR properties |
| Template Design (Phase 1) | No media queries for responsive (Pitfall 11) | Fluid design with percentages and max-width only |
| TOC Implementation (Phase 2) | Anchor IDs stripped (Pitfall 4) | Use simple ASCII IDs, test on target WP instance |
| TOC/FAQ Accordion (Phase 2) | `<details>/<summary>` stripped (Pitfall 8) | Test on target WP first; design graceful fallback |
| Product Cards (Phase 2) | External image 404s (Pitfall 7) | Host on Supabase, use explicit dimensions |
| Product Cards (Phase 2) | Grid layout collapses (Pitfall 1) | Use `inline-block` not `flex`/`grid` |
| Floating Buttons (Phase 2) | Z-index conflicts (Pitfall 9) | Use z-index:9999, test with admin bar and theme |
| N8N Prompt (Phase 3) | Expression injection breaks HTML (Pitfall 6) | Escape values, add null fallbacks |
| N8N Prompt (Phase 3) | Prompt/template/workflow drift (Pitfall 10) | Synchronize all three files as atomic unit |
| N8N Workflow (Phase 4) | Wrong API user role (Pitfall 3) | Verify admin + `unfiltered_html` capability |
| N8N Workflow (Phase 4) | Silent publish of broken content (Pitfall 15) | Validation nodes + draft-first publishing |
| N8N Workflow (Phase 4) | `wpautop` mangles HTML (Pitfall 13) | Test REST API behavior on target site |
| WordPress QA (Phase 5) | All pitfalls compound | Full rendering comparison: local HTML vs published WP post |

---

## Sources

### WordPress CSS Sanitization
- [safe_style_css hook - Developer.WordPress.org](https://developer.wordpress.org/reference/hooks/safe_style_css/)
- [safecss_filter_attr() - Developer.WordPress.org](https://developer.wordpress.org/reference/functions/safecss_filter_attr/)
- [WordPress Trac #43215 - Allow wp_kses to pass allowed CSS properties](https://core.trac.wordpress.org/ticket/43215)
- [wp_kses_post() - Developer.WordPress.org](https://developer.wordpress.org/reference/functions/wp_kses_post/)
- [wp_kses_allowed_html() - Developer.WordPress.org](https://developer.wordpress.org/reference/functions/wp_kses_allowed_html/)

### WordPress RTL Support
- [RTL WordPress Theme Problems - Pojo Blog](https://blog.pojo.me/problems-with-rtl-wordpress-themes-and-how-to-avoid-them/)
- [RTL Styling 101](https://rtlstyling.com/posts/rtl-styling/)
- [CSS Logical Properties - Ishadeed](https://ishadeed.com/article/css-logical-properties/)
- [Mixing RTL and LTR Words in WordPress Titles](https://blog.jarrousse.org/2026/02/10/mixing-rtl-and-ltr-words-in-wordpress-titles/)

### WordPress Accordion / TOC
- [TOC block not working with accordion - WordPress.org](https://wordpress.org/support/topic/table-of-contents-block-not-working-with-accordion/)
- [Stabilize Table of Contents Block - Gutenberg Issue #42229](https://github.com/WordPress/gutenberg/issues/42229)
- [Styling accordions in WordPress 6.9 - WordPress Developer Blog](https://developer.wordpress.org/news/2025/10/styling-accordions-in-wordpress-6-9/)

### WordPress Image Issues
- [How to Fix Common Image Issues in WordPress - WPBeginner](https://www.wpbeginner.com/beginners-guide/how-to-fix-common-image-issues-in-wordpress/)
- [10 Common WordPress Image Issues - ShortPixel](https://shortpixel.com/blog/wordpress-image-issues/)

### Floating Button Conflicts
- [Z-index floating button - WordPress.org](https://wordpress.org/support/topic/z-index-floating-button/)
- [WordPress Floating Button Plugins Review 2026](https://wisernotify.com/blog/wordpress-floating-buttons/)

### N8N Workflow Issues
- [N8N Expressions Documentation](https://docs.n8n.io/code/expressions/)
- [N8N WordPress Integration](https://n8n.io/integrations/wordpress/)
- [N8N Security Advisory 2026-01-08](https://blog.n8n.io/security-advisory-20260108/)

### WordPress Inline CSS
- [Inline style removed by WordPress - WordPress.com Forums](https://wordpress.com/forums/topic/inline-style-removed-by-wordpress/)
- [Inline CSS Styling in WordPress - ClarkWP](https://clarkwp.wordpress.com/2013/11/07/inline-css-styling-in-wordpress/)
