# Source Map — PowerPlug.ai Article System v3.0
Date: 2026-04-15

## Primary Sources

### Brand Identity
- **PowerPlug live site**: https://powerplug.ai
  - Logo: https://powerplug.ai/wp-content/uploads/2022/06/powerplug-logo.png
  - Contact: https://powerplug.ai/contact-us
  - About: https://powerplug.ai/about-us
  - Homepage: https://powerplug.ai/home
  - Blog: https://powerplug.ai/category/powerplug-blog
  - LinkedIn Insights: https://powerplug.ai/linkedin-insights
  - Why PC Power Management: https://powerplug.ai/why-is-pc-power-management-crucial-for-your-business

### Social Accounts (verified)
- **Facebook**: https://www.facebook.com/PowerPlugLtd/
- **Twitter/X**: https://twitter.com/PowerPlugLtd

### Institutional References (used in content)
- **U.S. Government Accountability Office (GAO)**: https://files.gao.gov/reports/GAO-26-109060/index.html — Software license management report
- **BTL Israel (government service portal)**: https://www.btl.gov.il — Self-service FAQ context
- **Israel Ministry of Finance FinOps training**: https://thekey.mof.gov.il — FinOps definition reference

### Image Assets
- All article images hosted on powerplug.ai CDN at `/wp-content/uploads/2026/04/`
- Image list:
  - `AScenarioTheEnterprisePayingTwicefortheSameCapability.avif`
  - `CloudCostControlandtheRiseofFinOps.avif`
  - `Buildinga12MonthEnterpriseCostSavingsRoadmap-scaled.avif`
  - `HowtoChooseaSolutionThatDeliversMeasurableITCostReduction.avif`

## Design & Pattern Sources

### UI Library Patterns
- **shadcn/ui** — Component anatomy, button variants, card structure, accordion discipline
  - Source: https://ui.shadcn.com
  - Applied: FAQ `<details>/<summary>` structure, card hover logic, social button CSS :hover
- **Aceternity UI** — Premium hero atmosphere, dark section framing
  - Source: https://ui.aceternity.com
  - Applied: Dark gradient hero, radial glow decoration, section rhythm
- **Uiverse** — Selective button/hover micro-inspiration (minimal, CSS-only)
  - Source: https://uiverse.io
  - Applied: Floating button pill shape and shadow depth

### CTA Patterns
- **HTMLStream CTA collection** — CTA section type taxonomy, layout variants
  - Source: https://htmlstream.com
  - Applied: Opening green CTA, mid-article outline CTA, closing dark CTA
- **Shelter Design Framework** — Button hierarchy, color roles, trust/disclaimer text
  - Source: https://shelter.design
  - Applied: Primary (green solid) > Secondary (dark outline) button hierarchy

### Design Rules
- **PAT-CTA-UI-Categorized-Patterns.md** — Button types, hover states, anti-patterns
  - Location: `skills/redesign-html-template/references/cta-ui-harvest/categorized-patterns.md`
- **PAT-CTA-Decision-Rules.md** — Context selection, quality checklist
  - Location: `skills/redesign-html-template/references/cta-ui-harvest/decision-rules.md`
- **wordpress-adaptation-rules.md** (UI Libraries)
  - Location: `skills/redesign-html-template/references/ui-library-harvest/wordpress-adaptation-rules.md`

## Workflow Sources

### N8N System
- **Improved_N8N_Workflow.json v3.0** — Article generation pipeline with 8 nodes
  - Nodes: Webhook Trigger → Fetch Brand Site → Extract Brand Intel → Load System Prompt → Prepare Prompt Context → Generate Article (AI) → Validate & Sanitize → Respond to Webhook
  - Validation rules: logo check, TOC prefix check, H1 count, content block check, floating button position check

### Prompt System
- **Improved_N8N_Prompt.txt v3.0** — Full article generation ruleset
  - Encoded rules: brand identity, color spec, structure order, CTA logic, content quality rules, WordPress safety, responsive rules, content block types and frequency, floating element specs

## Previous Version
- **v2.0** was built 2026-04-16 and established the base structure
- **v3.0** upgrades: Tip/How-To/Did You Know blocks, TOC numeric prefix removal, CSS :hover social buttons, scroll-to-top visibility toggle, mid-article inline nudges, logo → home URL link, date removal from hero

## Key Change Log (v2.0 → v3.0)
1. Added Tip blocks (2x) — amber (#f59e0b) left border
2. Added How-To block (1x) — green (#8AD628) left border
3. Added Did You Know blocks (2x) — indigo (#6366f1) left border
4. Removed "April 2026" from hero read-time line
5. Removed numeric prefixes from all TOC headings
6. Social hover: changed from inline JS `onmouseover` to CSS `:hover` classes
7. Scroll-to-top: added visibility toggle via `.visible` class + scroll listener
8. Contact floating button: always visible (removed conditional)
9. Logo in author section now links to `powerplug.ai/home`
10. Added mid-article inline CTA nudges (2x) between sections
11. Updated N8N prompt to v3.0 with all new rules
12. Updated N8N workflow validation to check all new rules
13. All dates references updated to `2026-04-15`
