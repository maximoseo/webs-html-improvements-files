# SKILL: Skills Best Practices — How to Write Agent Skills
**Source:** https://github.com/mgechev/skills-best-practices
**Domain:** agent-tools
**Trigger:** Use when creating, reviewing, or improving AI agent skills — for guidance on structure, frontmatter optimization, context management, trigger descriptions, and CI/CD validation.

## Summary
Concentrated best practices guide for writing professional-grade agent skills. Covers directory structure, frontmatter optimization, progressive disclosure, JiT loading, specific procedural instructions, and validation via `skillgrade`.

## Key Patterns
- Required structure: `skill-name/SKILL.md` + `scripts/` + `references/` + `assets/`
- Name: 1-64 chars, lowercase+numbers+hyphens, must match directory name exactly
- Description max 1,024 chars; include negative triggers ("Don't use for Vue/Svelte")
- Keep SKILL.md <500 lines; offload details to flat subdirectories (one level deep)
- JiT loading: explicitly instruct agent when to read reference files
- Use relative paths with forward slashes regardless of OS
- No README.md, CHANGELOG.md, or human-oriented docs in skill dirs
- Validate with `skillgrade` for regression testing

## Usage
Load this skill when writing or reviewing any agent skill. Apply frontmatter rules strictly. Test trigger descriptions before publishing.

## Code/Template
```
skill-name/
├── SKILL.md              # <500 lines, navigation + procedures
├── scripts/              # Tiny CLIs, not library code
├── references/           # One level deep only
└── assets/               # Templates, schemas, static files
```
