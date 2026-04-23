# SKILL: OpenHarness — TypeScript Agent Framework
**Source:** https://github.com/MaxGfeller/open-harness
**Domain:** code
**Trigger:** When building general-purpose AI agents in TypeScript with middleware, sessions, subagents, and React/Vue UI

## Summary
Agent framework based on Vercel AI SDK. Provides Agent, Session, Conversation, composable middleware (compaction, retry, turn-tracking), filesystem/bash tools, subagents, and MCP integration. React + Vue hooks for chat UIs.

## Key Patterns
- Agent: stateless executor; Session: multi-turn with compaction/retry/persistence
- Middleware: withTurnTracking, withCompaction, withRetry — composable via apply()
- Built-in tools: createFsTools, createBashTool (NodeFsProvider, NodeShellProvider)
- Resumable subagent sessions, background runs with separate run/session IDs

## Usage
Use as the base framework when building TypeScript AI coding agents or chat applications.

## Code/Template
```typescript
import { Agent, createFsTools, createBashTool, NodeFsProvider, NodeShellProvider } from "@openharness/core";
import { openai } from "@ai-sdk/openai";

const agent = new Agent({
  name: "dev", model: openai("gpt-5.4"),
  tools: { ...createFsTools(new NodeFsProvider()), ...createBashTool(new NodeShellProvider()) },
  maxSteps: 20,
});

const session = new Session({ agent, contextWindow: 128_000 });
for await (const event of session.send("Refactor the auth module")) {
  if (event.type === "text.delta") process.stdout.write(event.text);
}
```
