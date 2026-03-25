---
phase: 09-n8n-prompt-workflow-alignment
plan: 01
subsystem: n8n-pipeline
tags: [n8n, wordpress, prompt-engineering, workflow-json, hipsterstyle, hebrew-rtl]

requires:
  - phase: 01-baseline-audit-wordpress-risk-assessment
    provides: Contradiction and bug reports identifying CRIT-1, CRIT-2, BUG-1 through BUG-7
  - phase: 03-foundation-article-shell
    provides: Article shell with hs-top ID, inline-only CSS, RTL structure
  - phase: 04-toc-accordion-rebuild
    provides: Float-based accordion indicator pattern, ontoggle positional traversal
  - phase: 05-product-cards-redesign
    provides: Inline-block product grid pattern
  - phase: 06-faq-accordion-rebuild
    provides: FAQ accordion matching TOC pattern
  - phase: 07-author-section-floating-buttons
    provides: Text-based social links, HTML entity floating buttons, position:fixed pattern
  - phase: 08-json-ld-schema-hover-audit
    provides: JSON-LD Article+FAQ schema inside article, hover audit
provides:
  - Rebuilt N8N prompt TXT with exact injection block and hipsterstyle branding
  - Updated N8N workflow JSON with all Phase 1 bug fixes applied
  - Two production-ready pipeline files in claude-code/Files/
affects: [phase-10-final-integration-testing]

tech-stack:
  added: []
  patterns: [n8n-keypair-body-encoding, ld-json-script-preservation-regex, source-content-delimiter-injection-mitigation]

key-files:
  created:
    - claude-code/Files/Improved_N8N_Prompt-claude-code-2026-03-25.txt
    - claude-code/Files/Improved_N8N_Workflow-claude-code-2026-03-25.json
  modified: []

key-decisions:
  - "Embedded prompt in Build Final HTML Prompt node kept as separate condensed version (not loaded from TXT file dynamically) -- both versions share the same injection block and brand data but embedded version is optimized for LLM token efficiency"
  - "Clean HTML node preserves application/ld+json scripts via negative lookahead regex while stripping all other scripts unconditionally"
  - "WordPress Publish node switched from raw JSON body interpolation to N8N keypair body encoding to prevent HTML double-quote breakage"
  - "Error Handler connected via continueErrorOutput on Clean HTML and Publish to WordPress nodes instead of errorWorkflow self-reference (N8N limitation)"
  - "Prompt injection mitigation added to Build Blog Brief via source_content delimiters"

patterns-established:
  - "N8N keypair body: use specifyBody:keypair instead of raw JSON interpolation when body contains HTML with double quotes"
  - "LD+JSON preservation: regex negative lookahead to keep application/ld+json scripts while stripping all others"
  - "Prompt injection mitigation: wrap user-supplied content in <source_content> delimiters with instruction to treat as raw text"

requirements-completed: [N8N-01, N8N-02, N8N-03, N8N-04, N8N-05, N8N-06, N8N-07, N8N-08]

duration: 6min
completed: 2026-03-25
---

# Phase 9 Plan 1: N8N Prompt & Workflow Alignment Summary

**Rebuilt N8N prompt TXT and workflow JSON for hipsterstyle.co.il with exact injection block, all Phase 1 audit fixes (CRIT-1/CRIT-2/BUG-1/BUG-4), and template-aligned structure descriptions**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-25T20:47:55Z
- **Completed:** 2026-03-25T20:54:22Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Rebuilt prompt TXT from scratch with hipsterstyle branding, zero oritmartin references, exact CONTEXT.md injection block (no code fences), and template structure matching Phases 3-8
- Fixed all Phase 1 audit contradictions: removed MANDATORY CSS BLOCK (CRIT-1), added JSON-LD schema instructions (CRIT-2), replaced display:flex with float-based WP-safe alternatives (HIGH-1)
- Fixed workflow bugs: Clean HTML unconditional style stripping with ld+json preservation (BUG-1), embedded prompt aligned to new TXT (BUG-2), keypair body encoding for WordPress Publish (BUG-4), error handler connected (BUG-5)
- Updated all 17+ oritmartin references across workflow to hipsterstyle brand data

## Task Commits

Each task was committed atomically:

1. **Task 1: Rebuild N8N prompt TXT for hipsterstyle** - `f7c53dd` (feat)
2. **Task 2: Update N8N workflow JSON aligned to new prompt and template** - `60a2b74` (feat)

## Files Created/Modified
- `claude-code/Files/Improved_N8N_Prompt-claude-code-2026-03-25.txt` - Complete prompt TXT with hipsterstyle branding, exact injection block, template structure instructions, WP-safe CSS patterns
- `claude-code/Files/Improved_N8N_Workflow-claude-code-2026-03-25.json` - N8N workflow JSON with all bug fixes, hipsterstyle brand data, aligned embedded prompt, keypair body encoding

## Decisions Made
- Kept embedded prompt in Build Final HTML Prompt node as condensed version rather than loading TXT dynamically -- avoids adding file-read node complexity, both share same injection block
- Used negative lookahead regex in Clean HTML to preserve ld+json scripts: `/<script(?![^>]*type\s*=\s*["']application\/ld\+json["'])[^>]*>[\s\S]*?<\/script>/gi`
- Switched WordPress Publish from raw jsonBody to keypair body mapping -- N8N handles JSON encoding properly
- Connected Error Handler via continueErrorOutput on Clean HTML and Publish to WordPress nodes (N8N cannot self-reference errorWorkflow without a workflow ID)
- Added prompt injection mitigation to Build Blog Brief using source_content delimiters
- Removed gallery/about/phone/email URLs from Normalize Input (hipsterstyle is a Shopify store, not personal business)
- Updated product relevance keywords from Kabbalah/Sefirot to fashion/kids/style in Rank and Select Top Products

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added prompt injection mitigation to Build Blog Brief**
- **Found during:** Task 2 (Build Blog Brief node update)
- **Issue:** BUG-7 from Phase 1 audit flagged that user-supplied docContent passes directly into LLM prompt without sanitization
- **Fix:** Wrapped source content in `<source_content>` delimiters with instruction to treat content as raw text only
- **Files modified:** claude-code/Files/Improved_N8N_Workflow-claude-code-2026-03-25.json
- **Verification:** Visible in Build Blog Brief jsCode string
- **Committed in:** 60a2b74 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 missing critical -- security)
**Impact on plan:** Essential security improvement from Phase 1 audit. No scope creep.

## Issues Encountered
None

## Known Stubs
None -- both files are complete production artifacts with all placeholder values replaced.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Both pipeline files ready for Phase 10 integration testing
- Prompt TXT and workflow JSON are fully aligned with Phases 3-8 template structure
- All N8N-01 through N8N-08 requirements addressed

## Self-Check: PASSED

- FOUND: claude-code/Files/Improved_N8N_Prompt-claude-code-2026-03-25.txt
- FOUND: claude-code/Files/Improved_N8N_Workflow-claude-code-2026-03-25.json
- FOUND: .planning/phases/09-n8n-prompt-workflow-alignment/09-01-SUMMARY.md
- FOUND: f7c53dd (Task 1 commit)
- FOUND: 60a2b74 (Task 2 commit)

---
*Phase: 09-n8n-prompt-workflow-alignment*
*Completed: 2026-03-25*
