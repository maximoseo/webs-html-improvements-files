# 🔒 Hermes Multi-Agent Git Collaboration — Zero Conflict Plan

**Version:** 1.0
**Date:** April 28, 2026
**Author:** Manager AI
**Dashboard:** https://html-redesign-dashboard.maximo-seo.ai/
**Purpose:** Define the exact rules, structure, and workflow for 3 Hermes agents to work simultaneously on the same GitHub repository without breaking each other's code — targeting ZERO merge conflicts and ZERO functionality damage.

---

## Table of Contents

1. [Executive Summary — The Problem & Solution](#1-executive-summary)
2. [The 3 Agents — Role Assignments](#2-the-3-agents)
3. [Architecture: Git Worktrees (Not Just Branches)](#3-git-worktrees)
4. [File Ownership Map — Who Owns What](#4-file-ownership-map)
5. [The 6 Golden Rules — Never Break These](#5-golden-rules)
6. [Shared Files — The Danger Zone](#6-shared-files)
7. [Branch Naming Convention](#7-branch-naming)
8. [The Complete Workflow — Step by Step](#8-complete-workflow)
9. [Pull Request Protocol](#9-pull-request-protocol)
10. [Merge Order — Dependency-Aware Sequencing](#10-merge-order)
11. [Conflict Prevention — Proactive Strategies](#11-conflict-prevention)
12. [Conflict Resolution — When It Happens Anyway](#12-conflict-resolution)
13. [CI/CD Pipeline — Automated Guardrails](#13-ci-cd-pipeline)
14. [The AGENTS.md File — Repo-Level Rules](#14-agents-md-file)
15. [Communication Protocol Between Agents](#15-communication-protocol)
16. [Lock File System — Reserve Before Editing](#16-lock-file-system)
17. [Testing Requirements — Per Agent](#17-testing-requirements)
18. [Dashboard-Specific Split — Tab-by-Tab Ownership](#18-dashboard-specific-split)
19. [Emergency Procedures — When Things Break](#19-emergency-procedures)
20. [Setup Guide — Full Implementation](#20-setup-guide)
21. [Monitoring & Health Checks](#21-monitoring)
22. [Quick Reference — Cheat Sheet](#22-cheat-sheet)

---

## 1. Executive Summary

### The Problem

3 Hermes agents need to work simultaneously on the same GitHub repo (the dashboard at `html-redesign-dashboard.maximo-seo.ai`). Without strict rules:

```
WHAT CAN GO WRONG:

Agent A: Edits dashboard/src/components/Header.jsx
Agent B: Also edits dashboard/src/components/Header.jsx at the same time
→ RESULT: Whoever pushes last OVERWRITES the other's work. Silent data loss.

Agent A: Updates package.json to add a new dependency
Agent C: Also updates package.json to add a different dependency
→ RESULT: Merge conflict in package.json. Manual resolution needed.

Agent B: Changes the API response format in /api/tasks.js
Agent A: Expects the OLD API format in /components/TaskManager.jsx
→ RESULT: Runtime crash. Task Manager tab breaks in production.

Agent C: Runs `npm install` which regenerates package-lock.json
Agent A: Has a different package-lock.json from their own install
→ RESULT: 5,000+ line merge conflict in package-lock.json. Nightmare.
```

### The Solution

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  3 AGENTS → 3 GIT WORKTREES → 3 BRANCHES → 3 SEPARATE FOLDERS │
│                                                                 │
│  Each agent gets:                                               │
│  ✅ Their own working directory (folder on disk)                │
│  ✅ Their own branch (never touches main directly)              │
│  ✅ Their own file scope (assigned files ONLY)                  │
│  ✅ Their own test suite to verify before merge                 │
│                                                                 │
│  Path to main:                                                  │
│  Agent branch → PR → CI passes → Review → Merge (one at a time)│
│                                                                 │
│  Result: ZERO conflicts, ZERO overwrites, ZERO broken code      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. The 3 Agents — Role Assignments

Each Hermes agent gets a **distinct domain of responsibility**. They NEVER cross into each other's domain without explicit coordination.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  AGENT ALPHA (🔵)                                               │
│  Focus: Dashboard UI — Tabs, Components, Layout                 │
│  Model: Opus 4.7 (Design + Frontend)                            │
│  Owns:  /src/components/                                        │
│         /src/pages/                                              │
│         /src/styles/                                             │
│         /public/                                                 │
│  Branch prefix: alpha/                                          │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AGENT BETA (🟢)                                                │
│  Focus: Backend, API, Database, Data Logic                      │
│  Model: GPT 5.5 (Logic + API)                                  │
│  Owns:  /src/api/                                               │
│         /src/lib/                                                │
│         /src/utils/                                              │
│         /supabase/                                               │
│         /prisma/ or /drizzle/                                   │
│  Branch prefix: beta/                                           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  AGENT GAMMA (🟡)                                               │
│  Focus: Testing, QA, Documentation, CI/CD                       │
│  Model: Gemini 3.1 Pro (Analysis + Testing)                    │
│  Owns:  /tests/                                                 │
│         /docs/                                                   │
│         /.github/                                                │
│         /scripts/                                                │
│         /cypress/ or /playwright/                                │
│  Branch prefix: gamma/                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Why This Split Works

| Frontend (Alpha) | Backend (Beta) | Testing (Gamma) |
|-------------------|----------------|-----------------|
| Components, JSX, CSS | API endpoints, DB queries | Test files, CI config |
| Visual layout, styling | Data processing, auth | Documentation |
| Page routing | Supabase migrations | Deployment scripts |
| UI state management | Server-side logic | E2E test scenarios |

**These domains have natural boundaries — a component file almost never needs to be edited alongside a database migration file.**

---

## 3. Architecture: Git Worktrees (Not Just Branches)

### Why Worktrees, Not Just Branches?

```
WITH REGULAR BRANCHES (DANGEROUS):
┌─────────────────────┐
│  /project/           │ ← ONE folder
│  ├── .git/          │
│  ├── src/           │ ← All 3 agents share the SAME files
│  └── package.json   │ ← Lock contention, stale reads
└─────────────────────┘

Agent A: git checkout alpha/tab-redesign
Agent B: git checkout beta/api-fix        ← KICKS OUT Agent A's changes!
Agent C: git checkout gamma/add-tests     ← KICKS OUT Agent B's changes!

→ Only ONE agent can work at a time. USELESS.


WITH GIT WORKTREES (SAFE):
┌─────────────────────┐
│  /project/           │ ← Main repo (stays on main branch)
│  ├── .git/          │ ← Shared git history
│  ├── src/           │
│  └── package.json   │
├─────────────────────┤
│  /project-alpha/     │ ← Agent Alpha's ISOLATED folder
│  ├── .git (link)    │   (own branch, own files, own index)
│  ├── src/           │
│  └── package.json   │
├─────────────────────┤
│  /project-beta/      │ ← Agent Beta's ISOLATED folder
│  ├── .git (link)    │   (completely separate working directory)
│  ├── src/           │
│  └── package.json   │
├─────────────────────┤
│  /project-gamma/     │ ← Agent Gamma's ISOLATED folder
│  ├── .git (link)    │   (can't see other agents' uncommitted changes)
│  ├── src/           │
│  └── package.json   │
└─────────────────────┘

→ All 3 agents work SIMULTANEOUSLY. Complete filesystem isolation.
→ Changes in /project-alpha/ are INVISIBLE to /project-beta/
→ No lock contention. No stale reads. No overwrites.
```

### How It Works Technically

```
SHARED:
  ✅ Git object database (.git/objects/) — no disk duplication
  ✅ Git references (branches, tags)
  ✅ Git configuration

SEPARATE per worktree:
  ✅ Working directory (all source files)
  ✅ Git index (staging area)
  ✅ HEAD pointer (which branch is checked out)
  ✅ Untracked files
  ✅ node_modules/ (each worktree has its own)
```

### Setup Commands

```bash
# Clone the repo (main working copy)
git clone https://github.com/your-org/html-redesign-dashboard.git project
cd project

# Create worktrees for each agent
git worktree add ../project-alpha -b alpha/workspace
git worktree add ../project-beta -b beta/workspace
git worktree add ../project-gamma -b gamma/workspace

# Verify
git worktree list
# /path/to/project         abc1234 [main]
# /path/to/project-alpha   abc1234 [alpha/workspace]
# /path/to/project-beta    abc1234 [beta/workspace]
# /path/to/project-gamma   abc1234 [gamma/workspace]

# Each agent installs dependencies in their own worktree
cd ../project-alpha && npm install
cd ../project-beta && npm install
cd ../project-gamma && npm install
```

---

## 4. File Ownership Map — Who Owns What

### The Complete Ownership Table

```
PROJECT ROOT
│
├── 📁 src/
│   ├── 📁 components/          ← 🔵 ALPHA ONLY
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   ├── TabBar.jsx
│   │   ├── dashboard/          ← 🔵 ALPHA ONLY
│   │   │   ├── OverviewTab.jsx
│   │   │   ├── ScoreCards.jsx
│   │   │   └── RecentRuns.jsx
│   │   ├── prompt-studio/      ← 🔵 ALPHA ONLY
│   │   ├── kw-research/        ← 🔵 ALPHA ONLY
│   │   ├── task-manager/       ← 🔵 ALPHA ONLY
│   │   ├── skill-radar/        ← 🔵 ALPHA ONLY
│   │   ├── n8n-fixer/          ← 🔵 ALPHA ONLY
│   │   ├── reports/            ← 🔵 ALPHA ONLY
│   │   ├── settings/           ← 🔵 ALPHA ONLY
│   │   └── shared/             ← ⚠️ SHARED (see Section 6)
│   │       ├── Button.jsx
│   │       ├── Dropdown.jsx
│   │       ├── Modal.jsx
│   │       └── Table.jsx
│   │
│   ├── 📁 pages/               ← 🔵 ALPHA ONLY (routing)
│   │   ├── index.jsx
│   │   ├── dashboard.jsx
│   │   ├── tasks.jsx
│   │   └── settings.jsx
│   │
│   ├── 📁 styles/              ← 🔵 ALPHA ONLY
│   │   ├── globals.css
│   │   ├── components/
│   │   └── fixes.css
│   │
│   ├── 📁 api/                 ← 🟢 BETA ONLY
│   │   ├── tasks.js
│   │   ├── pipelines.js
│   │   ├── agents.js
│   │   ├── n8n-fixer.js
│   │   └── reports.js
│   │
│   ├── 📁 lib/                 ← 🟢 BETA ONLY
│   │   ├── supabase.js
│   │   ├── openrouter.js
│   │   ├── auth.js
│   │   └── cache.js
│   │
│   ├── 📁 utils/               ← 🟢 BETA ONLY
│   │   ├── formatters.js
│   │   ├── validators.js
│   │   └── helpers.js
│   │
│   ├── 📁 hooks/               ← ⚠️ SHARED (see Section 6)
│   │   ├── useAuth.js
│   │   ├── useTasks.js
│   │   └── useSupabase.js
│   │
│   └── 📁 types/               ← ⚠️ SHARED (see Section 6)
│       ├── task.ts
│       ├── pipeline.ts
│       └── agent.ts
│
├── 📁 supabase/                ← 🟢 BETA ONLY
│   ├── migrations/
│   └── seed.sql
│
├── 📁 tests/                   ← 🟡 GAMMA ONLY
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
│
├── 📁 docs/                    ← 🟡 GAMMA ONLY
├── 📁 scripts/                 ← 🟡 GAMMA ONLY
├── 📁 .github/                 ← 🟡 GAMMA ONLY
│   └── workflows/
│
├── 📁 public/                  ← 🔵 ALPHA ONLY
│
├── 📄 package.json             ← 🔒 LOCKED (see Section 6)
├── 📄 package-lock.json        ← 🔒 LOCKED
├── 📄 tsconfig.json            ← 🔒 LOCKED
├── 📄 next.config.js           ← 🔒 LOCKED
├── 📄 .env.example             ← 🔒 LOCKED
├── 📄 AGENTS.md                ← 📖 READ-ONLY (all agents read, nobody edits during work)
└── 📄 README.md                ← 🟡 GAMMA ONLY
```

### Ownership Rules

| Symbol | Meaning | Rule |
|--------|---------|------|
| 🔵 | Alpha owns | Only Alpha can create/edit/delete files here |
| 🟢 | Beta owns | Only Beta can create/edit/delete files here |
| 🟡 | Gamma owns | Only Gamma can create/edit/delete files here |
| ⚠️ | Shared | See Section 6 — special coordination required |
| 🔒 | Locked | Cannot be edited without ALL agents stopping work first |
| 📖 | Read-only | All agents read, nobody edits during active work |

---

## 5. The 6 Golden Rules — Never Break These

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   RULE 1: NEVER PUSH DIRECTLY TO MAIN                                   ║
║                                                                          ║
║   Every change goes through:                                             ║
║   Agent branch → Pull Request → CI passes → Review → Merge              ║
║   No exceptions. No "quick fixes." No "just this once."                 ║
║                                                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   RULE 2: NEVER EDIT FILES OUTSIDE YOUR OWNERSHIP SCOPE                  ║
║                                                                          ║
║   Alpha: ONLY files in /components/, /pages/, /styles/, /public/        ║
║   Beta:  ONLY files in /api/, /lib/, /utils/, /supabase/                ║
║   Gamma: ONLY files in /tests/, /docs/, /.github/, /scripts/            ║
║                                                                          ║
║   If you need a change in someone else's scope, REQUEST it               ║
║   via the communication protocol (Section 15).                           ║
║                                                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   RULE 3: NEVER EDIT LOCKED FILES WITHOUT FULL STOP                      ║
║                                                                          ║
║   package.json, package-lock.json, tsconfig.json, next.config.js,       ║
║   .env.example — these affect ALL agents.                                ║
║                                                                          ║
║   To change a locked file:                                               ║
║   1. ALL agents stop work and commit their current changes              ║
║   2. ONE designated agent makes the change on a special branch          ║
║   3. Change is merged to main                                           ║
║   4. ALL agents rebase their worktrees on new main                      ║
║   5. ALL agents resume work                                             ║
║                                                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   RULE 4: REBASE ON MAIN BEFORE CREATING A PULL REQUEST                 ║
║                                                                          ║
║   Before submitting your PR:                                             ║
║   git fetch origin main                                                  ║
║   git rebase origin/main                                                 ║
║                                                                          ║
║   This ensures your branch includes all previously merged work.          ║
║   If rebase creates conflicts, resolve them BEFORE creating the PR.     ║
║                                                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   RULE 5: ALL TESTS MUST PASS BEFORE MERGE                              ║
║                                                                          ║
║   CI runs: lint + typecheck + unit tests + integration tests            ║
║   If ANY test fails, the PR is blocked. Fix first, then merge.          ║
║                                                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   RULE 6: MERGE ONE PR AT A TIME — SEQUENTIAL, NOT PARALLEL             ║
║                                                                          ║
║   Even though agents WORK in parallel, merges happen ONE AT A TIME:     ║
║   1. Agent A's PR merges → CI runs → confirmed green                    ║
║   2. Agent B rebases on new main → PR merges → CI runs → green          ║
║   3. Agent C rebases on new main → PR merges → CI runs → green          ║
║                                                                          ║
║   This prevents "merge trains" where multiple changes interact badly.    ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 6. Shared Files — The Danger Zone

### What Are Shared Files?

Files that multiple agents might need to edit. These are the **#1 source of merge conflicts**.

### Shared File Registry

| File/Folder | Who Reads | Who Writes | Coordination Rule |
|-------------|-----------|------------|-------------------|
| `src/hooks/*` | Alpha + Beta | **Beta only** (creates hooks), Alpha only imports | Alpha requests new hooks via protocol |
| `src/types/*` | Alpha + Beta + Gamma | **Beta only** (defines types) | Types are contracts — change = breaking |
| `src/components/shared/*` | Alpha | **Alpha only** (creates shared components) | Beta/Gamma only import, never edit |
| `package.json` | All | **LOCKED** — designated agent only | Full stop protocol (Rule 3) |
| `package-lock.json` | All | **LOCKED** — auto-generated | Never manually edit |
| `tsconfig.json` | All | **LOCKED** | Full stop protocol |
| `.env.example` | All | **LOCKED** | Full stop protocol |
| `AGENTS.md` | All | **LOCKED** during work | Only edit between work sessions |

### How to Handle Shared File Changes

```
SCENARIO: Alpha needs a new API hook (useNewFeature)

WRONG:
  Alpha creates src/hooks/useNewFeature.js  ← IN BETA'S SCOPE!
  → Merge conflict when Beta also adds a hook

RIGHT:
  1. Alpha creates a CHANGE REQUEST:
     File: .github/change-requests/alpha-needs-hook.md
     Content: "Need useNewFeature hook that fetches /api/new-endpoint"

  2. Beta creates the hook in their worktree:
     src/hooks/useNewFeature.js

  3. Beta's PR is merged first

  4. Alpha rebases, now sees the new hook, imports it in their component

TIME TO COMPLETION: Same as doing it in parallel, but ZERO conflicts.
```

### Interface Contracts

The MOST important shared "file" is the **interface between frontend and backend**. Define it explicitly:

```typescript
// src/types/api-contracts.ts — OWNED BY BETA, READ BY ALL
// This file defines the EXACT shape of API responses
// Alpha relies on these types for component props
// Gamma relies on these types for test fixtures

export interface TaskResponse {
  id: string;
  title: string;
  status: 'todo' | 'in_progress' | 'done' | 'failed';
  priority: 'high' | 'medium' | 'low';
  assignee: string;
  domain: string;
  createdAt: string;
  updatedAt: string;
}

export interface PipelineRunResponse {
  id: string;
  domain: string;
  subdomain: string;
  agentName: string;
  modelName: string;
  status: 'running' | 'success' | 'warning' | 'error';
  scores: {
    accessibility: number;
    performance: number;
    design: number;
    layout: number;
  };
  costUsd: number;
  durationMs: number;
  completedAt: string | null;
}

// ⚠️ CHANGING THESE TYPES IS A BREAKING CHANGE
// All 3 agents must be notified before any change
// Old shape must be supported during transition period
```

---

## 7. Branch Naming Convention

### Format

```
{agent-prefix}/{category}/{short-description}

Examples:
  alpha/feature/task-manager-tab-redesign
  alpha/fix/dropdown-text-visibility
  alpha/refactor/header-component-split

  beta/feature/n8n-fixer-api-endpoints
  beta/fix/supabase-query-performance
  beta/migration/add-n8n-fixes-table

  gamma/test/task-manager-e2e-tests
  gamma/ci/add-lighthouse-audit
  gamma/docs/api-endpoint-documentation
```

### Categories

| Category | Meaning |
|----------|---------|
| `feature/` | New functionality |
| `fix/` | Bug fix |
| `refactor/` | Code restructuring (no behavior change) |
| `style/` | CSS/styling only |
| `migration/` | Database migration |
| `test/` | New or updated tests |
| `ci/` | CI/CD pipeline changes |
| `docs/` | Documentation |
| `chore/` | Maintenance (dependency updates, config) |

### Rules

```
✅ One branch per task/feature (not one mega-branch per agent)
✅ Keep branches short-lived (merge within 1-2 days)
✅ Delete branch after merge
❌ Never reuse a merged branch name
❌ Never have more than 3 active branches per agent
```

---

## 8. The Complete Workflow — Step by Step

### Agent's Daily Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  HERMES AGENT DAILY WORKFLOW                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  STEP 1: SYNC WITH MAIN (every session start)                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  cd /project-alpha                    (go to your worktree)     │   │
│  │  git fetch origin main                (get latest main)         │   │
│  │  git rebase origin/main               (update your branch)     │   │
│  │  npm install                          (if package.json changed) │   │
│  │  npm run build                        (verify build works)      │   │
│  │  npm test                             (verify tests pass)       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│  If ANY step fails → STOP. Fix or escalate before continuing.         │
│                                                                         │
│  STEP 2: CREATE FEATURE BRANCH                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  git checkout -b alpha/feature/task-manager-filters             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  STEP 3: VERIFY OWNERSHIP (before writing ANY code)                     │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  "Am I about to edit a file in MY scope?"                       │   │
│  │  Check AGENTS.md → File Ownership Map                          │   │
│  │  If NO → create Change Request instead                         │   │
│  │  If YES → proceed                                              │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  STEP 4: WRITE CODE (only in your owned files)                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  • Edit ONLY files in your ownership scope                      │   │
│  │  • Follow coding standards from AGENTS.md                      │   │
│  │  • Commit frequently (every logical chunk)                     │   │
│  │  • Write descriptive commit messages                           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  STEP 5: SELF-TEST (before creating PR)                                 │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  npm run lint                         (code style check)        │   │
│  │  npm run typecheck                    (type safety)             │   │
│  │  npm test                             (all tests pass)          │   │
│  │  npm run build                        (production build works)  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│  ALL FOUR must pass. If any fails → fix before proceeding.            │
│                                                                         │
│  STEP 6: REBASE ON LATEST MAIN                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  git fetch origin main                                          │   │
│  │  git rebase origin/main                                         │   │
│  │  (resolve any conflicts — they should be rare with ownership)  │   │
│  │  npm test                             (verify again after rebase)│   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  STEP 7: PUSH & CREATE PR                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  git push origin alpha/feature/task-manager-filters             │   │
│  │  gh pr create --title "feat(alpha): Task Manager filter fixes"  │   │
│  │    --body "## Changes\n- Fixed status dropdown\n- ..."         │   │
│  │    --label "agent:alpha"                                        │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  STEP 8: WAIT FOR CI + REVIEW → MERGE                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  CI pipeline runs automatically                                 │   │
│  │  Wait for all checks to pass                                   │   │
│  │  Reviewer (human or Verifier agent) approves                   │   │
│  │  Merge via GitHub (squash and merge recommended)               │   │
│  │  Delete branch after merge                                     │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  STEP 9: OTHER AGENTS REBASE                                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  After a PR is merged, OTHER agents must:                       │   │
│  │  git fetch origin main                                          │   │
│  │  git rebase origin/main                                         │   │
│  │  npm install (if deps changed)                                  │   │
│  │  This keeps everyone in sync                                   │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Pull Request Protocol

### PR Template (Required for Every PR)

```markdown
## Agent: [Alpha/Beta/Gamma]
## Type: [feature/fix/refactor/test/ci/docs]

### Summary
[One paragraph: what this PR does and why]

### Files Changed
- `src/components/task-manager/TaskFilters.jsx` (modified)
- `src/components/task-manager/TaskCard.jsx` (modified)
- `src/styles/components/task-manager.css` (modified)

### Ownership Verification
- [x] All changed files are within my assigned scope
- [x] No shared files edited (or Change Request approved)
- [x] No locked files edited

### Testing
- [x] `npm run lint` passes
- [x] `npm run typecheck` passes
- [x] `npm test` passes
- [x] `npm run build` passes
- [x] Manual testing done (describe what you tested)

### Screenshots (if UI change)
[Before/After screenshots]

### Breaking Changes
- [ ] This PR changes API contracts (types/api-contracts.ts)
- [ ] This PR changes shared hooks
- [ ] This PR requires database migration
- [ ] None

### Merge Dependencies
- [ ] Must be merged AFTER PR #XX (if applicable)
- [ ] No dependencies — can merge anytime
```

### PR Labels

| Label | Meaning |
|-------|---------|
| `agent:alpha` | Created by Agent Alpha |
| `agent:beta` | Created by Agent Beta |
| `agent:gamma` | Created by Agent Gamma |
| `scope:frontend` | UI/component changes |
| `scope:backend` | API/database changes |
| `scope:tests` | Test changes |
| `priority:critical` | Must merge first |
| `priority:normal` | Standard priority |
| `breaking-change` | Affects other agents |
| `needs-rebase` | Must rebase before merge |

---

## 10. Merge Order — Dependency-Aware Sequencing

### The Merge Queue

PRs are merged ONE AT A TIME in this priority order:

```
MERGE PRIORITY ORDER:

1. 🔒 LOCKED FILE CHANGES (package.json, config)
   → All agents stop, change merges, all agents rebase

2. 🟢 BETA (Backend/API) changes
   → Merged FIRST because frontend depends on backend
   → New API endpoints, type changes, database migrations

3. 🔵 ALPHA (Frontend) changes
   → Merged SECOND — can now use new APIs/types from Beta
   → Component updates, styling fixes, new pages

4. 🟡 GAMMA (Tests/CI) changes
   → Merged LAST — tests cover the newly merged code
   → New test cases, CI pipeline updates

WHY THIS ORDER:
  Backend defines the contracts → Frontend implements the UI → Tests verify both
```

### Merge Process

```
STEP-BY-STEP MERGE (e.g., merging Beta's PR):

1. Beta creates PR: beta/feature/n8n-fixer-api
2. CI runs → all green ✅
3. Reviewer approves
4. Beta merges PR (squash and merge)
5. Main branch is updated

6. Alpha: git fetch origin main && git rebase origin/main
   → Alpha now sees Beta's new API endpoints
   → Alpha can use them in components

7. Gamma: git fetch origin main && git rebase origin/main
   → Gamma now sees both Beta's API and Alpha's components
   → Gamma can write tests for them

8. Next PR ready to merge? Go to step 1.
```

### Visual Timeline

```
TIME →
════════════════════════════════════════════════════════════════

Agent Alpha:  [──── working ────][rebase][── working ──][rebase][── working ──]
Agent Beta:   [── working ──][PR merge ✅]             [── working ──][PR merge ✅]
Agent Gamma:  [─── working ───]         [rebase][─── working ───]         [rebase]

main branch:  ─────────────●──────────────────────●─────────────
                           ↑ Beta merge           ↑ Alpha merge

Key:
  ● = merge point
  [rebase] = agent updates to latest main
```

---

## 11. Conflict Prevention — Proactive Strategies

### Strategy 1: File Scope Boundaries (90% of conflicts prevented)

The ownership map (Section 4) prevents most conflicts. Enforce it with a pre-commit hook:

```bash
#!/bin/bash
# .git/hooks/pre-commit — Enforce file ownership

BRANCH=$(git branch --show-current)
AGENT=""

if [[ "$BRANCH" == alpha/* ]]; then AGENT="alpha"; fi
if [[ "$BRANCH" == beta/* ]]; then AGENT="beta"; fi
if [[ "$BRANCH" == gamma/* ]]; then AGENT="gamma"; fi

if [ -z "$AGENT" ]; then exit 0; fi  # Not an agent branch

CHANGED_FILES=$(git diff --cached --name-only)

# Define ownership
ALPHA_PATHS="src/components/ src/pages/ src/styles/ public/"
BETA_PATHS="src/api/ src/lib/ src/utils/ supabase/ prisma/"
GAMMA_PATHS="tests/ docs/ .github/ scripts/"

VIOLATIONS=""

for FILE in $CHANGED_FILES; do
  case "$AGENT" in
    alpha)
      ALLOWED=false
      for PATH in $ALPHA_PATHS; do
        [[ "$FILE" == ${PATH}* ]] && ALLOWED=true
      done
      ;;
    beta)
      ALLOWED=false
      for PATH in $BETA_PATHS; do
        [[ "$FILE" == ${PATH}* ]] && ALLOWED=true
      done
      ;;
    gamma)
      ALLOWED=false
      for PATH in $GAMMA_PATHS; do
        [[ "$FILE" == ${PATH}* ]] && ALLOWED=true
      done
      ;;
  esac

  if [ "$ALLOWED" = false ]; then
    VIOLATIONS="$VIOLATIONS\n  ❌ $FILE (not in $AGENT scope)"
  fi
done

if [ -n "$VIOLATIONS" ]; then
  echo "🚫 FILE OWNERSHIP VIOLATION"
  echo "Agent $AGENT tried to modify files outside their scope:"
  echo -e "$VIOLATIONS"
  echo ""
  echo "If you need to change these files, create a Change Request."
  exit 1
fi

exit 0
```

### Strategy 2: Import Contracts (Not Direct File Editing)

```
WRONG: Alpha edits src/lib/supabase.js to add a new query
  → This is Beta's file! Merge conflict guaranteed.

RIGHT: Alpha imports from Beta's files — never edits them.

  // Alpha's component:
  import { fetchTasks } from '@/lib/supabase';  // ← import only
  import { TaskResponse } from '@/types/api-contracts';  // ← import only

  // If Alpha needs a new function:
  // → Request Beta to add fetchTasksByDomain() to supabase.js
  // → Beta's PR adds it
  // → Alpha rebases and imports it
```

### Strategy 3: CSS Scoping by Tab

```css
/* Each tab's styles are SCOPED to prevent cross-tab conflicts */

/* Alpha: Task Manager tab — scoped */
.tab-task-manager .task-card { ... }
.tab-task-manager .filter-bar { ... }

/* Alpha: Skill Radar tab — scoped */
.tab-skill-radar .radar-chart { ... }
.tab-skill-radar .skill-list { ... }

/* NEVER use global selectors like: */
.card { ... }       /* ← Which card? What tab? Conflict risk! */
button { ... }      /* ← Overrides ALL buttons across ALL tabs! */
```

### Strategy 4: Component Isolation

```
WRONG: One mega-component that all agents need to edit

// src/components/Dashboard.jsx — 500 lines, everything in one file
// Alpha, Beta, and Gamma all need to touch this file
// → CONFLICT GUARANTEED


RIGHT: Small, focused components in separate files

// src/components/dashboard/OverviewTab.jsx    ← Alpha only
// src/components/dashboard/ScoreCards.jsx     ← Alpha only
// src/components/dashboard/RecentRuns.jsx     ← Alpha only
// src/api/dashboard.js                        ← Beta only
// tests/dashboard.test.js                     ← Gamma only

// No agent needs to edit another agent's files
```

---

## 12. Conflict Resolution — When It Happens Anyway

Despite all precautions, conflicts can still happen (especially in shared files). Here's the resolution protocol:

### Detection

```
Conflicts surface in TWO places:

1. DURING REBASE (agent rebases on main)
   git rebase origin/main
   → CONFLICT in src/hooks/useTasks.js

   Agent sees the conflict markers:
   <<<<<<< HEAD
   const tasks = await fetchTasks(domain);
   =======
   const tasks = await fetchTasksV2(domain, filters);
   >>>>>>> origin/main

2. DURING PR MERGE (GitHub shows "has conflicts")
   → PR cannot be merged until conflicts are resolved
```

### Resolution Rules

```
WHO RESOLVES THE CONFLICT?

Rule 1: The LATER agent resolves.
  If Beta's change was merged first, and Alpha rebases with a conflict,
  Alpha resolves it (incorporating Beta's work).

Rule 2: The FILE OWNER resolves.
  If the conflict is in a file owned by Beta (src/api/tasks.js),
  Beta must resolve it — even if Alpha's PR triggered the conflict.

Rule 3: For SHARED files (hooks, types), BETA resolves.
  Beta owns the contract layer. Type conflicts are resolved by Beta.

Rule 4: When in doubt, STOP and escalate.
  Don't guess. Don't "just pick one side."
  Create an issue: "Conflict in {file} — needs coordination between Alpha and Beta"
```

### Resolution Process

```bash
# Agent discovers conflict during rebase
git rebase origin/main
# CONFLICT in src/types/api-contracts.ts

# Step 1: Understand both sides
git diff --check  # See all conflict markers

# Step 2: Open the file and understand BOTH changes
# <<<<<<< HEAD (your changes)
# =======
# >>>>>>> origin/main (the other agent's changes)

# Step 3: KEEP BOTH changes (usually the right answer)
# Merge both changes logically — don't delete either side

# Step 4: Mark resolved
git add src/types/api-contracts.ts
git rebase --continue

# Step 5: Verify
npm run typecheck
npm test
npm run build

# Step 6: If tests fail after resolution → escalate
```

---

## 13. CI/CD Pipeline — Automated Guardrails

### GitHub Actions Workflow

```yaml
# .github/workflows/agent-pr-check.yml

name: Agent PR Check

on:
  pull_request:
    branches: [main]

jobs:
  # Job 1: Verify file ownership
  ownership-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check file ownership
        run: |
          BRANCH="${{ github.head_ref }}"
          AGENT=""

          [[ "$BRANCH" == alpha/* ]] && AGENT="alpha"
          [[ "$BRANCH" == beta/* ]] && AGENT="beta"
          [[ "$BRANCH" == gamma/* ]] && AGENT="gamma"

          if [ -z "$AGENT" ]; then
            echo "⚠️ Branch doesn't follow naming convention"
            exit 1
          fi

          CHANGED=$(git diff --name-only origin/main...HEAD)
          echo "Agent: $AGENT"
          echo "Changed files:"
          echo "$CHANGED"

          # Check ownership violations
          VIOLATIONS=0
          while IFS= read -r FILE; do
            case "$AGENT" in
              alpha)
                if [[ ! "$FILE" =~ ^(src/components/|src/pages/|src/styles/|public/) ]]; then
                  echo "❌ $FILE — outside Alpha scope"
                  VIOLATIONS=$((VIOLATIONS + 1))
                fi
                ;;
              beta)
                if [[ ! "$FILE" =~ ^(src/api/|src/lib/|src/utils/|supabase/) ]]; then
                  echo "❌ $FILE — outside Beta scope"
                  VIOLATIONS=$((VIOLATIONS + 1))
                fi
                ;;
              gamma)
                if [[ ! "$FILE" =~ ^(tests/|docs/|\.github/|scripts/) ]]; then
                  echo "❌ $FILE — outside Gamma scope"
                  VIOLATIONS=$((VIOLATIONS + 1))
                fi
                ;;
            esac
          done <<< "$CHANGED"

          if [ $VIOLATIONS -gt 0 ]; then
            echo "🚫 $VIOLATIONS ownership violations found"
            exit 1
          fi

          echo "✅ All files within $AGENT scope"

  # Job 2: Lint + Typecheck
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  # Job 3: Tests
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test -- --coverage
      - run: npm run build

  # Job 4: Security scan
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
```

### Branch Protection Rules (GitHub Settings)

```
MAIN BRANCH PROTECTION — CONFIGURE THESE:

✅ Require pull request reviews before merging
   - Required approvals: 1 (human or Verifier agent)

✅ Require status checks to pass before merging
   - ownership-check ✅
   - code-quality ✅
   - tests ✅
   - security ✅

✅ Require branches to be up to date before merging
   - Forces rebase before merge

✅ Require linear history
   - Squash and merge only

❌ Do not allow bypassing settings
   - Even admins must follow the rules

✅ Restrict who can push to matching branches
   - Only GitHub Actions (via merge) — no direct pushes
```

---

## 14. The AGENTS.md File — Repo-Level Rules

Create this file at the repo root. ALL agents read it before starting work:

```markdown
# AGENTS.md — Multi-Agent Collaboration Rules

## Active Agents

| Agent | Prefix | Scope | Model |
|-------|--------|-------|-------|
| Alpha | alpha/ | Frontend: /components, /pages, /styles, /public | Opus 4.7 |
| Beta  | beta/  | Backend: /api, /lib, /utils, /supabase | GPT 5.5 |
| Gamma | gamma/ | Testing: /tests, /docs, /.github, /scripts | Gemini 3.1 |

## Rules

1. NEVER push directly to main — use PRs only
2. NEVER edit files outside your scope — create a Change Request
3. NEVER edit locked files (package.json, config) — use Full Stop protocol
4. ALWAYS rebase on main before creating a PR
5. ALWAYS run lint + typecheck + test + build before pushing
6. ALWAYS use branch naming: {agent}/{category}/{description}
7. Commit messages: {type}({scope}): {description}
   - feat(alpha): add Task Manager filter dropdown
   - fix(beta): correct Supabase query for domain filter
   - test(gamma): add e2e tests for pipeline runs

## Shared Files Protocol

- /src/hooks/ — Beta writes, Alpha imports
- /src/types/ — Beta writes, all import
- /src/components/shared/ — Alpha writes, all import
- Locked files — Full Stop protocol required

## Coding Standards

- Use TypeScript strict mode
- Use functional components (React)
- Use named exports (not default)
- CSS: scope by tab class (.tab-{name} .element)
- No inline styles in React (use CSS modules or styled-components)
- No console.log in committed code (use logger)
- No any types in TypeScript
```

---

## 15. Communication Protocol Between Agents

### Change Request System

When one agent needs a change in another agent's scope:

```
CHANGE REQUEST FORMAT:

File: .github/change-requests/{requesting-agent}-{date}-{id}.md

---
Requesting Agent: Alpha
Target Agent: Beta
Priority: Normal
Status: Open

## Request
Need a new Supabase hook: useTasksByDomain(domain: string)
Should return: TaskResponse[] filtered by domain
Used in: src/components/task-manager/TaskFilters.jsx

## Acceptance Criteria
- Returns typed TaskResponse array
- Supports loading and error states
- Filters by domain parameter
- Sorted by createdAt descending
---
```

### Notification System

```
WHEN AN AGENT MERGES A PR THAT AFFECTS OTHERS:

1. Agent adds a note to: .github/notifications/CHANGELOG.md

   ## [2026-04-28] Beta merged: beta/feature/n8n-fixer-api
   - Added: /src/api/n8n-fixer.js (new endpoint)
   - Added: /src/types/n8n-fixer.ts (new types)
   - Modified: /src/types/api-contracts.ts (new NFixResult type)
   ⚠️ Alpha: New types available for N8N Fixer tab components
   ⚠️ Gamma: New API endpoints need test coverage

2. Other agents check this file after each rebase
```

---

## 16. Lock File System — Reserve Before Editing

For shared files that can't be split, use a lock file system:

```bash
# Agent wants to edit a shared file
# Step 1: Check if locked
cat .github/locks/hooks-useTasks.lock 2>/dev/null
# If file exists → someone else is editing it → WAIT

# Step 2: Acquire lock
echo "Agent: Beta
File: src/hooks/useTasks.js
Since: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Reason: Adding domain filter parameter" > .github/locks/hooks-useTasks.lock
git add .github/locks/ && git commit -m "lock: Beta editing useTasks.js"
git push

# Step 3: Edit the file

# Step 4: Release lock (in same PR)
rm .github/locks/hooks-useTasks.lock
git add .github/locks/ && git commit -m "unlock: Beta done with useTasks.js"
```

---

## 17. Testing Requirements — Per Agent

### What Each Agent Must Test

| Agent | Must Test Before PR | How |
|-------|-------------------|-----|
| **Alpha** | Components render correctly | Unit tests for each component |
| **Alpha** | No visual regressions | Screenshot comparison (optional) |
| **Alpha** | Accessibility passes | axe-core checks in tests |
| **Beta** | API endpoints return correct data | Integration tests with mock DB |
| **Beta** | Database queries work | Migration tests |
| **Beta** | No security vulnerabilities | Input validation tests |
| **Gamma** | All existing tests still pass | Full test suite run |
| **Gamma** | New tests cover merged code | Coverage report check |
| **Gamma** | E2E flows work end-to-end | Playwright/Cypress tests |

### Minimum Test Commands

```bash
# EVERY agent runs ALL of these before PR:
npm run lint          # ← Zero errors, zero warnings
npm run typecheck     # ← Zero type errors
npm test              # ← All tests pass
npm run build         # ← Production build succeeds

# Agent-specific:
# Alpha:
npm run test:components     # Component-level tests
npm run test:a11y           # Accessibility tests

# Beta:
npm run test:api            # API endpoint tests
npm run test:integration    # Database integration tests

# Gamma:
npm run test:e2e            # End-to-end tests
npm run test:coverage       # Coverage threshold check
```

---

## 18. Dashboard-Specific Split — Tab-by-Tab Ownership

For the Hermes dashboard specifically, here's how to split by TAB without conflicts:

```
DASHBOARD TAB OWNERSHIP:

Tab                    │ UI Components (Alpha)  │ API/Logic (Beta)      │ Tests (Gamma)
───────────────────────┼────────────────────────┼───────────────────────┼──────────────────
Overview/Dashboard     │ OverviewTab.jsx        │ api/dashboard.js      │ tests/dashboard/
                       │ ScoreCards.jsx         │ lib/metrics.js        │
                       │ RecentRuns.jsx         │                       │
───────────────────────┼────────────────────────┼───────────────────────┼──────────────────
Prompt Studio          │ PromptStudio.jsx       │ api/prompts.js        │ tests/prompts/
                       │ PromptEditor.jsx       │ lib/openrouter.js     │
                       │ TemplateSelector.jsx   │                       │
───────────────────────┼────────────────────────┼───────────────────────┼──────────────────
KW Research            │ KWResearch.jsx         │ api/keywords.js       │ tests/keywords/
                       │ KeywordTable.jsx       │ lib/keyword-tools.js  │
                       │ DomainSelector.jsx     │                       │
───────────────────────┼────────────────────────┼───────────────────────┼──────────────────
Task Manager           │ TaskManager.jsx        │ api/tasks.js          │ tests/tasks/
                       │ TaskCard.jsx           │ lib/task-engine.js    │
                       │ TaskFilters.jsx        │                       │
                       │ KanbanBoard.jsx        │                       │
───────────────────────┼────────────────────────┼───────────────────────┼──────────────────
Skill Radar            │ SkillRadar.jsx         │ api/skills.js         │ tests/skills/
                       │ RadarChart.jsx         │ lib/skill-analysis.js │
                       │ SkillTable.jsx         │                       │
───────────────────────┼────────────────────────┼───────────────────────┼──────────────────
N8N Fixer              │ N8NFixer.jsx           │ api/n8n-fixer.js      │ tests/n8n-fixer/
                       │ JSONEditor.jsx         │ lib/n8n-analyzer.js   │
                       │ DiagnosisPanel.jsx     │ lib/triple-verdict.js │
                       │ FixGallery.jsx         │                       │
───────────────────────┼────────────────────────┼───────────────────────┼──────────────────
Reports                │ Reports.jsx            │ api/reports.js        │ tests/reports/
                       │ ReportGenerator.jsx    │ lib/pdf-generator.js  │
───────────────────────┼────────────────────────┼───────────────────────┼──────────────────
Settings               │ Settings.jsx           │ api/settings.js       │ tests/settings/
                       │ SettingsForm.jsx       │ lib/config.js         │
```

### How 3 Agents Can Work on 3 Different Tabs Simultaneously

```
EXAMPLE: Alpha, Beta, Gamma all working at the same time

Agent Alpha (Opus 4.7):
  Branch: alpha/feature/task-manager-redesign
  Editing:
    src/components/task-manager/TaskManager.jsx
    src/components/task-manager/TaskCard.jsx
    src/components/task-manager/TaskFilters.jsx
    src/components/task-manager/KanbanBoard.jsx
    src/styles/components/task-manager.css

Agent Beta (GPT 5.5):
  Branch: beta/feature/n8n-fixer-api
  Editing:
    src/api/n8n-fixer.js
    src/lib/n8n-analyzer.js
    src/lib/triple-verdict.js
    src/types/n8n-fixer.ts
    supabase/migrations/20260428_n8n_fixes.sql

Agent Gamma (Gemini 3.1):
  Branch: gamma/test/skill-radar-e2e
  Editing:
    tests/e2e/skill-radar.spec.ts
    tests/fixtures/skill-data.json
    tests/unit/skill-analysis.test.ts

ZERO FILE OVERLAP → ZERO CONFLICTS → ALL 3 MERGE CLEANLY
```

---

## 19. Emergency Procedures — When Things Break

### Scenario 1: Agent Accidentally Edits Wrong File

```
IMMEDIATE ACTIONS:
1. STOP — don't commit the change
2. git checkout -- {wrong-file}  (discard the change)
3. If already committed:
   git revert {commit-hash}  (create a revert commit)
4. Create a Change Request for the correct agent
```

### Scenario 2: Merge Broke Production Build

```
IMMEDIATE ACTIONS:
1. git revert -m 1 {merge-commit}  (revert the bad merge)
2. Push to main (this restores the working state)
3. Investigate: which file caused the break?
4. Agent fixes on their branch
5. Re-submit PR with the fix
```

### Scenario 3: Two Agents Need the Same File RIGHT NOW

```
IMMEDIATE ACTIONS:
1. Both agents STOP editing that file
2. Decide: who has the simpler/faster change?
3. That agent goes first, finishes, and merges
4. Other agent rebases, then makes their change
5. NEVER try to merge concurrent edits to the same file
```

### Scenario 4: Package.json Needs Update

```
IMMEDIATE ACTIONS:
1. ALL agents commit and push current work
2. ALL agents stop editing
3. Designated agent (Beta) creates branch: beta/chore/update-deps
4. Beta updates package.json and runs npm install
5. Beta commits package.json + package-lock.json
6. PR reviewed and merged
7. ALL agents: git fetch && git rebase origin/main && npm install
8. ALL agents resume work
```

---

## 20. Setup Guide — Full Implementation

### One-Time Setup (Run Once)

```bash
# 1. Clone the repository
git clone https://github.com/your-org/html-redesign-dashboard.git project
cd project

# 2. Set up branch protection (do this in GitHub UI)
# See Section 13 for exact settings

# 3. Create the AGENTS.md file at repo root
# See Section 14 for content

# 4. Create worktrees for each agent
git worktree add ../project-alpha -b alpha/workspace
git worktree add ../project-beta -b beta/workspace
git worktree add ../project-gamma -b gamma/workspace

# 5. Install dependencies in each worktree
cd ../project-alpha && npm install
cd ../project-beta && npm install
cd ../project-gamma && npm install

# 6. Verify all worktrees build and test clean
for dir in project-alpha project-beta project-gamma; do
  echo "=== Testing $dir ==="
  cd ../$dir
  npm run build && npm test && echo "✅ $dir OK" || echo "❌ $dir FAILED"
done

# 7. Create required directories
mkdir -p .github/change-requests
mkdir -p .github/locks
mkdir -p .github/notifications
echo "# Agent Change Log" > .github/notifications/CHANGELOG.md

# 8. Install pre-commit hook (in main repo)
cp scripts/pre-commit-ownership-check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# 9. Add CI workflow
# Copy the YAML from Section 13 to .github/workflows/agent-pr-check.yml

echo "✅ Multi-agent setup complete!"
echo "  project/        — main (don't work here directly)"
echo "  project-alpha/  — Agent Alpha workspace"
echo "  project-beta/   — Agent Beta workspace"
echo "  project-gamma/  — Agent Gamma workspace"
```

### Per-Agent Startup Script

```bash
#!/bin/bash
# startup.sh — Run this at the beginning of each work session

AGENT=$1  # alpha, beta, or gamma

echo "🚀 Starting Agent $AGENT session..."

# Go to worktree
cd "../project-$AGENT" || exit 1

# Sync with main
echo "📥 Syncing with main..."
git fetch origin main
git rebase origin/main

if [ $? -ne 0 ]; then
  echo "❌ Rebase conflict detected. Resolve before continuing."
  exit 1
fi

# Install deps (in case they changed)
npm install

# Verify baseline
echo "🧪 Verifying baseline..."
npm run lint && npm run typecheck && npm test && npm run build

if [ $? -eq 0 ]; then
  echo "✅ Agent $AGENT ready to work!"
else
  echo "❌ Baseline broken. Fix before starting new work."
  exit 1
fi
```

---

## 21. Monitoring & Health Checks

### Daily Health Check Script

```bash
#!/bin/bash
# health-check.sh — Run daily to detect drift

echo "🏥 Multi-Agent Health Check"
echo "=========================="

# Check all worktrees exist
echo ""
echo "Worktrees:"
git worktree list

# Check for stale branches (not updated in 3+ days)
echo ""
echo "Branch freshness:"
for branch in $(git branch -r --format='%(refname:short)' | grep -E '^origin/(alpha|beta|gamma)/'); do
  LAST_COMMIT=$(git log -1 --format='%ar' "$branch")
  echo "  $branch — last updated $LAST_COMMIT"
done

# Check for conflicts between active branches
echo ""
echo "Conflict check:"
for agent in alpha beta gamma; do
  BRANCH=$(git -C "../project-$agent" branch --show-current 2>/dev/null)
  if [ -n "$BRANCH" ]; then
    # Try merge dry-run
    git merge-tree $(git merge-base origin/main "$BRANCH") origin/main "$BRANCH" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
      echo "  ✅ $agent ($BRANCH) — clean merge with main"
    else
      echo "  ⚠️  $agent ($BRANCH) — potential conflicts with main"
    fi
  fi
done

# Check for lock files
echo ""
echo "Active locks:"
if ls .github/locks/*.lock 2>/dev/null; then
  cat .github/locks/*.lock
else
  echo "  None"
fi

echo ""
echo "✅ Health check complete"
```

---

## 22. Quick Reference — Cheat Sheet

```
╔═══════════════════════════════════════════════════════════════════════╗
║                   HERMES MULTI-AGENT CHEAT SHEET                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  START OF SESSION:                                                    ║
║    cd project-{agent}                                                 ║
║    git fetch origin main && git rebase origin/main                   ║
║    npm install && npm test                                            ║
║                                                                       ║
║  START NEW TASK:                                                      ║
║    git checkout -b {agent}/feature/{description}                     ║
║                                                                       ║
║  CHECK OWNERSHIP:                                                     ║
║    "Is this file in MY scope?" → Check AGENTS.md                     ║
║    Alpha: /components, /pages, /styles, /public                      ║
║    Beta:  /api, /lib, /utils, /supabase                              ║
║    Gamma: /tests, /docs, /.github, /scripts                         ║
║                                                                       ║
║  BEFORE PR:                                                           ║
║    npm run lint && npm run typecheck && npm test && npm run build     ║
║    git fetch origin main && git rebase origin/main                   ║
║    git push origin {branch}                                           ║
║    gh pr create --label "agent:{name}"                               ║
║                                                                       ║
║  AFTER SOMEONE ELSE MERGES:                                           ║
║    git fetch origin main && git rebase origin/main                   ║
║    npm install (if deps changed)                                      ║
║                                                                       ║
║  NEED A FILE IN SOMEONE ELSE'S SCOPE:                                ║
║    Create .github/change-requests/{agent}-{date}.md                  ║
║    NEVER edit their files directly                                    ║
║                                                                       ║
║  MERGE ORDER: Beta → Alpha → Gamma                                   ║
║  (Backend first, then Frontend, then Tests)                          ║
║                                                                       ║
║  EMERGENCY: git revert -m 1 {commit} (undo a bad merge)             ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## Summary

| Problem | Solution | Conflict Risk |
|---------|----------|---------------|
| Same file edited by 2 agents | File ownership map — strict scopes | **0%** |
| Stale code (agent doesn't see other's changes) | Git worktrees — complete isolation | **0%** |
| Direct push breaks main | Branch protection + required PR + CI | **0%** |
| Merge conflicts in shared files | Lock system + change requests + sequential merge | **< 5%** |
| Dependency file conflicts (package.json) | Full Stop protocol — one agent at a time | **0%** |
| API contract breaks frontend | Types file owned by Beta, imported by Alpha | **0%** |
| Tests don't cover new code | Gamma writes tests after Alpha+Beta merge | **0%** |

**Total estimated conflict rate with this system: < 2%**
**Without this system: 40-60% conflict rate**

The key insight: **conflicts come from two agents editing the same file. If you prevent that with ownership boundaries, worktrees, and sequential merges — conflicts drop to near zero.**
