# Memo — Skill Ingestion 2026-04-20 0508

## TL;DR

35 GitHub sources processed. 9 installed. 7 referenced. 17 catalog-only. 2 unreachable.
HTML Redesign Mega Skill gets 7 new sub-skill patterns (brand auto-extract, token-swap theming, SVG motion, chart/image routing, AEO post-audit, scorecard rubric, nightly re-audit).

## Key decisions

1. **Depth policy**: strategic deep on 12 HTML-redesign-relevant repos; shallow one-liner on 23. Saves ~5× tokens vs. uniform-deep.
2. **Non-destructive**: NOTHING existing is overwritten. New mega skill lives at `redesign-html-template-mega` (new slug). Existing commands preserved.
3. **WordPress safety**: based on evidence from galoz.co.il v15.4.26 rebuild, the mega skill now formally allows ONE scoped `<style>` block. Old rule "no `<style>` block" was too strict.
4. **Brand allowlist**: social-icon rendering per domain gated on `domain-brand-map.json`. Galoz shows YouTube only (live scrape confirmed no FB/IG/LI/TT/X). Other domains will get their own entries.
5. **QA gate**: `agentic-seo-audit` (addyosmani) becomes a pre-publish hook. Fail-closed at grade < B.

## Conflicts with existing patterns

| Old rule | New decision | Evidence |
|---|---|---|
| "No `<style>` blocks in HTML output" | Allow ONE scoped block via `article[dir="rtl"]` | galoz build shipped; survived WP sanitization |
| "All classes forbidden" | Allowlist of 15 `galoz-*` classes | Same |
| "Products optional" | Products MANDATORY (min 6) for e-com articles | User explicit 2026-04-20 |
| "FB/IG/LI/YT/TT sockets always" | Per-domain allowlist from `domain-brand-map.json` | Avoids empty icons |

## What changed in user auto-memory

New index entry pending (add via next memory update):
- `[Reference — Skill Expansion 2026-04-20](reference_skill-expansion-2026-04-20.md) — 9 new skills integrated from 33 reachable repos (2 unreachable). HTML Redesign Mega Skill upgraded to v2 with 7 new sub-skill patterns (brand auto-extract, token theming, SVG motion, chart/image routing, AEO audit, scorecard rubric, nightly re-audit). Non-destructive. Backup at CLAUDE CODE BACKUP/2026-04-20-skill-expansion/`

## Open decisions for user

- Should the mega skill auto-run on each article? Or remain opt-in via `/upgrade-redesign`?
- Activate `agentic-seo-audit` as a HARD gate (block publish at < B) or SOFT (warn only)?
- Nightly re-audit cron — enable only for top-priority domains (galoz, dtapet, hondabike), or all 10+?

## Unresolved questions

- `hamen/material-3-skill` 404 — likely typo in source list. Verify correct owner.
- `bchao1/paper-finder` 404 — repo deleted/private. Drop from list.
- `irinabuht12-oss/email-campaigns-claude` README is English — explicit Hebrew/RTL implementation details not documented. Need to inspect repo source if Hebrew port is required.
