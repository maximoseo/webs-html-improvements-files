# SKILL: HyperAgents
**Source:** https://github.com/facebookresearch/HyperAgents
**Domain:** code
**Trigger:** When researching self-referential self-improving agent systems, or studying meta-agent architectures that optimize for arbitrary computable tasks

## Summary
A Meta/Facebook Research framework for self-improving agents that run experiments, push results, and optimize for any computable task. Features meta-agent + task-agent architecture with domain-specific optimization loops.

## Key Patterns
- Meta-agent: proposes code modifications to improve task-agent performance
- Task-agent: executes domain tasks and reports results back to meta-agent
- `generate_loop.py --domains <domain>` — entry point for running the algorithm
- `run_meta_agent.py` — run meta-agent and get diffs
- Outputs saved to `outputs/` directory
- `setup_initial.sh` — bootstraps initial agents
- Supports OpenAI, Anthropic, Gemini API keys via `.env`
- WARNING: executes untrusted model-generated code — use in sandboxed environment

## Usage
Clone, set API keys in `.env`, run `bash setup_initial.sh`, then `python generate_loop.py --domains <domain>`. Runs in Docker for safety. Research/experimental use only.

## Code/Template
```bash
# Setup
git clone https://github.com/facebookresearch/HyperAgents
cp .env.example .env  # add API keys
bash setup_initial.sh

# Run in Docker (recommended for safety)
docker build --network=host -t hyperagents .
docker run hyperagents python generate_loop.py --domains math

# Direct (uses venv)
python3.12 -m venv venv_nat && source venv_nat/bin/activate
pip install -r requirements.txt
python generate_loop.py --domains <domain>
```
