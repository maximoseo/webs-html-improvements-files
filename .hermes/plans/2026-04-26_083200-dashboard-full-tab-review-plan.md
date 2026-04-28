# Dashboard Full-Tab Review + Debug Plan

> **For Hermes:** Planning only. Do not implement from this plan until explicitly approved. When execution starts, use a sequential review/debug workflow with Codex-style rigor, but keep final orchestration in Hermes so findings stay scoped and traceable.

**Goal:** Run a thorough review/debug pass across every dashboard tab, find broken flows, weak UX, fragile code paths, visual regressions, missing tests, and production risks, then prioritize concrete improvements.

**Architecture:** This will be a staged audit across live production, local source, backend routes, and existing tests. We will combine browser QA, authenticated production smoke checks, code inspection, and targeted test review. Findings will be triaged by severity and then fixed in small batches.

**Tech Stack:** Single-file frontend (`index.html`), Python backend (`server.py`), Render Docker deploy, live authenticated dashboard, pytest suite.

---

## 1. Current Context

### Live dashboard domains
- Primary: `https://html-redesign-dashboard.maximo-seo.ai/`
- Render URL: `https://webs-html-improvements-files.onrender.com`

### Main dashboard tabs discovered
1. Projects
2. N8N Fixer
3. Skills Radar
4. KW Research
5. Tasks
6. Analytics
7. Settings

### Relevant files
- Frontend: `index.html`
- Backend: `server.py`
- KWR backend: `kwr_backend.py`
- Auth/login UI: `login-page.html`
- Tests: `tests/*.py`

### Recent change cluster to keep in mind
Recent commits are heavily mobile-focused:
- bottom nav / FAB / touch targets
- pull-to-refresh
- login polish
- mobile scroll fix
- mobile menu toggle + icon polish

This means the first audit pass should pay extra attention to:
- regressions caused by mobile patches
- shared header/nav state across tabs
- scroll locking / overlays / modals / tours
- code coupling around `showPage()`, nav state, and mobile drawer behavior

---

## 2. Audit Objectives

For **each tab**, the audit should answer:
1. Does the tab load correctly on production?
2. Are there JS console errors, silent exceptions, or failed requests?
3. Are there broken UI states, overlap, clipping, hidden content, or scroll traps?
4. Are primary actions discoverable and working?
5. Are empty/loading/error states sane?
6. Is the mobile layout usable?
7. Is the implementation brittle, duplicated, or missing tests?
8. What should be improved first: bugfix, UX polish, cleanup, test coverage, or architecture?

---

## 3. Review Methodology

### Phase A — Static code review and architecture map
Purpose: understand how each tab is wired before live testing.

#### Task A1: Map frontend tab entry points
**Files:**
- Read: `index.html`

**Check:**
- `showPage()` routing logic
- tab buttons and bottom-nav links
- page containers (`#page-fixer`, `#page-radar`, `#page-tasks`, `#page-kwr`, `#page-analytics`, `#page-settings`)
- per-page init hooks (`initFixerPage`, `initRadarPage`, etc.)

**Deliverable:**
- A small matrix: tab → container → init function → major actions → known shared UI dependencies.

#### Task A2: Map backend endpoints by tab
**Files:**
- Read/search: `server.py`, `kwr_backend.py`

**Check:**
- auth dependencies
- API endpoints each tab relies on
- long-running jobs or polling flows
- endpoints that mutate state versus read-only

**Deliverable:**
- A second matrix: tab → endpoints → auth needed → likely failure modes.

#### Task A3: Map existing automated coverage
**Files:**
- Read filenames in `tests/`
- Inspect the most relevant tests for each tab

**Check:**
- which tabs already have tests
- which flows are untested
- which tests are stale / narrow / snapshot-only

**Deliverable:**
- Coverage gap table.

---

### Phase B — Production smoke and browser QA by tab
Purpose: inspect the real live app instead of assuming code state == behavior.

#### Shared procedure for each tab
For every tab, do this in order:
1. Log in on production.
2. Navigate to the tab via the real UI.
3. Capture browser snapshot.
4. Check `browser_console()` immediately.
5. Inspect visual layout with `browser_vision()`.
6. Trigger 2–5 primary actions.
7. Re-check console and visible state.
8. Record findings under:
   - Functional bugs
   - UX friction
   - Visual/layout issues
   - Accessibility concerns
   - Performance/suspicious behavior
   - Test coverage needed

#### Tabs and what to test

##### Tab 1 — Projects
**Primary flows:**
- search
- sort
- grid/list switch
- open project card
- preview
- review notes
- expand all
- bottom nav state
- mobile drawer interactions

**Risks to inspect:**
- card click targets fighting with inner buttons
- onboarding/tour overlays blocking clicks
- list/grid persistence bugs
- sort/filter race conditions
- mobile scroll and sticky header interactions

##### Tab 2 — N8N Fixer
**Primary flows:**
- load workflows
- stuck workflow panel
- paste/import JSON
- run analysis
- diff view toggles
- copy/download/save/deploy actions

**Risks to inspect:**
- large JSON rendering freezes
- disabled/enabled state mismatches
- analysis button gating
- deploy/save actions with partial data
- mobile overflow in dense action areas

##### Tab 3 — Skills Radar
**Primary flows:**
- scan/start radar
- switch radar tabs (scores/trends/AI/reports/export)
- inspect reports list
- open/close drawer or overlay components

**Risks to inspect:**
- phantom drawer overlays
- scroll trapping in radar subpanels
- chart/report rendering issues
- stale state after repeated runs

##### Tab 4 — KW Research
**Primary flows:**
- fill required inputs
- run research
- inspect status and preview
- approve/export/report list
- regenerate / cancel

**Risks to inspect:**
- state machine desync
- long-polling UI failures
- row preview rendering issues
- action bar visibility bugs
- reports table/download states

##### Tab 5 — Tasks
**Primary flows:**
- create task
- edit task
- complete task
- switch list/board modes if present
- filters/search
- persistence after reload

**Risks to inspect:**
- state persistence edge cases
- modal/body scroll lock leaks
- mobile form usability
- stale filters after edits

##### Tab 6 — Analytics
**Primary flows:**
- tab load
- audit panels
- header alignment
- major data sections and cards

**Risks to inspect:**
- header collisions (known test exists)
- data empty-state clarity
- overflow in charts/tables/cards

##### Tab 7 — Settings
**Primary flows:**
- auth tooling panels
- warnings/runbook/checklist cards
- theme settings
- any save/test buttons

**Risks to inspect:**
- auth incident pack layout
- warning card sprawl on mobile
- controls with hidden dependencies

---

### Phase C — Codex-style review/debug pass
Purpose: review code like an autonomous coding reviewer would, but do it sequentially and traceably.

#### Task C1: Run a structured review prompt over the repo
Use Codex only after the manual map is ready.

**Prompt shape:**
- Review `index.html`, `server.py`, `kwr_backend.py`, `login-page.html`, and `tests/`
- Focus on:
  - fragile tab routing/state handling
  - scroll lock / overlay / modal bugs
  - dead CSS/JS or duplicated patterns
  - missing cleanup paths
  - production risks
  - tests missing for critical flows
- Ask for findings only, not fixes first

**Constraint:**
- Sequential, one review batch at a time
- No code changes during initial Codex review

#### Task C2: Cross-check Codex findings against live evidence
Every Codex finding must be tagged as one of:
- reproduced live
- confirmed by code inspection only
- likely false positive
- needs isolated reproduction

#### Task C3: Build prioritized fix queue
Priority order:
1. Production-breaking bugs
2. Silent JS exceptions / auth / save/deploy failures
3. Mobile navigation/scroll/input blockers
4. Visual overlap and interaction traps
5. Test coverage gaps on critical paths
6. Code health/refactor opportunities
7. Nice-to-have polish

---

### Phase D — Output artifacts
At the end of the review, produce these artifacts:

#### Artifact 1: Dashboard findings report
Per tab:
- status summary
- top bugs
- top UX improvements
- code smells
- suggested tests
- recommended next actions

#### Artifact 2: Prioritized implementation backlog
Each item should include:
- title
- severity
- affected tab
- root cause summary
- likely files to change
- recommended validation

#### Artifact 3: Optional execution plan
After approval, convert the backlog into a small-batch implementation plan.

---

## 4. Exact Execution Sequence (when approved)

### Step 1 — Read-only repo inspection
- inspect `showPage()` and per-tab init functions
- map backend endpoints
- map tests

### Step 2 — Production login + baseline smoke
- `/api/health`
- authenticated dashboard root
- console baseline on load

### Step 3 — Review tabs one at a time in this order
1. Projects
2. Tasks
3. Settings
4. Analytics
5. N8N Fixer
6. Skills Radar
7. KW Research

Reason for order:
- Projects/Tasks/Settings/Analytics are cheaper and expose shared shell/navigation issues first.
- Fixer/Radar/KWR are heavier and more stateful, so they should be reviewed after baseline shell confidence.

### Step 4 — Run Codex review after manual evidence exists
- one batch
- findings only
- no automatic edits yet

### Step 5 — Synthesize and prioritize
- merge browser evidence + code evidence + test gaps + Codex findings

### Step 6 — Ask approval before implementation
Because the user prefers approval-first and small batches, implementation should begin only after the findings report is presented.

---

## 5. Likely Files to Change Later
Not for this planning turn — this is the likely execution scope after approval.

### Frontend
- `index.html`
- possibly `login-page.html`

### Backend
- `server.py`
- `kwr_backend.py`

### Tests
Likely additions/modifications under:
- `tests/test_main_menu_design.py`
- `tests/test_tasks_tab_persistence_api.py`
- `tests/test_analytics_header_collision.py`
- `tests/test_kwr_controls.py`
- `tests/test_auth_smoke.py`
- new tab-specific smoke/interaction tests as needed

---

## 6. Risks and Constraints

### Risks
- `index.html` is very large and has many competing CSS overrides.
- Mobile fixes can regress desktop shell behavior and vice versa.
- Some browser-tool mobile simulation is imperfect, so real-device validation should remain part of acceptance.
- Production may briefly serve stale HTML during Render rollout, so frontend markers must always be checked after deploy.

### Constraints
- User prefers small batches and approval-first.
- Sub-agents should run sequentially, not broadly parallelized.
- Do not declare fixes complete on code diff alone — require live verification.

---

## 7. Recommended First Execution Batch
If/when execution is approved, start with this smallest high-value batch:

1. Shared shell/navigation review
   - header
   - top tabs
   - bottom nav
   - mobile drawer
   - scroll lock
2. Projects tab deep review
3. Tasks tab review
4. Settings tab review

This should expose most shared infrastructure issues before touching the heavier specialized tabs.

---

## 8. Success Criteria for the Review Itself
The review phase is complete only when:
- every tab was inspected live
- each tab has a short findings section
- console status is recorded for each tab
- endpoint dependencies are mapped
- existing test coverage is mapped
- high/medium/low findings are prioritized
- implementation has **not** started yet without approval

---

## 9. Proposed Next Step
If you approve execution of this plan, the next action should be:

**Run the shared-shell + Projects tab review first, produce a findings report, then pause for your approval before moving to the next batch.**
