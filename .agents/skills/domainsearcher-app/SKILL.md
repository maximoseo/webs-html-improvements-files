# SKILL: Domain Searcher - AI-Scored Domain Name Finder
**Source:** https://github.com/vasilytrofimchuk/domainsearcher-app
**Domain:** code
**Trigger:** When building domain name search tools, implementing multi-signal domain scoring systems, or creating AI-assisted brand naming tools

## Summary
Static HTML+JS domain search tool that generates 60 candidates, checks real-time availability via RDAP+DNS-over-HTTPS two-stage verification, and scores each on 6 dimensions (Length, Pronounceability, Memorability, Brandability, Zone, AI Fit) with adjustable weights.

## Key Patterns
- Two-stage availability check: RDAP (rdap.org) + Cloudflare DoH (1.1.1.1) to catch false negatives
- Single AI call scores PRO+MEM+BRD+FIT simultaneously (Groq/OpenAI/Anthropic)
- Adjustable dimension weights (FIT=5 default, others=1-2)
- Zero backend: CORS-enabled APIs, runs in browser, localStorage persistence
- Bundled Groq key for zero-setup; swap providers via env

## Usage
```bash
npx serve .  # or: python3 -m http.server 8080
# Must use HTTP server (not file://) for ES modules
```

## Code/Template
```javascript
// Two-stage availability: RDAP + DNS-over-HTTPS
// Stage 1: fetch(`https://rdap.org/domain/${domain}`) - 200=taken, 404=unconfirmed
// Stage 2: Cloudflare 1.1.1.1 DoH - NXDOMAIN=available, NS/SOA=taken
// AI scoring: single call for PRO, MEM, BRD, FIT dimensions
```
