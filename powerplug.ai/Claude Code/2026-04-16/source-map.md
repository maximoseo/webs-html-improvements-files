# PowerPlug.ai — Source Map

**Working date:** 2026-04-15

Every real brand asset, URL, contact, social handle, and trust signal incorporated into the redesign — with its live-site origin.

## Identity assets

| Asset | Value (used in template) | Source |
|---|---|---|
| Legal name | PowerPlug Ltd. | `https://powerplug.ai/` homepage + contact page footer |
| Homepage URL | `https://powerplug.ai/` | Live site |
| Tagline | "Optimize IT Operations And Cut Your Energy Bill" | Homepage hero |
| Language / direction | English / LTR | Homepage `<html lang="en">` |

## Logo + author block

| Asset | Value | Source |
|---|---|---|
| Logo URL (author block, linked to homepage) | `https://powerplug.ai/wp-content/uploads/2022/06/powerplug-logo.png` | Live `<img>` src pulled from homepage header |
| Author-logo anchor target | `https://powerplug.ai/` | Brand standard — author-block logo must route to homepage |
| Author display name | "The PowerPlug Team" | Brand convention (company-authored content) |

## Contact

| Channel | Value | Source |
|---|---|---|
| Contact page URL (canonical) | `https://powerplug.ai/contact-us` | Live fetch `WebFetch(https://powerplug.ai/contact-us)` — page title `Contact Us \| PowerPlug`, form labeled "LETS TALK" |
| Email (mailto) | `info@powerplug.ai` | Contact page body |
| Phone (tel) | `+1-646-751-7797` (display) / `+16467517797` (tel link) | Contact page body |
| Postal address (contextual reference only) | 7 HaArad Street, Tel Aviv 6971060, Israel | Contact page body |

## CTA destinations (all 5 CTA touchpoints)

Every one of the following MUST resolve to `https://powerplug.ai/contact-us`:

1. CTA #1 top button — "Get a Free Assessment"
2. CTA #2 mid button — "Talk to the PowerPlug Team"
3. CTA #3 bottom button — "Schedule a Free Consultation"
4. Secondary email link under CTA #3 — `mailto:info@powerplug.ai`
5. Secondary phone link under CTA #3 — `tel:+16467517797`
6. Floating Contact Us button (always visible) — `/contact-us`

## Social links (author block)

| Network | Profile URL | Hover brand color |
|---|---|---|
| LinkedIn | `https://www.linkedin.com/company/powerplug-ltd` | #0A66C2 |
| Facebook | `https://www.facebook.com/PowerPlugLtd/` | #1877F2 |
| Twitter / X | `https://twitter.com/PowerPlugLtd` | #000000 |

All three were scraped from the live homepage footer social row. No Instagram / YouTube / TikTok surfaced — none included (no fabrication).

## Internal deep links (in body copy)

| Anchor text (approx) | Target | Placement |
|---|---|---|
| "PowerPlug case study library" | `https://powerplug.ai/case-studies` | Section 5 — Endpoint Energy deployment narrative |
| "PowerPlug's platform" | `https://powerplug.ai/our-platform` | Section 10 — How to Choose a Solution |

## External authoritative links

| Anchor text | Target | Purpose |
|---|---|---|
| "FinOps" | `https://www.finops.org/` | Section 6 — defining the discipline |
| "FinOps practices" | `https://www.finops.org/introduction/what-is-finops/` | Section 1, Four Pillars list |

Both use `rel="nofollow noopener" target="_blank"`. Color #0a8c88 + underline.

## Trust signals / real proof points (used in body copy)

All of the following are real, publicly-published PowerPlug case studies. None are fabricated — if a future article's ORIGINAL_HTML does not already reference one of these, the prompt instructs the agent NOT to invent it.

| Customer | Scope | Outcome claimed |
|---|---|---|
| Clalit Health Services | 45,000+ PCs | ~$1.2M annual electricity savings |
| Rambam Healthcare Campus | 2,000+ PCs | ROI under 4 months |
| Ben Gurion University | 20,000+ student-facing PCs | Reduced power draw while preserving remote access |

## Color palette (brand tokens)

Locked to PowerPlug's recurring visual identity (navy + green + teal) across homepage, case studies, and contact page:

- Navy primary: `#131b3b`
- Mid navy (gradient step): `#1e2a52`
- Teal secondary: `#0a8c88`
- Green primary CTA + accent: `#8AD628`
- Green hover: `#78bd20`

## Assets NOT used (intentionally excluded)

- No Sentice or legacy-agency branding. All references scrubbed from the final HTML.
- No placeholder author image (Supabase-hosted test logo from earlier drafts). Real PowerPlug logo used instead.
- No Google Fonts, CDN links, jQuery, Font Awesome, or SVG icon sets — incompatible with WordPress inline-only rendering.
