# SKILL: mnemo (Agent Memory CLI)
**Source:** https://github.com/joshndala/mnemo-agent
**Domain:** code
**Trigger:** When managing, exporting, comparing, or querying AI agent memory across sessions and providers (Mem0, Letta, local filesystem)

## Summary
mnemo is a git-like CLI for agent memory: dump, diff, migrate, and query what agents know using a normalized fact schema. Supports semantic search, MCP server, web UI, S3 sync, and auto-extraction from chat logs.

## Key Patterns
- Normalized schema: `{entity, attribute, value, source, timestamp, confidence, metadata.tags}`
- 17 CLI commands: `add`, `show`, `recall`, `search`, `diff`, `dump`, `load`, `ingest`, `push`, `pull`
- Search modes: tfidf (default), semantic (fastembed ONNX), hybrid
- MCP server: `mnemo serve --agent <name> --stdio` for Claude Desktop/Cursor
- Auto-ingest chat logs: Claude.ai, ChatGPT, Cursor exports → structured facts
- Web UI: `mnemo ui` for visual browsing

## Usage
```bash
pip install mnemo-agent                    # core
pip install "mnemo-agent[semantic,ingest,s3,sdk]"   # all extras
mnemo init --agent my-agent
mnemo add --fact "User prefers TypeScript" --agent my-agent
mnemo recall "tech preferences" --agent my-agent --method semantic
mnemo serve --agent my-agent --stdio      # MCP server for Claude Desktop
```

## Code/Template
```bash
# Diff two agent memory snapshots
mnemo diff --agent-a agent-v1 --agent-b agent-v2 --html diff.html
# Ingest chat log
mnemo ingest --file claude_chat.json --agent my-agent --extractor claude
```
