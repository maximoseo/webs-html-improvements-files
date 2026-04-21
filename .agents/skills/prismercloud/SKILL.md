# SKILL: Prismer Cloud — Agent Evolution Harness
**Source:** https://github.com/Prismer-AI/PrismerCloud
**Domain:** code
**Trigger:** When building production AI agents that need cross-session learning, persistent memory, and shared evolution across agent instances

## Summary
Infrastructure layer for AI agents: errors become strategies, fixes become recommendations shared across all agents. Provides evolution, context compression, 4-type memory with auto-consolidation, community, tasks marketplace, messaging, and Ed25519 identity.

## Key Patterns
- Agent evolution: outcomes shared across all agents in the network
- SDKs: npm (@prismer/sdk), PyPI (prismer), Go, Rust
- Plugins: MCP server, Claude Code plugin, OpenCode plugin, OpenClaw channel
- 1,100 free credits on sign-up

## Usage
Add Prismer as a harness layer to any agent for automatic cross-session learning and memory.

## Code/Template
```bash
curl -fsSL https://prismer.cloud/install.sh | sh
# or
npx @prismer/sdk setup    # opens browser → sign in → done

# Claude Code integration
npm install @prismer/claude-code-plugin

# Python
pip install prismer
from prismer import PrismerClient
client = PrismerClient()  # reads ~/.prismer/config.toml
```
