# SKILL: OpenSEO — Open-Source Pay-As-You-Go SEO Tool
**Source:** https://github.com/every-app/open-seo
**Domain:** marketing
**Trigger:** Use when setting up a self-hosted SEO platform for keyword research, rank tracking, domain insights, backlink analysis, or site audits — as an affordable alternative to Semrush/Ahrefs.

## Summary
OpenSEO is a free, open-source, self-hostable SEO tool backed by DataForSEO's pay-per-use API. Core workflows: keyword research, rank tracking (desktop/mobile), domain insights, backlinks, and site audits. Docker or Cloudflare deployment. Roadmap includes AI/GEO/LLM visibility and MCP for Claude.

## Key Patterns
- No subscription — pay only for DataForSEO API usage
- Self-host via Docker (local) or Cloudflare (multi-device/team)
- DataForSEO credentials: base64 encode `login:password` → set as `DATAFORSEO_API_KEY`
- Key workflows: keyword research → rank tracking → domain insights → backlinks → site audit
- Roadmap: AI SEO, GEO, LLM Visibility, agentic workflows, MCP for Claude

## Usage
When user needs affordable SEO tooling without $100+/mo subscriptions. Start with Docker for local use, Cloudflare for team access.

## Code/Template
```bash
# Docker self-host
printf '%s' 'your_login:your_api_password' | base64  # → DATAFORSEO_API_KEY
echo "DATAFORSEO_API_KEY=<base64>" > .env
docker compose up -d

# Cloudflare deploy: set DATAFORSEO_API_KEY in Workers UI
```
