# SKILL: Code Review Graph - Blast-Radius Code Analysis for AI
**Source:** https://github.com/tirth8205/code-review-graph
**Domain:** code
**Trigger:** When reducing AI token usage during code review, computing blast radius of code changes, or building incremental code analysis pipelines for AI coding tools

## Summary
Builds a structural code graph using Tree-sitter, tracks changes incrementally, and provides precise context to AI assistants via MCP. Achieves 8.2x average token reduction by computing blast radius and supplying only relevant files instead of entire codebases.

## Key Patterns
- Tree-sitter AST → SQLite graph of nodes (functions, classes, imports) + edges (calls, inheritance, tests)
- Blast-radius analysis: traces every caller, dependent, and test affected by a change
- Incremental updates in <2 seconds via SHA-256 hash diffs
- MCP integration: injects graph-aware instructions into Claude Code, Cursor, Codex, etc.
- Monorepo optimization: 27,700+ files → ~15 files actually read (49x reduction)

## Usage
```bash
pip install code-review-graph          # or: pipx install code-review-graph
code-review-graph install              # auto-detects AI tools, writes MCP config
code-review-graph build                # parse codebase (~10s for 500 files)
# Then ask AI: "Build the code review graph for this project"
```

## Code/Template
```bash
# Target specific platform
code-review-graph install --platform claude-code
code-review-graph install --platform codex
code-review-graph install --platform cursor
# Supports: Codex, Claude Code, Cursor, Windsurf, Zed, Continue, OpenCode, Kiro
```
