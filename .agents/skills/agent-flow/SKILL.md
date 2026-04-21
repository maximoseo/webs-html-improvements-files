# SKILL: Agent Flow
**Source:** https://github.com/patoles/agent-flow
**Domain:** code
**Trigger:** When wanting to visualize Claude Code agent execution in real time — debugging tool call chains, understanding subagent coordination, or profiling agent performance

## Summary
Agent Flow is a real-time node-graph visualization of Claude Code agent orchestration. It auto-detects active sessions, streams events via Claude Code hooks, and renders interactive agent trees showing tool calls, branching, subagent coordination, timing, and file attention heatmaps.

## Key Patterns
- Claude Code hooks: lightweight HTTP hook server receives events for zero-latency streaming
- Auto-detects Claude Code sessions; also supports JSONL event log files
- Interactive canvas: pan, zoom, click agents/tool calls to inspect details
- Timeline + transcript panels + file attention heatmap
- Multi-session tabs for concurrent agent monitoring
- VS Code extension + standalone web app (`npx agent-flow-app`)

## Usage
```bash
# Standalone (no VS Code needed)
npx agent-flow-app             # starts visualizer + opens browser
# OR from source
git clone https://github.com/patoles/agent-flow && cd agent-flow
pnpm i && pnpm run setup       # configure Claude Code hooks (one-time)
pnpm run dev                   # start web app + event relay
# Start a Claude Code session in another terminal — events stream in
```

## Code/Template
```bash
# VS Code: Command Palette → "Agent Flow: Open Agent Flow"
# Keyboard: Cmd+Alt+A (Mac) / Ctrl+Alt+A (Win/Linux)
# Watch JSONL log:
# settings: agentVisualizer.eventLogPath = "/path/to/events.jsonl"
```
