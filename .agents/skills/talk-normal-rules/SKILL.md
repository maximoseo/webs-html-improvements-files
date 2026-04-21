---
name: Talk Normal (Anti-Filler Rules)
source: https://github.com/hexiecs/talk-normal
category: Prompting
purpose: System prompt that transforms verbose, corporate-sounding AI into direct, human communication — strips filler phrases, excessive hedging, and hollow affirmations
when_to_use: When AI responses sound overly formal, add unnecessary caveats, or use filler phrases before answering
tags: [communication, anti-filler, brevity, prompt, style, direct-communication]
---

# Talk Normal Rules

## Purpose
Single system prompt that makes any LLM talk like a normal person. No filler, no fluff, just the answer. Contributions from community — open rule suggestion system.

## When To Use
- AI says "Certainly! That is a great question..." before answering
- Responses are padded with unnecessary hedging
- You want direct, human-style communication
- Multi-language support: English + 中文 (Chinese)

## How To Apply
**Install as system prompt:** Drop the SKILL.md content into your system prompt or Claude Code skill.

**Core rules the prompt enforces:**
- Answer directly — no preamble like "Certainly!" or "Great question!"
- No hollow affirmations ("Absolutely!", "Of course!", "Sure!")
- No excessive hedging ("It's worth noting that...", "It's important to remember...")
- No summary announcements ("In summary...", "To recap...")
- No self-referential transparency ("As an AI language model...")
- Speak in first person naturally
- Be specific, not vague
- Give answers, not permission to answer

## Examples
Before: "Certainly! That's a great question. As an AI language model, I should note that it's important to consider... In summary, the answer is X."
After: "X."

## Integration Notes
- Community-maintained: rule suggestions via GitHub Issues
- CHANGELOG.md tracks rule evolution
- Pairs well with caveman-mode for maximum compression
- Different from caveman-mode: talk-normal removes filler but keeps full sentences; caveman removes structure itself
