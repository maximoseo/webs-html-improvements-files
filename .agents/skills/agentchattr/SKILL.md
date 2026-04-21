# SKILL: AgentChattr
**Source:** https://github.com/bcurts/agentchattr
**Domain:** code
**Trigger:** When coordinating multiple AI coding agents (Claude, Codex, Gemini, Copilot) in real-time or enabling agent-to-agent communication

## Summary
A local chat server that enables real-time coordination between multiple AI coding agents and humans via a shared web UI. Agents wake each other up via @mentions, communicate through channels, and coordinate on jobs without manual copy-pasting.

## Key Patterns
- Shared chat room with multiple channels (like Slack) for agent coordination
- @mention triggers auto-inject prompts into agent terminals
- Loop guard pauses after N agent-to-agent hops to prevent runaway conversations
- Jobs system for bounded work conversations with status tracking (To Do → Active → Closed)
- MCP-based integration: agents use `chat_send`, `chat_read`, `chat_channels` tools
- Auto-approve variants for autonomous operation (`--dangerously-skip-permissions`)
- Cross-platform launchers (Windows `.bat`, macOS/Linux `.sh` with tmux)

## Usage
Launch agent launchers from `windows/` or `macos-linux/` folders. Open http://localhost:8300 to chat. Type @agentname to wake an agent. Agents @mention each other to coordinate autonomously. Use /continue to resume after loop guard pause. Convert messages to jobs for tracked work items.

## Code/Template
```bash
# macOS/Linux
sh start_claude.sh    # starts Claude in tmux session
sh start_codex.sh     # starts Codex
# Detach: Ctrl+B, D — reattach: tmux attach -t agentchattr-claude

# MCP tools agents use:
# chat_send(channel="general", message="...")
# chat_read(channel="general")
# chat_channels()
```
