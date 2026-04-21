# SKILL: GBrain
**Source:** https://github.com/garrytan/gbrain
**Domain:** code
**Trigger:** When giving AI agents persistent memory, a knowledge graph, and hybrid search across meetings/emails/notes/companies

## Summary
A production-grade AI agent knowledge graph system (built by Garry Tan, YC CEO) with 26 skills, PGLite database (no server), typed entity links, hybrid search, and 30+ MCP tools. Recall@5 improves from 83% to 95% over pure vector search.

## Key Patterns
- PGLite (no server) — database ready in 2 seconds
- Self-wiring knowledge graph: entity extraction + typed links (`attended`, `works_at`, `invested_in`)
- Hybrid search: vector + graph traversal + backlink-boosted ranking
- 26 skills organized by `skills/RESOLVER.md` — resolver tells agent which skill to load
- 30+ MCP tools via stdio: `gbrain serve` for Claude Code/Cursor/Windsurf
- Remote MCP via ngrok for Claude Desktop, Perplexity, etc.
- Cron jobs for overnight memory consolidation and citation fixing
- Query examples: "who works at Acme AI?", "what did Bob invest in this quarter?"
- Graph-only F1: 86.6% vs grep's 57.8% (+28.8 pts)

## Usage
Install via agent: paste INSTALL_FOR_AGENTS.md URL into agent. Standalone: `git clone && bun install && bun link && gbrain init`. MCP config for Claude Code: add to `~/.claude/server.json`.

## Code/Template
```bash
# Standalone CLI
gbrain init                          # local brain, 2 seconds
gbrain import ~/notes/               # index markdown files
gbrain query "who attended YC S24?"  # hybrid search

# MCP server
gbrain serve                         # stdio MCP server

# ~/.claude/server.json
{"mcpServers": {"gbrain": {"command": "gbrain", "args": ["serve"]}}}
```
