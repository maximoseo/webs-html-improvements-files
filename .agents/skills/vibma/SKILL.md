# SKILL: Vibma - AI Agent Figma Design Tool (MCP)
**Source:** https://github.com/ufira-ai/Vibma
**Domain:** code
**Trigger:** When using AI agents to create Figma designs with proper auto-layout, design tokens, and component architecture; or building MCP tools for design tools

## Summary
MCP server enabling AI agents to produce structurally sound Figma files with proper auto-layout, design tokens, component architecture, and reusable design-system patterns. Now superseded by Figma's native MCP, but source remains useful for reference. Best with GPT-5.4 or Claude Opus 4.6.

## Key Patterns
- MCP tools for Figma: create frames, components, variables, styles, icons, images
- Library discovery via FIGMA_API_TOKEN (team library components + styles)
- Stock photo integration via Pexels API
- Supports any MCP-capable LLM (GPT 5.4 recommended, Claude Opus 4.6 for tool use)
- Optional: FIGMA_API_TOKEN, FIGMA_TEAM_ID, PEXELS_API_KEY

## Usage
```bash
# Install from npm (zero cloning)
# Follow CARRYME.md or tell your agent:
# "Set up Vibma so I can vibe-design in Figma. Follow https://raw.githubusercontent.com/ufira-ai/vibma/refs/heads/main/CARRYME.md"
```

## Code/Template
Note: Figma now has native MCP via "Figma for Agents". Vibma source is MIT-licensed reference.
Docs: https://ufira-ai.github.io/Vibma/
