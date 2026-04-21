---
name: Agentic SEO / AEO Audit
source: https://github.com/addyosmani/agentic-seo
category: SEO
purpose: Audit documentation and websites for Agentic Engine Optimization (AEO) — ensuring content is discoverable, parseable, and useful to AI coding agents
when_to_use: When optimizing docs/websites for AI agent consumption (not just human search), checking llms.txt, robots.txt, token budgets, and skill.md files
tags: [seo, aeo, ai-discoverability, llms-txt, robots-txt, token-budget, documentation]
---

# Agentic SEO / AEO Audit

## Purpose
Audit documentation and websites for how well AI coding agents can discover and use them. 10 checks across 5 categories, scored out of 100. CLI tool that runs locally — no API key needed.

## When To Use
- After publishing documentation or a developer website
- When AI agents aren't finding your docs correctly
- When setting up llms.txt, robots.txt, AGENTS.md, skill.md
- In CI pipelines to maintain AEO score above threshold

## How To Apply
```bash
# Quick audit of current directory
npx agentic-seo

# Audit a live URL
npx agentic-seo --url https://docs.example.com

# CI mode with threshold
npx agentic-seo --json --threshold 60

# Scaffold missing AEO files
npx agentic-seo init
```

**5 categories:**
1. Discovery (25pts): robots.txt, llms.txt, AGENTS.md
2. Content Structure (25pts): heading hierarchy, markdown availability
3. Token Economics (25pts): page token counts, meta tags
4. Capability Signaling (15pts): skill.md, agent permissions
5. UX Bridge (10pts): copy-for-AI buttons

**Priority order for new projects:**
1. Audit robots.txt (prevent agent lockout)
2. Add llms.txt
3. Measure token counts
4. Write skill.md
5. Add "Copy for AI" buttons

## Examples
- AEO audit scores 45/100 → add llms.txt, fix robots.txt to allow ClaudeBot
- CI fails below 60% → add AGENTS.md with project context

## Integration Notes
- Pure heuristic analysis — no AI, no API keys
- Supports: Next.js, Docusaurus, 11ty, Astro, Hugo, Jekyll, Gatsby, VitePress, MkDocs, Sphinx
- Programmatic API available: `import { audit } from 'agentic-seo'`
