---
name: HTML Redesign Mega Skill
source: internal
category: UI/UX
purpose: 17 sub-skills for complete WordPress-safe HTML redesign — responsive layout, RTL, accessibility, conversion CTAs, floating buttons, TOC, trust sections, and N8N sync
when_to_use: When redesigning any HTML page, WordPress post, landing page, or article with comprehensive UI/UX improvements
tags: [html, redesign, wordpress, rtl, hebrew, accessibility, cta, responsive, flexbox, grid]
---

# HTML Redesign Mega Skill

## Purpose
17 sub-skills that chain together for a complete HTML redesign run. WordPress-safe (inline CSS only), RTL-aware, WCAG AA compliant, conversion-optimized.

---

## Sub-Skill 1: Responsive Layout Fixer

### Purpose
Fix broken layouts using CSS Grid and Flexbox. Mobile-first. WordPress-safe.

### Trigger Conditions
- Layout breaks below 768px
- Side-by-side sections stack incorrectly
- Images overflow container
- Content runs edge-to-edge on mobile

### Implementation Pattern
```html
<!-- Mobile-first container -->
<div style="
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  padding: 16px;
  max-width: 1200px;
  margin: 0 auto;
  box-sizing: border-box;
">
  <!-- content -->
</div>
```

**Breakpoints:** 480px (mobile), 768px (tablet), 1024px (desktop), 1280px (wide)
**Rule:** Use inline `style=""` only — no external CSS, no `<style>` blocks that conflict with WordPress theme.

### Example
Before: `<div style="float:left; width:50%">` breaks on mobile.
After: Grid with `auto-fit minmax(280px, 1fr)` adapts to any screen.

---

## Sub-Skill 2: Dashboard UI Cleaner

### Purpose
Improve card spacing, section rhythm, visual hierarchy, and modal sizing in dashboard-style pages.

### Trigger Conditions
- Cards have inconsistent padding
- Sections feel cramped or disconnected
- Visual hierarchy is flat (everything looks equally important)
- Modals are too large or too small

### Implementation Pattern
```html
<!-- Card with consistent spacing -->
<div style="
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  border: 1px solid #e5e7eb;
">
  <h3 style="margin: 0 0 8px; font-size: 16px; font-weight: 600; color: #111827;">Card Title</h3>
  <p style="margin: 0; font-size: 14px; color: #6b7280; line-height: 1.6;">Content here</p>
</div>
```

**Spacing scale:** 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px (4px base)

### Example
Add `padding: 24px; gap: 16px;` to card grid → immediately cleaner visual hierarchy.

---

## Sub-Skill 3: Prompt Studio UX Improver

### Purpose
Multi-stage modal design, sticky headers/footers, scroll behavior for complex multi-step UX patterns.

### Trigger Conditions
- Multi-step form flows feel disconnected
- Users lose context during long modals
- Progress is not visible
- Footer actions get scrolled off screen

### Implementation Pattern
```html
<!-- Sticky modal header -->
<div style="
  position: sticky;
  top: 0;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  padding: 16px 24px;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
">
  <h2 style="margin: 0; font-size: 18px; font-weight: 600;">Step 2 of 4: Configure</h2>
  <div style="display: flex; gap: 8px;">
    <div style="width: 8px; height: 8px; border-radius: 50%; background: #3b82f6;"></div>
    <div style="width: 8px; height: 8px; border-radius: 50%; background: #3b82f6;"></div>
    <div style="width: 8px; height: 8px; border-radius: 50%; background: #d1d5db;"></div>
    <div style="width: 8px; height: 8px; border-radius: 50%; background: #d1d5db;"></div>
  </div>
</div>
```

---

## Sub-Skill 4: Keyword Research UI Optimizer

### Purpose
Table layouts, filter controls, data density, sortable column patterns for data-heavy research tools.

### Trigger Conditions
- Tables overflow on mobile
- Data is too dense or too sparse
- No visual differentiation between data rows
- Filters are not obviously interactive

### Implementation Pattern
```html
<!-- Responsive data table -->
<div style="overflow-x: auto; border-radius: 8px; border: 1px solid #e5e7eb;">
  <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
    <thead>
      <tr style="background: #f9fafb;">
        <th style="padding: 12px 16px; text-align: left; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb; white-space: nowrap;">
          Keyword ↕
        </th>
        <th style="padding: 12px 16px; text-align: right; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">Volume</th>
        <th style="padding: 12px 16px; text-align: right; font-weight: 600; color: #374151; border-bottom: 1px solid #e5e7eb;">KD%</th>
      </tr>
    </thead>
  </table>
</div>
```

---

## Sub-Skill 5: Modal / Popup UX System

### Purpose
Correct max-height/width, safe viewport padding, nested scroll prevention, ESC handling pattern.

### Trigger Conditions
- Modal extends beyond viewport height
- Content inside modal doesn't scroll independently
- ESC key closes only inner modal, not outer
- Mobile: modal touches screen edges

### Implementation Pattern
```html
<!-- Modal overlay -->
<div style="
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  padding: 16px;
  z-index: 9999;
" onclick="if(event.target===this)closeModal()">
  <!-- Modal container -->
  <div style="
    background: #fff;
    border-radius: 16px;
    max-width: 640px; width: 100%;
    max-height: calc(100vh - 32px);
    display: flex; flex-direction: column;
    overflow: hidden;
  ">
    <!-- Sticky header -->
    <div style="padding: 20px 24px; border-bottom: 1px solid #e5e7eb; flex-shrink: 0;">
      <h2 style="margin: 0;">Modal Title</h2>
    </div>
    <!-- Scrollable body -->
    <div style="padding: 24px; overflow-y: auto; flex: 1;">Content</div>
    <!-- Sticky footer -->
    <div style="padding: 16px 24px; border-top: 1px solid #e5e7eb; flex-shrink: 0; display: flex; gap: 12px; justify-content: flex-end;">
      <button onclick="closeModal()" style="padding: 10px 20px; border-radius: 8px; border: 1px solid #d1d5db; background: #fff; cursor: pointer;">Cancel</button>
      <button style="padding: 10px 20px; border-radius: 8px; background: #3b82f6; color: #fff; border: none; cursor: pointer;">Confirm</button>
    </div>
  </div>
</div>
<script>
document.addEventListener('keydown', e => { if(e.key === 'Escape') closeModal(); });
</script>
```

---

## Sub-Skill 6: Button & CTA Hierarchy Fixer

### Purpose
Primary/secondary/destructive button hierarchy, hover states, tap targets.

### Trigger Conditions
- All buttons look equally important
- No visual distinction between primary and secondary actions
- Tap targets below 44px minimum
- No hover/focus feedback

### Implementation Pattern
```html
<!-- Primary -->
<button style="
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: #fff; border: none; border-radius: 8px;
  padding: 12px 24px; font-size: 16px; font-weight: 600;
  cursor: pointer; min-height: 44px; min-width: 44px;
  transition: opacity 0.15s; box-shadow: 0 2px 8px rgba(59,130,246,0.3);
" onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">Primary Action</button>

<!-- Secondary -->
<button style="
  background: #fff; color: #374151;
  border: 1.5px solid #d1d5db; border-radius: 8px;
  padding: 12px 24px; font-size: 16px; font-weight: 500;
  cursor: pointer; min-height: 44px;
">Secondary</button>

<!-- Destructive -->
<button style="
  background: #fff; color: #dc2626;
  border: 1.5px solid #fca5a5; border-radius: 8px;
  padding: 12px 24px; font-size: 16px; font-weight: 500;
  cursor: pointer; min-height: 44px;
">Delete</button>
```

---

## Sub-Skill 7: Box / Row / Alignment System

### Purpose
Consistent spacing scale (4px base), border-radius tokens, shadow tokens across all elements.

### Trigger Conditions
- Spacing is inconsistent across components
- Elements don't align to a grid
- Shadow depths vary wildly
- Border-radius is random across cards

### Implementation Pattern
**Spacing tokens:** 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96px
**Border-radius tokens:** 4px (subtle), 8px (default), 12px (card), 16px (modal), 24px (pill), 9999px (round)
**Shadow tokens:**
- xs: `0 1px 2px rgba(0,0,0,0.05)`
- sm: `0 2px 8px rgba(0,0,0,0.08)`
- md: `0 4px 16px rgba(0,0,0,0.12)`
- lg: `0 8px 32px rgba(0,0,0,0.16)`
- xl: `0 16px 48px rgba(0,0,0,0.20)`

---

## Sub-Skill 8: WordPress-Safe HTML Generator

### Purpose
Inline CSS only, no external dependencies, style tags when absolutely necessary, RTL-safe, single H1.

### Trigger Conditions
- Target is WordPress page or post
- External stylesheets not allowed
- Must work in Classic Editor or Gutenberg HTML block
- Content must survive theme updates

### Rules
1. ONLY inline `style=""` attributes — no `<link>`, no external JS
2. `<style>` blocks only inside `<head>` if embedding full page; avoid in post body
3. One `<h1>` per page — use h2-h6 for hierarchy within content
4. All images: explicit width, height, max-width: 100%
5. No `@media` queries in inline styles — use JS for conditional display if needed
6. RTL-safe: use `margin-inline-start` not `margin-left` for RTL compatibility
7. No `!important` unless overriding WordPress theme

### Example
Bad: `<link rel="stylesheet" href="/my-styles.css">`
Good: `<div style="background:#fff; padding:24px; border-radius:12px;">`

---

## Sub-Skill 9: RTL / Hebrew Layout Engine

### Purpose
dir="rtl" on containers, icon placement after text, same-line alignment, chevron direction reversal.

### Trigger Conditions
- Page content is Hebrew, Arabic, or other RTL language
- Icons appear on wrong side in RTL context
- Chevrons point wrong direction
- Text and icon alignment is off

### Implementation Pattern
```html
<!-- RTL container -->
<div dir="rtl" style="text-align: right; font-family: 'Heebo', 'Arial Hebrew', Arial, sans-serif;">

  <!-- RTL row: text first, icon after -->
  <div style="display: flex; align-items: center; gap: 8px; justify-content: flex-start;">
    <span>קרא עוד</span>
    <!-- Chevron points LEFT in RTL context (→ in LTR becomes ← in RTL) -->
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M10 12L6 8L10 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>
  </div>

  <!-- RTL-safe margins -->
  <div style="margin-inline-start: 16px; margin-inline-end: 8px;">Content</div>

</div>
```

**Critical rules:**
- `dir="rtl"` on outermost container, not `text-align: right` alone
- Chevron: `←` in RTL where you'd use `→` in LTR
- Use `margin-inline-start/end` not `margin-left/right`
- Icons follow text in reading order (after text in RTL = visually left of text)

---

## Sub-Skill 10: TOC / FAQ Interaction System

### Purpose
Collapsed by default, smooth animation, chevron icons, no inline-blocked JS events.

### Trigger Conditions
- Long articles need table of contents
- FAQ section with many questions
- Accordion sections needed

### Implementation Pattern
```html
<!-- FAQ Item -->
<details style="border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 8px; overflow: hidden;">
  <summary style="
    padding: 16px 20px; cursor: pointer; font-weight: 600; font-size: 15px;
    display: flex; align-items: center; justify-content: space-between;
    list-style: none; color: #111827;
    background: #f9fafb;
  ">
    <span>What is your refund policy?</span>
    <span style="font-size: 20px; transition: transform 0.2s;" class="faq-chevron">›</span>
  </summary>
  <div style="padding: 16px 20px; color: #374151; line-height: 1.7; font-size: 15px;">
    We offer a 30-day money-back guarantee...
  </div>
</details>
<style>
details[open] .faq-chevron { transform: rotate(90deg); }
details summary::-webkit-details-marker { display: none; }
</style>
```

---

## Sub-Skill 11: Content Spacing Optimizer

### Purpose
Paragraph rhythm, callout blocks, section dividers, reading line length (60-75 chars per line).

### Trigger Conditions
- Text is wall-to-wall without breathing room
- No visual separation between sections
- Line length exceeds comfortable reading width
- No callout blocks for important information

### Implementation Pattern
```html
<!-- Optimal reading container -->
<div style="max-width: 680px; margin: 0 auto; font-size: 16px; line-height: 1.75; color: #374151;">

  <!-- Section divider -->
  <div style="height: 1px; background: #e5e7eb; margin: 40px 0;"></div>

  <!-- Callout block -->
  <div style="
    background: #eff6ff; border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0; padding: 16px 20px; margin: 24px 0;
    color: #1e40af; font-size: 15px; line-height: 1.7;
  ">
    <strong>💡 Key insight:</strong> Important information that deserves emphasis.
  </div>

  <p style="margin: 0 0 20px; line-height: 1.75;">Paragraph with proper spacing...</p>

</div>
```

---

## Sub-Skill 12: Author / Trust Section Builder

### Purpose
Logo + company + bio + trust signals + social links with real hrefs.

### Trigger Conditions
- Article needs author credibility
- Landing page needs trust signals
- Bio section is missing or sparse

### Implementation Pattern
```html
<div style="
  background: #f9fafb; border: 1px solid #e5e7eb;
  border-radius: 16px; padding: 32px;
  display: flex; gap: 24px; align-items: flex-start;
  margin: 48px 0;
">
  <!-- Avatar -->
  <img src="https://example.com/author.jpg" alt="Author Name"
    style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; flex-shrink: 0;"
    width="80" height="80">

  <div style="flex: 1;">
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px; flex-wrap: wrap;">
      <strong style="font-size: 18px; color: #111827;">Author Name</strong>
      <!-- Company badge -->
      <img src="https://example.com/logo.svg" alt="Company" style="height: 20px;" height="20">
    </div>
    <p style="margin: 0 0 12px; color: #6b7280; font-size: 14px;">CEO @ Company · 10 years experience in SEO and content strategy</p>
    <!-- Social links -->
    <div style="display: flex; gap: 12px;">
      <a href="https://linkedin.com/in/author" style="color: #3b82f6; font-size: 14px; text-decoration: none;">LinkedIn ↗</a>
      <a href="https://twitter.com/author" style="color: #3b82f6; font-size: 14px; text-decoration: none;">Twitter ↗</a>
    </div>
    <!-- Trust signals -->
    <div style="display: flex; gap: 16px; margin-top: 12px; flex-wrap: wrap;">
      <span style="font-size: 13px; color: #374151;">✓ Google Certified</span>
      <span style="font-size: 13px; color: #374151;">✓ 500+ articles</span>
      <span style="font-size: 13px; color: #374151;">✓ Featured in Forbes</span>
    </div>
  </div>
</div>
```

---

## Sub-Skill 13: Floating Buttons System

### Purpose
Fixed positioning with correct stacking order: WhatsApp (bottom-left), scroll-to-top (above WhatsApp, right), Contact CTA (bottom-right). Z-index management.

### Trigger Conditions
- Page needs WhatsApp contact button
- Long page needs scroll-to-top button
- Contact form needs persistent CTA

### Implementation Pattern
```html
<!-- WhatsApp - bottom left -->
<a href="https://wa.me/972501234567" target="_blank" rel="noopener"
  style="
    position: fixed; bottom: 20px; left: 20px; z-index: 9998;
    background: #25d366; color: #fff;
    width: 56px; height: 56px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 16px rgba(37,211,102,0.4);
    text-decoration: none; font-size: 28px;
  " aria-label="WhatsApp">📱</a>

<!-- Scroll to top - bottom right, above contact -->
<button onclick="window.scrollTo({top:0,behavior:'smooth'})"
  id="scroll-top-btn"
  style="
    position: fixed; bottom: 90px; right: 20px; z-index: 9997;
    background: #fff; border: 1.5px solid #e5e7eb;
    width: 44px; height: 44px; border-radius: 50%;
    display: none; align-items: center; justify-content: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12); cursor: pointer; font-size: 20px;
  " aria-label="Scroll to top">↑</button>

<!-- Contact CTA - bottom right -->
<a href="#contact"
  style="
    position: fixed; bottom: 20px; right: 20px; z-index: 9998;
    background: linear-gradient(135deg,#3b82f6,#1d4ed8); color: #fff;
    padding: 12px 20px; border-radius: 25px;
    text-decoration: none; font-size: 14px; font-weight: 600;
    box-shadow: 0 4px 16px rgba(59,130,246,0.4);
  ">📞 Contact Us</a>

<script>
const btn = document.getElementById('scroll-top-btn');
window.addEventListener('scroll', () => {
  btn.style.display = window.scrollY > 400 ? 'flex' : 'none';
});
</script>
```

**Z-index order:** WhatsApp/Contact = 9998, Scroll-top = 9997, Modal = 9999, Toast = 10000

---

## Sub-Skill 14: Conversion CTA Engine

### Purpose
Mid-article and end-of-article CTA blocks with gradient backgrounds and dual buttons.

### Trigger Conditions
- Article lacks conversion opportunities in the flow
- Single CTA at very end only
- CTA blocks lack visual urgency or clarity

### Implementation Pattern
```html
<!-- Mid-article CTA -->
<div style="
  background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
  border-radius: 16px; padding: 32px; margin: 48px 0;
  text-align: center; color: #fff;
">
  <p style="margin: 0 0 6px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.1em; opacity: 0.8;">Special Offer</p>
  <h3 style="margin: 0 0 12px; font-size: 24px; font-weight: 700;">Get Your Free Analysis</h3>
  <p style="margin: 0 0 24px; font-size: 16px; opacity: 0.9; max-width: 480px; margin-inline: auto;">Join 500+ businesses who increased traffic by 180%</p>
  <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
    <a href="/contact" style="
      background: #fff; color: #1e3a5f;
      padding: 14px 28px; border-radius: 8px;
      text-decoration: none; font-weight: 700; font-size: 16px;
    ">Get Free Analysis →</a>
    <a href="/services" style="
      background: transparent; color: #fff;
      border: 2px solid rgba(255,255,255,0.6);
      padding: 14px 28px; border-radius: 8px;
      text-decoration: none; font-weight: 600; font-size: 16px;
    ">View Plans</a>
  </div>
</div>
```

---

## Sub-Skill 15: Preview & Rendering Validator

### Purpose
Image src checks, broken link detection, layout shift prevention.

### Trigger Conditions
- Images might have broken src
- Layout shifts on page load (CLS)
- Links might be relative when they should be absolute
- Missing alt text

### Validation Checklist
1. **Image src**: All `<img>` tags have valid absolute URLs (not relative paths like `./image.jpg`)
2. **Image dimensions**: All `<img>` have explicit `width` and `height` attributes to prevent CLS
3. **Image alt**: All `<img>` have meaningful `alt` text (or `alt=""` for decorative)
4. **Links**: All `<a href>` values are valid and absolute for email; relative for web
5. **Max-width**: All images have `max-width: 100%` inline style
6. **WordPress**: No `<script>` tags that conflict with wp-includes; no `<style>` in post body
7. **RTL**: If dir="rtl" page, check all icons/chevrons point correct direction

---

## Sub-Skill 16: HTML + N8N Sync Engine

### Purpose
Workflow credential mapping, color token propagation, domain replacement for N8N-powered HTML workflows.

### Trigger Conditions
- HTML template uses placeholder domains (mapril.co.il, example.com)
- Color tokens need to match a brand palette
- N8N workflow credentials reference wrong domain

### Implementation Pattern
**Domain replacement:**
```powershell
# Replace placeholder domain across all HTML and workflow files
$old = "mapril.co.il"
$new = "yourdomain.com"
Get-ChildItem -Recurse -Include "*.html","*.json" | ForEach-Object {
    (Get-Content $_.FullName) -replace [regex]::Escape($old), $new | Set-Content $_.FullName
}
```

**Color token propagation:**
```javascript
// In HTML template, find and replace primary color tokens
const tokens = {
  '--primary': '#1e3a5f',
  '--accent': '#2563eb',
  '--text': '#111827',
};
// Inject into :root or inline styles
```

**N8N credential mapping:** Ensure `baseUrl` in HTTP Request nodes matches the new domain. Use environment variables in N8N for domain-specific config.

---

## Sub-Skill 17: Accessibility & Contrast Fixer

### Purpose
WCAG AA contrast ratios (4.5:1 for text), hover state readability, focus rings, semantic HTML.

### Trigger Conditions
- Text on colored backgrounds fails contrast check
- Hover states change text to low-contrast color
- No visible focus indicator on interactive elements
- Non-semantic elements used for structure

### Implementation Pattern
```html
<!-- Focus ring for keyboard navigation -->
<style>
*:focus-visible {
  outline: 3px solid #3b82f6;
  outline-offset: 2px;
  border-radius: 4px;
}
</style>

<!-- High contrast text on blue -->
<!-- ✓ PASS: #fff on #2563eb = 4.7:1 -->
<div style="background: #2563eb; color: #ffffff; padding: 16px;">Accessible text</div>

<!-- ✗ FAIL: #6b7280 on #ffffff = 3.2:1 (below 4.5:1) -->
<!-- ✓ FIX: #374151 on #ffffff = 7.9:1 -->

<!-- Semantic HTML -->
<!-- ✗ Bad: <div class="button" onclick="submit()"> -->
<!-- ✓ Good: <button type="submit" aria-label="Submit form"> -->

<!-- Skip navigation link -->
<a href="#main-content" style="
  position: absolute; top: -100px; left: 0;
  background: #000; color: #fff; padding: 8px 16px;
  z-index: 10000; text-decoration: none;
" onfocus="this.style.top='0'">Skip to main content</a>
```

**WCAG AA requirements:**
- Normal text (<18px): 4.5:1 contrast ratio
- Large text (≥18px or ≥14px bold): 3:1 contrast ratio
- UI components and graphical objects: 3:1

---

## MEGA ORCHESTRATION: Complete HTML Redesign Run

### Trigger
"Redesign this HTML page" / "Improve this landing page" / "WordPress page needs complete UX overhaul"

### Execution Sequence

```
Phase 1: AUDIT (Sub-skills 15, 17)
  → Validate images, links, contrast failures
  → Identify accessibility issues
  → Map RTL vs LTR content

Phase 2: STRUCTURE (Sub-skills 1, 8, 9)
  → Fix responsive layout (Grid/Flexbox)
  → Make WordPress-safe (inline CSS only)
  → Apply RTL/Hebrew rules if needed

Phase 3: VISUAL SYSTEM (Sub-skills 2, 7)
  → Apply spacing scale (4px base)
  → Standardize border-radius + shadows
  → Clean up dashboard/card styling

Phase 4: CONTENT UX (Sub-skills 3, 4, 10, 11)
  → Multi-step flows: sticky headers/footers
  → Data tables: responsive + sortable
  → TOC/FAQ: collapsed by default, smooth
  → Content spacing: 680px max-width, line height 1.75

Phase 5: CONVERSION (Sub-skills 6, 12, 13, 14)
  → Button hierarchy: primary/secondary/destructive
  → Author/trust section with real hrefs
  → Floating buttons: WhatsApp/scroll-top/contact
  → Mid-article + end-of-article CTAs

Phase 6: MODALS (Sub-skills 5)
  → Safe viewport, flex column, scroll body
  → ESC handler + click-outside to close

Phase 7: SYNC (Sub-skill 16)
  → Replace placeholder domains
  → Propagate color tokens
  → Validate N8N credential mapping

Phase 8: FINAL VALIDATION (Sub-skills 15, 17)
  → Re-check all image srcs
  → Verify contrast ratios
  → Confirm focus rings present
  → Test RTL alignment
```

### Output
- Single self-contained HTML file
- All CSS inline or in `<style>` block (WordPress-safe mode: inline only)
- No external dependencies except fonts (optional)
- WCAG AA compliant
- Mobile-first, RTL-ready
- Conversion-optimized with 3 CTA touchpoints
