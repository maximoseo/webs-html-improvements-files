# HTML Redesign Mega Skill — Upgrade Spec (v2)

Non-destructive upgrade doc. The working skill lives at multiple command paths already:

- `~/.claude/commands/redesign-html-template.md`
- `~/.claude/commands/mkt/redesign-html-template.md`
- `~/.claude/commands/mkt/write/redesign-html-template.md`

This spec ADDS a new consolidating skill at `~/.claude/skills/redesign-html-template-mega/SKILL.md` that orchestrates existing commands + the 17 sub-skills listed below. Nothing is deleted.

## 17 Sub-skills — status + upgrade actions

Legend: ✅ exists, ⬆ enhanced this batch, 🆕 new this batch.

### Layout & structure
1. **Responsive Layout Fixer** ✅ — existing pattern in `wordpress-html-template-builder`. ⬆ adopt breakpoint tokens from `hue` (auto-extract `--bp-sm/md/lg` per domain).
2. **Dashboard UI Cleaner** 🆕 — port metric-card + sparkline primitives from `marp-slides`. Integrate as `<div data-gz-stat>` blocks.
3. **Box / Row / Alignment System** ✅ — existing. ⬆ adopt `logo-generator-skill`'s proportion rules (40–50 % negative space) as CSS custom-property ranges.
4. **Content Spacing Optimizer** ✅. ⬆ rhythm rubric from `compose_skill` (weighted scorecard with ceilings — perf 35, struct 25, a11y 20, tokens 20).

### Typography & color
5. **Theme Token Engine** 🆕 — token-swap pattern from `html-ppt-skill` (36 themes via one `<link>`, runtime swap via CSS vars). Integrate with `hue` auto-extractor.
6. **Brand Auto-Extractor** 🆕 — wrap `npxskillui` + `hue`. Input: domain URL. Output: `tokens.json` → merged into `redesign-html-template` command.
7. **Accessibility & Contrast Fixer** ✅. ⬆ enforce WCAG AA contrast at token-generation time; reject palettes with ratio < 4.5.

### Interactive primitives
8. **TOC / FAQ Interaction System** ✅ (active in galoz.co.il v15.4.26). ⬆ port chevron rotation pattern as a reusable snippet block.
9. **Modal / Popup UX System** ✅. ⬆ add focus-trap + ESC-close polyfill; keep `<dialog>` as progressive enhancement.
10. **Floating Buttons System** ✅ (3-button stack shipped in galoz rebuild). ⬆ expose `left/right` + RTL auto-swap param so hondabike (left) vs. dtapet (right) reuse same code.
11. **Button & CTA Hierarchy Fixer** ✅. ⬆ adopt `email-campaigns-claude` pill-CTA block styles (frost-glass + black pill), translate to RTL.

### Content modules
12. **Author / Trust Section Builder** ✅. ⬆ social-icon allowlist per domain (galoz = YouTube only; honda = FB + YT, etc.). Registry in `domain-brand-map.json`.
13. **Conversion CTA Engine** ✅. ⬆ add `email-campaigns-claude` card variants + `marp-slides` metric strip as CTA prelude.
14. **WordPress-Safe HTML Generator** ✅. ⬆ allow ONE scoped `<style>` block (galoz build proved safety); add sanitization-safe class allowlist mechanism.
15. **RTL / Hebrew Layout Engine** ✅. ⬆ fold in `inside-lago-voice-skill` brand-voice patterns for Hebrew tone consistency; Heebo/Assistant font priority.

### QA & sync
16. **Preview & Rendering Validator** ✅. ⬆ invoke `agentic-seo-audit` (10 checks A–F grading) on every generated template. Fail-closed at grade < B.
17. **HTML + N8N Sync Engine** ✅. ⬆ nightly re-audit loop (pattern from `friday-showcase`): cron → fetch live WP post → re-grade → open PR if score drops.

### New support modules (not in original 17)
- **Illustration Layer** 🆕 — `svg-hand-drawn-skill` player as optional decorative enhancement. Opt-in per article; OFF by default for WP-safety.
- **Figure Router** 🆕 — `engineering-figure-banana` rule: numeric → plot (Chart.js inline), conceptual → AI image.
- **Post-Publish Monitor** 🆕 — `friday-showcase` cron pattern adapted for article watchdog.

## Integration points with existing artifacts

- Existing `/redesign-html-template` slash command remains the primary entry point. No signature change.
- New skill at `~/.claude/skills/redesign-html-template-mega/SKILL.md` is invoked via `Skill` tool when user says "upgrade" / "mega redesign".
- `domain-brand-map.json` (new) centralizes per-domain brand data (colors, fonts, socials, contact, WP target). Backfill with existing galoz.co.il, dtapet.com, hondabike.co.il entries.

## Non-destructive guarantees

- Existing command files: unchanged.
- Existing skills: unchanged.
- `.claude/skills/` additions are prefixed and do not shadow existing slugs.
- Backups of any replaced file go to `CLAUDE CODE BACKUP/2026-04-20-skill-expansion/`.
