# SKILL: cryload — HTTP Load Testing CLI
**Source:** https://github.com/sdogruyol/cryload
**Domain:** developer-tools
**Trigger:** Use when load testing HTTP APIs/microservices, benchmarking request throughput and latency percentiles, running stress tests in CI/CD pipelines, or comparing performance before/after changes.

## Summary
cryload is a cross-platform HTTP load testing CLI (Crystal lang) — a modern ab/wrk alternative with JSON/CSV output for CI/CD, p50–p999 latency percentiles, global RPS rate limiting, redirect following, and histogram summaries. Single binary, no Lua scripting.

## Key Patterns
- `cryload -c 50 -n 1000 https://api.example.com` — 50 concurrent, 1000 requests
- `cryload -c 10 -d 30 -t json https://api.example.com` — 30s duration, JSON output
- `--rate 100` — global RPS cap (rate limiting)
- JSON output for CI/CD integration; CSV for data analysis
- Latency percentiles: p50, p90, p99, p999
- Follow redirects, custom success HTTP codes, custom headers/body/auth

## Usage
When user needs to benchmark an API or run load tests in CI. Use JSON output for programmatic result parsing, or text for human-readable histogram.

## Code/Template
```bash
# Install
curl -sSfL https://raw.githubusercontent.com/sdogruyol/cryload/master/scripts/install.sh | sh -s

# Usage
cryload -c 50 -n 10000 https://api.example.com/health
cryload -c 10 -d 60 -t json https://api.example.com > results.json
cryload -c 20 -n 5000 --rate 500 -H "Authorization: Bearer $TOKEN" https://api.example.com
```
