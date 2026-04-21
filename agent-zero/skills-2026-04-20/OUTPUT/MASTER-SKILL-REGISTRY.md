# MASTER SKILL REGISTRY — 2026-04-20
**Total sources processed:** 35 GitHub repositories
**Total skills produced/upgraded:** 26 existing preserved + 2 new + 17-module mega-skill upgrade
**Status:** COMPLETE — all repos analyzed, all patterns extracted

---

## REGISTRY TABLE

| # | Skill Name | Category | Source Repos | Status | File |
|---|-----------|----------|--------------|--------|------|
| 1 | html-redesign-mega-skill | HTML/Design | 35 repos (mega upgrade) | ✅ NEW/UPGRADED | `html-redesign-mega-skill.SKILL.md` |
| 2 | html-redesign-premium-polish | HTML/Design | dtapet.com + WP analysis | ✅ PRESERVED (v2) | `html-redesign-premium-polish.SKILL.md` |
| 3 | wordpress-safe-article-layouts | WordPress | dtapet.com analysis | ✅ PRESERVED | `wordpress-safe-article-layouts.SKILL.md` |
| 4 | cta-selection-engine | CTA/Conversion | Internal | ✅ PRESERVED | `cta-selection-engine.SKILL.md` |
| 5 | seo-geo-content-systems | SEO/GEO | Internal | ✅ PRESERVED | `seo-geo-content-systems.SKILL.md` |
| 6 | seo-tools-master-reference | SEO Tools | 14 repos (v2) | ✅ PRESERVED | `seo-tools-master-reference.SKILL.md` |
| 7 | geo-ai-search-optimization | GEO/AI Search | AutoGEO repo | ✅ PRESERVED | `geo-ai-search-optimization.SKILL.md` |
| 8 | n8n-automation-workflow | N8N | Internal | ✅ PRESERVED | `n8n-automation-workflow.SKILL.md` |
| 9 | frontend-app-engineering | Frontend | Internal | ✅ PRESERVED | `frontend-app-engineering.SKILL.md` |
| 10 | browser-visual-qa | QA/Testing | Internal + awesome-cursor | ✅ PRESERVED | `browser-visual-qa.SKILL.md` |
| 11 | ui-ux-design-system | UI/UX | Internal | ✅ PRESERVED | `ui-ux-design-system.SKILL.md` |
| 12 | ui-style-matching-engine | Style | taste-skill (67 styles) | ✅ PRESERVED | `ui-style-matching-engine.SKILL.md` |
| 13 | anti-ai-slop-design | Anti-Pattern | pbakaus/impeccable | ✅ PRESERVED | `anti-ai-slop-design.SKILL.md` |
| 14 | prompt-engineering-cto-mode | Prompts | Internal | ✅ PRESERVED | `prompt-engineering-cto-mode.SKILL.md` |
| 15 | llm-systems-awareness | LLM/AI Infra | Internal | ✅ PRESERVED | `llm-systems-awareness.SKILL.md` |
| 16 | agent-memory-management | Memory | Internal | ✅ PRESERVED | `agent-memory-management.SKILL.md` |
| 17 | hermes-self-improving-agents | Agent Systems | hermes repos | ✅ PRESERVED | `hermes-self-improving-agents.SKILL.md` |
| 18 | gstack-multi-role-agents | Multi-Agent | gstack repos | ✅ PRESERVED | `gstack-multi-role-agents.SKILL.md` |
| 19 | kronos-architect-protocol | Architecture | Internal | ✅ PRESERVED | `kronos-architect-protocol.SKILL.md` |
| 20 | karpathy-coding-guardrails | Coding | karpathy skills | ✅ PRESERVED | `karpathy-coding-guardrails.SKILL.md` |
| 21 | persistent-memory-claude-mem | Memory | claude.mem | ✅ PRESERVED | `persistent-memory-claude-mem.SKILL.md` |
| 22 | document-to-markdown-markitdown | Documents | markitdown | ✅ PRESERVED | `document-to-markdown-markitdown.SKILL.md` |
| 23 | voxcpm-voice-tts | Voice/TTS | voxcpm | ✅ PRESERVED | `voxcpm-voice-tts.SKILL.md` |
| 24 | postiz-social-publishing | Social | postiz | ✅ PRESERVED | `postiz-social-publishing.SKILL.md` |
| 25 | modern-ui-pattern-harvester | UI Patterns | Internal | ✅ PRESERVED | `modern-ui-pattern-harvester.SKILL.md` |
| 26 | premium-component-composition | Components | Internal | ✅ PRESERVED | `premium-component-composition.SKILL.md` |
| 27 | SKILLS-INDEX | Meta | All | ✅ PRESERVED | `SKILLS-INDEX.md` |

---

## SOURCE REPO CLASSIFICATION

### UI/UX / Design Systems
| Repo | Key Value Extracted |
|------|--------------------|
| `dominikmartn/hue` | Brand design system extractor: URL/screenshot → color tokens, typography, spacing, components, light+dark mode. 17 brand examples. |
| `amaancoderx/npxskillui` | CLI reverse-engineers any website into Claude-ready design skill. Extracts colors, typography, animations, screenshots. |
| `lewislulu/html-ppt-skill` | 36 themes × 15 templates × 31 layouts × 47 animations. Presenter mode with BroadcastChannel sync. Pure HTML/CSS/JS. |
| `hamen/material-3-skill` | MD3 compliance: color roles, 30+ components, adaptive layouts, compliance audit mode. Primary: Jetpack Compose. |
| `robonuggets/marp-slides` | MARP presentations: SVG charts, metric cards, gauges, sparklines, 22 curated example decks. |
| `irinabuht12-oss/email-campaigns-claude` | Email HTML: frost-glass cards, video blocks, design tokens (3px radius, 560px max, GIF pipeline, Resend integration). |
| `op7418/logo-generator-skill` | SVG logos: geometric/dot-matrix/line, 12 background styles, hover HTML showcase, Gemini image integration. |
| `shaom/svg-hand-drawn-skill` | SVG path animation: draw paths → reveal fills → preserve colors. Output: preview.html + player.js. |
| `heyu-233/engineering-figure-banana` | Engineering figures: image mode (conceptual) + plot mode (quantitative). Publication-aware output. |
| `hamen/compose_skill` | Jetpack Compose audit: 4 categories scored, Gradle compiler reports, mandatory ceilings, cited findings. |

### Agent Architecture / Meta-Skills
| Repo | Key Value Extracted |
|------|--------------------|
| `AMAP-ML/SkillClaw` | Collective skill evolution: skills evolve from every session. Digest/deduplicate mechanism. Works with Hermes, OpenClaw, QwenPaw. |
| `WoJiSama/skill-based-architecture` | Meta-skill: point at codebase → distills into SKILL.md router + rules/ + workflows/ + references/gotchas.md. |
| `revfactory/harness` | Team-architecture factory: 6 patterns (Pipeline, Fan-out/Fan-in, Expert Pool, Producer-Reviewer, Supervisor, Hierarchical Delegation). |
| `midudev/autoskills` | Auto-detect project stack → install matching skills. Supports 40+ tech stacks. |
| `poteto/how` | Codebase explainer: Explain + Critique modes. Fan-out to parallel explorer subagents. |
| `LIDR-academy/manual-SDD` | Spec-Driven Development: single canonical source + symlinks for Codex/Cursor/Claude. |
| `LichAmnesia/lich-skills` | spec-driven-dev loop + debug-hypothesis loop + aggregate-N-sources loop. |
| `maiobarbero/my-ai-workflow` | Free-form Plan → PRD → Issues → Tasks → Code → Review → Final Audit. AI handles implementation, human owns review. |
| `Ar9av/PaperOrchestra` | 5-agent pipeline: Outline→Plotting→LitReview→SectionWriting→ContentRefinement. 50-68% win margin on quality benchmarks. |
| `missingus3r/friday-showcase` | Self-evolving AI assistant: skill acquisition + daily reflection + preference learning + world modeling. |
| `skydoves/android-skills-mcp` | MCP server + packager CLI: converts SKILL.md to 7 native formats (Claude, Cursor, Copilot, Gemini, JetBrains, Continue, Aider). |
| `40RTY-ai/shopify-admin-skills` | 63 Shopify skills across 10 categories. dry_run: true pattern before mutations. |

### Communication / Prompting
| Repo | Key Value Extracted |
|------|--------------------|
| `hexiecs/talk-normal` | Single system prompt: 73% response size reduction while preserving all useful information. |
| `amanattar/caveman-claude-skill` | 75% token reduction. 6 intensity levels (lite/full/ultra + wenyan modes). Auto-clarity exceptions for safety. |
| `getlago/inside-lago-voice-skill` | Write-in-your-voice template: 7 sections (Voice, Rules, Anti-Filler, Audience Adaptation, Channel Notes, Drafted-vs-Sent, Company Context). |
| `mohi-devhub/antivibe` | Anti-vibecoding: deep dives explain WHAT/WHY/WHEN/ALTERNATIVES for AI-generated code. Phase-aware. |

### SEO / Research
| Repo | Key Value Extracted |
|------|--------------------|
| `addyosmani/agentic-seo` | AEO (Agentic Engine Optimization): 10 checks, 5 categories, 0-100 score. llms.txt, AGENTS.md, token budget, capability signaling. |
| `agi-now/buffett-skills` | Investment analysis framework: Warren Buffett system covering moat, management, valuation, 8 industry playbooks. |
| `reysu/ai-life-skills` | Obsidian vault integration. Summarize YouTube/articles/PDFs → notes with wikilinks to people/concepts. |
| `Ar9av/PaperOrchestra` | Research paper pipeline with structured literature review and citation integration. |

### Other / Domain Specific
| Repo | Key Value Extracted |
|------|--------------------|
| `lugasia/3gpp-skill` | Deep 3GPP telecom: 2G→6G, protocol stacks, core network, security analysis. |
| `robonuggets/seedance-skill` | Video generation from app screenshots using ByteDance Seedance 2.0/Fal AI. |
| `spencerpauly/awesome-cursor-skills` | 30+ Cursor skill patterns: visual-QA, responsive testing, dark mode testing, accessibility auditing, parallel subagents, form testing, CI triage. |
| `aoyunyang/spider-king-skill` | Web protocol reverse engineering. Evidence-first, protocol-first, browser-free delivery. |

---

## DEDUPLICATION REPORT

| Conflict | Resolution |
|----------|------------|
| Multiple "coding guardrails" patterns (karpathy, LIDR, maiobarbero, LichAmnesia) | Merged into karpathy-coding-guardrails.SKILL.md — all unique loops preserved |
| Multiple "responsive design" sources (awesome-cursor + MiniMax + html-ppt) | Merged into Module 1 of html-redesign-mega-skill |
| Multiple "voice/tone" skills (caveman, talk-normal, lago-voice) | Kept as distinct patterns — different use cases (compression vs. voice matching) |
| Multiple "agent memory" sources (friday, ai-life-skills, SkillClaw) | Existing agent-memory-management.SKILL.md covers this; patterns noted in memo |
| hue + SkillUI both extract design systems | Merged into Bonus Module B1 — complementary tools |

---

## SECURITY SCAN

Repos scanned for exposed credentials: **None found**
- No API keys extracted or stored
- No tokens preserved
- No secrets in output files
