# SKILL: HTML Redesign Mega Skill — Full System
**Trigger phrases:** redesign HTML, mega redesign, improve template, polish article, premium layout, html cleanup, upgrade article HTML, responsive layout fix, dashboard UI, prompt studio UX, keyword research UI, modal UX, button hierarchy, box alignment, RTL layout, Hebrew layout, TOC interaction, FAQ interaction, floating buttons, conversion CTA, accessibility fix, contrast fix, brand design system, design system extract, HTML N8N sync, preview validator

**Version:** 3.0 — 2026-04-20 Mega Upgrade
**Sub-skills:** 17 active modules
**Inherits:** html-redesign-premium-polish.SKILL.md (all rules preserved)

---

## MODULE INDEX

| # | Module | Purpose | Trigger |
|---|--------|---------|--------|
| 1 | Responsive Layout Fixer | Fix breakpoints, grid, mobile | "responsive", "mobile broken", "layout fix" |
| 2 | Dashboard UI Cleaner | Clean metric cards, stats panels | "dashboard", "metrics UI", "stats panel" |
| 3 | Prompt Studio UX Improver | Textarea, model selector, token UI | "prompt studio", "prompt UI", "AI interface" |
| 4 | Keyword Research UI Optimizer | Tables, filters, bulk actions | "keyword UI", "KW table", "research UI" |
| 5 | Modal / Popup UX System | Overlays, dialogs, drawers | "modal", "popup", "dialog", "drawer" |
| 6 | Button & CTA Hierarchy Fixer | Primary/secondary/ghost/danger | "button hierarchy", "CTA fix", "button system" |
| 7 | Box / Row / Alignment System | Flex/grid layouts, spacing | "alignment", "box system", "layout grid" |
| 8 | WordPress-Safe HTML Generator | WP-safe cards, wpautop rules | "wordpress", "wp safe", "flatsome" |
| 9 | RTL / Hebrew Layout Engine | RTL text, Hebrew UI, bidirectional | "RTL", "Hebrew", "right-to-left" |
| 10 | TOC / FAQ Interaction System | Collapsible TOC, FAQ accordion | "TOC", "FAQ", "accordion", "collapsible" |
| 11 | Content Spacing Optimizer | Rhythm, whitespace, sections | "spacing", "whitespace", "rhythm" |
| 12 | Author / Trust Section Builder | Author box, trust signals, bio | "author box", "trust section", "bio" |
| 13 | Floating Buttons System | Sticky nav, floating CTAs, scroll-to-top | "floating button", "sticky", "scroll top" |
| 14 | Conversion CTA Engine | Hero CTAs, end-article CTAs, banners | "conversion", "CTA engine", "lead gen" |
| 15 | Preview & Rendering Validator | HTML lint, wpautop sim, QA checklist | "validate", "preview", "QA check", "lint" |
| 16 | HTML + N8N Sync Engine | Template variables, N8N handoff | "N8N sync", "template vars", "workflow sync" |
| 17 | Accessibility & Contrast Fixer | WCAG AA, color contrast, ARIA | "accessibility", "contrast", "a11y", "ARIA" |

**BONUS MODULES (new 2026-04-20):**
| B1 | Brand Design System Extractor | Extract any brand's design tokens | "brand system", "extract design", "design tokens" |
| B2 | Animation & Transition System | CSS animations, hover FX, transitions | "animation", "transition", "hover effect" |
| B3 | Email HTML Engine | Email-safe HTML, Resend patterns | "email HTML", "email template", "HTML email" |
| B4 | AEO Content Optimizer | AI-discoverable content structure | "AEO", "AI search ready", "LLM visible" |

---

## MODULE 1 — RESPONSIVE LAYOUT FIXER

### Breakpoints (MANDATORY)
```css
/* Desktop: default (≥769px) */
/* Tablet: @media(max-width:768px) */
/* Mobile: @media(max-width:480px) */
```

### Grid Fix Patterns
```css
/* 3→2→1 column grid */
.dta-grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:1.5rem; }
@media(max-width:768px){ .dta-grid-3 { grid-template-columns:repeat(2,1fr); gap:1rem; } }
@media(max-width:480px){ .dta-grid-3 { grid-template-columns:1fr; } }

/* 2→1 column grid */
.dta-grid-2 { display:grid; grid-template-columns:repeat(2,1fr); gap:1.5rem; }
@media(max-width:480px){ .dta-grid-2 { grid-template-columns:1fr; } }

/* Sidebar layout: 2/3 + 1/3 → stacked */
.dta-sidebar-layout { display:grid; grid-template-columns:2fr 1fr; gap:2rem; }
@media(max-width:768px){ .dta-sidebar-layout { grid-template-columns:1fr; } }
```

### Common Responsive Fixes
- Images: `max-width:100%; height:auto;` on mobile
- Tables: `overflow-x:auto; display:block;` wrapper on mobile
- Font scaling: `clamp(1rem, 2.5vw, 1.25rem)` for fluid typography
- Padding: `padding: 1.5rem 1rem` mobile vs `padding: 2rem 1.5rem` desktop
- Stack horizontal → vertical: `flex-direction:column` at ≤480px

### Responsive Testing Protocol (from awesome-cursor-skills)
1. Check desktop (1280px+): full 3-col grid, sidebar visible
2. Check tablet (768px): 2-col grid, sidebar stacked below
3. Check mobile (375px): single column, full width
4. Verify touch targets ≥44px × 44px
5. Test floating buttons: no overlap with content, fixed position safe

---

## MODULE 2 — DASHBOARD UI CLEANER

### Metric Card Pattern (dark theme)
```html
<div class="dta-metric-card">
  <div class="dta-metric-label">Total Revenue</div>
  <div class="dta-metric-value">$12,480</div>
  <div class="dta-metric-delta dta-delta--up">↑ 12.4% vs last month</div>
</div>
```

```css
.dta-metric-card {
  background: #1a1a2e;
  border: 1px solid rgba(124,58,237,0.15);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  display: flex; flex-direction: column; gap: 0.25rem;
}
.dta-metric-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: #888; }
.dta-metric-value { font-size: 2rem; font-weight: 700; color: #f0f0f5; line-height: 1.1; }
.dta-delta--up { color: #22c55e; font-size: 0.8rem; }
.dta-delta--down { color: #ef4444; font-size: 0.8rem; }
```

### Dashboard Layout Rules
- Top row: 3-4 KPI metric cards
- Charts row: 2/3 main chart + 1/3 breakdown
- Table row: full width data table with pagination
- Use subtle grid lines not heavy borders
- Sidebar nav: 240px fixed, collapses to icon-only at ≤768px
- Background hierarchy: #0a0a0f → #111118 → #1a1a2e → #252540

---

## MODULE 3 — PROMPT STUDIO UX IMPROVER

### Prompt Textarea Pattern
```html
<div class="dta-prompt-studio">
  <div class="dta-prompt-header">
    <label class="dta-prompt-label">Your Prompt</label>
    <span class="dta-token-count">0 / 4096 tokens</span>
  </div>
  <textarea class="dta-prompt-textarea" placeholder="Enter your prompt here..."></textarea>
  <div class="dta-prompt-toolbar">
    <select class="dta-model-select">...</select>
    <div class="dta-prompt-actions">
      <button class="dta-btn dta-btn--ghost">Clear</button>
      <button class="dta-btn dta-btn--primary">Generate →</button>
    </div>
  </div>
</div>
```

```css
.dta-prompt-textarea {
  width: 100%; min-height: 160px; resize: vertical;
  background: #0a0a0f; color: #f0f0f5;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px; padding: 1rem;
  font-family: 'Monaco', 'Courier New', monospace;
  font-size: 0.875rem; line-height: 1.6;
  transition: border-color 0.2s;
}
.dta-prompt-textarea:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 3px rgba(124,58,237,0.15);
}
.dta-model-select {
  background: #1a1a2e; color: #f0f0f5;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 6px; padding: 0.5rem 0.75rem;
  font-size: 0.875rem; cursor: pointer;
}
```

---

## MODULE 4 — KEYWORD RESEARCH UI OPTIMIZER

### KW Table Pattern
```css
.dta-kw-table { width:100%; border-collapse:collapse; font-size:0.875rem; }
.dta-kw-table th {
  text-align:left; padding:0.625rem 0.75rem;
  background:#1a1a2e; color:#888;
  font-size:0.7rem; text-transform:uppercase; letter-spacing:0.05em;
  border-bottom:1px solid rgba(255,255,255,0.08);
  cursor:pointer; /* sortable */
  user-select:none;
}
.dta-kw-table td {
  padding:0.75rem; color:#f0f0f5;
  border-bottom:1px solid rgba(255,255,255,0.04);
  vertical-align:middle;
}
.dta-kw-table tr:hover td { background:rgba(124,58,237,0.06); }
```

### Difficulty Badge System
```css
.dta-diff { display:inline-flex; align-items:center; gap:0.25rem; border-radius:4px; padding:0.2rem 0.5rem; font-size:0.7rem; font-weight:600; }
.dta-diff--easy { background:rgba(34,197,94,0.15); color:#22c55e; }
.dta-diff--medium { background:rgba(234,179,8,0.15); color:#eab308; }
.dta-diff--hard { background:rgba(239,68,68,0.15); color:#ef4444; }
```

---

## MODULE 5 — MODAL / POPUP UX SYSTEM

### CSS-Only Modal (no inline JS — WP-safe)
```html
<input type="checkbox" id="dta-modal-toggle" class="dta-modal-check" hidden>
<label for="dta-modal-toggle" class="dta-modal-open-btn dta-btn dta-btn--primary">Open</label>

<div class="dta-modal-overlay">
  <label for="dta-modal-toggle" class="dta-modal-backdrop"></label>
  <div class="dta-modal">
    <div class="dta-modal-header">
      <h3 class="dta-modal-title">Modal Title</h3>
      <label for="dta-modal-toggle" class="dta-modal-close" aria-label="Close">✕</label>
    </div>
    <div class="dta-modal-body">Content here</div>
    <div class="dta-modal-footer">
      <label for="dta-modal-toggle" class="dta-btn dta-btn--ghost">Cancel</label>
      <button class="dta-btn dta-btn--primary">Confirm</button>
    </div>
  </div>
</div>
```

```css
.dta-modal-check:checked ~ .dta-modal-overlay { display:flex; }
.dta-modal-overlay {
  display:none; position:fixed; inset:0; z-index:1000;
  align-items:center; justify-content:center;
}
.dta-modal-backdrop {
  position:absolute; inset:0;
  background:rgba(0,0,0,0.7); backdrop-filter:blur(4px);
  cursor:pointer;
}
.dta-modal {
  position:relative; z-index:1001;
  background:#111118; border:1px solid rgba(255,255,255,0.08);
  border-radius:16px; padding:2rem;
  width:min(90vw, 480px);
  box-shadow:0 24px 64px rgba(0,0,0,0.5);
  animation: dta-modal-in 0.2s ease;
}
@keyframes dta-modal-in {
  from { opacity:0; transform:translateY(-16px) scale(0.97); }
  to   { opacity:1; transform:translateY(0) scale(1); }
}
```

---

## MODULE 6 — BUTTON & CTA HIERARCHY FIXER

### Complete Button System
```css
/* Base */
.dta-btn {
  display:inline-flex; align-items:center; justify-content:center; gap:0.375rem;
  padding:0.625rem 1.25rem; border-radius:8px;
  font-size:0.875rem; font-weight:600; line-height:1;
  cursor:pointer; border:none; text-decoration:none;
  transition:all 0.15s ease; white-space:nowrap;
  position:relative; overflow:hidden;
}
.dta-btn:focus-visible {
  outline:2px solid #7c3aed; outline-offset:2px;
}

/* Primary */
.dta-btn--primary { background:#7c3aed; color:#fff; }
.dta-btn--primary:hover { background:#6d28d9; transform:translateY(-1px); box-shadow:0 4px 12px rgba(124,58,237,0.4); }
.dta-btn--primary:active { transform:translateY(0); }

/* Secondary */
.dta-btn--secondary { background:#1a1a2e; color:#f0f0f5; border:1px solid rgba(255,255,255,0.12); }
.dta-btn--secondary:hover { background:#252540; border-color:rgba(255,255,255,0.2); }

/* Ghost */
.dta-btn--ghost { background:transparent; color:#a0a0b5; border:1px solid rgba(255,255,255,0.08); }
.dta-btn--ghost:hover { background:rgba(255,255,255,0.05); color:#f0f0f5; }

/* Danger */
.dta-btn--danger { background:#ef4444; color:#fff; }
.dta-btn--danger:hover { background:#dc2626; }

/* Sizes */
.dta-btn--sm { padding:0.4rem 0.875rem; font-size:0.8rem; border-radius:6px; }
.dta-btn--lg { padding:0.875rem 1.75rem; font-size:1rem; border-radius:10px; }
.dta-btn--xl { padding:1rem 2rem; font-size:1.125rem; border-radius:12px; }

/* Disabled */
.dta-btn:disabled, .dta-btn[disabled] { opacity:0.4; cursor:not-allowed; pointer-events:none; }

/* Icon button */
.dta-btn--icon { padding:0.5rem; aspect-ratio:1/1; border-radius:8px; }
```

### Button Hierarchy Rules
1. ONE primary action per screen/section
2. Secondary = supporting actions
3. Ghost = destructive/cancel/low-priority
4. Danger = irreversible destructive actions
5. Buttons ≥44px height for touch targets
6. Icon + text on ONE line — NEVER wrap

---

## MODULE 7 — BOX / ROW / ALIGNMENT SYSTEM

```css
/* Flex utilities */
.dta-flex { display:flex; }
.dta-flex-col { display:flex; flex-direction:column; }
.dta-items-center { align-items:center; }
.dta-items-start { align-items:flex-start; }
.dta-justify-between { justify-content:space-between; }
.dta-justify-center { justify-content:center; }
.dta-gap-1 { gap:0.25rem; } .dta-gap-2 { gap:0.5rem; } .dta-gap-3 { gap:0.75rem; }
.dta-gap-4 { gap:1rem; } .dta-gap-6 { gap:1.5rem; } .dta-gap-8 { gap:2rem; }

/* Box / Card */
.dta-box {
  background:#111118; border:1px solid rgba(255,255,255,0.06);
  border-radius:12px; padding:1.5rem;
}
.dta-box--elevated {
  background:#1a1a2e; border-color:rgba(124,58,237,0.12);
  box-shadow:0 4px 24px rgba(0,0,0,0.2);
}

/* Section wrapper */
.dta-section { margin-bottom:3rem; }
.dta-section-title {
  font-size:1.5rem; font-weight:700; color:#f0f0f5;
  margin-bottom:1.5rem; padding-bottom:0.75rem;
  border-bottom:2px solid rgba(124,58,237,0.2);
}

/* Dividers */
.dta-divider { border:none; border-top:1px solid rgba(255,255,255,0.06); margin:2rem 0; }
```

---

## MODULE 8 — WORDPRESS-SAFE HTML GENERATOR
*(Full rules inherited from html-redesign-premium-polish.SKILL.md)*

### Additional WP-Safe Rules (2026-04-20)
1. NEVER use `<figure>` with nested `<figcaption>` inside `<a>` → wpautop breaks it
2. NEVER `<a href="..."><img ...><p>caption</p></a>` → block-in-anchor corruption
3. Use `data-` attributes instead of custom HTML attributes (WP strips unknown attrs)
4. Avoid `<template>` tags — stripped by some WP sanitizers
5. `<details>/<summary>` for CSS-only accordions: supported since WP 5.0+
6. Scoped `<style>` blocks: place ONCE at document top, never in the middle
7. Minify inline CSS in production to avoid WP editor wrapping issues
8. Test with Flatsome theme: check `.ux-container`, `.row`, `.col` class conflicts

### WP Rocket Safe Images
```html
<!-- CORRECT: explicit dimensions, no sizes=auto -->
<img src="image.jpg" alt="Description" width="800" height="600" loading="lazy">

<!-- WRONG: WP Rocket conflict -->
<img src="image.jpg" alt="Description" loading="lazy" sizes="auto">
```

---

## MODULE 9 — RTL / HEBREW LAYOUT ENGINE

### RTL Base Setup
```html
<!-- Wrap the entire article for RTL -->
<div class="dta-article dta-article--rtl" dir="rtl" lang="he">
  <!-- content -->
</div>
```

```css
.dta-article--rtl {
  direction: rtl;
  text-align: right;
  font-family: 'Noto Sans Hebrew', 'David Libre', Arial, sans-serif;
}

/* Flip flex directions */
.dta-article--rtl .dta-flex { flex-direction: row-reverse; }
.dta-article--rtl .dta-card-body { text-align: right; }

/* RTL-aware margins */
.dta-article--rtl .dta-section-title { border-right: 3px solid #7c3aed; border-left: none; padding-right: 0.75rem; padding-left: 0; }

/* RTL list bullets */
.dta-article--rtl ul { padding-right: 1.5rem; padding-left: 0; }
.dta-article--rtl ol { padding-right: 1.5rem; padding-left: 0; }

/* RTL TOC */
.dta-article--rtl .dta-toc { border-right: 3px solid #7c3aed; border-left: none; }
.dta-article--rtl .dta-toc-item::before { content: '← '; }

/* RTL floating buttons */
.dta-article--rtl .dta-float-contact { left: 1.5rem; right: auto; }
.dta-article--rtl .dta-float-scroll-top { right: auto; left: 5rem; }
```

### Hebrew Typography Rules
- Use `font-family: 'Noto Sans Hebrew', Arial, sans-serif`
- Line height: 1.8 (Hebrew needs more vertical space)
- Avoid italic for Hebrew (renders poorly)
- Numbers stay LTR within RTL text: `<span dir="ltr">$100</span>`
- Mixed Hebrew + English: use `unicode-bidi: embed` on English spans
- Dates: Israeli format dd/mm/yyyy

---

## MODULE 10 — TOC / FAQ INTERACTION SYSTEM

### CSS-Only TOC (collapsible)
```html
<details class="dta-toc" open>
  <summary class="dta-toc-header">
    <span class="dta-toc-icon">📋</span>
    <span>Table of Contents</span>
  </summary>
  <nav class="dta-toc-body">
    <ol class="dta-toc-list">
      <li><a href="#section-1">Introduction</a></li>
      <li><a href="#section-2">Main Section</a>
        <ol>
          <li><a href="#section-2-1">Sub-section</a></li>
        </ol>
      </li>
    </ol>
  </nav>
</details>
```

```css
.dta-toc {
  background:#111118; border:1px solid rgba(124,58,237,0.2);
  border-radius:12px; padding:1.25rem 1.5rem;
  margin-bottom:2rem;
}
.dta-toc-header {
  display:flex; align-items:center; gap:0.5rem;
  cursor:pointer; font-weight:600; font-size:1rem;
  list-style:none; /* remove default marker */
  color:#f0f0f5;
}
.dta-toc-header::-webkit-details-marker { display:none; }
.dta-toc-header::after { content:'▲'; margin-left:auto; font-size:0.75rem; color:#888; transition:transform 0.2s; }
details.dta-toc:not([open]) .dta-toc-header::after { content:'▼'; }
.dta-toc-list { margin:0.75rem 0 0; padding-left:1.25rem; }
.dta-toc-list li { margin-bottom:0.4rem; }
.dta-toc-list a { color:#a78bfa; text-decoration:none; font-size:0.9rem; }
.dta-toc-list a:hover { color:#c4b5fd; text-decoration:underline; }
```

### CSS-Only FAQ Accordion
```html
<div class="dta-faq">
  <details class="dta-faq-item">
    <summary class="dta-faq-question">Question text here?</summary>
    <div class="dta-faq-answer"><p>Answer text here.</p></div>
  </details>
</div>
```

```css
.dta-faq-item {
  border:1px solid rgba(255,255,255,0.08);
  border-radius:10px; overflow:hidden;
  margin-bottom:0.75rem;
  background:#111118;
}
.dta-faq-question {
  display:flex; align-items:center; justify-content:space-between;
  padding:1rem 1.25rem; cursor:pointer;
  font-weight:600; color:#f0f0f5;
  list-style:none;
}
.dta-faq-question::-webkit-details-marker { display:none; }
.dta-faq-question::after { content:'+'; font-size:1.25rem; color:#7c3aed; transition:transform 0.2s; flex-shrink:0; }
details.dta-faq-item[open] .dta-faq-question::after { transform:rotate(45deg); }
.dta-faq-answer { padding:0 1.25rem 1rem; color:#a0a0b5; line-height:1.7; }
```

---

## MODULE 11 — CONTENT SPACING OPTIMIZER

### Spacing Scale
```css
:root {
  --dta-space-1: 0.25rem; /* 4px */
  --dta-space-2: 0.5rem;  /* 8px */
  --dta-space-3: 0.75rem; /* 12px */
  --dta-space-4: 1rem;    /* 16px */
  --dta-space-5: 1.25rem; /* 20px */
  --dta-space-6: 1.5rem;  /* 24px */
  --dta-space-8: 2rem;    /* 32px */
  --dta-space-10: 2.5rem; /* 40px */
  --dta-space-12: 3rem;   /* 48px */
  --dta-space-16: 4rem;   /* 64px */
}
```

### Article Rhythm Rules
- `h2`: `margin-top: 3rem; margin-bottom: 1rem;`
- `h3`: `margin-top: 2rem; margin-bottom: 0.75rem;`
- `p`: `margin-bottom: 1rem; line-height: 1.75;`
- Between major sections: `margin-bottom: 3rem;`
- Callout blocks: `margin: 2rem 0;`
- Images: `margin: 2rem auto;`
- Code blocks: `margin: 1.5rem 0;`
- Pull quotes: `margin: 2.5rem 0;`

### Typography Scale
```css
.dta-article { font-size: 1.0625rem; /* 17px */ line-height: 1.75; color: #d0d0e0; }
.dta-article h1 { font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 800; color: #f0f0f5; }
.dta-article h2 { font-size: clamp(1.25rem, 3vw, 1.75rem); font-weight: 700; color: #f0f0f5; }
.dta-article h3 { font-size: clamp(1.1rem, 2vw, 1.35rem); font-weight: 600; color: #e0e0f0; }
.dta-article h4 { font-size: 1.1rem; font-weight: 600; color: #d0d0e0; }
```

---

## MODULE 12 — AUTHOR / TRUST SECTION BUILDER

```html
<div class="dta-author-box">
  <div class="dta-author-avatar">
    <img src="[AUTHOR_AVATAR_URL]" alt="[AUTHOR_NAME]" width="72" height="72" loading="lazy">
  </div>
  <div class="dta-author-info">
    <div class="dta-author-name">[AUTHOR_NAME]</div>
    <div class="dta-author-role">[ROLE] at [COMPANY]</div>
    <p class="dta-author-bio">[SHORT BIO 1-2 SENTENCES]</p>
    <div class="dta-author-links">
      <a href="[LINKEDIN_URL]" class="dta-author-link" rel="noopener">LinkedIn</a>
      <a href="[TWITTER_URL]" class="dta-author-link" rel="noopener">Twitter</a>
    </div>
  </div>
</div>
```

```css
.dta-author-box {
  display:flex; gap:1.25rem; align-items:flex-start;
  background:#111118; border:1px solid rgba(255,255,255,0.08);
  border-radius:12px; padding:1.5rem;
  margin-top:3rem;
}
.dta-author-avatar img { border-radius:50%; width:72px; height:72px; object-fit:cover; flex-shrink:0; }
.dta-author-name { font-weight:700; font-size:1rem; color:#f0f0f5; }
.dta-author-role { font-size:0.8rem; color:#7c3aed; margin-bottom:0.5rem; }
.dta-author-bio { font-size:0.875rem; color:#a0a0b5; line-height:1.6; margin:0 0 0.75rem; }
.dta-author-link {
  display:inline-flex; align-items:center; gap:0.25rem;
  font-size:0.8rem; color:#7c3aed; text-decoration:none;
  border:1px solid rgba(124,58,237,0.3); border-radius:4px;
  padding:0.2rem 0.5rem; margin-right:0.5rem;
  transition:all 0.15s;
}
.dta-author-link:hover { background:rgba(124,58,237,0.1); }
```

### Trust Rules
- ALWAYS use REAL author name and photo — no placeholders
- Include credentials/role
- 1-2 sentence bio max
- Publication date + "Updated:" date for SEO trust
- For dtapet.com: use brand logo + Hebrew bio

---

## MODULE 13 — FLOATING BUTTONS SYSTEM

```html
<div class="dta-floating-buttons">
  <!-- Contact button -->
  <a href="/contact/" class="dta-float-btn dta-float-contact" aria-label="Contact us">
    <span class="dta-float-icon">💬</span>
    <span class="dta-float-label">Contact</span>
  </a>
  <!-- Scroll to top -->
  <button class="dta-float-btn dta-float-scroll-top" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="Back to top">
    <span class="dta-float-icon">↑</span>
  </button>
</div>
```

```css
.dta-floating-buttons { position:fixed; bottom:1.5rem; right:1.5rem; z-index:100; display:flex; flex-direction:column; gap:0.75rem; align-items:flex-end; }
.dta-float-btn {
  display:inline-flex; align-items:center; gap:0.5rem;
  padding:0.625rem 1rem; border-radius:999px;
  font-size:0.875rem; font-weight:600; cursor:pointer;
  border:none; text-decoration:none;
  box-shadow:0 4px 16px rgba(0,0,0,0.3);
  transition:all 0.2s; white-space:nowrap;
}
.dta-float-contact { background:#7c3aed; color:#fff; }
.dta-float-contact:hover { background:#6d28d9; transform:translateY(-2px); box-shadow:0 6px 20px rgba(124,58,237,0.4); }
.dta-float-scroll-top { background:#1a1a2e; color:#f0f0f5; border:1px solid rgba(255,255,255,0.1); padding:0.625rem; }
.dta-float-scroll-top:hover { background:#252540; transform:translateY(-2px); }
@media(max-width:480px){
  .dta-float-label { display:none; }
  .dta-float-contact { padding:0.75rem; }
}
```

### Floating Button Rules
- Icon + text ALWAYS on ONE line (nowrap enforced)
- Contact button MUST link to `/contact/` (not scroll-to-section)
- Bottom-right is standard position
- RTL: flip to bottom-left
- Mobile: hide text label, show icon only

---

## MODULE 14 — CONVERSION CTA ENGINE
*(Integrated with cta-selection-engine.SKILL.md)*

### Hero CTA Block
```html
<section class="dta-cta-hero">
  <div class="dta-cta-hero-content">
    <h2 class="dta-cta-headline">[COMPELLING HEADLINE]</h2>
    <p class="dta-cta-subtext">[SUPPORTING TEXT — 1-2 sentences max]</p>
    <div class="dta-cta-actions">
      <a href="[PRIMARY_URL]" class="dta-btn dta-btn--primary dta-btn--xl">[PRIMARY CTA]</a>
      <a href="[SECONDARY_URL]" class="dta-btn dta-btn--ghost dta-btn--lg">[SECONDARY CTA]</a>
    </div>
  </div>
</section>
```

### End-of-Article CTA
```html
<div class="dta-cta-end">
  <div class="dta-cta-end-inner">
    <div class="dta-cta-end-icon">🚀</div>
    <h3 class="dta-cta-end-title">[TITLE]</h3>
    <p class="dta-cta-end-text">[SHORT PITCH]</p>
    <a href="[URL]" class="dta-btn dta-btn--primary dta-btn--lg">[CTA TEXT]</a>
  </div>
</div>
```

```css
.dta-cta-end {
  background:linear-gradient(135deg,rgba(124,58,237,0.15),rgba(76,29,149,0.1));
  border:1px solid rgba(124,58,237,0.3);
  border-radius:16px; padding:2.5rem;
  text-align:center; margin-top:3rem;
}
.dta-cta-end-icon { font-size:2.5rem; margin-bottom:1rem; }
.dta-cta-end-title { font-size:1.5rem; font-weight:700; color:#f0f0f5; margin-bottom:0.75rem; }
.dta-cta-end-text { color:#a0a0b5; margin-bottom:1.5rem; max-width:480px; margin-left:auto; margin-right:auto; }
```

---

## MODULE 15 — PREVIEW & RENDERING VALIDATOR

### Pre-Delivery Checklist (MANDATORY)
```
HTML STRUCTURE:
[ ] No <a> contains block-level children
[ ] All class names prefixed (dta-, art-, etc.)
[ ] Single <style> block at TOP
[ ] No inline style= on structural elements
[ ] No onmouseover/onmouseout handlers
[ ] No <script> tags in article content

IMAGES:
[ ] All <img> have width + height attributes
[ ] All <img> have loading="lazy"
[ ] All <img> have descriptive alt text
[ ] No sizes="auto" attribute
[ ] Images use object-fit:cover or contain

RESPONSIVE:
[ ] Grid has 768px breakpoint
[ ] Grid has 480px breakpoint
[ ] Floating buttons work on mobile
[ ] Tables are scroll-wrapped on mobile
[ ] Font sizes use clamp() or responsive values

WORDPRESS:
[ ] Mentally simulate wpautop: no </p> injections
[ ] Cards use div+overlay-a pattern
[ ] Flatsome class conflicts checked
[ ] WP Rocket: no sizes=auto

ACCESSIBILITY:
[ ] Color contrast ≥4.5:1 for body text
[ ] Color contrast ≥3:1 for large text / UI
[ ] All interactive elements have :focus-visible
[ ] All images have alt text
[ ] Buttons have aria-label if icon-only
[ ] Modals have role="dialog" + aria-modal
[ ] TOC/FAQ use native <details>/<summary> = free a11y

CONTENT:
[ ] No placeholder/fake content
[ ] No invented brand names or logos
[ ] Author section has real info
[ ] CTA present at end of article
[ ] TOC anchors match actual heading IDs
```

### wpautop Simulation Rules
PHP inserts `</p>` before any block-level HTML that appears after text.
Block elements that trigger wpautop issues:
- `<div>`, `<h1-h6>`, `<ul>`, `<ol>`, `<table>`, `<figure>`, `<blockquote>`, `<pre>`
- NEVER wrap these in `<a>` tags
- ALWAYS close `<p>` before starting block HTML

---

## MODULE 16 — HTML + N8N SYNC ENGINE

### Template Variable System
Use double-bracket vars that N8N replaces:
```html
<!-- N8N Template Variables -->
{{ARTICLE_TITLE}}    → Article headline
{{HERO_IMAGE_URL}}   → Main image URL
{{AUTHOR_NAME}}      → Author display name
{{AUTHOR_AVATAR}}    → Author photo URL
{{PUBLISH_DATE}}     → ISO date string
{{ARTICLE_CONTENT}}  → Main body HTML
{{META_DESCRIPTION}} → SEO description
{{CANONICAL_URL}}    → Canonical URL
{{CATEGORY}}         → Post category
{{TAGS}}             → Comma-separated tags
```

### N8N HTML Node Pattern
```javascript
// In N8N Function node:
const template = $node["HTML Template"].json["template"];
const filled = template
  .replace(/{{ARTICLE_TITLE}}/g, $json.title)
  .replace(/{{HERO_IMAGE_URL}}/g, $json.hero_image)
  .replace(/{{AUTHOR_NAME}}/g, $json.author_name)
  .replace(/{{ARTICLE_CONTENT}}/g, $json.content)
  .replace(/{{PUBLISH_DATE}}/g, new Date().toISOString());
return [{ json: { html: filled } }];
```

### Sync Protocol
1. HTML template stored in N8N as static asset or node
2. Variables injected via N8N Function node
3. Output sent to WordPress REST API: `POST /wp-json/wp/v2/posts`
4. Images pre-uploaded to WP Media: `POST /wp-json/wp/v2/media`
5. Test render locally before N8N deploy

---

## MODULE 17 — ACCESSIBILITY & CONTRAST FIXER

### WCAG AA Minimum Requirements
- Body text (< 18px): contrast ratio ≥ **4.5:1**
- Large text (≥ 18px / 14px bold): contrast ratio ≥ **3:1**
- UI components (borders, icons): contrast ratio ≥ **3:1**
- Focus indicators: ≥ **3:1** against adjacent colors

### Approved Color Pairings (dark theme, WCAG AA+)
```css
/* Text on dark backgrounds */
#f0f0f5 on #0a0a0f  → ratio 17.4:1  ✓ AAA
#d0d0e0 on #111118  → ratio 11.2:1  ✓ AAA
#a0a0b5 on #111118  → ratio  6.8:1  ✓ AA
#888 on #1a1a2e     → ratio  4.6:1  ✓ AA (borderline — prefer #999+)

/* Accent color checks */
#7c3aed on #fff     → ratio  5.2:1  ✓ AA
#fff on #7c3aed     → ratio  5.2:1  ✓ AA
#a78bfa on #0a0a0f  → ratio  9.4:1  ✓ AAA

/* Danger/success */
#22c55e on #111118  → ratio  7.2:1  ✓ AAA
#ef4444 on #111118  → ratio  4.8:1  ✓ AA
#eab308 on #111118  → ratio  9.1:1  ✓ AAA
```

### ARIA Patterns
```html
<!-- Dialog/Modal -->
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">Title</h2>
</div>

<!-- Navigation -->
<nav aria-label="Table of contents">...</nav>

<!-- Live region for dynamic content -->
<div role="status" aria-live="polite" aria-atomic="true"></div>

<!-- Progress -->
<progress aria-label="Loading" value="60" max="100"></progress>

<!-- Icon-only button -->
<button aria-label="Close dialog">✕</button>

<!-- Skip link (accessibility must-have) -->
<a href="#main-content" class="dta-skip-link">Skip to main content</a>
```

```css
/* Skip link (visible on focus only) */
.dta-skip-link {
  position:absolute; top:-100%; left:1rem;
  background:#7c3aed; color:#fff;
  padding:0.5rem 1rem; border-radius:0 0 8px 8px;
  font-weight:600; text-decoration:none; z-index:9999;
}
.dta-skip-link:focus { top:0; }

/* Focus visible for all interactive elements */
*:focus-visible {
  outline: 2px solid #7c3aed;
  outline-offset: 2px;
}
```

### Dark Mode Testing Protocol (from awesome-cursor-skills)
1. Check text/background contrast in both modes
2. Verify focus rings visible in both modes
3. Check images: ensure no pure white on white-bg in dark mode
4. Verify icon SVGs have both light + dark paths or use currentColor
5. Check hover states: visible in both modes

---

## BONUS MODULE B1 — BRAND DESIGN SYSTEM EXTRACTOR
*(inspired by hue + SkillUI)*

### Extraction Workflow
Given a brand URL or screenshot:

1. **Color Extraction**
   - Primary brand color (buttons, links, accents)
   - Background color(s) (base, surface, elevated)
   - Text colors (body, heading, muted)
   - State colors (success, error, warning, info)

2. **Typography Extraction**
   - Heading font family + weights
   - Body font family + size + line-height
   - Code font (if applicable)

3. **Spacing System**
   - Base spacing unit (4px, 8px, or custom)
   - Border radii (sharp=0, soft=4-8px, round=16px+)

4. **Component Patterns**
   - Button styles (filled vs ghost, rounded vs square)
   - Card patterns (border vs shadow vs flat)
   - Input styles (underline vs bordered vs filled)

5. **Design Tokens Output**
```css
:root {
  /* Extracted from [BRAND_URL] */
  --brand-primary: [HEX];
  --brand-bg: [HEX];
  --brand-surface: [HEX];
  --brand-text: [HEX];
  --brand-text-muted: [HEX];
  --brand-radius-sm: [px];
  --brand-radius-md: [px];
  --brand-radius-lg: [px];
  --brand-font-heading: '[FONT]', sans-serif;
  --brand-font-body: '[FONT]', sans-serif;
  --brand-shadow: [VALUE];
}
```

---

## BONUS MODULE B2 — ANIMATION & TRANSITION SYSTEM
*(inspired by html-ppt-skill + material-3-skill)*

### Core Transition Library
```css
/* Durations */
:root {
  --dta-dur-fast: 100ms;
  --dta-dur-base: 150ms;
  --dta-dur-slow: 250ms;
  --dta-dur-slower: 400ms;
  --dta-ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --dta-ease-in: cubic-bezier(0.4, 0, 1, 1);
  --dta-ease-out: cubic-bezier(0, 0, 0.2, 1);
  --dta-ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* slight overshoot */
}

/* Hover lift */
.dta-hover-lift { transition: transform var(--dta-dur-base) var(--dta-ease-out), box-shadow var(--dta-dur-base) var(--dta-ease-out); }
.dta-hover-lift:hover { transform: translateY(-2px); }

/* Hover glow */
.dta-hover-glow:hover { box-shadow: 0 0 20px rgba(124,58,237,0.35); }

/* Fade in on load */
@keyframes dta-fade-in {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.dta-fade-in { animation: dta-fade-in var(--dta-dur-slower) var(--dta-ease-out) both; }

/* Staggered children */
.dta-stagger > *:nth-child(1) { animation-delay: 0ms; }
.dta-stagger > *:nth-child(2) { animation-delay: 50ms; }
.dta-stagger > *:nth-child(3) { animation-delay: 100ms; }
.dta-stagger > *:nth-child(4) { animation-delay: 150ms; }
.dta-stagger > *:nth-child(5) { animation-delay: 200ms; }

/* Pulse (loading states) */
@keyframes dta-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
.dta-pulse { animation: dta-pulse 2s var(--dta-ease-standard) infinite; }

/* Shimmer skeleton */
@keyframes dta-shimmer {
  from { background-position: -200% 0; }
  to   { background-position: 200% 0; }
}
.dta-skeleton {
  background: linear-gradient(90deg, #1a1a2e 25%, #252540 50%, #1a1a2e 75%);
  background-size: 200% 100%;
  animation: dta-shimmer 1.5s infinite;
  border-radius: 4px;
}
```

### Animation Rules
- NEVER use `bounce` easing on UI elements — looks cheap
- Transitions: 100-250ms for UI, 300-500ms for page elements
- Use `will-change: transform` only on actively animating elements
- Respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

---

## BONUS MODULE B3 — EMAIL HTML ENGINE
*(from irinabuht12-oss/email-campaigns-claude)*

### Email HTML Rules (critical differences from web HTML)
1. Use TABLE layout for email (not CSS grid/flex — client support)
2. Max width: 600px, centered
3. Inline styles ONLY (no `<style>` blocks — Gmail strips them)
4. Images: absolute URLs, explicit width/height, alt text ALWAYS
5. Background colors: set on TD elements, not parent
6. No web fonts — use Arial, Georgia, system stacks only
7. All links: absolute URLs including protocol
8. Test in Litmus or Email on Acid before sending

### Email Design Tokens
```
Card corner radius: 3px (not 12px — email clients)
Card shadow: 0 2px 8px rgba(24,24,27,.06)
Typography: 26px heading / 15px body / 13px caption
Max card width: 560px
Primary CTA: black pill button, repeat 2x in email
Background: soft gradient + 6% noise texture
Spacing: 24px section gaps, 16px inner padding
```

### Email CTA Button (table-based)
```html
<table width="100%" cellspacing="0" cellpadding="0">
  <tr>
    <td align="center" style="padding:24px 0;">
      <table cellspacing="0" cellpadding="0">
        <tr>
          <td style="background:#000;border-radius:999px;">
            <a href="[URL]" style="display:inline-block;padding:14px 32px;color:#fff;font-family:Arial,sans-serif;font-size:15px;font-weight:700;text-decoration:none;">Get Started →</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

---

## BONUS MODULE B4 — AEO CONTENT OPTIMIZER
*(from addyosmani/agentic-seo)*

### AEO — Agentic Engine Optimization Checklist
Ensure content is discoverable and parseable by AI agents:

**Discovery (25pts)**
- [ ] robots.txt: AI crawlers NOT blocked
- [ ] llms.txt: structured index with descriptions + token counts
- [ ] AGENTS.md / CLAUDE.md: project context file present

**Content Structure (25pts)**
- [ ] Proper heading hierarchy (h1→h2→h3, no skips)
- [ ] Semantic HTML (`<article>`, `<section>`, `<nav>`, `<aside>`)
- [ ] Code examples in `<pre><code>` with language class
- [ ] Data in `<table>` not just visual layouts
- [ ] Markdown available at `/content.md` or API endpoint

**Token Economics (25pts)**
- [ ] Per-page: < 8000 tokens for blog posts
- [ ] No bloated boilerplate that wastes context window
- [ ] AI-friendly meta tags: `<meta name="description">`
- [ ] Structured data: JSON-LD schema markup

**Capability Signaling (15pts)**
- [ ] SKILL.md or capability description
- [ ] Clear input/output documentation
- [ ] Rate limit and access rules documented

**Direct Answer Optimization**
- Lead with the direct answer before explanation
- Use specific numbers, dates, named entities
- Avoid hedging phrases ("it depends", "there are many factors")
- Structure FAQ as actual Q&A pairs with direct answers
- Include a TL;DR or summary box at the top

---

## GOLD STANDARD CHECKLIST (COMBINED — All Modules)
*(Inherited + Extended)*

```
CORE STRUCTURE:
[ ] Single article wrapper with scoped class prefix
[ ] Single <style> block at top
[ ] No inline style= on structural elements
[ ] No onmouseover/onclick inline handlers
[ ] No <script> in article body
[ ] All class names prefixed

WORDPRESS SAFETY:
[ ] No <a> with block-level children
[ ] Cards: div + overlay-a pattern
[ ] No sizes=auto on images
[ ] Flatsome class conflicts checked

IMAGES:
[ ] width + height + loading=lazy + alt on ALL images
[ ] object-fit:cover where appropriate
[ ] Absolute URLs in email HTML

RESPONSIVE:
[ ] 768px breakpoint present
[ ] 480px breakpoint present
[ ] Touch targets ≥44px
[ ] Floating buttons work on mobile

ACCESSIBILITY:
[ ] WCAG AA contrast: 4.5:1 body, 3:1 large/UI
[ ] :focus-visible on all interactive elements
[ ] Icon-only buttons have aria-label
[ ] Skip link present (if standalone page)
[ ] prefers-reduced-motion respected

CONTENT QUALITY:
[ ] No fake/placeholder content
[ ] Real author info
[ ] End-of-article CTA
[ ] TOC with working anchors
[ ] FAQ section (if article-format)
[ ] Author box

PERFORMANCE:
[ ] Animations use CSS not JS
[ ] will-change used sparingly
[ ] No render-blocking resources
[ ] Images lazy-loaded
```

---

## SOURCE KNOWLEDGE
Built from:
- Original: dtapet.com WordPress analysis + ROOT_CAUSE_REPORT.md
- Upgrade sources (2026-04-20): 35 GitHub repos analyzed
- Key new sources: awesome-cursor-skills, hue/SkillUI (design extraction), html-ppt-skill (animation), email-campaigns-claude (email patterns), agentic-seo (AEO), material-3-skill (MD3 patterns), irinabuht12-oss (email tokens)
- Fixed templates: `/a0/usr/workdir/fixed_html_template.html`, `/a0/usr/workdir/fixed_article.html`
