# Master Skill Registry — 2026-04-20 Ingestion Batch

35 GitHub sources processed. 2 unreachable. 33 cataloged.

## Tier 1 — HIGH RELEVANCE (integrate into HTML redesign mega skill)

| # | Name | Owner | Category | One-liner | Relevance |
|---|---|---|---|---|---|
| 1 | html-ppt-skill | lewislulu | UI-UX / Agent Skill | HTML presentation generator, zero-build, 36 token themes | Token-swap theming + scoped template prefixes |
| 2 | hue | dominikmartn | Design Systems | URL/screenshot → full design system tokens | Auto-extract brand tokens per domain |
| 3 | npxskillui (SkillUI) | amaancoderx | Tools / Design | CLI: URL → SKILL.md + token bundle | Onboarding new domains (galoz, dtapet, etc.) |
| 4 | logo-generator-skill | op7418 | Design Systems | 6+ SVG logo variants + 12 showcase backdrops | Hero/section backgrounds, proportion rules as CSS tokens |
| 5 | marp-slides | robonuggets | Design / Tools | MARP presentations w/ inline SVG components | SVG chart/metric-card primitives |
| 6 | email-campaigns-claude | irinabuht12-oss | Automation / Design | Marketing email builder + Resend | Frost-card + pill-CTA blocks (port with RTL) |
| 7 | agentic-seo | addyosmani | SEO / QA | AEO audit (10 checks, A–F grading) | Post-render QA gate + per-article llms.txt |
| 8 | svg-hand-drawn-skill | shaom | UI-UX / Experimental | Animated hand-drawn SVG player | Decorative hero/section motion |
| 9 | compose_skill | hamen | Coding / Audit | Jetpack Compose rubric audit (weighted, cited) | Scorecard pattern for HTML (a11y/perf/SEO ceilings) |

## Tier 2 — MEDIUM RELEVANCE (reference / orchestration)

| # | Name | Owner | Category | Integration |
|---|---|---|---|---|
| 10 | harness | revfactory | Meta / Orchestration | Multi-agent team factory — orchestrate article rebuilds |
| 11 | skill-based-architecture | WoJiSama | Meta / Skills | Canonical folder structure for `~/.claude/skills/` |
| 12 | SkillClaw | AMAP-ML | Meta / Evolution | Auto-evolve skills loop (article pipeline self-improvement) |
| 13 | engineering-figure-banana | heyu-233 | Tools / Research | Split chart/image routing (numeric vs conceptual) |
| 14 | friday-showcase | missingus3r | Agent / Autonomy | Cron-based nightly re-audit pattern |
| 15 | lich-skills | LichAmnesia | Meta / Methodology | Spec-driven dev + scientific debug |
| 16 | manual-SDD | LIDR-academy | Meta / Methodology | SDD starter kit, canonical agent defs |

## Tier 3 — LOW RELEVANCE (catalog only — do NOT activate by default)

| # | Name | Owner | Category | Note |
|---|---|---|---|---|
| 17 | skills | MiniMax-AI | Agent Skills Collection | Reference only |
| 18 | autoskills | midudev | Tools | Already installed (prior batch) |
| 19 | awesome-cursor-skills | spencerpauly | Awesome List | Cursor-format cross-reference |
| 20 | inside-lago-voice-skill | getlago | Writing / Voice | Brand-voice patterns reusable |
| 21 | ai-life-skills | reysu | Productivity | Obsidian vault R/W patterns |
| 22 | antivibe | mohi-devhub | Educational | Code-explanation generator |
| 23 | my-ai-workflow | maiobarbero | Methodology | Reference doctrine |

## Tier 4 — UNRELATED / DO NOT INSTALL

| # | Name | Reason |
|---|---|---|
| 24 | shopify-admin-skills (40RTY-ai) | E-commerce ops |
| 25 | PaperOrchestra (Ar9av) | LaTeX paper pipeline |
| 26 | 3gpp-skill (lugasia) | Telecom domain |
| 27 | buffett-skills (agi-now) | Finance domain |
| 28 | android-skills-mcp (skydoves) | Android native |
| 29 | how (poteto) | Cursor-only |
| 30 | caveman-claude-skill (amanattar) | Ultra-compression — conflicts with rich HTML narrative |
| 31 | spider-king-skill (aoyunyang) | Web scraping RE |
| 32 | seedance-skill (robonuggets) | Video motion |
| 33 | talk-normal (hexiecs) | Style prompt — conflicts with rich narrative |

## Unreachable

| # | URL | Status |
|---|---|---|
| 34 | hamen/material-3-skill | README 404 on main + master |
| 35 | bchao1/paper-finder | README 404 |

## Dedup against prior batches

- `autoskills` — already installed 2026-04-18 batch 4+5
- `harness` — already installed as `agent-harness-construction` (sim)
- `npxskillui` — already in skill list (alias)
