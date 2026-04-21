# SKILL: Pi Autoresearch
**Source:** https://github.com/davebcn87/pi-autoresearch
**Domain:** code
**Trigger:** When running autonomous optimization loops for test speed, bundle size, LLM training, build times, or any measurable metric

## Summary
An extension for the pi coding agent that enables autonomous experiment loops: try an idea, benchmark it, keep improvements, revert regressions, repeat forever. Inspired by Karpathy's autoresearch.

## Key Patterns
- `init_experiment` — one-time session config (name, metric, unit, direction)
- `run_experiment` — runs command, times wall-clock, captures output
- `log_experiment` — records result, auto-commits, updates dashboard
- Session files: `autoresearch.md` (objective + history), `autoresearch.sh` (benchmark script)
- Confidence score after 3+ runs: ≥2.0× (likely real), 1.0-2.0× (marginal), <1× (noise)
- `/autoresearch off` — stops mode but keeps `.jsonl` history
- `/autoresearch finalize` — converts noisy branch into clean independent branches per logical change
- Status widget always visible; `Ctrl+X` for full dashboard; `Ctrl+Shift+X` for fullscreen overlay
- Results persist in `autoresearch.jsonl` — survives restarts and context resets

## Usage
Install: `pi install https://github.com/davebcn87/pi-autoresearch`. Start with `/skill:autoresearch-create`. Agent asks about goal, command, metric then starts looping autonomously. Monitor via widget or browser dashboard.

## Code/Template
```bash
# autoresearch.sh template
#!/bin/bash
set -e
# pre-checks
npm test --silent
# run workload and output metric
time_start=$(date +%s%3N)
npm run build
time_end=$(date +%s%3N)
echo "METRIC build_ms=$((time_end - time_start))"
```
