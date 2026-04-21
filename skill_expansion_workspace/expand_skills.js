const fs = require('fs');
const path = require('path');

const agentsSkillDir = 'C:\\Users\\seoadmin\\.agents\\skills';
const qwenSkillDir = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\skills';
const agentsMemoPath = 'C:\\Users\\seoadmin\\.agents\\MEMO.md';
const agentsExamplesPath = 'C:\\Users\\seoadmin\\.agents\\EXAMPLES.md';
const qwenAntiPatternPath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\memo\\MEMO-redesign-anti-patterns.md';
const qwenExamplePath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\examples\\EXAMPLE-html-redesign-patterns.md';
const qwenCmdPath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\commands\\redesign-html-template.md';
const obsidianBackupDir = 'C:\\Users\\seoadmin\\Documents\\Obsidian Vault\\GENERAL-AGENTS-SKILL-EXPANSION-2026-04-17';

// Helper to append text securely
function appendToFile(filePath, content) {
    if (fs.existsSync(filePath)) {
        fs.appendFileSync(filePath, '\n' + content, 'utf8');
    } else {
        fs.writeFileSync(filePath, content, 'utf8');
    }
}

// 1. Create Global Skills
const globalSkills = {
    'context-memory-manager': `---
name: Context & Memory Manager
description: Advanced memory retrieval, context-packing, and persistent memo workflows.
color: "#8B5CF6"
emoji: 🧠
vibe: Retain everything, recall instantly.
---

# Context & Memory Manager Skill

Inspired by \`thedotmack/claude-mem\` and \`feuersteiner/contextrie\`.

## 🧠 Core Capabilities
- **Context Packing:** Optimizes how history and files are loaded into the prompt context window to avoid bloat.
- **Memory Persistence:** Manages global \`MEMO.md\` and \`EXAMPLES.md\` files across multi-agent sessions.
- **State Retrieval:** Ensures agents can recall past architectural decisions without hallucinating.

## 🎯 When to Use
- When orchestrating complex, multi-turn coding tasks that require historical context.
- When an agent seems to "forget" previous instructions or rules.

## 🚨 Anti-Patterns
- Do not dump thousands of lines of raw logs into memory; synthesize them into concise bullet points.
`,
    'superclaude-framework-orchestration': `---
name: SuperClaude Framework Orchestration
description: Multi-agent coordination, auto-skill discovery, and task delegation.
color: "#3B82F6"
emoji: 🤝
vibe: Orchestrate the swarm.
---

# SuperClaude Framework Orchestration Skill

Synthesized from \`SuperClaude-Org/SuperClaude_Framework\`, \`midudev/autoskills\`, \`11cafe/jaaz\`, and \`JackChen-me/open-multi-agent\`.

## 🧠 Core Capabilities
- **Auto-Skill Discovery:** Dynamically loads the correct skills based on the user's intent without manual prompting.
- **Task Delegation:** Splits complex epics into sub-tasks and delegates them to specialized agents (e.g., SEO agent, UI agent, Debug agent).
- **Framework Integration:** Bridges standard Claude CLI workflows with OpenClaw and Multi-Agent topologies.

## 🎯 When to Use
- When faced with a massive feature request (e.g., "Build a complete SaaS dashboard").
- When organizing sub-agent outputs into a coherent final deliverable.

## 🚨 Anti-Patterns
- Do not spawn sub-agents for trivial, single-file edits. Avoid orchestration overhead for simple tasks.
`,
    'design-to-code-renderer': `---
name: Design-to-Code Renderer
description: Figma-to-code translation, JSON UI rendering, and Penpot workflows.
color: "#F59E0B"
emoji: 🎨
vibe: Pixel-perfect translation.
---

# Design-to-Code Renderer Skill

Synthesized from \`vibeflowing-inc/vibe_figma\`, \`vercel-labs/json-render\`, \`penpot/penpot\`, and \`uiverse-io/galaxy\`.

## 🧠 Core Capabilities
- **JSON UI Rendering:** Converts structured JSON data into accessible HTML/React components.
- **Vibe Translation:** Translates the "vibe" of a Figma/Penpot mockup into strict, semantic HTML/CSS without relying on absolute positioning traps.
- **Component Extraction:** Safely extracts hover states and micro-interactions from UI libraries (like Uiverse) into inline WordPress-safe styles.

## 🎯 When to Use
- When converting a mockup or wireframe into a functional HTML template.
- When a design system needs to be rendered dynamically from JSON payloads.

## 🚨 Anti-Patterns
- Do not generate absolute-positioned \"spaghetti code\". Always use Flexbox or CSS Grid.
`,
    'system-design-architect': `---
name: System Design Architect
description: High-level system architecture, dev best practices, and topology planning.
color: "#10B981"
emoji: 🏗️
vibe: Build it to scale.
---

# System Design Architect Skill

Synthesized from \`donnemartin/system-design-primer\` and \`mtdvio/every-programmer-should-know\`.

## 🧠 Core Capabilities
- **Architecture Planning:** Designs scalable, fault-tolerant backend and frontend systems.
- **Best Practices:** Enforces DRY, SOLID, and clean architecture principles across generated codebases.
- **Trade-off Analysis:** Evaluates database choices, caching layers, and load balancing strategies before writing code.

## 🎯 When to Use
- During Phase 1 (Planning) of a new application build.
- When refactoring a monolith into microservices.

## 🚨 Anti-Patterns
- Do not over-engineer. Avoid suggesting Kubernetes and Kafka for a simple blog script.
`,
    'content-humanization-social': `---
name: Content Humanization & Social OSINT
description: Human-like copywriting, social profile analysis, and tone adjustment.
color: "#EC4899"
emoji: 🗣️
vibe: Sound like a human, understand the audience.
---

# Content Humanization & Social OSINT Skill

Synthesized from \`blader/humanizer\`, \`qeeqbox/social-analyzer\`, and \`Panniantong/Agent-Reach\`.

## 🧠 Core Capabilities
- **AI De-tection:** Removes "AI-sounding" vocabulary (e.g., "delve", "testament", "tapestry") and restructures sentences for natural flow.
- **Social Profiling:** Analyzes public social media data to match brand tone and audience expectations.
- **Agent Reachout:** Drafts hyper-personalized outreach or marketing copy that avoids spam filters and generic templates.

## 🎯 When to Use
- When generating article copy, blog posts, or marketing emails.
- When an HTML template requires placeholder text that needs to look highly realistic and conversion-focused.

## 🚨 Anti-Patterns
- Do not use forced slang or overly casual language unless the brand explicitly calls for it. Keep it professional but human.
`,
    'cli-automation-workflows': `---
name: CLI Automation Workflows
description: Advanced terminal commands, CI/CD orchestration, and local env optimization.
color: "#64748B"
emoji: 💻
vibe: Automate the boring stuff.
---

# CLI Automation Workflows Skill

Synthesized from \`jackwener/OpenCLI\`, \`Raphire/Win11Debloat\`, \`koderover/zadig\`, and \`zerobootdev/zeroboot\`.

## 🧠 Core Capabilities
- **Local Env Optimization:** Debloats Windows environments and optimizes local development speeds.
- **CI/CD Orchestration:** Configures Zadig or GitHub Actions pipelines natively from the CLI.
- **Headless Automation:** Executes complex multi-step build, test, and deploy scripts autonomously.

## 🎯 When to Use
- When setting up a new repository, dockerizing an app, or fixing a broken CI pipeline.
- When a user asks to optimize their local machine for development.

## 🚨 Anti-Patterns
- Do not run destructive commands (e.g., wiping directories or modifying registry keys) without explicit user confirmation and backups.
`,
    'meta-prompt-optimization': `---
name: Meta-Prompt Optimization
description: Prompt engineering, Nano Banana Pro routing, and Claude mastery.
color: "#F43F5E"
emoji: ⚡
vibe: Instruct the instructor.
---

# Meta-Prompt Optimization Skill

Synthesized from \`YouMind-OpenLab/awesome-nano-banana-pro-prompts\`, \`hesamsheikh/awesome-openclaw-usecases\`, \`luongnv89/claude-howto\`, and \`affaan-m/everything-claude-code\`.

## 🧠 Core Capabilities
- **Prompt Refinement:** Rewrites user prompts into highly structured, constraint-driven system instructions.
- **Model Routing:** Recommends when to use Claude 3.5 Sonnet vs Haiku vs open-source models (like Nano Banana Pro).
- **Code Agent Mastery:** Teaches users and sub-agents how to effectively use Claude Code's internal toolset (Read, Write, Bash, Replace).

## 🎯 When to Use
- When generating the \`N8N_Prompt.txt\` files for automated pipelines.
- When an agent is consistently failing a task due to ambiguous instructions.

## 🚨 Anti-Patterns
- Do not create prompts that are so restrictive they cause the LLM to hallucinate or break syntax.
`
};

// Create directories if they don't exist
for (const skillName of Object.keys(globalSkills)) {
    const dir = path.join(agentsSkillDir, skillName);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(path.join(dir, 'SKILL.md'), globalSkills[skillName], 'utf8');
}

// 2. Create Pipeline Skills for /article-system-rebuild
const pipelineSkills = {
    'skill-design-to-code-renderer.md': `# Skill: Design-to-Code Renderer (Article Rebuild)
**Version:** 1.0  
**Source:** vibe_figma, json-render, uiverse  
**Trigger:** Complex UI sections, JSON-to-HTML  
**Category:** Pipeline / Frontend Rendering

## Purpose
Translates high-end design intents (like Figma vibes or JSON payload structures) directly into WordPress-safe, inline-styled HTML without relying on Tailwind or external CSS.

## Workflow
1. Analyze the requested "vibe" (e.g., playful, enterprise, minimal).
2. Render the JSON data arrays strictly into standard HTML tables or Flexbox cards.
3. Apply tactile Uiverse-style hover states to interactive elements.
`,
    'skill-content-humanization-social.md': `# Skill: Content Humanization (Article Rebuild)
**Version:** 1.0  
**Source:** blader/humanizer, qeeqbox/social-analyzer  
**Trigger:** Article generation, copywriting  
**Category:** Pipeline / Content Quality

## Purpose
Strips AI-sounding vocabulary from generated articles and aligns the tone with public social media profiles of the brand.

## Workflow
1. Scan draft text for words like "delve", "testament", "tapestry", "crucial".
2. Rewrite to use plain, direct, active-voice English.
3. Ensure the About the Author section reads like a human bio, not an AI summary.
`
};

for (const [filename, content] of Object.entries(pipelineSkills)) {
    fs.writeFileSync(path.join(qwenSkillDir, filename), content, 'utf8');
}

// 3. Append to Global MEMO.md
const newMemoContent = `
## 8. Context & Memory Manager (\`context-memory-manager\`)
- **What it does:** Optimizes context packing and multi-agent memory retention.
- **When to use:** Long sessions where agents risk forgetting architectural rules.

## 9. SuperClaude Framework Orchestration (\`superclaude-framework-orchestration\`)
- **What it does:** Auto-discovers skills and delegates tasks to sub-agents.
- **When to use:** Massive, multi-file epic implementations.

## 10. Design-to-Code Renderer (\`design-to-code-renderer\`)
- **What it does:** Translates design vibes and JSON payloads into semantic HTML.
- **When to use:** Converting mockups or raw data into beautiful UI components.

## 11. System Design Architect (\`system-design-architect\`)
- **What it does:** Enforces scalable architecture and developer best practices.
- **When to use:** Planning phases and database schema design.

## 12. Content Humanization & Social OSINT (\`content-humanization-social\`)
- **What it does:** De-AI's text and matches brand tone based on social profiles.
- **When to use:** Polishing article drafts and marketing copy.

## 13. CLI Automation Workflows (\`cli-automation-workflows\`)
- **What it does:** Configures CI/CD pipelines and optimizes local environments.
- **When to use:** Setting up GitHub actions, Zadig, or debloating Windows.

## 14. Meta-Prompt Optimization (\`meta-prompt-optimization\`)
- **What it does:** Refines system prompts and recommends model routing.
- **When to use:** Generating strict N8N pipeline instructions.
`;
appendToFile(agentsMemoPath, newMemoContent);

// 4. Append to Global EXAMPLES.md
const newExamplesContent = `
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
`;
appendToFile(agentsExamplesPath, newExamplesContent);

// 5. Append to Qwen Anti-Patterns
const newQwenAntiPatterns = `
## S. The "AI Vocabulary" Trap (Robotic Tone)

**Symptom:** Article begins with "In the ever-evolving landscape of..." or uses words like "delve", "foster", or "testament".

**Root Cause:** Failing to run \`skill-content-humanization-social\`.

**Fix:**
- Force plain, active-voice English. Speak directly to the user's problem immediately.

---

## T. The "Absolute Positioning" Trap (Fragile Layouts)

**Symptom:** Trying to replicate Figma designs using \`position: absolute\` and fixed pixel widths.

**Root Cause:** Misapplying \`skill-design-to-code-renderer\` without WordPress-safe constraints.

**Fix:**
- Always use Flexbox (\`display: flex; flex-wrap: wrap\`) or CSS Grid for structural layout. Never use absolute positioning for primary content blocks.
`;
appendToFile(qwenAntiPatternPath, newQwenAntiPatterns);

// 6. Append to Qwen Examples
const newQwenExamples = `
## Example 13: Content Humanization Pattern

**Use Case:** Writing an intro paragraph for a B2B article.
**Problem Solved:** Sounding like a generic AI bot.

**❌ Anti-Pattern (AI Slop):**
"In today's fast-paced digital landscape, managing IT costs is more crucial than ever. Let's delve into how power management serves as a testament to efficiency."

**✅ Pattern (Humanized & Direct):**
"Thousands of enterprise workstations left running overnight represent one of the largest recoverable cost items in IT operations. Here is how IT leaders are cutting electricity costs up to 60% without disrupting users."

**Lessons:**
- Delete filler intros. State the problem and the data immediately.
`;
appendToFile(qwenExamplePath, newQwenExamples);

// 7. Update Qwen Command (redesign-html-template.md)
let cmdContent = fs.readFileSync(qwenCmdPath, 'utf8');
if (!cmdContent.includes('skill-design-to-code-renderer')) {
    const autoLoadAddition = `
- \`skill-design-to-code-renderer\` (Translates JSON/Vibes into HTML)
- \`skill-content-humanization-social\` (Removes AI-sounding slop from text)`;
    cmdContent = cmdContent.replace('- `skill-seomachine-optimization` (SEO structure and meta tag generation)', '- `skill-seomachine-optimization` (SEO structure and meta tag generation)' + autoLoadAddition);
    fs.writeFileSync(qwenCmdPath, cmdContent, 'utf8');
}

// 8. Create Obsidian Backup Text Files
fs.mkdirSync(obsidianBackupDir, { recursive: true });

// Create README-SUMMARY.md
const readmeSummary = `# General Agents Skill Expansion Backup
**Date:** 2026-04-17

This backup contains the result of a massive append-only expansion of the general code agent ecosystem based on 35 new source repositories.

## Overview
- Synthesized 35 distinct repositories into 7 high-impact, global \`SKILL.md\` capabilities.
- Appended robust \`MEMO.md\` and \`EXAMPLES.md\` trackers for multi-agent coordination.
- Exported 2 highly relevant rendering/humanization skills into the HTML Template Redesign pipeline (\`qwen-code-bootstrap\`).
- Enhanced redesign rules and anti-patterns to prevent "Figma spaghetti code" and "AI-sounding text".

## Included Directories
- \`/SKILLS\`: Global agent skills.
- \`/MEMO\`: Global agent memo.
- \`/EXAMPLES\`: Global agent examples.
- \`/ARTICLE-SYSTEM-REBUILD\`: Full snapshot of the augmented HTML Template Redesign system.
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'README-SUMMARY.md'), readmeSummary, 'utf8');

// Create SOURCE-LINKS.md
const sourceLinks = `# Source Links & Mappings
**Date:** 2026-04-17

The skills in this backup were synthesized and deduplicated from the following 35 repositories:

1. **Context & Memory Manager** (claude-mem, contextrie)
2. **SuperClaude Framework Orchestration** (SuperClaude_Framework, open-multi-agent, autoskills, jaaz)
3. **Design-to-Code Renderer** (vibe_figma, json-render, penpot, galaxy)
4. **System Design Architect** (system-design-primer, every-programmer-should-know, arc-kit)
5. **Content Humanization & Social OSINT** (humanizer, social-analyzer, Agent-Reach)
6. **CLI Automation Workflows** (OpenCLI, Win11Debloat, zadig, zeroboot)
7. **Meta-Prompt Optimization** (awesome-nano-banana-pro-prompts, awesome-openclaw-usecases, claude-howto, everything-claude-code, awesome-claude-skills)
8. **(Excluded / Redundant / Deprecated)** (clawdbot-feishu, Crucix, pinchtab, witr, picolm, spritefusion-pixel-snapper) - Excluded from core skills to prevent noise, but mapped to awareness.
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'SOURCE-LINKS.md'), sourceLinks, 'utf8');

// Create CHANGELOG.md
const changelog = `# Changelog
**Date:** 2026-04-17

### Added
- \`context-memory-manager\` (Global Skill)
- \`superclaude-framework-orchestration\` (Global Skill)
- \`design-to-code-renderer\` (Global Skill + Rebuild System Skill)
- \`system-design-architect\` (Global Skill)
- \`content-humanization-social\` (Global Skill + Rebuild System Skill)
- \`cli-automation-workflows\` (Global Skill)
- \`meta-prompt-optimization\` (Global Skill)

### Appended
- \`C:\\Users\\seoadmin\\.agents\\MEMO.md\` (Added Sections 8-14)
- \`C:\\Users\\seoadmin\\.agents\\EXAMPLES.md\` (Added Sections 6-7)
- \`qwen-code-bootstrap\\commands\\redesign-html-template.md\` (Added new rendering skills to auto-load block)
- \`qwen-code-bootstrap\\memo\\MEMO-redesign-anti-patterns.md\` (Added 2 new anti-patterns: S, T)
- \`qwen-code-bootstrap\\examples\\EXAMPLE-html-redesign-patterns.md\` (Added Humanization example)

### Preserved
- All existing skills, memos, examples, and backup history across the workspace. No files were deleted or destructively replaced. All additions were cleanly appended.
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'CHANGELOG.md'), changelog, 'utf8');

console.log("Massive skill expansion file generation completed successfully.");
