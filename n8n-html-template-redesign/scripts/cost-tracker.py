#!/usr/bin/env python3
"""
Cost Tracker for n8n HTML Template Redesign Pipeline
Appends per-run cost data to runs/credits-log.jsonl.

Usage:
    python cost-tracker.py --run-id v2026.04.26.a --pipeline full \
        --agent agent-1 --tokens-in 1200 --tokens-out 1200 --model gpt-5.5
    python cost-tracker.py --summary
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Cost per 1M tokens (USD) — update as provider pricing changes
PRICING = {
    "gpt-5.5": {"input": 2.00, "output": 8.00, "provider": "Copilot"},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "provider": "Copilot"},
    "opus-4.7": {"input": 15.00, "output": 75.00, "provider": "Copilot"},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00, "provider": "Copilot"},
    "gemini-3.1-pro-preview": {"input": 1.25, "output": 5.00, "provider": "Gemini"},
    "gemini-3-pro-preview": {"input": 1.25, "output": 5.00, "provider": "Gemini"},
    "gemini-2.5-pro": {"input": 1.25, "output": 5.00, "provider": "Gemini"},
    "kimi-k2.6": {"input": 0.50, "output": 2.00, "provider": "Moonshot"},
    "kimi-k2.5": {"input": 0.50, "output": 2.00, "provider": "Moonshot"},
    "glm-5.1": {"input": 0.30, "output": 1.20, "provider": "Z.ai"},
    "local-script": {"input": 0.0, "output": 0.0, "provider": "local"},
}

LOG_PATH = Path(__file__).parent.parent / "runs" / "credits-log.jsonl"


def ensure_dir() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def calc_cost(model: str, tokens_in: int, tokens_out: int) -> float:
    pricing = PRICING.get(model.lower(), {"input": 2.00, "output": 8.00})
    cost_in = (tokens_in / 1_000_000) * pricing["input"]
    cost_out = (tokens_out / 1_000_000) * pricing["output"]
    return round(cost_in + cost_out, 6)


def log_run(run_id: str, pipeline: str, agent: str, tokens_in: int, tokens_out: int, model: str, skipped: bool = False) -> None:
    ensure_dir()
    cost = 0.0 if skipped else calc_cost(model, tokens_in, tokens_out)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "pipeline_type": pipeline,
        "agent": agent,
        "model": model,
        "provider": PRICING.get(model.lower(), {}).get("provider", "unknown"),
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": cost,
        "skipped": skipped,
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"Logged: {agent} = ${cost:.6f}")


def summarize() -> None:
    if not LOG_PATH.exists():
        print("No cost data logged yet.")
        return

    total_cost = 0.0
    total_in = 0
    total_out = 0
    agent_costs = {}
    model_costs = {}
    run_costs = {}

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            cost = entry.get("cost_usd", 0.0)
            total_cost += cost
            total_in += entry.get("tokens_in", 0)
            total_out += entry.get("tokens_out", 0)
            agent = entry["agent"]
            model = entry["model"]
            run_id = entry["run_id"]
            agent_costs[agent] = agent_costs.get(agent, 0.0) + cost
            model_costs[model] = model_costs.get(model, 0.0) + cost
            run_costs[run_id] = run_costs.get(run_id, 0.0) + cost

    print("=" * 50)
    print(f"Total cost:      ${total_cost:.4f}")
    print(f"Total tokens in:  {total_in:,}")
    print(f"Total tokens out: {total_out:,}")
    print("-" * 50)
    print("By agent:")
    for agent, cost in sorted(agent_costs.items(), key=lambda x: -x[1]):
        pct = (cost / total_cost * 100) if total_cost else 0
        print(f"  {agent:20s} ${cost:8.4f} ({pct:5.1f}%)")
    print("-" * 50)
    print("By model:")
    for model, cost in sorted(model_costs.items(), key=lambda x: -x[1]):
        pct = (cost / total_cost * 100) if total_cost else 0
        print(f"  {model:20s} ${cost:8.4f} ({pct:5.1f}%)")
    print("-" * 50)
    print("By run:")
    for run_id, cost in sorted(run_costs.items(), key=lambda x: -x[1]):
        print(f"  {run_id:20s} ${cost:8.4f}")
    print("=" * 50)


def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline cost tracker")
    parser.add_argument("--run-id", required=True, help="Run identifier")
    parser.add_argument("--pipeline", default="full", help="Pipeline type")
    parser.add_argument("--agent", help="Agent slug")
    parser.add_argument("--tokens-in", type=int, default=0, help="Input tokens")
    parser.add_argument("--tokens-out", type=int, default=0, help="Output tokens")
    parser.add_argument("--model", default="gpt-5.5", help="Model name")
    parser.add_argument("--skipped", action="store_true", help="Mark as skipped (zero cost)")
    parser.add_argument("--summary", action="store_true", help="Show cost summary")
    args = parser.parse_args()

    if args.summary:
        summarize()
        return 0

    if not args.agent:
        print("ERROR: --agent required unless --summary", file=sys.stderr)
        return 1

    log_run(args.run_id, args.pipeline, args.agent, args.tokens_in, args.tokens_out, args.model, args.skipped)
    return 0


if __name__ == "__main__":
    sys.exit(main())
