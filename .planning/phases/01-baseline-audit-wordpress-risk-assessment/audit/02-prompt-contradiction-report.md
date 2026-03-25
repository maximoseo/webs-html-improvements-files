# N8N Prompt Contradiction & Issue Report

**File audited:** `wp-n8n-html-design-improver/Improved_N8N_Prompt-claude-code-2026-03-25.txt`
**Total lines:** 331
**Audit date:** 2026-03-25
**Cross-referenced with:** HTML template (`Improved_HTML_Template-claude-code-2026-03-25.html`), Workflow JSON

---

## 1. Executive Summary

| Severity | Count | Description |
|----------|-------|-------------|
| CRITICAL | 2 | Direct internal contradictions that guarantee failure or undefined behavior |
| HIGH | 3 | Hardcoded brand data, WordPress-unsafe patterns, prompt-to-template drift |
| MEDIUM | 3 | QA checklist contradictions, ambiguous CSS instructions, N8N expression syntax concerns |

**Overall Prompt Health:** POOR. The prompt contains two self-defeating contradictions (style block mandated AND forbidden; JSON-LD forbidden but template includes it). All site-specific data is hardcoded for oritmartin.com and must be parameterized for hipsterstyle.co.il. The prompt instructs the LLM to produce `display:flex` and `display:inline-flex` patterns that WordPress `wp_kses_post()` strips.

---

## 2. CRITICAL Contradictions

### CRIT-1: Style Block Contradiction (4 conflicting instructions)

The prompt simultaneously mandates and forbids a `<style>` block. An LLM following this prompt cannot satisfy all instructions.

| Side | Line | Exact Text | Instruction |
|------|------|-----------|-------------|
| A (mandate) | Line 18 | `Inline CSS on each element PLUS one <style> block inside the article for hover and accordion effects` | Include one style block |
| A (mandate) | Line 29 | `Place this exact style block immediately after the opening <article> tag` | Include exact style block |
| A (mandate) | Lines 31-44 | Full `<style>` block with 13 CSS rules | Exact CSS to include |
| B (forbid) | Line 282 | `No html, head, body, or style wrapper` | No style wrapper |
| B (forbid) | Line 292 | `Style blocks.` (listed under FORBIDDEN PATTERNS) | Style blocks forbidden |
| B (forbid) | Line 320 | `No style block exists.` (in QA CHECKLIST) | Style block must not exist |

**Impact:** The LLM must either obey Lines 18/29-44 (include style block) or Lines 282/292/320 (forbid style block). It cannot do both. In practice, the current HTML template DOES include the style block (template lines 2-14), meaning the "mandate" side won. But the QA checklist at Line 320 would fail its own check.

**Cascading Impact:** The N8N workflow "Clean HTML for WordPress" node (workflow line 302) has code that tries to preserve the `#om-top` style block and then throws an error if any style block exists. This means even if the LLM correctly includes the mandated style block, the workflow rejects it.

**Resolution Strategy:** Remove the MANDATORY CSS BLOCK section (Lines 28-44) and the style block instruction at Line 18. Keep Lines 282, 292, 320 as authoritative. All hover/accordion effects must use inline `onmouseover`/`onmouseout` handlers and `ontoggle` (which the prompt already instructs at Lines 168, 227). This aligns with WordPress reality: `wp_kses_post()` strips `<style>` blocks.

---

### CRIT-2: JSON-LD Contradiction (prompt forbids, template includes)

| Side | Line/File | Exact Text | Instruction |
|------|-----------|-----------|-------------|
| A (forbid) | Prompt Line 26 | `No JSON-LD block at the end. The author section must remain the final section.` | No JSON-LD |
| B (include) | Template Lines 312-319 | Three `<script type="application/ld+json">` blocks (Article, LocalBusiness, FAQPage) | JSON-LD present after author section |

**Impact:** The prompt instructs no JSON-LD, but the current template includes 3 JSON-LD blocks after the author section (Lines 312-319). This violates two rules: (1) no JSON-LD, and (2) nothing after the author section.

**Resolution Strategy:** Decide whether JSON-LD is desired. If yes, remove Line 26 prohibition and add explicit JSON-LD instructions. If no, remove template Lines 312-319. Recommendation: Keep JSON-LD (valuable for SEO) but move it before the author section or make an explicit exception in the prompt.

---

## 3. HIGH Issues

### HIGH-1: Prompt Instructs WordPress-Unsafe CSS Patterns

The prompt instructs the LLM to generate CSS patterns that `wp_kses_post()` strips.

| Line | Instruction | WordPress Impact |
|------|-------------|------------------|
| Line 167 | TOC summary: `display:flex with justify-content:space-between` | `display` property NOT on `safe_style_css` whitelist -- stripped |
| Line 226 | FAQ summary: same `display:flex` instruction | Same -- stripped |
| Line 262 | Social links: `<span style="display:inline-flex;align-items:center;gap:6px;">` | `display:inline-flex` stripped |
| Line 276 | `Layout: fluid and responsive using ... auto-fit grids when needed` | `display:grid` stripped |

**Impact:** Every flex/grid layout instruction in the prompt produces HTML that collapses to default browser stacking when WordPress filters the content. The accordion indicator (+) loses its right-aligned positioning. Product grids collapse to single column. Author section buttons lose horizontal layout.

**Resolution Strategy:** Replace all `display:flex` instructions with float-based or `text-align:center` + margin alternatives. Replace grid instructions with percentage-width `inline-block` approaches. All flex child properties (`align-items`, `justify-content`, `gap`) ARE on the whitelist but are useless without `display:flex`.

---

### HIGH-2: All oritmartin.com Hardcoded Data in Prompt

Every site-specific reference in the prompt is hardcoded for oritmartin.com. For hipsterstyle.co.il deployment, all must change.

| Lines | Category | Current Value | Count |
|-------|----------|---------------|-------|
| Line 1 | Title | `ORIT MARTIN ARTICLE SYSTEM` | 1 |
| Line 5 | Role | `Orit Martin's WordPress article pipeline` | 1 |
| Lines 59-62 | Site URLs | `oritmartin.com`, `/about`, `/gallery`, `/contact` | 4 |
| Line 63 | Phone | `+972587676321` | 1 |
| Line 64 | Email | `orit-26@netvision.net.il` | 1 |
| Line 65 | Facebook | `facebook.com/...orit-martin-1430061693883873/` | 1 |
| Line 66 | Instagram | `instagram.com/orit_martin_spiritual_art/` | 1 |
| Line 67 | Portrait | `supabase.co/.../oritmartin/author-portrait.jpeg` | 1 |
| Line 107 | Purpose | `Orit Martin's real gallery` | 1 |
| Line 208 | CTA | `contacting Orit` + `oritmartin.com/contact` | 1 |
| Line 240 | CTA target | `Orit Martin destination` | 1 |
| Line 250 | Float btn | `oritmartin.com/contact` | 1 |
| Line 257 | Portrait | Supabase URL with `oritmartin` path | 1 |
| Line 259 | Bio | `Orit Martin's name, Jerusalem/Har Nof` | 1 |
| Line 260 | Contact | Phone + email hardcoded | 1 |
| Line 261 | Button | `oritmartin.com/about` | 1 |
| Lines 269-277 | Design | Brand colors (#C4A265 accent, #f8f6f3 bg) | Section |

**Total oritmartin references in prompt:** 18+ direct occurrences across 20 lines.

**Resolution Strategy:** Extract all brand-specific data into a variables section at the top of the prompt that can be swapped per-client. Or inject via N8N expressions from the "Normalize Input" node.

---

### HIGH-3: Prompt-to-Template Drift

Instructions in the prompt that don't match what the template actually contains.

| Feature | Prompt Instruction | Template Reality | Drift |
|---------|-------------------|------------------|-------|
| Style block | Line 18: "one `<style>` block" | Template Lines 2-14: style block present (but missing `summary{list-style:none}` rule from prompt Line 41) | Partial match -- template style block has 12 rules, prompt specifies 13 |
| JSON-LD | Line 26: "No JSON-LD block" | Template Lines 312-319: 3 JSON-LD blocks | CONTRADICTION |
| Floating Contact link | Line 250: `/contact` | Template Line 286: links to `/contact` | Match |
| WhatsApp button | Not mentioned in prompt | Template Lines 308-310: WhatsApp floating button present | DRIFT -- template has element not in prompt |
| Inline CTA banners | Lines 206-212: "exactly 2 soft CTA banners" | Template Lines 192-196, 214-221: 2 CTA banners present | Match |
| TOC closed default | Line 161: "closed by default" | Template Line 31: no `open` attribute | Match |
| Author portrait circle | Line 258: "110px circle, 3px solid #C4A265" | Template Line 293: matches exactly | Match |

---

## 4. MEDIUM Issues

### MED-1: QA Checklist Items Contradict Body Instructions

| QA Line | QA Says | Body Line | Body Says | Contradiction |
|---------|---------|-----------|-----------|---------------|
| Line 320 | "No style block exists" | Line 18, Lines 29-44 | Include style block | YES (part of CRIT-1) |
| Line 313 | "At least one real artwork image appears when justified" | Line 136 | "Optional artwork/product grid if justified" | Ambiguous -- QA implies required, body says optional |
| Line 319 | "Nothing appears after the author section" | Template Lines 308-319 | WhatsApp button + 3 JSON-LD blocks after author | YES -- template violates this |

### MED-2: Ambiguous or Conflicting CSS Instructions

| Line A | Says | Line B | Says | Ambiguity |
|--------|------|--------|------|-----------|
| Line 18 | "Inline CSS on each element PLUS one style block" | Line 120 | "Keep all CSS inline on each element" | Confusing -- is it inline + style, or inline only? |
| Line 115 | "DO include onmouseover, onmouseout, and ontoggle handlers" | Line 121 | "Every link and button must look styled and complete WITHOUT any JavaScript handlers" | Not contradictory but confusing -- both true simultaneously |
| Line 167 | Summary must use `display:flex` | Line 282 | No style wrapper (could be read as no inline style blocks) | Indirect tension |

### MED-3: N8N Expression Syntax

| Line | Expression | Status |
|------|-----------|--------|
| Line 83 | `{{ JSON.stringify($json["products"], null, 2) }}` | VALID -- standard N8N expression |
| Line 86 | `{{ $("Writing Blog").first().json.output }}` | VALID -- references "Writing Blog" node by name |
| Line 92-96 | `{{ $("Preparing Images for HTML").first().json.images.section_N.url }}` | VALID -- references node output correctly |

**Note:** Expression syntax is correct, but all node references are string-name-based. If node names change in the workflow, these expressions silently fail with undefined. The locked block instruction (Lines 70-80) correctly prevents modification of these expressions.

---

## 5. Cross-File Drift Matrix

| Feature | Prompt Says | Template Has | Match? | Issue |
|---------|-------------|-------------|--------|-------|
| Style block | Lines 18, 29-44: MANDATORY + Line 292: FORBIDDEN | Lines 2-14: Present | CONFLICT | Prompt contradicts itself; template follows mandate side |
| JSON-LD | Line 26: No JSON-LD | Lines 312-319: 3 blocks | CONFLICT | Template violates prompt |
| Accordion structure | Lines 161-170: details/summary, closed, +indicator | Lines 31-46: Correct implementation | MATCH | -- |
| Product cards | Lines 172-183: object-fit:contain, no crop | Lines 48-103: 6 cards with correct img styling | MATCH | -- |
| Floating buttons | Lines 244-252: Contact + Back to Top on left side | Lines 286-290: Contact + Back to Top on left | MATCH | -- |
| WhatsApp button | Not mentioned | Lines 308-310: WhatsApp on right side | DRIFT | Template adds unrequested element |
| Author section | Lines 254-265: final section, portrait, socials | Lines 292-306: Matches requirements | MATCH | -- |
| Social links | Lines 262-263: Facebook + Instagram with SVG | Lines 303-304: Both present with SVG | MATCH | -- |
| RTL handling | Not explicitly detailed beyond `dir="rtl"` | Line 1: `dir="rtl"` on article | PARTIAL | Prompt could be more explicit about RTL layout implications |
| Heading hierarchy | Line 196: "strong H2 hierarchy, optional H3" | Template: 6 H2 sections, no H3 | MATCH | -- |
| Summary card | Lines 152-157: 4-6 bullets | Lines 19-29: 6 bullets | MATCH | -- |
| CTA banners | Lines 206-212: exactly 2 | Lines 192-196, 214-221: 2 banners | MATCH | -- |

---

## 6. N8N Expression Audit

Every `{{ }}` expression found in the prompt file:

| Line | Expression | Purpose | Syntax Valid? | Node Reference |
|------|-----------|---------|---------------|----------------|
| 83 | `{{ JSON.stringify($json["products"], null, 2) }}` | Inject products JSON | YES | Current item's `products` field |
| 86 | `{{ $("Writing Blog").first().json.output }}` | Inject article content | YES | "Writing Blog" node output |
| 92 | `{{ $("Preparing Images for HTML").first().json.images.section_1.url }}` | Section image 1 URL | YES | "Preparing Images for HTML" node |
| 93 | `{{ $("Preparing Images for HTML").first().json.images.section_2.url }}` | Section image 2 URL | YES | Same node |
| 94 | `{{ $("Preparing Images for HTML").first().json.images.section_3.url }}` | Section image 3 URL | YES | Same node |
| 95 | `{{ $("Preparing Images for HTML").first().json.images.section_4.url }}` | Section image 4 URL | YES | Same node |
| 96 | `{{ $("Preparing Images for HTML").first().json.images.hero.url }}` | Hero image URL | YES | Same node |

**Total expressions:** 7
**All syntax valid:** YES
**Risk:** Node name coupling. If "Writing Blog" or "Preparing Images for HTML" nodes are renamed in the workflow, all expressions silently return undefined. The locked block instruction (Lines 70-80) correctly protects against accidental modification.

---

## 7. Recommendations for Phase 9 (Priority Order)

1. **[P0] Remove MANDATORY CSS BLOCK entirely** (Lines 28-44). Remove style block instruction from Line 18. All hover/accordion effects must use `onmouseover`/`onmouseout`/`ontoggle` inline handlers (already instructed at Lines 168, 227, 241). This resolves CRIT-1 and aligns with WordPress reality.

2. **[P0] Resolve JSON-LD policy** -- either add explicit JSON-LD instructions (recommended for SEO) or enforce the Line 26 prohibition. If keeping JSON-LD, update Line 26 and Line 305 ("Nothing after author section") to allow it.

3. **[P0] Replace all `display:flex` instructions** with WordPress-safe alternatives. Lines 167, 226, 262 must use float-based or `text-align:center` approaches. Document the `display` property gap in the prompt's WordPress Hardening section.

4. **[P1] Parameterize all oritmartin.com references.** Extract the MANDATORY SITE FACTS section (Lines 57-68) into variables that can be injected per-client. Move brand-specific instructions (Lines 107, 208, 240, 250, 257-261) to use these variables.

5. **[P1] Remove WhatsApp button from template** or add it to prompt instructions. Current state is undocumented drift.

6. **[P2] Strengthen QA CHECKLIST** (Lines 307-323) to not contradict body instructions. Remove Line 320 ("No style block exists") if style block is kept, or keep it if style block is removed.

7. **[P2] Add explicit RTL layout instructions.** Currently only `dir="rtl"` is mentioned. Prompt should specify right-to-left reading order for accordion indicators, float directions, and border accents.

8. **[P2] Add WordPress CSS survival note.** Include a section listing which CSS properties survive `wp_kses_post()` and which don't, so the LLM avoids generating stripped patterns.

9. **[P3] Consider parameterizing brand colors.** Lines 269-277 hardcode #C4A265 (gold accent), #f8f6f3 (bg), etc. If the pipeline serves multiple brands, these should be injectable.

---

*Report generated from direct line-by-line analysis of `Improved_N8N_Prompt-claude-code-2026-03-25.txt` (331 lines). All line numbers verified via grep.*
