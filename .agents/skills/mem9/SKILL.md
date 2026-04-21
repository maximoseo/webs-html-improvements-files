# SKILL: mem9 (Persistent AI Agent Memory)
**Source:** https://github.com/mem9-ai/mem9
**Domain:** code
**Trigger:** When AI agents need persistent cross-session memory, multi-agent shared memory, or cloud-backed memory with hybrid search across sessions and machines

## Summary
mem9 is a Go server + plugin suite that gives AI agents (Claude Code, OpenCode, OpenClaw) persistent cloud memory backed by TiDB Cloud. Stateless plugins connect to mnemo-server; all agents sharing a tenant ID share one memory pool with vector+keyword hybrid search.

## Key Patterns
- 5 tools: `memory_store`, `memory_search`, `memory_get`, `memory_update`, `memory_delete`
- Plugins for Claude Code (hooks+skills), OpenCode (plugin SDK), OpenClaw, REST API
- TiDB Cloud Starter free tier: 25 GiB, 250M RU/month, native VECTOR type, auto-embedding
- Stateless plugins — all state in mnemo-server; switch machines freely
- Multi-agent collaboration via shared tenant ID

## Usage
```bash
# Deploy server
cd server && MNEMO_DSN="user:pass@tcp(host:4000)/mnemos?parseTime=true" go run ./cmd/mnemo-server
# Claude Code plugin
/plugin marketplace add mem9-ai/mem9
/plugin install mem9@mem9
export MEM9_API_URL="http://localhost:8080" MEM9_API_KEY="..."
```

## Code/Template
```bash
# REST API
curl -X POST localhost:8080/v1alpha2/mem9s/memories \
  -H "X-API-Key: $MEM9_API_KEY" \
  -H "X-Mnemo-Agent-Id: claude-code" \
  -d '{"content": "User prefers TypeScript strict mode"}'
```
