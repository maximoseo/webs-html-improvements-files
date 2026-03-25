# Site Reference Migration Map

**Audit date:** 2026-03-25
**Purpose:** Document every oritmartin.com, Orit Martin, and non-hipsterstyle reference across all three baseline files. Map each to the required hipsterstyle.co.il equivalent.

---

## 1. Summary

| File | Lines with oritmartin | Lines with "Orit" (case-insensitive) | wixstatic URLs | Total Items Needing Replacement |
|------|----------------------|--------------------------------------|----------------|--------------------------------|
| HTML Template (321 lines) | 24 | 27 | 6 | 33 unique replacement points |
| N8N Prompt TXT (330 lines) | 9 | 18 | 0 | 18 unique replacement points |
| N8N Workflow JSON (675+ lines) | 3 | 7 | 0 | 7 unique replacement points |
| **TOTAL** | **36** | **52** | **6** | **58 replacement points** |

**Unique URLs requiring replacement:** 12 distinct oritmartin.com URLs + 6 wixstatic.com URLs + 1 Supabase URL with /oritmartin/ path + 1 netvision email + 1 phone number + 2 social profile URLs = **23 unique values**

---

## 2. HTML Template References

**File:** `wp-n8n-html-design-improver/Improved_HTML_Template-claude-code-2026-03-25.html`

### URL References

| Line | Current Value | Category | Required New Value |
|------|--------------|----------|-------------------|
| 16 | `https://www.oritmartin.com/about` | About page URL | `https://www.hipsterstyle.co.il/about` -- TBD verify path exists in Phase 2 |
| 53, 58 | `https://www.oritmartin.com/product-page/%D7%A2%D7%A5-%D7%94%D7%97%D7%99%D7%99%D7%9D-3` | Product URL (Tree of Life) | TBD -- discover hipsterstyle product URLs via Firecrawl in Phase 2 |
| 62, 67 | `https://www.oritmartin.com/product-page/%D7%90%D7%A0%D7%90-%D7%91%D7%9B%D7%95%D7%97` | Product URL (Ana BeKoach) | TBD -- discover via Firecrawl in Phase 2 |
| 71, 76 | `https://www.oritmartin.com/product-page/%D7%96%D7%95%D7%94%D7%A8-%D7%9E%D7%A2%D7%95%D7%9C%D7%9D-%D7%A2%D7%9C%D7%99%D7%95%D7%9F` | Product URL (Zohar) | TBD -- discover via Firecrawl in Phase 2 |
| 80, 85 | `https://www.oritmartin.com/product-page/%D7%A0%D7%99%D7%A6%D7%95%D7%A6%D7%95%D7%AA-1` | Product URL (Sparks) | TBD -- discover via Firecrawl in Phase 2 |
| 89, 94 | `https://www.oritmartin.com/product-page/%D7%A2%D7%95%D7%9C%D7%9E%D7%95%D7%AA-%D7%A2%D7%9C%D7%99%D7%95%D7%A0%D7%99%D7%9D` | Product URL (Upper Worlds) | TBD -- discover via Firecrawl in Phase 2 |
| 98, 103 | `https://www.oritmartin.com/product-page/%D7%A9%D7%A2%D7%A8-%D7%9C%D7%90%D7%99%D7%A0%D7%A1%D7%95%D7%A3-1` | Product URL (Gate to Infinity) | TBD -- discover via Firecrawl in Phase 2 |
| 122 | `https://www.oritmartin.com/sculptures-1/10-%D7%A1%D7%A4%D7%99%D7%A8%D7%95%D7%AA` | Gallery subpage URL (10 Sefirot) | TBD -- discover via Firecrawl in Phase 2 |
| 175 | `https://www.oritmartin.com/product-page/%D7%A0%D7%99%D7%A6%D7%95%D7%A6%D7%95%D7%AA-1` | Inline text link to Sparks | TBD -- same as product URL above |
| 175 | `https://www.oritmartin.com/product-page/%D7%96%D7%95%D7%94%D7%A8-%D7%9E%D7%A2%D7%95%D7%9C%D7%9D-%D7%A2%D7%9C%D7%99%D7%95%D7%9F` | Inline text link to Zohar | TBD -- same as product URL above |
| 185 | `https://www.oritmartin.com/gallery` | Gallery page URL | `https://www.hipsterstyle.co.il/gallery` -- TBD verify path in Phase 2 |
| 195 | `https://www.oritmartin.com/contact` | Contact page URL (CTA banner) | `https://www.hipsterstyle.co.il/contact` -- TBD verify path in Phase 2 |
| 218 | `https://www.oritmartin.com/gallery` | Gallery page URL (CTA banner) | Same as above |
| 284 | `https://www.oritmartin.com/gallery` | Gallery page URL (final CTA) | Same as above |
| 286 | `https://www.oritmartin.com/contact` | Contact page URL (floating button) | Same as above |
| 300 | `https://www.oritmartin.com/about` | About page URL (author section) | Same as above |

### Image References

| Line | Current Value | Category | Required New Value |
|------|--------------|----------|-------------------|
| 54 | `https://static.wixstatic.com/media/5c3fca_031245f57bf64771b10a90310bca1172~mv2.jpg/...` | Product image (Tree of Life) | Upload to Supabase, replace with stable URL |
| 63 | `https://static.wixstatic.com/media/5c3fca_575ef3b008ff4e0a975d6a0771b65a3c~mv2.png/...` | Product image (Ana BeKoach) | Upload to Supabase, replace with stable URL |
| 72 | `https://static.wixstatic.com/media/5c3fca_8493902df17d48189627ba93397d75c6~mv2.png/...` | Product image (Zohar) | Upload to Supabase, replace with stable URL |
| 81 | `https://static.wixstatic.com/media/5c3fca_97bada750959424e897d1ff18ad49db1~mv2.jpg/...` | Product image (Sparks) | Upload to Supabase, replace with stable URL |
| 90 | `https://static.wixstatic.com/media/5c3fca_54e6a665afb8438a8279816596d63502~mv2.jpg/...` | Product image (Upper Worlds) | Upload to Supabase, replace with stable URL |
| 99 | `https://static.wixstatic.com/media/5c3fca_df2eeab07ffd43ee8b1554cb46ccc131~mv2.jpg/...` | Product image (Gate to Infinity) | Upload to Supabase, replace with stable URL |
| 293 | `https://zqcnyllsfwnssnuduvmj.supabase.co/storage/v1/object/public/article-assets/oritmartin/author-portrait.jpeg` | Author portrait (Supabase) | Update path from `/oritmartin/` to `/hipsterstyle/` or keep if same Supabase bucket |

### Contact References

| Line | Current Value | Category | Required New Value |
|------|--------------|----------|-------------------|
| 219 | `tel:+972587676321` | Phone (tel: link) | TBD -- verify hipsterstyle phone in Phase 2 |
| 298 | `tel:+972587676321` | Phone (author section) | Same as above |
| 299 | `mailto:orit-26@netvision.net.il` | Email | TBD -- verify hipsterstyle email in Phase 2 |
| 308 | `https://wa.me/972587676321` | WhatsApp (floating button) | TBD -- verify hipsterstyle WhatsApp in Phase 2 |
| 316 | `+972-58-767-6321` | Phone (JSON-LD LocalBusiness) | Same as above |

### Social Profile References

| Line | Current Value | Category | Required New Value |
|------|--------------|----------|-------------------|
| 303 | `https://www.facebook.com/%D7%90%D7%95%D7%A8%D7%99%D7%AA-%D7%9E%D7%A8%D7%98%D7%99%D7%9F-%D7%A6%D7%99%D7%99%D7%A8%D7%AA-orit-martin-1430061693883873/` | Facebook profile | TBD -- discover hipsterstyle Facebook in Phase 2 |
| 304 | `https://www.instagram.com/orit_martin_spiritual_art/` | Instagram profile | TBD -- discover hipsterstyle Instagram in Phase 2 |

### Brand Name / Text References

| Line | Current Value | Category | Required New Value |
|------|--------------|----------|-------------------|
| 16, 50, 113, 185, 201, 282 | "אורית מרטין" (Hebrew text in body paragraphs) | Author name (Hebrew) | TBD -- hipsterstyle brand owner name or brand name |
| 54, 63, 72, 81, 90, 99 | "מאת אורית מרטין" in alt attributes | Image alt text (Hebrew) | Update to hipsterstyle brand |
| 284 | "לצפייה בגלריה של אורית מרטין" | CTA button text | Update to hipsterstyle gallery name |
| 286 | "צרו קשר עם אורית מרטין" | aria-label text | Update to hipsterstyle brand |
| 293 | "אורית מרטין, אמנית רוחנית קבלית מירושלים" | Image alt text | Update to hipsterstyle brand |
| 295 | "אורית מרטין, אמנות רוחנית וקבלית מירושלים" | Author subtitle text | Update to hipsterstyle brand |
| 296 | "אורית מרטין יוצרת מתוך חיבור..." | Author bio text | Rewrite for hipsterstyle brand |
| 300 | "עוד על אורית" | Button text | Update to hipsterstyle brand |

### JSON-LD / Structured Data References

| Line | Current Value | Category | Required New Value |
|------|--------------|----------|-------------------|
| 313 | `"name":"אורית מרטין"`, `"url":"https://www.oritmartin.com/about"`, `"name":"oritmartin.com"`, `"url":"https://www.oritmartin.com"` | Article schema author + publisher | Update all to hipsterstyle brand and URLs |
| 316 | `"name":"גלריה אורית מרטין"`, `"url":"https://www.oritmartin.com/gallery"`, `"telephone":"+972-58-767-6321"` | LocalBusiness schema | Update all to hipsterstyle data |
| 313 | Supabase URL with `/oritmartin/` path in author image | Schema author image | Update path segment |

---

## 3. N8N Prompt References

**File:** `wp-n8n-html-design-improver/Improved_N8N_Prompt-claude-code-2026-03-25.txt`

| Line | Current Value | Category | Required New Value |
|------|--------------|----------|-------------------|
| 1 | "ORIT MARTIN ARTICLE SYSTEM" | Document title | "HIPSTERSTYLE ARTICLE SYSTEM" |
| 5 | "Orit Martin's WordPress article pipeline" | Role description | "HipsterStyle's WordPress article pipeline" |
| 59 | `https://www.oritmartin.com/` | Main website URL | `https://www.hipsterstyle.co.il/` |
| 60 | `https://www.oritmartin.com/about` | About page | `https://www.hipsterstyle.co.il/about` -- TBD verify |
| 61 | `https://www.oritmartin.com/gallery` | Gallery page | `https://www.hipsterstyle.co.il/gallery` -- TBD verify |
| 62 | `https://www.oritmartin.com/contact` | Contact page | `https://www.hipsterstyle.co.il/contact` -- TBD verify |
| 63 | `+972587676321` | Phone number | TBD -- hipsterstyle phone |
| 64 | `orit-26@netvision.net.il` | Email | TBD -- hipsterstyle email |
| 65 | `https://www.facebook.com/...orit-martin...` | Facebook profile | TBD -- hipsterstyle Facebook |
| 66 | `https://www.instagram.com/orit_martin_spiritual_art/` | Instagram profile | TBD -- hipsterstyle Instagram |
| 67 | `https://...supabase.co/.../oritmartin/author-portrait.jpeg` | Author portrait URL | Update Supabase path to hipsterstyle |
| 107 | "Orit Martin's real gallery" | Instructions text | "HipsterStyle's gallery" |
| 208 | "contacting Orit (link to https://www.oritmartin.com/contact)" | CTA instruction | Update URL and name |
| 240 | "real internal Orit Martin destination" | CTA instruction | "real internal HipsterStyle destination" |
| 250 | `https://www.oritmartin.com/contact` | Floating button URL | `https://www.hipsterstyle.co.il/contact` |
| 257 | `https://...supabase.co/.../oritmartin/author-portrait.jpeg` | Author portrait (duplicate ref) | Same Supabase path update |
| 259 | "Orit Martin's name" | Author section instruction | Update to hipsterstyle brand name |
| 260 | `tel:+972587676321`, `mailto:orit-26@netvision.net.il` | Contact buttons | TBD -- hipsterstyle contacts |
| 261 | `https://www.oritmartin.com/about` | About button URL | `https://www.hipsterstyle.co.il/about` |

---

## 4. N8N Workflow References

**File:** `wp-n8n-html-design-improver/Improved_N8N_Workflow-claude-code-2026-03-25.json`

| Line | Current Value | Category | Required New Value |
|------|--------------|----------|-------------------|
| 51 | `siteUrl: 'https://www.oritmartin.com/'` (Prepare Input node) | Default site URL | `'https://www.hipsterstyle.co.il/'` |
| 51 | `businessName: 'אורית מרטין, אמנות רוחנית וקבלית מירושלים'` | Business name (Hebrew) | TBD -- hipsterstyle brand name |
| 51 | `businessDescription: 'גלריה ליצירות רוחניות וקבליות במהדורות מוגבלות, בהר נוף ירושלים.'` | Business description | TBD -- hipsterstyle description |
| 51 | `aboutUrl: 'https://www.oritmartin.com/about'` (verifiedLinks) | About URL | `'https://www.hipsterstyle.co.il/about'` |
| 51 | `galleryUrl: 'https://www.oritmartin.com/gallery'` (verifiedLinks) | Gallery URL | `'https://www.hipsterstyle.co.il/gallery'` |
| 51 | `phone: '+972587676321'` (verifiedLinks) | Phone | TBD -- hipsterstyle phone |
| 51 | `email: 'orit-26@netvision.net.il'` (verifiedLinks) | Email | TBD -- hipsterstyle email |
| 51 | `facebookUrl: 'https://www.facebook.com/...orit-martin...'` (verifiedLinks) | Facebook URL | TBD -- hipsterstyle Facebook |
| 261 | `ORIT MARTIN WORDPRESS HTML RENDERER` (Build Final HTML Prompt) | Prompt header in embedded string | "HIPSTERSTYLE WORDPRESS HTML RENDERER" |
| 261 | Multiple oritmartin.com URLs embedded in prompt string | All site URLs | Replace all with hipsterstyle.co.il equivalents |
| 261 | `orit_martin_spiritual_art` Instagram handle | Instagram | TBD -- hipsterstyle Instagram |
| 261 | `oritmartin/author-portrait.jpeg` Supabase path | Author image path | Update path segment |
| 261 | "Orit" name references (3x in prompt string) | Brand name | "HipsterStyle" or owner name |
| 657 | `"templateId": "improved-content-pipeline-oritmartin-claude-code-2026-03-25"` | Workflow template ID | Update to hipsterstyle slug |
| 675 | `"name": "orit-martin"` | Workflow tag name | `"name": "hipsterstyle"` |

---

## 5. Reference Categories Summary

| Category | Current Value | New Value | Count Across All Files |
|----------|--------------|-----------|----------------------|
| Main website URL | `https://www.oritmartin.com/` | `https://www.hipsterstyle.co.il/` | ~15 |
| About page | `https://www.oritmartin.com/about` | `https://www.hipsterstyle.co.il/about` -- TBD verify path | ~6 |
| Gallery page | `https://www.oritmartin.com/gallery` | `https://www.hipsterstyle.co.il/gallery` -- TBD verify path | ~7 |
| Contact page | `https://www.oritmartin.com/contact` | `https://www.hipsterstyle.co.il/contact` -- TBD verify path | ~6 |
| Product page URLs (6 unique) | `https://www.oritmartin.com/product-page/...` | TBD -- Firecrawl discovery in Phase 2 | ~14 (each product appears 2x in template) |
| Gallery subpage | `https://www.oritmartin.com/sculptures-1/10-...` | TBD -- Firecrawl discovery in Phase 2 | 1 |
| Phone number | `+972587676321` | TBD -- verify hipsterstyle phone | ~6 (tel:, wa.me, JSON-LD) |
| Email | `orit-26@netvision.net.il` | TBD -- verify hipsterstyle email | ~4 |
| Facebook profile | `facebook.com/...orit-martin...` | TBD -- discover hipsterstyle Facebook | ~4 |
| Instagram profile | `instagram.com/orit_martin_spiritual_art/` | TBD -- discover hipsterstyle Instagram | ~4 |
| Author portrait URL | `supabase.co/.../oritmartin/author-portrait.jpeg` | Update Supabase path or upload new image | ~4 |
| Product images (wixstatic) | 6 unique `static.wixstatic.com` URLs | Upload to Supabase, get stable URLs | 6 |
| Author name (English) | "Orit Martin" | TBD -- hipsterstyle brand owner or brand name | ~8 |
| Author name (Hebrew) | "אורית מרטין" | TBD -- hipsterstyle brand name (Hebrew) | ~10 |
| Business name | "oritmartin.com" / "גלריה אורית מרטין" | "hipsterstyle.co.il" / TBD Hebrew name | ~4 |
| Workflow name/tags | `"orit-martin"`, `"oritmartin"` in template ID | `"hipsterstyle"` | 2 |

---

## 6. Phase 2 Dependencies

Every replacement value marked "TBD" that requires Firecrawl discovery or manual verification.

| Dependency | Discovery Method | Blocking? |
|-----------|-----------------|-----------|
| hipsterstyle.co.il About page URL path | Firecrawl crawl of hipsterstyle.co.il | YES -- needed for template, prompt, workflow |
| hipsterstyle.co.il Gallery page URL path | Firecrawl crawl | YES |
| hipsterstyle.co.il Contact page URL path | Firecrawl crawl | YES |
| hipsterstyle.co.il product page URLs (6 products) | Firecrawl crawl of inner pages | YES -- product cards link to these |
| hipsterstyle.co.il phone number | Firecrawl crawl of contact page or manual | YES -- used in tel: links, WhatsApp, JSON-LD |
| hipsterstyle.co.il email address | Firecrawl crawl or manual | YES -- used in mailto: link |
| hipsterstyle.co.il Facebook page URL | Firecrawl social discovery or manual | YES -- author section social links |
| hipsterstyle.co.il Instagram profile URL | Firecrawl social discovery or manual | YES -- author section social links |
| hipsterstyle brand owner name (Hebrew) | Manual verification | YES -- 10+ text references |
| hipsterstyle brand owner name (English) | Manual verification | YES -- 8+ references |
| hipsterstyle author portrait image | Manual provision or reuse Supabase | MEDIUM -- can reuse existing if same person |
| hipsterstyle product images | Firecrawl image extraction from product pages | YES -- replace 6 wixstatic URLs |
| hipsterstyle business description (Hebrew) | Manual or derived from crawl | LOW -- only in workflow JSON |
| hipsterstyle YouTube channel (if any) | Firecrawl social discovery | LOW -- not currently referenced |

**Total TBD items requiring Phase 2 resolution: 14**

**Critical path items (block template rebuild):**
1. Site URL structure (about, gallery, contact paths)
2. Product page URLs (6 products)
3. Contact info (phone, email)
4. Social profiles (Facebook, Instagram)
5. Brand/author name (Hebrew + English)
6. Product images (Supabase upload)
