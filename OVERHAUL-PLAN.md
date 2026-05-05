# HTML Redesign Dashboard Overhaul Plan

## Document purpose

This plan is written for coding agents working in the current repository. It is based on the checked-in source, the live deployment at `https://html-redesign-dashboard.maximo-seo.ai/`, and the existing design audit in `docs/audits/html-redesign-dashboard-design-audit.md`.

The goal is to explain why the live dashboard currently looks wrong, identify the real source-of-truth files, and define an implementation order that can be executed in small PR-able units without guesswork.

---

## Repo reality summary

| Area | Current state | Implication |
|---|---|---|
| Main dashboard shell | `index.html` at repo root, ~1.35 MB, monolithic | This is the primary production dashboard implementation described by project rules and heavily covered by tests. |
| Alternate dashboard UI | `dashboard/index.html`, `dashboard/login.html`, `dashboard/styles/*` | This is a second UI implementation with separate styling tokens and login pages. It is not aligned with the main `index.html` architecture. |
| Auth login page | `login-page.html` at repo root | This is a third login implementation, visually more polished than `dashboard/login.html`. |
| Server entrypoint | `server.py` | Checked-in code currently routes `/` to `dashboard/index.html` and `/login` to `login-page.html`. |
| Deployment | `Dockerfile` runs `python server.py` | Production behavior should match `server.py`, but live evidence shows a mismatch. |
| Existing regression suite | `tests/` | Most tests assume the monolithic root `index.html` remains the main dashboard UI. |

---

# Part 1: Root Cause Analysis

## 1.1 Primary diagnosis

The live experience looks broken/bad because the repository currently contains **multiple competing dashboard implementations**, and the live deployment appears to be serving an **older or different routing behavior than the checked-in `server.py`**.

The result is:

1. Unauthenticated users land on a lightweight login page built from the `dashboard/` implementation.
2. That page references `/styles/design-tokens.css` and `/styles/components.css`.
3. Those asset URLs return `404` in production.
4. Therefore the login page renders almost completely unstyled.
5. Meanwhile, the real monolithic dashboard UI in root `index.html` is visually richer, but it is not the obvious active source of truth for the entry flow.

## 1.2 Evidence chain

### Source-code evidence

- `server.py` currently routes:
  - `/login` and `/login.html` → `login-page.html`
  - `/` → `dashboard/index.html`
- `dashboard/index.html` and `dashboard/login.html` both link:
  - `./styles/design-tokens.css`
  - `./styles/components.css`
- Root `index.html` contains its own large inline styling system and does **not** depend on external `dashboard/styles/*`.
- `tests/` overwhelmingly validate the root `index.html`, not `dashboard/index.html`.

### Live evidence

- Live `/` and `/login` return HTML matching `dashboard/login.html`, not `login-page.html`.
- Live `/styles/design-tokens.css` returns `404`.
- Existing audit doc `docs/audits/html-redesign-dashboard-design-audit.md` describes a much richer authenticated dashboard than the currently visible unauthenticated page, which means the live "broken" perception is happening at least partly before auth.

## 1.3 Root causes by layer

### A. Deployment/source mismatch

**Problem:** Production behavior does not match the checked-in route mapping in `server.py`.

**Likely causes:**

- Render is serving a stale image/container.
- The deployed branch/commit is not the repository state currently checked out on `main`.
- A prior container/image layer still exposes `dashboard/login.html` routing behavior.
- There may be deployment drift outside Git, despite the Dockerfile specifying `server.py`.

**Why this matters:** Until deployment/source drift is resolved, UI fixes may be applied to the wrong files and never appear live.

### B. Duplicate frontend implementations

There are at least three overlapping UI entrypoints:

1. `index.html`
2. `dashboard/index.html`
3. `login-page.html` / `dashboard/login.html`

This is the biggest structural problem in the repo's frontend.

**Impact:**

- Visual systems diverge.
- Fixes get applied to the wrong file.
- Routing behavior becomes hard to reason about.
- Tests only cover one implementation path well.

### C. Missing static asset delivery for the active login page

The live login page requests `/styles/design-tokens.css` and `/styles/components.css`, but those URLs 404 in production.

**Possible reasons:**

- The active server in production does not route `/styles/*` to `dashboard/styles/*`.
- Static fallback behavior is different in production than in the checked-in `server.py`.
- A stale deployment is serving old HTML without the corresponding static route support.

**Immediate effect:** Unstyled page, default browser typography, weak hierarchy, "broken" first impression.

### D. Mixed visual systems inside the authenticated app

Even beyond the broken login page, the existing audit shows the authenticated dashboard already suffers from:

- desktop-only nav polish
- dense pages
- long settings page
- inconsistent surface treatments
- too many controls

So there are **two different classes of issue**:

1. **P0/P1 deployment and routing issues** causing obviously broken styling
2. **P1/P2 product-design debt** inside the main dashboard

## 1.4 What the dashboard should be vs what it is

| Aspect | Should be | Currently is |
|---|---|---|
| Source of truth | One dashboard implementation, one login implementation | Multiple competing HTML implementations |
| Login styling | Fully styled, branded, accessible, consistent with dashboard | Live page appears to use CSS-dependent markup whose CSS 404s |
| Dashboard architecture | Clear ownership of root monolithic `index.html` until explicit migration | Unclear split between root app and `dashboard/` app |
| Deployment confidence | Production must match checked-in `main` | Live evidence conflicts with checked-in routing |
| Theme system | One token system supporting light/dark + brand accents | Separate token systems with different palettes and different files |

## 1.5 Root-cause conclusion

**Main conclusion:** The broken look is not primarily caused by one missing CSS rule inside the main dashboard. It is caused by **frontend duplication plus deployment drift**, with the live entry route exposing the wrong implementation and its assets not resolving.

---

# Part 2: UI / Visual Fixes

## 2.1 Files that must be treated as visual source-of-truth candidates

| File | Current role | Recommended future role |
|---|---|---|
| `index.html` | Main monolithic authenticated dashboard | Keep as authoritative dashboard UI unless a full migration is explicitly approved |
| `login-page.html` | Polished standalone login | Promote to canonical login page |
| `dashboard/index.html` | Alternate dashboard implementation | Decommission or isolate as prototype/archive |
| `dashboard/login.html` | Alternate login implementation | Decommission or replace with redirect/canonical file |
| `dashboard/styles/design-tokens.css` | Prototype token file | Do not extend as primary system unless full migration away from root `index.html` is approved |
| `dashboard/styles/components.css` | Prototype component styles | Same as above |
| `server.py` | Route and static file serving | Must be aligned to the chosen canonical UI files |

## 2.2 Exact visual issues found

### Issue V-01 — Unstyled login page in production

- **Current live appearance:** browser-default-looking typography and weak component styling because CSS files fail to load.
- **Should look like:** the polished dark login aesthetic already implemented in `login-page.html`.
- **Files involved:**
  - `server.py`
  - `login-page.html`
  - `dashboard/login.html`
  - `dashboard/styles/design-tokens.css`
  - `dashboard/styles/components.css`

**Fix direction:**

- Make `login-page.html` the sole login page.
- Ensure `/login` never depends on `/dashboard/styles/*`.
- Remove ambiguity in route targets.

### Issue V-02 — Conflicting login designs

- **Current state:** `dashboard/login.html` is light-token-based and depends on external CSS; `login-page.html` is inline-styled, dark, branded, and more mature.
- **Should look like:** one production login experience only.
- **Files involved:**
  - `dashboard/login.html`
  - `login-page.html`
  - `server.py`

**Fix direction:**

- Standardize on `login-page.html`.
- Either delete `dashboard/login.html`, archive it, or make it non-routable.

### Issue V-03 — Dashboard implementation split

- **Current state:** root `index.html` is the rich main UI, but `server.py` currently points `/` to `dashboard/index.html`.
- **Should look like:** `/` should serve the single production dashboard implementation that matches tests and project rules.
- **Files involved:**
  - `server.py`
  - `index.html`
  - `dashboard/index.html`
  - `tests/test_route_inventory_safety.py`
  - route-related tests under `tests/`

**Fix direction:**

- Route `/` to root `index.html` again unless there is an intentional migration plan to the `dashboard/` implementation.

### Issue V-04 — Desktop-only nav polish

- **Current state:** existing audit shows the polished tab nav is visible on desktop, but tablet/mobile fall back to a different experience.
- **Should look like:** consistent navigation language across desktop, tablet, and mobile.
- **Files involved:**
  - `index.html`
  - `docs/audits/html-redesign-dashboard-design-audit.md`
  - possible related tests:
    - `tests/test_main_menu_design.py`
    - `tests/test_project_mobile_actions_visibility.py`
    - `tests/test_dashboard_qa_static_behavior.py`

**Fix direction:**

- Keep desktop nav.
- Redesign the mobile/tablet drawer and triggers to use the same surface, color, spacing, and affordance system.

### Issue V-05 — Tap targets below accessibility guidance

- **Current state:** audit documents multiple controls below 44 px target height.
- **Should look like:** all actionable controls reach at least 44 px minimum hit area.
- **Files involved:**
  - `index.html`
  - any compact button styles embedded in `index.html`

**Fix direction:**

- Introduce shared min-height/min-width tokens for icon buttons, nav tabs, drawer items, search controls, and status buttons.

### Issue V-06 — Settings page is too long and dense

- **Current state:** settings page is 4k–7.6k px tall across devices according to audit.
- **Should look like:** categorized, collapsible, faster to scan.
- **Files involved:**
  - `index.html`
  - tests around settings:
    - `tests/test_settings_theme.py`
    - `tests/test_settings_theme_explicit_csrf_helper.py`
    - `tests/test_settings_auth_*`

**Fix direction:**

- Split settings into sections/subnav:
  - Providers
  - Authentication
  - GitHub/Render
  - N8N
  - Models
  - Maintenance

### Issue V-07 — Mixed inner-content component language

- **Current state:** cards/forms/toolbars/buttons use inconsistent darkness, spacing, text sizes, and density.
- **Should look like:** one coherent component language.
- **Files involved:**
  - `index.html`

**Fix direction:**

- Extract a documented token hierarchy inside `index.html`:
  - page background
  - elevated surface
  - card
  - border
  - primary button
  - secondary button
  - destructive button
  - field background
  - muted text
  - focus ring

## 2.3 File-by-file visual worklist

| File path | Visual issue | Required change |
|---|---|---|
| `server.py` | Wrong route target / deployment ambiguity | Route `/` and `/login` to canonical files only; ensure static paths reflect real assets or eliminate dependency |
| `index.html` | Dense, inconsistent, partial redesign | Standardize tokens, navigation, surfaces, spacing, tap targets, long-page structure |
| `login-page.html` | Best candidate but not guaranteed active | Finalize as canonical login UI; align branding/theme with dashboard |
| `dashboard/index.html` | Conflicting implementation | Remove from production routing or archive |
| `dashboard/login.html` | Conflicting implementation + CSS dependency | Remove from production routing or archive |
| `dashboard/styles/design-tokens.css` | Dead or prototype styles depending on routing decision | Archive if decommissioning `dashboard/`; otherwise rewire and expand |
| `dashboard/styles/components.css` | Same as above | Same as above |
| `docs/audits/html-redesign-dashboard-design-audit.md` | Existing baseline only | Reference in implementation PRs; update after fixes |
| `scripts/auth-runbook.sh` | Useful for post-deploy verification | Keep and use in rollout verification |
| `tests/test_route_inventory_safety.py` | Must guard static/route behavior | Extend to protect canonical route decisions |

---

# Part 3: Dark Mode Strategy

## 3.1 Decision

Implement dark mode as a **single tokenized theme system in root `index.html` plus `login-page.html`**, not as a separate parallel CSS stack in `dashboard/styles/*`.

### Why

- The main dashboard already has a substantial dark visual language in root `index.html`.
- The login page already has a coherent dark aesthetic in `login-page.html`.
- Building dark mode on top of `dashboard/styles/*` would deepen the split architecture instead of fixing it.

## 3.2 Dark mode architecture

### Recommended pattern

Use layered CSS custom properties:

```css
:root {
  --color-bg: #0a0b0d;
  --color-bg-elevated: #101216;
  --color-surface: rgba(17, 19, 24, 0.88);
  --color-card: rgba(255, 255, 255, 0.03);
  --color-card-hover: rgba(255, 255, 255, 0.05);
  --color-border: rgba(255, 255, 255, 0.08);
  --color-border-strong: rgba(255, 255, 255, 0.14);
  --color-text: #f7f8f8;
  --color-text-secondary: #d0d6e0;
  --color-text-muted: #8a8f98;
  --color-primary: #7170ff;
  --color-primary-hover: #828fff;
  --color-primary-strong: #5e6ad2;
  --color-success: #27a644;
  --color-warning: #f5a524;
  --color-danger: #ef5f6b;
  --focus-ring: 0 0 0 2px #0a0b0d, 0 0 0 4px #7170ff;
}

html[data-theme="light"] {
  --color-bg: #f5f7fb;
  --color-bg-elevated: #ffffff;
  --color-surface: rgba(255, 255, 255, 0.92);
  --color-card: rgba(17, 24, 39, 0.03);
  --color-card-hover: rgba(17, 24, 39, 0.06);
  --color-border: rgba(15, 23, 42, 0.10);
  --color-border-strong: rgba(15, 23, 42, 0.18);
  --color-text: #101828;
  --color-text-secondary: #344054;
  --color-text-muted: #667085;
  --color-primary: #5b5cf0;
  --color-primary-hover: #4f46e5;
  --color-primary-strong: #4338ca;
  --color-success: #15803d;
  --color-warning: #b45309;
  --color-danger: #dc2626;
  --focus-ring: 0 0 0 2px #ffffff, 0 0 0 4px #5b5cf0;
}
```

## 3.3 Dark mode palette

### Core dark palette

| Token | Value | Usage |
|---|---|---|
| `--color-bg` | `#0a0b0d` | App background |
| `--color-bg-elevated` | `#101216` | Sticky bars / drawers |
| `--color-surface` | `rgba(17, 19, 24, 0.88)` | Major surfaces |
| `--color-card` | `rgba(255,255,255,0.03)` | Cards |
| `--color-card-hover` | `rgba(255,255,255,0.05)` | Hover state |
| `--color-border` | `rgba(255,255,255,0.08)` | Default border |
| `--color-border-strong` | `rgba(255,255,255,0.14)` | Focus / active / dividers |
| `--color-text` | `#f7f8f8` | Primary text |
| `--color-text-secondary` | `#d0d6e0` | Supporting text |
| `--color-text-muted` | `#8a8f98` | Labels / metadata |
| `--color-primary` | `#7170ff` | Brand accent |
| `--color-primary-hover` | `#828fff` | Hover |
| `--color-primary-strong` | `#5e6ad2` | Pressed / gradients |
| `--color-success` | `#27a644` | Success |
| `--color-warning` | `#f5a524` | Warning |
| `--color-danger` | `#ef5f6b` | Errors / destructive |

## 3.4 Theme state behavior

### Strategy

1. Respect explicit user choice stored in localStorage.
2. If no saved choice exists, respect `prefers-color-scheme`.
3. Persist theme on settings updates only if the feature already exists for settings.
4. Keep login page and dashboard in sync using the same storage key.

### Recommended storage contract

```js
const THEME_KEY = 'dash-theme';
```

### Recommended initialization pattern

```js
function resolveInitialTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved === 'dark' || saved === 'light') return saved;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(THEME_KEY, theme);
}
```

## 3.5 Files that need dark mode work

| File path | Change needed |
|---|---|
| `index.html` | Normalize and document existing theme tokens; remove scattered ad hoc overrides where possible |
| `login-page.html` | Adopt same token names/storage key/theme toggle behavior as dashboard |
| `server.py` | No theme logic beyond correct route serving; only relevant if theme-related settings APIs are affected |
| `tests/test_settings_theme.py` | Update only if server-side theme persistence contract changes |
| `tests/test_settings_theme_explicit_csrf_helper.py` | Keep current settings theme API behavior if retained |
| new/updated theme tests | Add minimal targeted tests protecting shared theme key + `data-theme` behavior if repo already supports it in existing test patterns |

## 3.6 Code pattern examples

### Button pattern

```css
.ui-btn {
  min-height: 44px;
  padding: 0 14px;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background: var(--color-card);
  color: var(--color-text);
}

.ui-btn--primary {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-strong));
  border-color: transparent;
  color: #fff;
}
```

### Card pattern

```css
.ui-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.28);
}
```

### Field pattern

```css
.ui-field {
  min-height: 44px;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.04);
  color: var(--color-text);
}

.ui-field:focus-visible {
  outline: none;
  box-shadow: var(--focus-ring);
  border-color: var(--color-primary);
}
```

---

# Part 4: Structural / Code Quality Fixes

## 4.1 Architectural issues

### A-01 — Multiple frontend sources of truth

- **Files:** `index.html`, `dashboard/index.html`, `login-page.html`, `dashboard/login.html`, `server.py`
- **Severity:** Critical
- **Fix:** Choose one production dashboard and one production login entrypoint.

### A-02 — Deployment drift not detectable enough

- **Files:** `server.py`, `Dockerfile`, `scripts/auth-runbook.sh`, tests in `tests/`
- **Severity:** Critical
- **Fix:** Add route/asset smoke checks that prove the live HTML matches the intended file family.

### A-03 — Tests mainly cover root `index.html`, but routing points elsewhere

- **Files:** `server.py`, route tests under `tests/`
- **Severity:** High
- **Fix:** Align routing to tested implementation or extend test coverage for intentional alternative implementation.

## 4.2 Build / static asset problems

### B-01 — Live CSS 404s for login experience

- **Files:** `server.py`, `dashboard/styles/design-tokens.css`, `dashboard/styles/components.css`
- **Severity:** Critical
- **Fix:** Prefer eliminating dependency on these files for the canonical login page. If keeping them, verify server static serving for `/styles/*`.

### B-02 — Docker deploy may not reflect intended file graph

- **Files:** `Dockerfile`
- **Severity:** Medium
- **Fix:** Since `COPY . .` already copies everything, the problem is likely not missing files in Docker, but routing/deploy drift. Still, verify the container start path and smoke the served routes after deploy.

## 4.3 Performance issues

### P-01 — Root `index.html` is extremely large

- **Files:** `index.html`
- **Severity:** High
- **Impact:** harder maintainability, slower parsing, brittle edits, risk of style/JS collisions.
- **Fix direction:** Do not rewrite immediately. First stabilize production routing. Later extract additive sections or modularize inline blocks in controlled phases.

### P-02 — Excessive DOM/control density

- **Files:** `index.html`
- **Severity:** Medium
- **Fix direction:** progressive disclosure, collapsible advanced sections, action grouping.

### P-03 — Long-page scroll burden

- **Files:** `index.html`
- **Severity:** Medium
- **Fix direction:** section nav, accordions, sticky action areas only where needed.

## 4.4 Accessibility issues

### AX-01 — Small tap targets

- **Files:** `index.html`
- **Severity:** High
- **Fix:** enforce 44 px min target for interactive controls.

### AX-02 — Potential focus-noise from too many global controls

- **Files:** `index.html`
- **Severity:** Medium
- **Fix:** ensure hidden controls are removed from flow/tab order.

### AX-03 — Contrast inconsistency across mixed surfaces

- **Files:** `index.html`, `login-page.html`
- **Severity:** Medium
- **Fix:** normalize contrast tokens and run audit after consolidation.

## 4.5 Structural recommendations to reject

These should **not** be the default approach for the first overhaul pass:

1. **Do not migrate the whole app into `dashboard/` immediately.**
   The repo's tests, docs, and project rules all point to root `index.html` as the main app.

2. **Do not build a third theme system.**
   Consolidate existing tokens; do not add another independent CSS vocabulary.

3. **Do not rewrite the monolithic dashboard before fixing routing drift.**
   First ensure the correct files are live.

---

# Part 5: Implementation Order

## Overview

Each phase below is a PR-able unit with explicit dependencies, acceptance criteria, and complexity.

## Phase 1 — Reconcile production route/source of truth

**Goal:** Ensure the live app serves the intended dashboard and login files.

### Tasks

| # | Task | Files | Complexity | Estimate |
|---|---|---|---|---|
| 1.1 | Audit actual live routing vs checked-in routing and record the intended canonical files | `server.py`, `docs/`, `OVERHAUL-PLAN.md` | M | 0.5 day |
| 1.2 | Route `/login` to canonical `login-page.html` only | `server.py` | S | 0.25 day |
| 1.3 | Route `/` to canonical dashboard file (recommended: root `index.html`) | `server.py` | S | 0.25 day |
| 1.4 | Add/adjust tests protecting route targets and static fallback behavior | `tests/test_route_inventory_safety.py`, related route/auth tests | M | 0.5 day |
| 1.5 | Run local smoke + auth runbook + post-deploy smoke | `scripts/auth-runbook.sh`, existing tests | S | 0.25 day |

### Acceptance criteria

- `/login` returns markup from `login-page.html`, not `dashboard/login.html`.
- `/` serves the chosen dashboard source-of-truth file.
- No CSS 404 is required for login styling.
- Route inventory tests pass.
- Post-deploy smoke confirms live behavior matches intended files.

### Notes

This phase is the highest priority. Do not start visual cleanup until this is merged.

---

## Phase 2 — Decommission duplicate dashboard/login implementations

**Goal:** Remove ambiguity so future UI work lands in the correct files.

### Tasks

| # | Task | Files | Complexity | Estimate |
|---|---|---|---|---|
| 2.1 | Decide archival strategy for `dashboard/index.html` and `dashboard/login.html` | `dashboard/`, `docs/` | M | 0.5 day |
| 2.2 | Remove production routing to `dashboard/` HTML files | `server.py` | S | 0.25 day |
| 2.3 | Add banner/comments or documentation marking `dashboard/` files as non-canonical if kept | `docs/` or file headers if approved | S | 0.25 day |
| 2.4 | Update tests/docs to point future work to root `index.html` + `login-page.html` | `docs/hermes-multi-agent-git-collaboration.md`, tests as needed | M | 0.5 day |

### Acceptance criteria

- No production route depends on `dashboard/index.html` or `dashboard/login.html`.
- Documentation clearly names the canonical dashboard and login files.
- Future contributors cannot reasonably mistake the wrong implementation as live.

---

## Phase 3 — Fix login UX and unify auth entry visual language

**Goal:** Make the first visible screen feel intentional and production-grade.

### Tasks

| # | Task | Files | Complexity | Estimate |
|---|---|---|---|---|
| 3.1 | Final polish pass on `login-page.html` to match dashboard brand and accessibility standards | `login-page.html` | M | 0.5 day |
| 3.2 | Unify theme key/theme toggle logic with dashboard behavior | `login-page.html`, `index.html` | M | 0.5 day |
| 3.3 | Validate login focus order, keyboard behavior, and reduced-motion handling | `login-page.html` | S | 0.25 day |
| 3.4 | Add/adjust smoke test coverage for `/login` content markers | `tests/test_auth_smoke.py`, `tests/test_auth_login_flow.py`, or targeted new test | M | 0.5 day |

### Acceptance criteria

- Login page is fully styled without external asset dependency failure.
- Theme toggle works consistently.
- Keyboard navigation and focus states are visible and predictable.
- Live `/login` matches the intended polished design.

---

## Phase 4 — Create one shared theme/token system

**Goal:** Consolidate visual primitives without rewriting the whole app.

### Tasks

| # | Task | Files | Complexity | Estimate |
|---|---|---|---|---|
| 4.1 | Normalize root `index.html` theme tokens into a documented set | `index.html` | L | 1 day |
| 4.2 | Map `login-page.html` to the same token vocabulary | `login-page.html` | M | 0.5 day |
| 4.3 | Standardize primary/secondary/destructive button patterns | `index.html`, `login-page.html` | M | 0.5 day |
| 4.4 | Standardize card/field/status chip patterns | `index.html` | L | 1 day |
| 4.5 | Verify no regressions in theme-related tests | `tests/test_settings_theme.py`, `tests/test_settings_theme_explicit_csrf_helper.py` | S | 0.25 day |

### Acceptance criteria

- Token names are consistent across dashboard and login.
- No page introduces a separate conflicting palette.
- Primary components reuse the same border, radius, type, and focus conventions.

---

## Phase 5 — Navigation and responsive system cleanup

**Goal:** Make the redesign visible and usable across desktop, tablet, and mobile.

### Tasks

| # | Task | Files | Complexity | Estimate |
|---|---|---|---|---|
| 5.1 | Raise all core nav/search/icon interactions to 44 px minimum | `index.html` | M | 0.5 day |
| 5.2 | Apply desktop nav visual language to tablet/mobile drawer | `index.html` | L | 1 day |
| 5.3 | Add tablet-specific nav behavior instead of abrupt desktop-to-drawer switch | `index.html` | L | 1 day |
| 5.4 | Validate no overflow and no nav regressions across breakpoints | `index.html`, existing QA scripts/docs | M | 0.5 day |

### Acceptance criteria

- Desktop, tablet, and mobile each show a coherent navigation system.
- Tap targets meet 44 px minimum.
- No horizontal overflow.
- Active-state styling is consistent across navigation modes.

---

## Phase 6 — Information architecture and density reduction

**Goal:** Make the authenticated app faster to scan and operate.

### Tasks

| # | Task | Files | Complexity | Estimate |
|---|---|---|---|---|
| 6.1 | Split Settings into category sections with local navigation | `index.html` | L | 1 day |
| 6.2 | Collapse advanced/rare settings by default | `index.html` | M | 0.5 day |
| 6.3 | Reduce secondary-action clutter on Projects, N8N Fixer, KW Research, Analytics | `index.html` | XL | 1.5-2 days |
| 6.4 | Add page-specific sticky action areas only where task completion needs them | `index.html` | M | 0.5 day |

### Acceptance criteria

- Settings page is substantially more scannable.
- Long operational tabs present one clear primary action.
- Secondary/advanced actions are grouped without removing capability.

---

## Phase 7 — Regression hardening and rollout verification

**Goal:** Prevent recurrence of route drift, unstyled entry pages, and major UI regressions.

### Tasks

| # | Task | Files | Complexity | Estimate |
|---|---|---|---|---|
| 7.1 | Add regression tests asserting canonical route targets | `tests/test_route_inventory_safety.py`, auth tests | M | 0.5 day |
| 7.2 | Add test coverage for presence of expected login/dashboard markers | `tests/` targeted files | M | 0.5 day |
| 7.3 | Re-run/update visual audit artifacts | `docs/audits/html-redesign-dashboard-design-audit.md`, `output/playwright/` | M | 0.5 day |
| 7.4 | Run post-deploy production smoke checklist | `scripts/auth-runbook.sh`, docs | S | 0.25 day |

### Acceptance criteria

- CI/test suite would catch future route drift.
- Visual entrypoint regressions are detectable.
- Updated audit shows improvement on nav consistency, tap targets, and page density.

---

# Recommended first implementation decision

## Choose this unless a stakeholder explicitly says otherwise

### Canonical production files

- **Dashboard:** `index.html`
- **Login:** `login-page.html`
- **Server route owner:** `server.py`

### Why this is the safest path

1. Project rules explicitly describe the app as a single-page app in root `index.html`.
2. The test suite is already biased toward root `index.html`.
3. `login-page.html` is visually stronger than `dashboard/login.html`.
4. This path fixes the broken live styling issue with the smallest architectural risk.

---

# Acceptance checklist by area

## Routing / deployment

- [ ] Live `/` serves the chosen canonical dashboard file.
- [ ] Live `/login` serves the chosen canonical login file.
- [ ] Live login no longer depends on 404-ing CSS assets.
- [ ] Local and production route behavior match checked-in `server.py`.

## Visual consistency

- [ ] One token vocabulary is shared across login and dashboard.
- [ ] Button, field, card, and toolbar primitives are consistent.
- [ ] Mobile/tablet nav visually matches desktop language.

## Accessibility

- [ ] Core controls meet 44 px target size.
- [ ] Focus rings are visible and consistent.
- [ ] Contrast is normalized across dark and light themes.

## Maintainability

- [ ] One dashboard entrypoint and one login entrypoint are documented.
- [ ] Duplicate implementations are removed from production routing.
- [ ] Tests protect the chosen source-of-truth files.

---

# Suggested verification commands for implementation PRs

Use the existing repo patterns and keep checks targeted first.

```powershell
python -m py_compile "server.py" "kwr_backend.py"
pytest "tests/test_route_inventory_safety.py" -q
pytest "tests/test_auth_smoke.py" "tests/test_auth_login_flow.py" -q
pytest "tests/test_settings_theme.py" "tests/test_settings_theme_explicit_csrf_helper.py" -q
```

Then run broader validation as needed:

```powershell
pytest "tests" -q
```

Post-deploy smoke:

```powershell
bash "scripts/auth-runbook.sh" safe-prod
```

If credentials are available:

```powershell
$env:TEST_ADMIN_PASSWORD="***"; bash "scripts/auth-runbook.sh" full-prod
```

---

# Final implementation guidance for agents

1. **Do not start by redesigning components.** Start by fixing route/source-of-truth ambiguity.
2. **Do not add more files unless necessary.** Prefer converging on existing root files.
3. **Do not edit `index.html` broadly in one pass.** Keep changes scoped by section and verify with existing tests.
4. **Treat `server.py`, `index.html`, `Dockerfile`, and docs as coordinated changes.**
5. **After Phase 1, re-check production before Phase 2.** If production still serves the wrong HTML, resolve deployment drift before any more UI work.
