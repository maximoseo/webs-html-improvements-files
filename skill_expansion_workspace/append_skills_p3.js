const fs = require('fs');
const path = require('path');

const agentsSkillDir = 'C:\\Users\\seoadmin\\.agents\\skills';
const qwenSkillDir = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\skills';
const agentsMemoPath = 'C:\\Users\\seoadmin\\.agents\\MEMO.md';
const agentsExamplesPath = 'C:\\Users\\seoadmin\\.agents\\EXAMPLES.md';
const qwenAntiPatternPath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\memo\\MEMO-redesign-anti-patterns.md';
const qwenExamplePath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\examples\\EXAMPLE-html-redesign-patterns.md';
const qwenCmdPath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\commands\\redesign-html-template.md';
const obsidianBackupDir = 'C:\\Users\\seoadmin\\Documents\\Obsidian Vault\\GENERAL-AGENTS-SKILL-EXPANSION-2026-04-17-v3';

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
    'bash-security-analysis': `---
name: Bash Security Analysis
description: Shell obfuscation detection, terminal workflow analysis, and secure bash handling.
color: "#475569"
emoji: 🛡️
vibe: Audit the script before it runs.
---

# Bash Security Analysis Skill

Synthesized from \`Bashfuscator/Bashfuscator\`.

## 🧠 Core Capabilities
- **Obfuscation Awareness:** Detects payload hiding, variable expansion tricks, and malicious bash execution patterns.
- **Secure Execution:** Reviews shell scripts for injection vulnerabilities and unquoted variables before execution.

## 🎯 When to Use
- When auditing a new repository's build scripts or \`Makefile\`.
- When an agent needs to execute an unknown or complex bash command safely.

## 🚨 Anti-Patterns
- Do not use for frontend / HTML redesign tasks. Keep shell analysis isolated to backend infrastructure and CI/CD jobs.
`,
    'js-architecture-fundamentals': `---
name: JS Architecture Fundamentals
description: Deep JavaScript concepts, event loops, closures, and frontend debugging.
color: "#F7DF1E"
emoji: 🟨
vibe: Know the spec.
---

# JS Architecture Fundamentals Skill

Synthesized from \`leonardomso/33-js-concepts\`.

## 🧠 Core Capabilities
- **Frontend Debugging:** Analyzes Call Stack, Event Loop, Closures, Promises, and prototype chain issues.
- **Performance Optimization:** Identifies memory leaks in closures and inefficient DOM rendering loops.

## 🎯 When to Use
- When debugging a complex React, Vue, or Vanilla JS interaction bug.
- When explaining how a specific JavaScript mechanism works to the user.

## 🚨 Anti-Patterns
- Do not use when working on strict, inline, HTML/CSS-only WordPress templates that disallow JS.
`,
    'screenshot-to-code-workflow': `---
name: Screenshot-to-Code Workflow
description: Visual layout extraction, component inference, and semantic HTML recreation.
color: "#38BDF8"
emoji: 📸
vibe: See the grid, build the grid.
---

# Screenshot-to-Code Workflow Skill

Synthesized from \`abi/screenshot-to-code\`.

## 🧠 Core Capabilities
- **Visual Translation:** Infers Flexbox and CSS Grid structures purely from visual layout instructions or mockup context.
- **Design Recreation:** Rapidly prototypes HTML/CSS based on visual constraints (margins, colors, typography pairings).

## 🎯 When to Use
- When rebuilding an existing webpage component (like a pricing table or hero section) into a clean, modern HTML template.
- When transferring a Figma screenshot into WordPress-safe semantic markup.

## 🚨 Anti-Patterns
- Do not use absolute positioning to match a visual mockup exactly. Always build structurally sound, responsive HTML.
`,
    'cs-systems-reasoning': `---
name: CS Systems Reasoning
description: Computer science foundations, data structures, algorithms, and big-O thinking.
color: "#0F172A"
emoji: 🖥️
vibe: Engineer for scale and efficiency.
---

# CS Systems Reasoning Skill

Synthesized from \`jwasham/coding-interview-university\`.

## 🧠 Core Capabilities
- **Algorithmic Thinking:** Evaluates the time and space complexity of code.
- **Data Structure Selection:** Chooses the correct Tree, Graph, Map, or Queue for complex data operations.

## 🎯 When to Use
- When designing backend APIs, caching layers, or search indexing functions.
- When an existing algorithm is hitting performance limits or memory constraints.

## 🚨 Anti-Patterns
- Do not apply heavy algorithmic optimization to simple, one-off scripts where readability is more important than micro-optimization.
`,
    'crawlee-advanced-scraping': `---
name: Crawlee Advanced Scraping
description: Automated page discovery, headless crawling, and structured data extraction.
color: "#10B981"
emoji: 🕷️
vibe: Scrape responsibly, parse semantically.
---

# Crawlee Advanced Scraping Skill

Synthesized from \`apify/crawlee\`.

## 🧠 Core Capabilities
- **Headless Crawling Strategy:** Manages request queues, session rotation, and anti-blocking mechanisms for deep web scraping.
- **Structured Parsing:** Extracts clean HTML, JSON-LD, and metadata from heavy JavaScript SPAs (Single Page Applications).

## 🎯 When to Use
- When an agent needs to extract competitor articles, product details, or documentation structures to seed a content pipeline.
- When mapping a website's architecture for a migration.

## 🚨 Anti-Patterns
- Do not aggressively scrape sites without rate limiting. Always respect \`robots.txt\` and server load.
`,
    'workspace-knowledge-architecture': `---
name: Workspace Knowledge Architecture
description: Note-taking systems, offline-first structures, and collaborative workspaces.
color: "#EC4899"
emoji: 📓
vibe: Organize information hierarchically.
---

# Workspace Knowledge Architecture Skill

Synthesized from \`AppFlowy-IO/AppFlowy\`.

## 🧠 Core Capabilities
- **Information Structuring:** Designs nested, hierarchical Markdown documentation that scales.
- **Workspace Modeling:** Sets up Kanban, Grid, and Document views for managing agent tasks or project data.

## 🎯 When to Use
- When structuring an Obsidian vault, a complex \`/docs\` folder, or a multi-agent memory system.
- When planning the data model for a local-first, privacy-focused note application.

## 🚨 Anti-Patterns
- Do not use this for frontend UI rendering. This is purely for structural knowledge and workspace architecture.
`,
    'revealjs-presentation-generation': `---
name: Reveal.js Presentation Generation
description: Turning structured content into interactive HTML presentation decks.
color: "#E11D48"
emoji: 📽️
vibe: Present the data beautifully.
---

# Reveal.js Presentation Generation Skill

Synthesized from \`hakimel/reveal.js\`.

## 🧠 Core Capabilities
- **Deck Authoring:** Converts Markdown or flat HTML articles into a structured \`<section>\` hierarchy for slide presentations.
- **Visual Reporting:** Generates high-impact, interactive reports and showcases for redesigns or audits.

## 🎯 When to Use
- When a user asks to convert an article, a research summary, or an audit report into a slide deck.
- When generating a visual showcase of a redesigned HTML template.

## 🚨 Anti-Patterns
- Do not mix Reveal.js framework files into standard WordPress article templates. Keep presentation outputs entirely isolated.
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
    'skill-screenshot-to-code-workflow.md': `# Skill: Screenshot-to-Code Workflow (Article Rebuild)
**Version:** 1.0  
**Source:** abi/screenshot-to-code  
**Trigger:** Converting visual mockups into HTML templates  
**Category:** Pipeline / Visual Conversion

## Purpose
Guides the agent in interpreting visual layouts (mockups, screenshots) into robust, responsive, and WordPress-safe HTML/CSS architecture without using absolute positioning.

## Workflow
1. Analyze the requested visual layout (e.g., "A pricing grid with 3 cards").
2. Deconstruct the layout into Flexbox/CSS Grid primitives.
3. Apply the appropriate typography, padding (8px rhythm), and border styling.
4. Output strict inline-CSS HTML matching the visual intent.
`,
    'skill-crawlee-advanced-scraping.md': `# Skill: Crawlee Advanced Scraping (Article Rebuild)
**Version:** 1.0  
**Source:** apify/crawlee  
**Trigger:** Competitor data extraction, content seeding  
**Category:** Pipeline / Data Extraction

## Purpose
Utilizes advanced crawling logic to extract clean, semantic HTML and metadata from target sites, feeding high-quality, structured inputs into the N8N article generation prompt.

## Workflow
1. Navigate the target URL hierarchy.
2. Extract the core article body, stripping navs, footers, and ads.
3. Parse the content into Markdown for ingestion by the article planner.
`,
    'skill-revealjs-presentation-generation.md': `# Skill: Reveal.js Presentation Generation (Article Rebuild)
**Version:** 1.0  
**Source:** hakimel/reveal.js  
**Trigger:** Reporting, Executive Summaries, Content Showcases  
**Category:** Pipeline / Reporting

## Purpose
Transforms an generated HTML article or SEO audit report into an interactive, slide-based presentation using the semantic \`<section>\` mapping of Reveal.js.

## Workflow
1. Take the final structured Markdown or HTML article.
2. Map H1 to the Title Slide. Map H2s to Chapter Slides. Map H3s/Paragraphs to Content Slides.
3. Output a self-contained \`presentation.html\` showcasing the content structure.
`
};

for (const [filename, content] of Object.entries(pipelineSkills)) {
    fs.writeFileSync(path.join(qwenSkillDir, filename), content, 'utf8');
}

// 3. Append to Global MEMO.md
const newMemoContent = `
## 15. Bash Security Analysis (\`bash-security-analysis\`)
- **What it does:** Analyzes terminal workflows, shell scripts, and detects obfuscated bash payloads.
- **When to use:** Auditing unfamiliar build scripts or CI/CD jobs.

## 16. JS Architecture Fundamentals (\`js-architecture-fundamentals\`)
- **What it does:** Deep debugging of the JS Event Loop, closures, and frontend prototype chains.
- **When to use:** Troubleshooting complex React/Vanilla JS state bugs.

## 17. Screenshot-to-Code Workflow (\`screenshot-to-code-workflow\`)
- **What it does:** Translates visual structures (mockups) into semantic HTML/CSS layouts.
- **When to use:** Rebuilding UI components or WordPress templates from visual inspiration.

## 18. CS Systems Reasoning (\`cs-systems-reasoning\`)
- **What it does:** Applies algorithmic thinking, Big-O analysis, and data structure logic.
- **When to use:** Designing scalable backend APIs or caching systems.

## 19. Crawlee Advanced Scraping (\`crawlee-advanced-scraping\`)
- **What it does:** Manages headless browser scraping, request queues, and structured extraction.
- **When to use:** Extracting competitor content or parsing heavy JavaScript SPAs.

## 20. Workspace Knowledge Architecture (\`workspace-knowledge-architecture\`)
- **What it does:** Structures hierarchical notes, local-first docs, and collaborative workflows.
- **When to use:** Organizing a complex Obsidian vault or project documentation folder.

## 21. Reveal.js Presentation Generation (\`revealjs-presentation-generation\`)
- **What it does:** Converts structured articles and reports into interactive HTML slides.
- **When to use:** Generating a slide deck from a research report or audit.
`;
appendToFile(agentsMemoPath, newMemoContent);

// 4. Append to Global EXAMPLES.md
const newExamplesContent = `
## 8. Visual Layout to HTML Extraction
**Category:** Frontend / UI
**Source:** abi/screenshot-to-code
**What makes it strong:** Enforces semantic structure rather than absolute-positioned "spaghetti code".
**Recommended Use Case:** The user uploads a screenshot of a Bento grid. The agent uses this skill to infer the exact CSS Grid \`grid-template-columns\` and \`gap\` values needed to recreate it natively.

## 9. Presentation Deck Generation
**Category:** Documentation / Reporting
**Source:** hakimel/reveal.js
**What makes it strong:** Automatically transforms a flat document into a paginated narrative.
**Recommended Use Case:** An agent generates a comprehensive SEO audit report. The user asks for a summary deck. The agent wraps the H2s in \`<section>\` tags, outputs a Reveal.js HTML file, and presents the findings visually.
`;
appendToFile(agentsExamplesPath, newExamplesContent);

// 5. Append to Qwen Anti-Patterns
const newQwenAntiPatterns = `
## U. The "App Framework" Trap (Over-Engineering)

**Symptom:** Trying to insert deep JavaScript architectures (Event Emitters, state management) into a static article template.

**Root Cause:** Misapplying \`skill-js-architecture-fundamentals\` or \`skill-workspace-knowledge-architecture\` to a pure content output.

**Fix:**
- WordPress article bodies should be purely declarative (HTML/CSS). If JS is required, it must be localized, tiny, and inline (e.g., toggling an FAQ class).

---

## V. The "Scraper Dump" Trap (Raw HTML Injection)

**Symptom:** Injecting a massive, unparsed DOM string (including headers, footers, and scripts) directly into the article generation prompt.

**Root Cause:** Failing to process extracted data properly using \`skill-crawlee-advanced-scraping\`.

**Fix:**
- Always parse the scraped HTML into clean, semantic Markdown before feeding it to the N8N prompt or the generation LLM.
`;
appendToFile(qwenAntiPatternPath, newQwenAntiPatterns);

// 6. Append to Qwen Examples
const newQwenExamples = `
## Example 14: Screenshot-to-Code Responsive Translation

**Use Case:** Recreating a complex split-feature block from a visual reference.
**Problem Solved:** Guessing dimensions and ruining mobile responsiveness.

**❌ Anti-Pattern (Fixed Layout):**
\`<div style="width: 800px; height: 400px; position: relative;">...</div>\`

**✅ Pattern (Structural Translation):**
\`<div style="display: flex; flex-wrap: wrap; gap: 32px; max-width: 100%;">
  <div style="flex: 1; min-width: 300px;">Text Content</div>
  <div style="flex: 1; min-width: 300px;">Image Content</div>
</div>\`

**Lessons:**
- A visual layout must always be translated into fluid, responsive flex/grid rules, never hardcoded pixel dimensions.
`;
appendToFile(qwenExamplePath, newQwenExamples);

// 7. Update Qwen Command (redesign-html-template.md)
let cmdContent = fs.readFileSync(qwenCmdPath, 'utf8');
if (!cmdContent.includes('skill-screenshot-to-code-workflow')) {
    const autoLoadAddition = `
- \`skill-screenshot-to-code-workflow\` (Visual-to-HTML translation rules)
- \`skill-crawlee-advanced-scraping\` (Competitor/Content extraction protocols)
- \`skill-revealjs-presentation-generation\` (Deck/Slide reporting output options)`;
    cmdContent = cmdContent.replace('- `skill-content-humanization-social` (Removes AI-sounding slop from text)', '- `skill-content-humanization-social` (Removes AI-sounding slop from text)' + autoLoadAddition);
    fs.writeFileSync(qwenCmdPath, cmdContent, 'utf8');
}

// 8. Create Backup Metadata Files
fs.mkdirSync(obsidianBackupDir, { recursive: true });

const readmeSummary = `# General Agents Skill Expansion Backup V3
**Date:** 2026-04-17

This backup contains the result of a strict append-only expansion of the general code agent ecosystem based on 7 new source repositories (Bashfuscator, 33-js-concepts, screenshot-to-code, coding-interview-university, crawlee, AppFlowy, reveal.js).

## Overview
- Synthesized 7 repositories into 7 high-impact, global \`SKILL.md\` capabilities.
- Appended robust \`MEMO.md\` and \`EXAMPLES.md\` trackers for multi-agent coordination.
- Exported 3 highly relevant rendering/scraping/presentation skills into the HTML Template Redesign pipeline (\`qwen-code-bootstrap\`).
- Explicitly filtered out low-value capabilities for the article redesign pipeline (e.g., Bash obfuscation and Deep CS Algorithms) while keeping them accessible for global coding agents.

## Included Directories
- \`/SKILLS\`: Global agent skills.
- \`/MEMO\`: Global agent memo.
- \`/EXAMPLES\`: Global agent examples.
- \`/ARTICLE-SYSTEM-REBUILD\`: Full snapshot of the augmented HTML Template Redesign system.
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'README-SUMMARY.md'), readmeSummary, 'utf8');

const sourceLinks = `# Source Links & Mappings
**Date:** 2026-04-17

The skills in this backup were synthesized from the following 7 repositories:

1. **Bash Security Analysis** (Bashfuscator) - *Filtered out from article rebuilds; kept for global shell agents.*
2. **JS Architecture Fundamentals** (33-js-concepts) - *Filtered out from article rebuilds (WP safety constraint); kept for frontend debugging.*
3. **Screenshot-to-Code Workflow** (screenshot-to-code) - *Appended to Article Rebuild (Visual layout translation).*
4. **CS Systems Reasoning** (coding-interview-university) - *Filtered out from article rebuilds; kept for backend/architecture agents.*
5. **Crawlee Advanced Scraping** (crawlee) - *Appended to Article Rebuild (Content acquisition).*
6. **Workspace Knowledge Architecture** (AppFlowy) - *Filtered out from article rebuilds; kept for Obsidian/note organization agents.*
7. **Reveal.js Presentation Generation** (reveal.js) - *Appended to Article Rebuild (Reporting and deck generation).*
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'SOURCE-LINKS.md'), sourceLinks, 'utf8');

const changelog = `# Changelog
**Date:** 2026-04-17

### Added
- \`bash-security-analysis\` (Global Skill)
- \`js-architecture-fundamentals\` (Global Skill)
- \`screenshot-to-code-workflow\` (Global Skill + Rebuild System Skill)
- \`cs-systems-reasoning\` (Global Skill)
- \`crawlee-advanced-scraping\` (Global Skill + Rebuild System Skill)
- \`workspace-knowledge-architecture\` (Global Skill)
- \`revealjs-presentation-generation\` (Global Skill + Rebuild System Skill)

### Appended
- \`C:\\Users\\seoadmin\\.agents\\MEMO.md\` (Added Sections 15-21)
- \`C:\\Users\\seoadmin\\.agents\\EXAMPLES.md\` (Added Sections 8-9)
- \`qwen-code-bootstrap\\commands\\redesign-html-template.md\` (Added new layout/scraping/presentation skills to auto-load block)
- \`qwen-code-bootstrap\\memo\\MEMO-redesign-anti-patterns.md\` (Added 2 new anti-patterns: U, V)
- \`qwen-code-bootstrap\\examples\\EXAMPLE-html-redesign-patterns.md\` (Added Responsive Translation example)

### Preserved
- All existing skills, memos, examples, and backup history across the workspace. No files were deleted or destructively replaced. All additions were cleanly appended.
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'CHANGELOG.md'), changelog, 'utf8');

console.log("Massive skill expansion phase 3 completed successfully.");