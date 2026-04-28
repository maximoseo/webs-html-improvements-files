# SKILL: Atomic Chat — Open-Source Local LLM Chat App
**Source:** https://github.com/AtomicBot-ai/Atomic-Chat
**Domain:** code
**Trigger:** When setting up a local-first AI chat app with privacy, local LLMs, and MCP support

## Summary
Open-source ChatGPT alternative built with Tauri. Runs local LLMs (Llama, Gemma, Qwen) from HuggingFace, connects cloud providers, supports MCP integration, and exposes OpenAI-compatible API at localhost:1337.

## Key Patterns
- Local AI models via llama.cpp, cloud via OpenAI/Anthropic/Groq/MiniMax
- OpenAI-compatible local server at localhost:1337
- MCP integration for agentic capabilities
- Built with Tauri + Node.js, `make dev` for full setup

## Usage
Use when building or deploying a privacy-first chat interface with local LLM support and MCP tools.

## Code/Template
```bash
git clone https://github.com/AtomicBot-ai/Atomic-Chat
cd Atomic-Chat
make dev    # installs deps, builds, launches app
# Available targets: make dev | make build | make test | make clean
```
