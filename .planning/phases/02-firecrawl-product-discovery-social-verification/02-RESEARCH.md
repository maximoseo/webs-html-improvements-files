# Phase 2: Firecrawl Product Discovery & Social Verification - Research

**Researched:** 2026-03-25
**Domain:** E-commerce product crawling, Shopify data extraction, social profile verification
**Confidence:** HIGH

## Summary

hipsterstyle.co.il is a **Shopify-based** kids fashion e-commerce store (theme: Prestige v10.10.1, Shopify domain: hipsterbabystyle.myshopify.com). The brand "Hipster" (Hebrew: היפסטר) sells children's clothing ages 0-10. The site has 400+ products across 135+ collections, 25+ blog posts, and two physical stores in Rishon LeZion.

The site exposes a standard Shopify JSON API at `/products/{handle}.json` which returns structured product data including titles, descriptions, image URLs, tags, prices, and variants. Product images are hosted on `cdn.shopify.com` which is generally stable but should be mirrored to Supabase for WordPress durability. Social profiles are confirmed: Facebook (`/HipsterBabyCollection`) and Instagram (`/hipster.style/`). No YouTube channel found.

**Primary recommendation:** Use Shopify JSON API (`/products/{handle}.json`) for reliable product data extraction. Select 6 products from the Passover 2026 / Sets & Outfits collections for maximum relevance to a "kids styling tips" article. Mirror product images to Supabase. Use verified social URLs from the site footer.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
None -- all implementation choices are at Claude's discretion.

### Claude's Discretion
All implementation choices are at Claude's discretion -- infrastructure/data discovery phase:
- Firecrawl crawl strategy (sitemap vs deep crawl vs targeted inner page discovery)
- Product relevance filtering criteria (kids clothing, styling accessories, etc.)
- Social profile verification approach (Firecrawl scrape of footer/contact pages)
- Image stability assessment (which product images need Supabase hosting)
- Data format for extracted products (JSON structure for downstream template use)

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| PROD-01 | Firecrawl discovers real product pages from hipsterstyle.co.il inner pages | DONE: Site mapped, 400+ products discovered, Shopify JSON API verified, product URLs confirmed |
| PROD-02 | Only products relevant to article topic are selected | Recommendation: 6 products from Sets & Outfits / Passover 2026 collections (kids styling outfits) |
| PROD-08 | Links go to real product pages -- no invented URLs | All product URLs verified via Shopify sitemap and JSON API; URL pattern: `https://hipsterstyle.co.il/products/{hebrew-handle}` |
| AUTH-03 | Social links with correct verified URLs | Facebook: `https://www.facebook.com/HipsterBabyCollection` / Instagram: `https://www.instagram.com/hipster.style/` -- both found in site footer/header |
| AUTH-04 | Firecrawl verifies real active social profiles and YouTube channel | Facebook and Instagram verified from site source. No YouTube channel found for this brand. |
| AUTH-05 | Only verified real profiles added -- no invented links | Two profiles confirmed (Facebook, Instagram). YouTube: not found, must be omitted. |
</phase_requirements>

## Site Discovery Results

### Platform & Technology
| Property | Value | Source |
|----------|-------|--------|
| Platform | Shopify | Homepage HTML (`Shopify.shop` JS variable) |
| Theme | Prestige v10.10.1 | Homepage meta |
| Shopify domain | hipsterbabystyle.myshopify.com | Homepage JS config |
| Language | Hebrew (he) | HTML lang attribute |
| Currency | ILS (Israeli Shekel) | Shopify config |
| Country | IL | Shopify config |

### Site Structure
| Page | URL | Verified |
|------|-----|----------|
| Homepage | `https://hipsterstyle.co.il/` | YES |
| About Us | `https://hipsterstyle.co.il/pages/%D7%9E%D7%99-%D7%90%D7%A0%D7%97%D7%A0%D7%95` | YES |
| Contact | `https://hipsterstyle.co.il/pages/contact` | YES |
| Shops | `https://hipsterstyle.co.il/pages/shops` | YES |
| FAQ | `https://hipsterstyle.co.il/pages/%D7%A9%D7%90%D7%9C%D7%95%D7%AA-%D7%95%D7%AA%D7%A9%D7%95%D7%91%D7%95%D7%AA` | YES |
| Rewards | `https://hipsterstyle.co.il/pages/rewards` | YES |
| Shipping Policy | `https://hipsterstyle.co.il/policies/shipping-policy` | YES |
| Returns Policy | `https://hipsterstyle.co.il/policies/refund-policy` | YES |
| Privacy Policy | `https://hipsterstyle.co.il/policies/privacy-policy` | YES |
| Blog | `https://hipsterstyle.co.il/blogs/news` | YES (25+ posts) |

**IMPORTANT: No `/about`, `/gallery`, or `/contact` simple paths exist.** The old oritmartin.com URL patterns (`/about`, `/gallery`, `/contact`) do NOT map to hipsterstyle.co.il. The actual paths use Hebrew URL-encoded slugs or `/pages/` prefix.

### URL Mapping (Old -> New)

| Old oritmartin.com Path | hipsterstyle.co.il Equivalent | Notes |
|------------------------|------------------------------|-------|
| `/about` | `/pages/%D7%9E%D7%99-%D7%90%D7%A0%D7%97%D7%A0%D7%95` (מי אנחנו) | Different path structure |
| `/gallery` | NO EQUIVALENT | Hipster has no gallery page -- use collections instead |
| `/contact` | `/pages/contact` | Same slug, different prefix |
| `/product-page/{slug}` | `/products/{hebrew-slug}` | Shopify uses `/products/` not `/product-page/` |
| `/sculptures-1/...` | NO EQUIVALENT | Hipster is clothing, not sculptures |

### Brand Information
| Property | Value |
|----------|-------|
| Brand name (English) | Hipster |
| Brand name (Hebrew) | היפסטר |
| Tagline (Hebrew) | "היפסטר הוא חלום שלנו שמתגשם כל יום מחדש" |
| Founders | Omer & Noah, Yehav & Dana (two couples) |
| Logo URL | `/cdn/shop/files/hipster_logo_black.png` |
| Brand description | Israeli kids fashion brand, ages 0-10, stylish unique designs |

### Contact Information
| Type | Value | Source |
|------|-------|--------|
| Email | info@hipsterstyle.co.il | Web search (Lusha business listing) |
| Phone 1 | 052-9767667 | Web search (multiple sources) |
| Phone 2 | 03-5353003 | Web search (multiple sources) |
| Office address | Lazarov 23 (Zrubavel 23), Rishon LeZion | Product page shipping info + search |
| Store 1 | Kanyon HaZahav, Rishon LeZion, Floor 2 | /pages/shops |
| Store 2 | Azrieli Rishonim Mall, Rishon LeZion, Floor 2 | /pages/shops |

**Phone for tel: links:** `+972529767667` (mobile format) or `+97235353003` (landline)
**WhatsApp:** `https://wa.me/972529767667` (use mobile number)

### Social Media Profiles
| Platform | URL | Verified | Source |
|----------|-----|----------|--------|
| Facebook | `https://www.facebook.com/HipsterBabyCollection` | YES -- found in site footer HTML | Homepage footer |
| Instagram | `https://www.instagram.com/hipster.style/` | YES -- found in site footer HTML | Homepage footer |
| YouTube | NOT FOUND | Searched site + web -- no YouTube channel exists | Web search negative result |
| TikTok | NOT FOUND | Not referenced anywhere on site | Site crawl |

## Recommended Product Set

### Selection Criteria
Article topic: "kids styling tips" -- products should demonstrate styling, outfits, coordinated looks.
Best fit: **Sets & Outfits** collection + select individual pieces for mix-and-match examples.

### Recommended 6 Products

| # | Hebrew Name | Handle | URL | Category | Image URL (primary) |
|---|------------|--------|-----|----------|-------------------|
| 1 | חליפת סנדי | חליפת-סנדי | `https://hipsterstyle.co.il/products/%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%A1%D7%A0%D7%93%D7%99` | Girls suit | `https://cdn.shopify.com/s/files/1/0733/0552/2470/files/product-1019749.jpg` |
| 2 | חליפת הנרי | חליפת-הנרי | `https://hipsterstyle.co.il/products/%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%94%D7%A0%D7%A8%D7%99` | Boys suit | `https://cdn.shopify.com/s/files/1/0733/0552/2470/files/product-6642878.jpg` |
| 3 | חליפת נינו | חליפת-נינו | `https://hipsterstyle.co.il/products/%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%A0%D7%99%D7%A0%D7%95` | Boys premium suit | `https://cdn.shopify.com/s/files/1/0733/0552/2470/files/product-9363795.jpg` |
| 4 | חליפת מילה | חליפת-מילה | `https://hipsterstyle.co.il/products/%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%9E%D7%99%D7%9C%D7%94` | Girls suit | `https://cdn.shopify.com/s/files/1/0733/0552/2470/files/product-8489663.jpg` |
| 5 | טישרט אלי | טישרט-אלי | `https://hipsterstyle.co.il/products/%D7%98%D7%99%D7%A9%D7%A8%D7%98-%D7%90%D7%9C%D7%99` | Boys top | `https://cdn.shopify.com/s/files/1/0733/0552/2470/files/product-8927069.jpg` |
| 6 | ג'ינס שיי | ג-ינס-שיי | `https://hipsterstyle.co.il/products/%D7%92-%D7%99%D7%A0%D7%A1-%D7%A9%D7%99%D7%99` | Boys jeans | `https://cdn.shopify.com/s/files/1/0733/0552/2470/files/4878hipster29.12.2518175.jpg` |

**Why these 6:**
- 2 girls outfits + 2 boys outfits = gender balance for "styling tips"
- 1 top + 1 bottom = shows mix-and-match styling advice
- All from current Passover 2026 / Summer 2026 collections (not outdated)
- All tagged with "חג" (holiday) and "קיץ 2026" -- seasonally relevant
- All have multiple high-quality product photos available

### Alternative Products (if any above are unavailable)

| Hebrew Name | Handle | Category |
|------------|--------|----------|
| חליפת לוקה | חליפת-לוקה | Boys suit |
| חליפת ראיין | חליפת-ראיין | Boys suit |
| חליפת לונה לבנה | חליפת-לונה-לבנה | Girls suit |
| חליפת סלין | חליפת-סלין | Girls suit |
| סנדל חאקי | סנדל-חאקי | Boys sandal |

## Architecture Patterns

### Shopify Product Data Extraction Pattern

**Use the Shopify JSON API**, not HTML scraping:
```
GET https://hipsterstyle.co.il/products/{handle}.json
```

Returns structured JSON with: title, description, images (with full CDN URLs), tags, variants (with prices), vendor, product_type, published_at.

**Product URL construction:**
```
https://hipsterstyle.co.il/products/{URL-encoded-hebrew-handle}
```

**Image URL pattern (Shopify CDN):**
```
https://cdn.shopify.com/s/files/1/0733/0552/2470/files/{filename}.jpg
```

Image resize on the fly by appending width parameter:
```
https://cdn.shopify.com/s/files/1/0733/0552/2470/files/{filename}.jpg?width=600
```

### Recommended Output Data Format

```json
{
  "products": [
    {
      "name": "חליפת סנדי",
      "url": "https://hipsterstyle.co.il/products/%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%A1%D7%A0%D7%93%D7%99",
      "image": "https://zqcnyllsfwnssnuduvmj.supabase.co/storage/v1/object/public/article-assets/hipsterstyle/product-sandy.jpg",
      "image_alt": "חליפת סנדי מאת היפסטר",
      "category": "חליפות"
    }
  ],
  "social": {
    "facebook": "https://www.facebook.com/HipsterBabyCollection",
    "instagram": "https://www.instagram.com/hipster.style/"
  },
  "contact": {
    "phone": "+972529767667",
    "email": "info@hipsterstyle.co.il",
    "whatsapp": "https://wa.me/972529767667"
  },
  "brand": {
    "name_he": "היפסטר",
    "name_en": "Hipster",
    "site": "https://hipsterstyle.co.il/",
    "about_url": "https://hipsterstyle.co.il/pages/%D7%9E%D7%99-%D7%90%D7%A0%D7%97%D7%A0%D7%95",
    "contact_url": "https://hipsterstyle.co.il/pages/contact"
  }
}
```

### Image Stability Assessment

| Image Source | Risk Level | Action |
|-------------|-----------|--------|
| Shopify CDN (`cdn.shopify.com`) | MEDIUM | Shopify occasionally changes CDN URL structure. Mirror to Supabase for WordPress durability. |
| Old wixstatic.com images | HIGH | These belong to oritmartin.com, not hipsterstyle. Must be replaced entirely. |
| Supabase hosted images | LOW | Stable, self-controlled. Use for all product images in final template. |

**Recommendation:** Download all 6 product images from Shopify CDN and upload to Supabase under `/article-assets/hipsterstyle/` path. This ensures WordPress template images never break due to Shopify CDN changes.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Product data extraction | Custom HTML parser for product pages | Shopify JSON API (`/products/{handle}.json`) | Structured data, no DOM parsing needed, includes all fields |
| Image hosting | Direct links to Shopify CDN | Supabase storage mirror | Shopify CDN URLs can change; WordPress needs stable URLs |
| Social profile verification | Manual checking via browser | Site footer HTML extraction | Footer consistently has correct social links |
| URL encoding of Hebrew slugs | Manual percent-encoding | `encodeURIComponent()` or copy from sitemap | Hebrew URLs need proper encoding |

## Common Pitfalls

### Pitfall 1: Hebrew URL Encoding
**What goes wrong:** Product handles contain Hebrew characters that must be URL-encoded. Using the raw Hebrew in an `href` attribute may work in browsers but can break in WordPress processing.
**Why it happens:** WordPress may double-encode or strip non-ASCII characters.
**How to avoid:** Always use percent-encoded URLs from the sitemap or `encodeURIComponent()`. Example: `חליפת-סנדי` becomes `%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%A1%D7%A0%D7%93%D7%99`.
**Warning signs:** Broken product links in the rendered WordPress article.

### Pitfall 2: Assuming Old URL Patterns Exist
**What goes wrong:** Mapping oritmartin.com paths (`/about`, `/gallery`, `/contact`) directly to hipsterstyle.co.il.
**Why it happens:** Different platform (Wix -> Shopify), different URL conventions.
**How to avoid:** Use the verified URL map from this research. hipsterstyle uses `/pages/{slug}` for static pages and `/products/{handle}` for products. There is NO `/gallery` equivalent.
**Warning signs:** 404 errors when clicking template links.

### Pitfall 3: Product Image Size/Quality
**What goes wrong:** Using default Shopify CDN URLs without width parameter produces very large images (2000px+) that slow WordPress loading.
**Why it happens:** Shopify CDN default serves original upload size.
**How to avoid:** When downloading for Supabase upload, request a reasonable size: `?width=800` for product cards.
**Warning signs:** Slow page load, LCP issues in WordPress.

### Pitfall 4: Including Prices in Template
**What goes wrong:** Hardcoding prices (139.90 ILS etc.) in the template that become stale.
**Why it happens:** Prices change frequently in e-commerce.
**How to avoid:** Per PROD-09, no prices displayed. Link to live product pages for current pricing.
**Warning signs:** Outdated prices visible in article.

### Pitfall 5: Invented Social Links
**What goes wrong:** Adding YouTube or TikTok links that don't exist.
**Why it happens:** The old template had only Facebook and Instagram. Temptation to add more for completeness.
**How to avoid:** Per AUTH-05, only verified profiles: Facebook and Instagram. YouTube was not found for this brand -- do not add one.
**Warning signs:** Social links leading to wrong pages or 404s.

### Pitfall 6: Using oritmartin Contact Info
**What goes wrong:** Keeping the old phone number (+972587676321) or email (orit-26@netvision.net.il).
**Why it happens:** Copy-paste from existing template.
**How to avoid:** Use verified hipsterstyle contact info: phone 052-9767667 / email info@hipsterstyle.co.il.
**Warning signs:** Contact actions reach wrong business.

## Complete TBD Resolution Map

All 14 TBD items from Phase 1 migration map, resolved:

| # | TBD Item | Resolved Value | Confidence |
|---|----------|---------------|------------|
| 1 | About page URL | `https://hipsterstyle.co.il/pages/%D7%9E%D7%99-%D7%90%D7%A0%D7%97%D7%A0%D7%95` | HIGH |
| 2 | Gallery page URL | NO EQUIVALENT -- use collections page or remove | HIGH |
| 3 | Contact page URL | `https://hipsterstyle.co.il/pages/contact` | HIGH |
| 4 | Product URLs (6) | See Recommended Product Set above | HIGH |
| 5 | Phone number | `+972529767667` (mobile) / `+97235353003` (landline) | MEDIUM (from web search, not site HTML) |
| 6 | Email | `info@hipsterstyle.co.il` | MEDIUM (from web search, not site HTML) |
| 7 | Facebook profile | `https://www.facebook.com/HipsterBabyCollection` | HIGH (from site footer) |
| 8 | Instagram profile | `https://www.instagram.com/hipster.style/` | HIGH (from site footer) |
| 9 | Brand name (Hebrew) | היפסטר | HIGH |
| 10 | Brand name (English) | Hipster | HIGH |
| 11 | Author portrait | Needs new image -- founders are different people. Use brand logo or request from client. | LOW |
| 12 | Product images (6) | Shopify CDN URLs verified -- mirror to Supabase | HIGH |
| 13 | Business description (Hebrew) | "מותג אופנת ילדים ישראלי -- סטייל שונה מכולם" | MEDIUM |
| 14 | YouTube channel | NOT FOUND -- omit from template | HIGH |

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Manual verification (data discovery phase, not code) |
| Config file | N/A |
| Quick run command | Verify product URLs return 200 status |
| Full suite command | Verify all URLs + images load correctly |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PROD-01 | Products discovered from real inner pages | manual-only | Open each product URL in browser | N/A |
| PROD-02 | Products relevant to kids styling topic | manual-only | Review product selection against article topic | N/A |
| PROD-08 | Product links go to real pages | smoke | `curl -s -o /dev/null -w "%{http_code}" "https://hipsterstyle.co.il/products/%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%A1%D7%A0%D7%93%D7%99"` | N/A |
| AUTH-03 | Social links correct verified URLs | smoke | `curl -s -o /dev/null -w "%{http_code}" "https://www.facebook.com/HipsterBabyCollection"` | N/A |
| AUTH-04 | Firecrawl verifies active social profiles | manual-only | Confirmed via site footer HTML source | N/A |
| AUTH-05 | Only verified profiles added | manual-only | Audit final template for social links count (must be exactly 2) | N/A |

### Sampling Rate
- **Per task commit:** Verify product URLs return HTTP 200
- **Per wave merge:** All URLs + images load correctly
- **Phase gate:** All 6 product pages accessible, both social profiles confirmed, all images downloadable

### Wave 0 Gaps
None -- this is a data discovery phase, not a code phase. Validation is URL/data verification.

## Open Questions

1. **Author portrait image**
   - What we know: The old template uses an oritmartin author portrait on Supabase. Hipster is a different brand with different founders.
   - What's unclear: Should the article use the Hipster logo, a founder photo, or something else?
   - Recommendation: Use Hipster logo (`/cdn/shop/files/hipster_logo_black.png`) as author image. If a personal photo is needed, the user must provide one.

2. **Phone number accuracy**
   - What we know: 052-9767667 and 03-5353003 found via web search business listings, NOT from site HTML.
   - What's unclear: Which number is preferred for customer contact? Neither appears on the site's contact page directly.
   - Recommendation: Use mobile number (052-9767667) for tel: and WhatsApp links. Flag for user verification.

3. **Gallery replacement**
   - What we know: oritmartin.com had a `/gallery` page. hipsterstyle.co.il has no gallery -- it's a Shopify store with collections.
   - What's unclear: What should replace gallery links in the template?
   - Recommendation: Replace gallery links with the "All Items" collection: `https://hipsterstyle.co.il/collections/all-items` or the homepage.

4. **Brand owner name for author section**
   - What we know: Hipster was founded by two couples (Omer & Noah, Yehav & Dana). The old template had a single author name.
   - What's unclear: Should the author section say "Hipster" (brand), or list specific founder names?
   - Recommendation: Use brand name "היפסטר" rather than individual founder names. Simpler and more durable.

## Sources

### Primary (HIGH confidence)
- hipsterstyle.co.il homepage HTML -- platform identification (Shopify), navigation, social links, brand info
- hipsterstyle.co.il/sitemap.xml -- complete site structure including products, collections, pages, blogs sitemaps
- hipsterstyle.co.il/products/{handle}.json -- structured product data with images, prices, tags
- hipsterstyle.co.il/pages/contact -- contact page structure
- hipsterstyle.co.il/pages/מי-אנחנו -- about page with brand story, founders
- hipsterstyle.co.il/pages/shops -- physical store locations
- hipsterstyle.co.il/collections/passover-collection-2026 -- current seasonal products
- hipsterstyle.co.il/collections/sets-outfits -- styling-relevant products

### Secondary (MEDIUM confidence)
- Web search for contact info: phone 052-9767667, 03-5353003, email info@hipsterstyle.co.il (from Lusha business listing)
- Shopify CDN stability info (from Shopify changelog and community issues)

### Tertiary (LOW confidence)
- YouTube channel search -- negative result (no channel found), but absence of evidence is not evidence of absence

## Metadata

**Confidence breakdown:**
- Site structure/platform: HIGH -- directly verified via HTML source and Shopify JSON API
- Product data: HIGH -- verified via multiple Shopify endpoints and direct page loads
- Social profiles: HIGH -- found in site source code (footer HTML)
- Contact info: MEDIUM -- phone/email from web search business listings, not from site HTML
- YouTube absence: HIGH -- searched site source, web search, and sitemap; no references found
- Author portrait: LOW -- unclear how to handle for different brand

**Research date:** 2026-03-25
**Valid until:** 2026-04-25 (product availability may change, URLs/structure stable)
