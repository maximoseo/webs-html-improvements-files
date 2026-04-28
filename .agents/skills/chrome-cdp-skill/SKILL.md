# SKILL: chrome-cdp — Live Chrome Session Browser Automation
**Source:** https://github.com/pasky/chrome-cdp-skill
**Domain:** agent-tools
**Trigger:** Use when an AI agent needs to interact with the user's live, already-logged-in Chrome session — reading Gmail, GitHub, internal tools — without relaunching a fresh browser.

## Summary
chrome-cdp connects AI agents to the user's existing Chrome session via Chrome DevTools Protocol. Holds persistent daemon connections per tab (no repeated Allow prompts), handles 100+ tabs reliably, and avoids Puppeteer timeout issues.

## Key Patterns
- Enable once: `chrome://inspect/#remote-debugging` toggle
- `cdp.mjs list` — list all open tabs with targetIds
- `cdp.mjs snap <target>` — accessibility tree snapshot (semantic, compact)
- `cdp.mjs shot <target>` — screenshot
- `cdp.mjs click <target> "selector"` / `type <target> "text"` — interaction
- `cdp.mjs nav <target> https://...` — navigate and wait for load
- `cdp.mjs eval <target> "expr"` — execute JS in page context
- Daemons auto-exit after 20 min inactivity

## Usage
When agent needs to act on user's logged-in web sessions. Much more reliable than fresh-browser automation for authenticated workflows.

## Code/Template
```bash
# Install (pi skill)
pi install git:github.com/pasky/chrome-cdp-skill@v1.0.1

# Usage
scripts/cdp.mjs list
scripts/cdp.mjs snap abc123
scripts/cdp.mjs click abc123 "button.submit"
scripts/cdp.mjs type abc123 "Hello World"
scripts/cdp.mjs loadall abc123 ".load-more"
```
