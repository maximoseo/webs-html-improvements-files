---
name: Voice Style Skill (Writing Voice Capture)
source: https://github.com/getlago/inside-lago-voice-skill
category: Prompting
purpose: Capture your writing voice into a Claude skill — anti-patterns, audience splits, drafted-vs-sent examples, channel-specific notes
when_to_use: When you want AI to write in your authentic voice rather than generic AI style, for LinkedIn, email, HN, or any channel
tags: [voice, writing, personal-brand, communication, style, linkedin]
---
# Voice Style Skill

## Purpose
Template for creating a personal writing voice skill. Captures how you actually write (not how you wish you wrote) with real drafted-vs-sent examples.

## When To Use
- Draft LinkedIn posts, emails, or articles in your voice
- Reduce AI rewriting time by pre-encoding your style
- Maintain consistent voice across channels and contexts
- Share voice conventions with team members

## How To Apply
1. Clone `SKILL-TEMPLATE.md`
2. Read 10-20 things you wrote by hand
3. Fill in 7 sections:
   - **Voice** — how you actually write
   - **Core Rules** — non-negotiables from your past writing
   - **Anti-Filler Checklist** — patterns you always delete from AI drafts
   - **Audience Adaptation** — different registers (internal vs external, technical vs business)
   - **Channel-Specific Notes** — what changes per platform
   - **Drafted vs Sent** — real examples with lessons (most important section!)
   - **Company Context** — how you talk about product, competitors, positioning

4. Install: drop filled template in `~/.claude/skills/voice/SKILL.md`
5. Invoke: `/voice` in any session

## Integration Notes
- Built by Anh-Tho Chuong, CEO at Lago (open-source billing)
- "Drafted vs Sent" section is the key differentiator — encode the gap between AI output and your actual sends
- Living document — update whenever you rewrite an AI draft before sending
