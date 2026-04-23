# Code Agents Global Skill Examples
**Last Updated:** 2026-04-16

This file contains practical execution examples for the expanded agent skill set.

## 1. Scrapling Extraction (Stealth Data Fetch)
**Category:** Web Scraping / Data Ingestion
**Source:** D4Vinci/Scrapling
**What makes it strong:** Uses adaptive selectors and bypasses simple bot protection without heavy Playwright overhead.
**Recommended Use Case:** Extracting a competitor's pricing table or feature list to feed into a comparison article generator.
**Warning:** Do not use heavy fetchers if standard HTTP is unblocked.

## 2. Million Debug Loop (Evidence-Based Fix)
**Category:** Debugging
**Source:** millionco/debug-agent
**What makes it strong:** Replaces "LGTM" guesswork with hard runtime logs.
**Recommended Use Case:** A WordPress HTML template is dropping a specific `</div>` dynamically. The agent instruments the generator script, reads the NDJSON output, finds the exact line where the string manipulation fails, and patches it.

## 3. MarkItDown Ingestion
**Category:** Format Conversion
**Source:** microsoft/markitdown
**What makes it strong:** Preserves tables and image context from `.docx` or `.pdf` files.
**Recommended Use Case:** The user provides a 50-page PDF report. The agent uses `markitdown` to convert the PDF into Markdown, preserving data tables, which are then passed to the article generator for analysis.

## 4. SEOMachine Link Architecture
**Category:** SEO Optimization
**Source:** thecraighewitt/seomachine
**What makes it strong:** Contextual internal linking rather than forced keyword stuffing.
**Recommended Use Case:** The agent reviews a newly generated article, parses the site's existing sitemap, and automatically injects 3 highly relevant internal links with varied anchor text.

## 5. Codeburn Token Optimization
**Category:** Agent Efficiency
**Source:** AgentSeal/codeburn
**What makes it strong:** Identifies wasteful file re-reads during long coding sessions.
**Recommended Use Case:** The agent runs a session audit, notices it has read `package-lock.json` 14 times, and adds it to `.claudeignore` to save 500k tokens per session.


## 6. Design-to-Code Rendering (Vibe Translation)
**Category:** Frontend / UI
**Source:** vibe_figma / json-render
**What makes it strong:** Safely converts arbitrary JSON lists into beautifully styled HTML grids without React dependencies.
**Recommended Use Case:** An N8N workflow outputs an array of 5 product features. The agent uses this skill to iterate the JSON into a responsive Bento grid layout.

## 7. Content Humanization (Anti-AI Text)
**Category:** Content Quality
**Source:** blader/humanizer
**What makes it strong:** Actively hunts and destroys LLM "tells" (like starting paragraphs with "In today's fast-paced digital world").
**Recommended Use Case:** Running a final pass on the HTML article content to ensure the tone matches a senior human executive.


## 6. Design-to-Code Rendering (Vibe Translation)
**Category:** Frontend / UI
**Source:** vibe_figma / json-render
**What makes it strong:** Safely converts arbitrary JSON lists into beautifully styled HTML grids without React dependencies.
**Recommended Use Case:** An N8N workflow outputs an array of 5 product features. The agent uses this skill to iterate the JSON into a responsive Bento grid layout.

## 7. Content Humanization (Anti-AI Text)
**Category:** Content Quality
**Source:** blader/humanizer
**What makes it strong:** Actively hunts and destroys LLM "tells" (like starting paragraphs with "In today's fast-paced digital world").
**Recommended Use Case:** Running a final pass on the HTML article content to ensure the tone matches a senior human executive.


## 8. Visual Layout to HTML Extraction
**Category:** Frontend / UI
**Source:** abi/screenshot-to-code
**What makes it strong:** Enforces semantic structure rather than absolute-positioned "spaghetti code".
**Recommended Use Case:** The user uploads a screenshot of a Bento grid. The agent uses this skill to infer the exact CSS Grid `grid-template-columns` and `gap` values needed to recreate it natively.

## 9. Presentation Deck Generation
**Category:** Documentation / Reporting
**Source:** hakimel/reveal.js
**What makes it strong:** Automatically transforms a flat document into a paginated narrative.
**Recommended Use Case:** An agent generates a comprehensive SEO audit report. The user asks for a summary deck. The agent wraps the H2s in `<section>` tags, outputs a Reveal.js HTML file, and presents the findings visually.

## 10. Bash Obfuscation Awareness (Shell Security Audit)
**Category:** Security / CLI
**Source:** Bashfuscator/Bashfuscator
**What makes it strong:** Recognizes obfuscation patterns (POSIX, Data, External tools) so agents can flag suspicious shell payloads before running them.
**Recommended Use Case:** An agent receives a CI/CD pipeline script from an external source. Before executing, it audits the script for signs of eval-based obfuscation (`eval "$(echo ... | base64 -d)"`) and refuses or warns before execution.
**Caveat:** This skill is for defensive awareness only — do not generate obfuscated bash.

## 11. JavaScript Foundations Deep Reasoning
**Category:** Frontend / Architecture
**Source:** leonardomso/33-js-concepts
**What makes it strong:** Goes beyond syntax to explain *why* JS behaves the way it does — event loop, closure scoping, prototype chain, async/await execution order.
**Recommended Use Case:** An N8N Code node is failing with "Cannot read property of undefined" after async operations. The agent applies Event Loop + Promise execution order reasoning to identify that the node is reading data before the async fetch resolves, and fixes by awaiting properly.

## 12. Crawlee Site Audit (Content Extraction Pipeline)
**Category:** Web Scraping / Content Acquisition
**Source:** apify/crawlee
**What makes it strong:** Persistent URL queue, Cheerio/Playwright choice, automatic retry, structured Dataset output — production-ready in ~20 lines.
**Recommended Use Case:** Before redesigning a client's article template, the agent uses Crawlee to crawl all 200 article URLs on the site, collecting H1, meta description, word count, and H2 structure for each. The resulting JSON dataset informs which structural patterns are currently used and what needs improvement.

## 13. CS Algorithmic Reasoning (Performance Problem)
**Category:** System Design / Architecture
**Source:** jwasham/coding-interview-university
**What makes it strong:** Grounds decisions in complexity analysis rather than intuition — prevents accidentally writing O(n²) solutions when O(n) is trivially available.
**Recommended Use Case:** An article deduplication step in the N8N pipeline is timing out on 5,000 items. The agent reviews the current implementation (nested array .includes() = O(n²)), identifies the pattern as a linear search in a loop, and replaces with a Set lookup (O(n) total), reducing runtime from ~25 seconds to under 1 second.

## 14. AppFlowy Workspace Organization Pattern
**Category:** Knowledge Management / Productivity
**Source:** AppFlowy-IO/AppFlowy
**What makes it strong:** Space→Database→Document hierarchy applied to agent systems provides a clear mental model for organizing skills, playbooks, templates, and backups.
**Recommended Use Case:** A client project has grown to 40+ article templates, 15 N8N workflows, and 3 agent skill sets. The agent applies the AppFlowy Space/Grid/Document hierarchy to restructure the project folder: one `Space` per client → Grid for article tracking → Documents for templates and workflows. This prevents the "flat folder chaos" that kills large content projects.

## 15. Autoskills Project Bootstrap (GOD MODE #7)
**Category:** Agent Automation / Project Setup
**Source:** midudev/autoskills
**What makes it strong:** Zero-config skill bootstrap — one `npx autoskills` command reads your project's config files and installs exactly the right AI agent skills. The `-a claude-code` flag auto-generates a fresh CLAUDE.md summary.
**Recommended Use Case:** A new article-generation system project is started with Next.js, TypeScript, and Supabase. The agent runs `npx autoskills` in the project root. Autoskills detects the stack, installs React, TypeScript Advanced Types, Supabase, SEO optimization, and frontend-design skills automatically. Running `npx autoskills -a claude-code` generates a CLAUDE.md that documents all installed skills — the new article-system copilot immediately has full context about the project's skill set.
**Caveat:** Node.js >= 22 required. Skills sourced from skills.sh — review installed skill quality before treating them as authoritative.

## 16. DESIGN.md Article Template System (GOD MODE #7)
**Category:** Design System / Article Template / CSS Tokens
**Source:** VoltAgent/awesome-claude-design
**What makes it strong:** A 9-section structured markdown spec that bridges "brand identity" and "CSS implementation" — Claude Design generates working CSS custom properties, component HTML, and embedded regeneration prompts from a single file.
**Recommended Use Case:** The galoz.co.il article template needs a coherent design system. The agent writes a DESIGN.md for the editorial brand (Section 1: "authoritative Israeli news editorial, clean and modern"; Section 2: brand primary blue, white background, gray borders; Section 3: Heebo display + Heebo body for Hebrew + English; Sections 4-8: components, layout, elevation, guardrails, responsive rules; Section 9: embeds the agent prompt for future regeneration). The file is uploaded to Claude Design → receives `colors_and_type.css` with all design tokens → the agent pastes the `:root { }` block into the article template `<style>` block → all article components inherit the brand system. Section 9's Agent Prompt Guide is embedded into the N8N workflow prompt so every future template regeneration stays on-system.
**Reference brands for article design:** WIRED (editorial density), Notion (knowledge article warmth), Mintlify (clean documentation style), Sanity (CMS-first editorial).


## 10. Automated Skill Discovery
**Category:** Agent Orchestration
**Source:** midudev/autoskills
**What makes it strong:** Contextualizes the agent instantly without human intervention.
**Recommended Use Case:** An agent lands in a Vue.js repo, detects `package.json`, and automatically appends the `skill-vue-pinia` and `skill-tailwind` paths into `CLAUDE.md`.

## 11. DESIGN.md Enforcement
**Category:** UI/UX Design Systems
**Source:** VoltAgent/awesome-claude-design
**What makes it strong:** Replaces vague "make it look good" prompts with deterministic CSS token matrices.
**Recommended Use Case:** The agent is asked to redesign a pricing page. Instead of guessing colors, it first generates a `DESIGN.md` mapping the exact HEX values, border-radii, and shadow depths, then applies them systematically.


## 14. Surgical Editing Guardrails
**Category:** Coding Discipline
**Source:** forrestchang/andrej-karpathy-skills
**What makes it strong:** Prevents the dreaded "agent rewrite" where fixing a typo breaks the entire application.
**Recommended Use Case:** The user asks to change a button color. The agent uses `replace` on the exact CSS line rather than rewriting the entire `index.html` file and accidentally dropping the footer.

## 15. Multi-Role QA Simulation
**Category:** Validation
**Source:** garrytan/gstack
**What makes it strong:** Ensures outputs aren't just "technically correct", but actually good.
**Recommended Use Case:** Before finalizing a landing page, the agent mentally steps into the "Designer" role to check contrast, then the "PM" role to check CTA copy, then the "Security" role to check input sanitization.

## 17. CLI Harness for Agent Tool Wrapping (GOD MODE #8)
**Category:** Agent-Native Tool Integration
**Source:** CLI-Anything pattern
**What makes it strong:** Transforms unpredictable CLI output into structured agent-readable data — prevents parsing failures and retry loops in N8N workflows that call CLI tools.
**Recommended Use Case:** The N8N article pipeline calls `markitdown` CLI to convert client PDFs. Raw stdout is unpredictable (warnings mixed with content). The agent wraps markitdown in a harness: validates the input file exists, calls `markitdown file.pdf`, parses stdout into `{ success: bool, content: string, error: string }`, and propagates structured errors upstream. The N8N node now receives clean JSON instead of raw text.

## 18. Compound Engineering for Multi-Session Redesign (GOD MODE #8)
**Category:** Engineering Workflow / Multi-Agent
**Source:** Compound Engineering Workflow
**What makes it strong:** The 6 phases enforce explicit "what did we decide?" checkpoints, preventing the "let me just rewrite everything from scratch" impulse when resuming work after days.
**Recommended Use Case:** A client requests a major article template redesign spanning 3 sessions. Phase 1 (Plan): agent writes PLANNING.md with full scope. Phase 2 (Brainstorm): agent generates 5 design approaches. Phase 3 (Work): parallel agents implement approach B (HTML structure) and approach C (CSS tokens). Phase 4 (Compound): results merged into unified template. Phase 5 (Review): review agent checks for integration bugs, accessibility, schema. Phase 6 (Reflect): DECISIONS.md updated with rationale for choices made.

## 19. PM Framework for Article System Requirements (GOD MODE #8)
**Category:** Product Management / Requirements
**Source:** PM Skills Framework (65 skills + 36 workflows)
**What makes it strong:** Gives the agent a PM mindset — instead of just implementing requests, it asks the right questions first: Who is the user? What is the success metric? What is the MVP?
**Recommended Use Case:** Client says "improve the article generation system." Without PM framing, agent randomly adds features. With PM framework: agent writes a PRD — "Current state: X articles/week, average CTR 2.1%. Target state: 2x articles/week, CTR 3%+. Problem: template not mobile-first, schema incomplete. Solution: responsive template rewrite + FAQ schema + social meta. Success metric: Core Web Vitals green + CTR improvement in 4 weeks." The PRD becomes the source of truth for the entire redesign.

## 20. Planning Files for Multi-Agent Article Work (GOD MODE #8)
**Category:** Memory / Context / Multi-Agent Coordination
**Source:** Planning-with-Files Memory pattern
**What makes it strong:** Creates a shared memory layer that ALL agents can read and write to — no context loss between sessions, no duplicate work, no agents asking "what did we decide?".
**Recommended Use Case:** Article redesign project: `PLANNING.md` has the current design system spec. `TASKS.md` tracks 40 tasks with status (pending/in_progress/done/blocked). `DECISIONS.md` records "decided to use CSS custom properties instead of SCSS variables because the N8N output strips SCSS preprocessors." `ISSUES.md` notes "Hebrew RTL support is blocked pending client confirmation of font choice." Three agents (template builder, CSS agent, schema agent) all read/write the same files — no coordination call needed.

## 21. Multi-Agent Article Generation Orchestration (GOD MODE #8)
**Category:** Multi-Agent Orchestration
**Source:** Oh My Claude Code Orchestration
**What makes it strong:** Fan-out → fan-in makes parallel article generation coherent — 5 articles written simultaneously, results merged, reviewed as a batch.
**Recommended Use Case:** Client needs 20 articles in one batch. Single agent: 20 sequential runs = slow. Orchestrated: fan-out to 5 parallel agents (4 articles each), run simultaneously. Each writes its articles to a numbered output file. Fan-in agent collects all 20, validates schema, deduplicates any repeated content, formats for WordPress bulk import. Total time: 1/5 of sequential. Merged output: coherent batch ready for upload.

## 22. MarkItDown Client PDF to Article Draft (GOD MODE #9)
**Category:** Content Pipeline / Document Conversion
**Source:** microsoft/markitdown
**What makes it strong:** One command converts a client's PDF report into clean Markdown — feeding directly into the article generator without manual copy-paste or formatting work.
**Recommended Use Case:** A client provides a 40-page PDF sustainability report and requests 5 articles from its contents. The N8N workflow receives the PDF path, runs a Code node: `markitdown report.pdf` → outputs clean Markdown → LLM splits into 5 topic chunks → generates 5 structured articles. Without MarkItDown, this required manual extraction. With it: fully automated. The agent also extracts the client's Excel keyword list with `markitdown keywords.xlsx` → Markdown table → LLM matches keywords to articles.

## 23. Cross-Session Memory for Long Article Projects (GOD MODE #9)
**Category:** Memory / Context Retention
**Source:** thedotmack/claude-mem
**What makes it strong:** PostToolUse hook captures what was just done; SessionStart hook retrieves it next time — zero manual context catch-up.
**Recommended Use Case:** Week 1: Agent generates 30 articles for galoz.co.il, decides to use FAQ schema on all articles after testing showed CTR improvement. Week 2: New session starts. Without claude-mem: agent doesn't know what was done, asks again. With claude-mem: SessionStart retrieves "decided FAQ schema = yes, tested CTR improved from 2.1% to 3.4%, apply to all templates." Agent immediately continues from correct state. PostToolUse also captured: which 30 WordPress post IDs were created, which keywords were used, which H1 patterns performed best.

## 24. Kronos for Article Template Knowledge Search (GOD MODE #9)
**Category:** Semantic Memory / Codebase Search
**Source:** Ja1Denis/Kronos
**What makes it strong:** Pointer-based search returns "here's where that exists" in 300 tokens vs loading the full 200KB of templates and workflows into context (15,000+ tokens).
**Recommended Use Case:** An agent needs to find "how does the galoz article template handle Hebrew RTL?" Without Kronos: load all 15 template files into context, search manually, burn tokens. With Kronos: `@kronos How does the article template handle Hebrew RTL text?` → returns a pointer to `Improved_HTML_Template_galoz.html:line:87` (the `.rtl-content` CSS block) + pointer to `Improved_N8N_Prompt_galoz.txt:line:34` (the RTL handling instruction). Agent fetches just those two sections. 97%+ token savings. No hallucinated file names.

## 25. Audio Interview to Article (GOD MODE #9)
**Category:** Multimodal Content / Voice-to-Article
**Source:** OpenBMB/VoxCPM (voice awareness) + microsoft/markitdown (audio transcription)
**What makes it strong:** Demonstrates the audio → text → article pipeline using two complementary skills.
**Recommended Use Case:** A client records a 20-minute interview with their CEO for an article. Agent runs: `markitdown ceo-interview.mp3` → MarkItDown calls Whisper API → returns full transcript as Markdown → agent structures it into an article (intro, 5 key themes as H2s, quotes as blockquotes, conclusion). VoxCPM note: if client also wants an audio version of the published article, VoxCPM2 would generate narration in the CEO's voice from the published article text (future enhancement, GPU required).

## 26. Behavioral Guardrails for Template Fixes (GOD MODE #9)
**Category:** Coding Behavior / Quality Enforcement
**Source:** forrestchang/andrej-karpathy-skills
**What makes it strong:** Prevents the #1 failure mode in AI article template work — agent asked to fix one thing, rewrites three others.
**Recommended Use Case:** Client reports: "The FAQ section doesn't render correctly on mobile." Without guardrails: agent "fixes" mobile FAQ → also refactors the H2 section, modifies the breadcrumb, and "cleans up" the CSS (causing regressions). With Karpathy guardrails: agent asks "I see two interpretations: (a) fix only `.faq-section` responsive CSS; or (b) audit all mobile breakpoints. Which?" → agent implements ONLY the surgical fix → traces every changed line to the mobile FAQ issue → verifies via the goal: "FAQ section passes mobile responsive test at 375px." Zero collateral damage.

## 27. Hermes for Scheduled Article Generation (GOD MODE #9)
**Category:** Agent Infrastructure / Autonomous Scheduling
**Source:** NousResearch/hermes-agent
**What makes it strong:** Cron scheduler + Telegram delivery = fully autonomous article generation with human-readable status updates — no manual triggering.
**Recommended Use Case:** An article system generates 3 new articles every day at 6am for a client. Hermes setup: `hermes gateway` → enable Telegram. Schedule: "Every weekday at 6am, run the galoz article generation workflow: fetch 3 new keywords from the keyword queue, generate 3 articles using the approved template, post to WordPress via API, send me a Telegram summary with the titles, URLs, and word counts." Agent runs autonomously. If an article fails generation, Hermes sends a failure alert on Telegram with the error. The FTS5 session search lets you ask "what did you generate last Tuesday?" and Hermes returns the full generation log.

## 28. N8N Article-to-Social Pipeline (GOD MODE #9)
**Category:** Social Publishing / Distribution
**Source:** gitroomhq/postiz-app
**What makes it strong:** N8N node integration makes article-to-social distribution a one-node addition to an existing N8N article generation workflow.
**Recommended Use Case:** Existing N8N workflow: [Article Generator] → [WordPress Publish]. Addition: [WordPress Publish] → [Postiz Node]. Postiz node config: platforms = ['linkedin', 'twitter', 'reddit']. Content template: `New article: "${article.title}" | ${article.excerpt} | Read more: ${article.url}`. Schedule: LinkedIn at +1hr, Twitter at +2hr (thread format), Reddit at +4hr (appropriate subreddit from SEO metadata). Result: every published article automatically generates social posts across 3 platforms on a staggered schedule. N8N install: `npm install n8n-nodes-postiz` in ~/.n8n/custom, restart n8n.

## 29. gstack Article Template Redesign Pipeline (GOD MODE #9)
**Category:** Design Engineering / Article Template
**Source:** garrytan/gstack
**What makes it strong:** /design-consultation → /design-shotgun → /design-html gives a complete design-to-production-HTML pipeline specifically for article templates — not wireframes, actual working HTML.
**Recommended Use Case:** Client needs a full redesign of the jacknows.ai article template. Sprint flow: (1) `/office-hours` — "What makes this article template a success? Who reads it? What's the one metric that matters?" → Forces clarity before any design work. (2) `/plan-design-review` — rates the current template 0-10 across readability, hierarchy, mobile, performance, trust signals. (3) `/design-consultation` — builds a DESIGN.md with brand tokens, typography, layout spec. (4) `/design-shotgun` — generates 4-6 visual variants via AI image generation. (5) `/design-html` — approved variant → production HTML (Pretext layout, 30KB, zero deps). (6) `/qa` — opens real browser, tests at 375px, validates schema, clicks all links. (7) `/benchmark` — records Core Web Vitals baseline. (8) `/ship` — opens PR with test coverage. Article template shipped in one structured sprint, with real browser QA and performance baseline.


## 6. Design-to-Code Rendering (Vibe Translation)
**Category:** Frontend / UI
**Source:** vibe_figma / json-render
**What makes it strong:** Safely converts arbitrary JSON lists into beautifully styled HTML grids without React dependencies.
**Recommended Use Case:** An N8N workflow outputs an array of 5 product features. The agent uses this skill to iterate the JSON into a responsive Bento grid layout.

## 7. Content Humanization (Anti-AI Text)
**Category:** Content Quality
**Source:** blader/humanizer
**What makes it strong:** Actively hunts and destroys LLM "tells" (like starting paragraphs with "In today's fast-paced digital world").
**Recommended Use Case:** Running a final pass on the HTML article content to ensure the tone matches a senior human executive.


---

## New Skill Examples — 2026-04-20

### html-redesign-mega
"Redesign this article HTML template for galoz.co.il — WordPress-safe, RTL, collapsed TOC after first paragraph, floating Contact Us + scroll-to-top, real author block with logo, mid and end CTAs"

### harness-skill
"Build a harness for this Node.js API project with a Backend team (API architect + domain experts + database specialist + security reviewer)"

### skillui
"Extract the full design system from https://linear.app into a skill I can use for all future UI work on this project"

### buffett-skills
"Analyze NVIDIA as a potential long-term investment using Buffett's framework — moat, management, valuation, margin of safety"

### paper-orchestra-skill
"Write an academic paper from the experimental logs in ./results/ — I have idea.md and a template.tex ready"

### agentic-seo
"Run an AEO audit on https://galoz.co.il — check robots.txt, llms.txt, AGENTS.md, structured data, and token budget"

### autoskills
"Run npx autoskills in this Next.js + TypeScript + Prisma project and install all relevant skills"

### friday-skill
"Set up the Friday autonomous assistant — I have Claude Code Max plan, Telegram bot token, and ElevenLabs key ready"

### caveman-skill
"caveman mode ultra — I'm in a long session and need tight responses"

### ai-life-skills
"Summarize this YouTube video about React Server Components and save it to my Obsidian vault with wikilinks to every concept mentioned"

---

## New Skill Examples 2026-04-20

### shopify-admin-skills
1. "Recover all abandoned carts from the last 7 days and send a 10% discount email"
   -> Triggers: abandoned-cart-recovery skill -> dry_run preview -> confirm -> bulk execute
2. "Find all orders with fraud score > 80 and flag for manual review"
   -> Triggers: fraud-risk-detection skill -> GraphQL query -> tag high-risk orders -> report

### paper-orchestra-writing
1. "Turn my experiments in ~/diffusion-research into a NeurIPS 2026 submission"
   -> agent-research-aggregator reads ~/diffusion-research
   -> outline-agent generates structure
   -> plotting-agent + literature-review-agent run in parallel
   -> section-writing-agent drafts all sections
   -> content-refinement-agent polishes
   -> Output: complete LaTeX in ~/diffusion-research/paper/
2. "Write a 4-page ICLR paper from these 3 notebooks"
   -> Provide: idea.md + 3 experiment notebooks -> same pipeline -> shorter output

### buffett-investment
1. "Should I buy Nvidia at current valuations?"
   -> Moat analysis: fabless + CUDA ecosystem + data center dominance (wide moat)
   -> Management: Jensen Huang founder-led, high ROIC consistency
   -> Financials: 80%+ gross margin, FCF conversion
   -> Valuation: DCF + earnings multiple
   -> Output: structured verdict with buy/hold/sell + monitoring indicators
2. "What is Buffett's framework for insurance companies?"
   -> Loads reference 08 (insurance playbook)
   -> Float concept, combined ratio analysis, underwriting discipline
   -> Examples from Geico, General Re acquisition analysis

### agentic-seo-audit
1. "Audit our developer docs for AI discoverability"
   -> 
px agentic-seo --url https://docs.myproduct.com
   -> Score: 43/100 (Discovery: 10/25, Content: 18/25, Token: 8/25, Capability: 5/15, UX: 2/10)
   -> Fixes: add llms.txt (15pts), fix robots.txt to allow ClaudeBot (10pts), add AGENTS.md (5pts)
   -> Re-audit after fixes: 73/100
2. "Set up AEO files for a new product launch"
   -> 
px agentic-seo init
   -> Scaffolds: llms.txt, robots.txt, AGENTS.md, skill.md
   -> Fills templates with product context

### caveman-mode
1. User: "Why does React useState trigger a re-render?"
   Normal: "When you call the state setter function returned by useState, React schedules a re-render of the component to reflect the updated state value."
   Caveman: "Setter queues re-render. New state value triggers diff. Component re-runs."
2. Activate: "caveman ultra" -> max compression for session
   Deactivate: "stop caveman" -> back to normal

### harness-team-factory
1. "Build a harness for deep research on AI safety"
   -> Fan-out/Fan-in pattern selected
   -> Agents generated: web-researcher, academic-researcher, community-analyst, synthesis-agent
   -> Skills generated: web-search, semantic-scholar-query, reddit-sentiment, cross-validate, report-compile
   -> Output: .claude/agents/ + .claude/skills/ in current project
2. "Design an agent team for marketing campaign creation"
   -> Producer-Reviewer pattern
   -> Agents: market-researcher, copywriter, visual-concept-agent, ab-planner, campaign-reviewer
   -> Skills: market-research, ad-copywriting, visual-brief, ab-setup, campaign-review

### html-redesign-mega
1. "Redesign this WordPress landing page" + provide raw HTML
   -> Phase 1 (Audit): finds 3 broken image srcs, 2 contrast failures
   -> Phase 2 (Structure): switches float layout to CSS Grid, adds responsive breakpoints
   -> Phase 3 (Visual): applies 4px spacing scale, standardizes 12px border-radius
   -> Phase 4 (Content): adds TOC with smooth collapse, optimizes line length to 680px
   -> Phase 5 (Conversion): adds mid-article CTA + floating WhatsApp button + author trust section
   -> Phase 6 (Modals): if forms exist, adds safe-viewport modal pattern
   -> Phase 7 (N8N Sync): replaces mapril.co.il with client domain
   -> Phase 8 (Validation): re-checks all images, contrast, focus rings
   -> Output: single self-contained HTML, all inline CSS, WCAG AA
2. "Add RTL support to this Hebrew article"
   -> Sub-skill 9 (RTL): adds dir=rtl to container, flips chevrons, adjusts margins
   -> Sub-skill 8 (WordPress-safe): ensures inline-only CSS
   -> Sub-skill 17 (Accessibility): verifies contrast on rtl-specific elements

### paper-finder-ml
1. "Find papers on efficient attention for long sequences from the last 2 years"
   -> Search: Semantic Scholar API + 3 WebSearch angles
   -> Multi-angle: "linear attention", "sub-quadratic attention", "sequence modeling efficiency"
   -> Output: 15 papers in memory-bank.md + mind-graph + references.bib
   -> Top 3 recommended for deep dive
2. "Build a literature review for my paper on video generation"
   -> Multi-angle: "video diffusion", "temporal consistency", "motion synthesis"
   -> Following citation graph of top 2 papers
   -> Output: organized memory bank + BibTeX ready for LaTeX

### marp-slides-builder
1. "Create a dark-theme quarterly review deck with KPI cards and trend charts"
   -> theme: neo-brutalism (dark)
   -> layouts: cover + kpi-grid x 2 + chart-line + bullets + cta
   -> SVG sparklines for trends, metric cards for KPIs
   -> Export: PDF via MARP CLI
2. "Build a fitness dashboard presentation from my running data CSV"
   -> Parse CSV -> embed data in SVG charts
   -> layouts: dashboard + chart-area + stat-highlight
   -> Export as self-contained HTML with animations

### logo-generator-svg
1. "Generate a logo for my AI developer tool called BuildKit"
   -> Phase 1: industry=dev-tools, concept=modular/buildable, preference=minimal+cold
   -> Phase 2: 6 variants (dot matrix grid, circuit trace, hexagonal modular, diagonal lines, minimal mark, stacked)
   -> Phase 3: User selects variant 3 (hexagonal) + requests color adjustment
   -> Phase 4: Export to PNG -> Gemini generates in Frosted Horizon + Editorial Paper styles
   -> Output: HTML showcase page + 6 SVG files + 2 showcase images
2. "Create a warm, playful logo for a kids cooking app called Yummy"
   -> preference=warm colors, minimal complexity, child-friendly
   -> Variants: rainbow arch, chef hat minimal, fork-spoon combo, fruit mark, wave pattern
   -> Showcase: Morning Aura + Swiss Flat backgrounds

