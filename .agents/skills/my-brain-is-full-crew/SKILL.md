# SKILL: My Brain Is Full Crew
**Source:** https://github.com/gnekt/My-Brain-Is-Full-Crew
**Domain:** code
**Trigger:** When managing an Obsidian vault with AI agents for note organization, search, transcription, email triage, or building a second brain system

## Summary
8+ coordinated AI agents and 14 specialized skills that manage an Obsidian vault. Works via conversation on Claude Code, Gemini CLI, OpenCode, and Codex CLI. Supports any human language. Agents coordinate through a dispatcher to chain workflows automatically.

## Key Patterns
- Dispatcher coordinates 8+ agents: file/organize → Architect → transcription → email triage → etc.
- Chat IS the interface — no manual file dragging or folder maintenance
- Any language supported; agents respond in your language
- `create a new agent` command for building custom agents via conversation (no code/config)
- Agents chain automatically (e.g., transcription agent discovers project → Architect creates folder structure)
- Compatible platforms: Claude Code, Gemini CLI, OpenCode, Codex CLI (one codebase)
- GDPR note: process only your own data; you're responsible for third-party data compliance
- Custom agents coordinate with core crew, auto-discovered by agent platform

## Usage
Clone repo and open in Claude Code or supported agent. Talk naturally to manage your Obsidian vault. Say "organize my notes from yesterday" or "transcribe this meeting". Say "create a new agent" for custom automation.

## Code/Template
```
# Example agent conversation patterns:
"Organize all my notes from this week by project"
"Transcribe the audio file at ~/recordings/meeting.mp3 and file it"
"Show me all notes related to Project X from the last month"
"Triage my inbox and create action items"
"Create a new agent that tracks my grocery budget"

# Dispatching pattern:
User message → Dispatcher → selects agent → agent runs → 
  if new entity found → Dispatcher chains next agent automatically
```
