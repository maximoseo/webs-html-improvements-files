# SKILL: HF Agents
**Source:** https://github.com/huggingface/hf-agents
**Domain:** code
**Trigger:** When detecting what LLM models your hardware can run and spinning up a local coding agent with the best fit model

## Summary
A HuggingFace CLI extension that uses llmfit to detect hardware capabilities, recommends runnable models, starts a llama.cpp server with the best-fit model, and launches a Pi coding agent — all in one command.

## Key Patterns
- `hf agents fit recommend -n 5` — top 5 models for your hardware
- `hf agents fit system` — show detected hardware specs
- `hf agents fit search "qwen"` — search compatible models
- `hf agents fit recommend --use-case coding --min-fit good` — filtered recommendations
- `hf agents run pi` — interactive: pick model → start llama-server → launch Pi agent
- `hf agents run pi --print "hello"` — non-interactive, forward args to Pi
- Reuses existing llama-server if already running on target port
- `LLAMA_SERVER_PORT` env var (default 8080)
- Dependencies: llmfit, llama.cpp (`llama-server`), Pi, jq, fzf, curl

## Usage
Install HF CLI: `curl -LsSf https://hf.co/cli/install.sh | bash`. Install extension: `hf extensions install hf-agents`. Run `hf agents run pi` for interactive model selection and agent launch.

## Code/Template
```bash
# Install
curl -LsSf https://hf.co/cli/install.sh | bash
hf extensions install hf-agents

# Hardware detection
hf agents fit system
hf agents fit recommend -n 5

# Run local coding agent
hf agents run pi                           # interactive
hf agents run pi --print "write hello.py"  # non-interactive

# Custom port
LLAMA_SERVER_PORT=9090 hf agents run pi
```
