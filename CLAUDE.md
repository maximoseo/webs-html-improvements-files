# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Role & Responsibilities

Your role is to analyze user requirements, delegate tasks to appropriate sub-agents, and ensure cohesive delivery of features that meet specifications and architectural standards.

## Workflows

- Primary workflow: `./.claude/rules/primary-workflow.md`
- Development rules: `./.claude/rules/development-rules.md`
- Orchestration protocols: `./.claude/rules/orchestration-protocol.md`
- Documentation management: `./.claude/rules/documentation-management.md`
- And other workflows: `./.claude/rules/*`

**IMPORTANT:** Analyze the skills catalog and activate the skills that are needed for the task during the process.
**IMPORTANT:** You must follow strictly the development rules in `./.claude/rules/development-rules.md` file.
**IMPORTANT:** Before you plan or proceed any implementation, always read the `./README.md` file first to get context.
**IMPORTANT:** Sacrifice grammar for the sake of concision when writing reports.
**IMPORTANT:** In reports, list any unresolved questions at the end, if any.

## Hook Response Protocol

### Privacy Block Hook (`@@PRIVACY_PROMPT@@`)

When a tool call is blocked by the privacy-block hook, the output contains a JSON marker between `@@PRIVACY_PROMPT_START@@` and `@@PRIVACY_PROMPT_END@@`. **You MUST use the `AskUserQuestion` tool** to get proper user approval.

**Required Flow:**

1. Parse the JSON from the hook output
2. Use `AskUserQuestion` with the question data from the JSON
3. Based on user's selection:
   - **"Yes, approve access"** → Use `bash cat "filepath"` to read the file (bash is auto-approved)
   - **"No, skip this file"** → Continue without accessing the file

**Example AskUserQuestion call:**
```json
{
  "questions": [{
    "question": "I need to read \".env\" which may contain sensitive data. Do you approve?",
    "header": "File Access",
    "options": [
      { "label": "Yes, approve access", "description": "Allow reading .env this time" },
      { "label": "No, skip this file", "description": "Continue without accessing this file" }
    ],
    "multiSelect": false
  }]
}
```

**IMPORTANT:** Always ask the user via `AskUserQuestion` first. Never try to work around the privacy block without explicit user approval.

## Python Scripts (Skills)

When running Python scripts from `.claude/skills/`, use the venv Python interpreter:
- **Linux/macOS:** `.claude/skills/.venv/bin/python3 scripts/xxx.py`
- **Windows:** `.claude\skills\.venv\Scripts\python.exe scripts\xxx.py`

This ensures packages installed by `install.sh` (google-genai, pypdf, etc.) are available.

**IMPORTANT:** When scripts of skills failed, don't stop, try to fix them directly.

## [IMPORTANT] Consider Modularization
- If a code file exceeds 200 lines of code, consider modularizing it
- Check existing modules before creating new
- Analyze logical separation boundaries (functions, classes, concerns)
- Use kebab-case naming with long descriptive names, it's fine if the file name is long because this ensures file names are self-documenting for LLM tools (Grep, Glob, Search)
- Write descriptive code comments
- After modularization, continue with main task
- When not to modularize: Markdown files, plain text files, bash scripts, configuration files, environment variables files, etc.

## Documentation Management

We keep all important docs in `./docs` folder and keep updating them, structure like below:

```
./docs
├── project-overview-pdr.md
├── code-standards.md
├── codebase-summary.md
├── design-guidelines.md
├── deployment-guide.md
├── system-architecture.md
└── project-roadmap.md
```

**IMPORTANT:** *MUST READ* and *MUST COMPLY* all *INSTRUCTIONS* in project `./CLAUDE.md`, especially *WORKFLOWS* section is *CRITICALLY IMPORTANT*, this rule is *MANDATORY. NON-NEGOTIABLE. NO EXCEPTIONS. MUST REMEMBER AT ALL TIMES!!!*

<!-- GSD:project-start source:PROJECT.md -->
## Project

**HipsterStyle Article System Rebuild**

A full audit, professional redesign, and production-grade rebuild of the HipsterStyle WordPress article system. Produces 3 deliverables: an improved HTML template, an improved N8N prompt, and an improved N8N workflow JSON — all WordPress-hardened and ready for live deployment on mahsan.websreport.net.

**Core Value:** The final HTML output must be 100% WordPress-safe, premium, and production-grade — anything fragile will break in WordPress.

### Constraints

- **Inline CSS only**: WordPress strips style blocks — all CSS must be inline
- **No external dependencies**: No external CSS/JS, no CDN links for styles
- **WordPress-safe HTML**: article tag wrapper, no markdown, no code fences, no comments
- **Exact N8N injection block**: The TXT prompt must contain the exact injection expressions (non-negotiable)
- **File naming**: Files must be dated exactly 2026-03-25 with -claude-code- suffix
- **Local path**: Final files in ./claude-code/Files/ — not generic shared folders
- **Dropbox target**: /Webs/HTML IMPROVMENT FILES/hipsterstyle.co.il/claude-code/Files
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- JavaScript/TypeScript - All projects use TypeScript for type safety
- React 18/19 - UI layer for all frontend projects
- Node.js - Backend runtime
- SQL - Database schemas with Drizzle ORM and raw SQL migrations
- Shell/Bash - Build scripts and deployment automation
- HTML/CSS - Static markup and Tailwind CSS styling
## Runtime
- Node.js 18+ (explicit requirement in some projects)
- Bun or npm/pnpm as package manager (pnpm is preferred where specified)
- pnpm 9.12.3 - Primary package manager (`nextjs-ai-chatbot`, `paperclip`)
- npm - Secondary option
- Lockfile: `package-lock.json` (npm), `pnpm-lock.yaml` (pnpm), `bun.lock` (root)
## Frameworks
- Next.js 14.2.35, 16.0.10 - Full-stack React framework for web apps
- React 18/19 - Core UI library
- Vite 5.4.19, 6.0.0 - Build tool for SPA projects
- Express.js - HTTP server for backend API
- Tailwind CSS 3.4.x, 4.1.x - Utility-first CSS framework
- PostCSS - CSS processing
- Radix UI components - Accessible component library
- Framer Motion - Animation library
- Zustand - Lightweight state management (`automation/client`)
- React Query (@tanstack/react-query) - Server state management
- Vitest - Fast unit testing framework
- Playwright 1.50+, 1.58.2 - E2E testing
- Testing Library (React) - Component testing utilities
- Turbo - Monorepo build orchestration (`nextjs-ai-chatbot`)
- TypeScript 5.x - Language and type checking
- Biomjs 2.3.11 - Linter and formatter (`nextjs-ai-chatbot`)
- ESLint - Code linting
- tsx - TypeScript execution runtime
## Key Dependencies
- `@ai-sdk/gateway` 3.0.x - Vercel AI Gateway for model abstraction
- `@ai-sdk/react` 3.0.x - React hooks for AI SDK
- `ai` 6.0.37 - Core AI SDK for streaming responses
- `@anthropic-ai/sdk` - Anthropic Claude API client
- `openai` 5.12.x - OpenAI API client
- `drizzle-orm` 0.34.0, 0.44.5, 0.38.4 - Type-safe ORM
- `drizzle-kit` - Database migration tool
- `postgres` 3.4.x - PostgreSQL client
- `@libsql/client` 0.15.x - SQLite client for edge database
- `embedded-postgres` 18.1.0-beta - Embedded PostgreSQL for testing
- `next-auth` 5.0.0-beta.25 - NextAuth.js authentication framework
- `bcrypt-ts` 5.0.2 - Password hashing
- `bcryptjs` 3.0.3 - Alternative password hashing
- `@mendable/firecrawl-js` 4.16.0 - Web scraping and HTML parsing
- `cheerio` 1.2.0 - jQuery-like DOM manipulation
- `axios` 1.7.7 - HTTP client
- `googleapis` 150.0.1 - Google APIs client
- Supabase - PostgreSQL with authentication
- LibSQL (Turso) - Edge SQLite database
- Local file-based SQLite (`.data/` directory)
- `@vercel/blob` 0.24.1 - Vercel Blob storage
- `file-saver` 2.0.5 - Client-side file download
- Prosemirror - WYSIWYG editor toolkit
- CodeMirror 6.x - Code editor component
- Shiki 3.21.x - Code syntax highlighter
- react-syntax-highlighter - Alternative syntax highlighting
- `docx` 9.5.1 - Generate DOCX files
- `jspdf` 4.0.0 - PDF generation
- `html2canvas` 1.4.1 - HTML to canvas rendering
- `xlsx`, `exceljs` - Excel file handling
- Recharts 2.15.4, 3.7.0 - Chart library
- react-data-grid 7.0.0-beta - Data table component
- FullCalendar 6.1.x - Calendar widget
- `zod` 3.25.x - Schema validation and type inference
- `react-hook-form` 7.x - Efficient form state management
- `@hookform/resolvers` - Form validation adapters
- `papaparse` 5.5.2 - CSV parsing
- `fast-xml-parser` 5.3.0 - XML parsing
- `@radix-ui/*` - Headless UI component primitives
- `lucide-react` - Icon library
- `sonner` - Toast notifications
- `cmdk` - Command menu component
- `embla-carousel-react` - Carousel component
- `react-resizable-panels` - Resizable panel layout
- `clsx`, `classnames`, `tailwind-merge` - Conditional CSS classes
- `date-fns` 4.1.0 - Date manipulation
- `nanoid`, `uuid` - ID generation
- `dotenv` - Environment variable loading
- `class-variance-authority` - Type-safe CSS variants
- `fast-deep-equal` - Deep equality comparison
- `@opentelemetry/api` 1.9.0 - Distributed tracing
- `@vercel/analytics` 1.3.1 - Performance monitoring
- `@vercel/otel` 1.12.0 - OpenTelemetry integration
- `nodemailer` 6.9.15 - Email sending
- `redis` 5.0.0 - Redis client for caching/sessions
- `morgan` 1.10.0 - HTTP request logging
- `helmet` 7.1.0 - Security headers
- `cors` 2.8.5 - CORS middleware
- `tsx` - TypeScript executor
- `concurrently` - Run multiple commands
- `esbuild` 0.27.3 - Fast bundler
- `biome` - All-in-one toolchain (ESLint + Prettier)
- `ultracite` - Linting framework
## Configuration
- Environment variables loaded from `.env.local` (development)
- Required for: Database URLs, API keys, secrets
- Pattern: `AUTH_SECRET`, `DATABASE_URL`, `POSTGRES_URL`, `REDIS_URL`, `AI_GATEWAY_API_KEY`
- `next.config.ts` - Next.js build configuration
- `tsconfig.json` - TypeScript compiler options
- `drizzle.config.ts` - ORM migration config
- `vitest.config.ts` - Testing framework setup
- `tailwind.config.ts` - Tailwind CSS customization
- `biome.jsonc` - Code formatter and linter config
- `pnpm-workspace.yaml` - Workspace definition (paperclip)
- Root `package.json` with workspaces (automation)
## Platform Requirements
- Node.js 18+ (explicit in paperclip)
- TypeScript 5.4+
- Recommended: pnpm 9.12+
- Vercel (primary deployment platform for Next.js projects)
- Render (deployment config in `render.yaml`)
- Traditional Node.js hosting (Express server)
- Edge functions supported via `@vercel/functions`
- PostgreSQL (Vercel Postgres, Supabase)
- SQLite (LibSQL/Turso for edge computing)
- Redis (Vercel Redis for caching)
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Components: PascalCase (e.g., `AppShell.tsx`, `Button.tsx`, `ResearchDashboard.tsx`)
- API routes: lowercase with slashes (e.g., `route.ts` at `src/app/api/runs/route.ts`)
- Utilities/helpers: camelCase (e.g., `utils.ts`, `validation.ts`, `guards.ts`)
- Tests: original filename + `.test.ts` suffix (e.g., `validation.test.ts`, `research-progress.test.ts`)
- camelCase for all functions and async functions: `getAuthenticatedUserOrNull()`, `listProjectsForUser()`, `validateAndNormalizeRows()`
- Helper functions use verb-first pattern: `buildRun()`, `enrichQueries()`, `sanitizeFilenameSegment()`
- Event handlers use `on` prefix: `onClick`, `onChange`
- Type guards/checks use `is` or `validate` prefix: `isValid()`, `validateProjectSources()`
- camelCase for all variables and constants
- Constants at module level are UPPERCASE_SNAKE_CASE: `BLOCKED_DOMAINS`, `RESULT_SELECTORS`, `COMMON_SUBDOMAINS`
- Boolean variables often prefixed with `is` or `has`: `isValid`, `hasMarket`, `disabled`
- Callback/handler variables suffixed with `Handler` or use function name directly: `onClick`, `onChange`
- PascalCase for all types, interfaces, and type aliases
- Suffix-based organization: `*Input`, `*Output`, `*Schema`, `*Props`, `*Detail`, `*Snapshot`, `*Run`, `*Row`
- Examples: `CreateResearchInput`, `ButtonProps`, `ResearchRunDetail`, `PageSnapshot`, `ResearchRow`
## Code Style
- ESLint config extends `next/core-web-vitals` (configured at `.eslintrc.json`)
- No explicit Prettier config detected; relies on ESLint formatting
- Line length: appears to follow Next.js defaults (no hard limit visible, but reasonable wrapping observed)
- Semicolons: always used (enforced by default ESLint)
- Single quotes: used in code, double quotes in JSX attributes
- ESLint enabled with Next.js core Web Vitals rules
- No additional custom rules detected beyond Next.js standard
- TypeScript strict mode enabled: `"strict": true` in `tsconfig.json`
- 2 spaces consistently throughout codebase
- Tab character never used
## Import Organization
- `@/*` maps to `./src/*` (configured in `tsconfig.json`)
- Standard usage: `@/lib/*`, `@/server/*`, `@/components/*`, `@/app/*`
- Always preferred over relative imports
## Error Handling
- API routes: return `NextResponse.json()` with error message and HTTP status code
- Server functions: throw `Error` with descriptive message (e.g., `throw new Error('No viable pillar candidates...')`)
- Try-catch blocks: wrap promise operations and file parsing in `src/app/api/runs/route.ts`
- Explicit null/undefined checks before operations
- Type narrowing with `instanceof` checks (e.g., `error instanceof Error`)
- User-facing: descriptive, non-technical (e.g., `"Unable to create the project."`)
- Logging: detailed with context (e.g., `console.error('[POST /api/runs] Failed to create research run:', detail, error)`)
- Zod validation errors: first issue extracted: `parsed.error.issues[0]?.message`
## Logging
- `console.error()` for errors with context prefix: `console.error('[POST /api/runs] ...')`
- Error context includes: route/function name, operation description, error details
- Structured logging not used; simple string concatenation
- Server-side errors that require investigation
- Failed operations with details for debugging
- No logging for successful operations or routine control flow
## Comments
- Section dividers for major code sections: `// ── Sidebar ──`, `// --------------- Types --------`
- Complex logic explanations (e.g., SQL queries, algorithm descriptions)
- Business rule clarifications in validation schemas or agent logic
- API endpoint behavior documentation
- Limited use; focus is on self-documenting code
- Function parameters and return types rely on TypeScript inference
- Schema explanations use JSDoc above Zod schema: `/** For competitor discovery, aboutUrl and sitemapUrl are optional... */`
## Function Design
- Small functions preferred; most functions under 50 lines
- Larger functions (100+ lines) are server-side pipeline components handling complex workflows
- Complex pipelines decomposed into named helper functions
- Destructured objects for configuration/options
- Order: simple parameters first, then objects with default values
- Explicit types for all parameters; no implicit `any`
- Explicit return types on all functions
- Object returns use consistent structure: `{ ok: true, ...result }` or `{ error: string, ... }`
- Async functions always return Promise-wrapped types
## Module Design
- Named exports for functions and types (not default exports)
- Type exports marked with `export type` keyword
- Barrel files at layer boundaries: `src/components/ui/index.ts` exports all UI components
- Default exports only for React components when used in routes: `export default function DashboardPage()`
- Located at `src/components/ui/` - re-exports all UI components
- Enables: `import { Button, Card, Badge } from '@/components/ui'`
- Pattern repeated in `src/components/app/` and other subsystems
- `src/lib/`: shared utilities, types, validation schemas, helpers
- `src/server/`: backend logic isolated from client - auth, database, research operations
- `src/components/`: React components organized by purpose (ui/, app/, research/, auth/)
- `src/app/`: Next.js app router pages and API routes
## TypeScript Patterns
- Let TypeScript infer return types from implementations where obvious
- Explicit return type annotations on exported functions and all API handlers
- Parameter types always explicit
- Used in UI component variants: `variant: 'primary' | 'secondary' | 'ghost' | 'danger'`
- Type safety through literal types
- Used sparingly in utility functions
- Example: `safeJsonParse<T>(value: string, fallback: T): T`
## Client vs Server Code
- Applied to interactive components: buttons, forms, hooks, state management
- Located in `src/components/app/`, `src/components/auth/`, `src/components/research/`
- NOT used in pure presentational or data-fetching components
- Default behavior in Next.js 14 app router
- Used for data fetching at route level
- Examples: `src/app/(app)/dashboard/page.tsx` fetches projects server-side
- Use async/await for database operations and external calls
- Guards check authentication before operations: `const user = await requireAuthenticatedUser()`
- Never expose secrets or raw database queries to client
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
