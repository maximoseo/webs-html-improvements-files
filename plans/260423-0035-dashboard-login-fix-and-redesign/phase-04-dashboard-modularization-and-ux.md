# Phase 04 — Dashboard Modularization + UX

## Overview
- **Priority:** P1 (do immediately after P0 login work)
- **Status:** pending
- Break up the 15,659-line `index.html`. Apply tokens to nav, Prompt Studio, Keyword Research. Fix expand/collapse + modal traps.

## Module plan
```
webs-html-improvements-files-clean/
├── index.html                 (thin shell, <300 lines: skeleton, loads partials)
├── static/
│   ├── tokens.css
│   ├── base.css               reset + typography + containers
│   ├── components/
│   │   ├── button.css
│   │   ├── card.css
│   │   ├── nav.css
│   │   ├── modal.css
│   │   ├── table.css
│   │   └── form.css
│   └── features/
│       ├── prompt-studio.css
│       ├── keyword-research.css
│       └── radar.css
└── js/
    ├── api.js                 authedFetch + 401 interceptor
    ├── auth.js                me() + logout() + token refresh
    ├── router.js              hash-based routing
    ├── nav.js
    ├── features/
    │   ├── prompt-studio.js
    │   ├── keyword-research.js
    │   ├── radar.js
    │   └── comments.js
    └── utils/
        ├── modal.js
        ├── toast.js
        └── format.js
```

## Main nav redesign — spec
- Top bar, 56px, sticky, `--bg-1` background, `--line` bottom border.
- Logo + sections + user menu (see master report §4).
- Overflow to `⋯` menu at < 1024px.
- Active tab = 2px `--accent` bottom border, color `--fg-1`.
- Hover = `--bg-2` background, color `--fg-1`.

## Prompt Studio — spec
- Convert modal → dedicated route `/prompt-studio`.
- Sticky top bar with actions always visible.
- 3-pane: history | editor | preview.
- Textarea has autosize up to 60vh then scroll.
- Deploy button states: idle / confirming (double-click) / uploading (progress) / done (checkmark, auto-reset in 3s) / error (toast).
- Preview iframe has device toggle: mobile 375 / tablet 768 / desktop 1280.
- Comments panel: right drawer, collapsible, resolved comments hidden by default.

## Keyword Research — spec
- Sticky filter bar (domain / intent / volume / status) with counts.
- Data table with virtualized rows.
- Row actions: primary button visible, secondary in `⋮` menu.
- Batch select → sticky action bar at bottom ("Deploy 12 selected" / "Export CSV" / "Add to prompt").
- Empty state: illustration + CTA to run new research.
- Loading: shimmer rows.
- Error: inline banner with retry.

## Expand/collapse fix
- Switch from `max-height` animation to `<details>` with `::details-content` OR `height: auto` with `interpolate-size: allow-keywords` (modern browsers).
- Always keep a **sticky footer action bar** outside the collapsible area.
- If section expands past viewport, scroll container (`overflow-y: auto; max-height: calc(100vh - var(--nav-h) - 120px)`).

## Global
- Add `authedFetch(url, opts)` to `js/api.js`:
  ```js
  export async function authedFetch(url, opts = {}) {
    const res = await fetch(url, { credentials: 'same-origin', ...opts });
    if (res.status === 401) {
      const next = encodeURIComponent(location.pathname + location.search);
      location.replace(`/login?next=${next}`);
      throw new Error('unauthorized');
    }
    return res;
  }
  ```
- Migrate every `fetch(` in the dashboard to `authedFetch(` — single grep/sed.
- Add skeleton loaders for all async panels.
- Add global toast component for success/error.

## Implementation order
1. Extract tokens + base CSS; link from `index.html`.
2. Extract nav CSS + JS; replace inline.
3. Introduce `authedFetch`; migrate all API calls.
4. Extract Prompt Studio as route, apply spec.
5. Extract Keyword Research, apply spec.
6. Fix expand/collapse pattern globally.
7. Add empty/loading/error states.
8. Lighthouse + a11y regression.

## Todo
- [ ] Split index.html into partials.
- [ ] Create tokens/base/components CSS.
- [ ] authedFetch migration (greppable regex).
- [ ] Nav redesign.
- [ ] Prompt Studio page.
- [ ] Keyword Research table.
- [ ] Expand/collapse refactor.
- [ ] Skeleton/empty/error states.
- [ ] Mobile pass (360–428px).
- [ ] Tablet pass (768–1024px).

## Success criteria
- index.html < 300 lines.
- No single CSS/JS file >400 lines.
- All fetches route through `authedFetch`.
- Actions stay visible regardless of section height.
- No regressions in radar, comments, deploy.
