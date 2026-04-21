---
name: AI Life Skills (Obsidian Vault)
source: https://github.com/reysu/ai-life-skills
category: Tools
purpose: AI-managed Obsidian vault skills — summarize any video/article/PDF/podcast into structured vault notes with wikilinks, and summarize call recordings with speaker labels and transcripts
when_to_use: When summarizing content into an Obsidian vault, transcribing call recordings, or building a personal knowledge base with AI assistance
tags: [obsidian, summarize, transcript, knowledge-base, vault, youtube, pdf, calls]
---

# AI Life Skills (Obsidian Vault)

## Purpose
2 skills that pair with an AI-managed Obsidian vault: summarize any content (video, article, PDF, EPUB, podcast) into vault notes with wikilinks, and transcribe + summarize call recordings with speaker labels.

## When To Use
- `/summarize https://youtube.com/watch?v=...` — any YouTube video
- `/summarize The_Singularity_Is_Near.epub` — books/PDFs dropped in _Attachments/
- `/summarize-call ~/Downloads/call-with-alex.mp4` — call recordings
- Building a personal knowledge base incrementally
- Processing content at scale (10min video = short summary, 3h podcast = long summary)

## How To Apply
**Install (easy mode):**
Paste into Claude Code: "Install ai-life-skills from https://github.com/reysu/ai-life-skills. Clone to ~/src/ai-life-skills, ask where to put the vault, create structure, symlink skills."

**Vault structure:**
```
your-vault/
├── 01 Updates/ 02 Daily/ 03 Meetings/ 04 People/
├── 05 Projects/ 06 Research/ 07 References/ 08 Summaries/
├── _Templates/ _Attachments/ _Bases/
```

**Depth modes (both skills):**
- `detailed`: Creates reference notes for every wikilink, researches public figures, highest-quality model — full note graph
- `minimal`: Summary only, dangling wikilinks, creators/participants only, Sonnet — saves ~85% tokens

**Summarize-call transcription:**
- Local (free, private, slower): mlx_whisper + pyannote.audio (Mac MPS)
- Cloud (paid, fast): ElevenLabs Scribe STT (any OS)

## Examples
- `/summarize https://youtube.com/watch?v=X minimal` → fast summary note, no research
- `/summarize-call ~/meeting.mp4 detailed` → full transcript + speaker notes + participant bios

## Integration Notes
- Deps: yt-dlp, defuddle, pdftotext, pandoc (auto-checked on first run)
- Set VAULT_ROOT env var if running Claude from outside vault directory
- Templates shared between both skills via repo root /templates/
