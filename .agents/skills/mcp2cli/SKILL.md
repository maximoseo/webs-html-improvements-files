# SKILL: mcp2cli
**Source:** https://github.com/knowsuchagency/mcp2cli
**Domain:** code
**Trigger:** When an AI agent needs to call MCP servers, OpenAPI endpoints, or GraphQL APIs from the CLI without writing code — saving 96-99% of tokens wasted on tool schemas

## Summary
mcp2cli turns any MCP server, OpenAPI spec, or GraphQL endpoint into a CLI at runtime with zero codegen. Agents use it to call APIs without loading full tool schemas every turn. Supports OAuth, bake mode for saved configs, and usage-aware tool ranking.

## Key Patterns
- `mcp2cli --mcp <url> --list` — list MCP tools
- `mcp2cli --spec <openapi-url> <command> --arg val` — call OpenAPI endpoint
- `mcp2cli --graphql <url> <query>` — call GraphQL
- `mcp2cli --mcp-stdio "npx @mcp/server" --list` — stdio MCP servers
- Bake mode: `mcp2cli bake create <name> --spec <url>` → `mcp2cli @name command`
- `--top 10 --compact` — token-efficient list output (~20 tokens vs ~1400)
- OAuth: `--oauth` for browser flow, `--oauth-client-id/secret` for machine-to-machine
- Secrets via `env:VAR` or `file:/path` prefixes to avoid CLI exposure

## Usage
```bash
uvx mcp2cli --help
npx skills add knowsuchagency/mcp2cli --skill mcp2cli
```

## Code/Template
```bash
# Connect to MCP server
mcp2cli --mcp https://mcp.example.com/sse --list
mcp2cli --mcp https://mcp.example.com/sse search --query "test"
# Baked tool (no flags every time)
mcp2cli bake create myapi --spec https://api.example.com/openapi.json
mcp2cli @myapi --list --top 10 --compact
mcp2cli @myapi list-items --limit 5
```
