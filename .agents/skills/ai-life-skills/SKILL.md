---
name: AI Life Skills (Obsidian Summarizer)
source: https://github.com/reysu/ai-life-skills
category: Productivity
purpose: Summarize YouTube videos, articles, PDFs, EPUBs, podcasts, and calls into Obsidian vault notes with wikilinks and person notes
when_to_use: When you want to capture and organize research/media into an Obsidian knowledge base automatically
tags: [obsidian, summarize, productivity, knowledge-management, youtube, podcast, calls]
---
# AI Life Skills (Obsidian Summarizer)

## Purpose
Claude Code skills that read from and write to an Obsidian vault — summarizing any media into structured notes with wikilinks.

## Skills
- `summarize/` — YouTube, article, PDF, EPUB, podcast → summary note with wikilinks for every person/concept mentioned
- `summarize-call/` — call recording (video/audio) → transcribe (speaker labels) + call note + transcript + person notes

## Install
```
Install the ai-life-skills pack from https://github.com/reysu/ai-life-skills. 
Clone to ~/src/ai-life-skills, ask me where my Obsidian vault lives, 
create vault folder with full structure, and symlink every skill into ~/.claude/skills/.
```

## Usage
```
/summarize https://youtube.com/watch?v=...
/summarize The Singularity Is Near.epub
/summarize-call ~/Downloads/call-with-alex.mp4
```

## Depth Modes
- `minimal` — summary only, wikilinks dangling, ~85% fewer tokens
- `detailed` — reference notes for every wikilink, person notes for public figures

```
/summarize https://youtube.com/... minimal
/summarize-call ~/call.mp4 --detailed
```

## Vault Structure Created
```
your-vault/
├── 01 Updates/ | 02 Daily/ | 03 Meetings/ | 04 People/
├── 05 Projects/ | 06 Research/ | 07 References/ | 08 Summaries/
├── _Templates/ | _Attachments/ | _Bases/
```

## Integration Notes
- Requires: `yt-dlp`, `defuddle`, `pdftotext`, `pandoc`, `ffmpeg`
- Call transcription: local (whisper + pyannote) or ElevenLabs Scribe (API key)
- Set `VAULT_ROOT` env var if running Claude outside vault directory
- Tested: macOS 15, Apple Silicon, Python 3.11+, Claude Code CLI
