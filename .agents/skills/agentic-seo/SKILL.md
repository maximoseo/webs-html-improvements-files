---
name: Agentic SEO (AEO/GEO Audit)
source: https://github.com/addyosmani/agentic-seo
category: SEO
purpose: Audit sites for AI Engine Optimization — robots.txt, llms.txt, AGENTS.md, skill.md, token budget, structured data
when_to_use: When optimizing a site for AI crawlers (ChatGPT, Claude, Perplexity) or checking AEO/GEO readiness
tags: [seo, aeo, geo, llms.txt, robots.txt, ai-search, structured-data]
---
# Agentic SEO (AEO/GEO Audit)

## Purpose
Audit websites for Agentic Engine Optimization — ensuring AI agents can discover, index, and cite the site correctly.

## When To Use
- Optimizing sites for AI crawler visibility
- Adding llms.txt, AGENTS.md, or skill.md to a domain
- Checking token budget, robots.txt agent permissions, structured data
- GEO (Generative Engine Optimization) audits

## How To Apply
Run `npx agentic-seo <url>` — performs 10 checks across 5 categories:
1. **Crawlability** — robots.txt agent permissions, sitemap
2. **Discoverability** — llms.txt, AGENTS.md present
3. **Structured Data** — JSON-LD, schema.org types
4. **Token Budget** — page size, content density
5. **Citation Signals** — authorship, canonical, hreflang

Scoring: 0-100 per category. Output: JSON report + recommendations.

## Examples
```bash
npx agentic-seo https://example.com
npx agentic-seo https://galoz.co.il --format json
```

## Integration Notes
- Pairs with `geo-technical`, `geo-schema`, `geo-ai-visibility` skills
- Use before launching any new domain or after major redesigns
- llms.txt should list site purpose, key pages, and preferred citation format
