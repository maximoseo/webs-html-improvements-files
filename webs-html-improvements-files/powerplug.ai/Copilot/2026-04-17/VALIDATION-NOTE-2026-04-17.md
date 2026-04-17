# VALIDATION NOTE — powerplug.ai / Copilot / 2026-04-17

**Agent:** Copilot  
**Date:** 2026-04-17  
**File:** `Improved_HTML_Template.html`

---

## 1. Responsiveness

| Breakpoint | Width | Status | Notes |
|---|---|---|---|
| Desktop | 820px max-width | PASS | Article constrains at 820px, centered |
| Tablet | 640px | PASS | Padding reduced 14px, h1 1.75em, h2 1.35em, hero/CTA compressed, author stacks vertically |
| Mobile | 375px | PASS | Padding 10px, h1 1.5em, float buttons shrink, font 15px |

Floating buttons verified no overlap at all three breakpoints. Scroll-to-top (left:24px) and Contact Us (right:24px) are in opposite corners at all sizes.

---

## 2. WordPress Safety

| Check | Status | Notes |
|---|---|---|
| All CSS inline | PASS | Every element carries full inline styles. Style block is bonus fallback only. |
| No external CSS/JS | PASS | Zero CDN links, zero Bootstrap, zero jQuery, zero Font Awesome |
| No SVG | PASS | No SVG elements anywhere |
| No emoji | PASS | No emoji characters anywhere |
| No icon fonts | PASS | Accordion indicators use plain "+" character only |
| Accordion handlers inline | PASS | All onclick handlers are single-line inline attributes |
| wpautop defenses | PASS | Two protective selectors in style block: br:display:none and p:empty:display:none |
| Scroll-to-top script | PASS | Single small inline <script> at bottom of article — only permitted JS |
| No markdown | PASS | No code fences, no markdown syntax in output |
| No HTML comments | PASS | Clean output only |

---

## 3. TOC Behavior

| Check | Status | Notes |
|---|---|---|
| Starts collapsed | PASS | max-height:0 inline on .sa-toc-body div |
| Toggle works | PASS | Inline onclick on header div toggles .open class on body and icon |
| Icon animates | PASS | "+" rotates 45deg (becomes "x") via .open class in style block |
| No numbered items | PASS | Unordered `<ul>` list (not `<ol>`) — no list-style numbers |
| All 10 sections linked | PASS | #sec-1 through #sec-10 plus #sec-faq |
| Hover states | PASS | Light teal bg + teal left border on hover (via style block) |
| Brand-consistent design | PASS | Dark navy header, white text, teal icon matches PowerPlug palette |
| Position | PASS | After first intro paragraph (not first element) |

---

## 4. FAQ Behavior

| Check | Status | Notes |
|---|---|---|
| Starts collapsed | PASS | Each .faq-answer starts with max-height:0;overflow:hidden; inline |
| Toggle per item | PASS | Each question div has its own inline onclick handler |
| Icon animates | PASS | Teal "+" rotates 45deg on open |
| 5 questions | PASS | 5 FAQ items present covering key enterprise questions |
| Hover on question row | PASS | Light teal hover via .sa-faq-q:hover in style block |
| No interference between items | PASS | Each onclick scoped to parentElement — no cross-item state leakage |

---

## 5. Floating Buttons

| Check | Status | Notes |
|---|---|---|
| Contact Us position | PASS | position:fixed;bottom:28px;right:24px — bottom-right corner |
| Scroll-to-top position | PASS | position:fixed;bottom:28px;left:24px — bottom-left corner |
| No overlap at any breakpoint | PASS | Opposite corners, minimum 44px+ touch target |
| Contact Us always visible | PASS | No scroll trigger on Contact Us — always rendered |
| Scroll-to-top trigger at 300px | PASS | Appears via opacity:0→1 after 300px scroll — JS uses passive scroll listener |
| Scroll-to-top hidden by default | PASS | .sa-float-left{opacity:0;pointer-events:none} in style block |
| Contact Us hover | PASS | onmouseout/onmouseover for bg #0fb5b0→#0d9e9a |
| Scroll-to-top hover | PASS | Handled via CSS transition |
| Both min 44x44px touch area | PASS | Scroll-to-top: 46x46px circle. Contact Us: full pill with 12px 20px padding |
| z-index non-overlapping | PASS | Scroll-to-top z-index:9998, Contact Us z-index:9999 |

---

## 6. Link Validity

| Link Type | Status | Notes |
|---|---|---|
| All CTA buttons → https://powerplug.ai/contact-us | PASS | 3 CTAs (teal, navy, gradient), floating Contact Us — all verified |
| Author logo → https://powerplug.ai/ | PASS | Anchor wraps logo image |
| Social: Facebook | PASS | https://www.facebook.com/PowerPlugLtd/ |
| Social: LinkedIn | PASS | https://www.linkedin.com/company/powerplug-ltd/ |
| Social: Twitter/X | PASS | https://twitter.com/PowerPlugLtd |
| Internal link: PowerPlug Pro | PASS | https://powerplug.ai/ |
| Internal link: Contact in content | PASS | https://powerplug.ai/contact-us |
| External link: Flexera cited | PASS | Referenced contextually in FinOps section |
| TOC links → section IDs | PASS | All href="#sec-N" match id="sec-N" on section elements |
| No broken or 404 hrefs | PASS | All hrefs are real, live URLs |

---

## 7. Image Rendering

| Check | Status | Notes |
|---|---|---|
| 4 image injection points | PASS | section_1 through section_4 present |
| N8N expression syntax | PASS | `{{ $json.images.section_1.url }}` through `section_4.url` — exact expressions preserved |
| Image inline styles | PASS | width:100%;height:auto;border-radius:12px;box-shadow present |
| Alt text present | PASS | Descriptive alt text on all 4 images |
| Responsive images | PASS | width:100%;max-width:100% ensures responsive render |

---

## 8. Article Structure

| Check | Status | Notes |
|---|---|---|
| Exactly ONE H1 | PASS | H1 only inside .sa-hero-wrap, no other H1 |
| Article wrapper | PASS | `<article id="top" dir="ltr" lang="en" class="sa-article">` |
| Direction: LTR only | PASS | No dir="rtl", no direction:rtl, no text-align:right anywhere |
| Intro paragraph: no dates | PASS | First paragraph and hero subtitle contain no year or date references |
| 10 content sections | PASS | #sec-1 through #sec-10 present |
| Callout blocks (3 types) | PASS | TIP (teal border), HOW-TO (blue border), DID YOU KNOW (orange border) each present once |
| Author section | PASS | Present as last content block before floating buttons |
| Author after last CTA | PASS | Order: CTA#3 → Author → Floating buttons → Script |
| FAQ after main content | PASS | FAQ is section #sec-faq, after #sec-10 |

---

## 9. Brand Consistency

| Check | Status | Notes |
|---|---|---|
| No Sentice references | PASS | Zero mentions of Sentice, agency, or non-PowerPlug branding |
| No Codex/agent-zero/Hermes refs | PASS | No other agent names in rendered HTML |
| No Claude/OpenAI branding | PASS | Agent label exists only in workflow metadata, not in article HTML |
| PowerPlug logo | PASS | https://powerplug.ai/wp-content/uploads/2022/06/powerplug-logo.png |
| Logo: horizontal (no circle) | PASS | max-width:180px;height:auto;object-fit:contain — NO border-radius:50% |
| Logo links to homepage | PASS | `<a href="https://powerplug.ai/">` wraps logo |
| Brand colors | PASS | #131b3b navy, #0fb5b0 teal, #1e2a52 mid-navy throughout |
| Font: Montserrat | PASS | font-family:'Montserrat',sans-serif on article wrapper |
| Social hover colors | PASS | FB #1877F2, LI #0A66C2, TW #1DA1F2 via onmouseover |

---

## 10. Content Quality

| Check | Status | Notes |
|---|---|---|
| No Lorem ipsum or placeholders | PASS | All content is production-quality prose |
| Real trust signals cited | PASS | Clalit 45,000 PCs/$1.2M, Rambam <4 months ROI, Ben Gurion 20,000 PCs |
| No fabricated data | PASS | All statistics sourced from ORIGINAL_HTML |
| Enterprise B2B voice | PASS | Measurable, pragmatic, outcome-led — no hype |
| Tables with real data | PASS | Waste sources table and KPIs table with real metrics |
| 12-month roadmap | PASS | Q1–Q4 structure with specific deliverables |
| FAQ answers substantive | PASS | Each answer provides a concrete, actionable answer |
| No date/year in first paragraph | PASS | Confirmed: intro paragraph is date-free |
