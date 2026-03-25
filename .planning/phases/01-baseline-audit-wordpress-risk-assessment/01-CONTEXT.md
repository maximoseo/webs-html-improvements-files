# Phase 1: Baseline Audit & WordPress Risk Assessment - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Audit the existing HTML template, N8N prompt TXT, and N8N workflow JSON for WordPress-unsafe patterns. Document every issue with line numbers and fix strategies. Produce a before-state audit summary and WordPress rendering risk review.

</domain>

<decisions>
## Implementation Decisions

### Claude's Discretion
All implementation choices are at Claude's discretion — pure infrastructure/audit phase. Key focus areas:
- Identify every `<style>` block, class-based selector, and external dependency
- Check wp_kses_post() impact on existing HTML patterns
- Review N8N expression syntax and node references for correctness
- Document RTL alignment risks
- Prioritize changes by WordPress rendering impact severity

</decisions>

<code_context>
## Existing Code Insights

### Baseline Files
- `wp-n8n-html-design-improver/Improved_HTML_Template-claude-code-2026-03-25.html` (307 lines)
- `wp-n8n-html-design-improver/Improved_N8N_Prompt-claude-code-2026-03-25.txt` (322 lines)
- `wp-n8n-html-design-improver/Improved_N8N_Workflow-claude-code-2026-03-25.json` (683 lines)

### Known Issues from Research
- Lines 2-18 of HTML template contain a `<style>` block that WordPress strips
- Hover transitions for `.om-icon`, `.om-toc-link`, `.om-card`, `.om-float-btn`, `.om-cta` will silently disappear
- CSS properties like `display:flex`, `display:grid` may not survive wp_kses_post()
- `<details>/<summary>` tags may not survive on all WordPress setups

### Integration Points
- WordPress target: mahsan.websreport.net
- Main site: hipsterstyle.co.il
- Existing template uses oritmartin.com references that need updating to hipsterstyle

</code_context>

<specifics>
## Specific Ideas

No specific requirements — infrastructure/audit phase. Follow research findings from STACK.md and PITFALLS.md.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>
