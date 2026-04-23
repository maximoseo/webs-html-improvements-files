# SKILL: jCodeMunch MCP
**Source:** https://github.com/jgravelle/jcodemunch-mcp
**Domain:** code
**Trigger:** When an AI agent needs to navigate a codebase efficiently — finding functions, classes, references, or building context bundles — to reduce token usage by 95%+

## Summary
jCodeMunch is an MCP server that indexes codebases using tree-sitter and lets agents retrieve exact symbol implementations instead of scanning entire files. Cuts code-reading token usage by 95%+ in retrieval-heavy workflows.

## Key Patterns
- Index once: `jcodemunch index` — then query cheaply forever
- BM25 symbol search, fuzzy matching, semantic/hybrid search (opt-in)
- `get_ranked_context` — token-budgeted context assembly
- `find_dead_code`, `get_untested_symbols`, `get_changed_symbols` (git-diff-to-symbol)
- `get_blast_radius`, `get_class_hierarchy`, `get_symbol_importance` (PageRank)
- MUNCH compact format: 45.5% median byte savings on top of retrieval savings
- `plan_turn` — session-aware turn budgeting with negative evidence

## Usage
```bash
pip install jcodemunch-mcp
# Add to MCP config, then use find_symbol/find_references/get_ranked_context tools
```

## Code/Template
```python
# Any tool call accepts format= for compact output
find_references(identifier="get_user", format="auto")
# auto = compact if savings >= 15%, else JSON
```
