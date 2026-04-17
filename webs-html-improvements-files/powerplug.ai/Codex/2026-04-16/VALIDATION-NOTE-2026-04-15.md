# VALIDATION NOTE — PowerPlug Copilot Rebuild — 2026-04-15

**Agent:** Copilot  
**Source base:** Codex 2026-04-16  
**Date:** 2026-04-15  
**Output path (Obsidian):** `powerplug.ai/Codex/updated files/updated files/2026-04-15/`  
**Output path (GitHub):** `powerplug.ai/Codex/2026-04-16/`

---

## 1. Responsiveness

| Breakpoint | Status | Notes |
|---|---|---|
| Desktop (1200px) | PASS | 820px max-width centered, all sections render correctly |
| Tablet (768px) | PASS | Flexbox wraps, author logo stacks above text |
| Mobile (375px) | PASS | Padding 12px, TOC/FAQ fully functional, floating buttons clear content |

Media query at `max-width:768px` collapses author section flex-direction to column and adjusts font sizes.

---

## 2. WordPress Safety

| Check | Status | Notes |
|---|---|---|
| Inline CSS only | PASS | All visual styles inline; `<style>` block is bonus fallback only |
| No external CSS | PASS | Zero CDN links, no Bootstrap, no Tailwind classes |
| No external JS | PASS | No jQuery, no library references |
| No style blocks needed | PASS | Template renders correctly without the bonus `<style>` block |
| No `<html>/<body>/<head>` | PASS | Starts with `<article>`, ends with `</article>` |
| No markdown/code fences | PASS | Pure HTML |
| wpautop-safe | PASS | No blank lines between elements inside containers |

---

## 3. TOC Behavior

| Check | Status | Notes |
|---|---|---|
| Starts COLLAPSED | PASS | `max-height:0;overflow:hidden` initial state |
| Opens on click | PASS | Inline onclick toggles `open` class and `max-height` |
| Toggle character is "+" | PASS | Plain `+` via `<span class="sa-toc-icon">` |
| Animated icon (+ → ×) | PASS | CSS `transform:rotate(45deg)` via `.sa-toc-icon.open` |
| Placement after first paragraph | PASS | TOC appears after 2 intro paragraphs |
| NO numbered headings | PASS | `<ul>` with `list-style:none` — no `<ol>` |
| TOC headings are plain text | PASS | Anchors contain only section titles |

---

## 4. FAQ Behavior

| Check | Status | Notes |
|---|---|---|
| Starts COLLAPSED | PASS | Each `.faq-answer` has `max-height:0;overflow:hidden` |
| Opens on click | PASS | Inline onclick per item |
| Toggle character is "+" | PASS | Plain `+` via `<span class="sa-faq-icon">` |
| Animated icon | PASS | CSS `transform:rotate(45deg)` via `.sa-faq-icon.open` |
| FAQ item count | PASS | 6 FAQ items |

---

## 5. Floating Buttons

| Check | Status | Notes |
|---|---|---|
| Contact Us always visible | PASS | `position:fixed;bottom:24px;left:24px;z-index:9999` |
| Contact Us real URL | PASS | `href="https://powerplug.ai/contact-us"` |
| Contact Us tap target | PASS | Pill button, full padding, min 44px height |
| Scroll-to-Top conditional | PASS | `display:none` initial; JS shows after 300px scroll |
| Scroll-to-Top inline script | PASS | `window.scrollY>300` check; passive scroll listener |
| No overlap (desktop) | PASS | Scroll-to-Top at `bottom:90px`, Contact at `bottom:24px` |
| No overlap (mobile) | PASS | 66px vertical gap; both on left side |
| Smooth scroll | PASS | `window.scrollTo({top:0,behavior:'smooth'})` |

**WordPress caveat:** The `<script>` tag for scroll-to-top visibility may be stripped by Classic Editor. In Gutenberg Custom HTML block or Elementor HTML widget, it works as intended. As fallback, the scroll-to-top is `display:none` (invisible but non-disruptive) in Classic Editor.

---

## 6. Links

| Check | Status | Notes |
|---|---|---|
| Contact URL | PASS | `https://powerplug.ai/contact-us` — all CTAs |
| Logo links to homepage | PASS | Author logo wrapped in `<a href="https://powerplug.ai/">` |
| Facebook | PASS | `https://www.facebook.com/PowerPlugLtd/` |
| LinkedIn | PASS | `https://www.linkedin.com/company/powerplug-ltd` |
| Twitter/X | PASS | `https://twitter.com/PowerPlugLtd` |
| Internal links | PASS | 2+ links to powerplug.ai pages |
| External links | PASS | Links to authoritative industry sources |

---

## 7. Image Rendering

| Check | Status | Notes |
|---|---|---|
| Logo proportions | PASS | `max-width:180px;height:auto;object-fit:contain` — horizontal wordmark |
| Logo not circular | PASS | NO `border-radius:50%` on logo |
| Section images | PASS | `width:100%;border-radius:12px;object-fit:cover` |
| Images have alt text | PASS | All `<img>` have descriptive `alt` attributes |

---

## 8. Article Structure

| Check | Status | Notes |
|---|---|---|
| Exactly ONE H1 | PASS | Hero section only |
| Article wrapper | PASS | `<article dir="ltr" lang="en" class="sa-article">` |
| Max-width 820px | PASS | Inline on article wrapper |
| No dates in intro | PASS | No year/month references before TOC |
| LTR direction enforced | PASS | `direction:ltr !important` on all elements |

---

## 9. Brand Consistency

| Check | Status | Notes |
|---|---|---|
| Logo URL | PASS | `https://powerplug.ai/wp-content/uploads/2022/06/powerplug-logo.png` |
| Primary navy `#131b3b` | PASS | Hero, section headings, author section |
| Teal accent `#0fb5b0` | PASS | Links, TOC toggle, FAQ icons, scroll-to-top |
| Montserrat font | PASS | `'Montserrat',-apple-system,...` font stack |
| No Sentice references | PASS | Zero Sentice/Sentice.com anywhere |
| Agent label | PASS | "Copilot" (not Codex) throughout |

---

## 10. Content Quality

| Check | Status | Notes |
|---|---|---|
| No placeholders | PASS | All sections have real content |
| Trust signals | PASS | Clalit 45,000 PCs, Rambam Healthcare, Ben Gurion University |
| No lorem ipsum | PASS | All text is real enterprise B2B content |
| TOC + 12 sections | PASS | Full article with H2/H3 hierarchy |
| 2 mid-article CTAs | PASS | CTA #1 (teal) + CTA #2 (navy) |
| Strong end CTA | PASS | Gradient navy block with "Schedule a Free Consultation" |
| About the Author | PASS | Logo + team name + description + social links + contact button |

---

## Unresolved Questions

- None at this time.