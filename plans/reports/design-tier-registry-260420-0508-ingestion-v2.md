# Design Tier Registry — 2026-04-20 Ingestion Batch v2

Phase 1 of 221-repo githubawesome.com pass. Design tier = 59 repos; 2 deduped against existing catalog (`awesome-design-md`, `impeccable`); 57 processed; 24 VALUABLE / 31 SKIP / 2 UNREACHABLE.

## Tier 1 — VALUABLE (24 — will become individual SKILL.md files; top 15 done this batch)

| # | Name | Owner | Purpose | HTML-redesign angle | Key pattern |
|---|---|---|---|---|---|
| 1 | **design-extract** | Manavarya09 | Site crawler → 8 token formats (W3C/Tailwind/shadcn/Figma/CSS vars) | **CORE** — seed per-domain brand kits | Computed-style crawl → multi-format token export |
| 2 | **design-dna** | zanwei | Agent skill extracting Design DNA (tokens+effects+perception) from refs | **CORE** — competitor/brand ref → machine-readable tokens | 3-phase Structure → Analyze → Generate schema |
| 3 | **OpenBrand** | ethanjyx | Extract logos/colors/brand assets from any URL | Auto brand-kit per domain (colors + logo) | Multi-interface extractor (API/lib/skill/MCP) |
| 4 | **pi-generative-ui** | Michaelliv | Reverse-engineered Claude.ai generative-UI (72KB verbatim design-system) | **CORE** — Anthropic's own patterns for streaming HTML | 5 streaming-safe modules (interactive/chart/mockup/art/diagram) |
| 5 | **ui-design-brain** | carmahhawwari | 60+ UI components + 5 design-direction presets | Ready-made component catalog with brand presets | Preset-driven design direction (SaaS/Apple/Enterprise/Creative/Dashboard) |
| 6 | **posterskill** | ethanweber | Single-file HTML posters with live editor + JSON round-trip | Reference for self-contained single-HTML article shipping | Browser-editable single-file + JSON export-reimport |
| 7 | **codebase-to-course** | zarazhangrui | Any repo → single-page interactive HTML course | Single-file scroll-module pattern; "warm non-purple" aesthetic | Self-contained HTML + scroll modules + side-by-side code/explain |
| 8 | **fonttrio** | kapishdima | 49 curated font pairings (heading/body/mono), CSS vars | Direct drop-in typography for article templates | --font-heading/body/mono CSS-variable pairing |
| 9 | **brand-toolkit** | jgerton | Methodology-grounded brand building (Dunford/StoryBrand/Aaker/Chris Do) | Brand strategy layer before HTML generation | Compose expert frameworks as skills sharing manifest state |
| 10 | **animated-icons** | gorkem-bwl | CSS-only animated color icons (Lucide/Heroicons/Iconoir) | Plug-in animated icons for CTA/FAQ/toggles | CSS-var themed hover animations across 3 sets |
| 11 | **ai-website-cloner-template** | JCodesMore | /clone-website pipeline — recon→spec→parallel builders→visual-diff | Pipeline model for HTML redesign QA stage | Recon → spec → parallel worktree builders → visual-diff |
| 12 | **react-kino** | btahir | Scroll-driven cinematic HTML experiences | Scroll-pin, parallax, reveal patterns for article hero/CTA | Scene pinning + reveal + parallax scroll primitives |
| 13 | **tegaki** | KurtGokhan | Animated handwriting renderer (any font, multi-framework) | Decorative stroke-animation for hero/headline text | Font-to-stroke-path handwriting SVG animation |
| 14 | **Wireframed.js** | Lywald | Browser node-graph engine for 3D wireframe art (Three.js, no build) | Hero WebGL visuals via ~15-line embed | Node-graph pipeline + embeddable runtime.js |
| 15 | **jackbutcher.md** | visualizevalue | Jack Butcher's voice extracted from 50k tweets as prompt context | Brand-voice prompt pattern for article copywriting | Reverse-engineer writing voice → reusable prompt-context .md |
| 16 | visualise | bentossell | Inline SVG/HTML/chart visuals skill | Design-system skill structure reference | Design-system + components + diagrams + charts split |
| 17 | web-haptics | lochie | Haptic feedback for mobile web (React/Vue/Svelte/vanilla) | Tactile polish for CTAs/floating buttons on mobile | useWebHaptics hook with semantic triggers |
| 18 | stayview | louisnelza | Zero-dep vanilla dashboard (DM Sans + DM Serif Display) | Clean minimal-stack dashboard reference | Zero-dep vanilla dashboard + iCal aggregation |
| 19 | 3dsvg | renatoworks | SVG → interactive 3D via embeddable React component | SVG/3D hero elements, PBR presets | React-Three-Fiber wrapper + 10 PBR material presets |
| 20 | webreel | vercel-labs | Headless-Chrome → MP4 of scripted browser flows | Auto-generate demo videos of redesigned articles | JSON steps + cursor/keystroke HUD overlays |
| 21 | figma-mcp-go | vkhanhqui | MCP server granting AI tools Figma read/write (73 tools) | Pipe Figma tokens/specs into article HTML generation | Plugin arch bypassing Figma REST rate limits |
| 22 | boneyard | 0xGF | Skeleton loading screens extracted from real UI (6 frameworks) | Loading-state placeholders for perceived-perf | Auto-extract skeleton geometry from rendered DOM |
| 23 | OpenGenerativeUI | CopilotKit | LangChain demo: LLM-generated interactive HTML/SVG widgets | Sandboxed iframe wrapper for LLM-generated fragments | MCP assemble_document + design-system injection |
| 24 | htmx-vscode-toolkit | atoolz | VSCode extension for HTMX (IntelliSense, hover, diagnostics) | HTMX authoring support if templates adopt progressive-enh | Attribute schema + Levenshtein did-you-mean |

## Tier 2 — SKIP (31)

| Repo | Reason |
|---|---|
| remodex | iOS Codex remote control |
| OpenSquirrel | Archived Rust GPU tiling |
| clawport-ui | Ops dashboard, not patterns |
| paper-dl | arxiv PDF downloader |
| Fio | Desktop game engine |
| llm-circuit-finder | Model internals research |
| molmoweb | Browser-control VLM |
| ReactMotion | ML body-motion research |
| wet | Go proxy infra |
| holyclaude | Docker bundler |
| m33mu | ARM Cortex emulator |
| thereisnospoon | ML primer docs |
| druids | Agent orchestration infra |
| react-container-kit | State plumbing |
| gsd-2 | Agent harness |
| tui-studio | ANSI/TUI editor |
| larksuite/cli | Feishu CLI |
| clui-cc | macOS desktop wrapper |
| Odyssey | Rust agent runtime |
| claude-peers-mcp | Peer messaging infra |
| grafana-tui | Go TUI |
| lux | Redis-compat KV store |
| open-terminal | Remote shell sandbox |
| ai-scrum-master-template | PM orchestration |
| reading-ai-agent | Tauri desktop agent |
| sentrux | Code quality monitor |
| SwiftUI-Agent-Skill | iOS-only |
| querypad | SQL IDE |
| Auto-claude-code-research-in-sleep | ML research orchestrator |
| Recordly | Desktop recorder |
| follow-builders | Content curation |

## Tier 3 — UNREACHABLE (2)

| Repo | Status |
|---|---|
| elixir-volt/quickbeam | README 404 both branches |
| rangersui/Elastik | README 404 both branches (possibly private/deleted) |

## Dedup against existing catalog

- `VoltAgent/awesome-design-md` — already installed (skill `awesome-design-md`)
- `pbakaus/impeccable` — already installed (skill `impeccable`)

## What ships in this batch

- This registry (≈ 59 repos cataloged)
- 15 individual SKILL.md files at `~/.claude/skills/redesign-html-template-mega/sources/{slug}.SKILL.md`
- SKILLS-INDEX.md update entry
- Top-10 valuable repos report (below)

## Top 10 most valuable finds (ranked)

1. **design-extract** — fastest path to per-domain token seeds
2. **design-dna** — schema-based reference → HTML generation
3. **pi-generative-ui** — Anthropic's own streaming-HTML design rules, verbatim
4. **OpenBrand** — complement to design-extract for logos/assets
5. **ui-design-brain** — 60-component catalog ready to reference
6. **posterskill** — single-file + JSON round-trip is a new integration pattern worth studying
7. **brand-toolkit** — strategy layer most pipelines skip
8. **codebase-to-course** — scroll-module single-HTML pattern transferable to long articles
9. **fonttrio** — drop-in typography, solves "which font for this brand"
10. **ai-website-cloner-template** — QA pipeline pattern (visual-diff gate)

## Flagged for deeper analysis

- **pi-generative-ui** — contains Anthropic's ~72 KB design system verbatim; deserves its own deep-dive skill extract to inform our streaming-HTML patterns.
- **design-dna** — schema layout ("tokens+perception+effects") could become the canonical shape of `domain-brand-map.json`.
- **ai-website-cloner-template** — visual-diff QA stage is not currently in our pipeline; worth lifting.
