---
phase: 01-baseline-audit-wordpress-risk-assessment
plan: 01
subsystem: audit
tags: [wordpress, wp_kses_post, safe_style_css, display-flex, inline-css, oritmartin, hipsterstyle, wixstatic, migration]

# Dependency graph
requires: []
provides:
  - "Line-by-line HTML template risk inventory with 19 issues across 4 severity levels"
  - "Complete oritmartin-to-hipsterstyle site reference migration map with 58 replacement points"
  - "CSS property survival matrix for WordPress safe_style_css whitelist"
  - "Anchor ID, floating button, hidden text, and RTL alignment audits"
affects: [02-prompt-contradiction-report, 03-workflow-logic-bug-report, phase-02-template-rebuild, phase-03-firecrawl-discovery]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "WordPress wp_kses_post() CSS property survival analysis"
    - "Severity-based risk classification: CRITICAL/HIGH/MEDIUM/LOW"
    - "Grep-verified line-number referencing for audit artifacts"

key-files:
  created:
    - ".planning/phases/01-baseline-audit-wordpress-risk-assessment/audit/01-html-template-risk-inventory.md"
    - ".planning/phases/01-baseline-audit-wordpress-risk-assessment/audit/04-site-reference-migration-map.md"
  modified: []

key-decisions:
  - "display CSS property confirmed NOT on WordPress safe_style_css -- root cause of 64 layout-breaking occurrences"
  - "All hover handlers use this.style directly, not class selectors -- class attributes are dead weight"
  - "Hidden text audit PASSED -- no content hidden in base state, all hover effects purely decorative"
  - "14 TBD replacement values flagged for Phase 2 Firecrawl discovery"

patterns-established:
  - "Audit artifacts use grep-verified line numbers, never estimated"
  - "Risk severity follows CRITICAL (layout breaks) > HIGH (visual degradation) > MEDIUM (unfiltered_html dependent) > LOW (cosmetic)"

requirements-completed: [WP-01, WP-02, WP-03, WP-04, WP-05, WP-06, WP-07, WP-08]

# Metrics
duration: 8min
completed: 2026-03-25
---

# Phase 01 Plan 01: HTML Template Risk Inventory & Site Reference Migration Map Summary

**321-line HTML template audited against WordPress wp_kses_post() safe_style_css whitelist: 7 CRITICAL (display property stripped across 64 occurrences), 4 HIGH, 5 MEDIUM, 3 LOW issues documented with fix strategies. 58 oritmartin-to-hipsterstyle replacement points mapped across 3 files with 14 Phase 2 dependencies.**

## Performance

- **Duration:** ~8 min
- **Started:** 2026-03-25T13:40:40Z
- **Completed:** 2026-03-25T13:49:00Z
- **Tasks:** 2/2
- **Files created:** 2

## Accomplishments

- Complete line-by-line risk inventory of 321-line HTML template covering 10 audit sections (executive summary, CRITICAL/HIGH/MEDIUM/LOW issues, CSS property audit, anchor ID audit, floating button audit, hidden text risk audit, RTL alignment audit)
- 64 `display:` property occurrences documented as the single root cause of most CRITICAL layout issues (display NOT on safe_style_css)
- Complete migration map of 58 oritmartin/wixstatic/contact references across HTML template (33 points), N8N prompt (18 points), and N8N workflow (7 points)
- 14 TBD replacement values categorized and flagged as Phase 2 Firecrawl discovery dependencies

## Task Commits

Each task was committed atomically:

1. **Task 1: HTML Template Line-by-Line Risk Inventory** - `c0fbe40` (feat)
2. **Task 2: Site Reference Migration Map** - `1eb2e20` (feat)

## Files Created/Modified

- `.planning/phases/01-baseline-audit-wordpress-risk-assessment/audit/01-html-template-risk-inventory.md` - 220-line risk inventory with 7 CRITICAL, 4 HIGH, 5 MEDIUM, 3 LOW issues, CSS property audit table, anchor/floating/hidden-text/RTL audits
- `.planning/phases/01-baseline-audit-wordpress-risk-assessment/audit/04-site-reference-migration-map.md` - 202-line migration map with per-file reference tables, category summary, and Phase 2 dependency list

## Decisions Made

- **display is the root cause:** 64 inline style declarations use `display` (flex:27, inline-flex:25, grid:1, block:8, inline-block:1, none:2) which is NOT on safe_style_css. Fix strategies must focus on display replacement, not individual flex properties.
- **Class attributes are dead weight:** All 38 class attributes only function via the `<style>` block (lines 2-14) which WordPress strips. All hover handlers use `this.style` directly. Classes can be removed.
- **Hidden text risk: NONE.** All 28 onmouseover/onmouseout handlers are purely decorative (color shifts, transforms). Base inline styles show all text without JS.
- **14 replacement values deferred to Phase 2:** Product URLs, contact info, social profiles, brand names all require Firecrawl discovery from hipsterstyle.co.il.

## Deviations from Plan

None -- plan executed exactly as written.

## Issues Encountered

None.

## Known Stubs

None -- this plan produces audit documentation only, no code.

## User Setup Required

None -- no external service configuration required.

## Next Phase Readiness

- Risk inventory provides ground truth for template rebuild phases
- Migration map provides complete reference list for Phase 2 Firecrawl discovery
- Remaining Phase 1 plans (prompt contradictions, workflow bugs) can proceed in parallel
- **Blocker for template rebuild:** Firecrawl must resolve 14 TBD values before Phase 3+ can begin replacement
- **Open question:** Whether target WordPress (mahsan.websreport.net) has custom `safe_style_css` filter adding `display` -- if yes, CRITICAL severity of C2-C7 drops significantly

## Self-Check: PASSED

- [x] `01-html-template-risk-inventory.md` exists
- [x] `04-site-reference-migration-map.md` exists
- [x] Commit `c0fbe40` found in git log
- [x] Commit `1eb2e20` found in git log

---
*Phase: 01-baseline-audit-wordpress-risk-assessment*
*Completed: 2026-03-25*
