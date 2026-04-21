# SKILL: Nya AI — AI Chat + Collaboration Platform
**Source:** https://github.com/NitroRCr/nyaai
**Domain:** code
**Trigger:** When building or self-hosting a collaborative AI workspace with MCP, workspaces, and real-time sync

## Summary
Combines AI chat client (with MCP, message branching, web search) and collaboration platform (workspaces, cloud sync, real-time via Zero). BYOK, multimodal, self-hostable via Docker Compose.

## Key Patterns
- MCP integration: Tools, Resources, and Prompts
- Message branching, document input (docx/pdf/pptx), web search/crawl built-in
- Workspace file system with team sharing, roles, and shared AI quota
- Real-time sync via Rocicorp Zero (local-first feel), PWA support

## Usage
Self-host for team AI collaboration. Use docker-compose.example.yml as starting point.

## Code/Template
```bash
# Self-host
cp docker-compose.example.yml docker-compose.yml
# Edit .env, then:
docker compose up -d

# Dev setup
cp .env.example .env && bun install
bun dev:db-up && bun dev:server
npm i -g @rocicorp/zero && zero-cache-dev
bun dev:frontend
```
