# SKILL: OfficeCLI
**Source:** https://github.com/iOfficeAI/OfficeCLI
**Domain:** code
**Trigger:** When an AI agent needs to create, read, modify, or analyze Word (.docx), Excel (.xlsx), or PowerPoint (.pptx) files without Office installed

## Summary
OfficeCLI is a single-binary, dependency-free command-line tool that gives AI agents full control over Office documents. It ships with its own SKILL.md and supports path-based XPath-like navigation, live preview via `watch`, and resident mode for performance.

## Key Patterns
- `officecli create deck.pptx` — create blank file
- `officecli add <file> <path> --type <element> --prop key=val` — add elements
- `officecli set <file> <path> --prop key=val` — modify elements
- `officecli get <file> <path> --json` — read structured data
- `officecli view <file> outline|stats|issues|html` — inspect document
- `officecli query <file> <css-selector>` — CSS-like element query
- Resident mode: `officecli open <file>` → operate → `officecli close <file>`
- Help system: `officecli pptx set shape` for property reference

## Usage
Install: `curl -fsSL https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.sh | bash`
Or Windows: `irm https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.ps1 | iex`
Then direct agents to use `officecli` commands. The SKILL.md at https://officecli.ai/SKILL.md teaches agents full usage.

## Code/Template
```bash
officecli create deck.pptx
officecli add deck.pptx / --type slide --prop title="Q4 Report" --prop background=1A1A2E
officecli add deck.pptx '/slide[1]' --type shape --prop text="Revenue grew 25%" --prop x=2cm --prop y=5cm
officecli view deck.pptx html --browser
```
