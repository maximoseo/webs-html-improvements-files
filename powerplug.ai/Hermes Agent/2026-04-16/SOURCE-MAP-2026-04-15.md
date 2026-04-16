# Source Map — powerplug.ai Hermes Agent Redesign
**Working date:** 2026-04-15
**Version:** Hermes Agent / 2026-04-16

---

## Brand Assets

| Asset | Source | URL |
|---|---|---|
| Logo image | powerplug.ai live site | https://powerplug.ai/wp-content/uploads/2022/06/powerplug-logo.png |
| Contact page URL | powerplug.ai live site | https://powerplug.ai/contact-us |
| Facebook page | powerplug.ai /contact-us | https://www.facebook.com/PowerPlugLtd/ |
| Twitter/X page | powerplug.ai /contact-us | https://twitter.com/PowerPlugLtd |
| LinkedIn page | powerplug.ai /contact-us | https://www.linkedin.com/company/494877/ |
| Phone | powerplug.ai /contact-us | +1-646-7517797 |
| Email | powerplug.ai /contact-us | info@powerplug.ai |
| Address | powerplug.ai /contact-us | 7 HaArad Street, Tel Aviv 6971060, Israel |
| VAT ID | powerplug.ai /contact-us | 514261270 |

---

## Brand Colors

| Token | Value | Source |
|---|---|---|
| Primary navy | #151d3f | powerplug.ai live site (computed CSS) |
| Dark navy | #131b3b | powerplug.ai live site |
| Section navy | #202953 | powerplug.ai live site |
| Green accent | #8bc540 | powerplug.ai live site (computed CSS, CTA buttons) |
| Light section bg | #f5f9fc | powerplug.ai live site |
| Body text | #1a2540 | derived from brand palette |
| Light green tint | #f7fbf3 | derived from brand accent |

---

## Verified Trust Signals & Data

| Claim | Source |
|---|---|
| Up to 60% PC energy savings | powerplug.ai homepage |
| ROI in as little as 4 months | powerplug.ai homepage |
| Supports 100–50,000+ PCs | powerplug.ai homepage |
| Clalit Health Services — 45,000+ PCs, $1.2M annual savings, 14 hospitals + 1,200 clinics | powerplug.ai case studies |
| Rambam Healthcare Campus — 2,000+ PCs, ROI under 4 months, client since November 2009 | powerplug.ai case studies |
| Ben Gurion University — 20,000+ student PCs, green campus initiative | powerplug.ai case studies |

---

## External Reference Links

| Purpose | URL | Used in |
|---|---|---|
| Did You Know fact (idle PC energy) | https://www.energy.gov/eere/buildings/computers-and-office-equipment | Why PC Power Management section |

---

## Internal Links Used

| Anchor text | URL | Section |
|---|---|---|
| WakeUp Portal | https://powerplug.ai | WakeUp Technology section |
| PowerPlug | https://powerplug.ai | Author block logo |
| Contact PowerPlug | https://powerplug.ai/contact-us | Author block CTA |

---

## Reused Ideas from Reference Versions

| Idea | Source version | How used |
|---|---|---|
| <details>/<summary> for TOC/FAQ | Hermes Agent v1 | Retained and improved with animation, collapse-by-default |
| 3-CTA block structure | Hermes Agent v1 | Retained, strengthened with distinct labels and trust lines |
| Hero dark navy gradient | Hermes Agent v1 | Retained, improved with logo badge and refined copy |
| Case study proof strip | Codex/2026-04-16 | Used real numbers from Codex's approach, verified against live site |
| Section alternation pattern | Claude Code/2026-04-16 | Applied alternating white/#f7fbf3 surfaces |
| Author block rectangular logo | Hermes Agent v1 | Retained and improved with social links and contact button |

---

## N8N Workflow Changes

| Node | Change | Reason |
|---|---|---|
| Writing Blog (template node) | Full prompt replacement | Old prompt lacked floating button rules, no-date rule, collapsed TOC/FAQ requirement, social hover colors |
| Writing Blog (assembler node) | Full prompt replacement with improved writing-stage rules | Old prompt had weaker brand guidance and no Tips/How-To/Did You Know requirement |
| Image Prompts node | Brand token fix: #7238ce → #8bc540 | Purple was not a PowerPlug brand color; green matches actual brand accent |
| Workflow name | Updated to include 2026-04-15 reference | Working date alignment |
