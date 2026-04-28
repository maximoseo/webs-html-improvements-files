# SKILL: Browser Harness
**Source:** https://github.com/browser-use/browser-harness
**Domain:** code
**Trigger:** When automating, scraping, testing, or interacting with web pages via direct browser control (CDP)

## Summary
The thinnest self-healing browser automation harness that connects directly to Chrome via CDP (~592 lines of Python). The agent writes missing helpers mid-task. No framework, no recipes — just a websocket to Chrome.

## Key Patterns
- Invoke as `browser-harness` on `$PATH` — no `cd`, no `uv run`
- `new_tab(url)` for first navigation (not `goto` — avoids clobbering user's tab)
- `screenshot()` first to understand page state, then `click(x,y)`, then screenshot again
- Coordinate clicks pass through iframes/shadow/cross-origin at compositor level
- `http_get(url)` + `ThreadPoolExecutor` for bulk static pages (no browser overhead)
- `wait_for_load()` after every `goto`; `ensure_real_tab()` for stale tabs
- Agent self-edits `helpers.py` to add missing functions mid-task
- Search `domain-skills/` before inventing new approaches
- Remote browsers via `BROWSER_USE_API_KEY` + `BU_NAME` env var for parallel sub-agents

## Usage
Set up with install.md for first-time use. Read helpers.py before every session. Use domain-skills/ for site-specific patterns. Contribute new domain skills via PRs after figuring out non-obvious site mechanics.

## Code/Template
```bash
browser-harness <<'PY'
new_tab("https://example.com")
wait_for_load()
print(page_info())
PY

# Remote browser for parallel sub-agents:
browser-harness <<'PY'
start_remote_daemon("work")
PY
BU_NAME=work browser-harness <<'PY'
new_tab("https://example.com")
print(page_info())
PY
```
