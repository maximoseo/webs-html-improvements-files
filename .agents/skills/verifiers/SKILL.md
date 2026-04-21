# SKILL: Verifiers — LLM Reinforcement Learning Environments
**Source:** https://github.com/PrimeIntellect-ai/verifiers
**Domain:** code
**Trigger:** When training or evaluating LLMs with reinforcement learning, creating RL environments, or generating synthetic data

## Summary
Library for creating environments to train and evaluate LLMs. Each environment has a dataset, agent harness (tools, sandboxes, context management), and reward rubric. Integrates with Prime Intellect Environments Hub and prime-rl training framework.

## Key Patterns
- Composable Task/Agent/Environment architecture
- RLMEnv for coding/tool-use RL tasks
- `prime env init my-env` to scaffold a new environment
- Built-in: opencode harness, browser env, multi-worker env server
- `vf-tui` for eval visualization

## Usage
Use for RL fine-tuning of LLMs on code/reasoning tasks, or generating synthetic training data.

## Code/Template
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install prime && prime login
prime lab setup          # scaffold workspace
prime env init my-env    # create new environment template
uv run vf-build my-env   # build OpenEnv image

# environments/my_env/my_env.py
import verifiers as vf
env = vf.Environment(dataset=..., rubric=..., harness=...)
```
