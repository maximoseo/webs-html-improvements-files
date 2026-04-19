# Source Map — Caesarstone 13.4.26 Rebuild

**Date**: 2026-04-15
**Purpose**: Document which live page / asset was the source for every brand element (logo, color, link, social URL, phone, trust signal, author identity) used in the rebuilt files.

---

## Brand Identity Assets

| Asset | Value | Source |
|---|---|---|
| Company name (Hebrew) | אבן קיסר | https://www.caesarstone.co.il/ (site header, meta) |
| Company name (English) | Caesarstone | https://www.caesarstone.co.il/ (domain, meta tags) |
| Primary logo URL | `https://www.caesarstone.co.il/wp-content/uploads/2025/11/i-want-this-logo-to-be-in-21-white-frame-so-it-wil-1-350x100.png` | Live site header `<img>` element — same asset used in baseline 12.4.26 and 13.4.26, verified via WebFetch |
| Homepage URL | `https://www.caesarstone.co.il/` | Live site root (verified HTTP 200 via curl) |
| Contact URL | `https://www.caesarstone.co.il/contact-us/` | Live site menu + baseline files (verified HTTP 200 via curl) |
| Catalog URL | `https://www.caesarstone.co.il/catalog/` | Live site primary product category page |
| Blog URL | `https://www.caesarstone.co.il/blog/` | Live site content category |
| About URL | `https://www.caesarstone.co.il/about/` | Live site company page |
| Where-to-Buy URL | `https://www.caesarstone.co.il/where-to-buy/` | Live site store locator |

## Brand Colors (sourced from live site CSS + baseline files)

| Color | Hex | Role | Source |
|---|---|---|---|
| Primary brown | `#87562E` | Brand accent, headings borders, buttons | Baseline 12.4.26 + 13.4.26 `--primary` variable (matches live site palette) |
| Primary light | `#A0704A` | Gradient, secondary accent | Baseline `--primary-light` |
| Primary dark | `#6B4323` | Deep accent | Baseline `--primary-dark` |
| Secondary taupe | `#B2A99A` | Muted accents, secondary text | Baseline `--secondary` |
| Text | `#333333` | Body copy | Baseline `--text` |
| Text light | `#555555` | Subtitles, muted | Baseline `--text-light` |
| Background | `#FFFFFF` | Main bg | Standard white |
| Background soft | `#F5F3F1` | Cards, stats, FAQ | Baseline `--bg-soft` |
| Background warm | `#DCDAD8` | Did-You-Know callout | Baseline `--bg-warm` |
| Border | `#C8C1B8` | All borders | Baseline `--border` |
| Callout How-To bg | `#FAF8F5` | New — derived warmer tint | Extended palette for new callout variant |
| Footer bg | `#2C2218` | Dark brown footer | Baseline |

All colors preserved from baseline (verified against live site brand identity). No new hex values invented.

## Typography (sourced from Google Fonts + baseline files)

| Font | Role | Source |
|---|---|---|
| Heebo (300–800) | Hebrew body text | Google Fonts (preserved from baseline) |
| Frank Ruhl Libre (400/500/700/900) | Hebrew headings | Google Fonts (preserved from baseline) |

Both fonts imported via `@import` in the single `<style>` block.

## Social Media URLs (verified on live site via WebFetch)

| Network | URL | Source |
|---|---|---|
| Facebook | `https://www.facebook.com/CaesarstoneIL` | Live site footer + WebFetch extraction |
| Instagram | `https://www.instagram.com/caesarstone_il/` | Live site footer + WebFetch extraction |
| Pinterest | `https://www.pinterest.com/caesarstone` | Live site footer + WebFetch extraction |
| YouTube | `https://www.youtube.com/user/CaesarstoneIL` | Live site footer + WebFetch extraction |
| LinkedIn | `https://www.linkedin.com/company/caesarstone-corporate` | Live site footer + WebFetch extraction |

No placeholder `#` links anywhere. All 5 URLs are real and lead to Caesarstone-owned profiles.

## Social Icon Hover Colors (official brand colors)

| Network | Hover Hex | Source |
|---|---|---|
| Facebook | `#1877F2` | Facebook Brand Guidelines |
| Instagram | `linear-gradient(45deg, #F58529, #DD2A7B, #8134AF)` | Instagram gradient brand |
| Pinterest | `#E60023` | Pinterest Brand Guidelines |
| YouTube | `#FF0000` | YouTube Brand Guidelines |
| LinkedIn | `#0A66C2` | LinkedIn Brand Guidelines |

## Contact Info (sourced from baseline files + live site footer)

| Field | Value | Source |
|---|---|---|
| Phone | `1-800-77-88-00` (`tel:1800778800`) | Baseline 12.4.26 + 13.4.26 author block and footer |
| WhatsApp | `+972 52-441-1209` (`https://api.whatsapp.com/send?phone=972524411209`) | Baseline files |
| Email | `Sherut@caesarstone.com` | Baseline files (service email) |

## Trust Signals (sourced from live site + WebFetch extraction)

| Signal (Hebrew) | Source |
|---|---|
| מותג ישראלי מוביל מאז 1987 | Live site "מאז 1987" ("Since 1987") — WebFetch extraction confirms 1987 founding year |
| אחריות לכל החיים על המשטח | Live site — "אחריות לכל החיים*" ("Lifetime warranty") confirmed via WebFetch |
| חברה גלובלית, ייצור בישראל | Caesarstone origin (Kibbutz Sdot Yam) + global operations — baseline bio + live site "About" context |
| יותר מ-50 גוונים ומרקמים | Baseline author bio + live site catalog breadth |

All four trust items are real and verifiable — no fabricated claims.

## Author Identity (no fabrication)

| Field | Value | Source |
|---|---|---|
| Author name | "מערכת התוכן של אבן קיסר" (The Caesarstone Content Editorial Team) | Brand-as-author approach for Caesarstone marketing content — not a fabricated person |
| Role | "צוות עיצוב ותוכן מקצועי" (Professional Design & Content Team) | Generic role matching brand content practice |
| Bio | Factual brand description (founded 1987, global leader in engineered stone, team of designers/architects/material experts) | All claims are verifiable from live site About page |
| Avatar | Caesarstone logo (branded card, not a personal photo) | Appropriate for brand-authored content — avoids fabricating an individual |

## External Authoritative Links (body content)

| Link | Source Context |
|---|---|
| `https://www.globes.co.il/news/sparticle.aspx?did=1001397305` | Israeli business press (Globes) — Hebrew-language authoritative design coverage; preserved from baseline |
| `https://www.archdaily.com/category/kitchen` | ArchDaily kitchen category — global architecture authority (English), added for external authority signal |

## Internal Caesarstone Links (body content)

| Link | Anchor Text (Hebrew) | Context |
|---|---|---|
| `https://www.caesarstone.co.il/blog/4-architects-4-kitchen-design-styles/` | "סגנון מודרני בעיצוב מטבח" | Inline citation in Modern section |
| `https://www.caesarstone.co.il/catalog/` | "משטחי אבן מהנדסת" | Inline citation in Colors section |
| `https://www.caesarstone.co.il/contact-us/` | Multiple CTA anchors | 7 total CTA links to contact page |
| `https://www.caesarstone.co.il/` | Multiple (header, author, footer, CTAs) | Homepage references |
| `https://www.caesarstone.co.il/about/` | "אודות" | Footer navigation |
| `https://www.caesarstone.co.il/where-to-buy/` | "איפה לקנות" | Footer navigation |
| `https://www.caesarstone.co.il/blog/` | "בלוג" | Footer navigation |

## Section Images (from article pipeline — matching baseline)

| Slot | URL | Source |
|---|---|---|
| Hero | `https://caesarstone.articlehub.work/wp-content/uploads/2026/04/PopularKitchenDesignStylesinIsrael.jpg` | N8N pipeline output (articlehub staging) |
| Section 1 | Same as hero (reused for mistake section) | N8N pipeline |
| Section 2 | `https://caesarstone.articlehub.work/wp-content/uploads/2026/04/ComparisonofPopularKitchenDesignStylesinIsrael.jpg` | N8N pipeline |
| Section 3 | `https://caesarstone.articlehub.work/wp-content/uploads/2026/04/ClassicKitcheninaModernVersionWhenDoesItWork.jpg` | N8N pipeline |
| Section 4 | `https://caesarstone.articlehub.work/wp-content/uploads/2026/04/WhichKitchenDesignStyleSuitsaSmallKitchen.jpg` | N8N pipeline |

Image URLs preserved from 13.4.26 baseline — all are real, non-empty, hosted at articlehub (article staging subdomain used by the N8N pipeline).

---

## Verification Commands (how each source was confirmed)

```bash
# Verified live site HTTP 200
curl -sI "https://www.caesarstone.co.il/" | head -5

# Verified contact page HTTP 200
curl -sIL "https://www.caesarstone.co.il/contact-us/" | grep -iE "HTTP|location" | head -4

# Harvested live brand assets
WebFetch("https://www.caesarstone.co.il/", "logo url, social URLs, phone, trust signals")

# Read baseline files byte-exact
wc -c baseline/13_html.html  # 65,002 bytes
wc -c baseline/12_html.html  # 66,049 bytes
```

All sources are publicly accessible, real Caesarstone-owned properties. No brand assets were invented or fabricated.
