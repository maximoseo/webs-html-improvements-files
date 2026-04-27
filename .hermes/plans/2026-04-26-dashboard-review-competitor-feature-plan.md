# HTML Redesign Dashboard — Review, Debug, Competitor Research & Missing Features Plan

> **For Hermes:** Use systematic-debugging for every suspected bug. Do not implement fixes yet. Start slowly and carefully.

**Goal:** Build a careful, phased plan to review every dashboard tab, debug issues methodically, compare competitor products/workflows, and propose genuinely useful missing features before any implementation.

**Architecture:** Two-track audit. Track A audits the existing dashboard tab-by-tab (UI, UX, state, data, API, mobile, errors, regressions). Track B studies relevant competitor tools and patterns, then maps feature gaps into a prioritized dashboard roadmap. Findings are merged into one evidence-based recommendation set.

**Tech Stack:** Existing HTML Redesign Dashboard repo, production dashboard, browser/manual QA, code inspection, web research, competitor analysis.

---

## Scope

### In scope
- Full dashboard tab inventory
- Careful review/debug of each tab
- Shared shell/navigation/state checks
- Mobile/desktop behavior checks
- Console/API/error inspection
- Competitor research on adjacent products/workflows
- Missing feature identification
- Prioritized recommendation list

### Out of scope for this phase
- No code changes
- No fixes
- No deployment
- No feature implementation

---

## Phase 0: Baseline and guardrails

**Objective:** Ensure we inspect the right artifact and avoid rushing into fixes.

### Task 0.1: Confirm audit target
**Objective:** Lock the exact product/repo/env to inspect.

**Files:**
- Reference: `/home/seoadmin/webs-html-improvements-files/`
- Output: `/home/seoadmin/webs-html-improvements-files/.hermes/plans/2026-04-26-dashboard-review-competitor-feature-plan.md`

**Steps:**
1. Confirm repo path and dashboard target.
2. Confirm that this phase is planning + investigation only.
3. Confirm slow/careful batch order.

**Verification:**
- Repo exists
- Plan file saved

### Task 0.2: Define evidence standard
**Objective:** Avoid opinion-only findings.

**Evidence required per finding:**
- Repro steps
- Affected tab/screen
- Expected vs actual
- Screenshot or DOM evidence when needed
- Console/network evidence when needed
- Severity: critical/high/medium/low
- Scope: isolated/shared shell/data/API/mobile/copy/performance

---

## Phase 1: Careful dashboard audit plan

**Objective:** Review the dashboard from the outside in, starting with shared shell before deep tabs.

### Audit order (slow and careful)
1. Shared shell/navigation
2. Projects tab
3. Tasks tab
4. Settings tab
5. Analytics tab
6. N8N Fixer tab
7. Skills Radar tab
8. KW Research tab

### For each tab, inspect these layers
1. Entry/load behavior
2. Empty/loading/error/success states
3. Primary CTA clarity
4. Forms/validation
5. Data freshness and persistence
6. Console errors/warnings
7. Mobile usability
8. Visual hierarchy/readability
9. Edge cases
10. Cross-tab side effects

### Task 1.1: Shared shell checklist
**Objective:** Audit the frame that can break all tabs.

**Check:**
- Top nav/tab switching
- Bottom nav/mobile nav
- Active state accuracy
- Sticky header behavior
- Drawer/modal/overlay conflicts
- Scroll lock and scroll restoration
- Search/global controls if present
- Toasts/alerts layering
- Keyboard/focus basics
- Responsive breakpoints

**Output:**
- Shared shell findings list
- Risks that could invalidate tab-specific findings

### Task 1.2: Per-tab checklist template
**Objective:** Use the same rubric for each tab.

**Per-tab review template:**
- Purpose of tab
- Main user jobs-to-be-done
- First impression / clarity
- Core workflow steps
- Broken/friction points
- Console/API findings
- Mobile issues
- Missing affordances
- Improvement ideas
- Severity + confidence

---

## Phase 2: Systematic debug workflow

**Objective:** Investigate bugs without guessing.

### Task 2.1: Reproduction-first rule
For any bug candidate:
1. Write exact repro steps
2. Reproduce consistently
3. Inspect console/network/state
4. Check whether issue is shared-shell or tab-specific
5. Form root-cause hypothesis only after evidence

### Task 2.2: Bug categories to classify
- Navigation/state bug
- Rendering/layout bug
- Input/validation bug
- API/data bug
- Async/loading bug
- Mobile responsiveness bug
- Accessibility/usability bug
- Copy/IA confusion bug
- Performance bug

### Task 2.3: Debug output format
For every issue:
- ID
- Title
- Tab
- Repro steps
- Expected
- Actual
- Evidence
- Suspected layer
- Severity
- Recommended next action (investigate deeper / safe fix later / needs product decision)

---

## Phase 3: Competitor research plan

**Objective:** Study real products/workflows that solve adjacent problems so feature suggestions are grounded and useful.

### Competitor buckets to review
1. Internal tool / ops dashboards
2. AI workflow builders / prompt workbenches
3. SEO workflow dashboards
4. Content pipeline / template generation tools
5. QA / audit / issue triage dashboards

### What to compare in each competitor
- Information architecture
- Tab structure / navigation model
- Onboarding clarity
- Project overview quality
- Queue/run visibility
- Error handling clarity
- Review/approval flows
- Prompt/template management
- Change history/versioning
- Collaboration / assignment features
- Reporting/export features
- Mobile fallback behavior

### Competitor selection criteria
Choose tools that are closest to one or more dashboard jobs:
- managing redesign projects
- launching/monitoring AI workflows
- reviewing outputs
- debugging pipeline failures
- tracking task/status/progress
- keyword/SEO research execution

### Output per competitor
- Product name
- Why it is relevant
- What it does better than current dashboard
- What it does worse / should not be copied
- Reusable pattern worth adapting
- Estimated implementation value for this dashboard

---

## Phase 4: Missing feature discovery

**Objective:** Identify additions that actually help employees use the dashboard as a ready-to-use engine.

### Feature evaluation lens
A feature is worth proposing only if it meaningfully improves one or more of:
- faster task completion
- fewer operator mistakes
- easier debugging
- better visibility into pipeline state
- safer approvals / handoffs
- better output quality control
- less context switching
- stronger mobile usability

### Missing-feature categories to evaluate
1. Visibility & status
   - run timeline
   - health/status indicators
   - last successful run / failure reason
   - per-project activity feed
2. Review & QA
   - approval gates
   - side-by-side diff/review
   - issue tagging
   - regression checklist per output
3. Prompt & workflow management
   - prompt version history
   - test-run sandbox
   - saved templates/presets
   - rollback to previous config
4. Operations
   - retries/re-run controls
   - queue management
   - ownership / assignee
   - notifications / alerts
5. Analytics & SEO utility
   - result confidence / completeness markers
   - export summaries
   - competitor snapshot panels
   - keyword cluster QA helpers
6. UX foundations
   - global search/command palette
   - empty-state guidance
   - inline help
   - contextual warnings

### Prioritization framework
Score each candidate on:
- User value
- Frequency of use
- Risk reduction
- Implementation complexity
- Fit with current dashboard architecture

Priority labels:
- P1 = high value / low-medium complexity / strong operational benefit
- P2 = strong value but needs product/design work
- P3 = nice-to-have or speculative

---

## Phase 5: Deliverables

**Objective:** Produce a clean decision package before any implementation.

### Deliverable A: Findings report
Contains:
- Shared shell findings
- Per-tab findings
- Severity summary
- Repro evidence
- Root-cause hypotheses where possible

### Deliverable B: Competitor comparison report
Contains:
- competitor shortlist
- reusable patterns
- anti-patterns to avoid
- gap summary

### Deliverable C: Missing features roadmap
Contains:
- P1/P2/P3 missing features
- user problem solved
- expected operational impact
- dependencies/risks

### Deliverable D: Recommended next batch
A small, safe first batch only, such as:
- 1-2 shared shell fixes
- 1 high-confidence tab bug
- 1 high-value missing feature spec

---

## Proposed execution order after plan approval

### Batch 1 (investigation only)
- Shared shell review
- Projects tab review
- Initial competitor shortlist

### Batch 2
- Tasks + Settings review
- Competitor comparison deepening
- First missing-feature draft

### Batch 3
- Analytics + N8N Fixer review
- Feature prioritization refinement

### Batch 4
- Skills Radar + KW Research review
- Final merged recommendation set

---

## Success criteria
- Every tab has a structured review entry
- Shared shell is audited before deep conclusions
- Competitor suggestions are evidence-based, not generic
- Missing features are tied to concrete operator pain points
- No implementation starts before findings are prioritized

---

## Immediate next step
If approved, start **only with Batch 1 investigation**:
1. Shared shell review
2. Projects tab review
3. Competitor shortlist for adjacent dashboards/tools

No fixes yet.
