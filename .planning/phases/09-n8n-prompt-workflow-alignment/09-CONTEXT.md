# Phase 9: N8N Prompt & Workflow Alignment - Context

**Gathered:** 2026-03-25
**Status:** Ready for planning

<domain>
## Phase Boundary

Rebuild the N8N prompt TXT file aligned to the new template structure. Update the N8N workflow JSON to match. Must contain the EXACT injection block specified in requirements. Two-phase LLM generation pattern.

</domain>

<decisions>
## Implementation Decisions

### N8N Prompt TXT (NON-NEGOTIABLE injection block)
The prompt MUST contain this EXACT block — no additions, no modifications:

```
### מוצרים זמינים:
{{ JSON.stringify($json["products"], null, 2) }}

### תוכן הכתבה:
{{ $("Writing Blog").first().json.output }}

חובה! להקפיד לשים במאמר הקישורים החיצוניים וגם הקישורים הפנימיים כמו שקיבלת בתוכן הכתבה.

### תמונות זמינות:
Section image 1 URL: {{ $("Preparing Images for HTML").first().json.images.section_1.url }}
Section image 2 URL: {{ $("Preparing Images for HTML").first().json.images.section_2.url }}
Section image 3 URL: {{ $("Preparing Images for HTML").first().json.images.section_3.url }}
Section image 4 URL: {{ $("Preparing Images for HTML").first().json.images.section_4.url }}
Hero image URL:      {{ $("Preparing Images for HTML").first().json.images.hero.url }}
```

### Prompt Content Rules
- No extra JSON/N8N injection lines beyond the specified block
- HTML and CSS instructions ARE allowed in the prompt
- The prompt describes the new template structure to the LLM
- Must reference inline CSS only, no style blocks
- Must describe WordPress-safe patterns
- Remove all oritmartin.com references — use hipsterstyle.co.il

### Workflow JSON Rules
- Update embedded prompt node to match new TXT file
- Fix the Clean HTML node contradiction (from Phase 1 audit)
- Two-phase LLM generation: content then HTML rendering
- Update all oritmartin references to hipsterstyle
- Align node names with the injection block expressions

### Claude's Discretion
- Exact prompt wording for HTML generation instructions
- Workflow node configuration details
- Error handling in workflow nodes

</decisions>

<code_context>
## Existing Code Insights

### Baseline Files to Rebuild From
- wp-n8n-html-design-improver/Improved_N8N_Prompt-claude-code-2026-03-25.txt (322 lines — has contradictions from Phase 1 audit)
- wp-n8n-html-design-improver/Improved_N8N_Workflow-claude-code-2026-03-25.json (683 lines — has logic bugs from Phase 1 audit)

### Phase 1 Audit Findings
- Prompt contradictions: style block mandated AND forbidden
- Workflow bugs: Clean HTML node self-contradicting logic
- 24+ oritmartin.com references across prompt, 17+ in workflow

### New Template Structure (Phase 3-8)
- claude-code/Files/Improved_HTML_Template-claude-code-2026-03-25.html — the completed template to describe in prompt

</code_context>

<specifics>
## Specific Ideas

The prompt should describe the exact HTML structure built in Phases 3-8 so the LLM generates matching output.

</specifics>

<deferred>
## Deferred Ideas

None

</deferred>
