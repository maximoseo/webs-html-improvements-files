# SKILL: Claudebox — Claude in Isolated Docker Container
**Source:** https://github.com/ArmanJR/claudebox
**Domain:** code
**Trigger:** When you need to run Claude with full tool access in an isolated, sandboxed environment

## Summary
Runs Claude Code inside Docker with network isolation (iptables firewall, Anthropic domains only). Exposes HTTP API and OpenAI-compatible endpoints. Uses existing Claude subscription — no extra billing.

## Key Patterns
- CLI tool or Docker Compose service
- OpenAI-compatible /v1/chat/completions endpoint
- Network isolation: blocks all outbound except Anthropic API
- Max concurrent requests configurable, POST /prompt with options (model, maxTurns, maxBudgetUsd, allowedTools)

## Usage
Use when you need sandboxed Claude agent execution or to expose Claude as a microservice in a Docker Compose stack.

## Code/Template
```bash
# Install CLI
curl -fsSL https://raw.githubusercontent.com/ArmanJR/claudebox/main/install.sh | bash

claudebox prompt "explain how DNS works"
claudebox server --openai      # OpenAI-compatible API on :3000

# Docker Compose service
curl -fsSL https://raw.githubusercontent.com/ArmanJR/claudebox/main/setup-auth.sh | bash
# Add to docker-compose.yml:
# services:
#   claudebox:
#     image: ghcr.io/armanjr/claudebox:latest
#     ports: ["3000:3000"]
#     env_file: [.env.claude]
```
