# SKILL: SentrySearch — Semantic Video Search
**Source:** https://github.com/ssrajadh/sentrysearch
**Domain:** ai-tools
**Trigger:** Use when implementing natural language search over security camera footage, video archives, or any video collection — returning trimmed clips matching text queries.

## Summary
SentrySearch splits videos into overlapping chunks, embeds each via Gemini Embedding API or local Qwen3-VL, stores in ChromaDB, and returns trimmed clips matching natural language queries. Supports local-only mode with no API key via Ollama.

## Key Patterns
- `sentrysearch index /path/to/footage` — chunk and embed videos
- `sentrysearch search "red truck running stop sign"` — returns trimmed clip
- `--chunk-duration 30 --overlap 5` — chunking configuration
- `--target-resolution 480 --target-fps 5` — preprocessing for cost reduction
- Local mode: Qwen3-VL via Ollama (no API key needed)
- Cloud mode: Gemini API (set spending limit!)
- OpenClaw skill available at clawhub.ai

## Usage
When user wants to search surveillance video, personal footage archives, or any video collection using natural language. Set spending limit before using Gemini API.

## Code/Template
```bash
pip install uv
uv tool install .

sentrysearch init  # prompts for Gemini API key (or use Ollama)
sentrysearch index /path/to/footage
sentrysearch search "person in red jacket near entrance"
# → saves trimmed clip to output directory
```
