# Top-10 Design-Tier Finds — 2026-04-20 Phase 1

Ranked by direct impact on the HTML Redesign Mega Skill pipeline.

## 1. design-extract (Manavarya09)
**Why:** Fastest path from raw URL to a per-domain token bundle in 8 formats. Drop-in replacement for hand-curating CSS variables.
**Where it lands:** Phase 3 (Design System Resolution) — primary token source.
**Flag:** **Deep-dive worth.** Inspect export schemas; canonicalize one as the mega-skill's format.

## 2. design-dna (zanwei)
**Why:** Adds **perception** (mood, density, formality) and **effects** (shadow level, radius preference) alongside raw tokens. Converts "feel" into machine-readable state.
**Where it lands:** `domain-brand-map.json` schema — the 3-section shape (tokens / perception / effects).
**Flag:** **Deep-dive worth.** Likely becomes the canonical shape for all per-domain brand entries.

## 3. pi-generative-ui (Michaelliv)
**Why:** Contains Anthropic's own ~72KB design-system doc verbatim, organized as 5 streaming-safe modules (interactive / chart / mockup / art / diagram). This is the reference on how to structure generative HTML.
**Where it lands:** Primitive-catalog organization — mega-skill's sub-skills map to these 5 categories.
**Flag:** **Deep-dive required.** Budget for a dedicated session to extract the 5 modules as separate reference files.

## 4. OpenBrand (ethanjyx)
**Why:** Complements design-extract. Where extract does tokens, OpenBrand does logos + brand assets. Together they cover "everything from a URL".
**Where it lands:** Phase 1 (Domain Onboarding) — quick path.

## 5. ui-design-brain (carmahhawwari)
**Why:** 60 UI components + 5 design-direction presets (SaaS / Apple / Enterprise / Creative / Dashboard). Preset-driven design skips hours of token-hunting.
**Where it lands:** Phase 3 fast-path for known brand archetypes.

## 6. brand-toolkit (jgerton)
**Why:** Missing strategy layer most pipelines skip. Dunford positioning + StoryBrand + Aaker + Chris Do stylescapes — grounded, not vibes-based.
**Where it lands:** New optional phase between Onboarding and Design Resolution.

## 7. fonttrio (kapishdima)
**Why:** 49 curated heading/body/mono triplets with CSS variables. Solves "which font for this brand" deterministically.
**Where it lands:** Phase 3 — typography selection shortcut.

## 8. animated-icons (gorkem-bwl)
**Why:** CSS-only hover-animated icons for Lucide/Heroicons/Iconoir. Drop-in upgrade for CTA + TOC/FAQ chevrons. Zero JS runtime.
**Where it lands:** Sub-skills 8 (TOC/FAQ) + 11 (CTA Hierarchy).

## 9. ai-website-cloner-template (JCodesMore)
**Why:** Visual-diff QA gate is NOT currently in our pipeline. Recon→spec→parallel builders→diff is a clean 4-phase pattern.
**Where it lands:** Phase 7 (QA Gate) — adopt visual-diff regression detection.
**Flag:** **Deep-dive worth.** Extract the visual-diff implementation as a standalone skill.

## 10. codebase-to-course (zarazhangrui)
**Why:** Single-file scroll-module pattern applicable to long Hebrew technical articles. "Warm non-purple" aesthetic rules also worth internalizing.
**Where it lands:** Optional `scroll-module-layout` sub-skill — per-article opt-in.

## Honorable mentions (11–15, still got SKILL.md files)

- **posterskill** — single-file HTML + live editor + JSON round-trip
- **react-kino** — scroll-driven primitives (most port-able via @supports)
- **tegaki** — handwriting SVG animation for editorial/magazine flair
- **Wireframed.js** — 3D WebGL hero element for industrial B2B brands
- **jackbutcher.md** — brand-voice prompt-context pattern

## Deeper-analysis flags (3 repos warrant a follow-up session)

| Repo | Why deeper |
|---|---|
| **pi-generative-ui** | ~72KB of verbatim Anthropic design-system rules; extract the 5 modules as individual references |
| **design-dna** | Canonical schema candidate for `domain-brand-map.json`; align our data model |
| **ai-website-cloner-template** | Visual-diff QA stage not in our pipeline; lift and wrap as a standalone skill |

## What's NOT on this list (and why)

- **Desktop/TUI tools** (tui-studio, grafana-tui, m33mu, Fio, clui-cc) — no web-HTML transfer value.
- **Infrastructure/orchestration** (druids, Odyssey, open-terminal, harness) — already have parallel catalog coverage.
- **ML research** (molmoweb, llm-circuit-finder, ReactMotion, paper-dl) — off-scope.
- **Archived repos** (OpenSquirrel) — no upkeep commitment possible.
