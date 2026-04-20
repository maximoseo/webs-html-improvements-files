# Active Skill Set — 2026-04-20 Ingestion Batch

Activation policy: **additive only**. Nothing in existing catalog is disabled. 9 new installs are scheduled below. 7 new "referenced but not installed" skills. All Tier 4 skills are **catalog-only** (not installed, not active).

## New skills to activate (9 — Tier 1)

Target install path: `~/.claude/skills/{slug}/SKILL.md` (clone or SKILL.md-only, per repo size).

| Slug | Source | Trigger scenarios |
|---|---|---|
| `html-ppt-skill` | lewislulu/html-ppt-skill | Multi-theme HTML generation, slide/article variants |
| `hue-brand-extractor` | dominikmartn/hue | Onboarding a new domain — extract brand tokens |
| `skillui-cli` | amaancoderx/npxskillui (alias refresh) | CLI brand scrape → SKILL.md per domain |
| `logo-generator` | op7418/logo-generator-skill | Branding redesigned templates |
| `marp-slides` | robonuggets/marp-slides | Dashboard metrics / data-viz blocks in articles |
| `email-campaigns-claude-blocks` | irinabuht12-oss/email-campaigns-claude (blocks subset) | Inline CTA / hero card in article body |
| `agentic-seo-audit` | addyosmani/agentic-seo | Post-render QA gate before publish |
| `svg-hand-drawn` | shaom/svg-hand-drawn-skill | Decorative SVG motion layer |
| `compose-style-rubric` | hamen/compose_skill (rubric pattern only) | HTML quality scorecard with ceilings |

## Referenced — not installed (7 — Tier 2)

| Slug | Why not install | Use |
|---|---|---|
| `harness-meta-team` | Large plugin, orchestration-level | Studied for multi-agent article team design |
| `skill-based-architecture` | Structural pattern, no runtime | Folder layout guidance only |
| `skillclaw-evolution` | Experimental auto-evolver — risky non-destructive guarantees | Future: shadow evaluation |
| `engineering-figure-banana` | Python toolchain dependency | Pattern: chart vs image routing rule |
| `friday-showcase-cron` | Heavy infra (Telegram + SQLite) | Pattern: nightly re-audit loop |
| `lich-skills-spec-driven` | Overlaps with existing `manual-SDD`/`spec-driven` | Cross-reference |
| `manual-SDD-canonical` | Overlaps with existing SDD skills | Cross-reference |

## Catalog-only (Tier 3–4 — 17)

Not installed. Kept in registry for search/traceability. See `master-skill-registry-260420-0508-ingestion.md`.

## Activation checklist

- [ ] Each Tier 1 install lands at `~/.claude/skills/{slug}/SKILL.md` with frontmatter (`name`, `description`, `when-to-use`)
- [ ] Each install appends a 1-line entry to the user's auto-memory skill inventory
- [ ] No existing skill at the target path is overwritten — if conflict, append `-v2` suffix and preserve original
- [ ] Backup any replaced files to `CLAUDE CODE BACKUP/2026-04-20-skill-expansion/`
- [ ] `agentic-seo-audit` is wired into the article post-render hook (runs on `Improved_HTML_Template.html` before Obsidian deploy)
