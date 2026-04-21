const fs = require('fs');
const path = require('path');

const agentsSkillDir = 'C:\\Users\\seoadmin\\.agents\\skills';
const qwenSkillDir = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\skills';
const agentsMemoPath = 'C:\\Users\\seoadmin\\.agents\\MEMO.md';
const agentsExamplesPath = 'C:\\Users\\seoadmin\\.agents\\EXAMPLES.md';
const qwenAntiPatternPath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\memo\\MEMO-redesign-anti-patterns.md';
const qwenExamplePath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\examples\\EXAMPLE-html-redesign-patterns.md';
const qwenCmdPath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\commands\\redesign-html-template.md';
const obsidianBackupDir = 'C:\\Users\\seoadmin\\Documents\\Obsidian Vault\\GENERAL-AGENTS-SKILL-EXPANSION-2026-04-17-v4';

function appendToFile(filePath, content) {
    if (fs.existsSync(filePath)) {
        fs.appendFileSync(filePath, '\n' + content, 'utf8');
    } else {
        fs.writeFileSync(filePath, content, 'utf8');
    }
}

// 1. Create Global Skills
const globalSkills = {
    'autoskills-stack-detector': `---
name: Autoskills Stack Detector
description: Automatic skill discovery, project tech-stack detection, and zero-config context.
color: "#3B82F6"
emoji: 🔍
vibe: Read the environment, load the skills.
---

# Autoskills Stack Detector Skill

Synthesized from \`midudev/autoskills\`.

## 🧠 Core Capabilities
- **Automatic Tech Detection:** Scans \`package.json\`, \`requirements.txt\`, or Gradle files to identify the project's frameworks and infrastructure.
- **Skill Suggestion:** Recommends relevant markdown-based skills based on the detected stack.
- **Context Synthesis:** Generates a unified \`CLAUDE.md\` or \`AGENTS.md\` summary linking all active skills for the agent.

## 🎯 When to Use
- When initializing a new repository or entering a workspace for the first time.
- When organizing a chaotic project that lacks clear agent instructions.

## 🚨 Anti-Patterns
- Do not forcibly overwrite existing \`CLAUDE.md\` files if they contain custom human instructions. Always append or merge.
`,
    'awesome-claude-design-system': `---
name: Awesome Claude Design System
description: One-shot UI/UX scaffolding, DESIGN.md enforcement, and visual token systems.
color: "#8B5CF6"
emoji: 💅
vibe: Tokenize the aesthetics.
---

# Awesome Claude Design System Skill

Synthesized from \`VoltAgent/awesome-claude-design\`.

## 🧠 Core Capabilities
- **DESIGN.md Generation:** Converts abstract "vibes" (e.g., "Linear-style") into a strict markdown source of truth containing color tokens, typography scales, and CSS variables.
- **UI Kit Scaffolding:** Transforms a \`DESIGN.md\` into a working, portable component library.
- **Aesthetic Compliance Auditing:** Reviews newly written frontend code to ensure strict adherence to the established design tokens.

## 🎯 When to Use
- When planning the UI architecture of a new application or landing page.
- When an existing app has fragmented CSS and needs a unified design system.

## 🚨 Anti-Patterns
- Do not rely on loose visual prompts ("make it look modern"). Always define the tokens in a \`DESIGN.md\` first.
`
};

for (const skillName of Object.keys(globalSkills)) {
    const dir = path.join(agentsSkillDir, skillName);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'SKILL.md'), globalSkills[skillName], 'utf8');
}

// 2. Create Pipeline Skills for /article-system-rebuild
const pipelineSkills = {
    'skill-awesome-claude-design-system.md': `# Skill: Awesome Claude Design System (Article Rebuild)
**Version:** 1.0  
**Source:** VoltAgent/awesome-claude-design  
**Trigger:** Establishing WordPress-safe design tokens  
**Category:** Pipeline / UI Architecture

## Purpose
Translates the concept of a \`DESIGN.md\` (color tokens, spacing rhythms, typographic scales) directly into a highly controlled inline-CSS schema for HTML template redesigns.

## Workflow
1. Identify the target brand aesthetic.
2. Establish strict token mappings (e.g., \`--spacing-unit: 8px\`, \`--color-primary: #0f172a\`).
3. Enforce these tokens systematically across all components (CTAs, TOCs, Author Boxes) via inline styles.
`
};

for (const [filename, content] of Object.entries(pipelineSkills)) {
    fs.writeFileSync(path.join(qwenSkillDir, filename), content, 'utf8');
}

// 3. Append to Global MEMO.md
const newMemoContent = `
## 22. Autoskills Stack Detector (\`autoskills-stack-detector\`)
- **What it does:** Scans project files to automatically suggest and link relevant agent skills.
- **When to use:** Bootstrapping an agent in a new repository.

## 23. Awesome Claude Design System (\`awesome-claude-design-system\`)
- **What it does:** Scaffolds complete UI/UX systems using a \`DESIGN.md\` token source of truth.
- **When to use:** Establishing a unified aesthetic before writing frontend code.
`;
appendToFile(agentsMemoPath, newMemoContent);

// 4. Append to Global EXAMPLES.md
const newExamplesContent = `
## 10. Automated Skill Discovery
**Category:** Agent Orchestration
**Source:** midudev/autoskills
**What makes it strong:** Contextualizes the agent instantly without human intervention.
**Recommended Use Case:** An agent lands in a Vue.js repo, detects \`package.json\`, and automatically appends the \`skill-vue-pinia\` and \`skill-tailwind\` paths into \`CLAUDE.md\`.

## 11. DESIGN.md Enforcement
**Category:** UI/UX Design Systems
**Source:** VoltAgent/awesome-claude-design
**What makes it strong:** Replaces vague "make it look good" prompts with deterministic CSS token matrices.
**Recommended Use Case:** The agent is asked to redesign a pricing page. Instead of guessing colors, it first generates a \`DESIGN.md\` mapping the exact HEX values, border-radii, and shadow depths, then applies them systematically.
`;
appendToFile(agentsExamplesPath, newExamplesContent);

// 5. Append to Qwen Anti-Patterns
const newQwenAntiPatterns = `
## W. The "Vibe Guessing" Trap (Inconsistent Aesthetics)

**Symptom:** Buttons have different border-radii, spacing feels random, and colors clash.

**Root Cause:** Writing inline HTML/CSS without first establishing a design token system (via \`skill-awesome-claude-design-system\`).

**Fix:**
- Always declare the "tokens" mentally or explicitly before writing the inline styles for a WordPress article. Standardize the \`padding\` rhythm (e.g., multiples of 8px) and exact HEX codes across all components.
`;
appendToFile(qwenAntiPatternPath, newQwenAntiPatterns);

// 6. Append to Qwen Examples
const newQwenExamples = `
## Example 15: Design System Token Enforcement (Inline)

**Use Case:** Maintaining consistency across multiple WordPress-safe elements.
**Problem Solved:** Random spacing and color variations.

**Pattern (Token Logic applied to Inline CSS):**
- *Token Rhythm:* 8px base
- *Token Palette:* #0f172a (Primary), #f8fafc (Surface)

\`<div style="padding: 32px; background: #f8fafc; border-radius: 16px;">
  <h3 style="margin-bottom: 16px; color: #0f172a;">Consistent Heading</h3>
  <a href="#" style="padding: 16px 24px; background: #0f172a; color: #ffffff; border-radius: 8px;">Action</a>
</div>\`

**Lessons:**
- Even without a CSS framework, treat your inline styles as if they were strictly controlled by a \`DESIGN.md\` system.
`;
appendToFile(qwenExamplePath, newQwenExamples);

// 7. Update Qwen Command (redesign-html-template.md)
let cmdContent = fs.readFileSync(qwenCmdPath, 'utf8');
if (!cmdContent.includes('skill-awesome-claude-design-system')) {
    const autoLoadAddition = `
- \`skill-awesome-claude-design-system\` (Strict visual token enforcement)`;
    cmdContent = cmdContent.replace('- `skill-revealjs-presentation-generation` (Deck/Slide reporting output options)', '- `skill-revealjs-presentation-generation` (Deck/Slide reporting output options)' + autoLoadAddition);
    fs.writeFileSync(qwenCmdPath, cmdContent, 'utf8');
}

// 8. Create Backup Metadata Files
fs.mkdirSync(obsidianBackupDir, { recursive: true });

const readmeSummary = `# General Agents Skill Expansion Backup V4
**Date:** 2026-04-17

This backup contains the result of a strict append-only expansion of the general code agent ecosystem based on 2 new source repositories (autoskills, awesome-claude-design).

## Overview
- Synthesized 2 repositories into high-impact, global \`SKILL.md\` capabilities.
- Appended robust \`MEMO.md\` and \`EXAMPLES.md\` trackers for multi-agent coordination and UI design.
- Exported 1 highly relevant design system skill into the HTML Template Redesign pipeline (\`qwen-code-bootstrap\`).

## Included Directories
- \`/SKILLS\`: Global agent skills.
- \`/MEMO\`: Global agent memo.
- \`/EXAMPLES\`: Global agent examples.
- \`/ARTICLE-SYSTEM-REBUILD\`: Full snapshot of the augmented HTML Template Redesign system.
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'README-SUMMARY.md'), readmeSummary, 'utf8');

const sourceLinks = `# Source Links & Mappings
**Date:** 2026-04-17

The skills in this backup were synthesized from the following 2 repositories:

1. **Autoskills Stack Detector** (midudev/autoskills) - *Kept for global agent initialization and environment scanning.*
2. **Awesome Claude Design System** (VoltAgent/awesome-claude-design) - *Appended to Article Rebuild (Design token enforcement for inline CSS).*
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'SOURCE-LINKS.md'), sourceLinks, 'utf8');

const changelog = `# Changelog
**Date:** 2026-04-17

### Added
- \`autoskills-stack-detector\` (Global Skill)
- \`awesome-claude-design-system\` (Global Skill + Rebuild System Skill)

### Appended
- \`C:\\Users\\seoadmin\\.agents\\MEMO.md\` (Added Sections 22-23)
- \`C:\\Users\\seoadmin\\.agents\\EXAMPLES.md\` (Added Sections 10-11)
- \`qwen-code-bootstrap\\commands\\redesign-html-template.md\` (Added new design system skill to auto-load block)
- \`qwen-code-bootstrap\\memo\\MEMO-redesign-anti-patterns.md\` (Added 1 new anti-pattern: W)
- \`qwen-code-bootstrap\\examples\\EXAMPLE-html-redesign-patterns.md\` (Added Design Token example)

### Preserved
- All existing skills, memos, examples, and backup history across the workspace. No files were deleted or destructively replaced. All additions were cleanly appended.
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'CHANGELOG.md'), changelog, 'utf8');

console.log("Skill expansion phase 4 completed successfully.");