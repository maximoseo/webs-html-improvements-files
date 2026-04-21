# SKILL: OpenOats - Real-Time Meeting Transcription + Knowledge Search
**Source:** https://github.com/yazinsai/OpenOats
**Domain:** code
**Trigger:** When building macOS meeting assistants, implementing local speech transcription with knowledge base retrieval, or creating offline-capable AI meeting tools

## Summary
macOS app that transcribes both sides of meetings locally (offline), searches a personal knowledge base for relevant talking points in real-time, and surfaces suggestions during calls. Fully local with Ollama, or hybrid with OpenRouter + Voyage AI. Screen-share invisible by default.

## Key Patterns
- Offline speech transcription on-device (no audio leaves Mac)
- Knowledge base: chunks+embeds local .md/.txt files, searches at relevant moments
- Two-stage LLM: local Ollama or cloud OpenRouter (GPT-4o, Claude, Gemini)
- Embedding: Voyage AI, Ollama (nomic-embed-text), or any OpenAI-compatible /v1/embeddings
- Auto-saved transcripts to ~/Documents/OpenOats/
- Screen-share hidden: NSWindow flag prevents sharing capture

## Usage
```bash
brew tap yazinsai/openoats https://github.com/yazinsai/OpenOats
brew install --cask yazinsai/openoats/openoats
# Or: ./scripts/build_swift_app.sh
```

## Code/Template
Requirements: Apple Silicon Mac, macOS 15+, Xcode 26/Swift 6.2
Local mode: Ollama (qwen3:8b + nomic-embed-text) — zero network calls
Cloud mode: OpenRouter API key + Voyage AI API key
