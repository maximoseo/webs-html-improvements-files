---
name: Talk Normal (Anti-Verbose Communication)
source: https://github.com/hexiecs/talk-normal
category: Prompting
purpose: Single system prompt that eliminates AI verbosity — no filler, no fluff, just the answer
when_to_use: When AI responses are too verbose, full of corporate hedging, unnecessary preambles, or filler phrases
tags: [prompting, verbosity, communication, anti-filler, system-prompt]
---
# Talk Normal

## Purpose
Transforms verbose, corporate-sounding AI responses into natural, direct communication. Cuts filler without losing substance.

## When To Use
- AI is using too many hedge words ("Certainly!", "Great question!", "Of course!")
- Responses start with unnecessary preamble before answering
- Bullet lists where flowing text would be better
- Summaries that add no information

## How To Apply
Apply as system prompt or add to CLAUDE.md:
```
Rules: No filler phrases. Answer directly. No "Great question!" or "Certainly!". 
No restating the question. No closing summaries. Just the answer.
```

## Examples Eliminated
- ❌ "Certainly! I'd be happy to help you with that. Great question!"
- ✅ Direct answer
- ❌ "In summary, what we've covered today is..."
- ✅ (nothing — if there's a summary, make it useful)
- ❌ "It's important to note that..."
- ✅ Just state the note

## Integration Notes
- Works as global rule in CLAUDE.md or per-session system prompt
- Compatible with caveman-skill for extreme compression
- Contributions welcome via Issues for new rule suggestions
- CHANGELOG.md tracks rule additions
