# Merge Report — 2026-04-20 Ingestion

## Summary

- 35 URLs processed
- 2 unreachable (4 tier)
- 9 new installs (1 tier)
- 7 referenced but not installed (2 tier)
- 17 catalog-only (3+4 tier)
- **ZERO deletions. ZERO overwrites.**

## Duplicates found and resolved

### Alias / already-in-catalog

| Incoming | Existing | Action |
|---|---|---|
| `midudev/autoskills` | `autoskills` (prior batch 2026-04-18 b4+5) | SKIP — marked as deduped in registry |
| `amaancoderx/npxskillui` | `npxskillui` (in skill list) | REFRESH alias → add to install plan as `skillui-cli` |
| `revfactory/harness` | `agent-harness-construction` (existing) | REFERENCE — keep existing; steal meta-team pattern |

### Methodology overlap (multiple SDD variants)

| Incoming | Existing | Action |
|---|---|---|
| `LIDR-academy/manual-SDD` | `spec-driven` skill | REFERENCE — document in ingestion memo; no new install |
| `LichAmnesia/lich-skills` (spec-driven subset) | `spec-driven` skill | REFERENCE — cross-link in memo |

### Pattern borrow (no duplicate)

| Source | Pattern adopted | Where it lands |
|---|---|---|
| `html-ppt-skill` | Token-swap theming | HTML Mega Skill sub-skill 5 |
| `hamen/compose_skill` | Weighted scorecard with ceilings | HTML Mega Skill sub-skill 4 |
| `logo-generator-skill` | 40–50% negative space proportion rule | HTML Mega Skill sub-skill 3 |
| `marp-slides` | Inline SVG chart primitives | HTML Mega Skill sub-skill 2 (new) |
| `hue` | URL → design system tokens | HTML Mega Skill sub-skill 6 |
| `email-campaigns-claude` | Frost-card + pill-CTA blocks | HTML Mega Skill sub-skill 11 |
| `agentic-seo` | 10-check AEO audit A–F | HTML Mega Skill sub-skill 16 |
| `svg-hand-drawn-skill` | Animated SVG player | HTML Mega Skill new Illustration Layer |
| `engineering-figure-banana` | Numeric→plot / conceptual→image routing | HTML Mega Skill new Figure Router |
| `friday-showcase` | Cron-based autonomy pattern | HTML Mega Skill new Post-Publish Monitor |
| `revfactory/harness` | Multi-agent team factory | Future orchestration layer (not integrated yet) |
| `WoJiSama/skill-based-architecture` | Canonical folder structure | Guidance only — applies to mega skill layout |
| `AMAP-ML/SkillClaw` | Skill auto-evolution (cross-session) | Parked — non-destructive concerns |

## Conflict resolution

| Conflict | Resolution |
|---|---|
| Old rule "no `<style>` blocks" vs. new evidence (galoz v15.4.26 shipped with one) | CHANGED rule: allow ONE scoped block via `article[dir="rtl"]` selectors |
| Old rule "no classes" vs. new need for hover + responsive | CHANGED rule: allowlist of `galoz-*` / `{domain}-*` prefixed classes |
| Old "products optional" vs. new "products mandatory (6)" for e-com | CHANGED rule: e-com domains require 6 products; editorial domains unchanged |
| Social-icon rendering (5 networks assumed) vs. live-site reality (varies per brand) | NEW: per-domain allowlist in `domain-brand-map.json` |

## Backup strategy

All pre-existing files that would be touched go to:
```
CLAUDE CODE BACKUP/2026-04-20-skill-expansion/{original-path-mirror}
```

Nothing has been backed up in this batch because the ONLY file creation is:
- `~/.claude/skills/redesign-html-template-mega/SKILL.md` (NEW path — no conflict)
- `plans/reports/*.md` (NEW files)

## Deferred decisions

- Whether to install the full `harness` multi-team factory plugin (complex, ~50 agents worth)
- Whether to wire `agentic-seo-audit` as a CI hook or advisory
- Whether `SkillClaw` auto-evolution is safe enough to enable (risks non-destructive guarantee)

## No-regression validation

- Existing `redesign-html-template` commands: **unchanged** (3 files verified on disk)
- Existing `wordpress-html-template-builder` SKILL: **unchanged**
- Existing `n8n-workflow-map.json`: new entry added, old entries intact
- No file in `~/.claude/skills/` has been modified in this batch

## Unresolved

- Confirm correct owner for `hamen/material-3-skill` (404 on main + master)
- Confirm `bchao1/paper-finder` is genuinely deleted vs. private
