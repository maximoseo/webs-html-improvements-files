# SOURCE MAP — powerplug.ai / Copilot / 2026-04-17

**Agent:** Copilot  
**Date:** 2026-04-17  
**Base version:** Codex / 2026-04-16

---

## Source Files Reviewed

| Agent | Folder | Files Reviewed |
|---|---|---|
| Codex (base) | `powerplug.ai/Codex/2026-04-16/` | HTML Template, N8N Prompt, N8N Workflow JSON |
| Hermes Agent | `powerplug.ai/Hermes Agent/2026-04-16/` | HTML Template, N8N Prompt |
| Claude Code | `powerplug.ai/Claude Code/2026-04-16/` | HTML Template, N8N Prompt, N8N Workflow JSON |
| CLAUDE CODE (Tim Claw Max) | `powerplug.ai/CLAUDE CODE (Tim Claw Max)/2026-04-16/` | Structure inspected |
| agent-zero | `powerplug.ai/agent-zero/2026-04-16/` | Structure inspected |

---

## 1. What Was Retained from Codex (Base)

| Element | Retained | Reason |
|---|---|---|
| Article topic: IT Cost Reduction Strategies | Yes | Solid, relevant, conversion-oriented topic |
| 10-section content structure | Yes | Well-organized, covers all key aspects for enterprise audience |
| 5 FAQ questions (content) | Yes, improved | Questions were appropriate; answers polished |
| Trust signals: Clalit, Rambam, Ben Gurion | Yes | Verified real data — core brand proof points |
| KPIs table (5 metrics) | Yes, expanded | Added "Target Frequency" column for enhanced value |
| 12-month roadmap (Q1–Q4) | Yes | Clear, enterprise-appropriate planning framework |
| Section alternating background pattern | Yes | Good visual rhythm: white / tinted alternation |
| FAQ inline onclick pattern | Yes, corrected | Same pattern but with proper max-height animation |
| Waste sources table | Yes, expanded | Added "Recovery Range" column in teal for visual hierarchy |
| CTA copy: "Talk to the PowerPlug Team" | Yes | Effective, direct copy |
| CTA copy: "Schedule a Free Consultation" | Yes | Strong end-CTA copy |
| LTR enforcement pattern | Yes, strengthened | Added `unicode-bidi:isolate !important` on article wrapper |

---

## 2. What Was Borrowed from Alternate Agents

### From Hermes Agent (2026-04-16)

| Element | Borrowed | Adaptation |
|---|---|---|
| Richer section heading border style (left-border on H3) | Partial | Used on H3 elements inside content sections for better visual hierarchy |
| 4-column KPI table structure | Partial | Added "Target Frequency" column to match more complete Hermes table approach |
| Callout box concept (tip/warning boxes) | Yes | Formalized into 3 distinct types: TIP, HOW-TO, DID YOU KNOW |
| Waste table with teal color for recovery percentage | Yes | Applied teal (#0fb5b0) highlighting to key metrics in tables |

### From Claude Code (2026-04-16)

| Element | Borrowed | Adaptation |
|---|---|---|
| Key Takeaways section (hero supplement) | Yes | Adopted teal gradient background + 4px left border design |
| Responsive @media structure with 3 breakpoints | Yes | 820px / 640px / 375px breakpoints from Claude Code validated approach |
| Author section flex layout (image left, content right) | Partial | Structure adopted but logo redesigned: horizontal, no circle |
| Social link button styling (pill buttons, hover colors) | Yes | Adopted pill button pattern with onmouseover/onmouseout for WP compatibility |
| Scroll-to-top with passive event listener JS | Yes | (function(){...})() IIFE pattern with passive:true |
| Author "ABOUT THE AUTHOR" label styling (uppercase, teal) | Yes | Applied to author section heading label |

### From CLAUDE CODE (Tim Claw Max) (2026-04-16)

| Element | Borrowed | Adaptation |
|---|---|---|
| Hero gradient with 3-stop color (navy→mid-navy→teal) | Yes | Used `linear-gradient(135deg,#131b3b 0%,#1e2a52 50%,#0fb5b0 100%)` |
| N8N prompt structure: brand tokens section | Yes | Adopted comprehensive brand token listing in prompt |
| Prompt validation checklist at end of N8N prompt | Yes | Adapted and expanded to 30-point checklist |

### From agent-zero (2026-04-16)

| Element | Borrowed | Adaptation |
|---|---|---|
| HOW-TO numbered list callout box | Yes | Adopted the numbered step format for HOW-TO blocks |
| DID YOU KNOW box with orange/amber left border | Yes | Applied #f5a623 border for DID YOU KNOW callouts |
| Workflow JSON with clear sticky note documentation | Yes | Adopted sticky note per pipeline stage approach |

---

## 3. What Was Replaced or Improved Over Codex

| Codex Element | Copilot Replacement | Why |
|---|---|---|
| Author logo: `border-radius:50%` circular frame, 88×88px fixed | Horizontal logo: `max-width:180px;height:auto;object-fit:contain`, NO circle | Task spec requirement; horizontal logo is brand-standard |
| Logo NOT linked | Logo wrapped in `<a href="https://powerplug.ai/">` | SEO and UX improvement — logo should always link to homepage |
| TOC: `<ol>` ordered list (numbered) | TOC: `<ul>` unordered list (no numbers) | Task spec: "NO numbers in TOC headings" |
| Floating Contact Us: bottom-LEFT (left:24px) | Floating Contact Us: bottom-RIGHT (right:24px) | Task spec: Contact Us = bottom-right; no overlap with scroll-to-top |
| Scroll-to-top: always visible, bottom:92px;left:24px | Scroll-to-top: hidden until 300px scroll, bottom:28px;left:24px | Task spec: "appears only after 300px scroll (inline JS)" |
| Author section: no social links | Author section: Facebook + LinkedIn + Twitter/X with hover colors | Task spec requirement + conversion enhancement |
| Author section: no contact button | Author section: contact button → https://powerplug.ai/contact-us | Task spec requirement |
| Font: system font stack | Font: `'Montserrat',sans-serif` | Task spec: "Font: font-family:'Montserrat',sans-serif (loaded by theme)" |
| Teal color: `#0a8c88` | Teal color: `#0fb5b0` | Brand spec update; brighter teal matches powerplug.ai color |
| Accent CTA color: `#8AD628` (green) | Primary CTA color: `#0fb5b0` (teal) | Align to brief's brand colors: navy + teal (green was agent-specific) |
| No callout blocks (TIP/HOW-TO/DID YOU KNOW) | 3 callout block types woven naturally into content | Task spec + engagement improvement |
| No social link hover effects | onmouseover/onmouseout for FB/LI/TW hover | Task spec requirement for official hover colors |
| Table with 2 columns | Waste table expanded to 3 columns with "Recovery Range" | Higher information density; teal highlights key data |
| KPI table with 2 columns | KPI table expanded to 3 columns with "Target Frequency" | More actionable for enterprise IT readers |
| N8N prompt: generic accordion instructions | N8N prompt: explicit TOC unordered list rule + FAQ closed-by-default rule | Prevent regression on future generation runs |
| Workflow JSON: Codex agent references in sticky notes | Workflow JSON: "Copilot Agent — 2026-04-17" labels | Naming convention compliance |

---

## 4. What Was Rejected and Why

| Element/Approach | Source | Rejected Reason |
|---|---|---|
| External Google Fonts CDN link | Hermes Agent | WordPress safety: external dependencies stripped in many hosting environments; Montserrat is theme-loaded |
| SVG icons for social buttons | Claude Code | Task spec: "Zero SVG" — use text labels only |
| Background images on hero via `url()` | Some agents | Fragile in WordPress — inline background color/gradient is safer |
| Numbered TOC (ordered list) | Codex | Task spec explicitly prohibits numbers in TOC |
| Circular author logo (`border-radius:50%`) | Codex + Hermes | Task spec explicitly requires horizontal format, no circle |
| Script blocks for accordion toggles | Some agents | WordPress strips script tags in post content — inline onclick required |
| Both floating buttons on same side (left) | Codex | Overlap at small viewports + task spec requires opposite corners |
| `border-radius:50%` on logo at any size | All previous agents | PowerPlug logo is horizontal — circular crop cuts off brand name |
| Hard-coded article dates in intro paragraph | Some agents | Task spec: "NO dates/years in first paragraph or intro" |
| Generic "Lorem ipsum" placeholder content | N/A | Task spec: "Full files — no snippets or abbreviated content" |
| Sentice branding or references | All previous agents (some had residual refs) | Task spec HARD RULE: "NEVER use Sentice branding" |
| Emoji for callout box indicators | agent-zero | Task spec: "zero emoji" |
| `<i>` or `<span>` icon fonts for social buttons | Some agents | Task spec: zero icon fonts |
