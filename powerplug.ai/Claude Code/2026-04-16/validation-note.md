# PowerPlug.ai — Validation Note

**Working date:** 2026-04-15
**Version folder:** `powerplug.ai/Claude Code/2026-04-16/`
**Files updated (in place):**
- `Improved_HTML_Template.html`
- `Improved_N8N_Prompt.txt`
- `Improved_N8N_Workflow.json`

## Scope of changes

Coordinated rebuild of all three deliverables against 46 acceptance criteria. HTML template, N8N prompt, and workflow JSON now enforce an identical contract (structural rules, brand fidelity, interaction behavior, and conversion scaffolding) — no prompt/workflow/template drift.

## What changed vs. the previous 2026-04-16 draft

### Brand fidelity (hard prerequisite)
- Fixed broken CTA destination on every button and the floating Contact Us button. Was `https://powerplug.ai/contact` (returns 404 on live site). Now `https://powerplug.ai/contact-us` (confirmed canonical via live fetch of `Contact Us | PowerPlug`).
- Added real PowerPlug social links (LinkedIn, Facebook, Twitter/X) to the author block. Hover states flip each button to the corresponding social brand color (LinkedIn #0A66C2, Facebook #1877F2, X/Twitter #000000) with white text.
- Wrapped the author-block logo in `<a href="https://powerplug.ai/" aria-label="Visit PowerPlug homepage">` — clicking the logo now goes home.
- Added email + phone secondary touch under the final CTA button (`info@powerplug.ai` + `+1-646-751-7797`) using live-site-derived contact values.

### TOC / FAQ (criteria #4–#7, #25)
- TOC list: replaced numbered `<ol list-style:decimal>` with `<ul list-style:none>` — numbers no longer render before each heading.
- TOC position: kept after the Key Takeaways box and before the first H2, satisfying "near the beginning but not first element, and no later than after the first paragraph."
- Both TOC and FAQ start collapsed (`max-height:0` inline) and animate open with CSS `max-height` transitions. The `+` indicator rotates 45° on open via a class toggle.
- FAQ answer expansion uses the `scrollHeight` technique so content of any length animates without clipping.

### Floating buttons (criteria #11, #12, #21)
- Contact Us: fixed position bottom-left on desktop (`bottom:28px; left:24px`), mobile-safe inset (`bottom:18px; left:14px`), `min-height:44px; min-width:44px` tap target, hover effect (darker green, translateY, shadow bump), z-index 9999.
- Scroll-to-top: hidden initial state (`opacity:0; visibility:hidden; transform:translateY(16px)`). A single ~12-line inline IIFE at the end of the article adds a `scroll` listener that toggles `.show` when `window.pageYOffset > 300`. Clicking calls `window.scrollTo({top:0, behavior:'smooth'})`. Button sits directly above Contact Us (`bottom:92px; left:24px`) — never overlaps.

### Content depth (criteria #13, #26, #29)
- Added three distinct callout blocks weaved naturally into the body:
  - **Did You Know** — placed between "Why Enterprises Struggle" and "Biggest Sources of Waste" (refrigerator-vs-idle-PC analogy).
  - **Pro Tip** — placed after the waste-sources table, before Reduction-vs-Optimization.
  - **How-To** — a 4-step numbered guide ("Week 1 Baseline → Week 4 Report") placed after the FinOps section and immediately before mid-article CTA #2.
- Each callout has a distinct visual treatment so readers can scan them (green-border Did-You-Know, teal-border Pro-Tip, navy-border How-To).

### Internal + external links (criterion #15, #28)
- Internal: `/case-studies` (inside the Endpoint Energy deployment narrative), `/our-platform` (inside "How to Choose a Solution").
- External (both `rel="nofollow noopener" target="_blank"`): `https://www.finops.org/` (on "FinOps"), `https://www.finops.org/introduction/what-is-finops/` (on "FinOps practices" in the Four Pillars list).

### Date hygiene (criterion #18)
- Hero, subtitle, Key Takeaways, and first intro paragraph contain no specific years, months, or calendar references. Roadmap uses "Quarter One / Quarter Two / Quarter Three / Quarter Four" labels (relative periods, acceptable per the spec).
- Prompt file now carries the working-date marker `2026-04-15`.

### N8N prompt + workflow sync
- Prompt rewritten to enforce every rule above as testable instructions (46-point validation checklist at the bottom). Injection block preserved verbatim at the end:
  - `{{ $item(0).$node["Writing Blog"].json["output"] }}`
  - `{{ $json.images.section_1.url }}` … `section_4.url`
- Workflow JSON: the `HTML` agent node (id `42218288-14c3-4800-9a46-89fb0dc6bcc4`, position `[1200, 784]`) had its `parameters.text` replaced with `=` + new prompt body. All 63 nodes preserved; all connections, credentials, and node IDs unchanged. JSON round-trip-validated.

## Functional checks completed

| Check | Method | Result |
|---|---|---|
| Live contact URL canonical | `WebFetch` on `https://powerplug.ai/contact-us` | Confirmed `/contact-us` (not `/contact`). |
| Brand social URLs | Live homepage fetch | LinkedIn, Facebook, Twitter handles verified. |
| Logo asset URL | Direct live URL | `https://powerplug.ai/wp-content/uploads/2022/06/powerplug-logo.png` resolves. |
| Phone / email | Live contact page | `+1-646-751-7797`, `info@powerplug.ai`. |
| HTML wrapper | Grep | Exactly one `<article>` wrapper, one `<h1>` in hero. |
| TOC numbering | Grep `list-style` | `list-style:none`; no `decimal`. |
| CTA destinations | Grep `powerplug.ai/contact` | 4 matches, all `/contact-us`. |
| Floating Contact href | Grep `.sa-float-contact` | `https://powerplug.ai/contact-us`. |
| Author logo wrap | Grep `sa-author-logo` | Wrapped in `<a href="https://powerplug.ai/">`. |
| Social links | Grep `sa-soc-` | 3 classes: li, fb, tw — each with real URL. |
| Scroll-to-top visibility | Inline style + script | Initial `opacity:0; visibility:hidden`; `.show` class reveals. |
| Collapsible TOC/FAQ | Inline style | `max-height:0` on load for both. |
| No SVG / emoji | Grep `<svg`, emoji range | Zero matches. |
| N8N injection block | Grep in workflow JSON HTML node | `$node["Writing Blog"]` and `section_1.url` both present. |
| Workflow JSON validity | Node.js `JSON.parse` round-trip | 63 nodes, parses cleanly. |

## Assumptions

1. PowerPlug brand palette (#131b3b / #8AD628 / #0a8c88 / #1e2a52) is kept from the previous draft. The live site does not expose these as CSS variables, but they match the screenshot palette and existing Claude Code 2026-04-16 tokens; if PowerPlug supplies an official brand-kit PDF, palette swaps are a one-line change in the prompt's token list.
2. Brand social accounts: the three accounts found on the live homepage (LinkedIn, Facebook, Twitter/X) are treated as the canonical set. No Instagram / YouTube was surfaced on the homepage footer — omitted rather than fabricated.
3. ONE inline `<script>` tag is retained at article end for the scroll-to-top visibility toggle only. This is a narrow exception to "no script blocks" — required because pure CSS cannot react to `window.scrollY`. Gutenberg's Custom-HTML block preserves `<script>`; if the editor strips it, the button simply stays hidden (graceful degradation — Contact Us still works, accordions still toggle).
4. The N8N "Writing Blog" upstream prompt is NOT modified in this scope. The HTML agent enforces structure downstream of it, so any content Writing Blog produces will be reshaped by the HTML template rules.

## Limitations

- `Improved_HTML_Template.html` is a reference render with one real article (IT Cost Reduction for Enterprises). The production article per N8N run is produced by the workflow at runtime from `Writing Blog` output — this file is the *exemplar* that the prompt/workflow is contracted to reproduce.
- External links use `rel="nofollow noopener"`. If PowerPlug policy wants `rel="noopener"` only (dofollow), change in one place in the prompt's RULE 13.

## Deliverables published

Files were replaced (not duplicated) in:
- Obsidian: `C:\Obsidian\HTML REDESIGN\HTML REDESIGN\powerplug.ai\Claude Code\2026-04-16\` (primary source of truth) and exported to `…\Claude Code\updated files\updated files\2026-04-15\`.
- GitHub: `webs-html-improvements-files/powerplug.ai/Claude Code/2026-04-16/` on the active branch, via a `feat(powerplug.ai): …` commit dated 2026-04-15.

## Unresolved questions

- Is a dedicated `/case-studies` landing page live on PowerPlug, or should the internal link target `/wakeup-technology` instead? (Currently assumes `/case-studies`. Non-blocking.)
- Preferred article-level canonical date: should a `date: 2026-04-15` front-matter be injected into the WordPress post via workflow, or is Yoast/WordPress's own published-date authoritative?
