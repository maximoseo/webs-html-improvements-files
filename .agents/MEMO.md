# Code Agents Global Skill Memo
**Last Updated:** 2026-04-16

This memo documents the core capabilities added during the skill expansion across the agent ecosystem.

## 1. TextGen LLM Workflow (`textgen-llm-workflow`)
- **What it does:** Optimizes local LLM inference, pipeline architecture, and multimodal inputs using text-generation-webui principles.
- **When to use:** When troubleshooting local model OOM issues, VRAM offloading, or building offline Python tools.
- **When not to use:** When doing standard cloud API calls or frontend web design.
- **Input/Output:** In: hardware constraints / prompt requirements. Out: loader configs, tool definitions.
- **Dependencies:** Assumes access to local GPU/GGUF models.

## 2. Million Debug Agent (`million-debug-agent`)
- **What it does:** Provides an evidence-based debugging loop using runtime NDJSON instrumentation rather than static guessing.
- **When to use:** When chasing complex state bugs, race conditions, or silent template failures.
- **When not to use:** For simple syntax typos or CSS tweaks.
- **Input/Output:** In: Bug report. Out: Instrumentation code, execution logs, and verified patch.

## 3. SEOMachine Optimization (`seomachine-optimization`)
- **What it does:** Automates SEO workflows, readability scoring, and internal link architecture.
- **When to use:** When generating production-ready articles that need to rank, or when planning a topical map.
- **When not to use:** Internal dashboards or non-public tools.
- **Input/Output:** In: Draft text, keywords. Out: Optimized Markdown/HTML and meta data.

## 4. MarkItDown Conversion (`markitdown-conversion`)
- **What it does:** Transforms messy PDFs, Word docs, audio, and images into clean, LLM-ready Markdown.
- **When to use:** When preprocessing unstructured source material for a content pipeline.
- **When not to use:** When styling final HTML output.
- **Input/Output:** In: Binary/document file. Out: Semantic Markdown.

## 5. Scrapling Extraction (`scrapling-extraction`)
- **What it does:** Executes adaptive web scraping and stealth extraction while bypassing anti-bot measures.
- **When to use:** When fetching real competitor data, reviews, or API-less content to seed an article generation prompt.
- **When not to use:** Extracting PII or hitting sensitive internal APIs.
- **Input/Output:** In: Target URL. Out: Clean JSON or Markdown extraction.

## 6. API Mega Discovery (`api-mega-discovery`)
- **What it does:** Recommends APIs and MCP servers from a massive categorized directory to extend agent capabilities.
- **When to use:** When planning a new automation stack or enriching an article workflow with live data (weather, stocks, etc.).
- **When not to use:** Building custom scrapers when a free API already exists.
- **Input/Output:** In: Functional requirement. Out: API recommendations and integration plans.

## 7. Codeburn Optimization (`codeburn-optimization`)
- **What it does:** Audits agent session logs to optimize token usage, context windows, and one-shot success rates.
- **When to use:** When a codebase prompt is bloated, or token costs are spiraling out of control.
- **When not to use:** Do not aggressively strip critical instructions (like WordPress safety rules) just to save tokens.
- **Input/Output:** In: Session logs, prompt files. Out: Optimized `.claudeignore` rules and leaner prompts.


## 8. Context & Memory Manager (`context-memory-manager`)
- **What it does:** Optimizes context packing and multi-agent memory retention.
- **When to use:** Long sessions where agents risk forgetting architectural rules.

## 9. SuperClaude Framework Orchestration (`superclaude-framework-orchestration`)
- **What it does:** Auto-discovers skills and delegates tasks to sub-agents.
- **When to use:** Massive, multi-file epic implementations.

## 10. Design-to-Code Renderer (`design-to-code-renderer`)
- **What it does:** Translates design vibes and JSON payloads into semantic HTML.
- **When to use:** Converting mockups or raw data into beautiful UI components.

## 11. System Design Architect (`system-design-architect`)
- **What it does:** Enforces scalable architecture and developer best practices.
- **When to use:** Planning phases and database schema design.

## 12. Content Humanization & Social OSINT (`content-humanization-social`)
- **What it does:** De-AI's text and matches brand tone based on social profiles.
- **When to use:** Polishing article drafts and marketing copy.

## 13. CLI Automation Workflows (`cli-automation-workflows`)
- **What it does:** Configures CI/CD pipelines and optimizes local environments.
- **When to use:** Setting up GitHub actions, Zadig, or debloating Windows.

## 14. Meta-Prompt Optimization (`meta-prompt-optimization`)
- **What it does:** Refines system prompts and recommends model routing.
- **When to use:** Generating strict N8N pipeline instructions.


## 8. Context & Memory Manager (`context-memory-manager`)
- **What it does:** Optimizes context packing and multi-agent memory retention.
- **When to use:** Long sessions where agents risk forgetting architectural rules.

## 9. SuperClaude Framework Orchestration (`superclaude-framework-orchestration`)
- **What it does:** Auto-discovers skills and delegates tasks to sub-agents.
- **When to use:** Massive, multi-file epic implementations.

## 10. Design-to-Code Renderer (`design-to-code-renderer`)
- **What it does:** Translates design vibes and JSON payloads into semantic HTML.
- **When to use:** Converting mockups or raw data into beautiful UI components.

## 11. System Design Architect (`system-design-architect`)
- **What it does:** Enforces scalable architecture and developer best practices.
- **When to use:** Planning phases and database schema design.

## 12. Content Humanization & Social OSINT (`content-humanization-social`)
- **What it does:** De-AI's text and matches brand tone based on social profiles.
- **When to use:** Polishing article drafts and marketing copy.

## 13. CLI Automation Workflows (`cli-automation-workflows`)
- **What it does:** Configures CI/CD pipelines and optimizes local environments.
- **When to use:** Setting up GitHub actions, Zadig, or debloating Windows.

## 14. Meta-Prompt Optimization (`meta-prompt-optimization`)
- **What it does:** Refines system prompts and recommends model routing.
- **When to use:** Generating strict N8N pipeline instructions.


## 15. Bash Security Analysis (`bash-security-analysis`)
- **What it does:** Analyzes terminal workflows, shell scripts, and detects obfuscated bash payloads.
- **When to use:** Auditing unfamiliar build scripts or CI/CD jobs.

## 16. JS Architecture Fundamentals (`js-architecture-fundamentals`)
- **What it does:** Deep debugging of the JS Event Loop, closures, and frontend prototype chains.
- **When to use:** Troubleshooting complex React/Vanilla JS state bugs.

## 17. Screenshot-to-Code Workflow (`screenshot-to-code-workflow`)
- **What it does:** Translates visual structures (mockups) into semantic HTML/CSS layouts.
- **When to use:** Rebuilding UI components or WordPress templates from visual inspiration.

## 18. CS Systems Reasoning (`cs-systems-reasoning`)
- **What it does:** Applies algorithmic thinking, Big-O analysis, and data structure logic.
- **When to use:** Designing scalable backend APIs or caching systems.

## 19. Crawlee Advanced Scraping (`crawlee-advanced-scraping`)
- **What it does:** Manages headless browser scraping, request queues, and structured extraction.
- **When to use:** Extracting competitor content or parsing heavy JavaScript SPAs.

## 20. Workspace Knowledge Architecture (`workspace-knowledge-architecture`)
- **What it does:** Structures hierarchical notes, local-first docs, and collaborative workflows.
- **When to use:** Organizing a complex Obsidian vault or project documentation folder.

## 21. Reveal.js Presentation Generation (`revealjs-presentation-generation`)
- **What it does:** Converts structured articles and reports into interactive HTML slides.
- **When to use:** Generating a slide deck from a research report or audit.

## 22. Autoskills Stack Detection Extension (`autoskills-installer`)
- **What it does:** Scans project config files to auto-detect tech stack and install matching AI agent skills via `npx autoskills`. Also generates CLAUDE.md from installed skills. Extension notes (GOD MODE #7): the skills-map.ts detection pattern is independently reusable as a "detect stack → activate matching skills" pattern in any agent workflow.
- **When to use:** Bootstrapping any new project with correct skill coverage. Also use `npx autoskills -a claude-code` to regenerate CLAUDE.md from currently installed skills.
- **When NOT to use:** Manually curated skill sets; non-standard monorepo setups.
- **Key insight:** Install outputs `seo` and `frontend-design` skills which are directly relevant to article template design. Pair with `design-md-workflow` after autoskills runs.
- **Interoperates with:** `design-md-workflow` (run autoskills first → installs frontend-design + seo → use DESIGN.md to complete visual system)
- **Article Relevance:** MEDIUM — use to bootstrap new article-system repos; the auto-installed SEO + design thinking skills are relevant.

## 23. DESIGN.md Workflow (`design-md-workflow`)
- **What it does:** Structured 9-section DESIGN.md format that gives AI agents enough context to generate a complete design system: CSS custom property tokens, typography scale, component library HTML, preview cards, and embedded regeneration prompts (Section 9 — Agent Prompt Guide). Used with Claude Design or any capable LLM.
- **When to use:** Starting any new visual design system; redesigning article HTML templates; creating brand-aligned CSS tokens without writing raw CSS manually; when you need a design spec that agents can act on precisely.
- **When NOT to use:** Skip if an existing CSS design system is working. Don't rebuild what works. Skip for single-page one-off styling.
- **Input/Output:** Input: a written DESIGN.md (30-60 min); Output: colors_and_type.css, index.html component kit, SKILL.md regeneration prompts.
- **Dependencies:** Claude Design at `claude.ai/design` OR any capable LLM with CSS generation ability. No npm installs.
- **Article Relevance:** HIGH — Write a DESIGN.md for the article template system → feed to Claude Design → receive CSS tokens and component HTML stubs → apply directly to Improved_HTML_Template.html.
- **Key insight:** Section 9 (Agent Prompt Guide) becomes the embedded instruction set for consistent redesign regeneration — embed it in the N8N prompt for future template iterations.
- **Reference library:** 68 brand DESIGN.md examples at github.com/VoltAgent/awesome-claude-design. Most relevant for articles: WIRED, Notion, Mintlify, Sanity, The Verge.
- **Interoperates with:** `screenshot-to-code-workflow` (extract competitor layout → inspire DESIGN.md), `premium-frontend-ui`, `frontend-design`, `revealjs-presentation-generation` (visual system extends to slide themes)
- **Caveats:** Claude Design feature may not be available in API-only workflows; use direct CSS token prompt as fallback.


## 22. Autoskills Stack Detector (`autoskills-stack-detector`)
- **What it does:** Scans project files to automatically suggest and link relevant agent skills.
- **When to use:** Bootstrapping an agent in a new repository.

## 23. Awesome Claude Design System (`awesome-claude-design-system`)
- **What it does:** Scaffolds complete UI/UX systems using a `DESIGN.md` token source of truth.
- **When to use:** Establishing a unified aesthetic before writing frontend code.


## 29. Kronos Knowledge Graph (`kronos-knowledge-graph`)
- **What it does:** Semantic memory, temporal truth tracking, and protocol-driven development.
- **When to use:** Deep refactors requiring historical context.

## 30. VoxCPM Multimodal Voice (`voxcpm-multimodal-voice`)
- **What it does:** Voice design, controllable cloning, and TTS reasoning.
- **When to use:** Scripting for podcast/video generation.

## 31. Karpathy Coding Guardrails (`karpathy-coding-guardrails`)
- **What it does:** Enforces extreme simplicity and surgical, non-destructive edits.
- **When to use:** Writing or modifying any code.

## 32. Hermes Autonomous Learning (`hermes-autonomous-learning`)
- **What it does:** Dynamic skill creation and dialectic user modeling.
- **When to use:** Automating repetitive user workflows into permanent skills.

## 33. Postiz Social Publishing (`postiz-social-publishing`)
- **What it does:** Multi-platform social scheduling and content pipelines.
- **When to use:** Generating marketing copy to accompany a finished project.

## 34. GStack Startup Workflows (`gstack-startup-workflows`)
- **What it does:** Role-based execution layers (PM, Designer, QA) for macro-projects.
- **When to use:** Undertaking massive "0 to 1" application builds.

## 24. CLI-Anything Agent-Native Framework (`cli-anything-agent-native`)
- **What it does:** Converts existing CLI-based software into agent-native tools by wrapping them in structured harness layers — input validation, output normalization, error recovery, and agent-readable response formats.
- **When to use:** When an existing CLI tool needs to be reliably called by an AI agent in an N8N workflow, automation pipeline, or multi-agent system; when agent calls to CLI tools produce unpredictable output.
- **When NOT to use:** When the CLI tool already has a proper API or SDK; when the tool is only called interactively by humans.
- **Input/Output:** In: raw CLI tool + desired agent interface spec. Out: harness wrapper with structured input/output and error handling.
- **Dependencies:** Node.js or Python for harness layer; no mandatory framework.
- **Article Relevance:** MEDIUM — useful for wrapping CLI tools (markitdown CLI, WP-CLI, etc.) into agent-callable structured tools.
- **Source:** CLI-Anything pattern extraction.

## 25. Compound Engineering Workflow (`compound-engineering-workflow`)
- **What it does:** A 6-phase structured engineering workflow: Plan → Brainstorm → Work → Compound (combine parallel work) → Review → Reflect. Each phase has explicit deliverables and handoff criteria.
- **When to use:** Building a feature that spans multiple files, multiple agents, or multiple sessions; when work needs to be parallelized and merged coherently.
- **When NOT to use:** Simple single-file tasks; quick debugging sessions; exploratory spikes.
- **Input/Output:** In: feature spec. Out: structured plan → implementation across phases → reviewed and compounded result.
- **Key insight:** The "Compound" phase is the differentiator — it explicitly combines parallel streams before review, reducing integration bugs.
- **Article Relevance:** MEDIUM-HIGH — structure for multi-agent article template redesign sprints.
- **Interoperates with:** `planning-with-files-memory` (preserves state across phases), `oh-my-claudecode-orchestration` (coordinates parallel agents in compound phase).

## 26. PM Skills Framework (`pm-skills-framework`)
- **What it does:** Provides 65 PM skills (roadmapping, prioritization, stakeholder management, OKR writing, metrics definition) + 36 structured workflows + 8 productivity plugins for AI agents acting as product managers.
- **When to use:** When an agent needs to think and act like a product manager: writing PRDs, prioritizing features, planning sprints, or communicating strategy.
- **When NOT to use:** Pure implementation tasks; when the agent is acting as an engineer, not PM.
- **Input/Output:** In: product goal or feature request. Out: structured PM artifact (PRD, roadmap, OKR, prioritization matrix, stakeholder brief).
- **Dependencies:** No installs — prompt-level framework injection.
- **Article Relevance:** MEDIUM — useful for planning article generation systems as a product, writing requirements for the N8N article pipeline, or structuring client deliverables.

## 27. Planning-with-Files Memory (`planning-with-files-memory`)
- **What it does:** Manus-inspired persistent working memory via structured files: PLANNING.md, TASKS.md, PROGRESS.md, DECISIONS.md, ISSUES.md. The agent maintains these files as its external memory during multi-step work, enabling context persistence across sessions and handoffs between agents.
- **When to use:** Any multi-session or multi-agent project; when context overflow causes repeated work; when a project needs an audit trail of decisions; when handing off work to another agent.
- **When NOT to use:** Short, single-session tasks; when the overhead of maintaining memory files exceeds the benefit.
- **Input/Output:** In: project description + ongoing work context. Out: living set of structured markdown files that agents can read and write to maintain shared state.
- **Key files:** `PLANNING.md` (current plan), `TASKS.md` (status of all tasks), `PROGRESS.md` (what was done), `DECISIONS.md` (rationale log), `ISSUES.md` (blockers).
- **Article Relevance:** HIGH — directly applicable to article generation system: persistent memory for multi-session template redesigns, N8N workflow evolution, and client project state.
- **Interoperates with:** `claude-mem-persistent` (the two are complementary: claude-mem = semantic memory, planning-with-files = structured file-based state), `compound-engineering-workflow` (CE uses these files for phase handoffs).

## 28. Oh My Claude Code Orchestration (`oh-my-claudecode-orchestration`)
- **What it does:** Multi-agent orchestration plugin framework for Claude Code: defines orchestration patterns for spawning, coordinating, and merging results from multiple parallel Claude Code agents. Includes patterns for fan-out (one task → multiple agents), fan-in (collect results), and pipeline (sequential agents).
- **When to use:** When one task benefits from parallel agent execution: parallel article generation, parallel code review, parallel research, simultaneous test + implement.
- **When NOT to use:** When orchestration overhead exceeds the task duration; for single-threaded sequential tasks.
- **Input/Output:** In: task decomposition + orchestration pattern choice. Out: coordinated results from multiple agents, merged into a coherent output.
- **Key patterns:** Fan-out (parallel research), Fan-in (merge results), Pipeline (sequential hand-off), Competition (multiple agents solve same problem, best wins).
- **Article Relevance:** MEDIUM-HIGH — orchestrate parallel article generation across multiple clients or templates; fan-out research for competitor analysis.
- **Interoperates with:** `compound-engineering-workflow` (orchestration IS the "Compound" phase tool), `gstack-software-factory` (gstack uses orchestration for parallel sprint stages).

## 29. MarkItDown Document Pipeline (`markitdown-ingestion`)
- **What it does:** Microsoft's MarkItDown converts virtually any document format (PDF, DOCX, XLSX, PPTX, audio, video URLs, HTML, ZIP archives, images) to clean LLM-optimized Markdown. Available as Python library, CLI, and MCP server. Note: Entry #4 in this memo covers the core capability; this entry documents the full SKILL.md addition and enriched capabilities from GOD MODE #9 ingestion.
- **When to use:** Preprocessing ANY source material before feeding to an article generator or LLM — PDF reports, Excel keyword data, Word brand guidelines, audio interviews, YouTube videos, HTML competitor pages.
- **When NOT to use:** When source is already clean Markdown or plain text; for raw binary files where layout precision matters.
- **Input/Output:** In: file path, URL, or file-like object. Out: `result.text_content` — clean Markdown.
- **Dependencies:** `pip install markitdown[all]` — Python 3.10+. MCP server: `pip install markitdown-mcp`.
- **Key addition (GOD MODE #9):** Full SKILL.md now available at `.github/skills/markitdown-ingestion/`. Audio transcription via Whisper API. YouTube URL → transcript. ZIP batch processing. `[az-doc-intel]` for enterprise-grade OCR.
- **Article Relevance:** VERY HIGH — the single most important preprocessing tool for article content pipelines.

## 30. Claude-Mem Persistent Memory (`claude-mem-persistent`)
- **What it does:** Persistent cross-session memory for Claude Code agents (v6.5.0). Uses 5 lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd) to automatically save/retrieve context. SQLite + ChromaDB storage. 3-layer MCP workflow (search → timeline → get_observations) achieves 300-2,500 tokens vs 15,000+ for traditional RAG — 10x token savings.
- **When to use:** Long-running projects spanning multiple sessions; when agents repeatedly ask "what did we decide?"; when context overflow causes lost knowledge; for article projects that evolve over weeks.
- **When NOT to use:** One-off single-session tasks; when AGPL-3.0 license creates commercial concerns.
- **Input/Output:** In: observations captured during agent work. Out: relevant context injected into new sessions via MCP search.
- **Dependencies:** `npx claude-mem install` — Node.js 18+. Bun + uv auto-installed. Database at `~/.claude-mem/`.
- **Article Relevance:** HIGH — cross-session memory of article decisions, template versions, client rules, and WordPress state.
- **Caveats:** AGPL-3.0. ChromaDB requires specific Python version. Memory grows over time — periodic cleanup needed.

## 31. Kronos Semantic Memory (`kronos-semantic-memory`)
- **What it does:** Local pointer-based semantic memory system. Rust FastPath + SQLite FTS5 + ChromaDB hybrid. The Kronos Architect Protocol enforces search-before-build discipline: STOP & THINK → SEARCH → QUERY → REUSE → SYNTHESIS. 83-98% token reduction vs traditional RAG. 5-50x cost savings at scale. Windows-compatible via `setup.ps1`. MCP server for direct agent integration.
- **When to use:** Large codebases (100+ files) where context window can't hold everything; cost-sensitive workflows; when agents hallucinate names/paths; building a knowledge graph of templates and decisions.
- **When NOT to use:** Small projects (< 20 files); one-off scripts; non-technical teams.
- **Input/Output:** In: codebase + docs files. Out: knowledge graph queryable via MCP → pointer-based context injection.
- **Dependencies:** Python 3.10+, ChromaDB, SQLite FTS5, Visual Studio C++ Build Tools (Windows), OPENROUTER_API_KEY.
- **Install:** `./setup.ps1` (Windows). MCP uses venv Python path (not system Python).
- **Article Relevance:** MEDIUM-HIGH — ingest article templates + N8N workflows → query efficiently without loading everything.
- **Caveats:** OPENROUTER_API_KEY required. Initial ingestion time proportional to codebase size. Partial Croatian documentation (v0.6.2).

## 32. VoxCPM Voice Extension (`voxcpm-voice-extension`)
- **What it does:** Tokenizer-free TTS system (VoxCPM2 by OpenBMB). Zero-shot voice cloning from reference audio. Multilingual speech generation. Creative voice design without reference clips. Potential for audio article delivery.
- **When to use:** Audio article versions; podcast-style content generation; brand voice narration; future voice-enabled agent responses.
- **When NOT to use:** Core article generation (this is voice output only); when no GPU available; current article system (text-only focus). Mark as FUTURE ENHANCEMENT.
- **Input/Output:** In: text + optional reference audio for voice cloning. Out: synthesized speech audio.
- **Dependencies:** Python 3.10+, CUDA GPU, PyTorch. HuggingFace demo available for testing.
- **Article Relevance:** LOW-MEDIUM — optional future audio delivery channel; not needed for current core workflow.

## 33. Karpathy Behavioral Guardrails (`karpathy-coding-guardrails`)
- **What it does:** CLAUDE.md-based 4-principle behavioral framework: (1) Think Before Coding — state assumptions, ask vs guess; (2) Simplicity First — minimum code, no speculative features; (3) Surgical Changes — touch only what's required; (4) Goal-Driven Execution — success criteria over imperative instructions.
- **When to use:** Any coding session; always for article template work; when agents caused regressions via "helpful" side changes; when generated code is consistently overcomplicated.
- **When NOT to use:** Trivial one-liners; emergency hotfixes where speed trumps correctness.
- **Input/Output:** In: CLAUDE.md config (install once). Out: more predictable, minimal, correct code generation.
- **Dependencies:** Claude Code plugin: `/plugin marketplace add forrestchang/andrej-karpathy-skills`. OR: `curl -o CLAUDE.md [url]` for per-project.
- **Key synergy:** Karpathy = micro (per-task behavior). gstack = macro (per-sprint process). Use both together.
- **Article Relevance:** HIGH — prevents scope creep in N8N workflow edits; prevents accidental template restructuring when fixing one section.

## 34. Hermes Self-Improving Agent (`hermes-self-improving`)
- **What it does:** Nous Research's self-improving agent infrastructure. Closed learning loop: executes tasks → discovers patterns → autonomously creates skills → improves future performance. FTS5 full-text search across all past conversations. Honcho user modeling across sessions. 40+ tools, 6 terminal backends, messaging gateways (Telegram, Discord, Slack, WhatsApp, Signal). OpenClaw migration: `hermes claw migrate`.
- **When to use:** Long-running personal agent that should improve over time; multi-platform messaging continuity; scheduled automation (cron); when migrating from OpenClaw.
- **When NOT to use:** Windows native (WSL2 required); quick one-off tasks; infrastructure overhead not justified.
- **Input/Output:** In: conversation messages, files, URLs. Out: agent responses + autonomous skill creation + scheduled task execution.
- **Dependencies:** Linux/macOS/WSL2, Python 3.11, uv. Install: `curl [install.sh] | bash`. OpenClaw migration: `hermes claw migrate`.
- **Key caveat:** WSL2 REQUIRED on Windows — NOT native Windows compatible.
- **Article Relevance:** MEDIUM-HIGH — scheduled article batch generation; Telegram-accessible article requests; cross-platform continuity for ongoing content projects.
- **Interoperates with:** agentskills.io standard (shares skills with other supporting agents), OpenClaw migration path.

## 35. Postiz Social Publishing (`postiz-social-publishing`)
- **What it does:** Self-hosted AI social media scheduler supporting 15+ platforms. Public API + N8N custom node (`n8n-nodes-postiz`) + NodeJS SDK. Enables article-to-social post pipelines: WordPress publish → auto-schedule LinkedIn, Twitter, Reddit, Instagram posts.
- **When to use:** Article-to-social distribution; multi-platform scheduling after article publish; when N8N already handles article generation; for client content projects with social promotion.
- **When NOT to use:** Single-platform posting; low volume (< 10 posts/week); when cloud alternatives are preferred over self-hosting.
- **Input/Output:** In: content + platforms + schedule time + API key. Out: scheduled posts across all specified platforms + analytics.
- **Dependencies:** Self-host: Docker Compose + PostgreSQL + Redis. N8N node: `npm install n8n-nodes-postiz`. SDK: `npm install @postiz/node`.
- **License:** AGPL-3.0 — self-hosted free; commercial SaaS requires license.
- **Article Relevance:** MEDIUM — N8N article pipeline extension: add Postiz node after WordPress publish to auto-schedule social posts.

## 36. gstack Software Factory (`gstack-software-factory`)
- **What it does:** Garry Tan's (YC President) open source software factory. 23 specialist agents + 8 power tools implementing a complete sprint workflow: /office-hours (YC forcing questions) → /plan-ceo-review → /plan-eng-review → /design-consultation → /design-shotgun → /design-html (mockup→production HTML, 30KB, zero deps) → /review → /cso (OWASP+STRIDE security) → /qa (real browser testing) → /ship → /benchmark (Core Web Vitals) → /retro.
- **When to use:** Any non-trivial feature development; article template redesigns; security audits; performance benchmarking; when you want a full virtual engineering team in one tool.
- **When NOT to use:** Simple one-file tasks; tasks without git; trivial changes.
- **Input/Output:** In: feature spec or redesign goal. Out: planned, implemented, reviewed, tested, and shipped result with documentation.
- **Install:** `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup` — auto-detects GitHub Copilot.
- **Article Relevance:** HIGH — design-to-HTML pipeline (/design-consultation → /design-shotgun → /design-html) is exactly what article template redesign needs; /qa runs real browser tests on article pages; /benchmark tracks Core Web Vitals improvements.
- **Key synergy:** gstack (sprint workflow) + karpathy-coding-guardrails (per-task behavior) = the complete quality stack.
- **Pending Verification Source:** MALKA — see PENDING-VERIFICATION notes. Not ingested.


## 8. Context & Memory Manager (`context-memory-manager`)
- **What it does:** Optimizes context packing and multi-agent memory retention.
- **When to use:** Long sessions where agents risk forgetting architectural rules.

## 9. SuperClaude Framework Orchestration (`superclaude-framework-orchestration`)
- **What it does:** Auto-discovers skills and delegates tasks to sub-agents.
- **When to use:** Massive, multi-file epic implementations.

## 10. Design-to-Code Renderer (`design-to-code-renderer`)
- **What it does:** Translates design vibes and JSON payloads into semantic HTML.
- **When to use:** Converting mockups or raw data into beautiful UI components.

## 11. System Design Architect (`system-design-architect`)
- **What it does:** Enforces scalable architecture and developer best practices.
- **When to use:** Planning phases and database schema design.

## 12. Content Humanization & Social OSINT (`content-humanization-social`)
- **What it does:** De-AI's text and matches brand tone based on social profiles.
- **When to use:** Polishing article drafts and marketing copy.

## 13. CLI Automation Workflows (`cli-automation-workflows`)
- **What it does:** Configures CI/CD pipelines and optimizes local environments.
- **When to use:** Setting up GitHub actions, Zadig, or debloating Windows.

## 14. Meta-Prompt Optimization (`meta-prompt-optimization`)
- **What it does:** Refines system prompts and recommends model routing.
- **When to use:** Generating strict N8N pipeline instructions.


---

## Skills from 2026-04-20 GitHub Ingestion

**Date:** 2026-04-20
**Session:** Skills Mega-Ingestion (35 repos)
**Result:** 34 SKILL.md files created + html-redesign-mega (17 sub-skills)

### Key New Skills Added
- **html-redesign-mega** — 17 sub-skills for WordPress-safe RTL HTML redesign (most important)
- **harness-skill** — 6 multi-agent team architectures, +60% quality improvement
- **buffett-skills** — Investment analysis system, +33% pass rate improvement
- **friday-skill** — 24/7 autonomous AI assistant architecture (18 cron jobs, self-evolving)
- **skillui** — Design system extractor (
px skillui --url [site])
- **hue-design-skill** — Brand design system generator from URL/name/screenshot
- **paper-orchestra-skill** — Multi-agent academic paper pipeline (7 skills)
- **agentic-seo** — AEO/GEO audit (
px agentic-seo [url])
- **android-skills-mcp** — Google official Android skills as MCP server
- **autoskills** — Auto-detect stack, install skills (
px autoskills)

### Category Breakdown
UI/UX: 1 | Design Systems: 8 | Agent Skills: 6 | Coding: 7 | Research: 5 | Prompting: 3 | Automation: 2 | Other: 4

### Files Created
- 34x C:\Users\seoadmin\.agents\skills\<name>\SKILL.md
- 5x C:\Users\seoadmin\skill_expansion_workspace\*.md (registry, active set, workflow map, merge report, risk report)
- Obsidian backup: C:\Obsidian\CODE AGENTS SKILL BACKUPS\2026-04-20-skills-ingestion\

### Notes
- bchao1/paper-finder: 404, note file created in paper-orchestra-skill/
- seedance-skill: financial risk (.30/sec) — confirm budget before use
- harness-skill: requires experimental flag CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
- All 300+ existing skills preserved (zero deletions)

---

## Skills from 2026-04-20 GitHub Ingestion

### shopify-admin-skills
- **What:** 63 AI agent skills for Shopify Admin GraphQL API
- **When to use:** Managing Shopify stores — orders, inventory, pricing, refunds, fraud, fulfillment
- **When NOT:** Shopify storefront (not admin), Shopify Partner API, non-Shopify ecommerce
- **Input:** Business request + Shopify credentials; **Output:** GraphQL mutations with dry-run preview

### skillclaw-evolver
- **What:** Self-evolving skill system — extracts patterns from real interactions, propagates improvements
- **When to use:** Building agent systems that improve over time from real usage
- **When NOT:** One-off scripts, disposable agents with no reuse
- **Input:** Agent interactions; **Output:** Updated skill definitions

### paper-orchestra-writing
- **What:** 5-agent LaTeX paper writing pipeline (Outline→Plot→LitReview→Write→Refine)
- **When to use:** Turning experimental logs + research into conference-ready papers
- **When NOT:** Blog posts, non-academic writing, short content
- **Input:** idea.md + experimental_log.md + template.tex; **Output:** Submission-ready LaTeX

### spec-driven-dev-lidr
- **What:** SDD workflow: Free-form → PRD → Issues → Tasks → Code → Review → Audit
- **When to use:** Non-trivial features requiring traceability and review gates
- **When NOT:** Hot-fixes, quick experiments, 1-file scripts
- **Input:** Feature description; **Output:** PRD + issues + tasks + reviewed code

### lich-skills-personal
- **What:** 5 skills: spec-driven-dev, debug-hypothesis loop, wiki-aggregate, tavily-search, nano-banana
- **When to use:** Engineering workflows needing scientific debugging or multi-source research
- **When NOT:** Simple queries needing no structured methodology
- **Input:** Bug/research question; **Output:** Hypothesis tree → confirmed root cause OR aggregated research brief

### minimax-skills-suite
- **What:** 17 cross-platform skills: frontend, Android, iOS, Flutter, multimodal content (TTS, music, video)
- **When to use:** Building apps with MiniMax APIs or generating rich media
- **When NOT:** Non-MiniMax API workflows for multimodal content
- **Input:** Feature request; **Output:** Platform-appropriate code or media assets

### skill-based-architecture-meta
- **What:** Meta-skill that analyzes codebases and generates project-specific skill files
- **When to use:** Onboarding to new codebase, standardizing AI behavior across team
- **When NOT:** Single-developer scripts, prototype codebases
- **Input:** Codebase directory; **Output:** skills/<name>/SKILL.md

### agentic-seo-audit
- **What:** AEO audit CLI — 10 checks, 5 categories, 100-point score for AI discoverability
- **When to use:** Optimizing docs/websites for AI agent discovery (llms.txt, robots.txt, skill.md)
- **When NOT:** Traditional SEO (keyword rankings, backlinks) — different domain
- **Input:** URL or directory path; **Output:** JSON/markdown audit report with score

### buffett-investment
- **What:** Warren Buffett complete investment thinking system with 8 industry playbooks
- **When to use:** Analyzing any stock, company, financial report, or value investing question
- **When NOT:** Day trading, crypto speculation, market timing
- **Input:** Company/stock + question; **Output:** Structured analysis (moat/management/valuation/risks)

### skillui-design-extractor
- **What:** CLI that extracts design systems from URLs/repos into Claude-ready SKILL.md
- **When to use:** Replicating a website's visual design, onboarding to design systems
- **When NOT:** Creating new design systems from scratch
- **Input:** URL, git repo, or local directory; **Output:** SKILL.md + design tokens JSON + screenshots

### caveman-mode
- **What:** 6-level communication compression (lite→full→ultra→wenyan variants)
- **When to use:** Long coding sessions, token-limited contexts, fast iteration
- **When NOT:** Security warnings, destructive action confirmations, complex multi-step sequences
- **Input:** Trigger phrase + optional level; **Output:** Compressed responses for session

### spider-king-reverse
- **What:** Web protocol reverse engineering methodology — browser → pure Python collector
- **When to use:** When scraping fails due to dynamic params, signatures, encryption, WebSocket sessions
- **When NOT:** Simple static HTML pages (use scrapling instead)
- **Input:** Target URL + failure symptoms; **Output:** Python collector that works without browser

### paper-finder-ml
- **What:** ML/AI paper discovery with persistent memory bank, mind-graph, BibTeX
- **When to use:** Literature reviews, related work searches, paper collections
- **When NOT:** Non-ML/AI papers (use general search); when training knowledge is sufficient for 2020-era papers
- **Input:** Research topic; **Output:** Organized paper collection + references.bib + summaries

### hue-brand-design
- **What:** Analyzes any brand from URL/name/screenshot → complete design system SKILL.md
- **When to use:** Capturing existing brand identity for consistent AI-generated UI
- **When NOT:** Creating entirely new brand identity from scratch
- **Input:** URL, brand name, or screenshot; **Output:** design-model.yaml + landing-page.html

### voice-writing-template
- **What:** 7-section framework for capturing personal writing voice — calibrates AI to write like you
- **When to use:** Ghostwriting, content at scale that must sound authentic
- **When NOT:** Technical documentation (voice matters less there)
- **Input:** 10-20 samples of your own writing; **Output:** Calibrated voice SKILL.md

### jetpack-compose-audit
- **What:** Evidence-based Compose audit with actual Compiler reports — 4 categories, 0-10 scored
- **When to use:** Pre-ship Compose feature review, performance complaints, recomposition issues
- **When NOT:** XML layouts, non-Compose Android UI
- **Input:** Module path; **Output:** COMPOSE-AUDIT-REPORT.md with file:line citations

### material-3-md
- **What:** MD3 implementation guide for Compose (primary), Flutter (secondary), Web (limited)
- **When to use:** Implementing Material Design 3 components, theming, adaptive layouts
- **When NOT:** Material Design 2 projects; Web with M3 Expressive features needed (not available)
- **Input:** Component/theme request; **Output:** MD3-compliant Compose/Flutter code

### talk-normal-rules
- **What:** System prompt that eliminates AI filler, hedging, hollow affirmations
- **When to use:** AI sounds too corporate, padded, or formal
- **When NOT:** When caveats and disclaimers are genuinely needed
- **Input:** Add to system prompt; **Output:** Direct, human-style AI responses

### engineering-figure-banana
- **What:** Two-mode figure generation — image mode (diagrams) + plot mode (quantitative charts)
- **When to use:** Generating publication figures for engineering/CS papers
- **When NOT:** General data visualization, infographics, marketing charts
- **Input:** Figure description + mode selection; **Output:** PNG/SVG figure

### email-campaigns-html
- **What:** HTML email builder with Resend pipeline, frost-glass design, GIF optimization
- **When to use:** Launch emails, newsletters, drip sequences with modern design
- **When NOT:** Transactional system emails (use simpler templates)
- **Input:** Email brief; **Output:** Production HTML email + Resend send code

### html-ppt-studio
- **What:** HTML presentations with 36 themes, 31 layouts, 47 animations, presenter mode
- **When to use:** Creating any presentation, pitch deck, or data dashboard
- **When NOT:** Collaborative presentation tools (Google Slides, PowerPoint sharing)
- **Input:** Topic + theme preference; **Output:** self-contained HTML file

### 3gpp-telecom-expert
- **What:** Senior telecom consultant skill — 2G-6G, all releases, all protocol stacks
- **When to use:** Any 3GPP protocol question, network planning, security analysis
- **When NOT:** Wi-Fi, Bluetooth, proprietary wireless (non-3GPP standards)
- **Input:** Telecom question; **Output:** Standards-grounded answer with TS/TR citations

### ai-workflow-prd
- **What:** AI dev workflow: free-form plan → PRD → vertical-slice issues → tasks → review → audit
- **When to use:** Feature planning with AI assistance; traceability required
- **When NOT:** Same as spec-driven-dev-lidr — hot-fixes, experiments
- **Input:** Feature description + free-form thinking; **Output:** Structured PRD + issues + tasks

### friday-autonomous-ai
- **What:** 24/7 Claude Code autonomous assistant with 18 crons, self-evolving cognition, Telegram interface
- **When to use:** Building persistent always-on assistant with proactive capabilities
- **When NOT:** Simple chatbot, one-off assistant, if Anthropic Max is not budget-viable
- **Input:** SETUP.md → Claude Code; **Output:** Running 24/7 assistant system

### antivibe-learning
- **What:** Post-coding learning guide generator — explains what/why/when/alternatives for AI code
- **When to use:** After implementing with AI assistance, when you want to actually understand the code
- **When NOT:** Time-critical shipping when learning can be deferred
- **Input:** AI-generated code; **Output:** deep-dive/*.md learning guide

### logo-generator-svg
- **What:** 6+ SVG logo variants + 12 professional showcase backgrounds via Gemini
- **When to use:** Quick professional logo generation for startups/side projects
- **When NOT:** When client requires working with a human designer; complex illustrative logos
- **Input:** Product name + industry + core concept; **Output:** SVG files + showcase images + HTML

### how-codebase-explain
- **What:** Codebase explainer with auto-selected Explain/Critique modes, parallel exploration
- **When to use:** Onboarding to unfamiliar code, architectural critique, understanding complex flows
- **When NOT:** Simple function-level questions (just ask directly)
- **Input:** Natural language question; **Output:** Structured explanation or critique

### harness-team-factory
- **What:** Domain description → complete agent team architecture (6 patterns + skills)
- **When to use:** Designing multi-agent workflows for any complex domain
- **When NOT:** Single-agent tasks, simple automation without inter-agent communication
- **Input:** Domain sentence; **Output:** .claude/agents/ + .claude/skills/ directories

### ai-life-obsidian
- **What:** Obsidian vault integration — summarize any content, transcribe calls
- **When to use:** Building personal knowledge base, processing content at scale
- **When NOT:** Corporate knowledge bases (Notion/Confluence better), team wikis
- **Input:** URL/file/recording; **Output:** Vault notes with wikilinks + BibTeX

### marp-slides-builder
- **What:** MARP presentations with SVG charts, dashboard components, 22 reference decks
- **When to use:** Technical presentations, data dashboards, content where Markdown authoring is preferred
- **When NOT:** Highly visual presentations requiring design tool precision
- **Input:** Topic + style + data; **Output:** .md MARP file → PDF/PPTX/HTML

### seedance-video-gen
- **What:** App screenshots → cinematic liquid glass motion graphics via Seedance 2.0
- **When to use:** Promo videos, motion identity sequences, app store video ads
- **When NOT:** Tutorial videos, talking-head content, screen recordings
- **Input:** App screenshots (3-5) + description; **Output:** 4-10 second MP4

### svg-hand-drawn-anim
- **What:** SVG → hand-drawn animation with path-first reveal, fill afterwards
- **When to use:** Adding charm to diagrams in presentations, demos, proposals
- **When NOT:** Complex interactive SVG, animated data visualizations with live data
- **Input:** SVG file/URL; **Output:** preview.html + player.js

### android-skills-mcp
- **What:** MCP server for Google android/skills — list, search, get skills across 7 target formats
- **When to use:** Android Compose development with any MCP-capable AI coding assistant
- **When NOT:** Non-Android development
- **Input:** 
px android-skills-mcp in MCP config; **Output:** Skills available to all MCP clients

### html-redesign-mega
- **What:** 17 sub-skills for complete HTML/WordPress page redesign
- **When to use:** Redesigning any HTML page with comprehensive UX, accessibility, and conversion improvements
- **When NOT:** Static site generators with their own design systems; Webflow/Framer
- **Input:** HTML page URL or raw HTML; **Output:** Production-ready WordPress-safe HTML

