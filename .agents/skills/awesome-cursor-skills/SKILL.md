---
name: Awesome Cursor Skills (Curated Skill List)
source: https://github.com/spencerpauly/awesome-cursor-skills
category: Agent Skills
purpose: Curated list of the best SKILL.md files for Cursor AI — organized by category with install instructions
when_to_use: When discovering skills to add to a Cursor project; reference list for building a well-rounded skill set
tags: [cursor, skills, curated, reference, meta]
---
# Awesome Cursor Skills

## Purpose
Curated collection of high-quality SKILL.md files for Cursor AI — the "awesome list" for skills, organized by category.

## Categories Covered
- **Coding** — algorithms, data structures, patterns
- **UI/UX** — design systems, accessibility, responsive
- **Backend** — APIs, databases, architecture
- **DevOps** — CI/CD, Docker, infrastructure
- **AI/ML** — prompting, agent patterns, fine-tuning
- **Testing** — TDD, coverage, e2e patterns
- **Documentation** — README, JSDoc, API docs

## Install Pattern
For each skill in the list:
```bash
# Create skills dir if not exists
mkdir -p .cursor/skills/<skill-name>/

# Download and place SKILL.md
curl -o .cursor/skills/<skill-name>/SKILL.md \
  https://raw.githubusercontent.com/author/repo/main/SKILL.md
```

## Best Practice from This Repo
- Keep skills small and focused (one responsibility)
- Include concrete examples in every skill
- Add "when to use" to avoid over-triggering
- Version your skills with comments
- Test skill effectiveness by comparing output quality with/without

## Integration Notes
- Pairs with `autoskills` for auto-installation
- Cross-compatible with Claude Code (`.claude/skills/`), Cursor (`.cursor/rules/`), Copilot (`.github/instructions/`)
- Use `sdd-skill` for symlink-based multi-tool sharing
