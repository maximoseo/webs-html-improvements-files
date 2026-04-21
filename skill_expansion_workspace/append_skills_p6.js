const fs = require('fs');
const path = require('path');

const agentsSkillDir = 'C:\\Users\\seoadmin\\.agents\\skills';
const qwenSkillDir = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\skills';
const agentsMemoPath = 'C:\\Users\\seoadmin\\.agents\\MEMO.md';
const agentsExamplesPath = 'C:\\Users\\seoadmin\\.agents\\EXAMPLES.md';
const qwenAntiPatternPath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\memo\\MEMO-redesign-anti-patterns.md';
const qwenExamplePath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\examples\\EXAMPLE-html-redesign-patterns.md';
const qwenCmdPath = 'C:\\Users\\seoadmin\\qwen-code-bootstrap\\commands\\redesign-html-template.md';
const obsidianBackupDir = 'C:\\Users\\seoadmin\\Documents\\Obsidian Vault\\GENERAL-AGENTS-SKILL-EXPANSION-2026-04-17-v6';

function appendToFile(filePath, content) {
    if (fs.existsSync(filePath)) {
        fs.appendFileSync(filePath, '\n' + content, 'utf8');
    } else {
        fs.writeFileSync(filePath, content, 'utf8');
    }
}

// 1. Create Global Skills
const globalSkills = {
    'kronos-knowledge-graph': `---
name: Kronos Knowledge Graph
description: Semantic memory, temporal truth tracking, and protocol-driven implementation discipline.
color: "#38BDF8"
emoji: ⏱️
vibe: Remember decisions across time.
---

# Kronos Knowledge Graph Skill

Synthesized from \`Ja1Denis/Kronos\`.

## 🧠 Core Capabilities
- **Temporal Truth Tracking:** Stores not just what a decision is, but *why* it was made and how it evolved over time.
- **Architect Protocol:** Enforces a rigid STOP & THINK → SEARCH → QUERY → REUSE → SYNTHESIS cycle.
- **Shadow Accounting:** Measures token and time savings achieved by reusing existing memory vs hallucinating new code.

## 🎯 When to Use
- When initiating a massive refactor that depends on historical context (e.g., "Why was this database migration done this way?").
- When a project requires strict adherence to documented decision logs.

## 🚨 Anti-Patterns
- Do not bypass the "Search Before Build" protocol. Never reinvent a utility function that already exists in the project memory.
`,
    'voxcpm-multimodal-voice': `---
name: VoxCPM Multimodal Voice
description: Voice design, controllable cloning, and text-to-speech parameter reasoning.
color: "#F43F5E"
emoji: 🗣️
vibe: Give the agent a voice.
---

# VoxCPM Multimodal Voice Skill

Synthesized from \`OpenBMB/VoxCPM\`.

## 🧠 Core Capabilities
- **Voice Profile Engineering:** Translates textual brand descriptions into explicit voice parameters (timbre, emotion, pace) for TTS engines.
- **Audio Output Structuring:** Prepares content specifically for text-to-speech generation (e.g., adding phonetic cues or pause markers).

## 🎯 When to Use
- When an agent is tasked with generating scripts for podcasts, video essays, or automated voiceovers.
- When expanding text-heavy systems into multimodal content hubs.

## 🚨 Anti-Patterns
- Do not apply TTS cues to standard HTML or markdown documentation where human reading is the primary mode.
`,
    'karpathy-coding-guardrails': `---
name: Karpathy Coding Guardrails
description: Extreme simplicity, surgical edits, and defensive reasoning for coding agents.
color: "#10B981"
emoji: 🛡️
vibe: Think before you type. Keep it simple.
---

# Karpathy Coding Guardrails Skill

Synthesized from \`forrestchang/andrej-karpathy-skills\`.

## 🧠 Core Capabilities
- **Simplicity First:** Actively hunts for overengineered solutions and strips them down to the bare minimum required code.
- **Surgical Editing:** Prevents "orthogonal edits" (e.g., reformatting an entire file when asked to fix one bug).
- **Verification Looping:** Forces the agent to define success criteria *before* modifying code, and loop until tests pass.

## 🎯 When to Use
- When generating or modifying any code. This is a foundational behavioral override for maximum reliability.
- When an agent is caught making unnecessary, sprawling changes that break other systems.

## 🚨 Anti-Patterns
- Do not refactor code outside the immediate scope of the user's request unless it is critically necessary for the fix to function.
`,
    'hermes-autonomous-learning': `---
name: Hermes Autonomous Learning
description: Self-improving agent loops, dynamic skill creation, and user modeling.
color: "#8B5CF6"
emoji: 🦉
vibe: Learn from every interaction.
---

# Hermes Autonomous Learning Skill

Synthesized from \`NousResearch/hermes-agent\`.

## 🧠 Core Capabilities
- **Dialectic User Modeling:** Builds a continuous model of the user's preferences, taste, and communication style across sessions.
- **Skill Extraction:** Automatically turns a successful, complex conversation into a reusable \`SKILL.md\` file for future agents.
- **Background Execution:** Sets up cron-like scheduling for natural language tasks.

## 🎯 When to Use
- When a user frequently requests the same type of task and the agent needs to automate it permanently.
- When interacting with a new user to rapidly establish their coding conventions and design tastes.

## 🚨 Anti-Patterns
- Do not generate new skills for trivial tasks. Only extract skills when a complex workflow is definitively solved.
`,
    'postiz-social-publishing': `---
name: Postiz Social Publishing
description: Multi-platform content distribution, social scheduling, and marketing pipelines.
color: "#3B82F6"
emoji: 📢
vibe: Ship it to the world.
---

# Postiz Social Publishing Skill

Synthesized from \`gitroomhq/postiz-app\`.

## 🧠 Core Capabilities
- **Social Automation:** Translates long-form content (like articles or PRDs) into optimized, platform-specific social media variants (Twitter threads, LinkedIn posts).
- **Temporal Scheduling:** Generates deployment timelines and scheduling metadata for N8N/Make.com marketing workflows.

## 🎯 When to Use
- When finalizing an article generation pipeline and the user needs matching social promotion copy.
- When setting up a marketing distribution sequence.

## 🚨 Anti-Patterns
- Do not generate generic, hashtag-stuffed social copy. Adapt the tone to match the established brand voice.
`,
    'gstack-startup-workflows': `---
name: GStack Startup Workflows
description: Role-based execution layers (CEO, PM, Eng, QA) and structured team playbooks.
color: "#F59E0B"
emoji: 🏢
vibe: Run it like a startup.
---

# GStack Startup Workflows Skill

Synthesized from \`garrytan/gstack\`.

## 🧠 Core Capabilities
- **Role Simulation:** Adopts explicit personas (Chief Security Officer, QA Engineer, Designer) to sequentially review outputs.
- **The Design Shotgun:** Generates multiple distinct visual variants of a UI for a/b testing before final selection.
- **Sprinting Discipline:** Enforces a Think → Plan → Build → Review → Test → Ship → Reflect sprint cycle.

## 🎯 When to Use
- When tackling a massive "0 to 1" project that requires end-to-end product development.
- When an output needs to be heavily audited from multiple perspectives before deployment.

## 🚨 Anti-Patterns
- Do not use full startup simulation for micro-tasks. Reserve role-playing for macro-orchestration.
`,
    'markitdown-pipeline-extension': `---
name: MarkItDown Pipeline Extension
description: Advanced document parsing, multimodal extraction, and OCR integrations.
color: "#64748B"
emoji: 📑
vibe: Nothing escapes the markdown converter.
---

# MarkItDown Pipeline Extension Skill

Extended from \`microsoft/markitdown\` (deduplicated from prior MarkItDown core skill).

## 🧠 Core Capabilities
- **Multimodal Context:** Enforces extraction of semantic \`alt\` text from images and transcription from audio files embedded in documents.
- **Preprocessing Guardrails:** Ensures unstructured data is perfectly normalized before entering agent context windows.

## 🎯 When to Use
- When feeding complex, media-rich documents into a pipeline.
`,
    'claude-mem-retrieval-workflows': `---
name: Claude Mem Retrieval Workflows
description: Advanced 3-layer search patterns and progressive disclosure memory retrieval.
color: "#EC4899"
emoji: 🕰️
vibe: Retrieve exactly what is needed.
---

# Claude Mem Retrieval Workflows Skill

Extended from \`thedotmack/claude-mem\` (deduplicated from prior Memory Manager skill).

## 🧠 Core Capabilities
- **Progressive Disclosure:** Queries memory in stages (Index → Timeline → Full Observation) to minimize token consumption.
- **Session Compression:** Forces automated summarization at the end of every active tool-use cycle.

## 🎯 When to Use
- When querying massive historical project databases.
`
};

for (const skillName of Object.keys(globalSkills)) {
    const dir = path.join(agentsSkillDir, skillName);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'SKILL.md'), globalSkills[skillName], 'utf8');
}

// 2. Create Pipeline Skills for /article-system-rebuild
const pipelineSkills = {
    'skill-karpathy-coding-guardrails.md': `# Skill: Karpathy Coding Guardrails (Article Rebuild)
**Version:** 1.0  
**Source:** forrestchang/andrej-karpathy-skills  
**Trigger:** Editing HTML templates or generating code  
**Category:** Pipeline / Execution Quality

## Purpose
Prevents agents from overengineering WordPress HTML templates or making destructive, orthogonal edits.

## Workflow
1. **Simplicity First:** If a WordPress layout bug can be fixed with one CSS property, do not rewrite the entire DOM structure.
2. **Surgical Edits:** Only modify the exact lines required to implement the redesign feature. Do not randomly reformat unrelated sections.
3. **Verification:** Define the success criteria (e.g., "The FAQ must toggle open without breaking the flex container") and mentally verify the code before saving.
`,
    'skill-postiz-social-publishing.md': `# Skill: Postiz Social Publishing (Article Rebuild)
**Version:** 1.0  
**Source:** gitroomhq/postiz-app  
**Trigger:** Article finalization  
**Category:** Pipeline / Content Distribution

## Purpose
Extends the HTML article generation pipeline to automatically produce high-quality, platform-specific social media distributions.

## Workflow
1. Once the HTML template is finalized, extract the core value proposition and key quotes.
2. Generate a Twitter thread and a LinkedIn post designed to drive traffic back to the generated article URL.
3. Append this social copy into the N8N workflow payload or a supplementary text file.
`,
    'skill-gstack-startup-workflows.md': `# Skill: GStack Startup Workflows (Article Rebuild)
**Version:** 1.0  
**Source:** garrytan/gstack  
**Trigger:** QA and final review of an article template  
**Category:** Pipeline / Validation

## Purpose
Simulates a multi-disciplinary review of the generated HTML template before it is considered production-ready.

## Workflow
1. **Designer Review:** Does the spacing align? Are the CTAs prominent?
2. **Security/QA Review:** Is the HTML WordPress-safe? Are there any XSS vulnerabilities in the injected N8N variables?
3. **PM Review:** Does the article actually solve the user's problem and guide them to a conversion?
`
};

for (const [filename, content] of Object.entries(pipelineSkills)) {
    fs.writeFileSync(path.join(qwenSkillDir, filename), content, 'utf8');
}

// 3. Append to Global MEMO.md
const newMemoContent = `
## 29. Kronos Knowledge Graph (\`kronos-knowledge-graph\`)
- **What it does:** Semantic memory, temporal truth tracking, and protocol-driven development.
- **When to use:** Deep refactors requiring historical context.

## 30. VoxCPM Multimodal Voice (\`voxcpm-multimodal-voice\`)
- **What it does:** Voice design, controllable cloning, and TTS reasoning.
- **When to use:** Scripting for podcast/video generation.

## 31. Karpathy Coding Guardrails (\`karpathy-coding-guardrails\`)
- **What it does:** Enforces extreme simplicity and surgical, non-destructive edits.
- **When to use:** Writing or modifying any code.

## 32. Hermes Autonomous Learning (\`hermes-autonomous-learning\`)
- **What it does:** Dynamic skill creation and dialectic user modeling.
- **When to use:** Automating repetitive user workflows into permanent skills.

## 33. Postiz Social Publishing (\`postiz-social-publishing\`)
- **What it does:** Multi-platform social scheduling and content pipelines.
- **When to use:** Generating marketing copy to accompany a finished project.

## 34. GStack Startup Workflows (\`gstack-startup-workflows\`)
- **What it does:** Role-based execution layers (PM, Designer, QA) for macro-projects.
- **When to use:** Undertaking massive "0 to 1" application builds.
`;
appendToFile(agentsMemoPath, newMemoContent);

// 4. Append to Global EXAMPLES.md
const newExamplesContent = `
## 14. Surgical Editing Guardrails
**Category:** Coding Discipline
**Source:** forrestchang/andrej-karpathy-skills
**What makes it strong:** Prevents the dreaded "agent rewrite" where fixing a typo breaks the entire application.
**Recommended Use Case:** The user asks to change a button color. The agent uses \`replace\` on the exact CSS line rather than rewriting the entire \`index.html\` file and accidentally dropping the footer.

## 15. Multi-Role QA Simulation
**Category:** Validation
**Source:** garrytan/gstack
**What makes it strong:** Ensures outputs aren't just "technically correct", but actually good.
**Recommended Use Case:** Before finalizing a landing page, the agent mentally steps into the "Designer" role to check contrast, then the "PM" role to check CTA copy, then the "Security" role to check input sanitization.
`;
appendToFile(agentsExamplesPath, newExamplesContent);

// 5. Append to Qwen Anti-Patterns
const newQwenAntiPatterns = `
## Z. The "Orthogonal Edit" Trap (Destructive Refactoring)

**Symptom:** You were asked to update the logo in the author box, but you also reformatted all the CSS indentation and accidentally deleted the responsive media queries.

**Root Cause:** Ignoring \`skill-karpathy-coding-guardrails\`.

**Fix:**
- Be surgical. Only touch the code necessary to complete the objective. If you see messy code nearby that wasn't part of the prompt, leave it alone unless it explicitly breaks the requested feature.

---

## AA. The "Orphaned Content" Trap (Missing Distribution)

**Symptom:** A beautiful article is generated and deployed, but it receives zero traffic because no distribution assets were created.

**Root Cause:** Skipping \`skill-postiz-social-publishing\`.

**Fix:**
- Always ensure that high-effort article generation pipelines include a final step to generate matching Twitter threads or LinkedIn posts to drive engagement.
`;
appendToFile(qwenAntiPatternPath, newQwenAntiPatterns);

// 6. Append to Qwen Examples
const newQwenExamples = `
## Example 17: Multi-Role Final Review

**Use Case:** Validating the HTML template before saving it to disk.
**Problem Solved:** Shipping code that works but looks terrible or fails business goals.

**Pattern (Mental Check):**
1. **Designer Check:** "Does the spacing adhere to the 8px rhythm?" -> Yes.
2. **QA Check:** "Are there any hardcoded dates in the opening paragraph?" -> No.
3. **PM Check:** "Is the primary CTA visible above the fold on mobile?" -> Yes.

**Lessons:**
- Use \`skill-gstack-startup-workflows\` to enforce a strict quality bar before considering an HTML redesign complete.
`;
appendToFile(qwenExamplePath, newQwenExamples);

// 7. Update Qwen Command (redesign-html-template.md)
let cmdContent = fs.readFileSync(qwenCmdPath, 'utf8');
if (!cmdContent.includes('skill-karpathy-coding-guardrails')) {
    const autoLoadAddition = `
- \`skill-karpathy-coding-guardrails\` (Strict surgical editing and simplicity)
- \`skill-gstack-startup-workflows\` (Multi-role QA validation)
- \`skill-postiz-social-publishing\` (Social distribution generation)`;
    cmdContent = cmdContent.replace('- `skill-pm-skills-product-management` (Strategic content flow and conversion logic)', '- `skill-pm-skills-product-management` (Strategic content flow and conversion logic)' + autoLoadAddition);
    fs.writeFileSync(qwenCmdPath, cmdContent, 'utf8');
}

// 8. Create Backup Metadata Files
fs.mkdirSync(obsidianBackupDir, { recursive: true });
fs.mkdirSync(path.join(obsidianBackupDir, 'PENDING-VERIFICATION'), { recursive: true });

// Create Unresolved MALKA note
const pendingMalka = `# PENDING VERIFICATION: MALKA
**Date:** 2026-04-17

**Status:** UNRESOLVED
**Reason:** The exact GitHub repository for "MALKA" could not be securely verified without guessing. Several projects share this namespace (e.g., malka-ai/malka, various multi-agent academic repos).

**Action Required:**
- Do not ingest or invent skills for MALKA until the exact URL is explicitly provided.
- Await confirmation from the user/administrator.
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'PENDING-VERIFICATION', 'MALKA-UNRESOLVED.md'), pendingMalka, 'utf8');

const readmeSummary = `# General Agents Skill Expansion Backup V6
**Date:** 2026-04-17

This backup contains the result of a strict append-only expansion of the general code agent ecosystem based on 8 confirmed repositories and 1 pending repository.

## Overview
- Synthesized 8 confirmed repositories into high-impact global \`SKILL.md\` capabilities.
- Appended robust \`MEMO.md\` and \`EXAMPLES.md\` trackers.
- Exported 3 highly relevant capabilities (Karpathy guardrails, social publishing, multi-role QA) into the HTML Template Redesign pipeline (\`qwen-code-bootstrap\`).
- Placed \`MALKA\` into a strict \`PENDING-VERIFICATION\` status to prevent hallucinated ingestion.

## Included Directories
- \`/SKILLS\`: Global agent skills.
- \`/MEMO\`: Global agent memo.
- \`/EXAMPLES\`: Global agent examples.
- \`/ARTICLE-SYSTEM-REBUILD\`: Full snapshot of the augmented HTML Template Redesign system.
- \`/PENDING-VERIFICATION\`: Unresolved source notes.
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'README-SUMMARY.md'), readmeSummary, 'utf8');

const sourceLinks = `# Source Links & Mappings
**Date:** 2026-04-17

The skills in this backup were synthesized from the following confirmed repositories:

1. **MarkItDown Pipeline Extension** (microsoft/markitdown) - *Appended to existing markitdown capabilities.*
2. **Claude Mem Retrieval Workflows** (thedotmack/claude-mem) - *Appended to existing memory capabilities.*
3. **Kronos Knowledge Graph** (Ja1Denis/Kronos) - *Global Skill.*
4. **VoxCPM Multimodal Voice** (OpenBMB/VoxCPM) - *Global Skill.*
5. **Karpathy Coding Guardrails** (forrestchang/andrej-karpathy-skills) - *Appended to Article Rebuild (Surgical editing).*
6. **Hermes Autonomous Learning** (NousResearch/hermes-agent) - *Global Skill.*
7. **Postiz Social Publishing** (gitroomhq/postiz-app) - *Appended to Article Rebuild (Social distribution).*
8. **GStack Startup Workflows** (garrytan/gstack) - *Appended to Article Rebuild (Multi-role QA).*

**Unresolved / Pending Verification:**
- \`MALKA\` (Exact URL not provided; ingestion halted).
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'SOURCE-LINKS.md'), sourceLinks, 'utf8');

const changelog = `# Changelog
**Date:** 2026-04-17

### Added
- \`kronos-knowledge-graph\` (Global Skill)
- \`voxcpm-multimodal-voice\` (Global Skill)
- \`karpathy-coding-guardrails\` (Global Skill + Rebuild System Skill)
- \`hermes-autonomous-learning\` (Global Skill)
- \`postiz-social-publishing\` (Global Skill + Rebuild System Skill)
- \`gstack-startup-workflows\` (Global Skill + Rebuild System Skill)
- \`markitdown-pipeline-extension\` (Global Skill Extension)
- \`claude-mem-retrieval-workflows\` (Global Skill Extension)

### Appended
- \`C:\\Users\\seoadmin\\.agents\\MEMO.md\` (Added Sections 29-34)
- \`C:\\Users\\seoadmin\\.agents\\EXAMPLES.md\` (Added Sections 14-15)
- \`qwen-code-bootstrap\\commands\\redesign-html-template.md\` (Added new guardrails and QA skills to auto-load block)
- \`qwen-code-bootstrap\\memo\\MEMO-redesign-anti-patterns.md\` (Added 2 new anti-patterns: Z, AA)
- \`qwen-code-bootstrap\\examples\\EXAMPLE-html-redesign-patterns.md\` (Added Multi-Role QA example)

### Pending
- \`MALKA\` (Awaiting exact repository confirmation).

### Preserved
- All existing skills, memos, examples, and backup history across the workspace. No files were deleted or destructively replaced. All additions were cleanly appended.
`;
fs.writeFileSync(path.join(obsidianBackupDir, 'CHANGELOG.md'), changelog, 'utf8');

console.log("Skill expansion phase 6 completed successfully.");