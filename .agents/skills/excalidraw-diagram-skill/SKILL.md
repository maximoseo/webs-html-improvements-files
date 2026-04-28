# SKILL: Excalidraw Diagram Skill
**Source:** https://github.com/coleam00/excalidraw-diagram-skill
**Domain:** visual-communication
**Trigger:** Use when generating Excalidraw diagrams from natural language, creating technical architecture diagrams with visual validation, or building diagrams that "argue visually" rather than just display information.

## Summary
A coding agent skill that generates Excalidraw diagrams using opinionated visual methodology: fan-outs for one-to-many, timelines for sequences, convergence for aggregation. Includes a Playwright render pipeline for visual validation and brand-customizable color palettes.

## Key Patterns
- Diagrams argue, not display — shapes mirror their conceptual meaning
- Visual validation loop: render via Playwright → detect layout issues → fix → deliver
- Brand-customizable via single `references/color-palette.md` file
- Evidence artifacts: real code snippets and JSON payloads in technical diagrams
- File structure: SKILL.md (methodology) + element-templates.md + json-schema.md + render script

## Usage
Tell the agent: "Create an Excalidraw diagram showing [system/concept]". The skill handles concept mapping, layout, JSON generation, rendering, and visual validation automatically.

## Code/Template
```bash
# Install
git clone https://github.com/coleam00/excalidraw-diagram-skill.git
cp -r excalidraw-diagram-skill .claude/skills/excalidraw-diagram

# Setup renderer
cd .claude/skills/excalidraw-diagram/references
uv sync && uv run playwright install chromium

# Example prompt
"Create an Excalidraw diagram showing the microservices architecture"
```
