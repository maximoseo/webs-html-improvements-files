# SKILL: OpenCLI
**Source:** https://github.com/jackwener/opencli
**Domain:** code
**Trigger:** When an AI agent needs to automate websites, operate browser sessions, or turn web APIs into deterministic CLI commands

## Summary
OpenCLI turns websites, browser sessions, Electron apps, and local tools into deterministic CLI interfaces for AI agents. It has 90+ pre-built adapters (Bilibili, Reddit, HackerNews, Twitter, etc.) and a skill-based browser automation layer for agents.

## Key Patterns
- `opencli browser open <url>` — navigate; `opencli browser state` — read DOM snapshot
- `opencli browser click/type/select/wait/get/screenshot` — interact with pages
- `opencli-adapter-author` skill — agents author new site adapters end-to-end
- Browser reuses logged-in Chrome session; zero LLM cost at runtime
- Pattern: recon → classify (SPA/SSR/JSONP) → discover endpoint → decode fields → verify

## Usage
```bash
npm install -g @jackwener/opencli
# Install browser extension from GitHub Releases
opencli doctor    # verify setup
npx skills add jackwener/opencli --skill opencli-adapter-author
```

## Code/Template
```bash
# AI agent browser automation (via agent skill)
opencli browser open https://example.com
opencli browser state           # DOM snapshot
opencli browser click --sel "button.submit"
opencli browser get --sel "#result"
# Built-in adapters
opencli hackernews top --limit 5
opencli reddit hot --limit 10
```
