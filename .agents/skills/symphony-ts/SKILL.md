# SKILL: Symphony-TS — Autonomous Issue-to-Agent Orchestration
**Source:** https://github.com/OasAIStudio/symphony-ts
**Domain:** code
**Trigger:** When you want to autonomously dispatch coding agents to Linear issues in isolated workspaces

## Summary
TypeScript port of OpenAI Symphony. Polls Linear for eligible work, creates dedicated workspace per issue, runs coding agent (Codex app-server), exposes operator dashboard via SSE. WORKFLOW.md defines tracker, workspace, agent config.

## Key Patterns
- WORKFLOW.md is the only config: tracker (Linear), workspace root, codex command, port
- Per-issue isolated workspaces prevent cross-contamination
- Operator dashboard via SSE (server-sent events) + JSON API
- Retry, reconciliation, cleanup state visible to operators

## Usage
Use for autonomous ticket-to-PR workflows. Operators focus on work, not agent supervision.

## Code/Template
```bash
npm install -g symphony-ts
cd /path/to/your-repo
export LINEAR_API_KEY=your-token
symphony ./WORKFLOW.md --acknowledge-high-trust-preview --port 4321
```
```yaml
# WORKFLOW.md frontmatter
tracker:
  kind: linear
  api_key: $LINEAR_API_KEY
  project_slug: your-project
workspace:
  root: ~/code/symphony-workspaces
codex:
  command: codex app-server
server:
  port: 4321
```
