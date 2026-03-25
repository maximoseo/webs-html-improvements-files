# URL Verification Log -- Phase 2

**Date:** 2026-03-25
**Verified by:** Automated curl checks (HTTP status codes)

## Product Page URLs

| Product | URL | Status |
|---------|-----|--------|
| Sandy | https://hipsterstyle.co.il/products/%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%A1%D7%A0%D7%93%D7%99 | 200 |
| Henry | https://hipsterstyle.co.il/products/%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%94%D7%A0%D7%A8%D7%99 | 200 |
| Nino | https://hipsterstyle.co.il/products/%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%A0%D7%99%D7%A0%D7%95 | 200 |
| Mila | https://hipsterstyle.co.il/products/%D7%97%D7%9C%D7%99%D7%A4%D7%AA-%D7%9E%D7%99%D7%9C%D7%94 | 200 |
| Eli | https://hipsterstyle.co.il/products/%D7%98%D7%99%D7%A9%D7%A8%D7%98-%D7%90%D7%9C%D7%99 | 200 |
| Shay | https://hipsterstyle.co.il/products/%D7%92-%D7%99%D7%A0%D7%A1-%D7%A9%D7%99%D7%99 | 200 |

## Supabase Image URLs

| Image | URL | Status |
|-------|-----|--------|
| product-sandy.jpg | https://zqcnyllsfwnssnuduvmj.supabase.co/storage/v1/object/public/article-assets/hipsterstyle/product-sandy.jpg | 200 |
| product-henry.jpg | https://zqcnyllsfwnssnuduvmj.supabase.co/storage/v1/object/public/article-assets/hipsterstyle/product-henry.jpg | 200 |
| product-nino.jpg | https://zqcnyllsfwnssnuduvmj.supabase.co/storage/v1/object/public/article-assets/hipsterstyle/product-nino.jpg | 200 |
| product-mila.jpg | https://zqcnyllsfwnssnuduvmj.supabase.co/storage/v1/object/public/article-assets/hipsterstyle/product-mila.jpg | 200 |
| product-eli.jpg | https://zqcnyllsfwnssnuduvmj.supabase.co/storage/v1/object/public/article-assets/hipsterstyle/product-eli.jpg | 200 |
| product-shay.jpg | https://zqcnyllsfwnssnuduvmj.supabase.co/storage/v1/object/public/article-assets/hipsterstyle/product-shay.jpg | 200 |

## Social Profile URLs

| Platform | URL | Status | Notes |
|----------|-----|--------|-------|
| Facebook | https://www.facebook.com/HipsterBabyCollection | 200 | HEAD request returns 200; GET may return 302 (login redirect) -- page exists |
| Instagram | https://www.instagram.com/hipster.style/ | 200 | Verified with browser user-agent |
| YouTube | NOT FOUND | N/A | No channel exists for this brand -- confirmed via site crawl and web search |
| TikTok | NOT FOUND | N/A | Not referenced anywhere on hipsterstyle.co.il |

## Site Page URLs

| Page | URL | Status |
|------|-----|--------|
| Homepage | https://hipsterstyle.co.il/ | 200 |
| About | https://hipsterstyle.co.il/pages/%D7%9E%D7%99-%D7%90%D7%A0%D7%97%D7%A0%D7%95 | 200 |
| Contact | https://hipsterstyle.co.il/pages/contact | 200 |

## Summary

- Total URLs verified: 17 (6 product pages + 6 Supabase images + 2 social profiles + 3 site pages)
- All passing: Yes
- Issues: None
- Supabase upload: Completed successfully (6/6 images uploaded via REST API)
- Social profiles: Exactly 2 confirmed (Facebook + Instagram). YouTube and TikTok do not exist for this brand.
