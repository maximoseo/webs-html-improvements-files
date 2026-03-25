# Phase 10: QA Validation & File Delivery - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Final QA validation of all 3 deliverables, WordPress rendering risk review, responsive testing verification, file packaging with correct dated names, local save to ./claude-code/Files/, and Dropbox upload.

</domain>

<decisions>
## Implementation Decisions

### QA Validation (locked by spec)
- Desktop, tablet, mobile responsive validation
- WordPress rendering safety: zero style blocks, zero classes, zero display property
- Product cards: image above text, uniform size, no overlay
- TOC: correct position, anchors work, closed default
- FAQ: before author, closed default, no numbering
- Floating buttons: no overlap, professional
- Hover states: polished, readable, no hidden text
- Plus/minus indicators: correct WordPress rendering

### File Delivery (locked by spec)
- 3 files dated exactly 2026-03-25 with -claude-code- suffix
- Local path: ./claude-code/Files/
- Dropbox target: /Webs/HTML IMPROVMENT FILES/hipsterstyle.co.il/claude-code/Files
- Delete old files from Dropbox before upload
- Upload only final validated files

### Final Report (locked by spec)
- Before/after audit summary
- WordPress risks found and mitigated
- What was improved in each file
- Whether Supabase was used
- Whether real social profiles/YouTube were found
- Confirmation of file names, Dropbox status, local directory

### Claude's Discretion
- QA validation methodology (automated grep checks vs manual review)
- Report format and level of detail

</decisions>

<code_context>
## Files to Validate

### Deliverables in claude-code/Files/
- Improved_HTML_Template-claude-code-2026-03-25.html
- Improved_N8N_Prompt-claude-code-2026-03-25.txt
- Improved_N8N_Workflow-claude-code-2026-03-25.json

### Validation Checks
- HTML: zero style blocks, zero classes, zero display, article wrapper, RTL, all sections present
- TXT: exact injection block present, no extra injection lines, no oritmartin refs
- JSON: valid JSON, no oritmartin refs, node names match injection expressions

</code_context>

<specifics>
## Specific Ideas

Dropbox upload may require Dropbox API or manual upload if no API access.

</specifics>

<deferred>
## Deferred Ideas

None

</deferred>
