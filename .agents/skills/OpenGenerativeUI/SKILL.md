# SKILL: Open Generative UI
**Source:** https://github.com/CopilotKit/OpenGenerativeUI
**Domain:** design
**Trigger:** When building AI-generated interactive UI components, visual widgets, algorithm visualizations, or embedded iframes from LLM output

## Summary
An open-source showcase for building AI-generated interactive UI with CopilotKit and LangChain Deep Agents. An agent produces fully interactive HTML/SVG rendered in sandboxed iframes — not screenshots, but live components with sliders, charts, and animations streaming as tokens arrive.

## Key Patterns
- **Skills-based architecture**: SKILL.md files in `apps/agent/skills/` loaded on-demand via progressive disclosure
  - `advanced-visualization/SKILL.md` — UI mockups, dashboards, Chart.js, generative art
  - `master-playbook/SKILL.md` — response philosophy, decision trees, narration
  - `svg-diagrams/SKILL.md` — SVG generation rules, component patterns, diagram types
- **`widgetRenderer`**: Frontend `useComponent` hook receives agent HTML and renders in sandboxed iframe
- **Strong models required**: gpt-5.4/claude-opus-4-6/gemini-3.1-pro for complex HTML generation
- **MCP server included**: `assemble_document` tool wraps HTML with design system CSS; skill resources and prompt templates
- **Light/dark theming**: Automatic based on system preference; progressive reveal animations
- **Tech stack**: Next.js 16, React 19, Tailwind 4, LangGraph, CopilotKit v2

## Usage
```bash
make setup   # Install deps + create .env template
make dev     # Start all services (frontend + agent + mcp)
```

For MCP (Claude Code/Cursor): configure `openGenerativeUI` MCP pointing to `http://localhost:3100/mcp`

Available capabilities: algorithm visualizations, 3D animations, charts/diagrams, interactive widgets, forms, simulations.

## Code/Template
```python
# Deep Agent skill loading pattern
from langchain_deepagents import create_deep_agent

agent = create_deep_agent(
    skills_dir="apps/agent/skills/",
    tools=[widget_renderer_tool],
    system_prompt="When asked to visualize, call show_widget with complete HTML"
)
```
```json
{
  "mcpServers": {
    "open-generative-ui": {
      "command": "node",
      "args": ["dist/stdio.js"],
      "cwd": "/path/to/apps/mcp"
    }
  }
}
```
