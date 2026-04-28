# SKILL: Figma MCP Go
**Source:** https://github.com/vkhanhqui/figma-mcp-go
**Domain:** design
**Trigger:** When reading or writing Figma designs programmatically, automating Figma workflows, converting text to design, or generating code from Figma

## Summary
Open-source Figma MCP server with full read/write access via a Figma plugin bridge — no REST API, no rate limits. 73 tools for design automation covering styles, variables, components, prototypes, and content. Works with Cursor, Claude, GitHub Copilot, and any MCP-compatible AI tool.

## Key Patterns
- **No REST API**: Uses Figma plugin bridge — bypasses 6 calls/month Starter plan limit
- **73 tools** covering Create, Modify, Read, Styles, Variables, Components, Prototypes, Content, Export, and Navigation
- **Write tools**: create_frame, create_rectangle, create_ellipse, create_text, import_image, create_component, create_section
- **Modify tools**: set_text, set_fills, set_strokes, set_opacity, set_corner_radius, set_auto_layout, move_nodes, resize_nodes, rotate_nodes, set_constraints, clone_node, set_blend_mode
- **Read tools**: get_node_info, get_selection, get_page_nodes, get_styles, get_variables
- **Design strategies**: Built-in prompts for read_design_strategy, design_strategy
- **Installation**: 2 steps — configure MCP in AI tool + install Figma plugin

## Usage
Setup:
```bash
# Claude Code CLI
claude mcp add -s project figma-mcp-go -- npx -y @vkhanhqui/figma-mcp-go@latest
```
Then install Figma plugin from releases (manifest.json import in Figma Desktop).
Run plugin inside any Figma file to open the bridge.

## Code/Template
```json
// .mcp.json — Claude and MCP-compatible tools
{
  "mcpServers": {
    "figma-mcp-go": {
      "command": "npx",
      "args": ["-y", "@vkhanhqui/figma-mcp-go"]
    }
  }
}

// .vscode/mcp.json — Cursor / VS Code / GitHub Copilot
{
  "servers": {
    "figma-mcp-go": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@vkhanhqui/figma-mcp-go"]
    }
  }
}
```

Key tool patterns:
```
create_frame → { name, x, y, width, height, autoLayout, fill }
set_fills → { nodeId, color: "#635BFF" }
set_auto_layout → { nodeId, direction: "HORIZONTAL", gap: 16, padding: 24 }
set_corner_radius → { nodeId, radius: 8 }
create_text → { characters: "Hello", fontSize: 16, fontName: { family: "Inter" } }
clone_node → { nodeId, x, y }
```
