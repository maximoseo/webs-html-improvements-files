# Source Map — powerplug.ai Claude Code rebuild
**Working date:** 2026-04-15
**Version path:** `powerplug.ai / Claude Code / 2026-04-16`

---

## Brand Assets (from live site)

| Asset | Value | Source |
|---|---|---|
| Company name | PowerPlug Ltd. | powerplug.ai live scrape |
| Homepage | https://powerplug.ai | live scrape |
| Contact URL | https://powerplug.ai/contact-us | live scrape |
| Logo | https://powerplug.ai/wp-content/uploads/2022/06/powerplug-logo.png | live scrape (consistent across every reference version) |
| Phone | +1-646-751-7797 | live scrape + Hermes source-map |
| Email | info@powerplug.ai | live scrape + Hermes source-map |
| Address | 7 HaArad Street, Tel Aviv 6971060, Israel | Hermes source-map (verified) |
| Facebook | https://www.facebook.com/PowerPlugLtd/ | live scrape + every reference version |
| Twitter / X | https://twitter.com/PowerPlugLtd | live scrape + every reference version |
| LinkedIn | https://www.linkedin.com/company/powerplug-ltd | live scrape (slug form preferred over Hermes's numeric ID) |

## Brand Palette (documented hex values)

| Token | Value | Source |
|---|---|---|
| Navy primary | `#151d3f` | Hermes — computed CSS from live site |
| Navy section | `#202953` | Hermes |
| Navy deep | `#131b3b` | TimClaw — same live site, slightly deeper shade, used in hero gradient stop |
| Green accent | `#8bc540` | Hermes — computed CSS of CTA button |
| Green-light tint | `#f7fbf3` | Hermes — derived from accent |
| Surface | `#f5f9fc` | Hermes |
| Card | `#ffffff` | all versions |
| Text primary | `#1a2540` | Hermes |
| Text muted | `#475569` | derived (Tailwind slate-600 neutral, passes contrast) |
| Border | `#e2e5ea` | TimClaw |
| Social hover Facebook | `#1877F2` | Facebook brand guide |
| Social hover Twitter/X | `#000000` | X rebrand |
| Social hover LinkedIn | `#0A66C2` | LinkedIn brand guide |

## Element-by-Element Origin Tracing

| Element | Chosen implementation | Sourced from | Why |
|---|---|---|---|
| Article wrapper `<article id="powerplug-article" direction:ltr …>` | ✓ | Hermes | Hermes's scoped wrapper pattern is the cleanest across all five references — every style is namespaced under `#powerplug-article`, which survives a WordPress theme that also scopes its own CSS. |
| Single scoped `<style>` block for pseudo-states, chevron animation, breakpoints | ✓ | Hermes | Hermes is the only version that kept chevron animation + :hover + @media inside a single, short scoped block. TimClaw used multiple small blocks; Codex inlined at the expense of `:hover`. |
| Dark navy hero with green eyebrow pill and radial glow | ✓ | Hermes + Codex | Hermes contributes the navy gradient and "Enterprise … Playbook" eyebrow; Codex's radial decorative glow is layered on top at low opacity for depth. |
| Key Takeaways box on `#f5f9fc` | ✓ | Hermes | Hermes's "Key Takeaways" after the hero is the most useful hand-off for C-suite skimmers. |
| TOC as `<details class="pp-toc">` collapsed | ✓ | Hermes + TimClaw | Both versions converged on `<details>/<summary>` with a CSS chevron. Claude Code's previous version used a JS accordion which broke under WordPress plugin conflicts — rejected. |
| TOC placement (after Key Takeaways + intro paragraph) | ✓ | Hermes | Hermes is the only version that obeys rule 5 strictly ("after the first paragraph or first image, never the very first element"). |
| 3-stat trust strip (60% / <4 mo / 100-50K+) | ✓ | Hermes | Hermes sourced these three numbers directly from the live homepage; confirmed present on powerplug.ai. |
| Section template (H2 with green border-bottom, H3 with green left-border) | ✓ | Hermes + TimClaw | Green underline is distinctive, matches live site brand accent, and gives visual rhythm. TimClaw's H3 left-border discipline is adopted. |
| Tip block (amber left border on `#fffbe6`) | ✓ | TimClaw | TimClaw's amber palette is the cleanest among the references. Hermes used a similar structure without the tri-color discrimination. |
| How-To block (green left border on `#f0fbe8`) | ✓ | TimClaw | Distinct visual class from the Tip block while staying within brand palette. |
| Did-You-Know block (indigo left border on `#eef2ff`) | ✓ | TimClaw | Indigo provides colour contrast against amber/green so the reader scans different content classes by colour. |
| Mid-article green-tinted inline CTA | ✓ | Hermes | Hermes popularised the split-row inline nudge (headline + button on one line collapsing to stacked on mobile). |
| Mid-article dark-navy inline CTA | ✓ | new (Claude Code rebuild) | Added as the second mid-CTA to satisfy rule 8 (≥ 2 mid-article CTAs). Dark-navy variant distinguishes it from the green-tinted first block. |
| ROI comparison table | ✓ | Hermes | Hermes included a 3-row fleet-size comparison table. Retained with cleaner column widths and a footnote clarifying assumptions. |
| Case-study card grid (Clalit / Rambam / Ben Gurion) | ✓ | Hermes | Hermes source-map documents these three as verified from public PowerPlug case studies. Used verbatim. |
| End-of-article dark-navy CTA with radial glow + tel: button | ✓ | Hermes + new | Hermes's dark-navy end CTA is retained; added secondary `tel:+16467517797` button to strengthen the phone-as-CTA contextual contact rule (rule 10). |
| FAQ as 7 `<details class="pp-faq-item">` collapsed | ✓ | Hermes | Hermes uses `<details>` per item with no JS. Retained with the 7th question added ("Is there a minimum fleet size?") to broaden relevance. |
| About the Author (rectangular logo tile + social icons + brand-hover + contact button + phone/email/address row) | ✓ | Hermes | Hermes is the only version that puts the logo inside a bordered tile that links to the homepage and combines social icons with a phone/email/address utility row. Retained verbatim and given correct slug LinkedIn URL from live scrape. |
| Floating Contact Us button (bottom-right, always visible) | ✓ | Hermes + user rule 11 | Hermes placed it bottom-right; TimClaw placed it bottom-LEFT. User's rule 11 explicitly says "bottom-right for LTR", so Hermes's choice wins. |
| Floating Scroll-to-Top button (300 px threshold, `.pp-visible` toggle) | ✓ | Hermes | Hermes's single-class visibility toggle is the most WordPress-robust pattern — works across themes that strip event handlers. |
| Inline 6-line visibility script | ✓ | Hermes | Minimal, passive listener, no frameworks. Sized to survive WordPress plugin minifiers. |
| Social hover colors (FB #1877F2, X #000, LinkedIn #0A66C2) | ✓ | TimClaw + user rule 25 | Exact brand hex values as required. |
| Chevron animation (0.3 s `transform:rotate(45deg)`) | ✓ | Hermes | Short, smooth, and style-only. |

## What Was Deliberately NOT Carried Forward

| Source | Pattern | Reason |
|---|---|---|
| Current Claude Code/2026-04-16 | Off-brand teal gradient in the hero | Off-brand — PowerPlug palette is navy + green only. |
| Codex/2026-04-16 | Multiple `<style>` blocks scattered through the body | Fragile under WordPress shortcode filters. Consolidated into one scoped block. |
| CLAUDE CODE (Tim Claw Max)/2026-04-16 | Floating buttons on the LEFT side | User rule 11 explicitly requires bottom-RIGHT for LTR. |
| agent-zero/2026-04-16 | Emoji-heavy callouts with decorative `::before` pseudo-content | Looks AI-generated. Replaced with discrete eyebrow labels on each callout class. |
| agent-zero v2 (2026-04-15 updated) | "Read time: April 2026" in hero eyebrow | Rule 18 forbids dates in the hero / intro area. Removed. |
| TimClaw | `onmouseover=` / `onmouseout=` inline JS on social icons | Replaced with CSS `:hover` / `:focus` rules — cleaner and survives WordPress HTML sanitisers. |

## N8N Workflow Sources

| Node | Adapted from | Change |
|---|---|---|
| Webhook Trigger | TimClaw | Renamed path to `/powerplug-article`, response mode set to `responseNode` so Respond-to-Webhook can emit structured JSON. |
| Fetch PowerPlug Site | TimClaw | Added 20 s timeout. |
| Extract Brand Intelligence | TimClaw | Rewritten to use the Hermes-correct palette (`#151d3f`, `#8bc540`) and full social + trust-signal + external-reference arrays. |
| Load System Prompt | TimClaw v3 | Rewritten from scratch to encode all 34 rules from the user brief, with explicit CTA label set and structure order. |
| Prepare Prompt Context | TimClaw | Kept the webhook-merge pattern; added safer defaults and the combined `systemPrompt` + `userPrompt` split. |
| Generate Article (AI) | TimClaw | Temperature lowered to 0.35 (from 0.4) to keep the model closer to the structure rules. Max tokens 16,000. |
| Validate & Sanitize Output | TimClaw + new | Expanded to enforce rules 4, 6, 11, 12, 13, 14, 15, 16, 18, 20, 23 with explicit per-rule error/warning messages. |
| Respond to Webhook | TimClaw | Unchanged structure; now returns `{ success, html, validation }` with full stats. |

## External References Cited in the Article

| URL | Purpose |
|---|---|
| https://www.energystar.gov/products/office_equipment/computers | Device-class baseline for desktop idle draw (Did You Know block in "Why Power Management"). |
| https://www.iea.org/reports/digitalisation-and-energy | Referenced in the intro as broader research context. |
| https://www.gartner.com/en/information-technology/insights/sustainability | Cited in the ESG/Scope 2 section. |
| https://learn.microsoft.com/en-us/windows/win32/power/power-management-portal | Did You Know block in the Security section. |

## Version Comparison Summary

| Version | Size | Strengths | Discarded |
|---|---|---|---|
| Hermes Agent / 2026-04-16 | 37 KB | Strongest brand integrity, cleanest TOC/FAQ, verified case studies | (base reference — mostly kept) |
| Codex / 2026-04-16 | 43 KB | Section layout depth | Off-brand teal leakage |
| CLAUDE CODE (Tim Claw Max) / 2026-04-16 | 57 KB | Best callout discrimination (Tip/How-To/Did-You-Know palettes) | Left-side floating buttons |
| agent-zero / 2026-04-16 | 60 KB | Long-form depth | Emoji callouts, generic design |
| agent-zero v2 / 2026-04-15 | 48 KB | Trimmed layout | "April 2026" in hero (rule 18 violation) |
| Claude Code / 2026-04-16 (current) | 52 KB | Section alternation pattern | Off-brand hero colouring, weaker author block |
